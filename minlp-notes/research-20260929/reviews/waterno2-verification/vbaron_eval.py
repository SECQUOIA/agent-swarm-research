"""Exact evaluation of a BARON point (sol.txt written by vbaron.py) on a period subproblem.
usage: python3 vbaron_eval.py T t multipliers.json gamsdir"""
import sys, json
from fractions import Fraction as F
import vmodel, veval
T, t = int(sys.argv[1]), int(sys.argv[2])
K = json.load(open(sys.argv[3]))
lam = [[float(v) for v in l] for l in K["lam"]]; mu = float(K["mu"])
I = vmodel.instance(T); m = I["m"]
idx = {n: i for i, n in enumerate(m["names"])}
x = [F(0)] * len(m["names"])
for line in open(sys.argv[4] + "/sol.txt"):
    n, v = line.split()
    x[idx[n]] = F(v)
e = veval.evaluate(m, x, rows=I["per_rows"][t], vars_=I["per_vars"][t])
obj = vmodel.period_objective(I, t, lam, mu)
print(f"BARON point T={T} period {t}: Lagrangian value {float(sum(a * x[v] for v, a in obj.items())):.9f}, "
      f"max row violation {float(e['maxrow']):.3e} ({e['row']}), max bound violation {float(e['maxbnd']):.3e} ({e['bvar']}), "
      f"binaries integral {e['int_ok']}")
