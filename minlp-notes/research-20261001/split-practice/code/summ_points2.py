"""Per-set summary of the SDP points: gap closed by de Meijer et al.'s families
(stage 'cut' versus 'root'), numerical rank (eigenvalues > 1e-5 * lambda_max)
at the root and after the families, and solver status.
Optimal values: brute force (n <= 12) or logs/opt_gurobi.jsonl; when the
Gurobi run hit its time limit, the best of its incumbent and the integral
rank-1 SDP point is used (so gaps are upper bounds on the true gaps)."""
import json, os, collections, statistics as st
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
opt = {json.loads(l)['name']: json.loads(l) for l in open(os.path.join(ROOT, 'logs/opt_gurobi.jsonl'))}
print('set | inst | Gurobi timelimit | root rank (min/med/max) | SDP gap % mean | closed by families: all / mean % | rank after families (min/med/max) | inaccurate status (root, cut)')
for s in ['BT10', 'BT20', 'BT30', 'BT50', 'DM30', 'DM60']:
    by = collections.defaultdict(dict)
    for l in open(os.path.join(ROOT, f'logs/points_{s}.jsonl')):
        d = json.loads(l)
        if 'stage' in d:
            by[d['name']][d['stage']] = d
    rr, rc, gaps, cls, nclosed, tl, inacc = [], [], [], [], 0, 0, [0, 0]
    for nm, d in by.items():
        r, c = d['root'], d['cut']
        if r['opt'] is not None:
            o = r['opt']
        else:
            o = opt[nm]['best']
            if opt[nm]['status'] != 'optimal':
                tl += 1
        if c['rank']['1e-05'] == 1:
            family = 'BT' if s.startswith('BT') else 'DM'
            with np.load(os.path.join(ROOT, f'data/points_{s}/{nm}__{family}__cut.npz')) as point:
                x = point['Y'][0, 1:]
                xi = np.round(x)
                if (np.max(np.abs(x - xi)) < 1e-3 and np.max(np.abs(xi)) <= 1
                        and (not bool(point['linear']) or xi.sum() == 0)):
                    # Use a feasible integer objective, not the SDP lower bound.
                    o = min(o, float(xi @ point['Q'] @ xi + point['c'] @ xi))
        rr.append(r['rank']['1e-05']); rc.append(c['rank']['1e-05'])
        gaps.append(100 * (o - r['obj']) / abs(o))
        cl = 100 * (c['obj'] - r['obj']) / (o - r['obj']) if o - r['obj'] > 1e-9 else 100.0
        cls.append(min(cl, 100.0)); nclosed += (o - c['obj']) <= 1e-4 * abs(o)
        inacc[0] += r['status'] != 'optimal'; inacc[1] += c['status'] != 'optimal'
    f = lambda L: f'{min(L)}/{st.median(L):g}/{max(L)}'
    print(s, '|', len(by), '|', tl, '|', f(rr), '|', round(st.mean(gaps), 2), '|', nclosed, '/', round(st.mean(cls), 1),
          '|', f(rc), '|', inacc)
