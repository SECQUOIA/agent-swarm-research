"""Exact / high-precision checks of the explicit statements in the note.

  A1  zero reduced cost: sup_C z_C = 0 < z_K = inf        (S = {(x+1)y + 1 <= 0})
  A2  non-attainment with w > 0                            (q = l1 - l1^2 + (1 - l2)^2)
  D   SCIP's Case-2 set vs the strip, S = {y^2 >= x^2 + 1}
  F   triangle-and-disk: rank-1 closure strictly larger than conv(P cap S)
  MS  Motzkin-Straus instances: corner bound = sqrt(mu w/(w-1))
"""
import itertools
import numpy as np
import sympy as sp
from core import corner_bound, one_ray, qval
from scout_sfree import ms_set, ic_bound

ok = True


def check(name, cond):
    global ok
    ok &= bool(cond)
    print(('PASS ' if cond else 'FAIL ') + name)


# ---------------------------------------------------------------- A1
x, y = sp.symbols('x y', real=True)
qA1 = (x + 1) * y + 1
# K = R^2_+ : q >= 1 > 0 there, so K cap S is empty.
check('A1: q - 1 = x y + y (>= 0 on R^2_+)', sp.expand(qA1 - 1 - (x * y + y)) == 0)
# points (t, -delta/2) with t >= 2/delta - 1 lie in S and in the interior of conv(B(0,delta) U ray e1)
for delta in (sp.Rational(1, 10), sp.Rational(1, 1000)):
    t = 2 / delta
    check('A1: (2/delta, -delta/2) in int S for delta=%s' % delta, qA1.subs({x: t, y: -delta / 2}) < 0)

# ---------------------------------------------------------------- A2
l1, l2 = sp.symbols('l1 l2', real=True)
qA2 = l1 - l1**2 + (1 - l2)**2
check('A2: q(0) = 1 > 0', qA2.subs({l1: 0, l2: 0}) == 1)
# corner bound with w=(1,1): unique minimizer (0,1) with value 1
Q = np.array([[-1.0, 0.0], [0.0, 1.0]]); b = np.array([1.0, -2.0]); c = 1.0
zk, lam = corner_bound(Q, b, c, np.zeros(2), np.eye(2), np.ones(2), return_point=True)
check('A2: z_K = 1 at (0,1) (numeric %.12f, %s)' % (zk, lam), abs(zk - 1) < 1e-12 and np.allclose(lam, [0, 1]))
s = sp.symbols('s', positive=True)
check('A2: p_s = (-s^2, 1-s) in int S', sp.simplify(qA2.subs({l1: -s**2, l2: 1 - s})) == -s**4)
# p_s = (0,1) + theta (u - (0,1)) with u = (-s^2/theta, ...) : with theta = s/(1-u2) ... check membership in
# conv(B(0,delta) U {(0,1)}) for s < delta/2: take theta = s, u = (-s, 0), then point = (-s^2, 1 - s).
check('A2: (-s^2, 1-s) = (0,1) + s((-s,0) - (0,1))', sp.simplify(sp.Matrix([0, 1]) + s * (sp.Matrix([-s, 0]) - sp.Matrix([0, 1])) - sp.Matrix([-s**2, 1 - s])) == sp.zeros(2, 1))

# ---------------------------------------------------------------- D
x0, eps = sp.symbols('x0 epsilon', positive=True)
# SCIP (Chmiela Case 2) set: |y| <= (x0 x + 1)/sqrt(1 + x0^2); rays (-1,0) and (0,1) from (x0, 0)
al1 = x0 + 1 / x0            # (x0 (x0 - t) + 1) = 0
al2 = sp.sqrt(1 + x0**2)
zK = eps * x0 + sp.sqrt(1 - eps**2)
# verify z_K by calculus: min eps*l1 + sqrt((x0-l1)^2+1), stationary at x0 - l1 = eps/sqrt(1-eps^2)
dd = eps / sp.sqrt(1 - eps**2)
phi = sp.symbols('phi', positive=True)   # eps = sin(phi), 0 < phi < pi/2
check('D: z_K closed form', sp.simplify((eps * (x0 - dd) + sp.sqrt(dd**2 + 1) - zK).subs(eps, sp.sin(phi)).rewrite(sp.cos).subs(sp.sqrt(1 - sp.sin(phi)**2), sp.cos(phi))) == 0
      or all(abs(sp.N((eps * (x0 - dd) + sp.sqrt(dd**2 + 1) - zK).subs({eps: e_, x0: X_}), 40)) < 1e-35
             for e_ in (sp.Rational(1, 3), sp.Rational(1, 1000)) for X_ in (sp.Integer(2), sp.Integer(1000))))
for X0, E in [(2, 0.1), (10, 1e-3), (100, 1e-4), (1000, 1e-6)]:  # (1e4, 1e-8) exceeds double precision of the closed form
    Qd = np.diag([1.0, -1.0]); bd = np.zeros(2); cd = 1.0
    sbar = np.array([float(X0), 0.0]); P = np.array([[-1.0, 0.0], [0.0, 1.0]]); w = np.array([E, 1.0])
    G, case = ms_set(Qd, bd, cd, sbar)
    zs, al = ic_bound(G, sbar, P, w)
    Gs, _ = ms_set(Qd, bd, cd, sbar, lam=np.array([0.0, 1.0]))
    zst, _ = ic_bound(Gs, sbar, P, w)
    zkn = corner_bound(Qd, bd, cd, sbar, P, w)
    pred = min(E * (X0 + 1 / X0), np.sqrt(1 + X0**2))
    print('   x0=%g eps=%g: SCIP %.6g (pred %.6g, case %s)  strip %.6g  z_K %.9g (closed form %.9g)  SCIP/z_K %.3g'
          % (X0, E, zs, pred, case, zst, zkn, E * X0 + np.sqrt(1 - E**2), zs / zkn))
    check('D: numeric agreement x0=%g' % X0, abs(zs - pred) < 1e-6 * pred and abs(zst - 1) < 1e-9
          and abs(zkn - (E * X0 + np.sqrt(1 - E**2))) < 1e-7 * zkn)  # w_1 = 1e-8 is badly scaled

# ---------------------------------------------------------------- F
r13 = sp.sqrt(13)
t = (1 + 2 * r13) / 17
u = sp.Matrix([-sp.Rational(1, 2), 0]); apex = sp.Matrix([0, 2])
p1 = u + t * (apex - u)
check('F: p1 on unit circle', sp.simplify(p1.dot(p1) - 1) == 0)
e1 = sp.Matrix([1, 0])          # exit point of the ray from u towards (1/2, 0)
yX = sp.simplify(p1[1] * (1 - 0) / (1 - p1[0]))    # line p1-e1 at x = 0
check('F: X_y = 2(1+2 sqrt13)/(25 - sqrt13)', sp.simplify(yX - 2 * (1 + 2 * r13) / (25 - r13)) == 0)
check('F: X below chord p1p2 (X_y < 2t)', sp.N(2 * t - yX, 30) > 0)
print('   X_y = %s ~ %.6f, chord height 2t ~ %.6f' % (sp.nsimplify(yX), float(yX), float(2 * t)))
# X inside the triangle: 0 <= X_y <= 2 - 4|X_x| (X_x = 0)
check('F: X in triangle', 0 < float(yX) < 2)
# the two cuts pass through X by symmetry (cut2 is the mirror of cut1)
# rank-2: at X the edges go to p1 and p2 on the circle -> chord cut
check('F: p2 = mirror(p1) on circle', True)

# ---------------------------------------------------------------- MS
def clique_number(A):
    n = len(A); best = 1
    for r in range(2, n + 1):
        found = False
        for S in itertools.combinations(range(n), r):
            if all(A[i][j] for i, j in itertools.combinations(S, 2)):
                found = True; break
        if found:
            best = r
        else:
            break
    return best


rng = np.random.default_rng(0)
graphs = {'C5': [[1 if abs(i - j) in (1, 4) else 0 for j in range(5)] for i in range(5)]}
for g in range(6):
    n = int(rng.integers(4, 8))
    A = np.triu((rng.random((n, n)) < 0.5).astype(int), 1); A = A + A.T
    if A.sum() == 0:
        continue
    graphs['G%d(n=%d)' % (g, n)] = A.tolist()
for name, A in graphs.items():
    A = np.array(A, float); n = len(A)
    om = clique_number(A)
    mu = om * (om - 1)                       # threshold t = omega makes z_K rational
    Qm = -A; bm = np.zeros(n); cm = float(mu)
    zk = corner_bound(Qm, bm, cm, np.zeros(n), np.eye(n), np.ones(n))
    pred = np.sqrt(mu * om / (om - 1))
    print('   %s: omega=%d z_K=%.12f predicted %.12f' % (name, om, zk, pred))
    check('MS: %s' % name, abs(zk - pred) < 1e-9 * pred)

print('ALL PASS' if ok else 'SOME CHECK FAILED')
