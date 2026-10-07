# Data for the margin figure: 19 class (i) + 12 class (i-r) (instance, solver) pairs + 3 rocket LINDO.
import json, csv
from fractions import Fraction as F
R = json.load(open('results.json'))
best = {}
for r in R:
    c = r.get('cls', '')
    if not (c.startswith('(i) ') or c.startswith('(i-r)')):
        continue
    d = F(r['d_listed']); hi = F(str(r['obj_hi'])); m = d - hi
    k = (r['name'], r['solver'])
    if k not in best or m > best[k]['m']:
        best[k] = dict(m=m, d=d, s=r['d_listed'], hi=str(r['obj_hi']), cls='(i)' if c.startswith('(i) ') else '(i-r)',
                       group=r.get('i_group', ''), date=r['d_date'], point=r['point'])
for n, s, hi in (('rocket100', '-1.0128319', '-1.0128320069130'), ('rocket200', '-1.01283563', '-1.0128356770677'),
                 ('rocket400', '-1.01283634', '-1.0128365294821')):
    d = F(s); best[(n, 'LINDO')] = dict(m=d - F(hi), d=d, s=s, hi=hi, cls='(i) outside screen', group='tolerance-scale',
                                        date={'rocket100': '23 May 2018', 'rocket200': '08 Mar 2015', 'rocket400': '13 Sep 2017'}[n], point='own CONOPT')
w = csv.writer(open('margin_figure.csv', 'w', newline=''))
w.writerow(['instance', 'solver', 'class', 'size_label', 'listed_dual', 'proven_f_upper', 'margin', 'margin_rel_absd', 'margin_units', 'bound_date', 'point'])
for (n, s), v in sorted(best.items(), key=lambda kv: -float(kv[1]['m'] / abs(kv[1]['d']))):
    t = v['s'].lstrip('-'); k = len(t.split('.')[1]) if '.' in t else 0
    w.writerow([n, s, v['cls'], v['group'], v['s'], v['hi'], '%.6g' % float(v['m']), '%.4g' % float(v['m'] / abs(v['d'])),
                '%.4g' % float(v['m'] * 10**k), v['date'], v['point']])
print(len(best), 'rows')
