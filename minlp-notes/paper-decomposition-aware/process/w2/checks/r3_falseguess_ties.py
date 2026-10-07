"""List tied minimizers of the proximal stage for K=4 in rem:falseguess."""
from fractions import Fraction as Fr
import r3_falseguess as m

K = 4
mu, th = 3, Fr(1, 8)
eta = m.L * th * th / 4
rho = 2 * m.ceil_sqrt(2 * K)
c = (Fr(0), Fr(0))
for j in range(0, 34):
    h = Fr(1, 2 ** j)
    grids = []
    for ci in c:
        lo, hi = max(Fr(0), ci - rho * h), min(Fr(1), ci + rho * h)
        grids.append(m.graded(ci, lo, hi, h, th))
    d0, d1 = m.corr(grids[0]), m.corr(grids[1])
    vals = {}
    for a in grids[0]:
        for b in grids[1]:
            vals[(a, b)] = m.F(a, b) - d0[a] - d1[b] + eta * ((a - c[0]) ** 2 + (b - c[1]) ** 2)
    best = min(vals.values())
    arg = [k for k, v in vals.items() if v == best]
    if len(arg) > 1:
        print(j, "tied:", arg, "value", best, "grids", grids)
    c = (Fr(0), Fr(0)) if (Fr(0), Fr(0)) in arg else arg[0]
