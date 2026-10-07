"""Recheck of the sfree note's near-boundary adversarial instance (adversarial_ratio_8_margin.log,
restart 3; the note quotes z_A = 0.0280 and 'Clarabel infeasible from 0.029 on').  The family-(A)
bisection is redone in the normalized frame (sbar -> (0,0,1)), where the SDP is well scaled, with
Clarabel and SCS; the returned X is mapped back to F in the original coordinates, rounded to
rationals, and the containment of the shrunken simplex T_r (r = certified value) is checked in exact
rational arithmetic (the instance data are taken as the exact binary floats)."""
import json
import os
import numpy as np
import sympy as sp
import warnings
import rb
from adversarial_ratio import build

warnings.filterwarnings('ignore')
LOG = os.path.join(rb.SFREE, '..', 'logs', 'adversarial_ratio_8_margin.log')
r = [json.loads(l) for l in open(LOG) if l.startswith('{')][3]
sbar, P = build(np.array(r['theta']))
c = np.ones(3)
z, lam = rb.zK(sbar, P, c)
Pt = rb.scaled_rays(P, c, z)
print('zK = %.12f, support %s, q(sbar) = %.3e, D = %.1f' % (z, np.flatnonzero(lam > 1e-12).tolist(), rb.q(sbar), rb.D_inv(sbar, Pt)))
for solver in ('CLARABEL', 'SCS'):
    cert, hi, X = rb.zA_ratio(sbar, Pt, iters=40, solver=solver)
    print('%s: certified lower bound %.6f, bisection upper value %.6f' % (solver, cert, hi))
cert, hi, X = rb.zA_ratio(sbar, Pt, iters=40)
# map X (normalized frame, t = 1) back: X = K^{-T} F^T U D1  =>  F^T = K^T X (U D1)^{-1}
rq = np.sqrt(rb.q(sbar))
U = np.array([[1.0, sbar[0]], [0.0, 1.0]])
Lm = np.array([[1.0, 0.0], [sbar[1], 1.0]])
D1 = np.diag([rq, 1.0])
K = np.diag([rq, 1.0]) @ Lm
FT = K.T @ X @ np.linalg.inv(U @ D1)
assert np.allclose(rb.to_normalized_X(FT.T, sbar), X)
rr = sp.Rational(int(cert * 0.999 * 10 ** 6), 10 ** 6)
FTq = sp.Matrix(2, 2, [sp.Rational(v).limit_denominator(10 ** 15) for v in FT.ravel()])
sq = [sp.Rational(v) for v in sbar]
Pq = [[sp.Rational(v) for v in Pt[:, j]] for j in range(3)]
Mq = lambda s: sp.Matrix([[s[2], s[0]], [s[1], 1]])
def psd(A, strict=False):
    S = (A + A.T) / 2
    return (S[0, 0] > 0 and S.det() > 0) if strict else (S[0, 0] >= 0 and S[1, 1] >= 0 and S.det() >= 0)
ok = psd(FTq * Mq(sq), strict=True)
for j in range(3):
    v = [sq[i] + rr * Pq[j][i] for i in range(3)]
    ok = ok and psd(FTq * Mq(v))
print('exact check: rational F contains sbar in its interior and the vertices of T_r, r = %s (= %.6f): %s'
      % (rr, float(rr), 'PASS' if ok else 'FAIL'))
