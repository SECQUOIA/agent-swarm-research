"""Reviewer r3: independent recomputation of the new material of the revision after review round 2.
Reads the raw jsonl(.gz) records directly (no stream code).
 1. Recovery table of note Section 3.5 (d(20)-d(3), d(20)-d(10) per rule, 6x8 and 10x20, pooled o5s).
 2. Contrast: does the deficit shrink more under later SCIP rounds (oKs) than under continued orbit
    rounds?  (rule - orbit)(20) - (rule - orbit)(3), paired.
 3. Section 3.6 table on 6x8: share of rays where the chosen step alpha = 1/a is shorter than SCIP's,
    mean log10 ratio, loss after round 10, Spearman of rounds-0..4 share with the loss; and the 10x20
    within-rule Spearman range.
 4. Consistency of the rev2 trajectories with the main-run trajectories.
Usage (from this directory): python3 indep_rev2.py"""
import glob, gzip, json, collections, math
import numpy as np
from scipy import stats

L = '../../logs/'


def recs(pat):
    fs = sorted(set(glob.glob(L + pat)) | set(glob.glob(L + pat + '.gz')))
    fs = [f for f in fs if not (f.endswith('.gz') and f[:-3] in fs)]
    assert fs, pat
    for f in fs:
        op = gzip.open if f.endswith('.gz') else open
        with op(f, 'rt') as h:
            for ln in h:
                yield f, json.loads(ln)


def tci(d):
    d = np.asarray(d, float); n = len(d)
    h = stats.t.ppf(0.975, n - 1) * d.std(ddof=1) / math.sqrt(n)
    return '%+.4f [%+.4f, %+.4f] p %.3g (n %d)' % (d.mean(), d.mean() - h, d.mean() + h,
                                                  stats.ttest_1samp(d, 0).pvalue, n)


# ---- main trajectories
C = collections.defaultdict(dict)
for size in ('4x4', '6x8', '8x12', '10x20'):
    for pat in ('main/main_%s_*.jsonl', 'new/new_%s_*.jsonl', 'rev1/rev1_%s_*.jsonl', 'rev1/rev1b_%s_*.jsonl'):
        if not (glob.glob(L + pat % size) or glob.glob(L + pat % size + '.gz')):
            continue
        for f, r in recs(pat % size):
            if 'smoke' in f:
                continue
            assert r['status'] == 'ok'
            k = (size, r['inst'])
            c = np.array(r['closed'])
            if k in C[r['rule']]:
                assert np.array_equal(C[r['rule']][k], c), (f, r['rule'], k)
            C[r['rule']][k] = c

print('== 1. recovery table')
RULES = ('first_orbit', 'o2s', 'o3s', 'o5s', 'orbit')
for sizes in (('6x8',), ('10x20',), ('6x8', '10x20')):
    keys = sorted(k for k in C['scip'] if k[0] in sizes)
    print('--', sizes, len(keys))
    for ru in RULES:
        d = lambda r: np.array([C[ru][k][r] - C['scip'][k][r] for k in keys])
        print('  %-11s d20-d3 %s | d20-d10 %s' % (ru, tci(d(20) - d(3)), tci(d(20) - d(10))))
    print('  contrast vs orbit, (rule-orbit)(20) - (rule-orbit)(3):')
    for ru in RULES[:4]:
        e = lambda r: np.array([C[ru][k][r] - C['orbit'][k][r] for k in keys])
        print('    %-11s %s   [(rule-orbit) at r3 %+.4f, r20 %+.4f]' % (ru, tci(e(20) - e(3)), e(3).mean(), e(20).mean()))
    # ceiling: remaining gap of SCIP at r3 and r20
    print('  mean SCIP remaining gap r3 %.4f r10 %.4f r20 %.4f' % tuple(
        np.mean([1 - C['scip'][k][r] for k in keys]) for r in (3, 10, 20)))

# ---- diag
print('\n== 3. shorter-steps table (6x8)')
D = collections.defaultdict(dict)
for pat in ('diag/diag_6x8_*.jsonl', 'rev2/diag2_6x8_*.jsonl'):
    for f, r in recs(pat):
        assert r['status'] == 'ok'
        D[r['rule']][r['inst']] = r


def cutvals(c):
    if 'a_scip' not in c:
        return None
    a = np.array(c['a'], float); s = np.array(c['a_scip'], float)
    with np.errstate(divide='ignore'):
        al = np.where(a > 0, 1 / np.where(a > 0, a, 1), np.inf)
        asc = np.where(s > 0, 1 / np.where(s > 0, s, 1), np.inf)
    fin = np.isfinite(al) | np.isfinite(asc)
    if not fin.any():
        return None
    sh = float(np.mean(al[fin] < asc[fin] * (1 - 1e-9)))
    both = np.isfinite(al) & np.isfinite(asc)
    mlr = float(np.mean(np.log10(al[both] / asc[both]))) if both.any() else None
    return sh, mlr


BU = [(0, 0), (1, 2), (3, 5), (6, 10), (11, 19)]
S = D['scip']
pinst = {}
for ru in ('orbit', 'orbit_core', 'orbitB', 'pert0.1', 'pertE0.1', 'pertE1', 'lex0.1', 'geo', 'alt'):
    sh = [[] for _ in BU]; ml = [[] for _ in BU]
    for rec in D[ru].values():
        for c in rec['cuts']:
            v = cutvals(c)
            if v is None:
                continue
            for b, (lo, hi) in enumerate(BU):
                if lo <= c['r'] <= hi:
                    sh[b].append(v[0])
                    if v[1] is not None:
                        ml[b].append(v[1])
    ids = sorted(set(D[ru]) & set(S))
    loss = np.array([D[ru][i]['closed'][10] - S[i]['closed'][10] for i in ids])
    feat = []
    for i in ids:
        vv = [cutvals(c) for c in D[ru][i]['cuts'] if c['r'] <= 4]
        vv = [x[0] for x in vv if x is not None]
        feat.append(np.mean(vv))
    rho, p = stats.spearmanr(feat, loss)
    pinst[ru] = p
    shm = [np.mean(x) for x in sh]; mlm = [np.mean(x) for x in ml]
    print('  %-10s shorter %.3f-%.3f  mlr %+.3f..%+.3f  loss %+.4f (n %d)  spearman %+.3f p %.3g' % (
        ru, min(shm), max(shm), max(mlm), min(mlm), loss.mean(), len(ids), rho, p))
ps = sorted(pinst.values())
print('  Holm-adjusted smallest p over 9 rules: %.3f' % min(1, 9 * ps[0]))

print('\n   10x20 within-rule Spearman (shorter, rounds 0-4) vs loss after round 10')
D2 = collections.defaultdict(dict)
for f, r in recs('diag/diag_10x20_*.jsonl'):
    D2[r['rule']][r['inst']] = r
for ru in ('orbit', 'pertE0.1', 'geo'):
    ids = sorted(set(D2[ru]) & set(D2['scip']))
    loss = [D2[ru][i]['closed'][10] - D2['scip'][i]['closed'][10] for i in ids]
    feat = []
    for i in ids:
        vv = [cutvals(c) for c in D2[ru][i]['cuts'] if c['r'] <= 4]
        feat.append(np.mean([x[0] for x in vv if x is not None]))
    rho, p = stats.spearmanr(feat, loss)
    print('  %-10s n %d spearman %+.3f p %.3g' % (ru, len(ids), rho, p))

print('\n== 4. rev2 trajectories vs main runs (6x8)')
nd = npair = 0
for ru, M in D.items():
    for i, r in M.items():
        k = ('6x8', i)
        if k in C.get(ru, {}):
            npair += 1
            nd += int(not np.array_equal(C[ru][k], np.array(r['closed'])))
print('  pairs %d differing %d' % (npair, nd))
