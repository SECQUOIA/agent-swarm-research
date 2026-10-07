"""Rigorous global optimum of spring (exact rational arithmetic).

spring (17 variables) reduces, for each integer assignment, to one variable:
  e9, binaries: exactly one b_k = 1, so e8 gives x2 = c_k (11 values);
  i4 = n in {1..100};
  e2: x1 = x2*x5;  e3: x6 = (4x5-1)/(4x5-4) + 0.615/x5;
  e5: x3 = C*n*x5^3/x2 with C = 6.95652173913044e-7;
  objective (1.570796327 + 0.7853981635 n)*x1*x2^2 = K_n * c_k^3 * x5,
  increasing in x5.
The remaining conditions are intervals in x5:
  x5 >= 1.1;  x1 >= 0.414: x5 >= 0.414/c;  lb3 <= x3 <= 0.02: cube roots;
  e6: 2.1c + 1000*x3 + 1.05*c*n <= 14: cube root;  e7: x5 <= 3/c - 1;
  e4: 2546.47908913782*x6*x5/c^2 <= 189000, where x6*x5 = g(x5) =
      (x5-1) + 7/4 + 3/(4(x5-1)) + 0.615 is convex on x5 > 1, so e4 is
      y^2 - B*y + 3/4 <= 0 with y = x5 - 1, B = G - 2.365,
      G = 189000*c^2/2546.47908913782.
So for each (n, k) the feasible set is [max L, min U] and its minimum is
K_n c^3 max L. Cube and square roots are bracketed by rationals and every
bracket is checked by exact arithmetic. The reduction itself is checked:
every row and the objective of the OSiL model are compared exactly with the
formulas above at random rational points.
"""
import json
import math
import os
import random
from fractions import Fraction as Q

import osilq

HERE = os.path.dirname(os.path.abspath(__file__))
OSIL = os.path.expanduser('~/.cache/minlplib/minlplib/osil/spring.osil')
SCALE = 10 ** 30

m = osilq.Model(OSIL)
N = m.index
C = Q('6.95652173913044e-7')
K0, K1 = Q('1.570796327'), Q('.7853981635')
E4C, E4U = Q('2546.47908913782'), m.rub[m.rnames.index('e4')]
lb3, ub3 = m.lb[N['x3']], m.ub[N['x3']]
e8 = m.rnames.index('e8')
bins = ['b%d' % k for k in range(7, 18)]
cs = [-m.lin[e8][N[b]] for b in bins]
assert m.lb[N['x1']] == Q('.414') and m.lb[N['x5']] == Q('1.1')
assert m.lb[N['i4']] == 1 and m.ub[N['i4']] == 100 and m.vtype[N['i4']] == 'I'
assert all(m.vtype[N[b]] == 'B' for b in bins) and m.lb[N['x2']] == Q('.207')
assert m.lb[N['x6']] is None and m.ub[N['x6']] is None
assert m.ub[N['x1']] is None and m.ub[N['x2']] is None and m.ub[N['x5']] is None

# ---- check the reduction against the model at random rational points
rng = random.Random(1)
R = {r: m.rnames.index(r) for r in m.rnames}
for _ in range(200):
    x = [Q(rng.randint(1, 10 ** 6), rng.randint(1, 10 ** 6)) + 2 for _ in range(m.n)]
    x1, x2, x3, n, x5, x6 = (x[N[v]] for v in ('x1', 'x2', 'x3', 'i4', 'x5', 'x6'))
    assert m.row(R['e2'], x) == x5 - x1 / x2
    assert m.row(R['e3'], x) == x6 - ((4 * x5 - 1) / (4 * x5 - 4) + Q('.615') / x5)
    assert m.row(R['e4'], x) == E4C * x6 * x5 / x2 ** 2
    assert m.row(R['e5'], x) == x3 - C * x5 ** 3 * n / x2
    assert m.row(R['e6'], x) == Q('2.1') * x2 + 1000 * x3 + Q('1.05') * x2 * n
    assert m.row(R['e7'], x) == x1 + x2
    assert m.row(R['e8'], x) == x2 - sum(c * x[N[b]] for c, b in zip(cs, bins))
    assert m.row(R['e9'], x) == sum(x[N[b]] for b in bins)
    assert m.obj(x) == (K0 + K1 * n) * x1 * x2 ** 2
    x5 = Q(rng.randint(11, 10 ** 6), 10)     # g identity on x5 > 1
    assert x5 * ((4 * x5 - 1) / (4 * x5 - 4) + Q('.615') / x5) == \
        (x5 - 1) + Q(7, 4) + Q(3, 4) / (x5 - 1) + Q('.615')
assert [m.rlb[R[r]] for r in ('e2', 'e3', 'e5', 'e8', 'e9')] == [0, 0, 0, 0, 1]
assert [m.rub[R[r]] for r in ('e4', 'e6', 'e7')] == [189000, 14, 3]
assert all(m.rlb[R[r]] is None for r in ('e4', 'e6', 'e7'))


# ---- rational brackets of roots
def cbrt_br(a):
    """(lo, hi) with lo^3 <= a <= hi^3, hi - lo = 1/SCALE (a >= 0)."""
    t = a * SCALE ** 3
    n = t.numerator // t.denominator
    lo, hi = 0, 1
    while hi ** 3 <= n:
        hi *= 2
    while hi - lo > 1:
        mid = (lo + hi) // 2
        lo, hi = (mid, hi) if mid ** 3 <= n else (lo, mid)
    L, H = Q(lo, SCALE), Q(lo + 1, SCALE)
    assert L ** 3 <= a <= H ** 3
    return L, H


def sqrt_br(a):
    t = a * SCALE ** 2
    r = math.isqrt(t.numerator // t.denominator)
    L, H = Q(r, SCALE), Q(r + 1, SCALE)
    assert L * L <= a <= H * H
    return L, H


def combo(n, c):
    """Return ('infeasible', reason) or ('ok', lower bound on min x5,
    upper bound on min x5, which lower limit binds)."""
    n = Q(n)
    lows = {'x5>=1.1': (Q('1.1'),) * 2, 'x1>=0.414': (Q('.414') / c,) * 2,
            'x3>=lb': cbrt_br(lb3 * c / (C * n))}
    ups = {'x3<=0.02': cbrt_br(ub3 * c / (C * n)), 'e7': (3 / c - 1,) * 2}
    rest6 = 14 - Q('2.1') * c - Q('1.05') * c * n
    if rest6 <= 0:
        return ('infeasible', 'e6: 2.1c + 1.05cn >= 14')
    ups['e6'] = cbrt_br(rest6 * c / (1000 * C * n))
    G = E4U * c * c / E4C
    B = G - Q('2.365')
    disc = B * B - 3
    if B <= 0 or disc < 0:
        return ('infeasible', 'e4: g(x5) > G for all x5 > 1')
    s = sqrt_br(disc)
    # y1 = (B - sqrt(disc))/2, y2 = (B + sqrt(disc))/2
    lows['e4'] = (1 + (B - s[1]) / 2, 1 + (B - s[0]) / 2)
    ups['e4'] = (1 + (B + s[0]) / 2, 1 + (B + s[1]) / 2)
    Llo = max(v[0] for v in lows.values())
    Lhi = max(v[1] for v in lows.values())
    Ulo = min(v[0] for v in ups.values())
    Uhi = min(v[1] for v in ups.values())
    if Llo > Uhi:
        return ('infeasible', 'max lower limit > min upper limit')
    bind = max(lows, key=lambda k: lows[k][1])
    return ('ok', Llo, Lhi, Ulo, Uhi, bind)


rows = []
best = None
for n in range(1, 101):
    for k, c in enumerate(cs):
        r = combo(n, c)
        if r[0] == 'infeasible':
            rows.append(dict(n=n, b=bins[k], status='infeasible', reason=r[1]))
            continue
        _, Llo, Lhi, Ulo, Uhi, bind = r
        K = (K0 + K1 * n) * c ** 3
        flo, fhi = K * Llo, K * Lhi
        sure = Lhi <= Ulo            # min x5 certainly feasible
        rows.append(dict(n=n, b=bins[k], status='feasible' if sure else 'undecided',
                         fmin_lo=flo, fmin_hi=fhi, binding=bind))
        if best is None or flo < best['fmin_lo']:
            best = rows[-1]

T = Q('0.84624567') - Q(5, 10 ** 9)
lb_all = min(r['fmin_lo'] for r in rows if r['status'] != 'infeasible')
others = [r for r in rows if r['status'] != 'infeasible' and r is not best]
second = min(others, key=lambda r: r['fmin_lo'])
n_inf = sum(r['status'] == 'infeasible' for r in rows)
n_und = sum(r['status'] == 'undecided' for r in rows)


def dstr(q, d=25):
    s = '-' if q < 0 else ''
    q = abs(q)
    ip = q.numerator // q.denominator
    return s + str(ip) + '.' + str(int((q - ip) * 10 ** d)).rjust(d, '0')


out = dict(
    combos=len(rows), infeasible=n_inf, undecided=n_und,
    argmin=dict(n=best['n'], b=best['b'], status=best['status'], binding=best['binding']),
    global_opt_lower_bound=dstr(lb_all),
    argmin_fmin=[dstr(best['fmin_lo']), dstr(best['fmin_hi'])],
    second_best=dict(n=second['n'], b=second['b'], status=second['status'],
                     fmin_lo=dstr(second['fmin_lo'], 12), binding=second['binding']),
    threshold_d_minus_slack=dstr(T, 12),
    global_lb_ge_threshold=lb_all >= T,
    listed_dual='0.84624567',
    dual_minus_opt_upper=dstr(Q('0.84624567') - best['fmin_lo'], 20),
    listed_p3_value='0.8462441',
    opt_minus_p3_display=float(best['fmin_lo'] - Q('0.8462441')),
)
os.makedirs(os.path.join(HERE, 'logs'), exist_ok=True)
json.dump(out, open(os.path.join(HERE, 'logs', 'spring_global.json'), 'w'), indent=1)
print(json.dumps(out, indent=1))
