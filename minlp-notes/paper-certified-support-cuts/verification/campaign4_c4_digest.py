"""Campaign-4 Part C4 digest numbers (evidence/campaign4-c4-digest.md).

    PY campaign4_c4_digest.py

Read-only: loads experiments/v4/runs/partC4 (records.jsonl, cases/, replay.json
if present), experiments/v4/c4-references.json and the C3 cases
(experiments/v4/runs/partC3/cases, for sum_i min phi_i), and reuses the definitions
of experiments/v4/summarize_v4.py (imported, not modified): root bound, solved,
completed, SGM (shift 1 s), bound comparison, SCIP time excluding the callback,
funnel. Adds per-n median [min, max] tables, root bound minus bound (ii), root
and full runs ended at the root node, Gurobi and SCIP bounds against the exact
optimum, cap counts per run, the reference values, and a classification of
every recorded cut by its support direction and by the exact eliminated row.

Cut classification. A cut record has the support direction `coefficients`
(a_x, a_y, a_z, lambda) over the block features (x_i, y_i, z_i, nonlinear
remainder of row i) and the source side `signed_sides[0].affine_terms` (exact
rationals; the side is aff(x, y, z) - t + nl(x, y, z) <= rhs). Direction
classes: "row" (a = lambda * aff on the block variables, the exact support of
the whole row), "remainder" (a = 0), "other" (any other direction, i.e. from
the LP direction search `propose_direction`). The exported row is
`row_certificate.exact.coefficients` (exact rationals over all variables);
its y_i coefficient equals a_y - lambda * aff_y, so it is nonzero exactly when
the direction differs from the row direction in the y_i component.
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[2])

from collections import Counter, defaultdict
from fractions import Fraction as Q
import json
import math
import statistics
import sys
from pathlib import Path

V4 = Path((_PUBLIC_REPO + '/paper-certified-support-cuts/experiments/v4'))
sys.path.insert(0, str(V4))
import summarize_v4 as S  # noqa: E402

RUN = V4 / "runs/partC4"
MODES = ("baseline", "frozen-wide", "rowdir-wide", "baseline-extra")
CUT_MODES = ("frozen-wide", "rowdir-wide")


def med(v):
    return statistics.median(v) if v else None


def f(x, d=4):
    if x is None:
        return "-"
    if isinstance(x, float):
        return f"{x:.{d}g}"
    return str(x)


def mmm(v, d=3):
    v = [x for x in v if x is not None]
    return "-" if not v else f"{f(med(v), d)} [{f(min(v), d)}, {f(max(v), d)}]"


def short(name):
    return name.replace("interleaved_path_coupled_", "")


recs = [json.loads(line) for line in (RUN / "records.jsonl").read_text().splitlines() if line]
cases = {p.stem: json.loads(p.read_text()) for p in (RUN / "cases").glob("*.json")}
refs = {e["name"]: e for e in json.loads((V4 / "c4-references.json").read_text())["instances"]}
index = {(r["phase"], r["name"], r["mode"]): r for r in recs}
names = sorted(cases, key=lambda n: (cases[n]["mechanism"]["n"], cases[n]["mechanism"]["seed"]))
NS = sorted({cases[n]["mechanism"]["n"] for n in names})

print("##### checks")
print("records", len(recs), "unique run_ids", len({r["run_id"] for r in recs}),
      "runs/ files", len(list((RUN / "runs").glob("*.json"))))
print("phase x mode counts", dict(Counter((r["phase"], r["mode"]) for r in recs)))
print("failures", [r["run_id"] for r in recs if S.failed(r)])
print("returncodes", dict(Counter(r.get("returncode") for r in recs)),
      "worker_status", dict(Counter(r.get("worker_status") for r in recs if r.get("worker_status"))))
print("primal check failed", [r["run_id"] for r in recs if (r.get("primal_check") or {}).get("passed") is False])
print("no checked incumbent (phase, mode)",
      dict(Counter((r["phase"], r["mode"]) for r in recs if (r.get("primal_check") or {}).get("checked") is not True)))
print("max scaled violation of checked incumbents",
      f(max((r["primal_check"].get("max_scaled_violation") or 0) for r in recs
            if (r.get("primal_check") or {}).get("checked")), 3))
print("flagged", {r["run_id"]: S.flags(r) for r in recs if S.flags(r)})
print("reference witness check failed",
      [r["run_id"] for r in recs if (r.get("reference_witness_check") or {}).get("passed") is False])
print("root timelimit", [r["run_id"] for r in recs if r["phase"] == "root" and r.get("status") == "timelimit"])
print("root runs without finite root_dual",
      [(short(r["name"]), r["mode"], r["status"]) for r in recs if r["phase"] == "root" and not S.finite(r.get("root_dual"))])
print("full runs without finite root_dual",
      [(short(r["name"]), r["mode"], r["status"], r.get("nodes")) for r in recs
       if r["phase"] == "full" and r["mode"] != "gurobi" and not S.finite(r.get("root_dual"))])
over = [(r["run_id"], round(S.seconds(r) - r["time_limit"], 3)) for r in recs if S.seconds(r) > r["time_limit"]]
print("soft budget overshoots", len(over), "max overshoot s", f(max((o for _, o in over), default=None)),
      "statuses", dict(Counter(index_r["status"] for index_r in recs if S.seconds(index_r) > index_r["time_limit"])))
print("worker hard timeout s", sorted({r["worker_timeout"] for r in recs}),
      "max outer_wall_seconds", f(max(r.get("outer_wall_seconds", 0) for r in recs)))
print("classifier errors", [r["run_id"] for r in recs if (r.get("row_binding_rejection_causes") or {}).get("classifier_errors")])
print("cut_log_complete false", [r["run_id"] for r in recs if r.get("separation") and r.get("cut_log_complete") is not True])
print("cuts recorded = separation.cuts",
      all(len(r["cuts"]) == r["separation"]["cuts"] for r in recs if r.get("separation")))
print("case known_optimum/reference_bound_ii equal c4-references",
      all(cases[n]["known_optimum"] == refs[n]["optimum"] and cases[n]["reference_bound_ii"] == refs[n]["bound_ii"]["value"]
          for n in names))

print("\n##### (e) references")
diffs, zeros, rows = [], [], []
for n in names:
    e = refs[n]
    c = Q(e["coupling"]["c"])
    ysum = sum((Q(y) for y in e["y_exact"]), Q(0))
    d = e["optimum_minus_bound_ii"]
    diffs.append(d)
    if d < 1e-40:
        zeros.append(short(n))
    rows.append((short(n), e["coupling"]["c"], e["coupling"]["sum_y_star"], e["coupling"]["binds"], ysum == c,
                 e["bound_ii"]["fractional_copies"], e["bound_ii"]["mu"], e["multiplier_exact"],
                 e["optimum_certificate"]["certified"], e["witness_primal_check"]["passed"], d))
for row in rows:
    print("  ", row)
print("optimum - bound(ii): min", f(min(diffs), 3), "median", f(med(diffs), 3), "max", f(max(diffs), 3),
      "below 1e-40:", len(zeros), zeros)
print("fractional_copies>0:", [short(n) for n in names if refs[n]["bound_ii"]["fractional_copies"]])
print("all binds", all(refs[n]["coupling"]["binds"] for n in names),
      "sum y_exact == c on", sum(Q(refs[n]["coupling"]["c"]) == sum((Q(y) for y in refs[n]["y_exact"]), Q(0)) for n in names))
print("c / sum_y_star range", f(min(float(Q(refs[n]["coupling"]["c"]) / Q(refs[n]["coupling"]["sum_y_star"])) for n in names)),
      f(max(float(Q(refs[n]["coupling"]["c"]) / Q(refs[n]["coupling"]["sum_y_star"])) for n in names)))
print("mu range", f(min(refs[n]["bound_ii"]["mu"] for n in names)), f(max(refs[n]["bound_ii"]["mu"] for n in names)))

print("\n##### (b) root runs")
print("root statuses by mode", {m: dict(Counter(index[("root", n, m)]["status"] for n in names)) for m in MODES})
print("root runs not nodelimit", [(short(n), m, index[("root", n, m)]["status"], index[("root", n, m)]["nodes"])
                                   for n in names for m in MODES if index[("root", n, m)]["status"] != "nodelimit"])
print("root run charged time, median [min, max] s:", {m: mmm([S.seconds(index[("root", n, m)]) for n in names], 4) for m in MODES})
rb = {(n, m): S.root_bound(index[("root", n, m)]) for n in names for m in MODES}
opt = {n: cases[n]["known_optimum"] for n in names}
b2 = {n: cases[n]["reference_bound_ii"] for n in names}
for m in MODES:
    print(f"root bound {m}: " + "; ".join(f"n={k} {mmm([rb[(n, m)] for n in names if cases[n]['mechanism']['n'] == k], 4)}" for k in NS))
for label, target in (("optimum", opt), ("bound_ii", b2)):
    for m in MODES[1:]:
        vals = {n: (rb[(n, m)] - rb[(n, "baseline")]) / (target[n] - rb[(n, "baseline")]) for n in names}
        per = "; ".join(f"n={k} {mmm([vals[n] for n in names if cases[n]['mechanism']['n'] == k])}" for k in NS)
        print(f"gap closed vs {label} {m}: {per}; all {mmm(list(vals.values()))}")
for m in MODES:
    d2 = {n: rb[(n, m)] - b2[n] for n in names}
    do = {n: rb[(n, m)] - opt[n] for n in names}
    above2 = [(short(n), f(d2[n], 3)) for n in names if d2[n] > 0]
    aboveo = [(short(n), f(do[n], 3)) for n in names if do[n] > 0]
    print(f"root - bound_ii {m}: min {f(min(d2.values()), 4)} ({short(min(d2, key=d2.get))}) max {f(max(d2.values()), 4)} "
          f"({short(max(d2, key=d2.get))}); per n: " + "; ".join(
              f"n={k} {mmm([d2[n] for n in names if cases[n]['mechanism']['n'] == k], 3)}" for k in NS)
          + f"; above bound_ii {above2}; above optimum {aboveo}")
print("full-run root bound (S.root_bound of the full record) - bound_ii, runs above bound_ii:")
for m in MODES:
    above = []
    for n in names:
        r = index[("full", n, m)]
        v = S.root_bound(r)
        if v is not None and v > b2[n]:
            above.append((short(n), f(v - b2[n], 3), "opt-b2", f(refs[n]["optimum_minus_bound_ii"], 3), "nodes", r["nodes"], r["status"]))
    print(f"  {m}: {above}")
print("gaplimit root runs detail:")
for n in names:
    for m in MODES:
        r = index[("root", n, m)]
        if r["status"] != "nodelimit":
            print("  ", short(n), m, r["status"], "root_dual", r.get("root_dual"), "dual", r["dual"], "primal", r["primal"],
                  "opt", opt[n], "b2", b2[n], "nodes", r["nodes"])
print("root_dual equal between root and full run (same mode):")
for m in MODES:
    same = [n for n in names if S.finite(index[("root", n, m)].get("root_dual")) and S.finite(index[("full", n, m)].get("root_dual"))
            and index[("root", n, m)]["root_dual"] == index[("full", n, m)]["root_dual"]]
    diff = [(short(n), f(index[("root", n, m)].get("root_dual"), 7), f(index[("full", n, m)].get("root_dual"), 7)) for n in names
            if not (S.finite(index[("root", n, m)].get("root_dual")) and S.finite(index[("full", n, m)].get("root_dual"))
                    and index[("root", n, m)]["root_dual"] == index[("full", n, m)]["root_dual"])]
    print(f"  {m}: equal {len(same)}; differ/missing {diff}")
for m in CUT_MODES:
    same_cuts = sum(json.dumps(index[("root", n, m)]["cuts"][-1]["row_certificate"]["exact"], sort_keys=True)
                    == json.dumps(index[("full", n, m)]["cuts"][-1]["row_certificate"]["exact"], sort_keys=True)
                    and len(index[("root", n, m)]["cuts"]) == len(index[("full", n, m)]["cuts"]) for n in names)
    same_sep = sum(all(index[("root", n, m)]["separation"][k] == index[("full", n, m)]["separation"][k]
                       for k in ("calls", "certification_calls", "cuts", "row_binding_rejections", "candidate_lps")) for n in names)
    print(f"  {m}: same separator counts root vs full {same_sep}/20; same cut count and last exact cut {same_cuts}/20")

print("\n##### (c) full runs")
FULL = MODES + ("gurobi",)
for m in FULL:
    rs = [index[("full", n, m)] for n in names]
    sol = [short(r["name"]) for r in rs if S.solved(r)]
    print(f"{m}: solved {len(sol)} statuses {dict(Counter(r['status'] for r in rs))} solved list {sol}; "
          f"median nodes all {f(med([r['nodes'] for r in rs]))}; nodes==1 solved "
          f"{[short(r['name']) for r in rs if S.solved(r) and r['nodes'] == 1]}")
    print(f"   time solved: {mmm([S.seconds(r) for r in rs if S.solved(r)], 4)}; max time {f(max(S.seconds(r) for r in rs))}")
common = [n for n in names if all(S.solved(index[("full", n, m)]) for m in FULL)]
print("common solved (all 5 modes):", [short(n) for n in common])
for m in FULL:
    rs = [index[("full", n, m)] for n in common]
    print(f"  {m}: SGM {f(S.sgm([S.seconds(r) for r in rs]))} SGM solver {f(S.sgm([S.solver_seconds(r) for r in rs]))} "
          f"SGM SCIP excl cb {f(S.sgm([S.scip_excluding_callback(r) for r in rs]))} SGM cb {f(S.sgm([S.callback(r) for r in rs]))} "
          f"median nodes {f(med([r['nodes'] for r in rs]))}")
common4 = [n for n in names if all(S.solved(index[("full", n, m)]) for m in MODES)]
print("common solved (4 SCIP modes):", [short(n) for n in common4])
for m in MODES:
    rs = [index[("full", n, m)] for n in common4]
    print(f"  {m}: SGM {f(S.sgm([S.seconds(r) for r in rs]))} median nodes {f(med([r['nodes'] for r in rs]))}")
both = {m: [n for n in names if S.solved(index[("full", n, m)]) and S.solved(index[("full", n, "baseline")])] for m in FULL}
for m in FULL[1:]:
    print(f"  pairs with baseline {m}: {len(both[m])}; SGM mode {f(S.sgm([S.seconds(index[('full', n, m)]) for n in both[m]]))} "
          f"SGM baseline {f(S.sgm([S.seconds(index[('full', n, 'baseline')]) for n in both[m]]))}")
cw = [n for n in names if all(S.solved(index[("full", n, m)]) for m in CUT_MODES)]
for m in CUT_MODES + ("baseline-extra",):
    rs = [index[("full", n, m)] for n in names if S.solved(index[("full", n, m)])]
    print(f"  {m} over its own solved: SGM {f(S.sgm([S.seconds(r) for r in rs]))}")
for rtol in (1e-4,):
    for m in FULL[1:]:
        out = defaultdict(list)
        for n in names:
            out[S.compare(index[("full", n, m)], index[("full", n, "baseline")], "dual", rtol)].append(short(n))
        print(f"  final dual vs baseline rtol {rtol} {m}: " + "; ".join(f"{k} {len(v)} {v if k in ('worse', 'unavailable', 'flagged') else ''}" for k, v in out.items()))
print("final dual - exact optimum, by mode (positive = above the optimum):")
for m in FULL:
    above = []
    for n in names:
        r = index[("full", n, m)]
        d = float(Q(r["dual"]) - Q(refs[n]["optimum_exact"]))
        if d > 0:
            above.append((short(n), f(d, 3)))
    gaps = [float(Q(index[("full", n, m)]["dual"]) - Q(refs[n]["optimum_exact"])) for n in names]
    print(f"  {m}: above optimum {above}; dual - opt over solved {mmm([g for n, g in zip(names, gaps) if S.solved(index[('full', n, m)])], 3)}; "
          f"over unsolved {mmm([g for n, g in zip(names, gaps) if not S.solved(index[('full', n, m)])], 3)}")
    pbelow = [(short(n), f(float(Q(index[("full", n, m)]["primal"]) - Q(refs[n]["optimum_exact"])), 3)) for n in names
              if S.finite(index[("full", n, m)].get("primal")) and Q(index[("full", n, m)]["primal"]) < Q(refs[n]["optimum_exact"])]
    print(f"     incumbent below exact optimum: {pbelow}")
    above2 = [(short(n), f(index[("full", n, m)]["dual"] - b2[n], 3)) for n in names if index[("full", n, m)]["dual"] > b2[n]
              and refs[n]["optimum_minus_bound_ii"] > 1e-40]
    print(f"     final dual above bound_ii where bound_ii < optimum: {above2}")
print("gurobi details (name, status, gurobi_status_name, primal-opt, dual-opt, mip_gap, time, nodes, primal check max viol):")
for n in names:
    r = index[("full", n, "gurobi")]
    o = Q(refs[n]["optimum_exact"])
    print("  ", short(n), r["status"], r.get("gurobi_status_name"), f(float(Q(r["primal"]) - o), 3), f(float(Q(r["dual"]) - o), 3),
          f(r.get("mip_gap"), 3), f(S.seconds(r), 4), r["nodes"], f((r.get("primal_check") or {}).get("max_scaled_violation"), 2))
    print("     gurobi params", r.get("gurobi_params") if n == names[0] else "")

print("\n##### (d) funnel, caps, time")
for phase in ("root", "full"):
    for m in CUT_MODES:
        rs = [index[(phase, n, m)] for n in names]
        fu = S.funnel(rs)
        print(f"{phase} {m}: callbacks {fu['calls']} support {fu['certification_calls']} certfail {fu['certification_failures']} "
              f"rounding {fu['row_rounding_rejections']} binding {fu['row_binding_rejections']} (runs {fu['runs_with_binding_rejections']}) "
              f"causes {fu['row_binding_rejection_causes']} varstatus {fu['rejected_row_variable_statuses']} below {fu['below_violation_threshold']} "
              f"cuts {fu['cuts']} candidate_lps {fu['candidate_lps']} sampling_failures {fu['sampling_failures']} repeat_skips {fu['repeat_skips']} "
              f"exchange_samples {fu['exchange_samples']} budget_exhausted runs {fu['budget_exhausted_runs']} discovery_incomplete {fu['discovery_incomplete_runs']}")
        caps = Counter()
        for r in rs:
            s, c = r["separation"], r["config"]
            budget = min(c["max_separation_seconds"], c["separation_budget_fraction"] * r["time_limit"])
            hit = []
            if s["cuts"] >= c["max_cuts"]:
                hit.append("cuts")
            if s["certification_calls"] >= c["max_support_calls"]:
                hit.append("support")
            if s["calls"] >= c["max_rounds"]:
                hit.append("rounds")
            if s["callback_seconds"] >= budget:
                hit.append("time")
            caps[tuple(hit)] += 1
            caps["budget_" + f(budget)] += 1
        print(f"   caps (combination: runs): {dict(caps)}")
        print(f"   per run: callbacks {mmm([r['separation']['calls'] for r in rs])}; support calls / max "
              f"{mmm([r['separation']['certification_calls'] / r['config']['max_support_calls'] for r in rs])}; "
              f"cuts/max {mmm([r['separation']['cuts'] / r['config']['max_cuts'] for r in rs])}; callback s {mmm([r['separation']['callback_seconds'] for r in rs], 4)}; "
              f"max_cuts=16n {all(r['config']['max_cuts'] == 16 * cases[r['name']]['mechanism']['n'] for r in rs)}; "
              f"max_support_calls=40n {all(r['config']['max_support_calls'] == 40 * cases[r['name']]['mechanism']['n'] for r in rs)}; "
              f"max_cuts_per_round=4n {all(r['config']['max_cuts_per_round'] == 4 * cases[r['name']]['mechanism']['n'] for r in rs)}; "
              f"max_rounds {sorted({r['config']['max_rounds'] for r in rs})}; row_directions {sorted({r['config']['row_directions'] for r in rs})}")
        td = S.time_decomposition(rs)
        print(f"   time sums: charged {td['sum_seconds']:.1f} SCIP {td['sum_solver_seconds']:.1f} SCIP excl cb "
              f"{td['sum_solver_seconds_excluding_callback']:.1f} callback {td['sum_callback_seconds']:.1f} discovery {td['sum_discovery_seconds']:.1f} "
              f"candidate {td['sum_candidate_seconds']:.1f} certification {td['sum_certification_seconds']:.1f} rows {td['sum_row_seconds']:.1f}; "
              f"SGM charged {f(td['sgm_seconds'])} SCIP excl cb {f(td['sgm_solver_seconds_excluding_callback'])} cb {f(td['sgm_callback_seconds'])}; "
              f"callback share of charged {td['sum_callback_seconds'] / td['sum_seconds']:.3f}")
    for m in ("baseline", "baseline-extra"):
        rs = [index[(phase, n, m)] for n in names]
        td = S.time_decomposition(rs)
        print(f"{phase} {m}: SGM charged {f(td['sgm_seconds'])} SGM SCIP {f(td['sgm_solver_seconds'])} sums {td['sum_seconds']:.1f}")

print("time decomposition against baseline (pairs completed (root) or solved (full) by the mode and baseline):")
for phase in ("root", "full"):
    for m in CUT_MODES + ("baseline-extra",):
        common = [n for n in names if S.completed(index[(phase, n, m)], phase) and S.completed(index[(phase, n, "baseline")], phase)]
        rs = [index[(phase, n, m)] for n in common]
        rr = [index[(phase, n, "baseline")] for n in common]
        excl = [S.scip_excluding_callback(r) for r in rs]
        print(f"  {phase} {m} ({len(common)}): SGM total {f(S.sgm([S.seconds(r) for r in rs]))} SGM SCIP excl cb {f(S.sgm(excl))} "
              f"SGM cb {f(S.sgm([S.callback(r) for r in rs]))}; baseline SGM total {f(S.sgm([S.seconds(r) for r in rr]))} "
              f"SCIP {f(S.sgm([S.solver_seconds(r) for r in rr]))}; median SCIP-excl / baseline SCIP "
              f"{f(med([a / max(S.solver_seconds(b), 1e-9) for a, b in zip(excl, rr)]))}; median total / baseline "
              f"{f(med([S.seconds(a) / S.seconds(b) for a, b in zip(rs, rr)]))}")
print("full runs whose root_dual differs from the root run, and FIXED original variables at the end (native_statistics):")
for m in MODES:
    differ = [n for n in names if index[("full", n, m)].get("root_dual") != index[("root", n, m)].get("root_dual")]
    fixed_full = sum(1 for n in names if index[("full", n, m)]["native_statistics"]["original_variable_status"].get("FIXED", 0))
    fixed_root = sum(1 for n in names if index[("root", n, m)]["native_statistics"]["original_variable_status"].get("FIXED", 0))
    no_fixed = [short(n) for n in differ if not index[("full", n, m)]["native_statistics"]["original_variable_status"].get("FIXED", 0)]
    print(f"  {m}: differ {len(differ)} {[short(n) for n in differ]}; full runs with FIXED {fixed_full}; root runs with FIXED {fixed_root}; "
          f"differing without FIXED {no_fixed}")
for m in CUT_MODES:
    same = sum(json.dumps([(c["row_certificate"]["exact"], c["rhs"], c["block"]) for c in index[("root", n, m)]["cuts"]], sort_keys=True)
               == json.dumps([(c["row_certificate"]["exact"], c["rhs"], c["block"]) for c in index[("full", n, m)]["cuts"]], sort_keys=True)
               for n in names)
    print(f"  {m}: identical cut lists (exact row, rhs, block) in root and full run: {same}/20")
print("median nodes, all 20 full runs:", {m: med([index[("full", n, m)]["nodes"] for n in names]) for m in FULL})

print("\n##### (f) cut directions")


def classify(cut, var_names):
    a = cut["coefficients"]
    d = len(cut["variables"])
    lam = [Q(x) for x in a[d:]]
    side = cut["signed_sides"][0]
    aff = {k: Q(v) for k, v in side["affine_terms"]}
    syms = cut["symbols"]
    if len(cut["signed_sides"]) != 1 or len(lam) != 1:
        return "multi", None
    row_dir = all(Q(a[k]) == lam[0] * aff.get(syms[k], Q(0)) for k in range(d))
    if all(x == 0 for x in a[:d]):
        cls = "remainder"
    elif row_dir:
        cls = "row"
    else:
        cls = "other"
    exact = [Q(x) for x in cut["row_certificate"]["exact"]["coefficients"]]
    roles = {}
    for k, vi in enumerate(cut["variables"]):
        roles[var_names[vi].split("_")[0]] = exact[vi]
    tname = [k for k, v in aff.items() if v == -1 and k not in syms]
    ti = int(tname[0][1:]) if tname else None
    roles["t"] = exact[ti] if ti is not None else None
    nonzero_outside = [i for i, c in enumerate(exact) if c != 0 and i not in cut["variables"] and i != ti]
    return cls, {"roles": roles, "outside": nonzero_outside, "ay_minus_lam_affy": Q(a[1]) - lam[0] * aff.get(syms[1], Q(0)),
                 "lam": lam[0], "aff_y": aff.get(syms[1], Q(0))}


for phase in ("root", "full"):
    for m in CUT_MODES:
        cnt = Counter()
        slopes = defaultdict(list)
        per_run_other = []
        per_block_other = Counter()
        for n in names:
            r = index[(phase, n, m)]
            vn = r["original_model"]["var_names"]
            assert all(vn[4 * i:4 * i + 4] == [f"x_{i + 1}", f"y_{i + 1}", f"z_{i + 1}", f"t_{i + 1}"] for i in range(len(vn) // 4))
            k_other = 0
            blocks_with_other = set()
            for cut in r["cuts"]:
                cls, info = classify(cut, vn)
                cnt[(cls,)] += 1
                if info is None:
                    continue
                ro = info["roles"]
                ynz = ro["y"] != 0
                cnt[(cls, "y!=0" if ynz else "y=0")] += 1
                cnt[(cls, "x,z=0" if ro["x"] == 0 and ro["z"] == 0 else "x or z !=0")] += 1
                cnt[(cls, "pattern", "".join(v for v in ("x", "y", "z") if ro[v] != 0) or "-")] += 1
                cnt[("ay-lam*affy == exported y", info["ay_minus_lam_affy"] == ro["y"])] += 1
                cnt[("outside nonzero", bool(info["outside"]))] += 1
                cnt[("t coef > 0", ro["t"] is not None and ro["t"] > 0)] += 1
                if ro["t"] and ro["t"] > 0:
                    slopes[cls].append(float(-ro["y"] / ro["t"]))
                if cls == "other":
                    k_other += 1
                    blocks_with_other.add(cut["block"])
            per_run_other.append((short(n), k_other, len(r["cuts"]), len(blocks_with_other), cases[n]["mechanism"]["n"]))
        print(f"{phase} {m}: {dict(sorted(cnt.items(), key=str))}")
        for cls, v in slopes.items():
            q = statistics.quantiles(v, n=4) if len(v) > 1 else [None] * 3
            print(f"   y-slope (-coef_y/coef_t) {cls}: n {len(v)} min {f(min(v))} q1 {f(q[0])} median {f(med(v))} q3 {f(q[2])} max {f(max(v))} "
                  f"zero {sum(1 for x in v if x == 0)} negative {sum(1 for x in v if x < 0)} positive {sum(1 for x in v if x > 0)}")
        print(f"   per run (name, other cuts, cuts, blocks with an other cut, n): {per_run_other}")

print("bound of the row-direction cuts alone, sum_i min phi_i = optimum of the C3 instance with the same triples "
      "(runs/partC3/cases known_optimum; the C3 coupling row does not bind):")
closed = {}
for n in names:
    k, sd = cases[n]["mechanism"]["n"], cases[n]["mechanism"]["seed"]
    lo = json.loads((V4 / f"runs/partC3/cases/interleaved_path_n{k}_s{sd}.json").read_text())["known_optimum"]
    base = rb[(n, "baseline")]
    closed[n] = (lo - base) / (opt[n] - base)
    assert all(rb[(n, m)] > lo for m in CUT_MODES)
print("  gap closed vs optimum by sum min phi: " + "; ".join(
    f"n={k} {mmm([closed[n] for n in names if cases[n]['mechanism']['n'] == k])}" for k in NS) + f"; all {mmm(list(closed.values()))}")
print("  sum min phi below the baseline root bound on", sum(1 for v in closed.values() if v < 0), "instances; "
      "every frozen-wide and rowdir-wide root bound is above sum min phi (asserted)")

print("\n##### (a) replay")
rp = RUN / "replay.json"
if rp.exists():
    j = json.loads(rp.read_text())
    v4 = j.get("v4", {})
    print({k: j.get(k) for k in ("passed", "archived_passed", "records", "bound_runs", "admitted_runs", "cuts", "replayed_cuts",
                                 "missing_cut_logs", "replay_seconds", "wrapper_seconds", "source_files_verified",
                                 "replay_source_sha256", "wrapper_source_sha256")})
    print({k: v4.get(k) for k in ("coverage_complete", "config_failures", "config_checked_runs", "gurobi_failures",
                                  "gurobi_checked_runs", "modes_with_cuts", "tamper_controls_cover_all_cut_modes", "tamper_scope")})
    print("failed runs", [x.get("run_id") for x in j.get("runs", []) if x.get("passed") is False])
    print("omitted runs", len(j.get("omitted_runs", [])), dict(Counter(x.get("status") for x in j.get("omitted_runs", []))),
          "omitted cuts", sum(x.get("cuts", 0) or 0 for x in j.get("omitted_runs", [])))
    print("tamper_rejections", j.get("tamper_rejections"))
    for mode, t in (v4.get("tamper_controls_by_mode") or {}).items():
        rej = t.get("rejections") or {}
        print("  tamper", mode, t.get("run_id"), t.get("cuts_in_record"), t.get("untampered_first_cut_passed"),
              f"{sum(bool(x) for x in rej.values())} of {len(rej)}" if isinstance(rej, dict) else rej)
else:
    print("replay.json not present")
