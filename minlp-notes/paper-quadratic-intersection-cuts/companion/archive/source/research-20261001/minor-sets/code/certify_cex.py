"""Exact certificate: the orbit family of SCIP's minor sets misses the corner bound on a rational
full-dimensional simplicial corner with a tangent-edge minimizer (note, Theorem 8).

S = {det = 0} in R^4 (coordinates (a, b, c, d) of M = [[a, b], [c, d]]), w = (1, 1, 1, 1), rays
p_j = v_j - sbar, T* = conv{sbar, v1, ..., v4}.  Checks (exact rational arithmetic unless marked):
 (1)-(2) full-dimensional corner, det(sbar) > 0, min over T* of det = 0 only at t0 (so z_K = 1).
 (3) t0 in the relative interior of [v1, v2], tangent edge (grad det(t0).(v1 - v2) = 0),
     det(v1 - v2) > 0, KKT multipliers zero on rays 1, 2 and positive on rays 3, 4.
 (4) Lemma 6 pencil F_kappa^T = G0 + kappa G1; exact kappa-sets of all vertices; empty intersection.
 (5) rational positive definite dual certificates at z = 1 and at z = z_up < 1 (z_orbit <= z_up).
 (6) exact brackets for orbit, pr, bcm; SCIP's set in 50-digit arithmetic (numerical).
Usage: python3 certify_cex.py [JSON]   (default: instance A of the note)
"""
import json
import sys
from fractions import Fraction as Fr

import numpy as np
import sympy as sp

import exact_tools as ex
from cert_lib import Checker, load, corner_checks, orbit_upper, brackets, scip_value
from minor_core import FamilySolver, precondition

INSTANCE = {"sbar": [0, "5/2", "-1/2", "-1/2"], "v1": [-5, 3, 4, -4], "v2": [-8, 12, -8, 8],
            "v3": ["-3/2", -4, 2, "-7/2"], "v4": ["-7/2", "-1/2", "3/2", -4], "t0": [-6, 6, 0, 0]}
if len(sys.argv) > 1:
    INSTANCE = json.loads(sys.argv[1])
chk = Checker()
V = load(INSTANCE)
sb, v1, v2, t0 = V['sbar'], V['v1'], V['v2'], V['t0']
P, g, sigma, nu = corner_checks(chk, V)

# (3) tangent edge
d = ex.add(v1, v2, 1, -1)
c = next(c for c in range(4) if d[c] != 0)
mu = (t0[c] - v2[c]) / d[c]
chk('(3) t0 = mu v1 + (1 - mu) v2 with mu = %s in (0, 1)' % mu, 0 < mu < 1 and ex.add(v2, d, 1, mu) == t0)
chk('(3) tangent edge: grad det(t0) . (v1 - v2) = %s' % ex.dot(g, d), ex.dot(g, d) == 0)
chk('(3) second order: det(v1 - v2) = %s > 0' % ex.det4(d), ex.det4(d) > 0)
chk('(3) KKT multipliers nu = %s: zero on rays 1, 2, positive on rays 3, 4' % [str(x) for x in nu],
    nu[0] == 0 and nu[1] == 0 and nu[2] > 0 and nu[3] > 0)

# (4) pencil of Lemma 6
J = [[Fr(0), Fr(1)], [Fr(-1), Fr(0)]]
M0 = ex.m2(t0)
G0 = ex.mmul(J, ex.madj(ex.m2(d)))
G1 = ex.mmul(J, ex.madj(M0))
b0 = next(r for r in M0 if any(r))
k0 = 0 if b0[0] != 0 else 1
a0 = [M0[0][k0] / b0[k0], M0[1][k0] / b0[k0]]
chk('(4) M0 = a0 b0^T', [[a0[i] * b0[j] for j in range(2)] for i in range(2)] == M0)
Ga0 = [sum(G0[i][k] * a0[k] for k in range(2)) for i in range(2)]
chk('(4) G1 a0 = 0 and G0 a0 = c0 b0', [sum(G1[i][k] * a0[k] for k in range(2)) for i in range(2)] == [0, 0]
    and Ga0[0] * b0[1] - Ga0[1] * b0[0] == 0)
c0 = (Ga0[0] * b0[0] + Ga0[1] * b0[1]) / (b0[0] ** 2 + b0[1] ** 2)
sgn = 1 if c0 > 0 else -1
G0 = [[sgn * x for x in r] for r in G0]
G1 = [[sgn * x for x in r] for r in G1]
print('   c0 = %s; F_kappa^T = G0 + kappa G1, G0 = %s, G1 = %s' % (c0, [[str(x) for x in r] for r in G0],
                                                             [[str(x) for x in r] for r in G1]))
kap = sp.symbols('kappa', real=True)
FT = sp.Matrix(G0) + kap * sp.Matrix(G1)
chk('(4) det F_kappa^T = det(v1 - v2) for every kappa', sp.expand(FT.det() - ex.det4(d)) == 0)
inter = sp.S.Reals
sets = {}
for name in ('sbar', 'v1', 'v2', 'v3', 'v4'):
    A = FT * sp.Matrix(ex.m2(V[name]))
    A = (A + A.T) / 2
    s = (sp.solveset(A[0, 0] >= 0, kap, sp.S.Reals).intersect(sp.solveset(A[1, 1] >= 0, kap, sp.S.Reals))
         .intersect(sp.solveset(sp.expand(A.det()) >= 0, kap, sp.S.Reals)))
    sets[name] = s
    print('   kappa-set of %-4s: %s  ~ %s' % (name, s, s.evalf(8) if s != sp.S.EmptySet else ''))
    inter = inter.intersect(s)
chk('(4) the kappa-sets have empty intersection: no orbit set contains T*', inter == sp.S.EmptySet)
for n1 in sets:
    for n2 in sets:
        I1, I2 = sets[n1], sets[n2]
        if n1 != n2 and I1 != sp.S.EmptySet and I2 != sp.S.EmptySet and I1.intersect(I2) == sp.S.EmptySet \
                and I1.sup < I2.inf:
            print('   already disjoint: the sets of %s (sup %s) and %s (inf %s)' % (n1, sp.N(I1.sup, 10), n2, sp.N(I2.inf, 10)))

# (5) dual certificates
sbn = np.array([float(x) for x in sb])
Pn = np.array([[float(P[j][i]) for j in range(4)] for i in range(4)])
sI, PI = precondition(sbn, Pn)
c_, h_, _ = FamilySolver('orbit', sI, PI, np.ones(4)).best(1.0, iters=40)
print('   numerical orbit bound %.10f (bisection upper %.10f)' % (c_, h_))
orbit_upper(chk, V, P, Fr(1))
orbit_upper(chk, V, P, Fr(int(np.ceil(h_ * 1000)), 1000))

# (6) brackets
br = brackets(chk, V, P)
zs = scip_value(V, P)
print('SUMMARY z_K = 1 (tangent edge); orbit in [%.7f, %.7f]; pr in [%.7f, %.7f]; bcm in [%.7f, %.7f]; scip = %.10f'
      % (float(br['orbit'][0]), float(br['orbit'][1]), float(br['pr'][0]), float(br['pr'][1]),
         float(br['bcm'][0]), float(br['bcm'][1]), float(zs)))
print('ALL PASS' if chk.ok else 'SOME CHECK FAILED')
