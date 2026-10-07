"""Review r2: stock full-solve final dual bounds and optima vs MINLPLib references (objective sense from instancedata.csv)."""
import csv, re
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
rows = list(csv.DictReader((BASE / 'sources/instancedata.csv').open(), delimiter=';'))
sense = {r['name']: r['objsense'] for r in rows}
solu = {}
for l in (BASE / 'sources/minlplib.solu').read_text().splitlines():
    f = l.split()
    if len(f) >= 3 and f[0] in ('=opt=', '=best='):
        solu[f[1]] = (f[0], float(f[2]))
n = 0
for p in sorted((BASE / 'logs/full_stock').glob('*.log')):
    t = p.read_text(errors='replace')
    inst = p.name.split('.')[0]
    d = float(re.search(r'^Dual Bound\s*: (\S+)', t, re.M).group(1))
    pr = float(re.search(r'^Primal Bound\s*: (\S+)', t, re.M).group(1))
    st = re.search(r'^SCIP Status\s*: (.*)$', t, re.M).group(1)
    if inst not in solu:
        continue
    n += 1
    kind, z = solu[inst]
    tol = 1e-6 * max(1, abs(z))
    mx = sense[inst].startswith('max')
    if (d < z - tol) if mx else (d > z + tol):
        print('DUAL EXCLUDES', p.name, d, z)
    if 'optimal' in st and kind == '=opt=' and abs(pr - z) > tol:
        print('optimum differs', p.name, pr, z, pr - z)
print('checked', n, 'stock logs with a reference; senses', {sense[p.name.split(".")[0]] for p in (BASE / "logs/full_stock").glob("*.log")})
