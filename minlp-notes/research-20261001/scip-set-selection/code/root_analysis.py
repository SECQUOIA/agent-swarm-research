"""Careful analysis of the root benchmark (logs/root*.json from parse_logs.py).

Usage: python3 root_analysis.py ROOT.json [ROOTSEEDS.json] > OUT.md

Definitions (minimization; signs flipped for maximization instances):
  ref      MINLPLib reference value (=opt= or =best=, sources/minlplib.solu)
  RGC(X)   root gap closed = (db_X - firstlp_X) / (ref - firstlp_X), db_X = root "Final Dual Bound";
           computed when |ref - firstlp| > 1e-6 max(1, |ref|)
  D(X,Y)   RGC(X) - RGC(Y) on the same instance
  "complete" instances: every setting finished the root without hitting the time limit and without error.
  invalid-bound check: db_X better than ref by more than 1e-6 max(1,|ref|) with ref tagged =opt=.
Paired differences are tested with a two-sided Wilcoxon signed-rank test (scipy), zero differences dropped.
"""
import sys, os, json, csv
from collections import defaultdict
import numpy as np
from scipy.stats import wilcoxon

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', 'sources')
SETS = ['off', 'scip', 'corner', 'eff', 'scipS', 'cornerS', 'effS']


def load_ref():
    ref, tag = {}, {}
    for line in open(os.path.join(SRC, 'minlplib.solu')):
        p = line.split()
        if len(p) >= 3 and p[0] in ('=opt=', '=best='):
            ref[p[1]] = float(p[2]); tag[p[1]] = p[0]
    sense = {x['name']: x['objsense'] for x in csv.DictReader(open(os.path.join(SRC, 'instancedata.csv')), delimiter=';')}
    return ref, tag, sense


def rgc(r, ref, sgn):
    if r is None or r.get('rootdual') is None or r.get('firstlp') is None:
        return None
    den = sgn * (ref - r['firstlp'])
    if abs(den) <= 1e-6 * max(1.0, abs(ref)):
        return None
    return sgn * (r['rootdual'] - r['firstlp']) / den


def tl_hit(r):
    return r is None or r.get('status') is None or 'time limit' in r['status'] or r.get('error') \
        or r.get('returncode') not in ('0',)


def main():
    ref, tag, sense = load_ref()
    R = defaultdict(lambda: defaultdict(dict))
    for f in sys.argv[1:]:
        for r in json.load(open(f)):
            R[r['inst']][r['setting']][r['seed']] = r
    seeds = sorted({sd for i in R for s in R[i] for sd in R[i][s]})
    out = []
    P = print
    # invalid-bound check
    bad = []
    for i in R:
        if i not in ref:
            continue
        sgn = -1.0 if sense.get(i) == 'max' else 1.0
        for s in R[i]:
            for sd, r in R[i][s].items():
                if r.get('rootdual') is None:
                    continue
                if sgn * (r['rootdual'] - ref[i]) > 1e-6 * max(1.0, abs(ref[i])):
                    bad.append((i, s, sd, r['rootdual'], ref[i], tag[i], r.get('status')))
    P('### Root dual bounds better than the MINLPLib reference\n')
    if bad:
        P('| instance | setting | seed | root dual | ref | tag | status |'); P('|---|---|---|---|---|---|---|')
        for b in sorted(bad):
            P('| %s | %s | %s | %.10g | %.10g | %s | %s |' % b)
    else:
        P('None.')
    insts = sorted(i for i in R if i in ref)
    for sd in seeds:
        sets = [s for s in SETS if any(sd in R[i].get(s, {}) for i in insts)]
        if len(sets) < 2:
            continue
        complete = [i for i in insts if all(not tl_hit(R[i].get(s, {}).get(sd)) for s in sets)]
        P('\n### Seed %d: settings %s\n' % (sd, ', '.join(sets)))
        P('Instances: %d with a root run; %d complete (no time limit or error in any setting).\n' % (len(insts), len(complete)))
        g = {s: {} for s in sets}
        for i in complete:
            sgn = -1.0 if sense.get(i) == 'max' else 1.0
            for s in sets:
                v = rgc(R[i][s][sd], ref[i], sgn)
                if v is not None:
                    g[s][i] = v
        common = [i for i in complete if all(i in g[s] for s in sets)]
        P('| setting | n | mean RGC | median RGC | mean root CPU s | sgm root CPU s (shift 1) | cuts gen. (sum) | cuts in LP at root (sum) | select time (sum s) | intercut time (sum s) |')
        P('|---|---|---|---|---|---|---|---|---|---|')
        for s in sets:
            v = np.array([g[s][i] for i in common])
            t = np.array([R[i][s][sd]['time'] for i in common])
            gen = sum(R[i][s][sd].get('gencuts') or 0 for i in common)
            app = sum(R[i][s][sd].get('rootapplied') or 0 for i in common)
            st = sum(R[i][s][sd].get('seltime') or 0 for i in common)
            it = sum(R[i][s][sd].get('intercuttime') or 0 for i in common)
            P('| %s | %d | %.4f | %.4f | %.2f | %.2f | %d | %d | %.1f | %.1f |' % (
                s, len(v), v.mean(), np.median(v), t.mean(), np.exp(np.log(t + 1).mean()) - 1, gen, app, st, it))
        P('\nPaired differences D(X,Y) of RGC on the %d common complete instances:\n' % len(common))
        P('| X vs Y | mean D | median D | X better by > 0.01 | X worse by > 0.01 | Wilcoxon p (two-sided) |')
        P('|---|---|---|---|---|---|')
        pairs = [('scip', 'off'), ('corner', 'off'), ('eff', 'off'), ('corner', 'scip'), ('eff', 'scip'), ('eff', 'corner'),
                 ('scipS', 'scip'), ('cornerS', 'scipS'), ('effS', 'scipS')]
        for a, b in pairs:
            if a not in sets or b not in sets:
                continue
            d = np.array([g[a][i] - g[b][i] for i in common])
            nz = d[np.abs(d) > 1e-9]
            p = wilcoxon(nz).pvalue if len(nz) >= 10 else float('nan')
            P('| %s vs %s | %+.4f | %+.4f | %d | %d | %.3g |' % (a, b, d.mean(), np.median(d), (d > 0.01).sum(), (d < -0.01).sum(), p))
    # seed noise: same setting, different seeds
    if len(seeds) > 1:
        P('\n### Seed variation of RGC (same setting, different permutation seeds)\n')
        P('| setting | seeds | n | mean abs diff | diff > 0.01 (either sign) |')
        P('|---|---|---|---|---|')
        for s in SETS:
            for a in seeds:
                for b in seeds:
                    if b <= a:
                        continue
                    d = []
                    for i in insts:
                        ra, rb = R[i].get(s, {}).get(a), R[i].get(s, {}).get(b)
                        if tl_hit(ra) or tl_hit(rb):
                            continue
                        sgn = -1.0 if sense.get(i) == 'max' else 1.0
                        va, vb = rgc(ra, ref[i], sgn), rgc(rb, ref[i], sgn)
                        if va is not None and vb is not None:
                            d.append(va - vb)
                    if d:
                        d = np.array(d)
                        P('| %s | %d vs %d | %d | %.4f | %d |' % (s, a, b, len(d), np.abs(d).mean(), (np.abs(d) > 0.01).sum()))


if __name__ == '__main__':
    main()
