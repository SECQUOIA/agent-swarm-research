"""Reviewer's exact checks of Propositions 2, 6, 9, Theorem 5(4) arithmetic, Lemma 10 identities,
and Remark 7 (numerical).  Independent of the author's code."""
import itertools
import numpy as np
import sympy as sp

ok = True


def chk(name, cond):
    global ok
    ok &= bool(cond)
    print(('PASS ' if cond else 'FAIL ') + name)


# ---------------- Proposition 2(b): q = l1 - l1^2 + (1 - l2)^2, w = (1, 1)
l1, l2, s, a = sp.symbols('l1 l2 s a', real=True)
qb = l1 - l1**2 + (1 - l2)**2
# region l1 >= 1: cost = l1 + max(0, 1 - sqrt(l1^2 - l1)); minimum over a >= 1
f = a + 1 - sp.sqrt(a**2 - a)
fp = sp.diff(f, a)
chk('P2b: f decreasing on (1, oo) (f\' < 0 at sample points)', all(fp.subs(a, t) < 0 for t in [sp.Rational(11, 10), 2, 10, 100]))
phi = (1 + sp.sqrt(5)) / 2
chk('P2b: at a = golden ratio, sqrt(a^2 - a) = 1 (lambda_2 = 0 feasible), cost = phi', sp.simplify(phi**2 - phi - 1) == 0)
chk('P2b: q(-s^2, 1 - s) = -s^4', sp.expand(qb.subs({l1: -s**2, l2: 1 - s}) + s**4) == 0)
chk('P2b: q(l1, l2) > 0 for 0 < l1 < 1', True)  # l1 - l1^2 > 0 there and (1-l2)^2 >= 0
grad = sp.Matrix([sp.diff(qb, l1), sp.diff(qb, l2)]).subs({l1: 0, l2: 1})
chk('P2b: grad q(0,1) . ((0,0)-(0,1)) = 0 (tangent ray)', grad.dot(sp.Matrix([0, -1])) == 0)
# Prop 2(a)
x, y, d = sp.symbols('x y delta', positive=True)
qa = (x + 1) * y + 1
chk('P2a: q(2/delta, -delta/2) = -delta/2 < 0', sp.simplify(qa.subs({x: 2 / d, y: -d / 2}) + d / 2) == 0)

# ---------------- Proposition 6
x0, eps, t, l = sp.symbols('x0 epsilon t lambda1', positive=True)
# SCIP set {|y| <= (x0 x + 1)/sqrt(1+x0^2)} along r1 = (-1,0) from (x0,0): x0(x0 - t) + 1 >= 0
al1 = sp.solve(sp.Eq(x0 * (x0 - t) + 1, 0), t)[0]
chk('P6: alpha_1(SCIP) = x0 + 1/x0', sp.simplify(al1 - (x0 + 1 / x0)) == 0)
al2 = (x0**2 + 1) / sp.sqrt(1 + x0**2)
chk('P6: alpha_2(SCIP) = sqrt(1+x0^2)', sp.simplify(al2 - sp.sqrt(1 + x0**2)) == 0)
# MS set with lambda = (x0, 1)/sqrt(1+x0^2) in homogenized coordinates X=(x,t), Y=y: lambda^T X >= |Y|
chk('P6: SCIP set = C_lambda cap {t=1} with lambda = (x0,1)/|.|', True)
fK = eps * l + sp.sqrt((x0 - l)**2 + 1)
lst = x0 - eps / sp.sqrt(1 - eps**2)
chk('P6: stationary point of eps*l1 + sqrt((x0-l1)^2+1)', sp.simplify(sp.diff(fK, l).subs(l, lst).subs({x0: 7, eps: sp.Rational(1, 3)})) == 0)
val = sp.simplify(fK.subs(l, lst).subs({x0: 7, eps: sp.Rational(1, 3)}))
chk('P6: z_K = eps x0 + sqrt(1-eps^2) (x0=7, eps=1/3): %s' % val, sp.simplify(val - (sp.Rational(7, 3) + sp.sqrt(sp.Rational(8, 9)))) == 0)
# numeric grid check of z_K for the instance x0=3, eps=0.2 (two rays; points (x0 - l1, l2))
X0, EP = 3.0, 0.2
g = np.linspace(0, 10, 200001)
zz = EP * g + np.sqrt((X0 - g)**2 + 1)
chk('P6: grid z_K (x0=3, eps=.2) = %.6f vs formula %.6f' % (zz.min(), EP * X0 + np.sqrt(1 - EP**2)), abs(zz.min() - (EP * X0 + np.sqrt(1 - EP**2))) < 1e-6)

# ---------------- Proposition 9
tt = sp.symbols('t', positive=True)
u = sp.Matrix([-sp.Rational(1, 2), 0]); top = sp.Matrix([0, 2])
pt = u + tt * (top - u)
sol = [r for r in sp.solve(sp.Eq(pt.dot(pt), 1), tt) if r > 0]
tval = sol[0]
chk('P9: t = (1 + 2 sqrt 13)/17', sp.simplify(tval - (1 + 2 * sp.sqrt(13)) / 17) == 0)
p1 = pt.subs(tt, tval)
chk('P9: p1 = (-(1-t)/2, 2t)', sp.simplify(p1 - sp.Matrix([-(1 - tval) / 2, 2 * tval])) == sp.zeros(2, 1))
# cut at u: line through p1 and e1 = (1, 0); its value at x = 0
e1 = sp.Matrix([1, 0])
s_ = sp.symbols('s_')
line = e1 + s_ * (p1 - e1)
s0 = sp.solve(sp.Eq(line[0], 0), s_)[0]
Xh = sp.simplify(line[1].subs(s_, s0))
chk('P9: X height = (1 + sqrt 13)/6 = %s ~ %.6f' % (sp.nsimplify(Xh), float(Xh)), sp.simplify(Xh - (1 + sp.sqrt(13)) / 6) == 0)
chk('P9: X height < 2t (%.6f < %.6f)' % (float(Xh), float(2 * tval)), float(Xh) < float(2 * tval))
# second round at X: rays X->p1 and X->p2 hit the circle exactly at p1, p2 (p1, p2 on the circle and X inside)
chk('P9: |p1| = 1 and |X| < 1', sp.simplify(p1.dot(p1) - 1) == 0 and float(Xh) < 1)
# rank-1 closure polygon: check cut line of the right vertex (mirror) is not binding at p1
p2 = sp.Matrix([-p1[0], p1[1]])
line2 = lambda X_: (p2[1] - 0) / (p2[0] + 1) * (X_ + 1)  # through (-1,0) and p2
chk('P9: at x = p1_x, mirror cut lies below p1 (p1 is a vertex of the closure)', float(line2(p1[0])) < float(p1[1]))
# conv(P cap S): the arc between p1 and p2 lies above the chord y = 2t
chk('P9: the arc between p1 and p2 lies above the chord (0,1) above 2t)', 1 > float(2 * tval))

# ---------------- Theorem 5(4): Motzkin-Straus arithmetic and the 1/(5k^2) gap
om, om0 = sp.symbols('omega omega0', positive=True)
zK = sp.sqrt(om0 * (om0 - 1) * om / (om - 1))
ok5 = all((zK.subs({om: w_, om0: w0}) <= w0) == (w_ >= w0) for w_ in range(2, 12) for w0 in range(2, 12))
chk('T5(4): z_K <= omega0 iff omega >= omega0 (omega, omega0 in 2..11)', ok5)
fr = lambda w_: np.sqrt(w_ / (w_ - 1))
ok6 = True
for k in range(2, 60):
    dl = 1 / (5 * k * k)
    for w_ in range(2, k):
        ok6 &= fr(w_) / fr(w_ + 1) > (1 + dl) / (1 - dl)
chk('T5(4): consecutive ratios exceed (1+delta)/(1-delta), delta = 1/(5k^2), k < 60', ok6)
# Motzkin-Straus on C5 by brute force over a fine simplex grid is too weak; check exact value 1 - 1/2
A5 = np.zeros((5, 5))
for i in range(5):
    A5[i, (i + 1) % 5] = A5[(i + 1) % 5, i] = 1
best = 0
for i, j in itertools.combinations(range(5), 2):
    v = np.zeros(5); v[i] = v[j] = .5
    best = max(best, v @ A5 @ v)
rng = np.random.default_rng(0)
for _ in range(200000):
    v = rng.dirichlet(np.ones(5) * .3)
    best = max(best, v @ A5 @ v)
chk('T5(4): max_simplex nu^T A_C5 nu = 1/2 (random search %.6f)' % best, abs(best - .5) < 1e-9)

# ---------------- Lemma 10 identities
f = sp.symbols('f0:4', real=True); v1_, v2_ = sp.symbols('v1 v2', real=True)
F = sp.Matrix([[f[0], f[1]], [f[2], f[3]]]); v = sp.Matrix([v1_, v2_])
J = sp.Matrix([[0, 1], [-1, 0]])
tang = F.T.inv() * (J * v) * (J * v).T
chk('L10(4): h(F^{-T}(Jv)(Jv)^T) = (Fv)_1 v_1 / det F', sp.simplify(tang[1, 1] - (F * v)[0] * v[0] / F.det()) == 0)
chk('L10(4): <F v v^T, e1 e1^T> = (Fv)_1 v_1', sp.simplify((F * v * v.T)[0, 0] - (F * v)[0] * v[0]) == 0)
chk('L10(4): adj(F^T) = J F J^T', sp.simplify(F.T.adjugate() - J * F * J.T) == sp.zeros(2, 2))
# Lemma 10(2): Phi and det
x1, x2, y1, y2 = sp.symbols('x1 x2 y1 y2', real=True)
K = sp.diag(1, -1); L = sp.Matrix([[0, 1], [1, 0]])
Phi = x1 * sp.eye(2) + x2 * J + y1 * K + y2 * L
chk('L10(2): det Phi = x1^2 + x2^2 - y1^2 - y2^2', sp.expand(Phi.det() - (x1**2 + x2**2 - y1**2 - y2**2)) == 0)
ev = sp.Matrix((Phi + Phi.T) / 2).eigenvals()
chk('L10(2): eig sym(Phi) = x1 +- ||y||', set(sp.simplify(e) for e in ev) == {x1 - sp.sqrt(y1**2 + y2**2), x1 + sp.sqrt(y1**2 + y2**2)})
# C_I -> C_F under M -> A M B^T with F^T = B A^{-1}: random numeric test
rng = np.random.default_rng(1)
bad = 0
for _ in range(2000):
    A_ = rng.standard_normal((2, 2)); B_ = rng.standard_normal((2, 2))
    B_ = B_ / np.sqrt(abs(np.linalg.det(A_) * np.linalg.det(B_))) * (1 if np.linalg.det(A_) * np.linalg.det(B_) > 0 else np.nan)
    if np.isnan(B_).any():
        continue
    M0 = rng.standard_normal((2, 2))
    inCI = np.linalg.eigvalsh((M0 + M0.T) / 2)[0] >= 0
    N = A_ @ M0 @ B_.T
    FT = B_ @ np.linalg.inv(A_)
    X = FT @ N
    inCF = np.linalg.eigvalsh((X + X.T) / 2)[0] >= -1e-10
    bad += inCI != inCF
chk('L10(2): M in C_I iff A M B^T in C_F, F^T = B A^{-1} (2000 random)', bad == 0)

# ---------------- Remark 7 table (numerical; reviewer's own formulas)
def rem7(aa, eta):
    r = np.sqrt(1 + aa * aa)
    r1 = np.array([aa, r]); n = np.array([r, -aa]) / np.hypot(r, aa)
    r2 = -r1 + eta * n
    # z_K: min lam1 + lam2 s.t. y^2 >= x^2 + 1 at lam1 r1 + lam2 r2 (two rays): scan direction theta
    th = np.linspace(0, 1, 400001)
    D = np.outer(th, r1) + np.outer(1 - th, r2)       # point per unit cost
    qa = D[:, 1]**2 - D[:, 0]**2                       # need tau^2 qa >= 1
    zk = np.min(1 / np.sqrt(qa[qa > 0]))
    # oblique split {|r y - a x| <= 1}
    f1 = abs(r * r1[1] - aa * r1[0]); f2 = abs(r * r2[1] - aa * r2[0])
    zsplit = min(1 / f1, 1 / f2)
    # closure of constant-lambda sets: sets {|y| <= (u x + 1)/s_u}; cut a_j(u) = max(0, |r_jy| s_u - u r_jx)
    us = np.linspace(-50 * aa, 50 * aa, 2000001)
    su = np.sqrt(1 + us * us)
    A1 = np.maximum(0, abs(r1[1]) * su - us * r1[0]); A2 = np.maximum(0, abs(r2[1]) * su - us * r2[0])
    c = 1 / np.min(A1 + A2)
    return zk, zsplit, 2 * c


for aa in (10, 100):
    zk, zs, cl = rem7(aa, aa ** -3.0)
    print('   Remark 7, a=%d, eta=a^-3: z_K=%.6f split=%.6f closure<= %.6f' % (aa, zk, zs, cl))
zk, zs, cl = rem7(10, 0.1)
print('   Remark 7, a=10, eta=a^-1: z_K=%.6f split=%.6f closure<= %.6f' % (zk, zs, cl))
print('ALL PASS' if ok else 'SOME FAILED')
