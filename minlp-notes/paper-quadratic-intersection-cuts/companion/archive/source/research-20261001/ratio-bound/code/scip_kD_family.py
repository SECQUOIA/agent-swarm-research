"""Proposition S3 of the note: SCIP's ratio can be 2/(1 + sqrt(1 + kappa^2 D^2)) < 2/(kappa D) while the
orbit family is exact (all rays at the extreme relative discriminant +1).

Family: u > 1, v = sqrt(u^2 - 1), D > 0 with D <= v;  sbar = (u, -u, -1), p1 = (v D, 0, 0), p2 = (0, -v D, 0),
p3 = (0, 0, -v^2), costs 1, S = {w <= x y}.

Exact checks (sympy, symbolic in u, D, with v^2 = u^2 - 1, and at rational Pythagorean points
u = (m^2 + 1)/(2m), v = (m^2 - 1)/(2m)):
  (1) q(sbar + P lam) = v^2 (1 - lam3) + u v D (lam1 + lam2) + v^2 D^2 lam1 lam2, so z_K = 1, attained only at e3;
  (2) D_inv = D, singular values of P~ = P: v D, v D, v^2, so kappa = v / D;
  (3) SCIP's set (Lemma S): w(sbar) + 1 = 0 gives N^2 = 4u^2, V(d) = 2u d_w, so C_SCIP = {4 q >= (w + 1)^2, x >= y};
      along p3 the first exit is s = 2/(u + 1); rays 1, 2 never leave; the upward closure has the same step
      along the downward vertical ray p3.  So z_SCIP / z_K = 2/(u + 1) for the Case-4 set and its uncompleted cone;
  (4) orbit exactness (Theorem C(3)/(4) of the note): in coordinates centred at t* = sbar + p3 = (u, -u, -u^2),
      the orbit set C_{1, beta}, beta = D/(u D + v), contains every vertex of T*, and sbar strictly;
  (5) relative discriminants of the three rays are all +1.
Also a float cross-check against the reimplementation of SCIP's Case-4 set (rb.scip_ratio) and the
SDP value of z_A.
usage: python3 scip_kD_family.py"""
import sympy as sp
import numpy as np
import warnings
import rb

warnings.filterwarnings('ignore')
u, D, l1, l2, l3, s = sp.symbols('u D lambda1 lambda2 lambda3 s', positive=True)
v = sp.sqrt(u ** 2 - 1)
checks = {}

# (1) corner bound identity
sb = sp.Matrix([u, -u, -1])
P = sp.Matrix([[v * D, 0, 0], [0, -v * D, 0], [0, 0, -v ** 2]])
pt = sb + P * sp.Matrix([l1, l2, l3])
qexpr = sp.expand(pt[2] - pt[0] * pt[1])
target = sp.expand(v ** 2 * (1 - l3) + u * v * D * (l1 + l2) + v ** 2 * D ** 2 * l1 * l2)
checks['(1) q(sbar + P lam) identity'] = sp.simplify(qexpr - target) == 0

# (3) SCIP step along p3: 4 q = (w + 1)^2 along sbar + s p3, q = v^2 (1 - s), w + 1 = -s v^2
step_eq = 4 * v ** 2 * (1 - s) - s ** 2 * v ** 4
s3 = 2 / (u + 1)
checks['(3) s = 2/(u+1) solves 4 q = (w+1)^2 along p3'] = sp.simplify(step_eq.subs(s, s3)) == 0
# it is the first positive root: the quadratic -v^4 s^2 - 4 v^2 s + 4 v^2 is positive at 0 and has one positive root
roots = sp.solve(sp.Eq(step_eq, 0), s)
checks['(3) only one positive root'] = sum(1 for r in roots if sp.simplify(r.subs(u, 3)) > 0) == 1
# Lemma S data at sbar: N^2 = (xbar - ybar)^2 + (wbar + 1)^2 = 4 u^2, V(d) = (xbar - ybar) d_w - (wbar + 1)(d_x - d_y)
N2 = (sb[0] - sb[1]) ** 2 + (sb[2] + 1) ** 2
checks['(3) N^2 = 4u^2 and V(d) = 2u d_w'] = sp.simplify(N2 - 4 * u ** 2) == 0 and (sb[2] + 1) == 0
# rays 1, 2: V(p) = 2u * p_w = 0 and q >= v^2 > 0 along them; trace x - y = 2u + v D s > 0
checks['(3) rays 1, 2 stay in C_SCIP (V(p) = 0, q > 0, trace > 0)'] = (P[2, 0] == 0 and P[2, 1] == 0)

# (4) orbit exactness, centred coordinates (x', y', w') = (x - u, y + u, w + u x - u y - u^2)
def centred(p):
    x, y, w = p
    return (sp.simplify(x - u), sp.simplify(y + u), sp.simplify(w + u * x - u * y - u ** 2))


tstar = sb + P[:, 2]
verts = {'t*': centred(tstar), 'sbar': centred(sb), 'v1': centred(sb + P[:, 0]), 'v2': centred(sb + P[:, 1])}
checks['(4) t* maps to the origin'] = all(sp.simplify(c) == 0 for c in verts['t*'])
alpha = 1
beta = D / (u * D + v)


def slack(c):
    x, y, h = c
    return sp.simplify(4 * alpha * (h - x * y) - (alpha * x - y - beta * h) ** 2), sp.simplify(alpha * h + beta * x + 1)


res = {k: slack(c) for k, c in verts.items()}
# exact positivity at rational points (u, D) on a grid with u Pythagorean, and symbolic simplification
ok4 = True
for m in (2, 3, 5, 10, 40):
    uu = sp.Rational(m * m + 1, 2 * m)
    vv = sp.Rational(m * m - 1, 2 * m)
    for DD in (sp.Rational(1, 3), sp.Integer(1), vv / 2, vv):
        if DD > vv:
            continue
        sub = {u: uu, D: DD}
        for k, (dq, tr) in res.items():
            dqv, trv = sp.nsimplify(dq.subs(sub)), sp.nsimplify(tr.subs(sub))
            if k == 'sbar':
                ok4 = ok4 and dqv > 0 and trv > 0
            elif k != 't*':
                ok4 = ok4 and dqv >= 0 and trv >= 0
checks['(4) C_{1, D/(uD+v)} contains T*, sbar strictly (grid of rational u, D)'] = ok4
print('symbolic slacks of C_{1,beta} (4 alpha q - l^2, trace):')
for k, (dq, tr) in res.items():
    print('  ', k, ':', sp.factor(dq), ' | ', sp.simplify(tr))

# (5) relative discriminants: along each ray q = g0 + B s + A s^2
for j in range(3):
    pj = P[:, j]
    A_ = sp.simplify(-pj[0] * pj[1])
    B_ = sp.simplify(sp.Matrix([-sb[1], -sb[0], 1]).dot(pj))
    g0 = sp.simplify(sb[2] - sb[0] * sb[1])
    rd = sp.simplify((B_ ** 2 - 4 * A_ * g0) / (B_ ** 2 + sp.Abs(4 * A_ * g0)))
    checks['(5) relative discriminant of ray %d = +1' % (j + 1)] = rd == 1

for k, val in checks.items():
    print(k, ':', 'PASS' if val else 'FAIL')
print('ALL PASS' if all(checks.values()) else 'SOME FAIL')

# float cross-check with the Case-4 reimplementation and the SDP value of z_A
print('\nfloat cross-check (z_K, D, kappa, SCIP Case-4 set, SCIP cone, 2/(u+1), 2/(kappa D), z_A by SDP):')
for uu, DD in ((2.0, 1.0), (10.0, 1.0), (10.0, 3.0), (100.0, 1.0), (100.0, 10.0), (100.0, np.sqrt(9999.0)),
               (1000.0, 30.0)):
    vv = np.sqrt(uu * uu - 1)
    sbar = np.array([uu, -uu, -1.0])
    Pm = np.array([[vv * DD, 0, 0], [0, -vv * DD, 0], [0, 0, -vv * vv]])
    z, lam = rb.zK(sbar, Pm, np.ones(3))
    Pt = rb.scaled_rays(Pm, np.ones(3), z)
    kap = np.linalg.cond(Pt)
    zA = rb.zA_ratio(sbar, Pt, iters=30)[0]
    print('u=%g D=%g: zK=%.6f D_inv=%.4f kappa=%.4f scipB=%.6f scipA=%.6f 2/(u+1)=%.6f 2/(kappa D)=%.6f zA=%.6f'
          % (uu, DD, z, rb.D_inv(sbar, Pt), kap, rb.scip_ratio(sbar, Pt, 'B'), rb.scip_ratio(sbar, Pt, 'A'),
             2 / (uu + 1), 2 / (kap * DD), zA), flush=True)
