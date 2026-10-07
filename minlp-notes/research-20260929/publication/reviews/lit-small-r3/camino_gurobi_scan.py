"""Reviewer check (round 3): classify CAMINO Gurobi runs by early stop and bound = objective."""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[4])

import csv, json
src = (_PUBLIC_REPO + '/research-20260929/publication/literature/small/sources/eg/camino_benchmark/')
lim = json.load(open(src + 'wall_time_noncvx_sbmiqp.json'))['noncvx_sbmiqp.calc_time']
eq, neq, huge, failed, late = [], [], [], [], 0
for r in csv.DictReader(open(src + 'noncvx_gurobi.csv')):
    name = r['path'][:-4]
    try:
        obj, bd, t = float(r['obj']), float(r['dual_obj']), float(r['calc_time'])
    except ValueError:
        failed.append((name, r['dual_obj'])); continue
    if t >= 0.99 * lim[name]:
        late += 1; continue
    if abs(bd) >= 1e99: huge.append(name)
    elif bd == obj: eq.append(name)
    else: neq.append(name)
print('early, bound == obj:', len(eq)); print('early, finite bound != obj:', len(neq))
print('early, |bound| >= 1e99:', huge); print('failed:', failed); print('at limit:', late)
print('eg in eq:', [n for n in eq if n.startswith('eg_')])
