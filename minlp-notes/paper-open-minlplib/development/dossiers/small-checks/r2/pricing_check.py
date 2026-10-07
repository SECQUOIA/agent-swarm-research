"""pricing050: own Lagrangian certificate (window + exclusion method) and check of the saved author point.

Upper bound for max -c.x:  UB(mu) = mu.r - sum_j min_[0,10] F_j,  F_j(x) = c_j x + sum_i mu_i a_ij x exp(g_ij x^p).
Per j: x_hat = 50-digit stationary point (or end point); window W = [x_hat - d, x_hat + d] where
  F'' > 0 on W (interval) => F >= F(x_hat) - F'(x_hat)^2 / (2 F''_lo) on W   (or F' sign => endpoint);
outside W an interval B&B (natural + mean-value forms) shows F >= F(x_hat)_hi.
"""
import time
from fractions import Fraction as Fr
import mpmath
from mpmath import iv, mp
import osil

t0 = time.time()
m = osil.read('pricing050.osil')
N = 50
c = [Fr(0)] * N
for j, v in m['obj']['lin'].items():
    c[j] = -Fr(v)
assert m['obj']['sense'] == 'max' and all(v >= 0 for v in c)
terms = {}
rhs = []
for i, row in enumerate(m['cons']):
    assert row['lb'] == '-INF' and not row['lin'] and row['nl'][0] == 'sum'
    rhs.append(row['ub'])
    for t in row['nl'][1:]:
        assert t[0] == 'product' and t[1][0] == 'exp' and t[2][0] == 'var'
        j, a = t[2][1], t[2][2]
        e = t[1][1]
        if e[0] == 'var':
            g, p = e[2], 1; assert e[1] == j
        else:
            assert e[0] == 'product' and e[2][0] == 'num'
            g = e[2][1]
            if e[1][0] == 'square': p = 2; assert e[1] == ('square', ('var', j, '1'))
            else: assert e[1] == ('power', ('var', j, '1'), ('num', '3')); p = 3
        assert Fr(a) < 0 and Fr(g) < 0 and (i, j) not in terms
        terms[(i, j)] = (a, g, p)
print('terms per p:', {p: sum(1 for v in terms.values() if v[2] == p) for p in (1, 2, 3)},
      'g values:', sorted({v[1] for v in terms.values()}))
MU = {3: '3.0489011208166370021', 4: '2.1677509642745686136'}   # e5, e6 (verifier/author)

def build(prec_dps):
    iv.dps = prec_dps
    muI = {i: iv.mpf(s) for i, s in MU.items()}
    tI = {k: (iv.mpf(a), iv.mpf(g), p) for k, (a, g, p) in terms.items()}
    cI = [iv.mpf(v.numerator) / v.denominator for v in c]
    return muI, tI, cI

def pw(X, p):
    r = X
    for _ in range(p - 1): r = r * X
    return r

def Fs(j, X, muI, tI, cI, order):
    """value, first and second derivative enclosures"""
    f, f1, f2 = cI[j] * X, cI[j], iv.mpf(0)
    for i, mu in muI.items():
        if (i, j) not in tI: continue
        a, g, p = tI[(i, j)]
        u = g * pw(X, p)
        E = iv.exp(u)
        f = f + mu * a * X * E
        if order >= 1: f1 = f1 + mu * a * E * (1 + p * u)
        if order >= 2:
            xpm1 = pw(X, p - 1) if p > 1 else iv.mpf(1)
            f2 = f2 + mu * a * E * g * p * xpm1 * (1 + p + p * u)
    return f, f1, f2

mp.dps = 50
muI, tI, cI = build(50)
# float-free stationary points at 50 digits
def fprime_mp(j, x):
    s = mpmath.mpf(c[j].numerator) / c[j].denominator
    for i, mu in MU.items():
        if (i, j) not in terms: continue
        a, g, p = terms[(i, j)]
        a, g, mu = mpmath.mpf(a), mpmath.mpf(g), mpmath.mpf(mu)
        u = g * x**p
        s += mu * a * mpmath.exp(u) * (1 + p * u)
    return s
def fval_mp(j, x):
    s = mpmath.mpf(c[j].numerator) / c[j].denominator * x
    for i, mu in MU.items():
        if (i, j) not in terms: continue
        a, g, p = terms[(i, j)]
        s += mpmath.mpf(mu) * mpmath.mpf(a) * x * mpmath.exp(mpmath.mpf(g) * x**p)
    return s

total = iv.mpf(0)
nbox_total = 0
xhat = []
for j in range(N):
    # coarse scan for the global minimizer candidate
    grid = [mpmath.mpf(k) / 100 for k in range(0, 1001)]
    vals = [fval_mp(j, x) for x in grid]
    k = min(range(len(grid)), key=lambda q: vals[q])
    if k in (0, 1000):
        xh = grid[k]
    else:
        xh = mpmath.findroot(lambda z: fprime_mp(j, z), grid[k])
    xhat.append(xh)
    XH = iv.mpf(xh)
    fh, f1h, _ = Fs(j, XH, muI, tI, cI, 1)
    # window
    d = mpmath.mpf('1e-3')
    lo_w, hi_w = max(xh - d, mpmath.mpf(0)), min(xh + d, mpmath.mpf(10))
    W = iv.mpf([lo_w, hi_w])
    _, f1W, f2W = Fs(j, W, muI, tI, cI, 2)
    if f2W.a > 0 and 0 < xh < 10:
        wbound = fh - f1h * f1h / (2 * iv.mpf(f2W.a))
    elif f1W.a > 0 and xh == 0:
        wbound = fh      # increasing on W, xh = left end
    elif f1W.b < 0 and xh == 10:
        wbound = fh      # decreasing on W, xh = right end
    else:
        raise RuntimeError('window test failed for j=%d' % j)
    target = mpmath.mpf(fh.b)
    # exclusion B&B on [0, lo_w] and [hi_w, 10]
    stack = []
    if lo_w > 0: stack.append((mpmath.mpf(0), lo_w))
    if hi_w < 10: stack.append((hi_w, mpmath.mpf(10)))
    nb = 0
    while stack:
        a_, b_ = stack.pop(); nb += 1
        X = iv.mpf([a_, b_])
        fX, f1X, _ = Fs(j, X, muI, tI, cI, 1)
        cm = (a_ + b_) / 2
        fc, _, _ = Fs(j, iv.mpf(cm), muI, tI, cI, 0)
        lb = max(mpmath.mpf(fX.a), mpmath.mpf((fc + f1X * (X - iv.mpf(cm))).a))
        if f1X.a > 0: lb = max(lb, mpmath.mpf(Fs(j, iv.mpf(a_), muI, tI, cI, 0)[0].a))
        if f1X.b < 0: lb = max(lb, mpmath.mpf(Fs(j, iv.mpf(b_), muI, tI, cI, 0)[0].a))
        if lb >= target: continue
        assert b_ - a_ > mpmath.mpf('1e-12'), (j, a_, b_)
        stack += [(a_, cm), (cm, b_)]
    nbox_total += nb
    Lj = iv.mpf([min(mpmath.mpf(wbound.a), mpmath.mpf(fh.a)), mpmath.mpf(fh.b)])
    total = total + iv.mpf(Lj.a)
iv.dps = 50
muR = sum(iv.mpf(MU[i]) * iv.mpf(rhs[i]) for i in MU)
UB = muR - total
print('own certificate: %d exclusion boxes, %.1f s' % (nbox_total, time.time() - t0))
print('sum_j min F_j >=', mpmath.nstr(mpmath.mpf(total.a), 30))
print('mu.r =', mpmath.nstr(mpmath.mpf(muR.a), 30), '(exact', Fr(MU[3]) * Fr(rhs[3]) + Fr(MU[4]) * Fr(rhs[4]), ')')
print('UB (max form) <=', mpmath.nstr(mpmath.mpf(UB.b), 30))
disp = '-1813.8290784519730577'
print('display', disp, 'valid (>= UB):', mpmath.mpf(disp) >= mpmath.mpf(UB.b), ' margin %s' % mpmath.nstr(mpmath.mpf(disp) - mpmath.mpf(UB.b), 4))
print('stationary/end points: interior', sum(1 for x in xhat if 0 < x < 10), 'at 0:', sum(1 for x in xhat if x == 0), 'at 10:', sum(1 for x in xhat if x == 10))

# saved author point
iv.dps = 50
pt = {}
for line in open('pricing050_primal.txt'):
    a_, b_ = line.split(); pt[a_] = b_
xs = [Fr(pt.get(nm, '0')) for nm in m['names']]
assert all(0 <= v <= 10 for v in xs)
XI = [iv.mpf(v.numerator) / v.denominator for v in xs]
F = {'exp': iv.exp, 'pow': lambda a, b, tr: pw(a, int(tr[1])) if tr == ('num', '3') else None}
def pwf(a, b, tr):
    assert tr == ('num', '3'); return a * a * a
F['pow'] = pwf
for i in range(5):
    r = osil.row(m, i, XI, iv.mpf, F)
    print('  row', m['cons'][i]['name'], 'value upper end - rhs = %s' % mpmath.nstr(mpmath.mpf(r.b) - mpmath.mpf(rhs[i]), 5))
    assert r.b < mpmath.mpf(rhs[i])
obj = -sum(c[j] * xs[j] for j in range(N))
print('saved author point: exactly feasible; objective (exact rational) =', mpmath.nstr(mpmath.mpf(obj.numerator) / obj.denominator, 25))
print('gap UB - objective(author point) <= %s' % mpmath.nstr(mpmath.mpf(UB.b) - mpmath.mpf(obj.numerator) / obj.denominator, 6))
print('primal display -1813.8290784519731 <= objective:', Fr('-1813.8290784519731') <= obj)
