"""Critic check: compare the reproduction track's replays (R/publication/reproduction/water-audit)
with the stored certificates. Reads logs and JSON only; runs no solver.
usage: python3 replay_audit.py   (paths are absolute)"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[4])

import ast, gzip, json, re, collections
R = (_PUBLIC_REPO + '/research-20260929')
WA = R + '/publication/reproduction/water-audit'
for T in [6, 9, 12, 18, 24]:
    c = json.load(open(f'{R}/open-instances-wave2/waterno2/logs/cert_{T:02d}_w1_impl.json'))
    res = c['results'] if isinstance(c['results'], list) else ast.literal_eval(c['results'])
    orig = {r['t0']: r for r in res}
    log = open(f'{WA}/logs/w{T:02d}_certify.log').read()
    seen, diffs = set(), []
    for m in re.finditer(r'window (\d+)-\d+: estimate (\S+) target (\S+) certified (\S+) status (\S+) nodes (\d+)', log):
        t = int(m.group(1))
        if t in seen: continue
        seen.add(t)
        o = orig[t]
        if int(m.group(6)) != o['nodes'] or abs(float(m.group(4)) - o['bound']) > 5e-6:
            diffs.append(f'p{t}: replay est {m.group(2)} certified {m.group(4)} nodes {m.group(6)} | stored B_t {o["bound"]!r} nodes {o["nodes"]}')
    tail = [l for l in log.splitlines() if 'CERTIFIED' in l][-1]
    print(f'T={T}: stored {c["certified_bound_exact"]} | replay: {tail.strip()} | periods differing: {len(diffs)}')
    for d in diffs: print('   ', d)
rows = [json.loads(l) for l in open(f'{WA}/data/vrebound_certB_sample.jsonl')]
old = {}
for l in gzip.open(f'{R}/reviews/waterno2-cellslopes-review-checks/logs/rebound_certB_all.jsonl.gz', 'rt'):
    r = json.loads(l); old[r['key']] = r
same = sum((r['vbb2_status'], r['vbb2_bound'], r['nodes']) == (old[r['key']]['vbb2_status'], old[r['key']]['vbb2_bound'], old[r['key']]['nodes']) for r in rows)
g = collections.defaultdict(lambda: [0, 0.0, 0.0])
for r in rows:
    k = r['group']; g[k][0] += 1; g[k][1] += r['time']; g[k][2] += old[r['key']]['time']
print(f'vbb2 certB replay sample: {len(rows)} tasks, kinds {dict(collections.Counter(r["kind"] for r in rows))}, identical to review (status, bound, nodes): {same}')
for k, v in g.items(): print(f'   group {k}: {v[0]} tasks, time here {v[1]:.0f} s, review {v[2]:.0f} s, ratio {v[2]/v[1]:.2f}')
