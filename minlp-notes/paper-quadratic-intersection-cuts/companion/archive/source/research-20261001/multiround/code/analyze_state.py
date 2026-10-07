"""State-quality diagnostics of the reversal (diag records of mrloop.py with swap data).
Usage: python3 analyze_state.py 'GLOB'
For each rule's own trajectory and round bucket:
  own rate      (z_{r+1} - z_r) / (z_bil - z_r): fraction of the remaining gap closed by the round
  SCIP rate     same for one SCIP-rule round from the same state (swap counterfactual)
  orbit rate    same for one orbit-rule round from the same state
  potential     max over violated terms of z_K / (z_bil - z_r) (best single-cut gain of the most
                promising term, as a fraction of the remaining gap; <= 1 up to the w floor)
  tiny w        mean fraction of nonbasic directions with normalized reduced cost <= 1e-3
  repeat        fraction of cuts on a term that was also cut in the previous round
Only states with remaining gap > 1e-3 of the root gap are counted.  Means with a 95% t-interval
for the SCIP rate (the state-difficulty measure)."""
import sys, glob, json, collections
import recio
import numpy as np
from scipy import stats

BUCK = [(0, 0), (1, 2), (3, 5), (6, 10), (11, 19)]
recs = collections.defaultdict(list)
for f in recio.files(sys.argv[1]):
    for line in recio.lines(f):
        r = json.loads(line)
        recs[r['rule']].append(r)


def bucket(r):
    return [i for i, (a, z) in enumerate(BUCK) if a <= r <= z][0]


def ci(v):
    v = np.asarray(v, float)
    if len(v) < 2:
        return '%.4f' % (v.mean() if len(v) else np.nan)
    h = stats.t.ppf(0.975, len(v) - 1) * v.std(ddof=1) / np.sqrt(len(v))
    return '%.4f [%.4f,%.4f]' % (v.mean(), v.mean() - h, v.mean() + h)


for rule, L in recs.items():
    print('== states on the %s trajectory (%d instances)' % (rule, len(L)))
    D = [collections.defaultdict(list) for _ in BUCK]
    for rec in L:
        zbil, zlp = rec['zbil'], rec['zlp']; gap = zbil - zlp; c = rec['closed']
        cuts_by_r = collections.defaultdict(list)
        for cu in rec.get('cuts', []):
            cuts_by_r[cu['r']].append(cu)
        for x in rec['rounds']:
            r = x['r']; rem = zbil - x['z']
            if rem <= 1e-3 * gap or r + 1 >= len(c):
                continue
            b = bucket(r); d = D[b]
            d['own'].append((c[r + 1] - c[r]) * gap / rem)
            if 'swap_scip' in x and x['swap_scip'] is not None:
                d['scip'].append((x['swap_scip'] - x['z']) / rem)
            if 'swap_orbit' in x and x['swap_orbit'] is not None:
                d['orbit'].append((x['swap_orbit'] - x['z']) / rem)
            cs = cuts_by_r[r]
            zks = [cu['zk'] for cu in cs if cu.get('zk') is not None and np.isfinite(cu['zk'])]
            if zks:
                d['pot'].append(min(max(zks) / rem, 2.0))
            ws = [np.mean(np.array(cu['w']) <= 1e-3) for cu in cs if 'w' in cu]
            if ws:
                d['tiny'].append(np.mean(ws))
            prev = {cu['e'] for cu in cuts_by_r.get(r - 1, [])}
            if r > 0 and cs:
                d['rep'].append(np.mean([cu['e'] in prev for cu in cs]))
    print('%-7s %5s  %-26s %-26s %-26s %-8s %-8s %-8s' % ('rounds', 'n', 'own rate', 'SCIP-round rate', 'orbit-round rate', 'potent.', 'tiny w', 'repeat'))
    for b, d in enumerate(D):
        if not d['own']:
            continue
        print('r%-6s %5d  %-26s %-26s %-26s %-8.3f %-8.3f %-8.3f' % (
            '%d-%d' % BUCK[b], len(d['own']), ci(d['own']), ci(d['scip']), ci(d['orbit']),
            np.median(d['pot']) if d['pot'] else np.nan, np.mean(d['tiny']) if d['tiny'] else np.nan,
            np.mean(d['rep']) if d['rep'] else np.nan))


# ---------------------------------------------------------------------------------------------
# Paired by instance: for each instance and bucket, average a state metric over the states of
# each trajectory (remaining gap > 1e-3), then compare rule - scip across instances that have
# states in that bucket on both trajectories (95% t-interval; Wilcoxon signed-rank p).
def per_inst(rec):
    zbil, zlp = rec['zbil'], rec['zlp']; gap = zbil - zlp
    cuts_by_r = collections.defaultdict(list)
    for cu in rec.get('cuts', []):
        cuts_by_r[cu['r']].append(cu)
    out = [collections.defaultdict(list) for _ in BUCK]
    for x in rec['rounds']:
        r = x['r']; rem = zbil - x['z']
        if rem <= 1e-3 * gap or r == 0:
            continue
        d = out[bucket(r)]
        if x.get('swap_scip') is not None:
            d['scip_rate'].append((x['swap_scip'] - x['z']) / rem)
        if x.get('swap_orbit') is not None:
            d['orbit_rate'].append((x['swap_orbit'] - x['z']) / rem)
        zks = [cu['zk'] for cu in cuts_by_r[r] if cu.get('zk') is not None and np.isfinite(cu['zk'])]
        if zks:
            d['potential'].append(min(max(zks) / rem, 2.0))
        ws = [np.mean(np.array(cu['w']) <= 1e-3) for cu in cuts_by_r[r] if 'w' in cu]
        if ws:
            d['tiny_w'].append(np.mean(ws))
        if x.get('gamma') is not None:
            d['log10_gamma'].append(np.log10(max(x['gamma'], 1e-12)))
    return [{k: np.mean(v) for k, v in d.items()} for d in out]


print('\n== Paired by instance: (state metric on rule trajectory) - (same on scip trajectory)')
S = {rec['inst']: per_inst(rec) for rec in recs['scip']}
for rule in recs:
    if rule == 'scip':
        continue
    O = {rec['inst']: per_inst(rec) for rec in recs[rule]}
    print('rule %s' % rule)
    for key in ('scip_rate', 'orbit_rate', 'potential', 'tiny_w', 'log10_gamma'):
        cells = []
        for b in range(1, len(BUCK)):
            d = [O[i][b][key] - S[i][b][key] for i in O if i in S and key in O[i][b] and key in S[i][b]]
            if len(d) < 3:
                cells.append('   -   ')
                continue
            d = np.array(d); h = stats.t.ppf(0.975, len(d) - 1) * d.std(ddof=1) / np.sqrt(len(d))
            p = stats.wilcoxon(d).pvalue if np.any(d != 0) else 1.0
            cells.append('r%d-%d n=%d %+.4f [%+.4f,%+.4f] p=%.2g' % (BUCK[b] + (len(d), d.mean(), d.mean() - h, d.mean() + h, p)))
        print('  %-11s ' % key + ' | '.join(cells))
