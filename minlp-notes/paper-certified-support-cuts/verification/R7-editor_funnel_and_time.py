"""R7-editor: campaign-3 separator funnel, oracle usage and time decomposition.
Standard library only. Reads the archived v3 records; no solver is run.
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[2])

import json, collections, math
EXP = (_PUBLIC_REPO + '/paper-certified-support-cuts/experiments/')
def solved(r):
    pc = r.get('primal_check') or {}
    return r['status'] in ('optimal', 'gaplimit') and r.get('primal') is not None and pc.get('passed', pc.get('feasible', False))
def sgm(v, s=1.0):
    return math.exp(sum(math.log(x + s) for x in v) / len(v)) - s
KEYS = ['cuts', 'certification_calls', 'certification_failures', 'row_binding_rejections', 'row_rounding_rejections']
for p in ['v3/runs/partA-full', 'v3/runs/partA-root', 'v3/runs/partB', 'v3/runs/partC']:
    recs = [json.loads(l) for l in open(EXP + p + '/records.jsonl')]
    print('==', p)
    agg = collections.Counter(); rbm = collections.defaultdict(set); meth = collections.Counter()
    for r in recs:
        if r['mode'] == 'baseline': continue
        s = r.get('separation') or {}
        for k in KEYS:
            agg[(r['phase'], r['mode'], k)] += s.get(k, 0) or 0
        if s.get('row_binding_rejections'): rbm[(r['phase'], r['mode'])].add(r['name'])
        for c in r.get('cuts') or []:
            meth[(c.get('support_stats') or {}).get('method')] += 1
    for pm in sorted({k[:2] for k in agg}):
        print('  funnel', pm, {k: agg[pm + (k,)] for k in KEYS}, 'models with row-binding rejections', len(rbm[pm]))
    print('  support methods of recorded cuts', dict(meth))
    full = [r for r in recs if r['phase'] == 'full']
    if full:
        by = collections.defaultdict(dict)
        for r in full: by[(r['name'], r['seed'])][r['mode']] = r
        modes = sorted({r['mode'] for r in full})
        keys = [k for k, d in by.items() if all(m in d and solved(d[m]) for m in modes)]
        for m in modes:
            tot = [by[k][m]['total_seconds'] for k in keys]
            cb = [((by[k][m].get('separation') or {}).get('callback_seconds') or 0) for k in keys]
            print('  time', m, len(keys), 'SGM total %.3f' % sgm(tot), 'SGM total minus callback %.3f' % sgm([a - b for a, b in zip(tot, cb)]),
                  'sum nodes', sum(by[k][m].get('nodes') or 0 for k in keys))
