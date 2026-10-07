"""Summarise r2-logs/dyn_recompute.jsonl. Usage: python3 -B dyn_summary.py IN.jsonl"""
import gzip
import json
import sys
from collections import Counter

import numpy as np

rows = [json.loads(l) for l in (gzip.open(sys.argv[1], 'rt') if sys.argv[1].endswith('.gz') else open(sys.argv[1]))]
dyn = [r for r in rows if r['kind'] == 'dyn']
print('records with fail=numerics', len(rows), '; not dynamism (no nbadray increment)',
      sum(r['kind'] != 'dyn' for r in rows))


def dist(label, rs):
    for piece in ('1-3/4a', '4b'):
        v = np.array([r['ratio'] for r in rs if r['piece'] == piece])
        if not len(v):
            continue
        q = np.quantile(v, [.1, .5, .9])
        print(f'{label} piece {piece}: n={len(v)} q10/50/90 = {q[0]:.8e} {q[1]:.8e} {q[2]:.8e}; '
              f'<1e-25: {int((v < 1e-25).sum())} ({(v < 1e-25).mean():.1%}); '
              f'max {v.max():.3e}')


print('\n== all dynamism aborts in the dumps (full population) ==')
print('n', len(dyn))
dist('all', dyn)
s = [r for r in dyn if r['sampled']]
print('\n== sampled aborts ==')
print('n', len(s), 'lp/cons/fail_ray match analysis:', sum(r['match_lp_cons'] for r in s))
dist('sampled', s)
print('recomputed A,B,C max relative diff to dumped:', max(r['recomp_maxrel'] for r in s),
      '; tiny pattern identical in', sum(r['recomp_tiny_same'] for r in s), '/', len(s))

f = [r for r in s if r['piece'] == '1-3/4a']
print('\n== which entry is tiny (sampled, first piece) ==')
print(Counter(r['tiny'] for r in f))
K = np.array([r['K_needed'] for r in f])
print('\n== forward-error consistency: tiny entry <= K*u*(absolute evaluation) ==')
for k in (4, 16, 64, 256, 4500):
    print(f'K={k}: {int((K <= k).sum())}/{len(K)} ({(K <= k).mean():.1%})')
print('K quantiles 50/90/99/max', np.quantile(K, [.5, .9, .99]), K.max())
print('by tiny pattern, share with K<=64:')
for pat, n in Counter(r['tiny'] for r in f).most_common():
    sub = [r for r in f if r['tiny'] == pat]
    print(' ', pat, n, sum(r['K_needed'] <= 64 for r in sub))
# reviewer/author-style test: all negative-eigenspace components within 1e-12 of scale
rv = [r for r in f if r['neg_max_rel'] <= 1e-12 and (not r['case4'] or r.get('w_rel', 0) <= 1e-12)]
print('\nall neg-eigenspace components (and w(ray) in Case 4) <= 1e-12 of their scale:',
      len(rv), '/', len(f), f'({len(rv) / len(f):.1%})')
big = sorted(f, key=lambda r: -r['K_needed'])[:8]
print('largest K:')
for r in big:
    print(' ', r['inst'], r['k'], r['tiny'], f"{r['K_needed']:.3g}", f"{r['ratio']:.3g}")


# Ray scaling: replacing the ray r by lam*r maps (A, B, C) to (lam^2 A, lam B, C) and leaves the
# cut unchanged. Smallest dynamism ratio min_nonzero/max reachable by rescaling the ray:
def best_rescaled(c):
    a, b, cc = (abs(x) for x in c)
    best = 0.0
    for x in np.linspace(-40, 40, 16001):        # log10(lam), step 0.005
        v = [a * 10 ** (2 * x), b * 10 ** x, cc]
        nz = [t for t in v if t != 0]
        if nz:
            best = max(best, min(nz) / max(nz))
    return best


print('\n== ray-scale dependence of the test (first piece) ==')
for label, rs in (('sampled', f), ('all', [r for r in dyn if r['piece'] == '1-3/4a'])):
    br = np.array([best_rescaled(r['coefs']) for r in rs])
    passes = int((br > 1e-15).sum())
    print(f'{label}: {passes}/{len(rs)} ({passes / len(rs):.1%}) would pass the 1e-15 test after '
          f'rescaling the ray; median best ratio {np.median(br):.3e}')
    rq = np.array([r['rayqmax'] for r in rs])
    print(f'  largest |ray entry| on quadratic vars: median {np.median(rq):.3e}, '
          f'<1e-6 in {int((rq < 1e-6).sum())}/{len(rs)}')
br = np.array([best_rescaled(r['coefs']) for r in f])
for pat in ('A', 'AB', 'B', 'BC', 'C'):
    m = np.array([r['tiny'] == pat for r in f])
    print(f'  sampled, tiny {pat}: {int((br[m] > 1e-15).sum())}/{int(m.sum())} pass after rescaling')
fw = np.array([r['K_needed'] <= 64 for r in f])
print('sampled first piece: pass after rescaling or tiny entry within 64u:',
      int(((br > 1e-15) | fw).sum()), '/', len(f), '; neither:', int((~(br > 1e-15) & ~fw).sum()))


def tiny_pattern(c):
    mx = max(abs(x) for x in c)
    return ''.join('ABC'[j] for j in range(3) if c[j] != 0 and abs(c[j]) <= 1e-15 * mx)


print('\n== tiny-entry pattern, all first-piece aborts in the dumps ==')
allf = [r for r in dyn if r['piece'] == '1-3/4a']
cnt = Counter(tiny_pattern(r['coefs']) for r in allf)
print({k: f'{v} ({v / len(allf):.1%})' for k, v in cnt.most_common()})
print('sampled, tiny A only and not within 64u (A computed without cancellation):',
      sum(r['tiny'] == 'A' and r['K_needed'] > 64 for r in f), '/', len(f))
