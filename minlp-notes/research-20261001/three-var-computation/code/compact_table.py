"""Compact markdown table from logs/table_<dir>.md (method_table.py output).

One row per instance: U, then for KA, KAF, F, XF, X the gap closure relative to U
(safe bounds), then solve time (s) and total PSD dimension for KA, F and X.
Usage: python compact_table.py dir"""
import sys

rows = open('../logs/table_%s.md' % sys.argv[1]).read().splitlines()[2:]
data, order, cur = {}, [], None
for r in rows:
    c = [x.strip() for x in r.split('|')[1:-1]]
    if c[0]:
        cur = c[0]
        order.append(cur)
        data[cur] = {'U': c[1]}
    data[cur][c[2]] = {'closed': c[4], 'time': c[7], 'blocks': c[9], 'psd': c[12]}
M = ['KA', 'KAF', 'F', 'XF', 'X']
print('| instance | U | ' + ' | '.join('closed %s' % m for m in M) + ' | time KA / F / X (s) | PSD dim KA / F / X | blocks F / X |')
print('|---|---|' + '---|' * len(M) + '---|---|---|')
for t in order:
    d = data[t]
    g = lambda m, k: d[m][k] if m in d else '-'
    print('| %s | %s | %s | %s / %s / %s | %s / %s / %s | %s / %s |' % (
        t, d['U'].replace(' (feas)', '').replace(' (opt)', ' (opt.; tol.)'), ' | '.join(g(m, 'closed') for m in M),
        g('KA', 'time'), g('F', 'time'), g('X', 'time'), g('KA', 'psd'), g('F', 'psd'), g('X', 'psd'),
        g('F', 'blocks').replace(' F', ''), g('X', 'blocks').replace(' X', '')))
