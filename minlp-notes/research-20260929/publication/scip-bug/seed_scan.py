"""Run a model under default settings (plus optional extra parameters) for
random seed shifts 0..N-1 and classify each 'optimal' claim against the
exact witness value: WRONG if claim > witness value + 1e-4 (the witness is
exactly feasible, so any valid claim is <= its value up to tolerances).

usage: python3 seed_scan.py MODEL.cip WITNESS_VALUE N [extra-settings]
"""
import sys

import run_scip

path, wval, n = sys.argv[1], float(sys.argv[2]), int(sys.argv[3])
extra = run_scip.parse(sys.argv[4]) if len(sys.argv) > 4 else {}
nwrong = 0
for s in range(n):
    prm = dict(extra)
    prm["randomization/randomseedshift"] = s
    r = run_scip.solve(path, prm)
    wrong = r["status"] == "optimal" and r["dual"] > wval + 1e-4
    nwrong += wrong
    print(f"seed {s:3d} status {r['status']:9s} claimed {r['dual']:.6f} primal {r['primal']:.6f} nodes {r['nodes']:6d} "
          f"time {r['time']:.1f}s {'WRONG' if wrong else 'ok'}", flush=True)
print(f"# {path} extra={extra}: wrong in {nwrong} of {n} seeds")
