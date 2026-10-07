"""Review r2: my own exact/symbolic checks of the revised proofs and numbers (no stream code).

  A. Lemma 8 (general): S J^T S = -det(S) J, -v^T S N v = det(S) m^T J N J S m, v^T S v = det(S) m^T S m,
     v^T S m = 0, for symbolic symmetric S, arbitrary m, N. Theorem 14 forms from the corner data.
  B. Lemma 7 interior step: kernel of d -> sym(F^T M0(d)) is nonzero iff (F^{-T} J)_22 = 0, and then
     the affine image misses 0; random rank-deficient examples meet the PD cone when they meet PSD.
  C. Theorem 11(c) case (v): the identities and the bound (sqrt(65/14) - 1)/4 > 0.2886.
  D. W-corner, S = I: exact cut ((sqrt2 - 1)/4, (sqrt2 - 1)/4, 0, (sqrt2 + 1)/4) of B_F, via the
     boundary of C_F along each ray and a kept kernel vector (Lemma 6(a)).
  E. Theorem 11(b) integer certificate under Lemma 16 with I_0 = {4}.
  F. Rounded endpoints: 0.97538, 0.9953611, 0.2539, 0.25905, 0.2591, 0.2324859, 1.1166, 411.
"""
import random
from fractions import Fraction as Fr

import sympy as sp

ok = True


def check(msg, cond):
    global ok
    ok &= bool(cond)
    print(('PASS ' if cond else 'FAIL ') + msg, flush=True)


# ---------------- A. Lemma 8
a, b, c = sp.symbols('a b c', real=True)
m1, m2 = sp.symbols('m1 m2', real=True)
n = sp.symbols('n0:4', real=True)
S = sp.Matrix([[a, b], [b, c]])
J = sp.Matrix([[0, 1], [-1, 0]])
m = sp.Matrix([m1, m2])
N = sp.Matrix([[n[0], n[1]], [n[2], n[3]]])
v = J * S * m
check('A1 S J^T S = -det(S) J', sp.simplify(S * J.T * S + S.det() * J) == sp.zeros(2, 2))
L = sp.expand((m.T * J * N * J * S * m)[0])
check('A2 L = m^T J N J S m is linear in (a, b, c)', all(sp.Poly(L, a, b, c).degree(x) <= 1 for x in (a, b, c))
      and sp.Poly(L, a, b, c).total_degree() <= 1)
check('A3 -v^T S N v = det(S) L', sp.expand(-(v.T * S * N * v)[0] - S.det() * L) == 0)
check('A4 v^T S v = det(S) m^T S m', sp.expand((v.T * S * v)[0] - S.det() * (m.T * S * m)[0]) == 0)
check('A5 v^T S m = 0 (v kept: v^T Z v = (v^T S m) v_1 = 0)', sp.expand((v.T * S * m)[0]) == 0)
# Theorem 14 corner from its geometric data
sb = [sp.Rational(-9, 2), 0, sp.Rational(3, 2)]
verts = [[-1, -6, 18], [-5, 6, -18], [0, sp.Rational(5, 2), sp.Rational(5, 2)]]
Ms = sp.Matrix([[sb[2], sb[0]], [sb[1], 1]])
mt = Ms.inv() * sp.Matrix([1, 0])
forms = []
for vv in verts:
    p = [vv[i] - sb[i] for i in range(3)]
    Nj = Ms.inv() * sp.Matrix([[p[2], p[0]], [p[1], 0]])
    forms.append(sp.expand((mt.T * J * Nj * J * S * mt)[0]))
check('A6 Theorem 14 forms L = %s, m^T S m = %s' % (forms, sp.expand((mt.T * S * mt)[0])),
      forms == [-8 * b / 3, 8 * b / 3, 10 * b / 9] and sp.expand((mt.T * S * mt)[0]) == 4 * a / 9)

# ---------------- B. Lemma 7 interior step
f = sp.symbols('f0:4', real=True)
FT = sp.Matrix([[f[0], f[1]], [f[2], f[3]]])
w, x, y = sp.symbols('w x y', real=True)
Mws = sp.Matrix([[w, x], [y, 1]])
A = FT * Mws
A = (A + A.T) / 2
lin = sp.Matrix([A[0, 0], A[0, 1], A[1, 1]]).jacobian([w, x, y])
FinvTJ = (FT.inv() * J).applyfunc(sp.simplify)          # F^{-T} J, with F^T = FT
check('B1 det of linear part = -f2 det(F^T)/2 (singular iff (F^T)_21 = 0)',
      sp.simplify(lin.det() + f[2] * FT.det() / 2) == 0)
check('B2 (F^{-T} J)_22 = -(F^T)_21/det(F^T): zero iff the linear part is singular',
      sp.simplify(FinvTJ[1, 1] + f[2] / FT.det()) == 0)
check('B3 when (F^T)_21 = 0, the (2,2) entry of the image is the constant (F^T)_22 != 0 (image misses 0)',
      sp.simplify(A[1, 1].subs(f[2], 0)) == f[3])
# random rank-deficient F^T: the plane meets PD whenever it meets PSD (sampled, exact rationals)
random.seed(1)
cnt = good = 0
for _ in range(300):
    F0 = [Fr(random.randint(-5, 5), random.randint(1, 4)) for _ in range(4)]
    F0[2] = Fr(0)
    if F0[0] * F0[3] <= 0:
        continue
    # image: [[f0 w + f1 y, (f0 x + f1 + f3 y)/2], [., f3]] ; f3 > 0 needed for PSD
    if F0[3] <= 0:
        continue
    cnt += 1
    # pick s with A11 = 1, A12 = 0: then A = diag(1, f3) is PD
    ys = Fr(0)
    ws = (1 - F0[1] * ys) / F0[0]
    xs = (-F0[1] - F0[3] * ys) / F0[0]
    A11 = F0[0] * ws + F0[1] * ys
    A12 = (F0[0] * xs + F0[1] + F0[3] * ys) / 2
    good += A11 > 0 and A11 * F0[3] - A12 ** 2 > 0
check('B4 %d random rank-deficient F with det F > 0, (F^T)_22 > 0: image meets PD in all %d' % (cnt, good), good == cnt and cnt > 0)

# ---------------- C. Theorem 11(c), case (v)
be, cc, t = sp.symbols('beta c t', positive=True)
a1, b1 = 1, -be
f2 = ((cc - b1) * t - (a1 - b1)) / (2 * (a1 + 2 * b1 * t + cc * t ** 2))
tK = -(a1 + b1) / (b1 + cc)
h = cc ** 2 - (be + 3) * cc + 2 * be ** 2 + be
lit = sp.simplify(sp.diff(f2, t).subs(t, tK) * (be - cc) ** 2 - (cc - be ** 2) * h)
check('C1a the note\'s identity "f_2\'(t_K)(beta - c)^2 = (c - beta^2) h" read literally does NOT hold '
      '(difference nonzero): %s' % (lit != 0), lit != 0)
Nn = (cc - b1) * t - (a1 - b1)
Dd = a1 + 2 * b1 * t + cc * t ** 2
dnum = sp.diff(Nn, t) * Dd - Nn * sp.diff(Dd, t)        # numerator of f_2' (f_2' = dnum / (2 Dd^2))
check('C1b it holds for the numerator of f_2\': (N\'D - ND\')(t_K) (beta - c)^2 = (c - beta^2) h',
      sp.simplify(dnum.subs(t, tK) * (be - cc) ** 2 - (cc - be ** 2) * h) == 0)
check('C1c exact form: f_2\'(t_K) = (c - beta)^2 h / (2 (c - beta^2)(1 - 2 beta + c)^2), so sign f_2\'(t_K) = sign h',
      sp.simplify(sp.diff(f2, t).subs(t, tK) - (cc - be) ** 2 * h / (2 * (cc - be ** 2) * (1 - 2 * be + cc) ** 2)) == 0)
c0 = 2 * be ** 2 / (1 + be)
check('C2 h(beta, 2 beta^2/(1+beta)) = beta(beta-1)(4beta^2+beta-1)/(1+beta)^2',
      sp.simplify(h.subs(cc, c0) - be * (be - 1) * (4 * be ** 2 + be - 1) / (1 + be) ** 2) == 0)
check('C3 positive root of 4beta^2 + beta - 1 is (sqrt17 - 1)/8 < 2/5',
      sp.simplify(4 * ((sp.sqrt(17) - 1) / 8) ** 2 + (sp.sqrt(17) - 1) / 8 - 1) == 0 and (sp.sqrt(17) - 1) / 8 < sp.Rational(2, 5))
c1 = be * (3 * be + 1) / (be + 3)
check('C4 h(beta, c_1) = c_1^2 - beta^2', sp.simplify(h.subs(cc, c1) - (c1 ** 2 - be ** 2)) == 0)
ratio = (1 - 2 * be + cc) / (cc - be ** 2)
check('C5 d/dc of (1 - 2beta + c)/(c - beta^2) = -(1 - beta)^2/(c - beta^2)^2 (decreasing in c)',
      sp.simplify(sp.diff(ratio, cc) + (1 - be) ** 2 / (cc - be ** 2) ** 2) == 0)
check('C6 value at c_1 is (3 - beta)/(beta(1 + beta))', sp.simplify(ratio.subs(cc, c1) - (3 - be) / (be * (1 + be))) == 0)
g = (3 - be) / (be * (1 + be))
check('C7 (3 - beta)/(beta(1 + beta)) is decreasing on (0, 1) and equals 65/14 at 2/5',
      sp.simplify(g.subs(be, sp.Rational(2, 5))) == sp.Rational(65, 14)
      and all(sp.diff(g, be).subs(be, sp.Rational(k, 100)) < 0 for k in range(1, 100)))
num = (sp.sqrt(sp.Rational(65, 14)) - 1) / 4
check('C8 (sqrt(65/14) - 1)/4 = %.8f > 0.2886 exactly (65/14 > (1 + 4*0.2886)^2), and < 0.2887'
      % float(num), Fr(65, 14) > (1 + 4 * Fr('0.2886')) ** 2 and Fr(65, 14) < (1 + 4 * Fr('0.2887')) ** 2)
check('C9 0.2886 > (sqrt2 - 1)/2', sp.Rational(2886, 10000) > (sp.sqrt(2) - 1) / 2)

# ---------------- D. W-corner exact cut at S = I
sbw = [1, -1, 1]
Mw = sp.Matrix([[sbw[2], sbw[0]], [sbw[1], 1]])
mw = Mw.inv() * sp.Matrix([1, 0])
check('D0 m = (1/2, 1/2)', list(mw) == [sp.Rational(1, 2)] * 2)
rays = {1: (1, 0, 0), 2: (0, -1, 0), 3: (0, 0, 1), 4: (0, 0, -1)}       # (x, y, w)
X = sp.eye(2)
Z = (X * mw * sp.Matrix([[1, 0]]))
Z = (Z + Z.T) / 2
mu = sp.symbols('mu', positive=True)
alphas = {}
for j, p in rays.items():
    if j == 3:
        alphas[j] = sp.oo        # e_w is a recession direction of every B_F (Lemma 6(c))
        continue
    Nj = Mw.inv() * sp.Matrix([[p[2], p[0]], [p[1], 0]])
    Aj = X + mu * (X * Nj + (X * Nj).T) / 2
    dets = sp.solve(sp.Eq(Aj.det(), 0), mu)
    pos = sorted([r for r in dets if r.is_positive])
    if not pos:
        alphas[j] = sp.oo
        continue
    al = sp.nsimplify(sp.simplify(pos[0]))
    K = Aj.subs(mu, al)
    kv = K.nullspace()[0]
    kept = sp.simplify((kv.T * Z * kv)[0])
    # A(sbar + al p) PSD (both diagonal entries >= 0) so the segment is in C_F
    psd = all(sp.simplify(K[i, i]) >= 0 for i in range(2))
    check('D%d ray %d: boundary of C_F at mu = %s; kernel vector kept (v^T Z v = %s >= 0); PSD there'
          % (j, j, al, kept, ), kept >= 0 and psd)
    alphas[j] = al
acut = [sp.simplify(1 / alphas[j]) if alphas[j] != sp.oo else 0 for j in (1, 2, 3, 4)]
target = [(sp.sqrt(2) - 1) / 4, (sp.sqrt(2) - 1) / 4, 0, (sp.sqrt(2) + 1) / 4]
check('D5 cut vector of B_F at S = I is %s' % acut, all(sp.simplify(u - v_) == 0 for u, v_ in zip(acut, target)))
check('D6 a_1 + a_2 = (sqrt2 - 1)/2 and 1/(a_1 + a_2) = 2(sqrt2 + 1), the (t, t, 0, 0) threshold',
      sp.simplify(acut[0] + acut[1] - (sp.sqrt(2) - 1) / 2) == 0
      and sp.simplify(1 / (acut[0] + acut[1]) - 2 * (sp.sqrt(2) + 1)) == 0)

# ---------------- E. Theorem 11(b) integer certificate (Lemma 16 with I_0 = {4})
Ys = [sp.Matrix([[141, -63], [-63, 29]]), sp.Matrix([[4, 67], [67, 1322]]), sp.Matrix([[31, -132], [-132, 565]]), sp.zeros(2, 2)]
R = sp.zeros(2, 2)
for j, p in rays.items():
    R -= Mw.inv() * sp.Matrix([[p[2], p[0]], [p[1], 0]]) * Ys[j - 1]
check('E1 R = %s, symmetric, = [[14, 18], [18, 85]]' % R.tolist(), R == sp.Matrix([[14, 18], [18, 85]]))
check('E2 Y_1..Y_3 PSD with determinants 120, 799, 91', [Y.det() for Y in Ys[:3]] == [120, 799, 91] and all(Y[0, 0] > 0 for Y in Ys[:3]))
vertsQ = [R] + [R - Ys[j] / 20 for j in range(3)]
check('E3 Q PSD with positive trace at the 4 vertices of {a >= 0, a_4 = 0, 20(a1+a2+a3) <= 1}',
      all(Q[0, 0] >= 0 and Q[1, 1] >= 0 and Q.det() >= 0 and Q.trace() > 0 for Q in vertsQ))

# ---------------- F. rounded endpoints
prop10 = Fr(396503562307491652037015395705021177207626376155404352, 398351441316353660966368086274075897893464946699521021)
checks = [
    ('0.97538 <= 0.9753853514 (sfree certified A value)', Fr('0.97538') <= Fr('0.9753853514')),
    ('0.9953611 <= Prop 10 LP value < 0.9953612', Fr('0.9953611') <= prop10 < Fr('0.9953612')),
    ('0.99536 <= Prop 10 LP value (Summary item 4)', Fr('0.99536') <= prop10),
    ('136/525 <= 0.25905 <= 0.2591 (upper bounds rounded up)', Fr(136, 525) <= Fr('0.25905') <= Fr('0.2591')),
    ('w^T lam_hat = 464971761/2000000000 <= 0.2324859', Fr(11, 20) * Fr(2211, 10000) + Fr(1, 10**6) * Fr(8805, 10000) + Fr(9, 20) * Fr(2464, 10000) <= Fr('0.2324859')),
    ('0.2596 / 0.2324859 >= 1.1166', Fr('0.2596') / Fr('0.2324859') >= Fr('1.1166')),
    ('3 * 137 = 411', 3 * 137 == 411),
]
for msg, cond in checks:
    check('F ' + msg, cond)
print('ALL PASS' if ok else 'SOME CHECK FAILED')
raise SystemExit(0 if ok else 1)
