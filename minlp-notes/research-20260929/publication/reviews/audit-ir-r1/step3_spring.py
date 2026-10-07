"""spring: (1) build an exactly feasible rational point near p2/p3 and check it
with rv_osil.check; (2) prove the global optimum by enumerating all
(i4, wire diameter) combinations, with exact rational comparisons.

Model (read from the OSIL with rv_osil and asserted below):
  min (a + b*N) * x1 * x2^2,  a = 1.570796327, b = .7853981635
  e2: x5 = x1/x2           e3: x6 = (4x5-1)/(4x5-4) + .615/x5
  e4: K4 * x6 * x5 / x2^2 <= 189000, K4 = 2546.47908913782
  e5: x3 = k * x5^3 * N / x2, k = 6.95652173913044e-7
  e6: 2.1 x2 + 1000 x3 + 1.05 x2 N <= 14      e7: x1 + x2 <= 3
  e8: x2 = sum c_j b_j     e9: sum b_j = 1
  x1 >= .414, x2 >= .207, x3 in [L3, .02], L3 = 1.78571428571429e-3,
  N = i4 integer in [1, 100], x5 >= 1.1, x6 free, b binary.
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[4])

from fractions import Fraction as F
from decimal import Decimal, getcontext
import rv_osil as R

getcontext().prec = 50
m = R.load('spring')
V = {n: j for j, n in enumerate(m.vname)}
C = {n: r for r, n in enumerate(m.cname)}

a, b = F('1.570796327'), F('.7853981635')
k = F('6.95652173913044e-7')
K4 = F('2546.47908913782')
L3, U3 = m.vlb[V['x3']], m.vub[V['x3']]
assert L3 == F('1.78571428571429e-3') and U3 == F('2e-2')
assert m.vlb[V['x5']] == F('1.1') and m.vlb[V['x1']] == F('.414') and m.vlb[V['x2']] == F('.207')
assert m.vlb[V['i4']] == 1 and m.vub[V['i4']] == 100 and m.vtype[V['i4']] == 'I'
assert m.vlb[V['x6']] == '-INF' and m.vub[V['x6']] == 'INF'
assert m.vub[V['x1']] == 'INF' and m.vub[V['x2']] == 'INF' and m.vub[V['x5']] == 'INF'
diam = {'b%d' % (7 + i): -m.lin[C['e8']][V['b%d' % (7 + i)]] for i in range(11)}
assert m.lin[C['e8']][V['x2']] == 1 and len(m.lin[C['e8']]) == 12
print('diameters', [str(v) for v in diam.values()])


def dec(q):
    return Decimal(q.numerator) / Decimal(q.denominator)


def point(N, bname, x5):
    x = [F(0)] * len(m.vname)
    x[V['i4']] = F(N)
    x[V[bname]] = F(1)
    d = diam[bname]
    x[V['x2']] = d
    x[V['x5']] = x5
    x[V['x1']] = x5 * d
    x[V['x6']] = (4 * x5 - 1) / (4 * x5 - 4) + F('.615') / x5
    x[V['x3']] = k * x5 ** 3 * N / d
    return x


# randomized consistency test of the closed-form model against the OSIL rows
import random
random.seed(1)
for _ in range(200):
    N = random.randint(1, 100)
    bn = random.choice(list(diam))
    x5 = F(random.randint(1100, 20000), 1000)
    x = point(N, bn, x5)
    d = diam[bn]
    for r, want in [('e2', 0), ('e3', 0), ('e5', 0), ('e8', 0), ('e9', 1)]:
        assert R.row_value(m, C[r], x) == want, r
    assert R.row_value(m, C['e4'], x) == K4 * x[V['x6']] * x5 / d ** 2
    assert R.row_value(m, C['e6'], x) == F('2.1') * d + 1000 * x[V['x3']] + F('1.05') * d * N
    assert R.row_value(m, C['e7'], x) == x[V['x1']] + d
    assert R.obj_value(m, x) == (a + b * N) * x[V['x1']] * d ** 2
    assert (m.cub[C['e4']], m.cub[C['e6']], m.cub[C['e7']]) == (189000, 14, 3)
print('closed form agrees with the OSIL rows on 200 random points')


def cbrt_up(q, digits=40):
    """smallest decimal with 'digits' decimals whose cube >= q (q > 0)."""
    s = F(int(Decimal(q.numerator) / Decimal(q.denominator) ** 0 * 0) + 0)
    lo = F(0)
    hi = F(1)
    while hi ** 3 < q:
        hi *= 2
    scale = F(1, 10 ** digits)
    # bisection on integer multiples of scale
    L, H = 0, int(hi / scale) + 1
    while H - L > 1:
        M = (L + H) // 2
        if (M * scale) ** 3 >= q:
            H = M
        else:
            L = M
    return H * scale, L * scale


# (1) exactly feasible point for N = 9, b11 (the integer assignment of p2, p3)
for pname in ('p2', 'p3'):
    x, _ = R.read_sol(m, (_PUBLIC_REPO + '/research-20260929/bound-audit/sol/spring.%s.sol') % pname)
    print(pname, 'i4 =', x[V['i4']], 'ones:', [n for n in diam if x[V[n]] == 1], 'x2 =', x[V['x2']])
N, bn = 9, 'b11'
d = diam[bn]
c3 = L3 * d / (k * N)          # x5^3 at x3 = L3
x5_up, x5_dn = cbrt_up(c3)
x = point(N, bn, x5_up)
bad = R.check(m, x)
f = R.obj_value(m, x)
print('constructed point: violations', bad)
print('  x5 =', x5_up, ' x3 - L3 =', float(x[V['x3']] - L3))
print('  objective =', dec(f))
dl = F('0.84624567')
print('  d - f =', dec(dl - f), ' ratio to slack 5e-9 =', float((dl - f) / F(5, 10 ** 9)))
print('  in audit enclosure [0.8462456656363, 0.8462456656500]:', F('0.8462456656363') <= f <= F('0.8462456656500'))
fstar_lo = (a + b * N) * d ** 3 * x5_dn   # x5_dn^3 < c3 so x5_dn < cbrt(c3)
fstar_hi = (a + b * N) * d ** 3 * x5_up
print('  f* = (a+9b) d^3 cbrt(L3 d/(9k)) in [%s, %s]' % (dec(fstar_lo), dec(fstar_hi)))

# (2) global optimum. For each (N, d): objective = (a+bN) d^3 x5, increasing in x5.
# Relaxation lower bound: x5 >= max(1.1, .414/d, cbrt(L3 d/(kN))).
T = fstar_lo   # a rational strictly below f*
rest = []
infeas_simple = 0
for N in range(1, 101):
    for bn, d in diam.items():
        g = (a + b * N) * d ** 3
        # x5 needed to reach objective <= T
        cT = T / g
        # feasibility of the simple bounds: x3 <= min(U3, e6 cap), e7: x5 <= 3/d - 1
        x3cap = min(U3, (14 - F('2.1') * d - F('1.05') * d * N) / 1000)
        lo5 = max(F('1.1'), F('.414') / d)
        hi5 = 3 / d - 1
        # x5^3 range from x3 in [L3, x3cap]
        lo3 = L3 * d / (k * N)
        hi3 = x3cap * d / (k * N) if x3cap > 0 else F(-1)
        simple_infeasible = (x3cap < L3) or (hi5 < lo5) or (hi5 ** 3 < lo3) or (lo5 ** 3 > hi3)
        if simple_infeasible:
            infeas_simple += 1
            continue
        # can the combination reach an objective <= T ?  need x5 <= cT with x5 >= lo5 and x5^3 >= lo3
        if lo5 > cT or lo3 > cT ** 3:
            continue
        rest.append((N, bn, d, lo5, hi5, lo3, hi3, cT))
print('combos', 100 * 11, 'infeasible by simple bound/row checks:', infeas_simple,
      'remaining that could reach <= T:', [(r[0], r[1]) for r in rest])

# e4 in terms of C = x5 > 1:  K4/d^2 * h(C) <= 189000 with
#   h(C) = C*W(C) = C + 3/4 + 3/(4(C-1)) + .615   (exact identity, checked below)
# h is convex on C > 1 with minimum at c* = 1 + sqrt(3)/2, h(c*) = 2.365 + sqrt(3).
for C5 in [F(11, 10), F(3, 2), F(2), F(37, 7), F(100)]:
    W = (4 * C5 - 1) / (4 * C5 - 4) + F('.615') / C5
    assert C5 * W == C5 + F(3, 4) + 3 / (4 * (C5 - 1)) + F('.615')
SQ3_LO = F('1.7320508')
assert SQ3_LO ** 2 < 3
H_MIN_LO = F('2.365') + SQ3_LO       # <= min h


def h(C5):
    return C5 + F(3, 4) + 3 / (4 * (C5 - 1)) + F('.615')


def hmin_lower(p, q):
    """rational lower bound of min h on [p, q], 1 < p <= q (convexity)."""
    cstar_lo, cstar_hi = 1 + SQ3_LO / 2, 1 + F('1.7320509') / 2
    assert F('1.7320509') ** 2 > 3
    if q <= cstar_lo:
        return h(q)
    if p >= cstar_hi:
        return h(p)
    return H_MIN_LO


left = []
for (N, bn, d, lo5, hi5, lo3, hi3, cT) in rest:
    Rcap = 189000 * d ** 2 / K4
    # interval of C that could give objective <= T and satisfy the simple constraints:
    # C >= max(lo5, cbrt(lo3)) ; C <= min(hi5, cbrt(hi3), cT). Enclose cube roots outward.
    p = max(lo5, cbrt_up(lo3)[1])
    q = min(hi5, cbrt_up(hi3)[0], cT)
    if p > q:
        continue
    if hmin_lower(p, q) > Rcap:
        continue
    left.append((N, bn, float(p), float(q), float(Rcap), float(hmin_lower(p, q))))
print('combos not excluded from objective <= T by e4:', left)

# full per-combination minimum (for the second-best value and feasibility counts):
# feasible C-set = {C in [p0, q0] : h(C) <= Rcap}; with h convex this is an interval
# [p0, q0] intersect [r1, r2] (r1, r2 roots of h = Rcap). Minimum objective at its left end.
import math
feas, best = [], []
for N in range(1, 101):
    for bn, d in diam.items():
        x3cap = min(U3, (14 - F('2.1') * d - F('1.05') * d * N) / 1000)
        if x3cap < L3:
            continue
        p0 = max(F('1.1'), F('.414') / d, F(math.pow(float(L3 * d / (k * N)), 1 / 3)))
        q0 = min(3 / d - 1, F(math.pow(float(x3cap * d / (k * N)), 1 / 3)))
        Rcap = float(189000 * d ** 2 / K4)
        if float(H_MIN_LO) > Rcap + 1e-12 or p0 > q0:
            continue
        # roots of C + 3/4 + 3/(4(C-1)) + .615 = Rcap -> (C-1)^2 - (Rcap-2.365)(C-1) + 3/4 = 0
        s = Rcap - 2.365
        disc = s * s - 3
        if disc < 0:
            continue
        r1 = 1 + (s - math.sqrt(disc)) / 2
        r2 = 1 + (s + math.sqrt(disc)) / 2
        lo, hi = max(float(p0), r1), min(float(q0), r2)
        if lo <= hi:
            feas.append((N, bn))
            best.append((float((a + b * N) * d ** 3) * lo, N, bn))
best.sort()
print('numerically feasible combos: %d of 1100 (floating point, evidence only)' % len(feas))
print('best three (float):', best[:3])
