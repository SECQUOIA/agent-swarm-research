"""Aux-variable bounds in the author's sub model contain g([l, u]) exactly (g = k x^p, x in [l, u]).
python auxbounds.py <instance>"""
import sys, os
from fractions import Fraction as F
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import model
name = sys.argv[1]
B = model.build(name, "sub")
bad = n = 0
for v, keep in B.det.sel.items():
    l, u = F(B.inst.var_lb[v]), F(B.inst.var_ub[v])
    for j, (_, key, sc) in enumerate(keep):
        t = B.m.getVarByName(f"t{v}_{j}")
        g = str(sc.g)
        k, p = (int(g.split("*")[0]), int(g[-1])) if g[0].isdigit() else (1, int(g[-1]))
        vals = [k * l ** p, k * u ** p] + ([F(0)] if l <= 0 <= u else [])
        n += 1
        if not (F(t.LB) <= min(vals) and F(t.UB) >= max(vals)):
            bad += 1
print(name, "aux vars", n, "bounds not containing g([l,u]):", bad,
      "l>=0 for all selected:", all(B.inst.var_lb[v] >= 0 for v in B.det.sel))
