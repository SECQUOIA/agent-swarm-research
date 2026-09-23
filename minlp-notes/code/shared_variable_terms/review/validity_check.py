"""Validity of the links at a good feasible point of the NATIVE model.
For each instance: solve native with Gurobi (reviewer's builder), take the incumbent x, check it with the plain-float evaluator,
compute the implied t_k = x^p_k (and s, c), and test every added link constraint and the t bounds to 1e-7."""
import json, math, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from gmodel import build
tl, threads = float(sys.argv[1]), int(sys.argv[2])
for name in sys.argv[3:]:
    M, m, x, trig, pw = build(name, linked=False)
    m.Params.TimeLimit = tl; m.Params.Threads = threads; m.Params.MIPGap = 1e-4
    t0 = time.time(); m.optimize()
    if not m.SolCount:
        print(json.dumps({"name": name, "status": m.Status, "note": "no point"})); continue
    pt = [v.X for v in x]
    chk = M.check(pt)
    worst = 0.0; worst_what = None; nchecked = 0
    for v in trig:
        s, c = math.sin(pt[v]), math.cos(pt[v]); r = abs(s * s + c * c - 1); nchecked += 1
        if r > worst: worst, worst_what = r, ("trig", v, pt[v])
    for v, ps_ in pw.items():
        lo, hi, xv = M.lb[v], M.ub[v], pt[v]
        xv_c = min(max(xv, lo), hi)  # the point may violate its own bounds by Gurobi's tolerance; clamp for the power
        if xv_c <= 0 and min(ps_) < 0:
            worst_what = ("negative exponent at x=0", v, xv); worst = math.inf; continue
        t = {p: xv_c ** p for p in ps_}
        ref = min(ps_, key=abs)
        for p in ps_:
            a, b = sorted((lo ** p, hi ** p))
            bv = max(a - t[p], t[p] - b, 0.0) / max(1.0, abs(a), abs(b)); nchecked += 1
            if bv > worst: worst, worst_what = bv, ("t-bound", v, p, xv, t[p], (a, b))
            if p != ref:
                r = abs(t[p] - t[ref] ** (p / ref)) / max(1.0, abs(t[p])); nchecked += 1
                if r > worst: worst, worst_what = r, ("link", v, p, ref, xv, t[p], t[ref] ** (p / ref))
    print(json.dumps({"name": name, "status": m.Status, "obj": m.ObjVal, "dual": m.ObjBound, "time": round(time.time() - t0, 1),
                      "native_check": chk, "trig_vars": len(trig), "power_vars": len(pw), "link_checks": nchecked,
                      "max_link_or_tbound_violation": worst, "worst": worst_what}))
