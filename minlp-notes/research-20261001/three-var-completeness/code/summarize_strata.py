"""Summarize a stratum enumeration run (deduplicated by type key).
usage: python summarize_strata.py TAGPATTERN   e.g. '_dense*' or ''"""
import glob
import json
import sys

pat = sys.argv[1] if len(sys.argv) > 1 else ''
recs = {}
for f in sorted(glob.glob(f'../logs/stratum_enum{pat}_[0-9].jsonl')):
    for ln in open(f):
        r = json.loads(ln)
        recs[r['key']] = r
rs = list(recs.values())
print('types', len(rs), 'generic', sum(r['total'] == 9 for r in rs), 'determinantal', sum(r['total'] == 10 for r in rs))
for key in ['kernels', 'nonneg', 'interesting', 'tested_d3', 'notd3', 'missing']:
    print(key, sum(r[key] for r in rs))
vR = [r['min_r_R'] for r in rs if r['min_r_R'] is not None]
v0 = [r['min_r_d3'] for r in rs if r['min_r_d3'] is not None]
print('min r_R %.2e' % min(vR) if vR else 'min r_R none', '| min r_d3 %.2e' % min(v0) if v0 else '')
hits = [r for r in rs if r['notd3'] > 0]
print('types with rays outside cl(D3):', len(hits))
for r in hits:
    print('  ', r['total'], r['config'], 'nonneg', r['nonneg'], 'tested', r['tested_d3'], 'notd3', r['notd3'], 'minR %.1e' % r['min_r_R'])
fam_types = [r for r in rs if r['total'] == 10 and r['config'] == "(((-1, 0, 0), ()), ((-1, 0, 1), ()), ((-1, 1, 0), ()), ((0, -1, 1), ()), ((0, 1, -1), ()))"]
for r in fam_types:
    print('five-edge family stratum: kernels', r['kernels'], 'nonneg', r['nonneg'], 'notd3', r['notd3'])
sc = {}
for r in rs:
    for k, v in r['signclass_counts'].items():
        sc[k] = sc.get(k, 0) + v
print('sign classes of nonnegative kernels', sc)
print('types with a nonnegative kernel', sum(r['nonneg'] > 0 for r in rs), '| with a tested kernel', sum(r['interesting'] > 0 for r in rs))
