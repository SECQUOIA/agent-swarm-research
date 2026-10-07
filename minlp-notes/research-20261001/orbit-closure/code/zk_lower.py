"""Exact lower bound z_K(w) >= z0 at a rational corner: q(sbar + P lam) > 0 on the simplex
T = {lam >= 0, w^T lam <= z0}.  q is a quadratic in the barycentric coordinates of T; its minimum
over T is attained at a stationary point of q restricted to (the relative interior of) some face,
so enumerating all faces and solving the linear stationarity systems exactly gives the exact minimum.
Usage: python3 zk_lower.py   (instance: Theorem 14 corner, w = (11/20, 1/10^6, 9/20), z0 = 2596/10000)
"""
import itertools, sys
from fractions import Fraction as Fr
import sympy as sp

sb = [Fr(-9, 2), Fr(0), Fr(3, 2)]
V = [[Fr(-1), Fr(-6), Fr(18)], [Fr(-5), Fr(6), Fr(-18)], [Fr(0), Fr(5, 2), Fr(5, 2)]]
P = [[V[j][i] - sb[i] for i in range(3)] for j in range(3)]
w = [Fr(11, 20), Fr(1, 10 ** 6), Fr(9, 20)]
z0 = Fr(2596, 10000)
verts = [list(sb)] + [[sb[i] + z0 / w[j] * P[j][i] for i in range(3)] for j in range(3)]


def q(s):
    return s[2] - s[0] * s[1]


best = None
for k in range(1, 5):
    for face in itertools.combinations(range(4), k):
        ts = sp.symbols('t0:%d' % k)
        # point = sum t_i v_face[i], sum t_i = 1
        lag = sp.symbols('mu')
        pt = [sum(ts[i] * sp.Rational(str(verts[face[i]][c])) for i in range(k)) for c in range(3)]
        Q = pt[2] - pt[0] * pt[1]
        eqs = [sp.diff(Q, ts[i]) - lag for i in range(k)] + [sum(ts) - 1]
        sol = sp.solve(eqs, list(ts) + [lag], dict=True)
        for so in sol:
            vals = [so.get(t, None) for t in ts]
            if any(v is None for v in vals):
                continue                      # degenerate face (a line of stationary points): skip, covered by subfaces
            if all(v >= 0 for v in vals):
                val = Q.subs(so)
                best = val if best is None or val < best else best
print('exact minimum of q over T_{z0} (z0 = %s): %s = %.6g' % (z0, best, float(best)))
ok = best > 0
print('=> z_K(w) >= z0 = %s: %s' % (z0, 'PASS' if ok else 'FAIL'))
sys.exit(0 if ok else 1)
