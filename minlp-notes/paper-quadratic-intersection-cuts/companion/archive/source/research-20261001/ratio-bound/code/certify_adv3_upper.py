"""Exact upper bound for family (A) on the sfree note's near-boundary adversarial instance
(adversarial_ratio_8_margin.log, restart 3), added in the revision after review round 1.

recheck_adv3.py proves z_A/z_K >= 763/25000 with an explicit orbit set.  This script proves an upper bound
z_A/z_K <= R by a dual (Farkas-type) certificate.  Let v_0 = sbar and v_j = sbar + R p~_j (j = 1, 2, 3) be the
vertices of T_R.  If symmetric PSD matrices Y_0 != 0, Y_1, Y_2, Y_3 satisfy
      sum_{j=0..3} M(v_j) Y_j = 0,
then for every 2x2 X:  0 = tr(X sum_j M(v_j) Y_j) = sum_j <sym(X M(v_j)), Y_j>.  If s-bar lies in the interior of
an orbit set C_X (X = F^T, det F != 0), then sym(X M(sbar)) is positive definite, so the j = 0 term is positive and
some v_j (j >= 1) has <sym(X M(v_j)), Y_j> < 0, i.e. v_j is not in C_X.  So no orbit set with s-bar in its interior
contains T_R, and every such set has some step alpha~_j <= R: z_A/z_K <= R.

The dual is solved in floating point in the normalized frame (well scaled), mapped back to the original
coordinates by the congruence Y_j = B^T Y'_j B of Lemma N (M(phi(s)) = A M(s) B^T), rounded to rationals,
made exactly consistent (Y_1 is rescaled by an exact factor so that Y_0 := -M(sbar)^{-1} sum_{j>=1} M(v_j) Y_j is
symmetric), and checked in exact rational arithmetic.  As in recheck_adv3.py, the instance data and the scaled rays
p~_j = z_K p_j are taken as the exact binary floats used by the code (z_K is the float corner bound, equal to 1 up
to the printed digits).
usage: python3 certify_adv3_upper.py [R]   (default R = 153/5000 = 0.0306)"""
import json
import os
import sys
import warnings
from fractions import Fraction as Fr
import numpy as np
import cvxpy as cp
import rb
from adversarial_ratio import build

warnings.filterwarnings('ignore')
R = Fr(sys.argv[1]) if len(sys.argv) > 1 else Fr(153, 5000)
LOG = os.path.join(rb.SFREE, '..', 'logs', 'adversarial_ratio_8_margin.log')
rec = [json.loads(l) for l in open(LOG) if l.startswith('{')][3]
sbar, P = build(np.array(rec['theta']))
c = np.ones(3)
z, lam = rb.zK(sbar, P, c)
Pt = rb.scaled_rays(P, c, z)
print('zK (float) = %r, z_K - 1 = %.3e, q(sbar) = %.4e' % (z, z - 1, rb.q(sbar)))

# ---- dual in the normalized frame: Y'_0 + sum_j (I + R N_j) Y'_j = 0, Y'_j >= t I, sum tr = 1, max t
Pn = rb.normalize(sbar, Pt)
Ns = [np.eye(2)] + [np.eye(2) + float(R) * rb.M(Pn[:, j], h=0.0) for j in range(3)]
Ys = [cp.Variable((2, 2), symmetric=True) for _ in range(4)]
t = cp.Variable()
expr = sum(Ns[j] @ Ys[j] for j in range(4))
cons = [expr == 0, sum(cp.trace(Y) for Y in Ys) == 1] + [Y - t * np.eye(2) >> 0 for Y in Ys]
pr = cp.Problem(cp.Maximize(t), cons)
pr.solve(solver='CLARABEL')
print('normalized-frame dual: status %s, margin t = %.4e' % (pr.status, t.value))

# ---- map back: normalized map phi has alpha = 1/sqrt(qbar), beta = 1/sqrt(qbar), a = -alpha xbar, b = -beta ybar;
# M(phi(s)) = A M(s) B^T with B = [[beta, b], [0, 1]], so sum_j M(v_j) (B^T Y'_j B) = 0 in the original frame
qb = rb.q(sbar)
beta = 1.0 / np.sqrt(qb)
Bm = np.array([[beta, -beta * sbar[1]], [0.0, 1.0]])
Yo = [Bm.T @ Y.value @ Bm for Y in Ys]


def frac_sym(A, den=10 ** 15):
    a = Fr(A[0, 0]).limit_denominator(den)
    b = Fr(0.5 * (A[0, 1] + A[1, 0])).limit_denominator(den)
    d = Fr(A[1, 1]).limit_denominator(den)
    return [[a, b], [b, d]]


def mat_mul(A, B):
    return [[A[i][0] * B[0][j] + A[i][1] * B[1][j] for j in range(2)] for i in range(2)]


def mat_add(A, B):
    return [[A[i][j] + B[i][j] for j in range(2)] for i in range(2)]


def Mq(s):
    return [[s[2], s[0]], [s[1], Fr(1)]]


def inv2(A):
    d = A[0][0] * A[1][1] - A[0][1] * A[1][0]
    return [[A[1][1] / d, -A[0][1] / d], [-A[1][0] / d, A[0][0] / d]]


sq = [Fr(v) for v in sbar]
Pq = [[Fr(v) for v in Pt[:, j]] for j in range(3)]
V = [sq] + [[sq[i] + R * Pq[j][i] for i in range(3)] for j in range(3)]
Yq = [None] + [frac_sym(Yo[j]) for j in range(1, 4)]
Minv0 = inv2(Mq(V[0]))


def Y0_of(Y1scale):
    Z = [[Fr(0), Fr(0)], [Fr(0), Fr(0)]]
    for j in range(1, 4):
        Yj = [[Y1scale * v for v in row] for row in Yq[j]] if j == 1 else Yq[j]
        Z = mat_add(Z, mat_mul(Mq(V[j]), Yj))
    Y0 = mat_mul(Minv0, Z)
    return [[-v for v in row] for row in Y0]


# asymmetry of Y0 is affine in the scale mu of Y_1: solve for mu exactly
a0 = Y0_of(Fr(1))
a1 = Y0_of(Fr(2))
asym = lambda Y: Y[0][1] - Y[1][0]
mu = 1 - asym(a0) / (asym(a1) - asym(a0))
Yq[1] = [[mu * v for v in row] for row in Yq[1]]
Y0 = Y0_of(Fr(1))
Yq[0] = Y0


def pd(Y):
    return Y[0][1] == Y[1][0] and Y[0][0] > 0 and Y[0][0] * Y[1][1] - Y[0][1] * Y[1][0] > 0


res = mat_add(mat_mul(Mq(V[0]), Yq[0]), [[Fr(0)] * 2] * 2)
for j in range(1, 4):
    res = mat_add(res, mat_mul(Mq(V[j]), Yq[j]))
checks = {
    'sum_j M(v_j) Y_j = 0 exactly': all(v == 0 for row in res for v in row),
    'Y_0 symmetric positive definite': pd(Yq[0]),
    'Y_1, Y_2, Y_3 symmetric positive definite': all(pd(Yq[j]) for j in range(1, 4)),
}
print('R = %s = %.6f; exact rescaling of Y_1: mu - 1 = %.3e' % (R, float(R), float(mu - 1)))
for k, v in checks.items():
    print('  %s: %s' % (k, 'PASS' if v else 'FAIL'))
ok = all(checks.values())
print('conclusion (exact, float instance data): no orbit set with sbar in its interior contains T_R, so z_A/z_K <= %s'
      % R if ok else 'certificate not established')
print('ALL PASS' if ok else 'SOME FAIL')
