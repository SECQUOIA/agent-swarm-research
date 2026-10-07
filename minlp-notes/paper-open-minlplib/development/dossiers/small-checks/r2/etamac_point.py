"""etamac: exact facts on exponents, the majorant constant, and an exactly feasible point defined
from the AUTHOR'S SAVED decimals (logs/etamac_primal.txt) by the exact recursion of all rows."""
from fractions import Fraction as Fr
import mpmath
from mpmath import iv, mp
import osil

m = osil.read('etamac.osil'); N = m['n']
p1, p2, p3, q = Fr('.342222222222222'), Fr('.427777777777778'), Fr('.794444444444445'), Fr('.818181818181818')
s = (p2 + p3) * q
print('p1*q =', float(p1 * q), ' s-1 =', float(s - 1), ' exact s-1 =', s - 1)
print('decimals vs 11/9-scaled rationals: p1-0.28*11/9 = %.3g, p2-0.35*11/9 = %.3g, p3-0.65*11/9 = %.3g, q-9/11 = %.3g'
      % (float(p1 - Fr(28, 100) * Fr(11, 9)), float(p2 - Fr(35, 100) * Fr(11, 9)), float(p3 - Fr(65, 100) * Fr(11, 9)), float(q - Fr(9, 11))))
iv.dps = 40
mp.dps = 60
for W in ('1015.6000321087411', '2022.06', '2062.83'):
    k = iv.exp(iv.mpf(str((s - 1).numerator)) / iv.mpf(str((s - 1).denominator)) * iv.log(iv.mpf(W)))
    print('W = %s: W^(s-1) - 1 <= %s' % (W, mpmath.nstr(mpmath.mpf(k.b) - 1, 6)))
# roles (1-based variable names)
K = lambda t: t - 1; KN = lambda t: 8 + t - 1; Y = lambda t: 17 + t - 1; YN = lambda t: 25 + t - 1
L = lambda t: 34 + t - 1; LN = lambda t: 43 + t - 1; E = lambda t: 52 + t - 1; EN = lambda t: 61 + t - 1
C = lambda t: 70 + t - 1; I = lambda t: 79 + t - 1; EC = lambda t: 88 + t - 1
pt = {}
for line in open('etamac_primal.txt'):
    a, b = line.split(); pt[a] = b
dec = lambda j: iv.mpf(pt[m['names'][j]])
F = {'ln': iv.log, 'exp': iv.exp, 'pow': lambda a, b, tr: iv.exp(b * iv.log(a))}
num = iv.mpf
rows = {c['name']: c for c in m['cons']}
x = [None] * N
x[K(1)] = iv.mpf('12.32657617084')
for t in range(1, 10):
    x[LN(t)], x[EN(t)] = dec(LN(t)), dec(EN(t))
for t in range(1, 9):
    x[I(t)] = dec(I(t))
g = iv.mpf('4.91287681'); dl = iv.mpf('.8153726976')
x[L(1)] = x[LN(1)] + iv.mpf('2.038431744'); x[E(1)] = x[EN(1)] + iv.mpf('40.76863488')
# Y_1 from e43: Y_1 = 3.4653339648 - nl(e43)
x[Y(1)] = iv.mpf('3.4653339648') - osil.ev(rows['e43']['nl'], x, num, F)
for t in range(2, 10):
    x[KN(t)] = g * x[I(t - 1)]
    x[K(t)] = dl * x[K(t - 1)] + x[KN(t)]
    x[L(t)] = dl * x[L(t - 1)] + x[LN(t)]
    x[E(t)] = dl * x[E(t - 1)] + x[EN(t)]
    x[YN(t)] = -osil.ev(rows['e%d' % (t + 7)]['nl'], x, num, F)   # e9..e16: YN_t + nl = 0
    x[Y(t)] = dl * x[Y(t - 1)] + x[YN(t)]
x[I(9)] = iv.mpf('7e-2') * x[K(9)]
for t in range(1, 10):
    c = rows['e%d' % (51 + t)]['lin']
    x[EC(t)] = -(num(c[L(t)]) * x[L(t)] + num(c[E(t)]) * x[E(t)]) / iv.mpf('1e3')
    x[C(t)] = x[Y(t)] - x[I(t)] - x[EC(t)]
assert all(v is not None for v in x)
# rows: every enclosure must contain 0 (they hold exactly by construction); report widths
worst = 0
for i, c in enumerate(m['cons']):
    r = osil.row(m, i, x, num, F)
    if c['lb'] != '-INF': assert (r - iv.mpf(c['lb'])).b >= 0, c['name']
    if c['ub'] != 'INF': assert (r - iv.mpf(c['ub'])).a <= 0, c['name']
    w = mpmath.mpf(r.b) - mpmath.mpf(r.a); worst = max(worst, w)
margin = min(mpmath.mpf((x[j] - iv.mpf(m['lb'][j])).a) for j in range(N) if m['lb'][j] != '-INF' and j != K(1))
print('rows consistent with exact satisfaction (max enclosure width %s); min bound margin %s' % (mpmath.nstr(worst, 3), mpmath.nstr(margin, 4)))
f = osil.objective(m, x, num, F)
print('objective of the exactly feasible point (author decisions):', mpmath.nstr(f.a, 25), mpmath.nstr(f.b, 25))
dual = Fr('-15.2946756433680921685')     # verifier lower end, truncated downward
print('gap to verifier dual -15.2946756433680921685: <= %s' % mpmath.nstr(mpmath.mpf(f.b) - mpmath.mpf(dual.numerator) / dual.denominator, 6))
print('primal objective of reviewer point (log): [-15.29467564336808959198292336..]; display -15.29467564336808959 safe:',
      Fr('-15.29467564336808959') >= Fr('-15.2946756433680895919829233612845357438291772'))
print('dual display -15.294675643368093 <= -15.2946756433680921685:', Fr('-15.294675643368093') <= dual)
