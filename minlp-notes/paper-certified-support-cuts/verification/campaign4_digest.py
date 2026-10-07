"""Campaign-4 digest numbers (evidence/campaign4-digest.md).

    PY campaign4_digest.py {C2|C3|B2|D|caps}

Read-only: loads records.jsonl and cases of the finished campaign-4 parts
(experiments/v4/runs/partC2, partC3, partB2, partD-root, partD-full), the
campaign-3 references (experiments/v3/runs/partC, partB) and the v3d diagnostic
(experiments/v3d/runs/partC-rowdir), and reuses the definitions of
experiments/v4/summarize_v4.py (imported, not modified): root bound, solved,
SGM (shift 1 s), bound comparison, SCIP time excluding the callback, funnel.
Adds per-n medians with min/max, per-model lists, the v3d cells of the C2 2x2
design, Gurobi details, and separator cap counts. Does not read partC4.
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[2])

import json, math, statistics, sys
from pathlib import Path
from collections import Counter, defaultdict
V4 = Path((_PUBLIC_REPO + '/paper-certified-support-cuts/experiments/v4'))
sys.path.insert(0, str(V4))
import summarize_v4 as S

def load(d):
    d = Path(d)
    return [json.loads(l) for l in (d / "records.jsonl").read_text().splitlines() if l]
def cases(d):
    return {p.stem: json.loads(p.read_text()) for p in (Path(d) / "cases").glob("*.json")}
def idx(recs, prefix=""):
    return {(r["phase"], r["name"], prefix + r["mode"]): r for r in recs}
def med(v): return statistics.median(v) if v else None
def rng(v): return (min(v), max(v)) if v else (None, None)
def f(x, d=4):
    if x is None: return "-"
    if isinstance(x, float): return f"{x:.{d}g}"
    return str(x)
def mmm(v, d=3):
    if not v: return "-"
    return f"{f(med(v),d)} [{f(min(v),d)}, {f(max(v),d)}]"

part = sys.argv[1]
print("#####", part)

RUNS = V4 / "runs"
V3 = V4.parent / "v3" / "runs"
V3D = V4.parent / "v3d" / "runs"

def path_root_table(index, cs, modes, base_key, extra_keys=()):
    """Per-instance root bound, gap closed vs base, residual; grouped by n."""
    rows = []
    for name, c in cs.items():
        opt = c["known_optimum"]; n = c["mechanism"]["n"]
        base = S.root_bound(index.get(("root", name, base_key)))
        row = {"name": name, "n": n, "opt": opt, "base": base, "rb": {}, "gc": {}, "res": {}}
        for m in modes:
            rb = 0.0 if m == "pair-hull" else S.root_bound(index.get(("root", name, m)))
            row["rb"][m] = rb
            if rb is not None and base is not None:
                row["gc"][m] = (rb - base) / (opt - base)
                row["res"][m] = rb / opt
        rows.append(row)
    return sorted(rows, key=lambda r: (r["n"], r["name"]))

def by_n(rows, field, m):
    out = {}
    for n in sorted({r["n"] for r in rows}):
        out[n] = [r[field][m] for r in rows if r["n"] == n and m in r[field]]
    return out

def print_root(rows, modes):
    for field, label in (("gc", "root gap closed vs base"), ("res", "residual closure root/opt")):
        print(f"-- {label}: median [min, max] per n; all")
        for m in modes:
            g = by_n(rows, field, m)
            allv = [v for vs in g.values() for v in vs]
            print(f"  {m}: " + "; ".join(f"n={n} {mmm(v)}" for n, v in g.items()) + f"; all20 {mmm(allv)}")
    print("-- root bound median [min,max] per n")
    for m in ["base"] + list(modes):
        if m == "base":
            g = {n: [r["base"] for r in rows if r["n"] == n] for n in sorted({r["n"] for r in rows})}
        else:
            g = {n: [r["rb"][m] for r in rows if r["n"] == n and r["rb"][m] is not None] for n in sorted({r["n"] for r in rows})}
        print(f"  {m}: " + "; ".join(f"n={n} {mmm(v,4)}" for n, v in g.items()))

def full_summary(index, names, modes, cs=None):
    print("-- full: solved per mode")
    for m in modes:
        rs = [index.get(("full", n, m)) for n in names]
        sol = [n for n, r in zip(names, rs) if r and S.solved(r)]
        st = Counter(r.get("status") for r in rs if r)
        print(f"  {m}: solved {len(sol)}/{len(names)} statuses {dict(st)} missing {sum(r is None for r in rs)}")
        print(f"     solved: {sorted(sol, key=lambda s: (int(s.split('_n')[1].split('_')[0]) if '_n' in s else 0, s))}")
        nodes_all = [r["nodes"] for r in rs if r and isinstance(r.get("nodes"), int)]
        print(f"     median nodes all runs {f(med(nodes_all))} [{f(min(nodes_all))}, {f(max(nodes_all))}]")
    common = [n for n in names if all(index.get(("full", n, m)) and S.solved(index[("full", n, m)]) for m in modes)]
    print(f"  common solved by all {len(modes)} modes: {len(common)}: {common}")
    for m in modes:
        rs = [index[("full", n, m)] for n in common]
        print(f"   {m}: SGM total {f(S.sgm([S.seconds(r) for r in rs]))} SGM SCIP {f(S.sgm([S.solver_seconds(r) for r in rs]))}"
              f" SGM SCIP excl cb {f(S.sgm([S.scip_excluding_callback(r) for r in rs]))} median nodes {f(med([r['nodes'] for r in rs]))}")
    return common

def pairwise_sgm(index, names, a, b):
    common = [n for n in names if index.get(("full", n, a)) and S.solved(index[("full", n, a)])
              and index.get(("full", n, b)) and S.solved(index[("full", n, b)])]
    ra = [index[("full", n, a)] for n in common]; rb = [index[("full", n, b)] for n in common]
    return len(common), S.sgm([S.seconds(r) for r in ra]), S.sgm([S.seconds(r) for r in rb]), \
        med([r["nodes"] for r in ra]), med([r["nodes"] for r in rb])

def gurobi_table(index, names, cs):
    print("-- gurobi per instance: status, gurobi status name, primal, dual, mip_gap, dual-opt, primal-opt, seconds, nodes, primal check")
    for n in names:
        r = index.get(("full", n, "gurobi"))
        if r is None: print("  ", n, "MISSING"); continue
        opt = cs[n]["known_optimum"]
        pc = r.get("primal_check") or {}
        print(f"  {n}: {r['status']} ({r.get('gurobi_status_name')}) primal {f(r.get('primal'),8)} dual {f(r.get('dual'),8)} "
              f"mip_gap {f(r.get('mip_gap'),3)} dual-opt {f(r['dual']-opt if S.finite(r.get('dual')) else None,3)} "
              f"primal-opt {f(r['primal']-opt if S.finite(r.get('primal')) else None,3)} t {f(S.seconds(r),4)} nodes {r.get('nodes')} "
              f"pc {pc.get('checked')}/{pc.get('passed')} viol {f(pc.get('max_scaled_violation'),2)} ref {(r.get('reference_check') or {}).get('dual_consistent')}")

def caps(rows):
    """Runs hitting each cap: budget_exhausted, discovery_incomplete, cuts==max_cuts, support calls>=max, callbacks>=max_rounds."""
    c = Counter()
    for r in rows:
        s = r.get("separation") or {}; cfg = r.get("config") or {}
        if not s: continue
        c["runs"] += 1
        c["budget_exhausted"] += bool(s.get("budget_exhausted"))
        c["discovery_incomplete"] += bool(s.get("discovery_incomplete"))
        if cfg.get("max_cuts") is not None and s.get("cuts", 0) >= cfg["max_cuts"]: c["cut_cap"] += 1
        if cfg.get("max_support_calls") is not None and s.get("certification_calls", 0) >= cfg["max_support_calls"]: c["support_cap"] += 1
        if cfg.get("max_rounds") is not None and s.get("calls", 0) >= cfg["max_rounds"]: c["round_cap"] += 1
    return dict(c)

def extra_checks(recs, label):
    pcf = [r["run_id"] for r in recs if (r.get("primal_check") or {}).get("passed") is False]
    noinc = Counter((r["mode"], r["phase"]) for r in recs if (r.get("primal_check") or {}).get("checked") is not True)
    fails = [r["run_id"] for r in recs if S.failed(r)]
    flagged = {r["run_id"]: S.flags(r) for r in recs if S.flags(r)}
    over = [(r["run_id"], round(S.seconds(r), 2), r["time_limit"]) for r in recs if "total_seconds" in r and S.seconds(r) > r["time_limit"] + 0.01]
    rootTL = [r["run_id"] for r in recs if r["phase"] == "root" and r.get("status") == "timelimit"]
    clerr = [r["run_id"] for r in recs if (r.get("row_binding_rejection_causes") or {}).get("classifier_errors")]
    nonfin_root = [r["run_id"] for r in recs if r["phase"] == "root" and not S.finite(r.get("root_dual"))]
    print(f"-- checks {label}: records {len(recs)}; failures {fails}; primal check failed {pcf}; flagged {flagged}; "
          f"overshoots {over}; root timelimit {rootTL}; classifier errors {clerr}")
    print(f"   no incumbent checked (mode, phase): {dict(noinc)}")
    print(f"   root runs without finite root_dual: {nonfin_root}")
    reasons = Counter(r.get('worker_status') for r in recs if r.get('worker_status'))
    print(f"   worker_status values: {dict(reasons)}; returncodes: {dict(Counter(r.get('returncode') for r in recs))}")

def time_rows(index, names, phase, modes, ref):
    """Common pairs (completed by every listed mode); SGM total, SCIP, SCIP excl cb, cb; median ratio of SCIP excl cb (m) to SCIP (ref)."""
    common = [n for n in names if all(S.completed(index.get((phase, n, m)), phase) for m in modes)]
    print(f"-- time decomposition {phase}: {len(common)} common pairs (modes {modes}); reference {ref}")
    for m in modes:
        rs = [index[(phase, n, m)] for n in common]
        rr = [index[(phase, n, ref)] for n in common]
        excl = [S.scip_excluding_callback(r) for r in rs]
        ratio_excl = [a / max(S.solver_seconds(b), 1e-9) for a, b in zip(excl, rr)]
        ratio_tot = [S.seconds(a) / max(S.seconds(b), 1e-9) for a, b in zip(rs, rr)]
        print(f"   {m}: SGM total {f(S.sgm([S.seconds(r) for r in rs]))}; SGM SCIP {f(S.sgm([S.solver_seconds(r) for r in rs]))}; "
              f"SGM SCIP excl cb {f(S.sgm(excl))}; SGM cb {f(S.sgm([S.callback(r) for r in rs]))}; "
              f"median ratio SCIPexcl/refSCIP {f(med(ratio_excl))}; median ratio total/ref {f(med(ratio_tot))}; median nodes {f(med([r.get('nodes') for r in rs if isinstance(r.get('nodes'), int)]))}")

def funnel_print(rows, label):
    fu = S.funnel(rows); cp = caps(rows)
    print(f"   {label}: runs {len(rows)} callbacks {fu['calls']} support {fu['certification_calls']} certfail {fu['certification_failures']} "
          f"certified {fu['certified_supports']} rounding {fu['row_rounding_rejections']} below {fu['below_violation_threshold']} "
          f"binding {fu['row_binding_rejections']} (runs {fu['runs_with_binding_rejections']}) causes {fu['row_binding_rejection_causes']} "
          f"varstatus {fu['rejected_row_variable_statuses']} cuts {fu['cuts']} caps {cp}")
    td = S.time_decomposition(rows)
    print(f"      sums: callback {td['sum_callback_seconds']:.1f} discovery {td['sum_discovery_seconds']:.1f} candidate {td['sum_candidate_seconds']:.1f} "
          f"certification {td['sum_certification_seconds']:.1f} rows {td['sum_row_seconds']:.1f}")

if part == "C2":
    recs = load(RUNS / "partC2"); c3 = load(V3 / "partC"); v3d = load(V3D / "partC-rowdir")
    cs = cases(RUNS / "partC2")
    index = idx(recs); index.update(idx(c3, "c3:")); index.update(idx(v3d, "v3d:"))
    names = sorted(cs, key=lambda s: (cs[s]["mechanism"]["n"], s))
    # v3d baseline root == c3 baseline root?
    diffs = [(n, S.root_bound(index[("root", n, "c3:baseline")]), S.root_bound(index[("root", n, "v3d:baseline")])) for n in names
             if S.root_bound(index[("root", n, "c3:baseline")]) != S.root_bound(index[("root", n, "v3d:baseline")])]
    print("v3d baseline root differs from c3 baseline root:", diffs)
    v3dc = cases(V3D / "partC-rowdir"); print("v3d cases equal C2 cases:", all(v3dc[n] == cs[n] for n in names), len(v3dc))
    modes = ["baseline-novarlocks", "baseline-extra", "frozen-wide", "c3:all-diag-mech", "v3d:all-diag-mech", "v3d:all-diag-mech-wide", "pair-hull"]
    rows = path_root_table(index, cs, modes, "c3:baseline")
    print_root(rows, modes)
    print("-- per instance root (base, novarlocks, extra, frozen-wide, c3 mech, v3d mech, v3d wide)")
    for r in rows:
        print(f"  {r['name']}: opt {f(r['opt'],6)} base {f(r['base'],6)} " + " ".join(f"{m}={f(r['rb'][m],6)}({f(r['gc'].get(m),3)})" for m in modes[:-1]))
    print("-- root runs solved at root (status optimal/gaplimit) per mode")
    for m in ["c3:baseline"] + modes[:-1]:
        print(f"   {m}: {sum(S.solved(index[('root', n, m)]) for n in names)} statuses {dict(Counter(index[('root', n, m)]['status'] for n in names))}")
    fm = ["c3:baseline", "c3:all-diag-mech", "baseline-novarlocks", "baseline-extra", "frozen-wide", "gurobi"]
    full_summary(index, names, fm)
    print("-- pairwise SGM vs c3:baseline (pairs, SGM mode, SGM c3:baseline, median nodes mode, median nodes base)")
    for m in fm[1:]:
        print(f"   {m}: {pairwise_sgm(index, names, m, 'c3:baseline')}")
    print("-- 2x2 full")
    for m in ["c3:all-diag-mech", "frozen-wide", "v3d:all-diag-mech", "v3d:all-diag-mech-wide", "v3d:baseline", "c3:baseline"]:
        sol = [n for n in names if S.solved(index[("full", n, m)])]
        print(f"   {m}: solved {len(sol)}/20: {sol}")
        print(f"      root-node solved (root phase): {sum(S.solved(index[('root', n, m)]) for n in names)}")
    print("-- 2x2 root gap closed medians per n (vs c3 baseline)")
    for m in ["c3:all-diag-mech", "frozen-wide", "v3d:all-diag-mech", "v3d:all-diag-mech-wide"]:
        g = by_n(rows, "gc", m)
        print(f"   {m}: " + "; ".join(f"n={n} {mmm(v)}" for n, v in g.items()))
    gurobi_table(index, names, cs)
    print("-- final dual vs opt, max excess (dual - opt) per mode, full")
    for m in fm:
        ex = [(index[("full", n, m)]["dual"] - cs[n]["known_optimum"], n) for n in names if S.finite(index[("full", n, m)].get("dual"))]
        print(f"   {m}: max dual-opt {f(max(ex)[0],3)} at {max(ex)[1]}; count dual>opt {sum(e > 0 for e, _ in ex)}")
    print("-- full bound comparison (1e-4) vs c3:baseline, worse list")
    for m in fm[1:]:
        for rt in (1e-4, 1e-6):
            out = Counter(); worse = []
            for n in names:
                o = S.compare(index[("full", n, m)], index[("full", n, "c3:baseline")], "dual", rt); out[o] += 1
                if o == "worse": worse.append(n)
            print(f"   {m} rtol {rt}: {dict(out)} worse {worse}")
    print("-- funnel")
    for m in ["c3:all-diag-mech", "frozen-wide", "v3d:all-diag-mech", "v3d:all-diag-mech-wide"]:
        for ph in ("root", "full"):
            funnel_print([index[(ph, n, m)] for n in names], f"{m} {ph}")
    time_rows(index, names, "root", ["c3:baseline", "c3:all-diag-mech", "baseline-novarlocks", "baseline-extra", "frozen-wide"], "c3:baseline")
    time_rows(index, names, "full", fm, "c3:baseline")
    for m in ["c3:all-diag-mech", "frozen-wide"]:
        time_rows(index, names, "full", ["c3:baseline", m], "c3:baseline")
    print("-- load_start mean per mode (C2 runs vs c3)")
    for m in fm:
        L = [index[("full", n, m)]["load_start"][0] for n in names if "load_start" in index[("full", n, m)]]
        print(f"   {m} full: mean load {f(statistics.fmean(L),3)}")
    extra_checks(recs, "partC2")

if part == "C3":
    recs = load(RUNS / "partC3"); cs = cases(RUNS / "partC3")
    index = idx(recs)
    names = sorted(cs, key=lambda s: (cs[s]["mechanism"]["n"], s))
    modes = ["baseline-extra", "all-diag-mech", "rowdir-wide", "pair-hull"]
    rows = path_root_table(index, cs, modes, "baseline")
    print_root(rows, modes)
    print("-- rowdir-wide root: bound - opt per instance, status, nodes")
    for r in rows:
        x = index[("root", r["name"], "rowdir-wide")]
        print(f"  {r['name']}: rb-opt {f(r['rb']['rowdir-wide'] - r['opt'],3)} status {x['status']} root_dual {f(x.get('root_dual'),8)} dual {f(x.get('dual'),8)} nodes {x.get('nodes')} t {f(S.seconds(x),4)}")
    print("-- root runs solved at root per mode")
    for m in ["baseline", "baseline-extra", "all-diag-mech", "rowdir-wide"]:
        print(f"   {m}: {sum(S.solved(index[('root', n, m)]) for n in names)} statuses {dict(Counter(index[('root', n, m)]['status'] for n in names))}")
    fm = ["baseline", "all-diag-mech", "rowdir-wide", "baseline-extra", "gurobi"]
    full_summary(index, names, fm)
    print("-- pairwise SGM vs baseline (pairs, SGM mode, SGM baseline, median nodes mode, median nodes base)")
    for m in fm[1:]:
        print(f"   {m}: {pairwise_sgm(index, names, m, 'baseline')}")
    print("-- rowdir-wide full per instance: status, t, nodes, cb")
    for n in names:
        x = index[("full", n, "rowdir-wide")]
        print(f"   {n}: {x['status']} t {f(S.seconds(x),4)} nodes {x['nodes']} cb {f(S.callback(x),4)} scip_excl {f(S.scip_excluding_callback(x),3)}")
    gurobi_table(index, names, cs)
    print("-- final dual vs opt, primal vs opt per mode, full")
    for m in fm:
        ex = [(index[("full", n, m)]["dual"] - cs[n]["known_optimum"], n) for n in names if S.finite(index[("full", n, m)].get("dual"))]
        px = [(index[("full", n, m)]["primal"] - cs[n]["known_optimum"], n) for n in names if S.finite(index[("full", n, m)].get("primal"))]
        print(f"   {m}: max dual-opt {f(max(ex)[0],3)} at {max(ex)[1]}; count dual>opt {sum(e > 0 for e, _ in ex)}; min primal-opt {f(min(px)[0],3)} at {min(px)[1]}")
    print("-- full bound comparison vs baseline, worse list")
    for m in fm[1:]:
        for rt in (1e-4, 1e-6):
            out = Counter(); worse = []
            for n in names:
                o = S.compare(index[("full", n, m)], index[("full", n, "baseline")], "dual", rt); out[o] += 1
                if o == "worse": worse.append(n)
            print(f"   {m} rtol {rt}: {dict(out)} worse {worse}")
    print("-- funnel")
    for m in ["all-diag-mech", "rowdir-wide"]:
        for ph in ("root", "full"):
            funnel_print([index[(ph, n, m)] for n in names], f"{m} {ph}")
    time_rows(index, names, "root", ["baseline", "baseline-extra", "all-diag-mech", "rowdir-wide"], "baseline")
    time_rows(index, names, "full", fm, "baseline")
    for m in ["all-diag-mech", "rowdir-wide", "baseline-extra"]:
        time_rows(index, names, "full", ["baseline", m], "baseline")
    extra_checks(recs, "partC3")

if part == "B2":
    recs = load(RUNS / "partB2"); c3 = [r for r in load(V3 / "partB") if r["phase"] == "root"]
    cs = cases(RUNS / "partB2")
    index = idx(recs); index.update(idx(c3, "c3:"))
    names = [j["name"] for j in json.loads((RUNS / "partB2" / "jobs.json").read_text())["jobs"]]
    names = list(dict.fromkeys(names))
    print("models", len(names))
    cut_modes = ["c3:all", "c3:auto", "c3:all-diag", "all-noaggr", "all-diag-noaggr", "all-diag-rowdir-noaggr"]
    print("-- funnel")
    for m in cut_modes:
        funnel_print([index[("root", n, m)] for n in names], m)
    print("-- per model: binding rejections / cuts (c3:all, all-noaggr, c3:all-diag, all-diag-noaggr, all-diag-rowdir-noaggr) and causes in noaggr modes")
    for n in names:
        cells = []
        for m in ["c3:all", "all-noaggr", "c3:all-diag", "all-diag-noaggr", "all-diag-rowdir-noaggr"]:
            s = index[("root", n, m)].get("separation") or {}
            cells.append(f"{s.get('row_binding_rejections', 0)}/{s.get('cuts', 0)}")
        causes = {m: (index[("root", n, m)].get("row_binding_rejection_causes") or {}).get("causes") for m in ["all-noaggr", "all-diag-noaggr"]}
        vs = {m: (index[("root", n, m)].get("row_binding_rejection_causes") or {}).get("variable_statuses") for m in ["all-noaggr", "all-diag-noaggr"]}
        if any(c != "0/0" for c in cells):
            print(f"  {n}: {' | '.join(cells)} causes {causes} varstatus {vs}")
    print("-- presolve status of original variables, baseline-noaggr runs with non-COLUMN status")
    for n in names:
        st = (index[("root", n, "baseline-noaggr")].get("native_statistics") or {}).get("original_variable_status") or {}
        if set(st) - {"COLUMN"}: print(f"   {n}: {st}")
    print("-- root bound comparisons")
    pairs = [("all-noaggr", "baseline-noaggr"), ("all-diag-noaggr", "baseline-noaggr"), ("all-diag-rowdir-noaggr", "baseline-noaggr"),
             ("baseline-noaggr", "c3:baseline"), ("baseline-extra", "c3:baseline"), ("c3:all", "c3:baseline"), ("c3:all-diag", "c3:baseline"),
             ("c3:auto", "c3:baseline"), ("baseline-extra", "baseline-noaggr")]
    for m, ref in pairs:
        for rt in (1e-4, 1e-6):
            out = defaultdict(list)
            for n in names:
                o = S.compare(index[("root", n, m)], index[("root", n, ref)], S.root_bound, rt); out[o].append(n)
            print(f"   {m} vs {ref} rtol {rt}: " + "; ".join(f"{k} {len(v)}" for k, v in out.items()))
            for k in ("better", "worse", "flagged", "unavailable"):
                if out.get(k):
                    det = []
                    for n in out[k]:
                        a = S.root_bound(index[("root", n, m)]); b = S.root_bound(index[("root", n, ref)])
                        try: tgt = float(cs[n].get("reference_primal"))
                        except (TypeError, ValueError): tgt = None
                        sign = -1 if index[("root", n, m)].get("sense") == "max" else 1
                        gc = (a - b) / (tgt - b) if tgt is not None and sign * (tgt - b) > 0 else None
                        det.append(f"{n} {f(a,7)} vs {f(b,7)} (gc {f(gc,3)}, target {f(tgt,7)})")
                    print(f"      {k}: " + "; ".join(det))
    print("-- solved at root (optimal/gaplimit) per mode")
    for m in ["c3:baseline", "c3:all", "c3:auto", "c3:all-diag", "baseline-noaggr", "baseline-extra", "all-noaggr", "all-diag-noaggr", "all-diag-rowdir-noaggr"]:
        sol = [n for n in names if S.solved(index[("root", n, m)])]
        print(f"   {m}: {len(sol)} {sol}")
    print("-- native separators per model, baseline-extra (interminor calls/found/applied; minor; rlt; quadratic nlhdlr cuts)")
    for n in names:
        st = index[("root", n, "baseline-extra")].get("native_statistics") or {}
        sp = st.get("separators") or {}
        q = (st.get("nlhdlrs") or {}).get("quadratic") or {}
        cell = lambda k: "/".join(str((sp.get(k) or {}).get(c, 0)) for c in ("Calls", "FoundCuts", "Applied"))
        print(f"   {n}: eccuts {cell('eccuts')} interminor {cell('interminor')} minor {cell('minor')} rlt {cell('rlt')} intersection {q.get('Cuts', 0)} (enforce {q.get('#Enforce', 0)})")
    print("-- native separators per model, baseline-noaggr (for contrast)")
    for n in names:
        st = index[("root", n, "baseline-noaggr")].get("native_statistics") or {}
        sp = st.get("separators") or {}
        cell = lambda k: "/".join(str((sp.get(k) or {}).get(c, 0)) for c in ("Calls", "FoundCuts", "Applied"))
        if any((sp.get(k) or {}).get("Calls") for k in ("interminor", "minor", "eccuts")):
            print(f"   {n}: interminor {cell('interminor')} minor {cell('minor')} rlt {cell('rlt')}")
    time_rows(index, names, "root", ["c3:baseline", "c3:all", "c3:auto", "c3:all-diag", "baseline-noaggr", "baseline-extra", "all-noaggr", "all-diag-noaggr", "all-diag-rowdir-noaggr"], "c3:baseline")
    time_rows(index, names, "root", ["baseline-noaggr", "all-noaggr", "all-diag-noaggr", "all-diag-rowdir-noaggr"], "baseline-noaggr")
    extra_checks(recs, "partB2")

if part == "D":
    root = load(RUNS / "partD-root"); full = load(RUNS / "partD-full")
    cs = cases(RUNS / "partD-root")
    index = idx(root); index.update(idx(full))
    names = list(dict.fromkeys(j["name"] for j in json.loads((RUNS / "partD-root" / "jobs.json").read_text())["jobs"]))
    scan = {r["name"]: r for r in (json.loads(l) for l in open(V4 / "scanD" / "records.jsonl"))}
    print("models", len(names))
    def target(n):
        try: return float(cs[n].get("reference_primal"))
        except (TypeError, ValueError): return None
    print("-- model info: sense, nvars, target, scan discovery s, baseline root, root status per mode")
    for n in names:
        b = index[("root", n, "baseline")]
        print(f"  {n}: sense {b.get('sense')} nvars {scan[n]['nvars']} target {f(target(n),8)} scan_disc {f(scan[n]['discovery_seconds'],3)} "
              f"base_root {f(S.root_bound(b),8)} statuses " + ",".join(f"{m}:{index[('root', n, m)]['status']}" for m in ["baseline", "baseline-extra", "all", "all-diag", "all-diag-rowdir"]))
    rmodes = ["all", "all-diag", "all-diag-rowdir", "baseline-extra"]
    print("-- root per mode")
    for m in rmodes:
        rs = {n: index[("root", n, m)] for n in names}
        withcuts = [n for n in names if (S.cuts(rs[n]) or [])]
        print(f"  {m}: models with cuts {len(withcuts)}: " + ", ".join(f"{n}({len(S.cuts(rs[n]))})" for n in withcuts))
        for rt in (1e-4, 1e-6):
            out = defaultdict(list)
            for n in names:
                out[S.compare(rs[n], index[("root", n, "baseline")], S.root_bound, rt)].append(n)
            print(f"     rtol {rt}: " + "; ".join(f"{k} {len(v)}" for k, v in out.items()))
            for k in ("better", "worse", "flagged", "unavailable"):
                if out.get(k):
                    det = []
                    for n in out[k]:
                        a = S.root_bound(rs[n]); b = S.root_bound(index[("root", n, "baseline")]); t = target(n)
                        sign = -1 if rs[n].get("sense") == "max" else 1
                        gc = (a - b) / (t - b) if t is not None and a is not None and b is not None and sign * (t - b) > 0 else None
                        det.append(f"{n} {f(a,8)} vs {f(b,8)} (gc {f(gc,3)}; cuts {len(S.cuts(rs[n]) or [])})")
                    print(f"        {k}: " + "; ".join(det))
        gcs = []
        for n in names:
            a = S.root_bound(rs[n]); b = S.root_bound(index[("root", n, "baseline")]); t = target(n)
            sign = -1 if rs[n].get("sense") == "max" else 1
            if t is not None and a is not None and b is not None and sign * (t - b) > 0:
                gcs.append((a - b) / (t - b))
        print(f"     root gap closed over {len(gcs)} models with target: median {f(med(gcs),3)} min {f(min(gcs),3)} max {f(max(gcs),3)}; >1e-4: {sum(g > 1e-4 for g in gcs)}; < -1e-4: {sum(g < -1e-4 for g in gcs)}")
    print("-- flagged details")
    for r in root + full:
        if S.flags(r): print("  ", r["run_id"], S.flags(r), r.get("reference_check"), "root_dual", r.get("root_dual"), "dual", r.get("dual"), "primal", r.get("primal"))
    print("-- root timelimit runs")
    for r in root:
        if r["status"] == "timelimit":
            print(f"   {r['run_id']}: root_dual {f(r.get('root_dual'),8)} dual {f(r.get('dual'),8)} nodes {r.get('nodes')} t {f(S.seconds(r),4)} cb {f(S.callback(r),3)}")
    print("-- funnel root and full")
    for m in ["all", "all-diag", "all-diag-rowdir"]:
        funnel_print([index[("root", n, m)] for n in names], f"root {m}")
    for m in ["all", "auto"]:
        funnel_print([index[("full", n, m)] for n in names], f"full {m}")
    print("-- discovery-incomplete / per-model separation (root all): disc_incomplete, discovery_seconds, callback, support calls, cuts, scan discovery")
    for ph, m in (("root", "all"), ("full", "all"), ("full", "auto"), ("root", "all-diag")):
        inc = [n for n in names if (index[(ph, n, m)].get("separation") or {}).get("discovery_incomplete")]
        print(f"  {ph} {m}: discovery incomplete {len(inc)}: {inc}")
        print(f"     scan discovery s of those: {[round(scan[n]['discovery_seconds'],2) for n in inc]}")
        print(f"     scan discovery > 1 s: {[n for n in names if scan[n]['discovery_seconds'] > 1]}")
    for n in names:
        s = index[("root", n, "all")].get("separation") or {}
        s2 = index[("root", n, "all-diag")].get("separation") or {}
        print(f"   {n}: all: inc {s.get('discovery_incomplete')} disc {f(s.get('discovery_seconds'),3)} cb {f(s.get('callback_seconds'),3)} calls {s.get('certification_calls')} cuts {s.get('cuts')} | "
              f"all-diag: disc {f(s2.get('discovery_seconds'),3)} cb {f(s2.get('callback_seconds'),3)} calls {s2.get('certification_calls')} fail {s2.get('certification_failures')} bind {s2.get('row_binding_rejections')} cuts {s2.get('cuts')} budget {s2.get('budget_exhausted')}")
    print("-- full")
    fm = ["baseline", "all", "auto", "baseline-extra"]
    for m in fm:
        sol = [n for n in names if S.solved(index[("full", n, m)])]
        print(f"  {m}: solved {len(sol)}: {sol}; statuses {dict(Counter(index[('full', n, m)]['status'] for n in names))}")
    for m in fm[1:]:
        for rt in (1e-4, 1e-6):
            out = defaultdict(list)
            for n in names:
                out[S.compare(index[("full", n, m)], index[("full", n, "baseline")], "dual", rt)].append(n)
            print(f"   {m} rtol {rt}: " + "; ".join(f"{k} {len(v)}" for k, v in out.items()))
            for k in ("better", "worse", "flagged"):
                if out.get(k):
                    print(f"      {k}: " + "; ".join(f"{n} {f(index[('full', n, m)]['dual'],8)} vs {f(index[('full', n, 'baseline')]['dual'],8)}" for n in out[k]))
    print("-- full: cuts per model in all/auto")
    for m in ("all", "auto"):
        print(f"   {m}: " + ", ".join(f"{n}({len(S.cuts(index[('full', n, m)]))})" for n in names if S.cuts(index[("full", n, m)])))
    time_rows(index, names, "root", ["baseline", "baseline-extra", "all", "all-diag", "all-diag-rowdir"], "baseline")
    time_rows(index, names, "full", fm, "baseline")
    print("-- full: all runs (not only solved) SGM total / SCIP / SCIP excl cb per mode")
    for m in fm:
        rs = [index[("full", n, m)] for n in names]
        print(f"   {m}: SGM total {f(S.sgm([S.seconds(r) for r in rs]))} SCIP {f(S.sgm([S.solver_seconds(r) for r in rs]))} excl {f(S.sgm([S.scip_excluding_callback(r) for r in rs]))} sum cb {sum(S.callback(r) for r in rs):.1f} median nodes {f(med([r['nodes'] for r in rs]))}")
    extra_checks(root, "partD-root"); extra_checks(full, "partD-full")

if part == "caps":
    dirs = {"C2": V4/"runs/partC2", "C3": V4/"runs/partC3", "B2": V4/"runs/partB2", "D-root": V4/"runs/partD-root", "D-full": V4/"runs/partD-full",
            "v3 C": V4.parent/"v3/runs/partC", "v3 B": V4.parent/"v3/runs/partB", "v3d C": V4.parent/"v3d/runs/partC-rowdir"}
    for label, d in dirs.items():
        recs = [json.loads(l) for l in (d/"records.jsonl").read_text().splitlines() if l]
        groups = {}
        for r in recs:
            s = r.get("separation")
            if not s: continue
            if label == "v3 B" and r["phase"] != "root": continue
            groups.setdefault((r["phase"], r["mode"]), []).append(r)
        for (ph, m), rs in sorted(groups.items()):
            c = Counter()
            for r in rs:
                s, cfg = r["separation"], r["config"]
                cut = s["cuts"] >= cfg["max_cuts"]; sup = s["certification_calls"] >= cfg["max_support_calls"]
                rnd = s["calls"] >= cfg["max_rounds"]; be = bool(s.get("budget_exhausted")); di = bool(s.get("discovery_incomplete"))
                c["runs"] += 1; c["cut_cap"] += cut; c["support_cap"] += sup; c["round_cap(10 callbacks)"] += rnd
                c["time_budget(inferred: flag, no cut/support cap)"] += be and not cut and not sup
                c["of which discovery stopped"] += di
                c["no cap/budget"] += not (be or rnd)
            print(f"{label} {ph} {m}: {dict(c)}  limits max_cuts={rs[0]['config']['max_cuts']} max_support={rs[0]['config']['max_support_calls']} sep_s={rs[0]['config']['max_separation_seconds']} frac={rs[0]['config']['separation_budget_fraction']}")
