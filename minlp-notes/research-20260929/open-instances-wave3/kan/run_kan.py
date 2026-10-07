"""Driver: certified bound + primal point for one KAN instance.

    python3 run_kan.py <name> <tol_rel> <time_limit_s>

Writes ../logs/<name>.bb.log (via stdout redirection by the caller),
../sol/<name>.wave3.sol (primal point, 30 digits) and ../logs/<name>.result.json.
"""
import json
import os
import sys

import mpmath as mp
import numpy as np

import kan_bb as kb
import kan_check as kc

HERE = os.path.dirname(os.path.abspath(__file__))


def main(name, tol, tl):
    net, res, lb_cert = kb.main2(name, tol, tl)
    M = net.M
    u = res["u"]
    # primal point: the incumbent must satisfy the true h-constraints, not only the relaxed ones
    x, r = kc.point_report(M, [mp.mpf(float(v)) for v in u], "primal (60-digit propagation)")
    hmod = [x[Hd["h"]] for Hd in M["hidden"]]
    q2mp = lambda q: mp.mpf(q.numerator) / q.denominator
    with mp.workdps(60):
        inside = all(q2mp(Hd["box"][0]) <= h <= q2mp(Hd["box"][1]) for Hd, h in zip(M["hidden"], hmod))
    kc.write_sol(M, x, os.path.join(HERE, "..", "sol", f"{name}.wave3.sol"))
    # re-evaluate the rounded (30-digit) point from the file
    import ev
    vals = ev.read_sol(os.path.join(HERE, "..", "sol", f"{name}.wave3.sol"))
    xr = [vals[v] for v in M["I"]["names"]]
    rr = ev.evaluate(M["I"], xr, 60)
    print(f"rounded 30-digit point: obj {mp.nstr(rr['obj'], 20)} max row viol {mp.nstr(rr['row_viol'], 3)} ({rr['worst_row']})"
          f" bound viol {mp.nstr(rr['bound_viol'], 3)}")
    out = dict(name=name, LB_ideal=res["LB"], UB_ideal=res["UB"], Delta=float(net.Delta), dual_bound=lb_cert,
               done=res["done"], processed=res["processed"], open=res["open"], time=res["time"],
               u=[float(v) for v in u], primal_obj=str(mp.nstr(rr["obj"], 20)),
               primal_row_viol=str(mp.nstr(rr["row_viol"], 3)), primal_bound_viol=str(mp.nstr(rr["bound_viol"], 3)),
               h_inside_true_box=bool(inside))
    with open(os.path.join(HERE, "..", "logs", f"{name}.result.json"), "w") as f:
        json.dump(out, f, indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main(sys.argv[1], float(sys.argv[2]), float(sys.argv[3]))
