"""Exact checks of hand-written displays in sections/E-audit.tex (round-1 items G7-07).
Run in a /tmp copy: kraw/ holds copies of research-20260929/reviews/bound-audit-verification/logs/
kraw_*.json; exact_forms.py and pages/models/gms/methanol50.gms are copies from
research-20260929/publication/minlplib-status/; the OSIL file is read from ~/.cache/minlplib."""
import json, math, sys
from fractions import Fraction as F


def ceil_dec(x, k):
    n = math.ceil(x * 10 ** k)
    s = '-' if n < 0 else ''
    a = str(abs(n)).rjust(k + 1, '0')
    return s + a[:-k] + '.' + a[-k:]


print('tab:audit-second, second-proof upper ends (field obj_hi), exact ceilings at the printed decimals')
for pt, old in [('glider100.p2', '-983842.2577881224'), ('methanol50.p4', '0.0079302187992'),
                ('nuclear14.p3', '-1.12968744117116'), ('ghg_3veh.p2', '7.754006050057346')]:
    hi = F(json.load(open(f'kraw/kraw_{pt}.json'))['obj_hi'])
    k = len(old.split('.')[1])
    new = ceil_dec(hi, k)
    print(f'  {pt}: obj_hi = {hi} ~ {float(hi):.17g}; printed {old}: '
          f"{'SAFE' if F(old) >= hi else 'UNSAFE, below by %.4e' % float(hi - F(old))}; ceiling at {k} decimals = {new}")

sys.path.insert(0, '.')
import exact_forms as X
X.HERE = '.'
g = X.read_gms('pages/models/gms/methanol50.gms')
o = X.read_osil(X.OSIL + '/methanol50.osil')
_, gobj = X.gms_objective(g)
d = X.coef_diffs(gobj, o['obj'][0])
pairs = [(F(a), F(b)) for _, a, b in d]
rel = [abs(b - a) / abs(a) for a, b in pairs if a != 0]
mx = max(rel)
print(f'methanol50 objective: {len(pairs)} coefficient differences, {sum(1 for a, b in pairs if a == 0)} new terms; '
      f'max relative change = {mx} ~ {float(mx):.10e}; <= 2.38e-16: {mx <= F("2.38e-16")}; <= 2.39e-16: {mx <= F("2.39e-16")}')
