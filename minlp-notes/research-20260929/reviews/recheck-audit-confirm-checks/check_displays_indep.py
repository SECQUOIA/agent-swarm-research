"""Independent check of every rigorous display in bound-audit/audit-report.md.

For each "[lo, hi]" the intended exact quantity is the one whose exact lower end is nearest
to lo (not "any quantity that fits", as in bound-audit/check_display.py). The display must
enclose it: lo <= exact_lo and exact_hi <= hi. For each value ending in "…", the digits
shown must be a truncation of an exact value. "≥ x", "opt >= x" and "at least x" are
checked against the exact emfl lower bounds. Exact data: bound-audit/results.json and
bound-audit/logs/cert_socp_*.json. Read-only.

Usage: python3 check_displays_indep.py
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[3])

import json, re
from fractions import Fraction as F
from decimal import Decimal

A = (_PUBLIC_REPO + '/research-20260929/bound-audit/')
R = json.load(open(A + 'results.json'))
ex = {}
for r in R:
    if r.get('obj_lo'):
        ex[f"{r['name']}.{r['point']}"] = (F(r['obj_lo']), F(r['obj_hi']), r['obj_lo'], r['obj_hi'])
L = {}
for n in ['emfl050_3_3', 'emfl050_5_5', 'emfl100_3_3', 'emfl100_5_5']:
    c = json.load(open(A + f'logs/cert_socp_{n}.json'))
    lo = F(c['lower_bound_30_digits_rounded_down'].replace('e-30', '')) / 10**30
    ub = F(c['rigorous_upper_bound_from_numerical_optimum'])
    # the upper bound is stored as float(ub_exact): exact value within half an ulp
    ulp = F(2) ** (Decimal(c['rigorous_upper_bound_from_numerical_optimum']).adjusted() * 0 - 52 + 5)  # 2^-47 >= ulp for values < 64
    L[n] = lo
    ex[n + '.opt'] = (lo, ub + ulp, None, None)
txt = open(A + 'audit-report.md').read()
t = txt.replace('−', '-')
num = r'-?\d+\.\d+'
lines = lambda i: t.count('\n', 0, i) + 1
print('== intervals')
for m in re.finditer(r'\[(' + num + r')…?, (' + num + r')…?\]', t):
    lo, hi = F(m.group(1)), F(m.group(2))
    k = min(ex, key=lambda k: abs(ex[k][0] - lo))
    a, b = ex[k][0], ex[k][1]
    ok = lo <= a and b <= hi
    print(('ok  ' if ok else 'FAIL'), 'line', lines(m.start()), m.group(0), '->', k,
          '' if ok else f'exact [{float(a)!r}, {float(b)!r}]')
print('== truncated values (…)')
exact_strings = [s for v in ex.values() for s in v[2:] if s] + \
    [str(json.load(open(A + f'logs/cert_socp_{n}.json'))['lower_bound_30_digits_rounded_down']) for n in L]
def dec30(s):
    if 'e-30' in s:
        d = s.replace('e-30', ''); return d[:-30] + '.' + d[-30:]
    return s
exact_strings = [dec30(s).lstrip('-') for s in exact_strings]
for m in re.finditer(r'(\d+\.\d+)…', t):
    s = m.group(1)
    hit = any(e.startswith(s) for e in exact_strings)
    print(('ok  ' if hit else 'NOT A TRUNCATION'), 'line', lines(m.start()), s + '…')
print('== lower bounds')
for m in re.finditer(r'(?:opt >= |≥ |at least )(\d+(?:\.\d+)?e-\d+|' + num + r')', t):
    v = m.group(1); ln = lines(m.start())
    ctx = t[max(0, m.start() - 160): m.start()]
    if 'e-' in v:  # "at least 1.42e-5 / 6.87e-6": difference exact optimum - listed optimal value
        pairs = {'1.42e-5': ('emfl050_3_3', '10.40173793'), '6.87e-6': ('emfl100_5_5', '32.63818348')}
        if v in pairs:
            n, p = pairs[v]; diff = L[n] - F(p)
            print(('ok  ' if F(Decimal(v)) <= diff else 'FAIL'), 'line', ln, 'at least', v, 'exact diff >=', float(diff))
        continue
    x = F(v)
    cand = [n for n in L if abs(L[n] - x) < F(1, 10**6)]
    if not cand:
        print('skip', 'line', ln, m.group(0)); continue
    print(('ok  ' if all(x <= L[n] for n in cand) else 'FAIL'), 'line', ln, m.group(0), cand)
