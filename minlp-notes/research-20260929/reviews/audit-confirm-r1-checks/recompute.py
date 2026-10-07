"""Independent recomputation of the numbers changed in Section 10.2 of bound-audit/audit-report.md.

Read-only on the audit's data. Exact arithmetic with Fraction throughout.
Usage: python3 recompute.py   (run from any directory)
"""
import json, os, re
from collections import Counter
from decimal import Decimal, getcontext, ROUND_FLOOR, ROUND_CEILING
from fractions import Fraction as F

getcontext().prec = 80
HERE = os.path.dirname(os.path.abspath(__file__))
BA = os.path.join(HERE, '..', '..', 'bound-audit')
REV = os.path.join(HERE, '..')
R = json.load(open(os.path.join(BA, 'results.json')))
P = json.load(open(os.path.join(BA, 'pages.json')))


def dec(q, n=30):
    """Decimal expansion of a Fraction, truncated toward zero at n decimals."""
    s = '-' if q < 0 else ''
    q = abs(q)
    ip = q.numerator // q.denominator
    fr = q - ip
    return s + str(ip) + '.' + str((fr * 10**n).numerator // (fr * 10**n).denominator).zfill(n)


def outward(lo, hi, n):
    """Round [lo, hi] outward at n decimals."""
    lo_d = Decimal(lo.numerator) / Decimal(lo.denominator)
    hi_d = Decimal(hi.numerator) / Decimal(hi.denominator)
    qz = Decimal(1).scaleb(-n)
    return str(lo_d.quantize(qz, ROUND_FLOOR)), str(hi_d.quantize(qz, ROUND_CEILING))


print('== item 1: margins of the four "clear" pairs')
for name, solver in [('methanol50', 'LINDO'), ('glider100', 'COUENNE'), ('glider100', 'LINDO'),
                     ('topopt-cantilever_60x40_50', 'LINDO')]:
    rows = [r for r in R if r['name'] == name and r['solver'] == solver and r.get('obj_hi')]
    best = None
    for r in rows:
        d = F(r['d_listed'])
        f = F(r['obj_hi']) if r['sense'] == 'min' else F(r['obj_lo'])
        m = d - f if r['sense'] == 'min' else f - d
        if best is None or m > best[0]:
            best = (m, d, r['point'])
    m, d, pt = best
    print(f'{name} {solver} {pt}: d-f = {float(m):.6g}; /|d| = {float(m / abs(d)):.6g}; '
          f'/max(1,|d|) = {float(m / max(1, abs(d))):.6g}; |d| = {float(abs(d)):.6g}')

print('\n== item 2: solver labels in pages.json')
cnt = Counter()
finite = 0
for inst in P:
    for dl in inst['duals']:
        cnt[dl['solver']] += 1
        try:
            v = float(dl['value'])
            finite += v == v and abs(v) != float('inf')
        except ValueError:
            pass
print('labels', len(cnt), 'duals', sum(cnt.values()), 'finite', finite)
flag_solvers = sorted({r['solver'] for r in R})
print('solvers in results.json:', len(flag_solvers), flag_solvers)
print('with flagged pairs:', sum(cnt[s] for s in flag_solvers), {s: cnt[s] for s in flag_solvers})
others = {s: c for s, c in cnt.items() if s not in flag_solvers}
print('others:', sum(others.values()), others)
# independent re-screen: does any dual of any label lie strictly beyond a listed point with infeas <= 1e-5?
screened = Counter()
for inst in P:
    if inst['sense'] not in ('min', 'max'):
        continue
    for dl in inst['duals']:
        try:
            d = F(dl['value'])
        except (ValueError, ZeroDivisionError):
            continue
        for p in inst['points']:
            try:
                if float(p['infeas']) > 1e-5:
                    continue
                v = F(p['value'])
            except (ValueError, TypeError):
                continue
            if (inst['sense'] == 'min' and d > v) or (inst['sense'] == 'max' and d < v):
                screened[dl['solver']] += 1
print('re-screened pairs per label:', dict(screened), 'total', sum(screened.values()))

print('\n== item 3: "…" values')
ln = open(os.path.join(REV, 'bound-audit-verification', 'logs', 'nd_netgen_exact.log')).read()
m = re.search(r'variant A: .*?objective = (\d+)/(\d+)', ln)
q = F(int(m.group(1)), int(m.group(2)))
print('verifier nd_netgen variant A:', dec(q, 24))
g = json.load(open(os.path.join(BA, 'logs', 'verify', 'ghg_3veh.p2.json')))
glo, ghi = F(g['obj_lo']), F(g['obj_hi'])
print('ghg_3veh.p2 exact ends:', dec(glo, 20), dec(ghi, 20))
print('ghg_3veh outward at 14 decimals:', outward(glo, ghi, 14), ' at 12:', outward(glo, ghi, 12))

print('\n== item 5: emfl listed points versus the exact lower bound L')
L = {}
U = {}
for n in ['emfl050_3_3', 'emfl050_5_5', 'emfl100_3_3', 'emfl100_5_5']:
    c = json.load(open(os.path.join(BA, 'logs', f'cert_socp_{n}.json')))
    L[n] = F(int(c['lower_bound_30_digits_rounded_down'].split('e')[0]), 10**30)
    U[n] = F(c['rigorous_upper_bound_from_numerical_optimum'])
for inst in P:
    if inst['name'] not in L:
        continue
    n = inst['name']
    for p in inst['points']:
        v = F(p['value'])
        dec_places = len(p['value'].split('.')[1]) if '.' in p['value'] else 0
        vhi = v + F(1, 2 * 10**dec_places)
        print(f"{n} {p['point']} {p['section']:6s} infeas {p['infeas']:>6s} value {p['value']:>12s} "
              f"L - (v + half unit) = {float(L[n] - vhi):+.4g}  rel {float((L[n] - v) / L[n]):+.3g}  "
              f"above U: {v > U[n]}")
    print(f"  listing primal {inst['listing_primal']}, duals max {max(F(d['value']) for d in inst['duals'])} <= L: "
          f"{all(F(d['value']) <= L[n] for d in inst['duals'])}")

print('\n== item 6: LINDO sssd*persp and nuclear14 pair margins (strongest point)')
for name in ['sssd20-04persp', 'sssd22-08persp', 'sssd25-04persp', 'sssd25-08persp', 'nuclear14']:
    ms = []
    for r in R:
        if r['name'] == name and r['solver'] == 'LINDO':
            d = F(r['d_listed'])
            m = d - F(r['obj_hi']) if r['sense'] == 'min' else F(r['obj_lo']) - d
            ms.append((m / abs(d), r['point']))
    print(name, [(pt, f'{float(x):.4g}') for x, pt in ms], 'pair:', f'{float(max(ms)[0]):.4g}')

print('\n== item 7: emfl enclosures [L, U], outward at 10 decimals; recheck intervals inside')
rk = {'emfl050_5_5': ('18.9136329557291', '18.9136329557624'),
      'emfl100_3_3': ('18.1326531242336', '18.1326531242359'),
      'emfl100_5_5': ('32.6381903545115', '32.6381903545301'),
      'emfl050_3_3': ('10.40175213184103', '10.40175213184476')}
for n in L:
    # the stored upper bound is float(ub); pad it by one ulp-scale amount (1e-14) to be safe
    lo, hi = outward(L[n], U[n] + F(1, 10**14), 10)
    a, b = map(F, rk[n])
    print(n, [lo, hi], 'gap U-L', f'{float(U[n] - L[n]):.3g}', 'recheck/verifier interval inside exact [L, U]:',
          L[n] <= a and b <= U[n], ' inside displayed:', F(lo) <= a and b <= F(hi))
