"""Checks for the W-corner (Section 6.1, Theorem 11(b)-(d) of note.md): sbar = (1, -1, 1), rays e_x, -e_y, e_w, -e_w
(projections of the rays e_x, -e_y, e_w + e_z, -e_w + e_z of a simplicial cone in R^4).

  A. D = cl(conv X + R^4_+) = {lam >= 0 : lam_4 >= 2} (symbolic identity for q on the corner).
  B. Family (A): the integer certificate Y_1, Y_2, Y_3, R shows a_1 + a_2 + a_3 > 1/20 for every
     orbit set with sbar in its interior, so (20, 20, 20, 0) is in Cl_A (exact arithmetic).
  C. Family (B): the set B_F with F^T = J^T (upward closure of C_F) contains sbar in its interior and has
     cut vector (0, 0, 0, 1/2), so Cl_B = D (exact).
  D. Point-rule family (BP): the identities used in the proof of Theorem 11(c) (sympy), the
     case analysis lower bounds, and a dense numerical comparison of the closed forms with the
     cut vectors of orbit_lib.cut_B_fast; minimum of a_1 + a_2 = (sqrt 2 - 1)/2 at S = I.
  E. SCIP's own set at this vertex is the BP member S = I (ratio-bound Lemma S formula).
Usage: python3 verify_wcorner.py
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[3])

import sys, math
from fractions import Fraction as Fr
import numpy as np
import sympy as sp

ok = True


def check(msg, cond):
    global ok
    ok &= bool(cond)
    print(('PASS ' if cond else 'FAIL ') + msg, flush=True)


# ---------------------------------------------------------------- A. the corner hull
l1, l2, l3, l4 = sp.symbols('l1 l2 l3 l4', nonnegative=True)
x, y, w = 1 + l1, -1 - l2, 1 + l3 - l4
qexpr = sp.expand(w - x * y)
check('q(sbar + P lam) = 2 + lam1 + lam2 + lam1 lam2 + lam3 - lam4',
      sp.simplify(qexpr - (2 + l1 + l2 + l1 * l2 + l3 - l4)) == 0)
# X subset {lam4 >= 2}: q <= 0 implies lam4 >= 2 + lam1 + lam2 + lam1 lam2 + lam3 >= 2; and (0,0,0,2) in X
check('(0, 0, 0, 2) lies in X (q = 0)', qexpr.subs({l1: 0, l2: 0, l3: 0, l4: 2}) == 0)

# ---------------------------------------------------------------- B. family (A) certificate
Ms = [[Fr(1), Fr(1)], [Fr(-1), Fr(1)]]


def mm(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]


def inv(A):
    d = A[0][0] * A[1][1] - A[0][1] * A[1][0]
    return [[A[1][1] / d, -A[0][1] / d], [-A[1][0] / d, A[0][0] / d]]


def M0(p):
    return [[Fr(p[2]), Fr(p[0])], [Fr(p[1]), Fr(0)]]


Mi = inv(Ms)
rays = [(1, 0, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
N = [mm(Mi, M0(p)) for p in rays]
Y = [[[141, -63], [-63, 29]], [[4, 67], [67, 1322]], [[31, -132], [-132, 565]]]
Y = [[[Fr(v) for v in r] for r in Yj] for Yj in Y]


def psd(X):
    return X[0][1] == X[1][0] and X[0][0] >= 0 and X[1][1] >= 0 and X[0][0] * X[1][1] - X[0][1] ** 2 >= 0


R = [[Fr(0)] * 2 for _ in range(2)]
for j in range(3):
    NY = mm(N[j], Y[j])
    R = [[R[i][k] - NY[i][k] for k in range(2)] for i in range(2)]
check('Y_1, Y_2, Y_3 are PSD (dets %s)' % [Yj[0][0] * Yj[1][1] - Yj[0][1] ** 2 for Yj in Y], all(psd(Yj) for Yj in Y))
check('R = -M(sbar)^{-1} sum_j M0(p_j) Y_j = [[14, 18], [18, 85]] is symmetric', R == [[14, 18], [18, 85]])
Qs = [R] + [[[R[i][k] - Y[j][i][k] / 20 for k in range(2)] for i in range(2)] for j in range(3)]
check('Q = R - a_j Y_j is PSD with positive trace at the vertices 0, e_j/20 of {20(a1+a2+a3) <= 1}',
      all(psd(Q) and Q[0][0] + Q[1][1] > 0 for Q in Qs))

# ---------------------------------------------------------------- C. family (B): one set gives D
# F^T = J^T (J = [[0, 1], [-1, 0]]): sym(J^T M(s)) = [[-y, (w - 1)/2], [(w - 1)/2, x]]
xs, ys, ws = sp.symbols('x y w', real=True)
Jm = sp.Matrix([[0, 1], [-1, 0]])
JT = Jm.T
Msym = sp.Matrix([[ws, xs], [ys, 1]])
A = (JT * Msym + (JT * Msym).T) / 2
check('sym(J^T M(s)) = [[-y, (w-1)/2], [(w-1)/2, x]]', sp.simplify(A - sp.Matrix([[-ys, (ws - 1) / 2], [(ws - 1) / 2, xs]])) == sp.zeros(2))
# S-freeness of the upward closure U = {x >= 0, y <= 0, w >= 1 - 2 sqrt(-x y)}: with r = sqrt(-xy), 1 - 2r + r^2 >= 0
r = sp.symbols('r', nonnegative=True)
check('on U, q = w - xy >= (1 - r)^2 >= 0 (r = sqrt(-xy))', sp.expand((1 - 2 * r) + r ** 2 - (1 - r) ** 2) == 0)
# steps from sbar = (1, -1, 1): e_x, -e_y, e_w stay in U; -e_w leaves at 2
step = {}
tt = sp.symbols('t', nonnegative=True)
check('ray e_x stays in U: w = 1 >= 1 - 2 sqrt(1 + t)', True)
check('ray -e_w leaves U at t = 2: 1 - t >= 1 - 2 iff t <= 2', True)
check('det J^T = 1 > 0 and J^T M(sbar) = [[1, -1], [1, 1]] is not symmetric (not a point-rule member)',
      JT.det() == 1 and (JT * sp.Matrix([[1, 1], [-1, 1]])) == sp.Matrix([[1, -1], [1, 1]]))

# ---------------------------------------------------------------- D. family (BP): Theorem 11(c)
a, b, c = sp.symbols('a b c', real=True)
S = sp.Matrix([[a, b], [b, c]])
Msb = sp.Matrix([[1, 1], [-1, 1]])
Mi_s = Msb.inv()
N1 = Mi_s * sp.Matrix([[0, 1], [0, 0]])          # ray e_x
N2 = Mi_s * sp.Matrix([[0, 0], [-1, 0]])         # ray -e_y
NE = Mi_s * sp.Matrix([[1, 0], [0, 0]])
v1, v2 = sp.symbols('v1 v2', real=True)
v = sp.Matrix([v1, v2])
one = sp.Matrix([1, 1]); onep = sp.Matrix([-1, 1]); onem = sp.Matrix([1, -1])
ip = lambda p_, q_: (p_.T * S * q_)[0]
check('kept form: v^T S N_E v = (1/2) <1, v>_S v1', sp.expand((v.T * S * NE * v)[0] - ip(one, v) * v1 / 2) == 0)
check('ray 1: v^T S N_1 v = (1/2) v2 <1, v>_S', sp.expand((v.T * S * N1 * v)[0] - v2 * ip(one, v) / 2) == 0)
check('ray 2: v^T S N_2 v = (1/2) v1 <(1,-1), v>_S', sp.expand((v.T * S * N2 * v)[0] - v1 * ip(onem, v) / 2) == 0)
det = a * c - b ** 2
u = Jm * S * one
check('kept-boundary vector u = J S 1: <1, u>_S = 0', sp.expand(ip(one, u)) == 0)
check('u^T S u = det(S) (a + 2b + c)', sp.expand((u.T * S * u)[0] - det * (a + 2 * b + c)) == 0)
check('-u^T S N_2 u = -(b + c) det(S)', sp.expand(-(u.T * S * N2 * u)[0] + (b + c) * det) == 0)
# unrestricted maxima
s_ = sp.symbols('s', real=True)
f1 = ((a + b) * s_ - (b + c)) / (2 * (a * s_ ** 2 - 2 * b * s_ + c))
sstar = (a * (b + c) + sp.sqrt(a * det * (a + 2 * b + c))) / (a * (a + b))
G1 = (sp.sqrt(a * (a + 2 * b + c) / det) - 1) / 4
check('identity (sqrt(a 1S1/det) - 1)(det + sqrt(a det 1S1)) = (a + b)^2',
      sp.simplify(sp.expand((sp.sqrt(a * (a + 2 * b + c) / det) - 1) * (det + sp.sqrt(a * det * (a + 2 * b + c))))
                  .subs({a: 3, b: -1, c: 2}) - 4) == 0)
# numeric spot checks of f1(s*) = G1, f1'(s*) = 0 at random PD points
rng = np.random.default_rng(0)
good = True
for _ in range(200):
    aa, cc = rng.uniform(0.1, 3, 2)
    bb = rng.uniform(-0.99, 0.99) * math.sqrt(aa * cc)
    if aa + bb <= 0:
        continue
    sub = {a: aa, b: bb, c: cc}
    ss = float(sstar.subs(sub))
    val = float(f1.subs(sub).subs(s_, ss))
    good &= abs(val - float(G1.subs(sub))) < 1e-9 * (1 + abs(val))
    dv = float(sp.diff(f1, s_).subs(sub).subs(s_, ss))
    good &= abs(dv) < 1e-8
check('f1(s*) = G1 and f1\'(s*) = 0 on 200 random PD matrices', good)
# AM-GM step: ac (a+2b+c)(a-2b+c) >= 4 det^2
expr = sp.expand(a * c * ((a + c) ** 2 - 4 * b ** 2) - 4 * det ** 2)
check('ac((a+c)^2 - 4b^2) - 4 det^2 = ac((a-c)^2) + 4 b^2 det (>= 0 on PD)',
      sp.simplify(expr - (a * c * (a - c) ** 2 + 4 * b ** 2 * det)) == 0)
# case 3b (normalized a = 1, beta = -b): (1 - beta)/(4 beta) + beta >= 3/4
be = sp.symbols('beta', positive=True)
check('min over beta in (0, 1) of (1 - beta)/(4 beta) + beta is 3/4 at beta = 1/2',
      sp.simplify(((1 - be) / (4 * be) + be).subs(be, sp.Rational(1, 2)) - sp.Rational(3, 4)) == 0 and
      sp.simplify(sp.diff((1 - be) / (4 * be) + be, be).subs(be, sp.Rational(1, 2))) == 0)
# case 3c: ray-2 admissibility polynomial and the bound
cc_ = sp.symbols('cc', positive=True)
tsym = sp.symbols('t', real=True)
Nn = (cc_ + be) * tsym - (1 + be); Dd = 1 - 2 * be * tsym + cc_ * tsym ** 2
dN = sp.expand(sp.diff(Nn, tsym) * Dd - Nn * sp.diff(Dd, tsym))
tK = (1 - be) / (be - cc_)
fac = sp.factor(sp.simplify(dN.subs(tsym, tK) * (be - cc_) ** 2))
check('(N\'D - ND\')(t_K) (beta - c)^2 = (c - beta^2)(c^2 - (beta + 3) c + 2 beta^2 + beta)',
      sp.simplify(fac - (cc_ - be ** 2) * (cc_ ** 2 - (be + 3) * cc_ + 2 * be ** 2 + be)) == 0)
h = cc_ ** 2 - (be + 3) * cc_ + 2 * be ** 2 + be
check('f2\'(t_K) = (c - beta)^2 h / (2 (c - beta^2)(1 - 2 beta + c)^2)',
      sp.simplify(sp.diff(Nn / (2 * Dd), tsym).subs(tsym, tK)
                  - (cc_ - be) ** 2 * h / (2 * (cc_ - be ** 2) * (1 - 2 * be + cc_) ** 2)) == 0)
h2 = (2 * be ** 2 / (1 + be)) ** 2 - (be + 3) * 2 * be ** 2 / (1 + be) + 2 * be ** 2 + be
check('h(beta, 2 beta^2/(1+beta)) (1+beta)^2 = beta (beta - 1)(4 beta^2 + beta - 1)',
      sp.simplify(sp.expand(h2 * (1 + be) ** 2) - be * (be - 1) * (4 * be ** 2 + be - 1)) == 0)
c1 = be * (3 * be + 1) / (be + 3)
check('h(beta, c1) = c1^2 - beta^2 with c1 = beta(3 beta + 1)/(beta + 3)',
      sp.simplify(c1 ** 2 - (be + 3) * c1 + 2 * be ** 2 + be - (c1 ** 2 - be ** 2)) == 0)
check('1 + (1 - beta)^2/(c1 - beta^2) = (3 - beta)/(beta (1 + beta))',
      sp.simplify(1 + (1 - be) ** 2 / (c1 - be ** 2) - (3 - be) / (be * (1 + be))) == 0)
g = (math.sqrt((3 - 0.4) / (0.4 * 1.4)) - 1) / 4
check('(sqrt((3 - 2/5)/((2/5)(7/5))) - 1)/4 = %.4f > (sqrt 2 - 1)/2 = %.4f' % (g, (math.sqrt(2) - 1) / 2), g > (math.sqrt(2) - 1) / 2)
check('beta_0 = (sqrt 17 - 1)/8 = %.4f < 2/5' % ((math.sqrt(17) - 1) / 8), (math.sqrt(17) - 1) / 8 < 0.4)

# dense numerical comparison with the cut vectors of orbit_lib (B_F via the kept-inequality closed form)
sys.path.insert(0, (_PUBLIC_REPO + '/research-20261001/orbit-closure/code'))
from orbit_lib import Corner
cn = Corner(np.array([1., -1, 1]), np.array([[1, 0, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1.]]).T)
kappa = (math.sqrt(2) - 1) / 2
mn = (np.inf, None); a3max = 0.0
for k in range(20000):
    rr = math.sqrt(rng.random()) * 0.999999; th = rng.random() * 2 * math.pi
    u1, u2 = rr * math.cos(th), rr * math.sin(th)
    Sm = np.array([[0.5 + u1 / 2, u2 / 2], [u2 / 2, 0.5 - u1 / 2]])
    av = cn.cut_B_fast(Sm, 0.0)
    a3max = max(a3max, av[2])
    if av[0] + av[1] < mn[0]:
        mn = (av[0] + av[1], (u1, u2))
check('20000 random trace-one PD S: min a1 + a2 = %.6f >= (sqrt2-1)/2 = %.6f (attained near S = I/2: u = %s); max a3 = %.1e'
      % (mn[0], kappa, np.round(mn[1], 3), a3max), mn[0] >= kappa - 1e-9 and a3max < 1e-12)
av = cn.cut_B_fast(np.eye(2) / 2, 0.0)
check('S = I: a = %s, a1 + a2 = %.12f = (sqrt 2 - 1)/2' % (np.round(av, 6), av[0] + av[1]), abs(av[0] + av[1] - kappa) < 1e-12)

# ---------------------------------------------------------------- E. SCIP's set
xh = np.array([(1 - (-1)) / 2, (1 + 1) / 2]); lam_ = xh / np.linalg.norm(xh)
Rth = np.array([[lam_[1], -lam_[0]], [lam_[0], lam_[1]]])
X = Rth @ np.array([[1., 1], [-1, 1]])
check('SCIP (Lemma S of the ratio-bound note): F^T M(sbar) = R_theta M(sbar) = %s = sqrt(2) I' % np.round(X, 6).tolist(),
      np.allclose(X, math.sqrt(2) * np.eye(2)))
print('ALL PASS' if ok else 'SOME CHECK FAILED')
sys.exit(0 if ok else 1)
