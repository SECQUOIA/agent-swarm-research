import json, sys, numpy as np
recs = [json.loads(l) for l in open(sys.argv[1] if len(sys.argv) > 1 else '../logs/n3_selective.jsonl')]
print('objectives:', len(recs))
for kind in ('blocks', 'cuts'):
    rounds, counts, closed, gapleft = [], [], [], []
    for r in recs:
        h = r[kind]; last = h[-1]
        rounds.append(len(h) - 1)
        counts.append(last['blocks'] if kind == 'blocks' else last['cuts'])
        closed.append((last['bound'] - r['B']) / (r['X'] - r['B']))
        gapleft.append(r['X_safe'] - last['bound'])
    rounds, counts, closed = map(np.array, (rounds, counts, closed))
    print('%-6s rounds: median %d max %d | %s at end: median %d mean %.1f max %d | closed: min %.6f median %.6f | max(X_safe - bound) %.2e' % (
        kind, np.median(rounds), rounds.max(), kind, np.median(counts), counts.mean(), counts.max(), closed.min(), np.median(closed), max(gapleft)))
    # closure after first round
    c1 = np.array([(r[kind][1]['bound'] - r['B']) / (r['X'] - r['B']) if len(r[kind]) > 1 else 1 for r in recs])
    print('        closed after one round: median %.4f min %.4f' % (np.median(c1), c1.min()))
    nv0 = np.array([r[kind][0]['nviol'] for r in recs]); print('        violated orientations at B solution: median %d min %d max %d' % (np.median(nv0), nv0.min(), nv0.max()))
