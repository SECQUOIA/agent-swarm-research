"""Review r2: were the eight wall-timeout attempts in logs/full_stock retried without bias?

For each archived attempt: the retried final log must repeat the attempt's display rows
(all columns except time and memory); report CPU at the attempt's last node in both, and
final status. Also lists every non-zero return code in driver.jsonl.
"""
import json, re
from pathlib import Path

D = Path(__file__).resolve().parents[2] / 'logs/full_stock'


def rows(p):
    out = []
    for l in p.read_text(errors='replace').splitlines():
        m = re.match(r'^[ a-zA-Z*]?\s*([0-9.]+)s\|(.*)$', l)
        if m:
            c = m.group(2).split('|')
            out.append((float(m.group(1)), '|'.join(c[:4] + c[5:])))
    return out


ev = [json.loads(l) for l in (D / 'driver.jsonl').open()]
print('driver events:', {e: sum(r['event'] == e for r in ev) for e in ('start', 'done', 'skip', 'finish', 'cancelled')})
print('non-zero returns:', [(r['instance'], r['seed'], r['returncode'], round(r['wall'])) for r in ev if r['event'] == 'done' and r['returncode'] != 0])
print('final logs:', len(list(D.glob('*.log'))), 'attempts:', len(list((D / 'attempts').glob('*.log'))))
for a in sorted((D / 'attempts').glob('*.log')):
    name = a.name.split('.')[0] + '.scip.' + a.name.split('.')[2] + '.log'
    f = D / name
    ra, rf = rows(a), rows(f)
    same = all(x[1] == y[1] for x, y in zip(ra, rf))
    t = f.read_text(errors='replace')
    st = re.search(r'^SCIP Status\s*: (.*)$', t, re.M).group(1)
    cpu = re.search(r'^Solving Time \(sec\)\s*: (\S+)', t, re.M).group(1)
    print(f'{name}: attempt rows {len(ra)} all repeated in retry: {same}; CPU at last attempt row: attempt {ra[-1][0]} s, retry {rf[len(ra) - 1][0]} s; final {st}, {cpu} s')
