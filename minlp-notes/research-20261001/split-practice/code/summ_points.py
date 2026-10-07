"""Summarise logs/points_*.jsonl: ranks (eigenvalues > t * lambda_max) by stage."""
import json, sys, collections, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for s in sys.argv[1:]:
    rows = [json.loads(l) for l in open(os.path.join(ROOT, 'logs', f'points_{s}.jsonl'))]
    by = collections.defaultdict(dict)
    for r in rows:
        if 'stage' in r: by[r['name']][r['stage']] = r
    print(f'== {s}: {len(by)} instances')
    for st in ('root', 'cut', 'cut_trace', 'cut_rand'):
        for t in ('0.001', '1e-05', '1e-07'):
            c = collections.Counter(d[st]['rank'][t] for d in by.values() if st in d and 'rank' in d[st])
            print(f'  {st:9s} rank@{t:6s}', dict(sorted(c.items())))
    r1 = sum(1 for d in by.values() if d['cut']['rank']['1e-05'] == 1)
    print('  final cut points of rank 1 (at 1e-5):', r1)
    for nm, d in sorted(by.items()):
        c = d['cut']
        if c['rank']['1e-05'] > 1:
            print('   ', nm, 'root', round(d['root']['obj'], 4), 'cut', round(c['obj'], 4), 'rk', c['rank'],
                  'trace-rk', d.get('cut_trace', {}).get('rank'), 'rounds', c['rounds'], 'ncuts', c['ncuts'],
                  'eig', [round(x, 5) for x in c['eig'][:8]])
