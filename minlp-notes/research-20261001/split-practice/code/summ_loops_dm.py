"""Compare the de Meijer loop alone ('cut' stage of exp_points.py) with
dmfam (+ {0,+-1} splits, |supp| <= 3) and dmplus (+ exact normalised general
splits) on the open instances.  Gap = (best known - bound)/|best known|."""
import glob, json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
opt = {json.loads(l)['name']: json.loads(l) for l in open(os.path.join(ROOT, 'logs/opt_gurobi.jsonl'))}
pts = {}
for f in glob.glob(os.path.join(ROOT, 'logs/points_*.jsonl')):
    for l in open(f):
        d = json.loads(l)
        if d.get('stage') in ('cut', 'root'):
            pts.setdefault(d['name'], {})[d['stage']] = d
res = {}
for m in ('dmfam', 'dmplus'):
    p = os.path.join(ROOT, f'logs/loop_{m}_open.jsonl')
    if os.path.exists(p):
        for l in open(p):
            r = json.loads(l)
            if 'name' in r:
                res.setdefault(r['name'], {})[m] = r
print('instance | Gurobi status | root gap % | after dM families | + |supp|<=3 splits (rounds, stop, s) | + general splits (rounds, stop, s) | final rank dmplus')
for nm in open(os.path.join(ROOT, 'logs/open_gap.txt')).read().split():
    o = opt[nm]['best']
    g = lambda b: 100 * (o - b) / abs(o)
    row = [nm, opt[nm]['status'], f"{g(pts[nm]['root']['obj']):.3f}", f"{g(pts[nm]['cut']['obj']):.4f}"]
    for m in ('dmfam', 'dmplus'):
        r = res.get(nm, {}).get(m)
        row.append('-' if r is None else f"{g(r['final']):.4f} ({r['rounds']}, {r.get('stopped')}, {r['time']:.0f})")
    r = res.get(nm, {}).get('dmplus')
    row.append('-' if r is None else r['final_rank']['1e-05'])
    print(' | '.join(map(str, row)))
