"""hvycrash: structure, identity (sympy, exact rationals) and an analytic feasible point."""
import sympy as sp
from fractions import Fraction as Fr
from mpmath import iv, mp
import osil

m = osil.read('hvycrash.osil')
n = m['n']; C = m['cons']
assert n == 201 and len(C) == 150
print('objective:', m['obj'])
X = sp.symbols('x0:%d' % n, real=True)

def sym(tr):
    op = tr[0]
    if op == 'num': return sp.Rational(tr[1])
    if op == 'var': return sp.Rational(tr[2]) * X[tr[1]]
    a = [sym(c) for c in tr[1:]]
    if op in ('sum', 'plus'): return sp.Add(*a)
    if op in ('product', 'times'): return sp.Mul(*a)
    if op == 'negate': return -a[0]
    if op == 'divide': return a[0] / a[1]
    if op == 'minus': return a[0] - a[1]
    if op == 'cos': return sp.cos(a[0])
    raise NotImplementedError(op)

def rowsym(c):
    e = sum((sp.Rational(v) * X[j] for j, v in c['lin'].items()), sp.Integer(0))
    if c['nl'] is not None: e += sym(c['nl'])
    return e - sp.Rational(c['lb']), c['lb'] == c['ub']

h = sp.Rational('4.37e-3')
# bounds
for j in range(n):
    nm = m['names'][j]
    k = j + 1
    if k <= 50 or k == 101: assert (m['lb'][j], m['ub'][j]) == ('0', '6.2831854'), nm
    elif k <= 100: assert (m['lb'][j], m['ub'][j]) == ('8e-2', '.417'), nm
    else: assert (m['lb'][j], m['ub'][j]) == ('-INF', 'INF'), (nm, m['lb'][j], m['ub'][j])
th = lambda k: X[100] if k == 0 else X[k - 1]      # theta_0 = x101, theta_k = x_k
cc = lambda k: X[49 + k]                           # c_k = x_{50+k}
rr = lambda k: X[100 + k]                          # r_k = x_{101+k}
ss = lambda k: 0 if k == 0 else X[201 - k]         # s_k = x_{202-k}
assert m['obj']['lin'] == {151: '1'} and m['obj']['nl'] is None and m['obj']['sense'] == 'min'
D = lambda k: sp.Rational('.486237') * cc(k)**2 + sp.Rational('1.62079e-2')
A = lambda k: cc(k) / (sp.Rational('.3') * cc(k)**2 + sp.Rational('1e-2'))
nchecked = 0
for k in range(1, 51):
    acc, eq1 = rowsym(C[3 * k - 3]); alg, eq2 = rowsym(C[3 * k - 2]); dyn, eq3 = rowsym(C[3 * k - 1])
    assert eq1 and eq2 and eq3
    alg_t = -1 / rr(k) - sp.cos(th(k)) / (D(k) * rr(k)**3)
    assert sp.simplify(alg - alg_t) == 0
    # acc: s_{k-1} - s_k + h cos/(D r^2)  (sign of the linear part checked)
    acc_t = ss(k - 1) - ss(k) + h * sp.cos(th(k)) / (D(k) * rr(k)**2)
    if sp.simplify(acc - acc_t) != 0:
        assert sp.simplify(acc + acc_t) == 0
    dyn_t = sp.Rational(1, 10) * th(k - 1) - sp.Rational(1, 10) * th(k) + h * A(k) / rr(k)**2 \
        - h * sp.cos(th(k)) / (D(k) * rr(k)**4)
    if sp.simplify(dyn - dyn_t) != 0:
        assert sp.simplify(dyn + dyn_t) == 0
    # identities: acc_t = s_{k-1} - s_k - h - h r alg_t ; dyn_t = 0.1(th_{k-1}-th_k) + h(A+1)/r^2 + h alg_t / r
    assert sp.simplify(acc_t - (ss(k - 1) - ss(k) - h - h * rr(k) * alg_t)) == 0
    assert sp.simplify(dyn_t - (sp.Rational(1, 10) * (th(k - 1) - th(k)) + h * (A(k) + 1) / rr(k)**2 + h * alg_t / rr(k))) == 0
    nchecked += 1
print('rows matched and identities verified symbolically for', nchecked, 'stages')
# hence on the feasible set s_k = s_{k-1} - h, objective x152 = s_50 = -50 h:
print('objective constant =', -50 * h, '=', float(-50 * h))

# analytic feasible point: c_k = 0.08, theta_50 = 3, theta_{k-1} = theta_k - kappa/(-cos theta_k)
c0 = Fr('0.08'); hq = Fr('4.37e-3')
Dq = Fr('.486237') * c0**2 + Fr('1.62079e-2'); Aq = c0 / (Fr('.3') * c0**2 + Fr('1e-2'))
kap = 10 * hq * (Aq + 1) * Dq
print('A(0.08) =', Aq, ' D(0.08) =', Dq, ' kappa =', kap, '=', float(kap))
# cos 2.6 <= -0.85: for x = 2.6 the terms x^(2j)/(2j)! decrease from j = 1 on, so a partial
# sum of the alternating series that ends with a POSITIVE term (j even) is an upper bound.
x = Fr(26, 10); s = Fr(0); ub_cos = None
for j in range(0, 40):
    s += (-1)**j * x**(2 * j) / Fr(int(sp.factorial(2 * j)))
    if j % 2 == 0 and j >= 6:
        ub_cos = s; break
lb_cos = ub_cos - x**(2 * j + 2) / Fr(int(sp.factorial(2 * j + 2)))
print('cos(2.6) in [%.12f, %.12f] (Taylor partial sums through x^%d and x^%d)' % (float(lb_cos), float(ub_cos), 2 * j + 2, 2 * j))
assert ub_cos < Fr(-85, 100)
assert 50 * kap / Fr(85, 100) < Fr(4, 10)
assert Fr(3) < Fr(223, 71)  # 223/71 < pi (Archimedes)
print('50*kappa/0.85 =', float(50 * kap / Fr(85, 100)), '< 0.4 => all theta_k in [2.6, 3] subset (pi/2, pi)')

# interval verification of the constructed point on the OSIL rows (independent evaluator)
iv.dps = 60
def F_cos(a): return iv.cos(a)
F = {'cos': F_cos, 'ln': iv.log, 'exp': iv.exp, 'sqrt': iv.sqrt}
num = lambda s_: iv.mpf(s_)
xv = [None] * n
theta = {50: iv.mpf(3)}
for k in range(50, 0, -1):
    theta[k - 1] = theta[k] - iv.mpf(kap.numerator) / kap.denominator / (-iv.cos(theta[k]))
Div = iv.mpf('.486237') * iv.mpf('0.08')**2 + iv.mpf('1.62079e-2')
for k in range(1, 51):
    xv[k - 1] = theta[k]; xv[49 + k] = iv.mpf('0.08')
    xv[100 + k] = iv.sqrt(-iv.cos(theta[k]) / Div)
    xv[201 - k] = -k * iv.mpf('4.37e-3')
xv[100] = theta[0]
viol = max(max(abs(osil.row(m, i, xv, num, F).a), abs(osil.row(m, i, xv, num, F).b)) for i in range(150))
print('max |row| on enclosure: %.3g' % float(viol))
lo_th = min(float(theta[k].a) for k in range(51)); hi_th = max(float(theta[k].b) for k in range(51))
print('theta range [%.6f, %.6f]; theta_0 = %s' % (lo_th, hi_th, mp.nstr(theta[0].mid, 20)))
print('max cos(theta_k) = %.6f' % max(float(iv.cos(theta[k]).b) for k in range(51)))
obj = osil.objective(m, xv, num, F)
print('objective enclosure:', obj)
