"""Reviewer check: dynamism-abort shares by case and per instance, from the stream's dump index
(logs/index/minlplib__*.jsonl; index fields are copied from the dumps), and the distribution of the
dynamism ratio min/max(|A|,|B|,|C|) for sampled failures (analysis fields fail_minabc/fail_maxabc)."""
import json, glob, os, collections
import numpy as np
L = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../logs')
byc = collections.defaultdict(collections.Counter); byi = collections.defaultdict(collections.Counter)
for f in glob.glob(os.path.join(L, 'index', 'minlplib__*.jsonl')):
    for l in open(f):
        r = json.loads(l)
        if 'outcome' not in r:
            continue
        dyn = r['outcome'] == 'fail:numerics'
        byc[r.get('case')]['n'] += 1; byc[r.get('case')]['dyn'] += dyn
        byi[r['inst']]['n'] += 1; byi[r['inst']]['dyn'] += dyn
for c in sorted(byc, key=str):
    print('case', c, 'attempts', byc[c]['n'], 'dyn', byc[c]['dyn'], 'share %.3f' % (byc[c]['dyn'] / byc[c]['n']))
print('instances with dyn share > 0.5:', sum(v['dyn'] > 0.5 * v['n'] for v in byi.values()), 'of', len(byi))
# sampled failures
rat = []; piece = collections.Counter()
for f in glob.glob(os.path.join(L, 'an_minlplib', '*.jsonl')) + glob.glob(os.path.join(L, 'an_minlplib2', '*.jsonl')):
    for l in open(f):
        r = json.loads(l)
        if r.get('fail') != 'numerics' or 'fail_dynratio' not in r:
            continue
        d = r['fail_dynratio']
        p = '1234a' if d and d[0] >= 1e15 else '4b'
        piece[p] += 1
        if p == '1234a':
            rat.append(r['fail_minabc'] / r['fail_maxabc'])
rat = np.array(rat)
print('sampled dyn failures by piece', dict(piece))
print('min/max |A,B,C| on piece 1-3/4a: quantiles 10/50/90%:', np.quantile(rat, [.1, .5, .9]))
for thr in (1e-30, 1e-25, 1e-20, 1e-17, 1e-15):
    print('  fraction with min/max < %.0e: %.3f' % (thr, np.mean(rat < thr)))
