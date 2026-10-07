"""Check the rigorous displays in audit-report.md against the exact values.

Exact data: the enclosures in results.json and the emfl bounds in logs/cert_socp_*.json.
- "[lo, hi]": matched to its intended quantity, the exact enclosure whose lower end is nearest
  to lo. The display must enclose it. Intervals quoted from the reviews (tighter, or a different
  repaired point) fail as "NOT ENCLOSING" and must be checked by hand.
- A number ending in "…": must be a truncation of an exact audit value (an enclosure end, an
  enclosed exact objective, or an emfl lower bound). Values quoted from the reviews fail as
  "NOT A TRUNCATION" and must be checked by hand.
- "opt >= x" or "≥ x": if x is within 1e-6 of an emfl lower bound L, x <= L is required. Other
  "≥" numbers (the histogram row "≥ 0.1") are skipped.
- "value v is below the exact optimum by at least g": g <= L - v for the emfl instance whose L
  is nearest to v.
Not checked: margins, ratios and other "at least" statements (sizes, rounded to nearest).

Usage: python3 check_display.py
"""
import json, os, re
from fractions import Fraction

os.chdir(os.path.dirname(os.path.abspath(__file__)))
R = json.load(open('results.json'))
exact = {}  # label -> (lo, hi) exact
for r in R:
    if r.get('obj_lo'):
        exact[f"{r['name']}.{r['point']}"] = (Fraction(r['obj_lo']), Fraction(r['obj_hi']))
Ls = {}
for n in ['emfl050_3_3', 'emfl050_5_5', 'emfl100_3_3', 'emfl100_5_5']:
    c = json.load(open(f'logs/cert_socp_{n}.json'))
    L = Fraction(c['lower_bound_30_digits_rounded_down'].replace('e-30', '')) / 10**30
    Ub = Fraction(c['rigorous_upper_bound_from_numerical_optimum'])
    U = Ub + Fraction(1, 10**14)  # the stored float is within half an ulp (< 1e-14) of the exact bound
    Ls[n] = L
    exact[n + '.opt'] = (L, U)
# exact values a "…" display may truncate, each as an interval known to contain it
values = []
for k, (a, b) in exact.items():
    if k.endswith('.opt'):
        values.append((k, a, a + Fraction(1, 10**30)))  # the exact lower bound (stored rounded down at 30 decimals)
    else:
        values += [(k, a, a), (k, b, b), (k, a, b)]  # enclosure ends (exact), and the enclosed objective
txt = open('audit-report.md').read().replace('−', '-')
num = r'-?\d+\.\d+'
line = lambda i: txt.count('\n', 0, i) + 1
ok = bad = skipped = 0
for m in re.finditer(r'\[(' + num + r'), (' + num + r')\]', txt):
    lo, hi = Fraction(m.group(1)), Fraction(m.group(2))
    k = min(exact, key=lambda k: abs(exact[k][0] - lo))
    a, b = exact[k]
    if lo <= a and b <= hi:
        ok += 1
    else:
        bad += 1; print('NOT ENCLOSING line', line(m.start()), m.group(0), '->', k, [float(a), float(b)])
for m in re.finditer(r'(' + num + r')…', txt):
    s = m.group(1); v = Fraction(s); u = Fraction(1, 10**len(s.split('.')[1]))
    trunc = lambda a, b: (v <= a and b < v + u) if v >= 0 else (v - u < a and b <= v)
    hits = [k for k, a, b in values if trunc(a, b)]
    if hits:
        ok += 1
    else:
        bad += 1; print('NOT A TRUNCATION line', line(m.start()), s + '…')
for m in re.finditer(r'(?:opt >= |≥ )(' + num + r')', txt):
    v = Fraction(m.group(1))
    cand = [n for n, L in Ls.items() if abs(L - v) < Fraction(1, 10**6)]
    if not cand:
        skipped += 1; print('skipped (not an emfl lower bound) line', line(m.start()), m.group(0)); continue
    if all(v <= Ls[n] for n in cand): ok += 1
    else: bad += 1; print('LOWER BOUND ABOVE EXACT line', line(m.start()), m.group(0))
for m in re.finditer(r'value (' + num + r') is below the\s+exact optimum by at least (\d+(?:\.\d+)?e-\d+)', txt):
    v, g = Fraction(m.group(1)), Fraction(m.group(2))
    n = min(Ls, key=lambda n: abs(Ls[n] - v))
    if g <= Ls[n] - v: ok += 1
    else: bad += 1; print('DIFFERENCE NOT PROVEN line', line(m.start()), n, m.group(2), float(Ls[n] - v))
print(f'ok {ok}, failed {bad}, skipped {skipped}')
