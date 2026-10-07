"""Summary tables of the fidelity check and of z_C/z_K for SCIP's actual corners.

Inputs: logs/an_mc11.jsonl, logs/an_mc12.jsonl, logs/an_minlplib/*.jsonl (first sample),
logs/an_minlplib2/*.jsonl (second sample, if present), logs/gurobi_zk.jsonl (bounds on z_K for
records with rho >= 4, if present).

Fidelity: rays on which SCIP computed a step (t_scip present) compared with the 'fixed' model
(SCIP's formulas) and the 'note' model (the sfree note's ms_set); classes from analyze.compare.

Ratios.  For each analysed record with status ok:
  class allzero_w : every objective rate is 0 (z_K is 0 or +inf; ratio undefined);
  class zeroface  : the face of zero-rate rays meets S, so z_K = z_C = 0 (ratio undefined);
  class ratio     : z_C / z_K with
     z_C = single-cut bound of SCIP's set from SCIP's own steps if every ray has one (generated cuts),
           else from the validated model ('fixed'; failed attempts and monoidal rays);
     z_K exact (rho <= 2), by 3-ray KKT (rho = 3), or for rho >= 4 the smaller of the support-<=2
           value and Gurobi's solver-reported incumbent; with Gurobi's reported best bound the
           ratio has a reported bracket, 'gurobi' if within 1e-4 relative. These solver reports
           are numerical estimates, not certificates (see note.md, Section 5).
Reported: n, mean, quartiles, fractions < 0.9, < 0.5, >= 1 - 1e-6; per record and instance-weighted
(each instance weight 1 split over its records).
Usage: python3 summarize.py
"""
import os, sys, json, glob, collections
import numpy as np
L = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../logs')


def load(paths):
    R = []
    for p in paths:
        for l in open(p):
            r = json.loads(l)
            if 'sampling' in r or 'counters' in r or 'nlhdlrstats' in r:
                continue
            R.append(r)
    return R


def rclass(r):
    if r['wmax'] <= 0:
        return 'allzero_w'
    if r.get('zeroface_meets_S'):
        return 'zeroface'
    return 'ratio'


GUR = {}
if os.path.exists(os.path.join(L, 'gurobi_zk.jsonl')):
    for l in open(os.path.join(L, 'gurobi_zk.jsonl')):
        g = json.loads(l); GUR[(g['inst'], g['k'])] = g


def ratio_of(r):
    zc = r['zC_scip'] if r['zC_scip'] is not None else r['zC_fixed']
    src = 'scip' if r['zC_scip'] is not None else 'model'
    zk = r['zK']; kind = r['zK_kind']
    lo = None
    if kind == 'upper' and (r['inst'], r['k']) in GUR:
        g = GUR[(r['inst'], r['k'])]
        if g.get('obj') is not None:
            zk = min(zk, g['obj'])                       # solver-reported incumbent
        if g.get('bound') is not None and g['bound'] > 0:
            lo = min(g['bound'], zk)                     # solver-reported bracket, not a certificate
            kind = 'gurobi' if zk - lo <= 1e-4 * zk else 'bracket'
    if zc is None or zk is None or not np.isfinite(zk) or zk <= 0:
        return None
    rat = zc / zk
    rat_hi = zc / lo if lo else None
    return dict(r=rat, r_hi=rat_hi, src=src, kind=kind)


def stats(vals, weights=None):
    v = np.array(vals, float)
    if v.size == 0:
        return 'n 0'
    w = np.ones_like(v) if weights is None else np.array(weights, float)
    w = w / w.sum()
    o = np.argsort(v); cw = np.cumsum(w[o])
    q = lambda p: float(v[o][np.searchsorted(cw, p)])
    return ('n %d  mean %.3f  q25 %.3f  median %.3f  q75 %.3f  <0.9 %.3f  <0.5 %.3f  >=1-1e-6 %.3f  >1+1e-6 %d'
            % (v.size, float(np.sum(w * v)), q(0.25), q(0.5), q(0.75), float(np.sum(w * (v < 0.9))),
               float(np.sum(w * (v < 0.5))), float(np.sum(w * (v >= 1 - 1e-6))), int(np.sum(v > 1 + 1e-6))))


def fidelity(R, name):
    print('== fidelity', name)
    ok = [r for r in R if r.get('status') == 'ok']
    for var in ('fixed', 'note'):
        tot = collections.Counter(); by = collections.defaultdict(collections.Counter)
        for r in ok:
            c = {k: v for k, v in r['cmp_' + var].items() if k != 'na'}
            tot.update(c)
            by[(r['case_scip'], 'kappa=0' if r['kappa'] == 0 else 'kappa!=0')].update(c)
        print('  %-5s all: %s' % (var, dict(tot)))
        for k in sorted(by):
            print('        case %s %-8s %s' % (k[0], k[1], dict(by[k])))
    print('  records', len(ok), ' case agreement SCIP vs python:', sum(r['case_scip'] == r['case_py'] for r in ok), 'of', len(ok))
    print('  max rel |t_scip - t_fixed| in records without diff rays (all compared rays match): %.3g'
          % max((r['maxrelall_fixed'] for r in ok if 'diff' not in r['cmp_fixed']), default=0))
    print('  max rel |t_scip - t_fixed| over diff rays: %.3g' % max((r['maxrel_fixed'] for r in ok), default=0))
    cc = [r['coef_vs_inv_t'] for r in ok if r.get('coef_vs_inv_t') is not None]
    print('  max rel |coef - 1/t| (non-monoidal rays): %.3g over %d records' % (max(cc, default=0), len(cc)))


def ratios(R, name, inst_weight=False, subset=None):
    ok = [r for r in R if r.get('status') == 'ok']
    if subset:
        ok = [r for r in ok if subset(r)]
    cl = collections.Counter(rclass(r) for r in ok)
    rr = [(r, ratio_of(r)) for r in ok if rclass(r) == 'ratio']
    rr = [(r, x) for r, x in rr if x is not None]
    print('== ratios', name, ' records', len(ok), ' classes', dict(cl))
    if not rr:
        return
    print('   z_C source', dict(collections.Counter(x['src'] for _, x in rr)), ' z_K kind', dict(collections.Counter(x['kind'] for _, x in rr)))
    vals = [x['r'] for _, x in rr]
    print('   per record          ', stats(vals))
    if inst_weight:
        cnt = collections.Counter(r['inst'] for r, _ in rr)
        print('   instance-weighted   ', stats(vals, [1.0 / cnt[r['inst']] for r, _ in rr]), ' instances', len(cnt))
    ex = [x['r'] for _, x in rr if x['kind'] in ('exact', 'kkt3', 'gurobi')]
    print('   z_K exact/kkt3/gurobi', stats(ex))
    up = [(x['r'], x['r_hi']) for _, x in rr if x['kind'] in ('upper', 'bracket')]
    if up:
        print('   z_K only bounded: %d records; ratio lower bounds %s' % (len(up), stats([a for a, _ in up])))
        hi = [b for _, b in up if b is not None]
        if hi:
            print('      with Gurobi lower bound on z_K, ratio upper bounds', stats(hi))
    mono = [x['r'] for r, x in rr if r.get('nmono', 0) > 0]
    if mono:
        print('   records with monoidal coefficients: %d (ratio of the plain set reported)' % len(mono))
    return rr


def main():
    mc11 = load([os.path.join(L, 'an_mc11.jsonl')]); mc12 = load([os.path.join(L, 'an_mc12.jsonl')])
    m1 = load(sorted(glob.glob(os.path.join(L, 'an_minlplib', '*.jsonl'))))
    m2 = load(sorted(glob.glob(os.path.join(L, 'an_minlplib2', '*.jsonl'))))
    for R, n in ((mc11, 'mc11'), (mc12, 'mc12'), (m1 + m2, 'minlplib (both samples)')):
        fidelity(R, n)
    print()
    for R, n in ((mc11, 'mc11 all attempts'), (mc12, 'mc12 all attempts')):
        ratios(R, n, inst_weight=True)
    # earlier-note-comparable subset: per instance, first LP with an attempt, most violated expression
    for R, n in ((mc11, 'mc11 first LP, most violated'), (mc12, 'mc12 first LP, most violated')):
        best = {}
        for r in R:
            if r.get('status') != 'ok':
                continue
            key = r['inst']
            if key not in best or (r['lp'], -r['viol_scip']) < (best[key]['lp'], -best[key]['viol_scip']):
                best[key] = r
        ratios(list(best.values()), n)
    for R, n in ((mc11, 'mc11 depth > 0'), (mc12, 'mc12 depth > 0')):
        ratios(R, n, subset=lambda r: r['depth'] > 0)
    ratios(m1, 'minlplib first sample (50/instance)', inst_weight=True)
    if m2:
        ratios(m1 + m2, 'minlplib both samples', inst_weight=True)
        ratios(m1 + m2, 'minlplib both samples, generated cuts only', inst_weight=True, subset=lambda r: r.get('gen') == 1)
        ratios(m1 + m2, 'minlplib both samples, failed attempts (model z_C)', inst_weight=True, subset=lambda r: r.get('gen') != 1)
    # theory check: violated side with n_+ = 0 has a convex complement, so z_C = z_K must hold
    chk = [ratio_of(r) for r in m1 + m2 if r.get('status') == 'ok' and rclass(r) == 'ratio' and r['npos'] == 0]
    chk = [x for x in chk if x is not None]
    print('\n== check n_+ = 0 (MINLPLib): records %d, ratio within 1e-6 of 1: %d'
          % (len(chk), sum(abs(x['r'] - 1) <= 1e-6 for x in chk)))
    # per-instance table (MINLPLib)
    print('\n== MINLPLib per instance (both samples): analysed, classes, ratio median / min / frac<0.9, zK kinds')
    byi = collections.defaultdict(list)
    for r in m1 + m2:
        if r.get('status') == 'ok':
            byi[r['inst']].append(r)
    for i in sorted(byi):
        X = byi[i]; c = collections.Counter(rclass(r) for r in X)
        rv = [ratio_of(r) for r in X if rclass(r) == 'ratio']
        rv = [x for x in rv if x is not None]
        v = np.array([x['r'] for x in rv])
        kinds = dict(collections.Counter(x['kind'] for x in rv))
        print('  %-28s %4d  zeroface %4d allzero %3d ratio %4d' % (i, len(X), c['zeroface'], c['allzero_w'], c['ratio']),
              ('  med %.3f min %.3f <0.9 %.2f %s' % (np.median(v), v.min(), np.mean(v < 0.9), kinds)) if v.size else '')


if __name__ == '__main__':
    main()
