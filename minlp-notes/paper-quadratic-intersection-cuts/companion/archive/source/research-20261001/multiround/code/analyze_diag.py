"""Diagnostics of the reversal from diag runs of mrloop.py (records with 'cuts' and swaps).
Usage: python3 analyze_diag.py 'GLOB'
All gains are fractions of the instance's root gap z_bil - z_LP.  Round buckets:
r = 0, 1-2, 3-5, 6-10, 11-19.  Only rounds with at least one violated term are counted.
"""
import sys, glob, json, collections
import recio
import numpy as np

BUCK = [(0, 0), (1, 2), (3, 5), (6, 10), (11, 19)]
recs = collections.defaultdict(list)
for f in recio.files(sys.argv[1]):
    for line in recio.lines(f):
        r = json.loads(line)
        recs[r['rule']].append(r)
rules = list(recs)
print('rules:', rules, ' instances per rule:', {k: len(v) for k, v in recs.items()})


def bucket(r):
    for i, (a, b) in enumerate(BUCK):
        if a <= r <= b:
            return i
    return None


def fmt(v):
    return '   -  ' if v is None or (isinstance(v, float) and np.isnan(v)) else '%6.3f' % v


def table(title, fn, rule_list=rules):
    print('\n' + title)
    print('%-9s ' % 'rule' + ' '.join('%7s' % ('r%d-%d' % b if b[0] != b[1] else 'r%d' % b[0]) for b in BUCK))
    for k in rule_list:
        vals = [fn(k, i) for i in range(len(BUCK))]
        print('%-9s ' % k + ' '.join(' ' + fmt(v) for v in vals))


# ---------------------------------------------------------------- round-level
RD = {k: [[] for _ in BUCK] for k in rules}
for k in rules:
    for rec in recs[k]:
        gap = rec['zbil'] - rec['zlp']
        rds = rec['rounds']
        for t, ri in enumerate(rds):
            b = bucket(ri['r'])
            if b is None:
                continue
            nxt = rds[t + 1]['z'] if t + 1 < len(rds) else None
            RD[k][b].append(dict(ri, gap=gap, nxt=nxt))


def mean_of(key, f=lambda x: x):
    def g(k, b):
        v = [f(d[key]) for d in RD[k][b] if d.get(key) is not None]
        return float(np.mean(v)) if v else None
    return g


def med_of(key):
    def g(k, b):
        v = [d[key] for d in RD[k][b] if d.get(key) is not None and np.isfinite(d[key])]
        return float(np.median(v)) if v else None
    return g


table('Number of rounds counted (rounds with violated terms)', lambda k, b: float(len(RD[k][b])))
table('Fraction of rounds whose vertex has a zero reduced cost (w_j <= 1e-9 max(1, max w))',
      mean_of('nzero', lambda x: float(x > 0)))
table('Fraction of rounds with a near-zero reduced cost (w_j <= 1e-6 max(1, max w))',
      mean_of('nnear', lambda x: float(x > 0)))
table('Mean number of near-zero reduced costs per vertex', mean_of('nnear'))
table('Median pointedness gamma of the basis cone', med_of('gamma'))
table('Mean number of cuts per round', mean_of('ncuts'))
table('Mean cut rows in the basis', mean_of('ncutrows_in_basis'))


def gain(key):
    def g(k, b):
        v = [(d[key] - d['z']) / d['gap'] for d in RD[k][b] if d.get(key) is not None]
        return float(np.mean(v)) if v else None
    return g


table('Mean round gain from the same state: SCIP-rule round', gain('swap_scip'))
table('Mean round gain from the same state: orbit-rule round', gain('swap_orbit'))


def swapwin(k, b):
    v = [((d['swap_scip'] - d['swap_orbit']) / d['gap']) for d in RD[k][b] if d.get('swap_scip') is not None]
    return float(np.mean([x > 1e-3 for x in v])) if v else None


def swaplose(k, b):
    v = [((d['swap_scip'] - d['swap_orbit']) / d['gap']) for d in RD[k][b] if d.get('swap_scip') is not None]
    return float(np.mean([x < -1e-3 for x in v])) if v else None


table('Fraction of states where the SCIP round gains more than the orbit round by > 0.001 gap', swapwin)
table('Fraction of states where the orbit round gains more than the SCIP round by > 0.001 gap', swaplose)

# ---------------------------------------------------------------- cut-level
CU = collections.defaultdict(lambda: [[] for _ in BUCK])
for k in rules:
    for rec in recs[k]:
        gap = rec['zbil'] - rec['zlp']
        zr = {ri['r']: ri for ri in rec['rounds']}
        for c in rec.get('cuts', []):
            b = bucket(c['r'])
            if b is None:
                continue
            key = k if k != 'both' else 'both:' + c['set']
            CU[key][b].append(dict(c, gap=gap, round=zr.get(c['r'])))
ckeys = sorted(CU)


def cmean(fn):
    def g(k, b):
        v = [fn(c) for c in CU[k][b]]
        v = [x for x in v if x is not None and np.isfinite(x)]
        return float(np.mean(v)) if v else None
    return g


def cmed(fn):
    def g(k, b):
        v = [fn(c) for c in CU[k][b]]
        v = [x for x in v if x is not None and np.isfinite(x)]
        return float(np.median(v)) if v else None
    return g


table('Mean |cos| between cut normal and objective (1 = objective-parallel)', cmean(lambda c: abs(c['cosobj'])), ckeys)
table('Mean max |cos| with cuts of the same round', cmean(lambda c: c['maxcos_round']), ckeys)
table('Fraction of cuts with max |cos| > 0.99 to an earlier cut of the same round',
      cmean(lambda c: float(c['maxcos_round'] > 0.99)), ckeys)
table('Mean max |cos| with cuts of earlier rounds', cmean(lambda c: c['maxcos_prev']), ckeys)
table('Mean single-cut LP gain (fraction of gap)', cmean(lambda c: c['gain_single'] / c['gap'] if c.get('gain_single') is not None else None), ckeys)
table('Median depth dist(xbar, K cap cut)', cmed(lambda c: c['depth']), ckeys)
table('Median efficacy', cmed(lambda c: c['eff']), ckeys)
table('Mean z_C / z_K of the chosen set (floored w)', cmean(lambda c: min(c['zC'] / c['zk'], 1.0) if c['zk'] > 0 and np.isfinite(c['zk']) else None), ckeys)
table('Mean z_C / z_K of SCIP set at the same corner', cmean(lambda c: min(c['zC_scip'] / c['zk'], 1.0) if c.get('zC_scip') is not None and c['zk'] > 0 and np.isfinite(c['zk']) else None), ckeys)


def steps(c, sel):
    if 'a_scip' not in c:
        return None
    a = np.array(c['a']); s = np.array(c['a_scip']); w = np.array(c['w'])
    m = sel(w) & (a > 0) & (s > 0)
    if not m.any():
        return None
    return float(np.median(np.log10(s[m] / a[m])))   # log10(alpha_rule / alpha_scip)


table('Median log10(alpha_rule/alpha_scip), rays with normalized w_j <= 1e-3 (cheap rays)',
      cmean(lambda c: steps(c, lambda w: w <= 1e-3)), ckeys)
table('Median log10(alpha_rule/alpha_scip), rays with 1e-3 < w_j <= 0.1',
      cmean(lambda c: steps(c, lambda w: (w > 1e-3) & (w <= 0.1))), ckeys)
table('Median log10(alpha_rule/alpha_scip), rays with w_j > 0.1 (expensive rays)',
      cmean(lambda c: steps(c, lambda w: w > 0.1)), ckeys)


def shortfrac(c, sel):
    if 'a_scip' not in c:
        return None
    a = np.array(c['a']); s = np.array(c['a_scip']); w = np.array(c['w'])
    m = sel(w) & (s > 0)
    if not m.any():
        return None
    return float(np.mean(a[m] > 2 * s[m]))     # alpha_rule < alpha_scip / 2


table('Fraction of expensive rays (w_j > 0.1) where alpha_rule < alpha_scip/2',
      cmean(lambda c: shortfrac(c, lambda w: w > 0.1)), ckeys)
table('Fraction of cheap rays (w_j <= 1e-3) where alpha_rule < alpha_scip/2',
      cmean(lambda c: shortfrac(c, lambda w: w <= 1e-3)), ckeys)

# complementarity: round gain / max single gain
def compl(k, b):
    out = []
    for rec in recs[k]:
        gap = rec['zbil'] - rec['zlp']
        rds = rec['rounds']
        for t, ri in enumerate(rds[:-1]):
            if bucket(ri['r']) != b:
                continue
            gs = [c['gain_single'] for c in rec['cuts'] if c['r'] == ri['r'] and c.get('gain_single') is not None]
            if not gs or max(gs) <= 1e-9 * gap:
                continue
            out.append((rds[t + 1]['z'] - ri['z']) / max(gs))
    return float(np.median(out)) if out else None


table('Median (round gain) / (largest single-cut gain in the round)', compl)

# depth relative to the violation (the convergence theorem needs depth >= eta(violation))
table('Median minstep / violation (minstep = min_j alpha_j ||r_j||)',
      cmed(lambda c: c['minstep'] / c['viol'] if c.get('viol') and np.isfinite(c.get('minstep', np.inf)) else None), ckeys)
table('10% quantile of minstep / violation',
      lambda k, b: (lambda v: float(np.quantile(v, 0.1)) if v else None)(
          [c['minstep'] / c['viol'] for c in CU[k][b] if c.get('viol') and np.isfinite(c.get('minstep', np.inf))]), ckeys)
table('Median depth / violation',
      cmed(lambda c: c['depth'] / c['viol'] if c.get('viol') else None), ckeys)
table('Median violation of cut terms', cmed(lambda c: c.get('viol')), ckeys)
