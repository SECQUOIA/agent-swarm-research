"""R8_c4: independent recomputation of the Part C4 digest (evidence/campaign4-c4-digest.md).

Standard library only. Reads experiments/v4/runs/partC4/{records.jsonl, jobs.json, cases/*.json,
replay.json} and experiments/v4/c4-references.json directly. It imports no producer code
(summarize_c4, summarize_v4, mechanism_c4, campaign4_c4_digest). For two cross-references the
digest takes from evidence/campaign4-digest.md, it also streams the C2/C3 records
(experiments/v4/runs/partC2, partC3) and reads the C3 cases.

Definitions, implemented here from the protocol (campaign-v4-protocol.md, Amendment 1) and the
runner README:

- solved: status optimal or gaplimit, normal worker exit (returncode 0, no worker_status, status
  not a failure status), primal_check.checked and primal_check.passed, finite primal;
- time: total_seconds + preparation_seconds; SCIP time: scip_solve_seconds (Gurobi:
  solver_runtime_seconds); callback: separation.callback_seconds; SCIP excl. callback: difference
  (floored at 0);
- SGM: exp(mean(log(t + 1))) - 1 over the instances solved (full) or completed with a root bound
  (root) by every compared mode;
- root bound: root_dual if finite; else, for a SCIP run that ended at the root (node limit 1 or one
  node), the final dual bound;
- gap closed: (root(m) - root(baseline)) / (ref - root(baseline)), ref = optimum (case
  known_optimum) or bound (ii) (case reference_bound_ii);
- bound comparison: better if a - b > tol, worse if a - b < -tol, tie otherwise,
  tol = rtol * max(1, |a|, |b|); 'flagged' if either run failed its primal check or conflicts with
  the reference (reference_check.dual_consistent / root_dual_consistent false).

Bound (ii) is recomputed exactly for all 20 instances from the case rows: for each copy i the four
vertex quadratics D_i(x, y, z), (x, z) in {0, 1}^2 (the row is separable and concave in x and z,
which is asserted), give phi_i = min of four parabolas. The Lagrangian dual
h(mu) = sum_i min_{y in [0,1]} (phi_i(y) + mu y) - mu c is evaluated in exact rationals; bisection
on mu gives a lower bound max(h(lo), h(hi)) and an upper bound from a primal point (convex
combination of the minimizers at lo and hi with sum y = c). The stored multiplier is then checked
exactly against the optimality condition S_min(mu) <= c <= S_max(mu), which makes h(mu) the exact
bound (ii). For three instances (n10_s9, n20_s8, n80_s7) bound (ii) is also computed from lower
convex hulls of phi_i on the grid j / 2^16 plus exact pieces (parabola vertices, bitangent points),
minimized by a greedy slope fill under the coupling row.

Usage: python R8_c4.py [--values] [--json OUT] [--cache PICKLE]  (the cache only skips re-reading records.jsonl)
"""
from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction as Q
import hashlib
import json
import math
import re
import statistics
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
V4 = ROOT / "experiments/v4"
RUN = V4 / "runs/partC4"
REF_PATH = V4 / "c4-references.json"
C3RUN = V4 / "runs/partC3"
C2RUN = V4 / "runs/partC2"
EVID = ROOT / "evidence"
FAIL_STATUS = {"process_timeout", "worker_error", "worker_no_output", "worker_output_parse_error"}
SCIP_MODES = ("baseline", "baseline-extra", "frozen-wide", "rowdir-wide")
ALL_MODES = SCIP_MODES + ("gurobi",)
CUT_MODES = ("frozen-wide", "rowdir-wide")
NS = (10, 20, 40, 80)
SEEDS = (5, 6, 7, 8, 9)
HULL_INSTANCES = ("interleaved_path_coupled_n10_s9", "interleaved_path_coupled_n20_s8",
                  "interleaved_path_coupled_n80_s7")


# ----------------------------------------------------------------------------- helpers

def short(name):
    return name.replace("interleaved_path_coupled_", "")


def n_of(name):
    return int(name.split("_n")[1].split("_")[0])


def s_of(name):
    return int(name.rsplit("_s", 1)[1])


def finite(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)


def failed(r):
    return r.get("status") in FAIL_STATUS or bool(r.get("worker_status")) or r.get("returncode", 0) != 0


def solved(r):
    pc = r.get("primal_check") or {}
    return (r is not None and not failed(r) and r.get("status") in ("optimal", "gaplimit")
            and pc.get("checked") is True and pc.get("passed") is True and finite(r.get("primal")))


def seconds(r):
    return r["total_seconds"] + r.get("preparation_seconds", 0.0)


def solver_seconds(r):
    v = r.get("scip_solve_seconds", r.get("solver_runtime_seconds"))
    return v if finite(v) else None


def callback(r):
    return (r.get("separation") or {}).get("callback_seconds", 0.0) or 0.0


def scip_excl(r):
    v = solver_seconds(r)
    return None if v is None else max(0.0, v - callback(r))


def root_bound(r):
    if r is None or failed(r):
        return None
    if finite(r.get("root_dual")):
        return r["root_dual"]
    if (r.get("node_limit") == 1 or r.get("nodes") == 1) and finite(r.get("dual")) and r.get("mode") != "gurobi":
        return r["dual"]
    return None


def completed_root(r):
    return r is not None and not failed(r) and "total_seconds" in r and root_bound(r) is not None


def sgm(values):
    values = [v for v in values if v is not None]
    return math.exp(statistics.fmean(math.log(v + 1.0) for v in values)) - 1.0 if values else None


def flagged(r):
    if (r.get("primal_check") or {}).get("passed") is False:
        return True
    rc = r.get("reference_check") or {}
    return rc.get("dual_consistent") is False or rc.get("root_dual_consistent") is False


def compare(a, b, va, vb, rtol):
    if a is None or b is None or failed(a) or failed(b) or not finite(va) or not finite(vb):
        return "unavailable"
    if flagged(a) or flagged(b):
        return "flagged"
    tol = rtol * max(1.0, abs(va), abs(vb))
    d = va - vb
    return "better" if d > tol else "worse" if d < -tol else "tie"


def med(xs):
    xs = [x for x in xs if x is not None]
    return statistics.median(xs) if xs else None


def mmm(xs):
    xs = [x for x in xs if x is not None]
    return (statistics.median(xs), min(xs), max(xs)) if xs else (None, None, None)


def hexq(h):
    return Q(float.fromhex(h))


def iso(ts):
    return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ")


# ----------------------------------------------------------------------------- loading

def stream_c4():
    """Stream records.jsonl; keep a slim copy of each record and per-cut facts."""
    slim, cutinfo, sigs, cutproblems = [], {}, {}, Counter()
    with open(RUN / "records.jsonl") as fh:
        for line in fh:
            r = json.loads(line)
            cuts = r.pop("cuts", None)
            om = r.pop("original_model", None)
            r.pop("model_metadata", None)
            r.pop("original_values", None)
            ns = r.pop("native_statistics", None)
            if ns is not None:
                seps = ns.get("separators") or {}
                r["_ns"] = {"status": ns.get("original_variable_status") or {},
                            "seps": {k: (seps.get(k) or {}).get("Calls") for k in ("eccuts", "interminor", "minor")},
                            "quad": (ns.get("nlhdlrs") or {}).get("quadratic") or {}}
            r["_ncuts"] = len(cuts) if isinstance(cuts, list) else None
            if cuts and r["mode"] in CUT_MODES:
                info, sig = analyse_cuts(r, cuts, om, cutproblems)
                cutinfo[r["run_id"]] = info
                sigs[r["run_id"]] = sig
            slim.append(r)
    return slim, cutinfo, sigs, cutproblems


def analyse_cuts(r, cuts, om, problems):
    names = om["var_names"]
    ncols = len(names)
    out = []
    h = hashlib.sha256()
    for c in cuts:
        b = c["block"]
        xv, yv, zv = c["variables"]
        if not (names[xv].startswith("x_") and names[yv].startswith("y_") and names[zv].startswith("z_")):
            problems["block variables not x_, y_, z_"] += 1
        if len(c["signed_sides"]) != 1:
            problems["signed_sides != 1"] += 1
        side = c["signed_sides"][0]
        aff = {int(s[1:]): Q(v) for s, v in side["affine_terms"]}
        tcols = [k for k, v in aff.items() if k not in (xv, yv, zv)]
        if len(tcols) != 1 or aff[tcols[0]] != -1 or not names[tcols[0]].startswith("t_"):
            problems["t column not identified"] += 1
        tv = tcols[0]
        d = [hexq(x) for x in c["support_witness"]["model"]["coefficients"]]
        if [float(x) for x in d] != list(c["coefficients"]):
            problems["coefficients != support_witness hex"] += 1
        a, lam = d[:3], d[3]
        affv = [aff.get(v, Q(0)) for v in (xv, yv, zv)]
        if all(a[j] == lam * affv[j] for j in range(3)):
            cls = "row"
        elif all(x == 0 for x in a):
            cls = "remainder"
        else:
            cls = "LP"
        ex = c["row_certificate"]["exact"]
        E = ex["coefficients"]
        X = c["row_certificate"]["exported"]["coefficients"]
        if len(E) != ncols or len(X) != ncols:
            problems["coefficient vector length"] += 1
        block = {xv, yv, zv, tv}
        ec = {v: Q(E[v]) for v in block}
        if any(ec[v] != a[j] - lam * affv[j] for j, v in enumerate((xv, yv, zv))):
            problems["exact x/y/z coef != a - lambda aff"] += 1
        if ec[tv] != lam:
            problems["exact t coef != lambda"] += 1
        if not ec[tv] > 0:
            problems["t coefficient not positive"] += 1
        if any(E[k] != "0" for k in range(ncols) if k not in block) or \
                any(X[k] != 0.0 for k in range(ncols) if k not in block):
            problems["nonzero outside block"] += 1
        ar = c["actual_row"]
        m = {e["source"]: e["transformed"] for e in ar["source_to_transformed"]}
        stored_cols = set(ar["columns"])
        allowed = {m.get(f"v{v}") for v in block}
        if not stored_cols <= allowed:
            problems["stored row outside block"] += 1
        ykey = m.get(f"v{yv}")
        ynz = [a[1] - lam * affv[1] != 0, ec[yv] != 0, X[yv] != 0.0,
               ykey in ar["columns"] and ar["columns"][ykey] != 0.0]
        if len(set(ynz)) != 1:
            problems["y zero/nonzero inconsistent across 4 places"] += 1
        pat = "".join(ch for ch, v in zip("xyz", (xv, yv, zv)) if ec[v] != 0)
        slope = float(-ec[yv] / ec[tv])
        out.append((b, cls, pat, ec[yv] != 0, slope, (Q(ex["compensated_rhs"]) / ec[tv]) if cls == "row" else None))
        h.update(json.dumps([b, E, ex["compensated_rhs"], ex["eliminated_rhs"]]).encode())
    return out, h.hexdigest()


def load_jobs():
    jobs = json.load(open(RUN / "jobs.json"))["jobs"]
    return [(j["phase"], ru["mode"], j["name"], ru["run_id"]) for j in jobs for ru in j["runs"]]


def load_cases(d):
    return {json.load(open(p))["name"]: json.load(open(p)) for p in sorted((d / "cases").glob("*.json"))}


def stream_other(path, wanted_modes):
    out = []
    pat = re.compile(r'"mode": "([^"]+)"')
    with open(path) as fh:
        for line in fh:
            m = pat.search(line[:400])
            if not m or m.group(1) not in wanted_modes:
                continue
            r = json.loads(line)
            for k in ("cuts", "original_model", "model_metadata", "original_values", "native_statistics"):
                r.pop(k, None)
            out.append(r)
    return out


# ----------------------------------------------------------------------------- bound (ii)

def copy_pieces(case, i):
    """Vertex quadratics (A, B, C) of copy i (1-based) from the case row; asserts the structure."""
    row = case["model"]["rows"][i]
    base = 4 * (i - 1)
    xs, ys, zs, ts = base, base + 1, base + 2, base + 3
    lin = {int(k): hexq(v["binary64"]) for k, v in row["lin"].items()}
    assert set(lin) <= {xs, ys, zs, ts} and lin[ts] == -1, ("lin", i)
    quad = defaultdict(Q)
    for j, k, v in row["quad"]:
        quad[(min(j, k), max(j, k))] += hexq(v["binary64"])
    assert set(quad) <= {(xs, xs), (ys, ys), (zs, zs), (xs, ys), (ys, zs)}, ("quad keys", i)
    assert quad[(xs, xs)] <= 0 and quad[(zs, zs)] <= 0, ("concavity", i)
    assert row["lb"]["binary64"] == "-inf" and row["nl"] is None
    ub = hexq(row["ub"]["binary64"])
    pieces = {}
    for x in (0, 1):
        for z in (0, 1):
            A = quad[(ys, ys)]
            B = lin.get(ys, Q(0)) + quad[(xs, ys)] * x + quad[(ys, zs)] * z
            C = lin.get(xs, Q(0)) * x + lin.get(zs, Q(0)) * z + quad[(xs, xs)] * x * x + quad[(zs, zs)] * z * z - ub
            pieces[(x, z)] = (A, B, C)
    return pieces


def phi(pieces, y):
    return min(A * y * y + B * y + C for A, B, C in pieces)


def copy_min(pieces, mu):
    best, ys = None, set()
    for A, B, C in pieces:
        Bp = B + mu
        y = min(max(-Bp / (2 * A), Q(0)), Q(1))
        v = A * y * y + Bp * y + C
        if best is None or v < best:
            best, ys = v, {y}
        elif v == best:
            ys.add(y)
    return best, ys


def lagrange(allp, c, mu):
    tot, smin, smax, ties, mins = Q(0), Q(0), Q(0), 0, []
    for p in allp:
        v, ys = copy_min(p, mu)
        tot += v
        smin += min(ys)
        smax += max(ys)
        ties += len(ys) > 1
        mins.append(ys)
    return tot - mu * c, smin, smax, ties, mins


def bound_ii_exact(allp, c, steps=110):
    lo, hi = Q(0), Q(4)
    h0, smin0, _, _, _ = lagrange(allp, c, lo)
    assert smin0 > c, "coupling row does not bind at mu = 0"
    assert lagrange(allp, c, hi)[2] <= c
    exact = None
    for _ in range(steps):
        mid = (lo + hi) / 2
        _, smin, smax, _, _ = lagrange(allp, c, mid)
        if smin > c:
            lo = mid
        elif smax < c:
            hi = mid
        else:
            exact = mid
            break
    if exact is not None:
        hx = lagrange(allp, c, exact)[0]
        return {"lo": exact, "hi": exact, "L": hx, "U": hx, "exact_mid": exact}
    hlo, _, _, _, mlo = lagrange(allp, c, lo)
    hhi, _, _, _, mhi = lagrange(allp, c, hi)
    L = max(hlo, hhi)
    ylo = [min(s) for s in mlo]
    yhi = [max(s) for s in mhi]
    Slo, Shi = sum(ylo), sum(yhi)
    th = (c - Shi) / (Slo - Shi)
    assert 0 <= th <= 1
    U = sum(th * phi(p, a) + (1 - th) * phi(p, b) for p, a, b in zip(allp, ylo, yhi))
    return {"lo": lo, "hi": hi, "L": L, "U": U, "exact_mid": exact}


def exact_multiplier(allp, c, res):
    """Exact optimal multiplier: candidates from the structure inside the final bracket, each checked
    against S_min(mu) <= c <= S_max(mu)."""
    lo, hi = res["lo"], res["hi"]
    cands = [res["exact_mid"]] if res["exact_mid"] is not None else []
    mid = (lo + hi) / 2
    num_, den_ = Q(0), Q(0)
    for p in allp:
        v, ys = copy_min(p, mid)
        A, B, C = next(q for q in p if min(max(-(q[1] + mid) / (2 * q[0]), Q(0)), Q(1)) in ys
                       and q[0] * min(ys) ** 2 + (q[1] + mid) * min(ys) + q[2] == v)
        y = -(B + mid) / (2 * A)
        if 0 < y < 1:
            num_ += -B / (2 * A)
            den_ += 1 / (2 * A)
        else:
            num_ += min(max(y, Q(0)), Q(1))
    if den_:
        cands.append((num_ - c) / den_)
    for p in allp:
        for i1, (A1, B1, C1) in enumerate(p):
            for (A2, B2, C2) in p[i1 + 1:]:
                if A1 == A2 and B1 != B2:
                    mu = (4 * A1 * (C1 - C2) / (B1 - B2) - B1 - B2) / 2
                    if lo <= mu <= hi:
                        cands.append(mu)
    for mu in cands:
        h, smin, smax, ties, _ = lagrange(allp, c, mu)
        if smin <= c <= smax:
            return mu, h, smin, smax, ties
    return None


def hull_bound(allp, c, G=16):
    N = 2 ** G
    grid = [j / N for j in range(N + 1)]
    segs, base_val, base_sum = [], 0.0, 0.0
    for pieces in allp:
        extra = set()
        me = []
        for A, B, C in pieces:
            m = -B / (2 * A)
            e = C - A * m * m
            me.append((A, m, e))
            if 0 <= m <= 1:
                extra.add(float(m))
        for (A1, m1, e1) in me:
            for (A2, m2, e2) in me:
                if m1 != m2 and A1 == A2:
                    d = (e2 - e1) / (2 * A1 * (m2 - m1))
                    for y in (m1 + d, m2 + d):
                        if 0 <= y <= 1:
                            extra.add(float(y))
        P = [(float(A), float(B), float(C)) for A, B, C in pieces]
        ys = sorted(set(grid) | extra)
        pts = [(y, min(A * y * y + B * y + C for A, B, C in P)) for y in ys]
        hull = []
        for p in pts:
            while len(hull) >= 2 and ((hull[-1][0] - hull[-2][0]) * (p[1] - hull[-2][1])
                                      - (hull[-1][1] - hull[-2][1]) * (p[0] - hull[-2][0])) <= 0:
                hull.pop()
            hull.append(p)
        k = min(range(len(hull)), key=lambda j: (hull[j][1], hull[j][0]))
        base_val += hull[k][1]
        base_sum += hull[k][0]
        for j in range(k, 0, -1):
            (y0, f0), (y1, f1) = hull[j - 1], hull[j]
            segs.append(((f0 - f1) / (y1 - y0), y1 - y0))
    need = base_sum - float(c)
    assert need > 0
    val = base_val
    for cost, length in sorted(segs):
        take = min(length, need)
        val += cost * take
        need -= take
        if need <= 0:
            break
    return val, len(allp) * (1.0 / N) ** 2 / 2


# ----------------------------------------------------------------------------- main analysis

def main():
    want_values = "--values" in sys.argv
    V = {}           # recomputed values, printed with --values
    problems = []    # hard inconsistencies found in the data

    jobs = load_jobs()
    cases = load_cases(RUN)
    REF = json.load(open(REF_PATH))
    refs = {e["name"]: e for e in REF["instances"]}
    RP = json.load(open(RUN / "replay.json"))
    cache = sys.argv[sys.argv.index("--cache") + 1] if "--cache" in sys.argv else None
    if cache and Path(cache).exists() and Path(cache).stat().st_size > 0:
        import pickle
        recs, cutinfo, sigs, cutproblems = pickle.loads(Path(cache).read_bytes())
    else:
        recs, cutinfo, sigs, cutproblems = stream_c4()
        if cache:
            import pickle
            Path(cache).write_bytes(pickle.dumps((recs, cutinfo, sigs, cutproblems)))
    names = sorted(cases, key=lambda nm: (n_of(nm), s_of(nm)))
    assert len(names) == 20

    # ---- checks: coverage, failures, case/REF agreement
    idx = {}
    for r in recs:
        k = (r["phase"], r["mode"], r["name"])
        if k in idx:
            problems.append(("duplicate record", k))
        idx[k] = r
    sched = {j[3] for j in jobs}
    recorded = [r["run_id"] for r in recs]
    V["scheduled"], V["recorded"] = len(sched), len(recorded)
    V["missing"] = sorted(sched - set(recorded))
    V["unscheduled"] = sorted(set(recorded) - sched)
    V["dup_run_ids"] = len(recorded) - len(set(recorded))
    V["returncode_nonzero"] = sum(r.get("returncode", 0) != 0 for r in recs)
    V["worker_status"] = sum(bool(r.get("worker_status")) for r in recs)
    V["failed"] = sum(map(failed, recs))
    V["primal_checked"] = sum((r.get("primal_check") or {}).get("checked") is True for r in recs)
    V["primal_passed"] = sum((r.get("primal_check") or {}).get("passed") is True for r in recs)
    V["max_scaled_violation"] = max((r.get("primal_check") or {}).get("max_scaled_violation", 0) for r in recs)
    V["flagged"] = sum(map(flagged, recs))
    V["witness_checks_passed"] = sum((r.get("reference_witness_check") or {}).get("passed") is True for r in recs)
    V["classifier_errors"] = sum((r.get("row_binding_rejection_causes") or {}).get("classifier_errors", 0) or 0 for r in recs)
    V["case_ref_equal"] = sum(cases[n]["known_optimum"] == refs[n]["optimum"]
                              and cases[n]["reference_bound_ii"] == refs[n]["bound_ii"]["value"]
                              and cases[n]["known_optimum_exact"] == refs[n]["optimum_exact"] for n in names)
    V["refcheck_value_equals_opt"] = sum((r.get("reference_check") or {}).get("value") == cases[r["name"]]["known_optimum"]
                                         for r in recs)
    opt = {n: cases[n]["known_optimum"] for n in names}
    optx = {n: Q(refs[n]["optimum_exact"]) for n in names}
    b2 = {n: cases[n]["reference_bound_ii"] for n in names}
    for n in names:
        if float(optx[n]) != opt[n]:
            problems.append(("known_optimum != float(optimum_exact)", n))

    # ---- (a) replay
    a = {}
    a["passed"], a["archived_passed"] = RP["passed"], RP["archived_passed"]
    a["records"], a["bound_runs"], a["admitted_runs"] = RP["records"], RP["bound_runs"], RP["admitted_runs"]
    a["cuts"], a["replayed_cuts"] = RP["cuts"], RP["replayed_cuts"]
    a["failed_runs"] = sum(not x["passed"] for x in RP["runs"])
    a["missing_cut_logs"] = RP["missing_cut_logs"]
    a["coverage"] = RP["v4"]["coverage"]
    a["config"] = (len(RP["v4"]["config_failures"]), RP["v4"]["config_checked_runs"])
    a["gurobi"] = (len(RP["v4"]["gurobi_failures"]), RP["v4"]["gurobi_checked_runs"])
    om = RP["omitted_runs"]
    a["omitted"] = (len(om), dict(Counter(x["status"] for x in om)), sum(x["cuts"] for x in om),
                    all("__gurobi" in x["run_id"] for x in om))
    a["source_files_verified"] = RP["source_files_verified"]
    a["replay_seconds"], a["wrapper_seconds"] = RP["replay_seconds"], RP["wrapper_seconds"]
    a["replay_sha"], a["wrapper_sha"] = RP["replay_source_sha256"], RP["wrapper_source_sha256"]
    a["sha_replay_v4.py"] = hashlib.sha256((V4 / "replay_v4.py").read_bytes()).hexdigest()
    per_mode_phase = Counter()
    for x in RP["runs"]:
        r = next(rr for rr in recs if rr["run_id"] == x["run_id"])
        per_mode_phase[(r["mode"], r["phase"])] += x["replayed_cuts"]
    a["replayed_by_mode_phase"] = dict(per_mode_phase)
    tc = RP["v4"]["tamper_controls_by_mode"]
    a["tamper"] = {m: (tc[m]["run_id"], tc[m]["cuts_in_record"], tc[m]["untampered_first_cut_passed"],
                       sum(tc[m]["rejections"].values()), len(tc[m]["rejections"])) for m in tc}
    a["tamper_part"] = (sum(RP["tamper_rejections"].values()), len(RP["tamper_rejections"]))
    a["tamper_cover"] = RP["v4"]["tamper_controls_cover_all_cut_modes"]
    a["replay_mtime"] = datetime.fromtimestamp((RUN / "replay.json").stat().st_mtime, timezone.utc).strftime("%H:%M:%SZ")
    log = (V4 / "runs/replay-partC4.log").read_text().strip().splitlines()
    a["log_lines"] = len(log)
    a["replay_start_est"] = datetime.fromtimestamp((RUN / "replay.json").stat().st_mtime - RP["wrapper_seconds"], timezone.utc).strftime("%H:%M:%SZ")
    # identical cut lists root vs full
    same = {m: sum(sigs.get(idx[("root", m, n)]["run_id"]) == sigs.get(idx[("full", m, n)]["run_id"])
                   and sigs.get(idx[("root", m, n)]["run_id"]) is not None for n in names) for m in CUT_MODES}
    a["identical_cut_lists"] = same
    rtxt = (EVID / "campaign4-replay.md").read_text()
    a["replay_md_has"] = {s: s in rtxt for s in ("56,771 replayed cuts", "56,771 = **95,267**", "56,771 = 64,269",
                                                 "21:03:44Z to 21:24:37Z")}
    V["a"] = a

    # ---- (b) root runs
    b = {}
    R = {m: {n: idx.get(("root", m, n)) for n in names} for m in SCIP_MODES}
    F = {m: {n: idx.get(("full", m, n)) for n in names} for m in ALL_MODES}
    b["status"] = {m: dict(Counter(R[m][n]["status"] for n in names)) for m in SCIP_MODES}
    b["root_gaplimit"] = {m: [(short(n), R[m][n]["nodes"]) for n in names if R[m][n]["status"] == "gaplimit"] for m in SCIP_MODES}
    b["time"] = {m: mmm([seconds(R[m][n]) for n in names]) for m in SCIP_MODES}
    rb = {m: {n: root_bound(R[m][n]) for n in names} for m in SCIP_MODES}
    b["n10_s6"] = {"fw": rb["frozen-wide"]["interleaved_path_coupled_n10_s6"],
                   "rw": rb["rowdir-wide"]["interleaved_path_coupled_n10_s6"],
                   "inc_fw": R["frozen-wide"]["interleaved_path_coupled_n10_s6"]["primal"],
                   "inc_rw": R["rowdir-wide"]["interleaved_path_coupled_n10_s6"]["primal"],
                   "opt": opt["interleaved_path_coupled_n10_s6"], "b2": b2["interleaved_path_coupled_n10_s6"]}
    b["rb_table"] = {m: {k: mmm([rb[m][n] for n in names if n_of(n) == k]) for k in NS} for m in SCIP_MODES}
    b["opt_table"] = {k: mmm([opt[n] for n in names if n_of(n) == k]) for k in NS}
    b["better_than_base"] = {m: {rt: Counter(compare(R[m][n], R["baseline"][n], rb[m][n], rb["baseline"][n], rt)
                                             for n in names) for rt in (1e-4, 1e-6)}
                             for m in ("baseline-extra", "frozen-wide", "rowdir-wide")}
    gaps = {}
    for label, ref in (("opt", opt), ("b2", b2)):
        gaps[label] = {}
        for m in ("baseline-extra", "frozen-wide", "rowdir-wide"):
            g = {}
            for n in names:
                base = rb["baseline"][n]
                if finite(rb[m][n]) and finite(base) and ref[n] - base > 0:
                    g[n] = (rb[m][n] - base) / (ref[n] - base)
            gaps[label][m] = g
    b["gap"] = {label: {m: {**{k: mmm([g[n] for n in g if n_of(n) == k]) for k in NS},
                            "all": mmm(list(g.values())),
                            "argmin": short(min(g, key=g.get)), "argmax": short(max(g, key=g.get)),
                            "count": len(g)}
                        for m, g in gm.items()} for label, gm in gaps.items()}
    b["gap_differs"] = sorted(short(n) for n in names
                              if any(gaps["opt"][m].get(n) != gaps["b2"][m].get(n) for m in gaps["opt"]))
    diff = {m: {n: rb[m][n] - b2[n] for n in names} for m in SCIP_MODES}
    b["minus_b2"] = {m: {"min": min(d.values()), "argmin": short(min(d, key=d.get)),
                         "max": max(d.values()), "argmax": short(max(d, key=d.get)),
                         **{k: med([d[n] for n in names if n_of(n) == k]) for k in NS}}
                     for m, d in diff.items()}
    b["root_above_b2"] = sum(rb[m][n] > b2[n] for m in SCIP_MODES for n in names)
    b["root_above_opt"] = sum(rb[m][n] > float(optx[n]) for m in SCIP_MODES for n in names)
    b["rw_n80_range"] = (min(diff["rowdir-wide"][n] for n in names if n_of(n) == 80),
                         max(diff["rowdir-wide"][n] for n in names if n_of(n) == 80))
    # full-run root bounds
    def rd(r):
        return r.get("root_dual") if finite(r.get("root_dual")) else None
    differ = {}
    for m in SCIP_MODES:
        lst = []
        for n in names:
            x, y = rd(R[m][n]), rd(F[m][n])
            if x != y:
                lst.append((short(n), x, y))
        differ[m] = lst
    b["root_dual_differs"] = {m: len(v) for m, v in differ.items()}
    b["root_dual_differs_list"] = differ
    b["differ_full_higher"] = all(y > x for m in SCIP_MODES for (_, x, y) in differ[m] if x is not None and y is not None)
    b["differ_full_fixed"] = all(F[m]["interleaved_path_coupled_" + s]["_ns"]["status"].get("FIXED", 0) > 0
                                 for m in SCIP_MODES for (s, _, _) in differ[m])
    b["root_runs_fixed"] = sum(R[m][n]["_ns"]["status"].get("FIXED", 0) > 0 for m in SCIP_MODES for n in names)
    b["full_runs_fixed"] = sum(F[m][n]["_ns"]["status"].get("FIXED", 0) > 0 for m in SCIP_MODES for n in names)
    b["fixed_but_same_root_dual"] = [(m, short(n)) for m in SCIP_MODES for n in names
                                     if F[m][n]["_ns"]["status"].get("FIXED", 0) > 0
                                     and short(n) not in {s for s, _, _ in differ[m]}]
    b["rw_n40_s8"] = (rd(R["rowdir-wide"]["interleaved_path_coupled_n40_s8"]),
                      rd(F["rowdir-wide"]["interleaved_path_coupled_n40_s8"]))
    above = []
    for m in SCIP_MODES:
        for n in names:
            r = F[m][n]
            v = root_bound(r)
            if v is not None and v > b2[n]:
                above.append((m, short(n), r["status"], r["nodes"], v - b2[n], v < float(optx[n]),
                              float(optx[n] - Q(b2[n])), r["_ns"]["status"].get("FIXED", 0) > 0,
                              "root_dual" if finite(r.get("root_dual")) else "dual"))
    b["full_root_above_b2"] = above
    allscip = [r for r in recs if r["mode"] != "gurobi"]
    b["scip_dual_above_optx"] = sum(finite(r["dual"]) and Q(r["dual"]) > optx[r["name"]] for r in allscip)
    V["b"] = b

    # ---- (c) full runs
    c = {}
    c["solved"] = {m: sum(solved(F[m][n]) for n in names) for m in ALL_MODES}
    c["status"] = {m: dict(Counter(F[m][n]["status"] for n in names)) for m in ALL_MODES}
    c["solved_list"] = {m: [short(n) for n in names if solved(F[m][n])] for m in ALL_MODES}
    c["time_solved"] = {m: mmm([seconds(F[m][n]) for n in names if solved(F[m][n])]) for m in ALL_MODES}
    c["nodes_all"] = {m: med([F[m][n]["nodes"] for n in names]) for m in ALL_MODES}
    c["one_node"] = {m: [(short(n), F[m][n]["status"]) for n in names if solved(F[m][n]) and F[m][n]["nodes"] == 1]
                     for m in ALL_MODES}
    common6 = [n for n in names if all(solved(F[m][n]) for m in ALL_MODES)]
    c["common6"] = [short(n) for n in common6]
    c["sgm6"] = {m: sgm([seconds(F[m][n]) for n in common6]) for m in ALL_MODES}
    c["sgm6_solver"] = {m: sgm([solver_seconds(F[m][n]) for n in common6]) for m in ALL_MODES}
    c["sgm6_excl"] = {m: sgm([scip_excl(F[m][n]) for n in common6]) for m in CUT_MODES}
    c["sgm6_cb"] = {m: sgm([callback(F[m][n]) for n in common6]) for m in CUT_MODES}
    c["nodes6"] = {m: med([F[m][n]["nodes"] for n in common6]) for m in ALL_MODES}
    ratios = {}
    for m in ALL_MODES:
        if m == "baseline":
            continue
        rs = [seconds(F[m][n]) / max(seconds(F["baseline"][n]), 1e-9) for n in names
              if solved(F[m][n]) and solved(F["baseline"][n])]
        ratios[m] = (statistics.median(rs), len(rs), sum(x < 1 for x in rs))
    c["ratio"] = ratios
    common10 = [n for n in names if all(solved(F[m][n]) for m in SCIP_MODES)]
    c["common10"] = [short(n) for n in common10]
    c["sgm10"] = {m: sgm([seconds(F[m][n]) for n in common10]) for m in SCIP_MODES}
    c["nodes10"] = {m: med([F[m][n]["nodes"] for n in common10]) for m in SCIP_MODES}
    c["sgm20"] = {m: sgm([seconds(F[m][n]) for n in names]) for m in CUT_MODES}
    c["n80_range"] = {m: (min(seconds(F[m][n]) for n in names if n_of(n) == 80),
                          max(seconds(F[m][n]) for n in names if n_of(n) == 80)) for m in CUT_MODES}
    cmpf = {}
    for m in ("baseline-extra", "frozen-wide", "rowdir-wide", "gurobi"):
        cmpf[m] = {}
        for rt in (1e-4, 1e-6):
            outc = {n: compare(F[m][n], F["baseline"][n], F[m][n]["dual"], F["baseline"][n]["dual"], rt) for n in names}
            cmpf[m][rt] = (dict(Counter(outc.values())), {k: sorted(short(n) for n in names if outc[n] == k)
                                                           for k in set(outc.values())})
    c["cmp"] = cmpf
    c["rw_worse_1e6_on_common10"] = sorted(short(n) for n in common10
                                           if compare(F["rowdir-wide"][n], F["baseline"][n], F["rowdir-wide"][n]["dual"],
                                                      F["baseline"][n]["dual"], 1e-6) == "worse")
    c["rw_common10_status"] = dict(Counter(F["rowdir-wide"][n]["status"] for n in common10))
    c["rw_common10_detail"] = [(short(n), F["rowdir-wide"][n]["status"], F["rowdir-wide"][n]["dual"] - F["baseline"][n]["dual"])
                               for n in common10]
    dmo = {m: [float(Q(F[m][n]["dual"]) - optx[n]) for n in names if solved(F[m][n])] for m in ALL_MODES}
    c["dual_minus_opt"] = {m: mmm(v) for m, v in dmo.items()}
    c["fw_n80_s5"] = (F["frozen-wide"]["interleaved_path_coupled_n80_s5"]["dual"], float(optx["interleaved_path_coupled_n80_s5"]))
    inc = [(float(Q(r["primal"]) - optx[r["name"]]), r["mode"], r["phase"], short(r["name"])) for r in recs
           if finite(r.get("primal"))]
    c["scip_inc_min"] = min(x for x in inc if x[1] != "gurobi")
    c["gurobi_inc_min"] = min(x for x in inc if x[1] == "gurobi")
    c["incumbents"] = len(inc)
    g = {}
    for n in names:
        r = F["gurobi"][n]
        g[short(n)] = {"status": r["status"], "gs": r["gurobi_status_name"], "dmo": float(Q(r["dual"]) - optx[n]),
                       "dual_eq_primal": r["dual"] == r["primal"], "mip_gap": r["mip_gap"], "time": seconds(r),
                       "runtime": r["solver_runtime_seconds"], "nodes": r["nodes"],
                       "params": r["gurobi_params"], "version": r["gurobi_version"],
                       "tl_eq_budget": r["gurobi_params"]["TimeLimit"] == r["remaining_solve_budget"]}
    c["gurobi"] = g
    V["c"] = c

    # ---- (d) funnel, caps, time decomposition
    d = {}
    fun = {}
    for ph in ("root", "full"):
        for m in CUT_MODES:
            rows = [idx[(ph, m, n)] for n in names]
            S = [r["separation"] for r in rows]
            t = {k: sum(s.get(k, 0) or 0 for s in S) for k in
                 ("calls", "certification_calls", "certification_failures", "row_rounding_rejections",
                  "row_binding_rejections", "cuts", "candidate_lps", "exchange_samples", "sampling_failures",
                  "repeat_skips", "selection_skips")}
            t["certified"] = t["certification_calls"] - t["certification_failures"]
            t["below"] = t["certified"] - t["row_rounding_rejections"] - t["row_binding_rejections"] - t["cuts"]
            t["binding_runs"] = sum(bool(s.get("row_binding_rejections")) for s in S)
            causes, vst = Counter(), Counter()
            for r in rows:
                causes.update(r["row_binding_rejection_causes"].get("causes", {}))
                vst.update(r["row_binding_rejection_causes"].get("variable_statuses", {}))
            t["causes"], t["varstatus"] = dict(causes), dict(vst)
            t["share"] = t["row_binding_rejections"] / (t["row_binding_rejections"] + t["cuts"])
            # caps
            cfg = [r["config"] for r in rows]
            ok_cfg = all(cf["max_cuts"] == 16 * n_of(r["name"]) and cf["max_support_calls"] == 40 * n_of(r["name"])
                         and cf["max_cuts_per_round"] == 4 * n_of(r["name"]) and cf["max_rounds"] == 10
                         and cf["max_blocks"] == n_of(r["name"]) and cf["max_separation_seconds"] == 60.0
                         and cf["separation_budget_fraction"] == 0.5
                         and cf["row_directions"] is (m == "rowdir-wide") for cf, r in zip(cfg, rows))
            t["config_ok"] = ok_cfg
            t["cut_cap_reached"] = sum(s["cuts"] == cf["max_cuts"] for s, cf in zip(S, cfg))
            t["support_cap_reached"] = sum(s["certification_calls"] >= cf["max_support_calls"] for s, cf in zip(S, cfg))
            t["support_ratio"] = (min(s["certification_calls"] / cf["max_support_calls"] for s, cf in zip(S, cfg)),
                                  max(s["certification_calls"] / cf["max_support_calls"] for s, cf in zip(S, cfg)))
            t["round_cap_reached"] = sum(s["calls"] >= cf["max_rounds"] for s, cf in zip(S, cfg))
            t["calls_range"] = (min(s["calls"] for s in S), max(s["calls"] for s in S))
            budgets = [min(cf["max_separation_seconds"], cf["separation_budget_fraction"] * r["time_limit"])
                       for cf, r in zip(cfg, rows)]
            t["budget_values"] = sorted(set(budgets))
            t["time_cap_reached"] = sum(s["callback_seconds"] >= bu for s, bu in zip(S, budgets))
            t["cb_range"] = (min(s["callback_seconds"] for s in S), max(s["callback_seconds"] for s in S))
            t["budget_exhausted"] = sum(bool(s.get("budget_exhausted")) for s in S)
            t["discovery_incomplete"] = sum(bool(s.get("discovery_incomplete")) for s in S)
            t["cut_log_ok"] = sum(r["cut_log_complete"] is True and r["_ncuts"] == r["separation"]["cuts"] for r in rows)
            fun[(ph, m)] = t
    d["funnel"] = fun
    keys_cmp = [k for k in fun[("root", "frozen-wide")] if k not in ("cb_range", "budget_values", "time_cap_reached")]
    d["funnel_same_phases"] = {m: all(fun[("root", m)][k] == fun[("full", m)][k] for k in keys_cmp) for m in CUT_MODES}
    td = {}
    for ph in ("root", "full"):
        for m in ("frozen-wide", "rowdir-wide", "baseline-extra"):
            if ph == "root":
                pairs = [n for n in names if completed_root(R[m][n]) and completed_root(R["baseline"][n])]
                A_, B_ = R, R
            else:
                pairs = [n for n in names if solved(F[m][n]) and solved(F["baseline"][n])]
                A_, B_ = F, F
            td[(ph, m)] = {
                "pairs": len(pairs),
                "sgm_total": sgm([seconds(A_[m][n]) for n in pairs]),
                "sgm_excl": sgm([scip_excl(A_[m][n]) for n in pairs]),
                "sgm_cb": sgm([callback(A_[m][n]) for n in pairs]),
                "base_total": sgm([seconds(B_["baseline"][n]) for n in pairs]),
                "base_scip": sgm([solver_seconds(B_["baseline"][n]) for n in pairs]),
                "med_excl_ratio": statistics.median(scip_excl(A_[m][n]) / solver_seconds(B_["baseline"][n]) for n in pairs),
                "med_total_ratio": statistics.median(seconds(A_[m][n]) / seconds(B_["baseline"][n]) for n in pairs)}
    d["td"] = td
    sums = {}
    for ph in ("root", "full"):
        for m in CUT_MODES:
            rows = [idx[(ph, m, n)] for n in names]
            S = [r["separation"] for r in rows]
            s = {"charged": sum(map(seconds, rows)), "scip": sum(map(solver_seconds, rows)),
                 "excl": sum(map(scip_excl, rows)), "cb": sum(map(callback, rows))}
            for k in ("discovery_seconds", "candidate_seconds", "certification_seconds", "row_seconds"):
                s[k] = sum(x[k] for x in S)
            s["pct"] = 100 * s["cb"] / s["charged"]
            s["uncovered"] = s["cb"] - s["discovery_seconds"] - s["candidate_seconds"] - s["certification_seconds"] - s["row_seconds"]
            sums[(ph, m)] = s
    d["sums"] = sums
    load = {}
    for ph, modes in (("root", SCIP_MODES), ("full", ALL_MODES)):
        for m in modes:
            load[(ph, m)] = statistics.fmean(idx[(ph, m, n)]["load_start"][0] for n in names)
    d["load"] = load
    d["load_range"] = {ph: (min(v for (p, _), v in load.items() if p == ph), max(v for (p, _), v in load.items() if p == ph))
                       for ph in ("root", "full")}
    d["window"] = (min(r["started_utc"] for r in recs), max(r["ended_utc"] for r in recs))
    V["d"] = d

    # ---- (e) reference values and exact bound (ii)
    e = {}
    omb = {n: refs[n]["optimum_minus_bound_ii"] for n in names}
    e["omb_min"], e["omb_med"], e["omb_max"] = min(omb.values()), statistics.median(omb.values()), max(omb.values())
    e["omb_argmax"] = short(max(omb, key=omb.get))
    e["zero"] = [short(n) for n in names if omb[n] < 2.4e-59]
    e["zero_fc0_and_float_equal"] = all(refs[n]["bound_ii"]["fractional_copies"] == 0 and refs[n]["bound_ii"]["value"] == refs[n]["optimum"]
                                        for n in names if omb[n] < 2.4e-59)
    e["pos"] = {short(n): (omb[n], refs[n]["bound_ii"]["fractional_copies"]) for n in names if omb[n] >= 2.4e-59}
    e["c"] = {short(n): refs[n]["coupling"]["c"] for n in names}
    cq = {n: Q(refs[n]["coupling"]["c"]) for n in names}
    e["c_min"] = short(min(names, key=lambda n: cq[n])), str(min(cq.values()))
    e["c_max"] = short(max(names, key=lambda n: cq[n])), str(max(cq.values()))
    e["c_ratio"] = (float(min(cq[n] / Q(refs[n]["coupling"]["sum_y_star"]) for n in names)),
                    float(max(cq[n] / Q(refs[n]["coupling"]["sum_y_star"]) for n in names)))
    e["sumy"] = {short(n): refs[n]["coupling"]["sum_y_star"] for n in ("interleaved_path_coupled_n10_s5", "interleaved_path_coupled_n80_s5")}
    e["binds"] = sum(refs[n]["coupling"]["binds"] is True for n in names)
    e["yexact_sum_c"] = sum(sum(Q(y) for y in refs[n]["y_exact"]) == cq[n] for n in names)
    mu = {n: Q(refs[n]["multiplier_exact"]) for n in names}
    e["mu_min"] = (short(min(names, key=lambda n: mu[n])), str(min(mu.values())), float(min(mu.values())))
    e["mu_max"] = (short(max(names, key=lambda n: mu[n])), str(max(mu.values())), float(max(mu.values())))
    e["certified"] = sum(refs[n]["optimum_certificate"]["certified"] is True for n in names)
    e["witness_pc"] = sum(refs[n]["witness_primal_check"]["passed"] is True for n in names)
    e["switches0"] = sum(refs[n]["assignment_switches_after_gurobi"] == 0 for n in names)
    # independent exact recomputation
    ind = {}
    c3cases = load_cases(C3RUN)
    for n in names:
        case = cases[n]
        nn = n_of(n)
        allp = []
        for i in range(1, nn + 1):
            p = copy_pieces(case, i)
            assert all(A == 2 for A, _, _ in p.values())
            tr = case["mechanism"]["triples"][i - 1]
            expect = sorted((Q(2), -2 * (Q(s) + Q(t)), Q(s) ** 2 + Q(t) ** 2) for s in tr["a"] for t in tr["c"])
            if sorted(p.values()) != expect:
                problems.append(("row pieces != triples", n, i))
            allp.append(list(p.values()))
        rows = case["model"]["rows"]
        yidx = {4 * (i - 1) + 1 for i in range(1, nn + 1)}
        last = rows[-1]
        cc = cq[n]
        coupling_ok = (set(int(k) for k in last["lin"]) == yidx and all(hexq(v["binary64"]) == 1 for v in last["lin"].values())
                       and hexq(last["ub"]["binary64"]) == cc and not last["quad"])
        # y* and c
        ystar = [min(copy_min(p, Q(0))[1]) for p in allp]
        sumys = sum(ystar)
        c_calc = Q(math.floor(64 * sumys / 2), 64)
        summin = sum(copy_min(p, Q(0))[0] for p in allp)
        res = bound_ii_exact(allp, cc)
        _, smin_s, smax_s, _, _ = lagrange(allp, cc, mu[n])
        stored_mu_opt = smin_s <= cc <= smax_s
        em = exact_multiplier(allp, cc, res)
        mu_opt = em is not None
        if mu_opt:
            mustar, hs, smin, smax, ties = em
        else:
            mustar, hs, smin, smax, ties = None, None, None, None, None
        frac = (1 if smin < cc < smax else 0) if mu_opt else None
        wx = [Q(v) for v in refs[n]["witness_exact"]]
        wsum = sum(wx[4 * (i - 1) + 1] for i in range(1, nn + 1))
        wfeas = True
        for i in range(1, nn + 1):
            x, y, z, t = wx[4 * (i - 1): 4 * i]
            if x not in (0, 1) or z not in (0, 1) or not (0 <= y <= 1):
                wfeas = False
                continue
            A, B, C = copy_pieces(case, i)[(int(x), int(z))]
            if t < A * y * y + B * y + C:
                wfeas = False
        wobj = sum(wx[4 * (i - 1) + 3] for i in range(1, nn + 1))
        yex = [Q(y) for y in refs[n]["y_exact"]]
        yobj = sum(phi(p, y) for p, y in zip(allp, yex))
        ind[n] = {
            "coupling_row_ok": coupling_ok, "c_formula_ok": c_calc == cc,
            "ystar_ok": [str(y) for y in ystar] == refs[n]["coupling"]["y_star"],
            "sum_y_star_ok": str(sumys) == refs[n]["coupling"]["sum_y_star"],
            "sum_min_phi": summin, "c3_opt": c3cases[case["mechanism"]["c3_name"]]["known_optimum"],
            "c3_opt_exact": c3cases[case["mechanism"]["c3_name"]].get("known_optimum_exact"),
            "L": res["L"], "U": res["U"], "exact_mid": res["exact_mid"],
            "stored_mu_in_bracket": res["lo"] <= mu[n] <= res["hi"], "stored_mu_optimal_for_b2": stored_mu_opt,
            "mu_star": mustar, "mu_star_minus_ref_mu": float(mustar) - refs[n]["bound_ii"]["mu"] if mu_opt else None,
            "mu_star_eq_stored": mustar == mu[n] if mu_opt else None,
            "mu_optimal": mu_opt, "bound_exact": hs if mu_opt else None, "ties": ties, "fractional": frac,
            "fc_ref": refs[n]["bound_ii"]["fractional_copies"],
            "witness_feasible": wfeas, "c_minus_witness_ysum": cc - wsum,
            "witness_obj_ok": wobj == Q(refs[n]["witness_objective_exact"]),
            "witness_obj_minus_opt": float(wobj - optx[n]),
            "yexact_sum_eq_c": sum(yex) == cc, "yexact_obj_eq_opt": yobj == optx[n],
        }
        B = ind[n]["bound_exact"]
        if B is not None:
            ind[n]["in_LU"] = res["L"] <= B and (res["U"] is None or B <= res["U"])
            ind[n]["bound_minus_ref_value"] = float(B - Q(refs[n]["bound_ii"]["value"]))
            ind[n]["bound_minus_lower_exact"] = float(B - Q(refs[n]["bound_ii"]["lower_exact"]))
            ind[n]["opt_minus_bound"] = optx[n] - B
    e["ind"] = ind
    ms = {n: v["mu_star"] for n, v in ind.items() if v["mu_star"] is not None}
    e["mu_star_min"] = (short(min(ms, key=ms.get)), str(min(ms.values())), float(min(ms.values())))
    e["mu_star_max"] = (short(max(ms, key=ms.get)), str(max(ms.values())), float(max(ms.values())))
    e["stored_mu_not_b2"] = sorted(short(n) for n, v in ind.items() if not v["stored_mu_optimal_for_b2"])
    e["ref_mu_range"] = (min(refs[n]["bound_ii"]["mu"] for n in names), max(refs[n]["bound_ii"]["mu"] for n in names))
    hull = {}
    for n in HULL_INSTANCES:
        allp = [list(copy_pieces(cases[n], i).values()) for i in range(1, n_of(n) + 1)]
        hv, errb = hull_bound(allp, cq[n])
        hull[short(n)] = {"hull": hv, "err_bound": errb, "minus_exact": hv - float(ind[n]["bound_exact"]),
                          "minus_ref": hv - refs[n]["bound_ii"]["value"]}
    e["hull"] = hull
    V["e"] = e

    # ---- (f) cut directions
    f = {}
    for ph in ("root", "full"):
        for m in CUT_MODES:
            allc = []
            perrun = {}
            for n in names:
                info = cutinfo[idx[(ph, m, n)]["run_id"]]
                allc.extend(info)
                nn = n_of(n)
                lp_blocks = Counter(b_ for b_, cl, *_ in info if cl == "LP")
                row_blocks = Counter(b_ for b_, cl, *_ in info if cl == "row")
                perrun[short(n)] = {"LP": sum(lp_blocks.values()), "row": sum(row_blocks.values()),
                                    "all_blocks_LP": len(lp_blocks) == nn,
                                    "row_one_per_block": (len(row_blocks) == nn and set(row_blocks.values()) == {1})
                                    if m == "rowdir-wide" else (len(row_blocks) == 0),
                                    "cuts": len(info)}
            cls = {}
            for k in ("LP", "remainder", "row"):
                sel = [x for x in allc if x[1] == k]
                sl = [x[4] for x in sel]
                entry = {"cuts": len(sel), "ynz": sum(x[3] for x in sel), "pattern": dict(Counter(x[2] for x in sel))}
                if sl:
                    entry["slope"] = {"median": statistics.median(sl),
                                      "q_incl": statistics.quantiles(sl, n=4, method="inclusive") if len(sl) > 1 else None,
                                      "q_excl": statistics.quantiles(sl, n=4, method="exclusive") if len(sl) > 1 else None,
                                      "min": min(sl), "max": max(sl), "neg": sum(s < 0 for s in sl),
                                      "pos": sum(s > 0 for s in sl), "zero": sum(s == 0 for s in sl)}
                cls[k] = entry
            f[(ph, m)] = {"total": len(allc), "classes": cls, "ynz_total": sum(x[3] for x in allc),
                          "perrun": perrun}
    f["ynz_both_phases"] = sum(f[(ph, m)]["ynz_total"] for ph in ("root", "full") for m in CUT_MODES)
    f["yz_both_phases"] = sum(f[(ph, m)]["total"] - f[(ph, m)]["ynz_total"] for ph in ("root", "full") for m in CUT_MODES)
    f["cutproblems"] = dict(cutproblems)
    f["same_phases"] = {m: f[("root", m)]["classes"] == f[("full", m)]["classes"] for m in CUT_MODES}
    smp = {n: float(ind[n]["sum_min_phi"]) for n in names}
    f["summin_eq_c3"] = sum(abs(smp[n] - ind[n]["c3_opt"]) <= 1e-15 * max(1, abs(smp[n])) for n in names)
    f["summin_eq_c3_exact"] = sum(ind[n]["c3_opt_exact"] is not None and ind[n]["sum_min_phi"] == Q(ind[n]["c3_opt_exact"])
                                  for n in names)
    rowgap = {n: (smp[n] - rb["baseline"][n]) / (opt[n] - rb["baseline"][n]) for n in names}
    f["rowgap"] = mmm(list(rowgap.values()))
    f["rowgap_below_base"] = sum(smp[n] < rb["baseline"][n] for n in names)
    f["cut_roots_above_summin"] = all(rb[m][n] > smp[n] for m in CUT_MODES for n in names)
    minphi = {n: [copy_min(list(copy_pieces(cases[n], i).values()), Q(0))[0] for i in range(1, n_of(n) + 1)] for n in names}
    f["row_cut_rhs_eq_min_phi"] = sum(x[5] == minphi[n][x[0]] for ph in ("root", "full") for n in names
                                      for x in cutinfo[idx[(ph, "rowdir-wide", n)]["run_id"]] if x[1] == "row")
    V["f"] = f

    # ---- (g) and cross-references
    gg = {}
    gg["max_root_time"] = max(seconds(R[m][n]) for m in SCIP_MODES for n in names)
    gg["root_timelimit"] = sum(R[m][n]["status"] == "timelimit" for m in SCIP_MODES for n in names)
    gg["max_outer"] = max(r["outer_wall_seconds"] for r in recs)
    gg["cert_fail"] = sum((r.get("separation") or {}).get("certification_failures", 0) for r in recs)
    gg["round_rej"] = sum((r.get("separation") or {}).get("row_rounding_rejections", 0) for r in recs)
    gg["no_root_dual_multi_node"] = [(m, short(n), F[m][n]["status"], F[m][n]["nodes"]) for m in SCIP_MODES for n in names
                                     if not finite(F[m][n].get("root_dual")) and F[m][n]["nodes"] > 1]
    tl = [r for r in recs if r["status"] == "timelimit"]
    gg["timelimit_runs"] = (len(tl), dict(Counter(r["mode"] for r in tl)))
    gg["timelimit_over"] = (min(seconds(r) - r["time_limit"] for r in tl), max(seconds(r) - r["time_limit"] for r in tl))
    gg["overshoot_001"] = dict(Counter(r["mode"] for r in recs if seconds(r) > r["time_limit"] + 0.01))
    ns_ = {}
    for ph in ("root", "full"):
        rows = [idx[(ph, "baseline-extra", n)] for n in names]
        ns_[ph] = (sum(bool(r["_ns"]["quad"].get("Cuts")) for r in rows), sum(r["_ns"]["quad"].get("#Enforce", 0) for r in rows),
                   sum(r["_ns"]["quad"].get("Cuts", 0) for r in rows))
    gg["intersection"] = ns_
    gg["eccuts_interminor_minor_calls"] = sum((r["_ns"]["seps"].get(k) or 0) for r in recs if "_ns" in r
                                              for k in ("eccuts", "interminor", "minor"))
    gg["base_n20_s5_s8_time"] = (min(seconds(F["baseline"]["interleaved_path_coupled_n20_s%d" % s]) for s in (5, 6, 7, 8)),
                                 max(seconds(F["baseline"]["interleaved_path_coupled_n20_s%d" % s]) for s in (5, 6, 7, 8)))
    vr = (V4 / "results-c4v/results.md").read_text()
    gg["vr_pairhull_line"] = "pair-hull bound 0" in vr
    # C3 rowdir-wide and C2/C3 Gurobi excess (cross-references to evidence/campaign4-digest.md)
    c3 = stream_other(C3RUN / "records.jsonl", {"baseline", "rowdir-wide", "gurobi"})
    c3i = {(r["phase"], r["mode"], r["name"]): r for r in c3}
    c3names = sorted({r["name"] for r in c3})
    c3gap = []
    for n in c3names:
        base, rw = root_bound(c3i[("root", "baseline", n)]), root_bound(c3i[("root", "rowdir-wide", n)])
        o = c3cases[n]["known_optimum"]
        c3gap.append((rw - base) / (o - base))
    gg["c3_rw_gap"] = (min(c3gap), max(c3gap), len(c3gap))
    gg["c3_rw_full"] = (sum(solved(c3i[("full", "rowdir-wide", n)]) for n in c3names),
                        max(seconds(c3i[("full", "rowdir-wide", n)]) for n in c3names))
    c2 = stream_other(C2RUN / "records.jsonl", {"gurobi"})
    c2cases = load_cases(C2RUN)
    exc = []
    for r, cs in [(r, c3cases) for r in c3 if r["mode"] == "gurobi"] + [(r, c2cases) for r in c2]:
        if finite(r.get("dual")):
            exc.append((float(Q(r["dual"]) - Q(cs[r["name"]]["known_optimum_exact"])), r["part"], r["name"]))
    gg["c23_gurobi_max_excess"] = max(exc)
    V["g"] = gg

    # ------------------------------------------------------------------------- comparisons
    checks = build_checks(V, names, problems)
    nok = sum(ok for ok, *_ in checks)
    print(f"R8_c4: {nok} of {len(checks)} digest checks match; data problems: {len(problems)}")
    for ok, label, printed, value in checks:
        if not ok:
            print(f"  MISMATCH  {label}: digest {printed!r}  recomputed {value!r}")
    if problems:
        print("data problems:", problems)
    if want_values:
        for ok, label, printed, value in checks:
            print(f"  {'ok ' if ok else 'BAD'} {label}: digest {printed!r} | {value!r}")
        dump(V)
    if "--json" in sys.argv:
        out = sys.argv[sys.argv.index("--json") + 1]
        Path(out).write_text(json.dumps({"checks": [{"ok": ok, "label": l, "digest": p, "value": repr(v)}
                                                    for ok, l, p, v in checks], "problems": [repr(p) for p in problems]},
                                        indent=1))


def dump(V):
    def conv(x):
        if isinstance(x, Q):
            return f"{float(x):.17g} (exact {'%d/%d' % (x.numerator, x.denominator) if x.denominator < 10**30 else 'long'})"
        if isinstance(x, dict):
            return {str(k): conv(v) for k, v in x.items()}
        if isinstance(x, (list, tuple)):
            return [conv(v) for v in x]
        return x
    for sec in ("a", "b", "c", "d", "e", "f", "g"):
        print(f"--- section {sec}")
        print(json.dumps(conv(V[sec]), indent=1, default=str))


# ----------------------------------------------------------------------------- digest numbers

def tol_of(s):
    t = s.strip().lstrip("+-").replace(",", "").replace("%", "")
    if "e" in t:
        mant, ex = t.split("e")
        dec = len(mant.split(".")[1]) if "." in mant else 0
        return 0.5 * 10.0 ** (int(ex) - dec)
    dec = len(t.split(".")[1]) if "." in t else 0
    return 0.5 * 10.0 ** (-dec)


def num(s):
    return float(s.replace(",", "").replace("%", "").replace("+", ""))


def build_checks(V, names, problems):
    out = []

    def N(label, printed, value, scale=1.0):
        ok = value is not None and abs(value * scale - num(printed)) <= tol_of(printed) * (1 + 1e-9) + 1e-15
        out.append((ok, label, printed, value))

    def X(label, printed, value):
        out.append((printed == value, label, printed, value))

    a, b, c, d, e, f, g = (V[k] for k in "abcdefg")
    # checks section
    X("records scheduled", 180, V["scheduled"]); X("records recorded", 180, V["recorded"])
    X("missing/unscheduled/dups", ([], [], 0), (V["missing"], V["unscheduled"], V["dup_run_ids"]))
    X("returncode nonzero", 0, V["returncode_nonzero"]); X("worker_status", 0, V["worker_status"])
    X("primal checks passed (180 incumbents)", 180, V["primal_passed"]); X("primal checked", 180, V["primal_checked"])
    N("max scaled violation", "9.97e-7", V["max_scaled_violation"])
    X("flagged runs", 0, V["flagged"]); X("reference witness checks passed", 180, V["witness_checks_passed"])
    X("classifier errors", 0, V["classifier_errors"]); X("case refs equal REF", 20, V["case_ref_equal"])
    # (a)
    X("replay passed/archived", (True, True), (a["passed"], a["archived_passed"]))
    X("records/bound/admitted", (180, 160, 160), (a["records"], a["bound_runs"], a["admitted_runs"]))
    X("cuts/replayed", (48000, 48000), (a["cuts"], a["replayed_cuts"]))
    X("replayed per mode and phase", {("frozen-wide", "root"): 12000, ("frozen-wide", "full"): 12000,
                                      ("rowdir-wide", "root"): 12000, ("rowdir-wide", "full"): 12000},
      {k: v for k, v in a["replayed_by_mode_phase"].items() if v})
    X("failed runs", 0, a["failed_runs"]); X("missing_cut_logs", 0, a["missing_cut_logs"])
    X("coverage", (180, 180, [], [], []), (a["coverage"]["scheduled"], a["coverage"]["recorded"], a["coverage"]["missing"],
                                           a["coverage"]["unscheduled"], a["coverage"]["duplicates"]))
    X("config failures", (0, 160), a["config"]); X("gurobi failures", (0, 20), a["gurobi"])
    X("omitted runs", (20, {"timelimit": 14, "optimal": 6}, 0, True), a["omitted"])
    X("source_files_verified", 106, a["source_files_verified"])
    N("replay_seconds", "1658.4", a["replay_seconds"]); N("wrapper_seconds", "1684.3", a["wrapper_seconds"])
    X("replay sha prefix", "10115390a428ca2e", a["replay_sha"][:16]); X("wrapper sha prefix", "05e0138106104ee5", a["wrapper_sha"][:16])
    X("wrapper sha == sha256sum replay_v4.py", True, a["wrapper_sha"] == a["sha_replay_v4.py"])
    X("tamper frozen-wide", ("001_interleaved_path_coupled_n80_s6__full__s0__frozen-wide", 1280, True, 14, 14), a["tamper"]["frozen-wide"])
    X("tamper rowdir-wide", ("002_interleaved_path_coupled_n80_s7__full__s0__rowdir-wide", 1280, True, 14, 14), a["tamper"]["rowdir-wide"])
    X("tamper part-level", (14, 14), a["tamper_part"]); X("tamper cover", True, a["tamper_cover"])
    X("RL single line", 1, a["log_lines"])
    X("replay done before 22:18:45Z (replay.json mtime)", True, a["replay_mtime"] <= "22:18:45Z")
    X("replay start ~21:50:33Z (mtime - wrapper_seconds, to the second)", True, abs(int(a["replay_start_est"][6:8]) + 60 * int(a["replay_start_est"][3:5]) - (33 + 60 * 50)) <= 2 and a["replay_start_est"][:2] == "21")
    X("identical cut lists root/full", {"frozen-wide": 20, "rowdir-wide": 20}, a["identical_cut_lists"])
    X("campaign4-replay.md totals present", {"56,771 replayed cuts": True, "56,771 = **95,267**": True, "56,771 = 64,269": True,
                                             "21:03:44Z to 21:24:37Z": True}, a["replay_md_has"])
    X("104,771 = 56,771 + 48,000", 104771, 56771 + a["replayed_cuts"])
    X("112,269 = 64,269 + 48,000", 112269, 64269 + a["replayed_cuts"])
    X("143,267 = 95,267 + 48,000", 143267, 95267 + a["replayed_cuts"])
    # (b)
    X("root status baseline", {"nodelimit": 20}, b["status"]["baseline"])
    X("root status baseline-extra", {"nodelimit": 20}, b["status"]["baseline-extra"])
    X("root status frozen-wide", {"nodelimit": 19, "gaplimit": 1}, b["status"]["frozen-wide"])
    X("root status rowdir-wide", {"nodelimit": 19, "gaplimit": 1}, b["status"]["rowdir-wide"])
    X("root gaplimit run fw", [("n10_s6", 1)], b["root_gaplimit"]["frozen-wide"])
    X("root gaplimit run rw", [("n10_s6", 1)], b["root_gaplimit"]["rowdir-wide"])
    for m, vals in (("baseline", ("1.082", "0.3045", "2.336")), ("baseline-extra", ("1.278", "0.3859", "2.576")),
                    ("frozen-wide", ("10.77", "3.007", "33.16")), ("rowdir-wide", ("11.12", "3.213", "34.48"))):
        for lab, p, v in zip(("median", "min", "max"), vals, b["time"][m]):
            N(f"root time {m} {lab}", p, v)
    N("n10_s6 root fw", "0.2546312", b["n10_s6"]["fw"]); N("n10_s6 root rw", "0.2546430", b["n10_s6"]["rw"])
    N("n10_s6 incumbent fw", "0.2546538", b["n10_s6"]["inc_fw"]); N("n10_s6 incumbent rw", "0.2546538", b["n10_s6"]["inc_rw"])
    N("n10_s6 optimum", "0.2546539", b["n10_s6"]["opt"]); N("n10_s6 bound ii", "0.2546539", b["n10_s6"]["b2"])
    rbt = {"baseline": [("-0.0234", "-0.1117", "0.2214"), ("0.09005", "-0.0242", "0.2429"), ("0.0889", "-0.2923", "0.205"), ("0.2171", "-0.1272", "0.7687")],
           "baseline-extra": [("0.01975", "-0.07763", "0.2353"), ("0.2405", "0.1192", "0.4682"), ("0.4817", "0.2029", "0.6438"), ("0.9267", "0.6044", "1.463")],
           "frozen-wide": [("0.1284", "0.04714", "0.2546"), ("0.3407", "0.33", "0.5257"), ("0.613", "0.4903", "0.8234"), ("1.273", "1.112", "1.76")],
           "rowdir-wide": [("0.1297", "0.06637", "0.2546"), ("0.3473", "0.3301", "0.5369"), ("0.6259", "0.5173", "0.8405"), ("1.325", "1.166", "1.812")]}
    for m, rowsp in rbt.items():
        for k, trip in zip(NS, rowsp):
            for lab, p, v in zip(("med", "min", "max"), trip, b["rb_table"][m][k]):
                N(f"root bound {m} n={k} {lab}", p, v)
    for k, trip in zip(NS, [("0.1301", "0.06988", "0.2547"), ("0.3526", "0.3327", "0.5402"), ("0.6300", "0.5366", "0.8541"), ("1.341", "1.186", "1.840")]):
        for lab, p, v in zip(("med", "min", "max"), trip, b["opt_table"][k]):
            N(f"optimum n={k} {lab}", p, v)
    for m in ("baseline-extra", "frozen-wide", "rowdir-wide"):
        for rt in (1e-4, 1e-6):
            X(f"root better than baseline {m} rtol {rt}", {"better": 20}, dict(b["better_than_base"][m][rt]))
    gt = {"opt": {"baseline-extra": [("0.287", "0.188", "0.640"), ("0.600", "0.299", "0.758"), ("0.685", "0.594", "0.734"), ("0.655", "0.553", "0.684"), ("0.615", "0.188", "0.758")],
                  "frozen-wide": [("0.983", "0.875", "0.999"), ("0.960", "0.945", "0.986"), ("0.954", "0.944", "0.969"), ("0.933", "0.926", "0.943"), ("0.953", "0.875", "0.9993")],
                  "rowdir-wide": [("0.997", "0.981", "0.9997"), ("0.989", "0.984", "0.997"), ("0.981", "0.977", "0.992"), ("0.982", "0.974", "0.986"), ("0.986", "0.974", "0.9997")]},
          "b2": {"baseline-extra": [("0.287", "0.188", "0.641"), ("0.600", "0.299", "0.760"), ("0.685", "0.594", "0.734"), ("0.655", "0.553", "0.684"), ("0.615", "0.188", "0.760")],
                 "frozen-wide": [("0.984", "0.875", "0.999"), ("0.960", "0.945", "0.986"), ("0.954", "0.944", "0.969"), ("0.933", "0.926", "0.943"), ("0.954", "0.875", "0.9993")],
                 "rowdir-wide": [("0.997", "0.981", "0.9997"), ("0.991", "0.985", "0.997"), ("0.981", "0.977", "0.992"), ("0.982", "0.974", "0.986"), ("0.986", "0.974", "0.9997")]}}
    for label, tab in gt.items():
        for m, rowsp in tab.items():
            for k, trip in zip(NS + ("all",), rowsp):
                for lab, p, v in zip(("med", "min", "max"), trip, b["gap"][label][m][k]):
                    N(f"gap closed vs {label} {m} {k} {lab}", p, v)
    X("gap vs opt argmin/argmax bx", ("n10_s8", "n20_s8"), (b["gap"]["opt"]["baseline-extra"]["argmin"], b["gap"]["opt"]["baseline-extra"]["argmax"]))
    X("gap vs opt argmin/argmax fw", ("n10_s8", "n10_s6"), (b["gap"]["opt"]["frozen-wide"]["argmin"], b["gap"]["opt"]["frozen-wide"]["argmax"]))
    X("gap vs opt argmin/argmax rw", ("n80_s5", "n10_s6"), (b["gap"]["opt"]["rowdir-wide"]["argmin"], b["gap"]["opt"]["rowdir-wide"]["argmax"]))
    X("gap tables differ only on the 7 positive-gap instances", 7, len(b["gap_differs"]))
    mb = {"baseline": ("-1.413", "n80_s7", "-0.03328", "n10_s6", "-0.155", "-0.297", "-0.558", "-1.19"),
          "baseline-extra": ("-0.5813", "n80_s8", "-0.01931", "n10_s6", "-0.0904", "-0.100", "-0.210", "-0.414"),
          "frozen-wide": ("-0.1043", "n80_s7", "-2.273e-5", "n10_s6", "-0.0027", "-0.0117", "-0.0290", "-0.0735"),
          "rowdir-wide": ("-0.02876", "n80_s9", "-1.096e-5", "n10_s6", "-0.000474", "-0.00263", "-0.0101", "-0.0251")}
    for m, (mn, amn, mx, amx, *meds) in mb.items():
        v = b["minus_b2"][m]
        N(f"root - b2 {m} min", mn, v["min"]); X(f"root - b2 {m} argmin", amn, v["argmin"])
        N(f"root - b2 {m} max", mx, v["max"]); X(f"root - b2 {m} argmax", amx, v["argmax"])
        for k, p in zip(NS, meds):
            N(f"root - b2 {m} n={k} median", p, v[k])
    N("main: closest root run below b2 (rw n10_s6)", "-1.1e-5", b["minus_b2"]["rowdir-wide"]["max"])
    X("no root bound above b2", 0, b["root_above_b2"]); X("no root bound above optimum", 0, b["root_above_opt"])
    N("rw n80 below b2 lower end", "-0.0288", b["rw_n80_range"][0]); N("rw n80 below b2 upper end", "-0.0158", b["rw_n80_range"][1])
    X("full root_dual differs counts", {"baseline": 1, "baseline-extra": 2, "frozen-wide": 4, "rowdir-wide": 12}, b["root_dual_differs"])
    X("where both finite full higher", True, b["differ_full_higher"])
    X("every differing full run has FIXED vars", True, b["differ_full_fixed"])
    X("no root run has FIXED", 0, b["root_runs_fixed"])
    N("rw n40_s8 root-run root_dual", "0.7404318", b["rw_n40_s8"][0]); N("rw n40_s8 full-run root_dual", "0.7504922", b["rw_n40_s8"][1])
    above = {(m, s): (st, nd, dv, below, gapo, fx) for m, s, st, nd, dv, below, gapo, fx, _ in b["full_root_above_b2"]}
    X("six full runs with root bound above b2 (set)",
      {("frozen-wide", "n10_s7"), ("frozen-wide", "n10_s9"), ("rowdir-wide", "n10_s7"), ("rowdir-wide", "n10_s9"),
       ("rowdir-wide", "n20_s6"), ("rowdir-wide", "n20_s8")}, set(above))
    for (m, s), p in ((("frozen-wide", "n10_s7"), "7.15e-6"), (("frozen-wide", "n10_s9"), "5.51e-5"), (("rowdir-wide", "n10_s7"), "9.34e-6"),
                      (("rowdir-wide", "n10_s9"), "4.75e-5"), (("rowdir-wide", "n20_s6"), "1.12e-5"), (("rowdir-wide", "n20_s8"), "5.92e-4")):
        if (m, s) in above:
            N(f"full root above b2 {m} {s}", p, above[(m, s)][2])
            X(f"full root above b2 {m} {s} gaplimit at 1 node, below opt, FIXED", ("gaplimit", 1, True, True),
              (above[(m, s)][0], above[(m, s)][1], above[(m, s)][3], above[(m, s)][5]))
    for s, p in (("n10_s7", "1.53e-5"), ("n10_s9", "6.10e-5"), ("n20_s6", "2.71e-5"), ("n20_s8", "6.47e-4")):
        N(f"opt - b2 {s}", p, float(e["ind"]["interleaved_path_coupled_" + s]["opt_minus_bound"]))
    X("no SCIP final dual above exact optimum", 0, b["scip_dual_above_optx"])
    # (c)
    X("full solved", {"baseline": 10, "baseline-extra": 13, "frozen-wide": 20, "rowdir-wide": 20, "gurobi": 6}, c["solved"])
    X("full status baseline", {"optimal": 10, "timelimit": 10}, c["status"]["baseline"])
    X("full status baseline-extra", {"optimal": 12, "gaplimit": 1, "timelimit": 7}, c["status"]["baseline-extra"])
    X("full status frozen-wide", {"optimal": 15, "gaplimit": 5}, c["status"]["frozen-wide"])
    X("full status rowdir-wide", {"optimal": 9, "gaplimit": 11}, c["status"]["rowdir-wide"])
    X("full status gurobi", {"optimal": 6, "timelimit": 14}, c["status"]["gurobi"])
    n10 = [f"n10_s{s}" for s in SEEDS]; n20 = [f"n20_s{s}" for s in SEEDS]
    X("solved list baseline", n10 + n20, c["solved_list"]["baseline"])
    X("solved list baseline-extra", n10 + n20 + ["n40_s5", "n40_s6", "n40_s8"], c["solved_list"]["baseline-extra"])
    X("solved list gurobi", n10 + ["n20_s9"], c["solved_list"]["gurobi"])
    for m, trip in (("baseline", ("1.598", "0.4948", "14.08")), ("baseline-extra", ("1.929", "0.4624", "98.96")), ("frozen-wide", ("11.85", "3.267", "107.5")),
                    ("rowdir-wide", ("11.04", "3.244", "133.7")), ("gurobi", ("0.1103", "0.03426", "0.42"))):
        for lab, p, v in zip(("median", "min", "max"), trip, c["time_solved"][m]):
            N(f"full solved time {m} {lab}", p, v)
    for m, p in (("baseline", "22,533.5"), ("baseline-extra", "19,584"), ("frozen-wide", "83.5"), ("rowdir-wide", "1"), ("gurobi", "156,598")):
        N(f"median nodes all 20 {m}", p, c["nodes_all"][m])
    X("one-node solves baseline", [], c["one_node"]["baseline"])
    X("one-node solves baseline-extra", [("n10_s6", "gaplimit")], c["one_node"]["baseline-extra"])
    X("one-node solves frozen-wide", [(s, "gaplimit") for s in ("n10_s5", "n10_s6", "n10_s7", "n10_s9")], c["one_node"]["frozen-wide"])
    X("one-node solves rowdir-wide", [(s, "gaplimit") for s in n10 + ["n20_s5", "n20_s6", "n20_s8", "n20_s9", "n40_s5", "n40_s8"]], c["one_node"]["rowdir-wide"])
    X("common 6", n10 + ["n20_s9"], c["common6"])
    for m, (t1, t2, t3, t4, nd) in (("baseline", ("0.9168", "0.8778", None, None, "239.5")), ("baseline-extra", ("0.8636", "0.8251", None, None, "113")),
                                    ("frozen-wide", ("3.996", "3.959", "0.5505", "3.41", "1")), ("rowdir-wide", ("3.737", "3.695", "0.2356", "3.465", "1")),
                                    ("gurobi", ("0.1429", "0.1386", None, None, "70"))):
        N(f"SGM6 {m}", t1, c["sgm6"][m]); N(f"SGM6 solver {m}", t2, c["sgm6_solver"][m]); N(f"nodes6 {m}", nd, c["nodes6"][m])
        if t3:
            N(f"SGM6 excl {m}", t3, c["sgm6_excl"][m]); N(f"SGM6 callback {m}", t4, c["sgm6_cb"][m])
    for m, (p, pairs, fast) in (("baseline-extra", ("0.7346", 10, 7)), ("frozen-wide", ("3.514", 10, 2)), ("rowdir-wide", ("3.248", 10, 2)), ("gurobi", ("0.1502", 6, 6))):
        N(f"ratio median {m}", p, c["ratio"][m][0]); X(f"ratio pairs/faster {m}", (pairs, fast), c["ratio"][m][1:])
    X("common 10 = n10, n20", n10 + n20, c["common10"])
    for m, p, nd in (("baseline", "2.496", "476"), ("baseline-extra", "1.900", "289.5"), ("frozen-wide", "5.126", "9"), ("rowdir-wide", "4.905", "1")):
        N(f"SGM10 {m}", p, c["sgm10"][m]); N(f"nodes10 {m}", nd, c["nodes10"][m])
    N("SGM20 fw", "12.96", c["sgm20"]["frozen-wide"]); N("SGM20 rw", "12.20", c["sgm20"]["rowdir-wide"])
    N("n80 time fw min", "37.6", c["n80_range"]["frozen-wide"][0]); N("n80 time fw max", "108", c["n80_range"]["frozen-wide"][1])
    N("n80 time rw min", "37.3", c["n80_range"]["rowdir-wide"][0]); N("n80 time rw max", "134", c["n80_range"]["rowdir-wide"][1])
    n4080 = sorted([f"n40_s{s}" for s in SEEDS] + [f"n80_s{s}" for s in SEEDS])
    for m in ("baseline-extra", "frozen-wide", "rowdir-wide"):
        X(f"final dual vs baseline 1e-4 {m}", {"better": 10, "tie": 10}, c["cmp"][m][1e-4][0])
        X(f"final dual better set 1e-4 {m}", n4080, c["cmp"][m][1e-4][1].get("better"))
    X("gurobi final dual vs baseline 1e-4", {"better": 10, "tie": 6, "worse": 4}, c["cmp"]["gurobi"][1e-4][0])
    X("gurobi worse set", ["n20_s5", "n20_s6", "n20_s7", "n20_s8"], c["cmp"]["gurobi"][1e-4][1].get("worse"))
    X("rw worse at 1e-6 on all 10 common", 10, len(c["rw_worse_1e6_on_common10"]))
    X("rw statuses on the 10 common (digest implies all gaplimit)", {"gaplimit": 10}, c["rw_common10_status"])
    for m, trip in (("baseline", ("-5.05e-6", "-7.9e-6", "-2.15e-6")), ("baseline-extra", ("-8.06e-6", "-1.96e-5", "-2.91e-6")),
                    ("frozen-wide", ("-1.13e-5", "-1.63e-4", "-4.01e-6")), ("rowdir-wide", ("-1.97e-5", "-5.92e-5", "-5.31e-6"))):
        for lab, p, v in zip(("median", "min", "max"), trip, c["dual_minus_opt"][m]):
            N(f"final dual - opt {m} {lab}", p, v)
    N("fw n80_s5 final dual", "1.78331", c["fw_n80_s5"][0]); N("n80_s5 optimum", "1.78347", c["fw_n80_s5"][1])
    N("SCIP incumbent min - opt", "-3.08e-5", c["scip_inc_min"][0]); X("SCIP incumbent min where", ("rowdir-wide", "n80_s5"), (c["scip_inc_min"][1], c["scip_inc_min"][3]))
    N("Gurobi incumbent min - opt", "-1.28e-5", c["gurobi_inc_min"][0]); X("Gurobi incumbent min where", "n40_s9", c["gurobi_inc_min"][3])
    X("incumbents", 180, c["incumbents"])
    G = c["gurobi"]
    X("gurobi params", True, all(v["params"]["Threads"] == 1 and v["params"]["NonConvex"] == 2 and v["params"]["MIPGap"] == 1e-4
                                 and v["params"]["Seed"] == 0 and v["version"] == "13.0.3" and v["tl_eq_budget"] for v in G.values()))
    for s, p, tm, nd in zip(n10, ("2.0e-8", "3.3e-8", "2.7e-8", "1.11e-9", "1.29e-8"), ("0.0834", "0.0343", "0.110", "0.136", "0.111"), (39, 5, 95, 309, 45)):
        X(f"gurobi {s} status", ("optimal", "OPTIMAL", 0, True), (G[s]["status"], G[s]["gs"], G[s]["mip_gap"], G[s]["dual_eq_primal"]))
        N(f"gurobi {s} dual - opt", p, G[s]["dmo"]); N(f"gurobi {s} time", tm, G[s]["time"]); X(f"gurobi {s} nodes", nd, G[s]["nodes"])
    X("gurobi n20_s9 status", ("optimal", "OPTIMAL", 0), (G["n20_s9"]["status"], G["n20_s9"]["gs"], G["n20_s9"]["mip_gap"]))
    N("gurobi n20_s9 dual - opt", "-6.89e-6", G["n20_s9"]["dmo"]); N("gurobi n20_s9 time", "0.42", G["n20_s9"]["time"]); X("gurobi n20_s9 nodes", 815, G["n20_s9"]["nodes"])
    for s, p, mg in zip(("n20_s5", "n20_s6", "n20_s7", "n20_s8"), ("-3.26e-4", "-6.32e-4", "-3.98e-4", "-2.60e-4"), ("9.46e-4", "1.32e-3", "1.11e-3", "4.76e-4")):
        X(f"gurobi {s} status", ("timelimit", "TIME_LIMIT"), (G[s]["status"], G[s]["gs"]))
        N(f"gurobi {s} dual - opt", p, G[s]["dmo"]); N(f"gurobi {s} mip_gap", mg, G[s]["mip_gap"]); N(f"gurobi {s} time", "300.2", G[s]["time"])
    X("gurobi n20 s5-s8 nodes range", (941457, 1242198), (min(G[s]["nodes"] for s in ("n20_s5", "n20_s6", "n20_s7", "n20_s8")),
                                                         max(G[s]["nodes"] for s in ("n20_s5", "n20_s6", "n20_s7", "n20_s8"))))
    for k, (d1, d2, g1, g2, nr) in ((40, ("-3.33e-3", "-8.92e-3", "3.89e-3", "0.0166", (377298, 441453))), (80, ("-0.0734", "-0.113", "0.0456", "0.0879", (126449, 162053)))):
        ss = [f"n{k}_s{s}" for s in SEEDS]
        X(f"gurobi n{k} all timelimit", True, all(G[s]["status"] == "timelimit" for s in ss))
        N(f"gurobi n{k} dual - opt closest", d1, max(G[s]["dmo"] for s in ss)); N(f"gurobi n{k} dual - opt farthest", d2, min(G[s]["dmo"] for s in ss))
        N(f"gurobi n{k} mip_gap min", g1, min(G[s]["mip_gap"] for s in ss)); N(f"gurobi n{k} mip_gap max", g2, max(G[s]["mip_gap"] for s in ss))
        X(f"gurobi n{k} nodes range", nr, (min(G[s]["nodes"] for s in ss), max(G[s]["nodes"] for s in ss)))
        X(f"gurobi n{k} time 300.2", True, all(abs(G[s]["time"] - 300.2) <= 0.05 for s in ss))
    N("C2/C3 Gurobi max excess", "1.16e-6", g["c23_gurobi_max_excess"][0])
    # (d)
    for m, vals in (("frozen-wide", (20, 141, 14186, 0, 14186, 0, 1939, 247, 20, 12000, 14179, 13079)),
                    ("rowdir-wide", (20, 141, 15204, 0, 15204, 0, 2989, 215, 20, 12000, 14381, 13383))):
        for ph in ("root", "full"):
            t = d["funnel"][(ph, m)]
            got = (20, t["calls"], t["certification_calls"], t["certification_failures"], t["certified"], t["row_rounding_rejections"],
                   t["below"], t["row_binding_rejections"], t["binding_runs"], t["cuts"], t["candidate_lps"], t["exchange_samples"])
            X(f"funnel {ph} {m}", vals, got)
            X(f"funnel causes {ph} {m}", {"column_set_differs_tiny_coefficient_dropped": vals[7]}, t["causes"])
            X(f"funnel sampling/varstatus {ph} {m}", (0, {}), (t["sampling_failures"], t["varstatus"]))
    X("repeat skips fw/rw", (6, 12), (d["funnel"][("root", "frozen-wide")]["repeat_skips"], d["funnel"][("root", "rowdir-wide")]["repeat_skips"]))
    N("binding share fw %", "2.0%", d["funnel"][("root", "frozen-wide")]["share"], 100)
    N("binding share rw %", "1.8%", d["funnel"][("root", "rowdir-wide")]["share"], 100)
    X("funnel identical in both phases", {"frozen-wide": True, "rowdir-wide": True}, d["funnel_same_phases"])
    for m, sr, cr, cbr, cbf in (("frozen-wide", ("0.448", "0.505"), (6, 8), ("2.749", "31.03"), ("2.84", "33.51")),
                                ("rowdir-wide", ("0.475", "0.525"), (7, 8), ("3.011", "32.96"), ("2.955", "35.78"))):
        for ph in ("root", "full"):
            t = d["funnel"][(ph, m)]
            X(f"caps {ph} {m}: cut cap reached / support / rounds / time / config ok", (20, 0, 0, 0, True),
              (t["cut_cap_reached"], t["support_cap_reached"], t["round_cap_reached"], t["time_cap_reached"], t["config_ok"]))
            N(f"support ratio min {ph} {m}", sr[0], t["support_ratio"][0]); N(f"support ratio max {ph} {m}", sr[1], t["support_ratio"][1])
            X(f"callbacks per run {ph} {m}", cr, t["calls_range"])
            X(f"budget_exhausted / discovery incomplete / cut log ok {ph} {m}", (20, 0, 20), (t["budget_exhausted"], t["discovery_incomplete"], t["cut_log_ok"]))
            X(f"time budget value {ph} {m}", [60.0], t["budget_values"])
        N(f"callback seconds root min {m}", cbr[0], d["funnel"][("root", m)]["cb_range"][0]); N(f"callback seconds root max {m}", cbr[1], d["funnel"][("root", m)]["cb_range"][1])
        N(f"callback seconds full min {m}", cbf[0], d["funnel"][("full", m)]["cb_range"][0]); N(f"callback seconds full max {m}", cbf[1], d["funnel"][("full", m)]["cb_range"][1])
    tdx = {("root", "frozen-wide"): (20, "10.49", "0.864", "9.654", "1.078", "1.007", "0.884", "10.76"),
           ("root", "rowdir-wide"): (20, "10.65", "0.6581", "10.02", "1.078", "1.007", "0.626", "10.44"),
           ("root", "baseline-extra"): (20, "1.213", "1.143", "0", "1.078", "1.007", "1.119", "1.129"),
           ("full", "frozen-wide"): (10, "5.126", "0.774", "4.325", "2.496", "2.444", "0.321", "3.514"),
           ("full", "rowdir-wide"): (10, "4.905", "0.4177", "4.468", "2.496", "2.444", "0.2025", "3.248"),
           ("full", "baseline-extra"): (10, "1.900", "1.852", "0", "2.496", "2.444", "0.729", "0.735")}
    for key, (pairs, *vals) in tdx.items():
        t = d["td"][key]
        X(f"td pairs {key}", pairs, t["pairs"])
        for lab, p in zip(("sgm_total", "sgm_excl", "sgm_cb", "base_total", "base_scip", "med_excl_ratio", "med_total_ratio"), vals):
            N(f"td {key} {lab}", p, t[lab])
    sx = {("root", "frozen-wide"): ("283.1", "281.3", "19.4", "261.9", "92.5", "10.2", "36.5", "129.6", "1.5", "84.1"),
          ("root", "rowdir-wide"): ("291.2", "289.4", "14.5", "274.8", "94.4", "10.7", "36.6", "137.7", "1.4", "88.4"),
          ("full", "frozen-wide"): ("430.3", "428.4", "162.8", "265.6", "61.7", "10.6", "37.1", "131.6", "1.5", "84.8"),
          ("full", "rowdir-wide"): ("424.7", "422.7", "144.7", "278.1", "65.5", "10.8", "37.5", "139.0", "1.5", "89.3")}
    for key, vals in sx.items():
        s = d["sums"][key]
        for lab, p in zip(("charged", "scip", "excl", "cb", "pct", "discovery_seconds", "candidate_seconds", "certification_seconds", "row_seconds", "uncovered"), vals):
            N(f"sums {key} {lab}", p, s[lab])
    N("load root min", "8.13", d["load_range"]["root"][0]); N("load root max", "8.19", d["load_range"]["root"][1])
    N("load full min", "7.86", d["load_range"]["full"][0]); N("load full max", "9.10", d["load_range"]["full"][1])
    X("run window", ("2026-10-03T20:59:57Z", "2026-10-03T21:32:14Z"), d["window"])
    # (e)
    N("omb min", "2.77e-61", e["omb_min"]); N("omb median", "2.90e-60", e["omb_med"]); N("omb max", "6.47e-4", e["omb_max"]); X("omb argmax", "n20_s8", e["omb_argmax"])
    X("zero-gap list", ["n10_s5", "n10_s6", "n10_s8", "n20_s5", "n20_s9"] + [f"n40_s{s}" for s in SEEDS] + ["n80_s5", "n80_s6", "n80_s8"], e["zero"])
    X("zero-gap: fractional 0 and float equal", True, e["zero_fc0_and_float_equal"])
    for s, p in (("n10_s7", "1.53e-5"), ("n10_s9", "6.10e-5"), ("n20_s6", "2.71e-5"), ("n20_s7", "1.53e-4"), ("n20_s8", "6.47e-4"), ("n80_s7", "2.69e-4"), ("n80_s9", "6.02e-5")):
        N(f"positive omb {s}", p, e["pos"].get(s, (None,))[0]); X(f"positive omb {s} fractional", 1, e["pos"].get(s, (None, None))[1])
    X("positive set size", 7, len(e["pos"]))
    X("c min", ("n10_s6", "87/64"), e["c_min"]); X("c max", ("n80_s5", "1001/64"), e["c_max"])
    X("c n10_s5 / n80_s5", ("123/64", "1001/64"), (e["c"]["n10_s5"], e["c"]["n80_s5"]))
    X("sum y* n10_s5 / n80_s5", {"n10_s5": "495/128", "n80_s5": "4005/128"}, e["sumy"])
    N("c / sum y* min", "0.4957", e["c_ratio"][0]); N("c / sum y* max", "0.5", e["c_ratio"][1])
    X("binds 20/20", 20, e["binds"]); X("y_exact sums to c 20/20", 20, e["yexact_sum_c"])
    X("mu min", ("n10_s8", "29/288"), e["mu_min"][:2]); N("mu min float", "0.1007", e["mu_min"][2])
    X("mu max", ("n10_s6", "99/256"), e["mu_max"][:2]); N("mu max float", "0.3867", e["mu_max"][2])
    X("certified / witness pc / switches 0", (20, 20, 20), (e["certified"], e["witness_pc"], e["switches0"]))
    # independent bound (ii)
    ind = e["ind"]
    X("indep: coupling row = sum y <= c in all 20 cases", 20, sum(v["coupling_row_ok"] for v in ind.values()))
    X("indep: c = floor(64 * 0.5 * sum y*) / 64 (20)", 20, sum(v["c_formula_ok"] and v["ystar_ok"] and v["sum_y_star_ok"] for v in ind.values()))
    X("indep: exact bound-(ii) multiplier found and checked (20)", 20, sum(v["mu_optimal"] for v in ind.values()))
    X("indep: |mu* - REF bound_ii.mu| <= 1e-15 (20)", 20, sum(v["mu_optimal"] and abs(v["mu_star_minus_ref_mu"]) <= 1e-15 for v in ind.values()))
    X("digest: REF multiplier_exact is the bound-(ii) multiplier (instances where it is not)", [], e["stored_mu_not_b2"])
    X("bound-(ii) multiplier min/max instances", ("n10_s8", "n10_s6"), (e["mu_star_min"][0], e["mu_star_max"][0]))
    N("bound-(ii) multiplier min", "0.1007", e["mu_star_min"][2]); N("bound-(ii) multiplier max", "0.3867", e["mu_star_max"][2])
    X("indep: exact bound in own [L, U] (20)", 20, sum(v.get("in_LU", False) for v in ind.values()))
    X("indep: |exact bound - REF bound_ii.value| <= 1e-9 (20)", 20, sum(abs(v.get("bound_minus_ref_value", 1)) <= 1e-9 for v in ind.values()))
    X("indep: optimum >= exact bound (20)", 20, sum(v.get("opt_minus_bound", -1) >= 0 for v in ind.values()))
    X("indep: optimum == exact bound exactly on 13", 13, sum(v.get("opt_minus_bound") == 0 for v in ind.values()))
    X("indep: fractional copies equal REF (20)", 20, sum(v["fractional"] == v["fc_ref"] for v in ind.values()))
    X("indep: witness feasible, objective exact (20)", 20, sum(v["witness_feasible"] and v["witness_obj_ok"] for v in ind.values()))
    X("indep: coupling binds at witness: 0 <= c - sum y <= n 2^-52 (20)", 20,
      sum(0 <= v["c_minus_witness_ysum"] <= Q(n_of(k), 2 ** 52) for k, v in ind.items()))
    X("indep: y_exact sums to c and attains the optimum (20)", 20, sum(v["yexact_sum_eq_c"] and v["yexact_obj_eq_opt"] for v in ind.values()))
    for s, h in e["hull"].items():
        X(f"hull {s}: 0 <= hull - exact <= n h^2/2", True, -1e-12 <= h["minus_exact"] <= h["err_bound"])
    # (f)
    fx = {"frozen-wide": {"LP": (11986, 11955, {"xyz": 11951, "xz": 31, "yz": 3, "xy": 1}, ("-0.3125", "-0.5312", "-0.0625", "-5.858", "2.281"), (9449, 2506, 31)),
                          "remainder": (14, 14, {"xyz": 14}, ("-1.578", "-1.797", "-1.344", "-2.031", "-1.062"), (14, 0, 0)),
                          "row": (0, 0, {}, None, None)},
          "rowdir-wide": {"LP": (11236, 11205, {"xyz": 11201, "xz": 31, "yz": 4}, ("-0.2734", "-0.5312", "-0.09375", "-5.888", "1.875"), (9285, 1920, 31)),
                          "remainder": (14, 14, {"xyz": 14}, ("-1.578", "-1.797", "-1.344", "-2.031", "-1.062"), (14, 0, 0)),
                          "row": (750, 0, {"": 750}, None, (0, 0, 750))}}
    for m, tab in fx.items():
        for ph in ("root", "full"):
            cl = f[(ph, m)]["classes"]
            X(f"cuts total {ph} {m}", 12000, f[(ph, m)]["total"])
            for k, (cnt, ynz, pat, sl, signs) in tab.items():
                X(f"class {ph} {m} {k} cuts/ynz/pattern", (cnt, ynz, pat), (cl[k]["cuts"], cl[k]["ynz"], cl[k]["pattern"]))
                if sl:
                    q = cl[k]["slope"]
                    N(f"slope {ph} {m} {k} median", sl[0], q["median"])
                    okq = all(abs(qq - num(p)) <= tol_of(p) * (1 + 1e-9) for qq, p in zip((q["q_incl"][0], q["q_incl"][2]), sl[1:3])) or \
                        all(abs(qq - num(p)) <= tol_of(p) * (1 + 1e-9) for qq, p in zip((q["q_excl"][0], q["q_excl"][2]), sl[1:3]))
                    out.append((okq, f"slope {ph} {m} {k} q1,q3", sl[1:3], (q["q_incl"][0], q["q_incl"][2], q["q_excl"][0], q["q_excl"][2])))
                    N(f"slope {ph} {m} {k} min", sl[3], q["min"]); N(f"slope {ph} {m} {k} max", sl[4], q["max"])
                if signs:
                    q = cl[k]["slope"]
                    X(f"slope signs {ph} {m} {k}", signs, (q["neg"], q["pos"], q["zero"]))
            X(f"ynz total {ph} {m}", {"frozen-wide": 11969, "rowdir-wide": 11219}[m], f[(ph, m)]["ynz_total"])
            pr = f[(ph, m)]["perrun"]
            X(f"every block has LP cuts {ph} {m}", 20, sum(v["all_blocks_LP"] for v in pr.values()))
            X(f"row cuts one per block {ph} {m}", 20, sum(v["row_one_per_block"] for v in pr.values()))
            n80lp = [v["LP"] for s_, v in pr.items() if s_.startswith("n80")]
            X(f"n80 LP cuts range {ph} {m}", {"frozen-wide": (1278, 1279), "rowdir-wide": (1198, 1199)}[m], (min(n80lp), max(n80lp)))
            X(f"cut count = 16n per run {ph} {m}", 20, sum(v["cuts"] == 16 * int(s_[1:].split("_")[0]) for s_, v in pr.items()))
    N("ynz share fw %", "99.7%", 11969 / 12000, 100); N("ynz share rw %", "93.5%", 11219 / 12000, 100)
    N("LP negative share fw %", "79%", f[("root", "frozen-wide")]["classes"]["LP"]["slope"]["neg"] / f[("root", "frozen-wide")]["classes"]["LP"]["cuts"], 100)
    N("LP negative share rw %", "83%", f[("root", "rowdir-wide")]["classes"]["LP"]["slope"]["neg"] / f[("root", "rowdir-wide")]["classes"]["LP"]["cuts"], 100)
    N("LP xyz share fw %", "99.7%", 11951 / 11986, 100); N("LP xyz share rw %", "99.7%", 11201 / 11236, 100)
    X("y coef zero/nonzero over root+full", (46376, 1624), (f["ynz_both_phases"], f["yz_both_phases"]))
    X("row cuts are exactly t_i >= min phi_i (root+full)", 1500, f["row_cut_rhs_eq_min_phi"])
    X("cut-level problems (4-place consistency, exact = a - lambda aff, outside block, t > 0)", {}, f["cutproblems"])
    X("class tables identical root/full", {"frozen-wide": True, "rowdir-wide": True}, f["same_phases"])
    X("sum min phi = C3 optimum (20)", 20, f["summin_eq_c3"])
    N("row-cut bound gap closed median", "0.0243", f["rowgap"][0]); N("row-cut bound gap closed min", "-5.70", f["rowgap"][1]); N("row-cut bound gap closed max", "0.693", f["rowgap"][2])
    X("row-cut bound below baseline root on", 10, f["rowgap_below_base"]); X("fw/rw roots above sum min phi", True, f["cut_roots_above_summin"])
    N("C3 rw root gap closed min (prints 1)", "1.000", g["c3_rw_gap"][0]); X("C3 rw solved", 20, g["c3_rw_full"][0]); N("C3 rw max solved time", "33.2", g["c3_rw_full"][1])
    # (g)
    N("max root time", "34.48", g["max_root_time"]); X("root timelimit", 0, g["root_timelimit"]); N("max outer wall", "302.3", g["max_outer"])
    X("cert failures / rounding rejections", (0, 0), (g["cert_fail"], g["round_rej"]))
    X("full runs without finite root_dual and > 1 node",
      {("frozen-wide", "n20_s5", "optimal", 7), ("rowdir-wide", "n20_s7", "optimal", 3), ("baseline", "n10_s6", "optimal", 2), ("baseline-extra", "n10_s7", "optimal", 79)},
      set(g["no_root_dual_multi_node"]))
    X("timelimit runs", (31, {"baseline": 10, "baseline-extra": 7, "gurobi": 14}), g["timelimit_runs"])
    X("all timelimit runs charged > 300 s", True, g["timelimit_over"][0] > 0)
    N("max overshoot", "0.198", g["timelimit_over"][1])
    X("overshoots > limit + 0.01 s (C list)", {"baseline": 10, "baseline-extra": 7, "gurobi": 14}, g["overshoot_001"])
    X("intersection cuts root (runs, #Enforce, cuts)", (20, 27288, 12692), g["intersection"]["root"])
    X("intersection cuts full (runs, #Enforce, cuts)", (20, 83316305, 12940), g["intersection"]["full"])
    X("eccuts/interminor/minor calls", 0, g["eccuts_interminor_minor_calls"])
    N("baseline n20_s5-s8 time min", "3.95", g["base_n20_s5_s8_time"][0]); N("baseline n20_s5-s8 time max", "14.1", g["base_n20_s5_s8_time"][1])
    X("VR has pair-hull line", True, g["vr_pairhull_line"])
    return out


if __name__ == "__main__":
    main()
