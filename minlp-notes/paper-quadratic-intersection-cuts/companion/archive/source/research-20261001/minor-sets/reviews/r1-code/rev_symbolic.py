"""Reviewer r1 (second reviewer): symbolic and exact checks of identities used in the minor-sets note.
Does not import the stream's code.
 1. Prop 1 coordinates: M = x1 I + x2 J' + y1 K + y2 L, det = |x|^2 - |y|^2, x1(R_phi^T M) formula,
    and SCIP's eigenvector coordinates equal (x1, x2, y1, y2) up to the factor sqrt(2).
 2. Prop 3(2): g(M) = A M B^T maps C_F to C_F' with F'^T = B F^T A^{-1} (symbolic identity
    B F^T A^{-1} (A M B^T) = B (F^T M) B^T, a congruence); transposition gives F^{-1}.
 3. Lemma 6 identities for symbolic a0, b0, D (with the tangency constraint).
 4. Prop 11: the four step lengths of C_I and of C_diag(1,1/delta), symbolic in delta.
 5. Theorem 8: the small z = 1 certificate printed in the note (sum_V V Y_V = 0, Y_V PD).
 6. Adversarial corners: non-degeneracy margins of the float corners (recomputed) and of the
    corners rounded to denominator 10^4 (the corners that were actually certified).
Usage: python3 rev_symbolic.py LOGDIR
"""
import json
import sys
from fractions import Fraction as Fr

import numpy as np
import sympy as sp

LOGDIR = sys.argv[1]
ok_all = True


def chk(name, cond):
    global ok_all
    ok_all &= bool(cond)
    print(('PASS ' if cond else 'FAIL ') + name, flush=True)


# 1
x1, x2, y1, y2, ph = sp.symbols('x1 x2 y1 y2 phi', real=True)
I2 = sp.eye(2); Jp = sp.Matrix([[0, -1], [1, 0]]); K = sp.Matrix([[-1, 0], [0, 1]]); L = sp.Matrix([[0, 1], [1, 0]])
M = x1 * I2 + x2 * Jp + y1 * K + y2 * L
a, b, c, d = M[0, 0], M[0, 1], M[1, 0], M[1, 1]
chk('1: det M = x1^2 + x2^2 - y1^2 - y2^2', sp.expand(M.det() - (x1**2 + x2**2 - y1**2 - y2**2)) == 0)
chk('1: xhat = ((a+d)/2, (c-b)/2), yhat = ((d-a)/2, (b+c)/2)',
    sp.simplify((a + d) / 2 - x1) == 0 and sp.simplify((c - b) / 2 - x2) == 0 and sp.simplify((d - a) / 2 - y1) == 0
    and sp.simplify((b + c) / 2 - y2) == 0)
R = sp.cos(ph) * I2 + sp.sin(ph) * Jp
N = sp.expand(R.T * M)
# coordinates of N
nx1, nx2 = (N[0, 0] + N[1, 1]) / 2, (N[1, 0] - N[0, 1]) / 2
ny1, ny2 = (N[1, 1] - N[0, 0]) / 2, (N[0, 1] + N[1, 0]) / 2
chk('1: x1(R^T M) = cos x1 + sin x2, x2(R^T M) = cos x2 - sin x1', sp.simplify(nx1 - (sp.cos(ph) * x1 + sp.sin(ph) * x2)) == 0
    and sp.simplify(nx2 - (sp.cos(ph) * x2 - sp.sin(ph) * x1)) == 0)
chk('1: |yhat(R^T M)| = |yhat(M)|', sp.simplify(ny1**2 + ny2**2 - y1**2 - y2**2) == 0)
S = (N + N.T) / 2
chk('1: sym(N) = [[x1-y1, y2],[y2, x1+y1]] in N-coordinates',
    sp.simplify(S - sp.Matrix([[nx1 - ny1, ny2], [ny2, nx1 + ny1]])) == sp.zeros(2, 2))
EV = sp.Matrix([[1, 1, 0, 0], [0, 0, -1, 1], [-1, 1, 0, 0], [0, 0, 1, 1]]) / sp.sqrt(2)
v = sp.Matrix([a, d, b, c])   # SCIP vars order (xik, xjl, xil, xjk)
chk('1: SCIP eigen-coordinates = sqrt(2) (x1, x2, y1, y2)',
    sp.simplify(EV * v - sp.sqrt(2) * sp.Matrix([x1, x2, y1, y2])) == sp.zeros(4, 1))
# BCM (14a) in these coordinates
l1, l2 = sp.symbols('l1 l2', real=True)
chk('1: BCM (14a) lhs = 2(l1 x1 - l2 x2), rhs^2 = 4|y|^2',
    sp.simplify(l1 * (a + d) + l2 * (b - c) - 2 * (l1 * x1 - l2 * x2)) == 0
    and sp.simplify((b + c)**2 + (a - d)**2 - 4 * (y1**2 + y2**2)) == 0)

# 2
A = sp.Matrix(2, 2, sp.symbols('a11 a12 a21 a22')); B = sp.Matrix(2, 2, sp.symbols('b11 b12 b21 b22'))
F = sp.Matrix(2, 2, sp.symbols('f11 f12 f21 f22')); Mg = sp.Matrix(2, 2, sp.symbols('m11 m12 m21 m22'))
FpT = B * F.T * A.inv()
chk('2: F\'^T (A M B^T) = B (F^T M) B^T', sp.simplify(FpT * (A * Mg * B.T) - B * (F.T * Mg) * B.T) == sp.zeros(2, 2))
# transposition: v^T F^T M v = (Fv)^T M^T ... -> u^T F^{-T} M^T u with u = F v
vv = sp.Matrix(sp.symbols('v1 v2'))
u = F * vv
chk('2: v^T F^T M v = u^T F^{-T} M^T u, u = F v',
    sp.simplify((vv.T * F.T * Mg * vv)[0] - (u.T * F.inv().T * Mg.T * u)[0]) == 0)

# 3 Lemma 6
p1, p2, q1, q2 = sp.symbols('p1 p2 q1 q2', real=True)
a0 = sp.Matrix([p1, p2]); b0 = sp.Matrix([q1, q2]); M0 = a0 * b0.T
D = sp.Matrix(2, 2, sp.symbols('d11 d12 d21 d22', real=True))
J = sp.Matrix([[0, 1], [-1, 0]])
adj = lambda X: sp.Matrix([[X[1, 1], -X[0, 1]], [-X[1, 0], X[0, 0]]])
G0, G1 = J * adj(D), J * adj(M0)
chk('3: adj(a b^T) = (J b)(J a)^T', sp.simplify(adj(M0) - (J * b0) * (J * a0).T) == sp.zeros(2, 2))
chk('3: adj(D) = J^T D^T J', sp.simplify(adj(D) - J.T * D.T * J) == sp.zeros(2, 2))
chk('3: G1 a0 = 0', sp.simplify(G1 * a0) == sp.zeros(2, 1))
tang = (adj(M0) * D).trace()
chk('3: (J b0)^T G0 a0 = tr(adj(M0) D)', sp.simplify((J * b0).T * G0 * a0 - sp.Matrix([[tang]])) == sp.zeros(1, 1))
kap = sp.symbols('kappa')
chk('3: det(G0 + k G1) = det D + k tr(adj(M0) D)', sp.expand((G0 + kap * G1).det() - D.det() - kap * tang) == 0)
chk('3: J adj(D + k M0) = G0 + k G1', sp.simplify(J * adj(D + kap * M0) - G0 - kap * G1) == sp.zeros(2, 2))

# 4 Prop 11
dl, t = sp.symbols('delta t', positive=True)
sb = sp.Matrix([[1, 0], [0, dl]])
rays = [sp.Matrix([[0, 1], [0, 0]]), sp.Matrix([[-1, 0], [0, 0]]), sp.Matrix([[0, 0], [0, -dl]]), sp.Matrix([[0, 0], [-dl, 0]])]


def step_sym(FT, sbar, p):
    X = FT * (sbar + t * p); X = (X + X.T) / 2
    # PSD boundary: first t > 0 where det = 0 or a diagonal entry = 0
    cands = [r for r in sp.solve(sp.Eq(X.det(), 0), t) if r.is_positive] + \
            [r for r in sp.solve(sp.Eq(X[0, 0], 0), t) if r.is_positive] + [r for r in sp.solve(sp.Eq(X[1, 1], 0), t) if r.is_positive]
    return sp.Min(*cands) if cands else sp.oo


stI = [sp.simplify(step_sym(sp.eye(2), sb, p)) for p in rays]
print('   C_I steps:', stI)
chk('4: C_I steps = (2 sqrt(delta), 1, 1, 2/sqrt(delta))',
    [sp.simplify(x - y) for x, y in zip(stI, [2 * sp.sqrt(dl), 1, 1, 2 / sp.sqrt(dl)])] == [0, 0, 0, 0])
stD = [sp.simplify(step_sym(sp.diag(1, 1 / dl), sb, p)) for p in rays]
print('   C_diag steps:', stD)
chk('4: C_diag(1,1/delta) steps = (2, 1, 1, 2)', stD == [2, 1, 1, 2])
lam = sp.symbols('l1:5', nonnegative=True)
Mx = sb + sum((lam[i] * rays[i] for i in range(4)), sp.zeros(2, 2))
chk('4: det(sbar + P lam) = delta[(1-l2)(1-l3) + l1 l4]',
    sp.expand(Mx.det() - dl * ((1 - lam[1]) * (1 - lam[2]) + lam[0] * lam[3])) == 0)
chk('4: (16 + 2 sqrt 73)/3 < 11.1', float((16 + 2 * sp.sqrt(73)) / 3) < 11.1)
# BCM bound numerically for delta in a grid (dense scan over phi)
J2 = np.array([[0.0, 1.0], [-1.0, 0.0]])


def stepn(FT, s, p):
    A0 = FT @ s; A0 = (A0 + A0.T) / 2
    B0 = FT @ p; B0 = (B0 + B0.T) / 2
    ev = np.linalg.eigvalsh(A0)
    if ev[0] <= 0:
        return -np.inf
    Lc = np.linalg.cholesky(A0); Li = np.linalg.inv(Lc)
    mn = np.linalg.eigvalsh(Li @ B0 @ Li.T)[0]
    return np.inf if mn >= 0 else -1.0 / mn


worst = 0.0
for k in range(1, 9):
    dv = 0.25 * 10.0 ** (-(k - 1) / 1.0)
    s = np.diag([1.0, dv]); P = [np.array([[0, 1.0], [0, 0]]), np.array([[-1.0, 0], [0, 0]]),
                                 np.array([[0, 0], [0, -dv]]), np.array([[0, 0], [-dv, 0]])]
    best = 0.0
    for phv in np.linspace(-np.pi / 2, np.pi / 2, 200001):
        FT = np.cos(phv) * np.eye(2) + np.sin(phv) * J2
        v_ = min(stepn(FT, s, p) for p in P)
        best = max(best, v_)
    worst = max(worst, best / np.sqrt(dv))
    print('   delta %.2e: best BCM (scan) = %.6f = %.4f sqrt(delta)' % (dv, best, best / np.sqrt(dv)))
chk('4: best BCM bound / sqrt(delta) <= 11.1 on the grid (max %.4f)' % worst, worst <= 11.1)

# 5 Theorem 8 small certificate at z = 1
sbar = [Fr(0), Fr(5, 2), Fr(-1, 2), Fr(-1, 2)]
V = [sbar, [Fr(-5), Fr(3), Fr(4), Fr(-4)], [Fr(-8), Fr(12), Fr(-8), Fr(8)], [Fr(-3, 2), Fr(-4), Fr(2), Fr(-7, 2)],
     [Fr(-7, 2), Fr(-1, 2), Fr(3, 2), Fr(-4)]]
Y = [[[Fr(237, 250), Fr(133, 500)], [Fr(133, 500), Fr(57, 500)]], [[Fr(453, 1000), Fr(7, 20)], [Fr(7, 20), Fr(29, 100)]],
     [[Fr(9, 100), Fr(11, 100)], [Fr(11, 100), Fr(17, 100)]], [[Fr(1, 100), Fr(0)], [Fr(0), Fr(7, 50)]],
     [[Fr(1, 100), Fr(0)], [Fr(0), Fr(1, 100)]]]
Ssum = [[sum(sum(Vv[2 * i + k] * Yv[k][j] for k in range(2)) for Vv, Yv in zip(V, Y)) for j in range(2)] for i in range(2)]
chk('5: note Thm 8 z=1 certificate: sum_V V Y_V = 0 (got %s)' % Ssum, Ssum == [[0, 0], [0, 0]])
chk('5: all Y_V positive definite', all(Yv[0][0] > 0 and Yv[0][0] * Yv[1][1] - Yv[0][1] ** 2 > 0 for Yv in Y))


# 6 adversarial margins
def pf(s, t):
    return 0.5 * (s[0] * t[3] + s[3] * t[0] - s[1] * t[2] - s[2] * t[1])


def margins(sb, Vs, t0=None):
    sb = np.asarray(sb, float); Vs = [np.asarray(x, float) for x in Vs]
    P = [x - sb for x in Vs]
    ds = sb[0] * sb[3] - sb[1] * sb[2]
    m = []
    for p in P:
        Bv = pf(sb, p); dp = p[0] * p[3] - p[1] * p[2]
        m.append(abs(Bv * Bv - ds * dp) / (Bv * Bv + abs(ds * dp)))
    if t0 is None:     # recompute t* as the minimizer on the edge [v1, v2] (tangent point)
        # det(v2 + s (v1 - v2)) minimal over s in [0, 1]
        dd = Vs[0] - Vs[1]
        ss = np.linspace(0, 1, 200001)
        vals = [(Vs[1] + x * dd) for x in ss[::1000]]
        a_ = dd[0] * dd[3] - dd[1] * dd[2]; b_ = 2 * pf(Vs[1], dd)
        s0 = -b_ / (2 * a_)
        t0 = Vs[1] + s0 * dd
    g = np.array([t0[3], -t0[2], -t0[1], t0[0]])
    gp = [g @ p for p in P]
    sig = -1.0 / gp[0]
    nu = [1 + sig * x for x in gp]
    m += [nu[2], nu[3]]
    dd = Vs[0] - Vs[1]
    ddet = dd[0] * dd[3] - dd[1] * dd[2]; Bd = pf(dd, sb)
    m.append(ddet * ds / (Bd * Bd + ddet * ds) if ddet > 0 else -1.0)
    m.append(ds / max(abs(p[0] * p[3] - p[1] * p[2]) + abs(pf(sb, p)) for p in P))
    return m


for f in ('adversarial_m01_s1.jsonl', 'adversarial_m01_s2.jsonl', 'adversarial_m05_s1.jsonl'):
    for line in open(LOGDIR + '/' + f):
        r = json.loads(line)
        if 'V' not in r:
            continue
        mf = margins(r['sbar'], r['V'], np.array(r['t0']))
        sbq = [float(Fr(x).limit_denominator(10 ** 4)) for x in r['sbar']]
        Vq = [[float(Fr(x).limit_denominator(10 ** 4)) for x in v] for v in r['V']]
        mq = margins(sbq, Vq)
        print('   %s start %3d: final ratio %.4f; min margin float %.5f (logged %.5f, argmin %d); rounded corner: min margin %.5f (argmin %d)'
              % (f, r['start'], r['final_cert'], min(mf), min(r['margins']), int(np.argmin(mf)), min(mq), int(np.argmin(mq))))
print('ALL PASS' if ok_all else 'SOME CHECK FAILED')
