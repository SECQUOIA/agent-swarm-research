"""Order-2 sparse moment relaxations of the chiral chain (b, g, ev) = (0.6, 0.3, 0.05), pair cliques, linear box
constraints, in variants that differ in how the box constraints are localized:
  all    : localizing matrices (bivariate, order 1) for 1 +- x and 1 +- y in every clique (the note's Prop. C.5 setting)
  good   : each constraint in one clique: 1 + x_i in clique (i-1, i), 1 - x_i in clique (i, i+1) (ends: their clique)
  bad    : each constraint in one clique: 1 - x_i in clique (i-1, i), 1 + x_i in clique (i, i+1) (ends: their clique)
  univar : Waki et al. (2006) basic form (20): univariate SOS multipliers (localizing matrices in x_i alone)
Floating point (cvxpy + Clarabel)."""
import sys
import cvxpy as cp
b, g, ev = 0.6, 0.3, 0.05; a = b + ev


def solve(n, variant):
    mons = [(i, d - i) for d in range(5) for i in range(d + 1)]
    Y = [dict((m, cp.Variable()) for m in mons if m != (0, 0)) for _ in range(n - 1)]
    y = lambda e, m: 1.0 if m == (0, 0) else Y[e][m]
    cons = []
    b2 = [(0, 0), (1, 0), (0, 1), (2, 0), (1, 1), (0, 2)]; b1 = [(0, 0), (1, 0), (0, 1)]
    def loc(e, lin, basis):
        return cp.bmat([[sum(cf * y(e, (p[0] + q[0] + sh[0], p[1] + q[1] + sh[1])) for cf, sh in lin) for q in basis] for p in basis]) >> 0
    PX, MX, PY, MY = [(1, (0, 0)), (1, (1, 0))], [(1, (0, 0)), (-1, (1, 0))], [(1, (0, 0)), (1, (0, 1))], [(1, (0, 0)), (-1, (0, 1))]
    for e in range(n - 1):
        cons.append(cp.bmat([[y(e, (p[0] + q[0], p[1] + q[1])) for q in b2] for p in b2]) >> 0)
        if e < n - 2:
            for d in range(1, 5):
                cons.append(Y[e][(0, d)] == Y[e + 1][(d, 0)])
        first, last = (e == 0), (e == n - 2)
        if variant == "all":
            for lin in (PX, MX, PY, MY):
                cons.append(loc(e, lin, b1))
        elif variant in ("good", "bad"):
            # clique e = (x_e, x_{e+1}) in 0-based clique index; x is variable e, y is variable e+1
            if variant == "good":
                use = [PY, MX]            # 1 + x_{e+1} and 1 - x_e
            else:
                use = [MY, PX]            # 1 - x_{e+1} and 1 + x_e
            if first:
                use += [PX, MX]
            if last:
                use += [PY, MY]
            for lin in {id(l): l for l in use}.values():
                cons.append(loc(e, lin, b1))
        elif variant == "univar":
            bx = [(0, 0), (1, 0)]; by = [(0, 0), (0, 1)]
            for lin in (PX, MX):
                cons.append(loc(e, lin, bx))
            if last:
                for lin in (PY, MY):
                    cons.append(loc(e, lin, by))
    obj = sum(a / 2 * (y(e, (2, 0)) + y(e, (0, 2))) + b * y(e, (1, 1)) + g / 2 * (y(e, (1, 2)) - y(e, (2, 1))) for e in range(n - 1))
    obj = obj + a / 2 * y(0, (2, 0)) + a / 2 * y(n - 2, (0, 2))
    pr = cp.Problem(cp.Minimize(obj), cons); pr.solve(solver="CLARABEL")
    return pr.value, pr.status


for n in (5, 8):
    for v in ("all", "good", "bad", "univar"):
        val, st = solve(n, v)
        print(f"n={n} variant={v:6s}: value {val:+.4e} ({st})", flush=True)
