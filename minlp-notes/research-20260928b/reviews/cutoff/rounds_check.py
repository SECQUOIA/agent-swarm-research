"""Propositions 3.9 and 3.10 of cutoff-propagation.md, reviewer's code.

3.9: f = s^2 - 2as + a^2 (terms s^2 and s), HC4 from [a - y0, a + x0], cutoff
     -eps.  Checks (i) the one-round recursion y' = y - (y^2+eps)/(2a),
     x' = sqrt(a^2 + 2ax - eps) - a against the propagator, (ii) the proved
     lower bound on the number of nonempty rounds, (iii) rounds*sqrt(eps)/a.
     Also a chaotic schedule, for comparison.
3.10: u = t^2, v = u^2, f = u - 2v on [-1/3, 2/3]: rounds against the bound
     2 + log2(ln(1/(2eps))/ln(1/(2U0))).
Also: Theorem 3.1(a) with a shared non-variable base s = x - y.
Run: python3 rounds_check.py > logs/rounds_check.log
"""
import math
import numpy as np
from ifbbt import DAG
from t31_check import tmin
from numpy.polynomial import polynomial as P


def quad(a):
    d = DAG(1); p = d.pow(0, 2); d.sum([p, 0], [1.0, -2.0 * a], a * a)
    return d


print('Prop 3.9: recursion check (a=1, eps=1e-4, x0=y0=0.25), first 5 rounds')
a, eps = 1.0, 1e-4
d = quad(a)
x, y = 0.25, 0.25
for k in range(1, 6):
    st, Z, r = d.propagate([(a - 0.25, a + 0.25)], -eps, max_rounds=k)
    x, y = math.sqrt(a * a + 2 * a * x - eps) - a, y - (y * y + eps) / (2 * a)
    lo, hi = Z[0]
    print(f'  round {k}: propagator s = [{lo:.12f}, {hi:.12f}]  recursion [{a - y:.12f}, {a + x:.12f}]')

print('\nProp 3.9: rounds until empty vs proved lower bound LB')
print('  a    eps    x0     y0    rounds  LB      rounds*sqrt(eps)/a  chaotic')
viol = 0
for a in (1.0, 2.0):
    d = quad(a)
    for x0, y0 in ((a / 4, a / 4), (a / 4, a / 10), (a / 20, a / 4)):
        for e in (1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-7):
            if e > a * a / 16:
                continue
            st, _, r = d.propagate([(a - y0, a + x0)], -e, max_rounds=10 ** 6)
            st2, _, r2 = d.propagate([(a - y0, a + x0)], -e, max_rounds=10 ** 6, schedule='chaotic')
            z0 = min(x0, y0)
            LB = a / (4 * math.sqrt(e)) * (math.atan(z0 / math.sqrt(e)) - math.atan(4 * math.sqrt(e) / a)) - 1
            viol += r < LB
            print(f'  {a:.0f}  {e:.0e}  {x0:.3f}  {y0:.3f}  {r:7d}  {LB:8.1f}  {r * math.sqrt(e) / a:6.3f}   {st2} {r2}')
print(f'  lower-bound violations: {viol}')

print('\nProp 3.10: u-form rounds vs bound')
du = DAG(1); u = du.pow(0, 2); v = du.pow(u, 2); du.sum([u, v], [1.0, -2.0])
U0 = 4 / 9
for e in (1e-2, 1e-4, 1e-6, 1e-8, 1e-12):
    st, _, r = du.propagate([(-1 / 3, 2 / 3)], -e)
    bnd = 2 + math.log2(math.log(1 / (2 * e)) / math.log(1 / (2 * U0)))
    print(f'  eps={e:.0e}: {st} after {r} rounds; bound {bnd:.2f}')

print('\nTheorem 3.1(a) with a shared base s = x - y (terms phi(x), psi(s), chi(s), s):')
rng = np.random.default_rng(5)
worst, cnt = -np.inf, 0
for trial in range(40):
    cx = [rng.normal(size=5) for _ in range(2)]
    cs = [rng.normal(size=5) for _ in range(2)]
    for c in cx + cs:
        c[0] = 0.0
    lin = rng.normal()
    dd = DAG(2)
    s = dd.sum([0, 1], [1.0, -1.0])
    ch = [dd.up(0, cx[0]), dd.up(0, cx[1]), dd.up(s, cs[0]), dd.up(s, cs[1]), s]
    dd.sum(ch, [1, 1, 1, 1, lin])
    box = [(rng.uniform(-1.5, 0.5), 0), (rng.uniform(-1.5, 0.5), 0)]
    box = [(lo, lo + rng.uniform(0.5, 2.0)) for lo, _ in box]
    F0 = dd.forward_box(box)[-1]
    for frac in (0.1, 0.3, 0.5, 0.7):
        c = F0[0] + frac * (dd.f([0.5 * (p + q) for p, q in box]) - F0[0])
        st, Z, r = dd.propagate(box, c, max_rounds=20000)
        if Z is None:
            continue
        X, Sg = Z[0], Z[s]
        terms = [(cx[0], X), (cx[1], X), (cs[0], Sg), (cs[1], Sg), (np.array([0.0, lin]), Sg)]
        mins = [tmin(cc, *I) for cc, I in terms]
        hs = [max(P.polyval(I[0], cc), P.polyval(I[1], cc)) for cc, I in terms]
        Phi = sum(mins) + max(hh - mm for hh, mm in zip(hs, mins))
        worst = max(worst, Phi - c)
        cnt += 1
print(f'  {cnt} nonempty fixed boxes; max (Phi(base intervals) - c) = {worst:.2e} (<= 0 expected)')
