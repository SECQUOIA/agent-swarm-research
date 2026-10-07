"""Review r1: independent recomputation of the root (Section 6) and full-solve (Section 7) tables of
scip-set-selection/note.md directly from the raw SCIP logs. Does not import any stream code.

Usage: python3 recompute.py > ../r1-logs/recompute.md
"""
import csv
import math
import os
import re
from collections import defaultdict

import numpy as np
from scipy.stats import wilcoxon

STREAM = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
LOGS = os.path.join(STREAM, 'logs')
NUM = r'([-+]?(?:\d+\.?\d*(?:[eE][-+]?\d+)?|[-+]?inf(?:inity)?))'


def num(s):
    try:
        return float(s)
    except (TypeError, ValueError):
        return None


def stat_block(txt):
    """Text after the last 'SCIP Status' line (the statistics of 'display statistics')."""
    k = txt.rfind('SCIP Status')
    return txt[k:] if k >= 0 else ''


def parse(path):
    txt = open(path, errors='replace').read()
    name = os.path.basename(path)[:-4]
    inst, setting, seed = name.rsplit('.', 2)
    st = stat_block(txt)
    r = dict(inst=inst, setting=setting, seed=int(seed[1:]))
    m = re.search(r'SCIP Status\s*:\s*(.*)', st)
    r['status'] = m.group(1).strip() if m else None

    def grab(pat, src=st):
        m = re.search(pat, src)
        return num(m.group(1)) if m else None
    # 'Solving Time' and 'Solving Nodes' are printed after the first 'SCIP Status' line, before the statistics
    k = txt.find('SCIP Status')
    head = txt[k:] if k >= 0 else ''
    r['time'] = grab(r'Solving Time \(sec\)\s*:\s*' + NUM, head)
    r['nodes'] = grab(r'Solving Nodes\s*:\s*(\d+)', head)
    r['firstlp'] = grab(r'First LP value\s*:\s*' + NUM)
    r['rootdb'] = grab(r'Final Dual Bound\s*:\s*' + NUM)
    # bounds in the "Solution" section of the statistics (last occurrences)
    sol = st[st.rfind('Solution           :'):] if 'Solution           :' in st else ''
    r['primal'] = grab(r'\n  Primal Bound\s*:\s*' + NUM, sol)
    r['dual'] = grab(r'\n  Dual Bound\s*:\s*' + NUM, sol)
    m = re.search(r'@@ wallclock \S+ returncode (\S+)', txt)
    r['rc'] = m.group(1) if m else None
    m = re.search(r'  Quadratic Nlhdlr :\s+(\d+)\s+(\d+)', st)
    r['gencuts'] = int(m.group(1)) if m else None
    m = re.search(r'  Quadratic SetSel :' + r'\s+(\S+)' * 11, st)
    if m:
        g = m.groups()
        r['seltime'] = float(g[7]); r['ictime'] = float(g[6]); r['rootappl'] = int(g[10])
        r['selcalls'] = int(g[1]); r['selchanged'] = int(g[2])
    r['errmsg'] = bool(re.search(r'^\[.*\] ERROR|^ERROR', txt, re.M))
    r['objsense_log'] = (re.search(r'Original Problem   :.*?Objective        : (\w+)', st, re.S) or [None, None])[1]
    return r


def load_ref():
    ref, tag = {}, {}
    for line in open(os.path.join(STREAM, 'sources', 'minlplib.solu')):
        p = line.split()
        if len(p) >= 3 and p[0] in ('=opt=', '=best='):
            ref[p[1]] = float(p[2]); tag[p[1]] = p[0]
    sense = {x['name']: x['objsense'] for x in
             csv.DictReader(open(os.path.join(STREAM, 'sources', 'instancedata.csv')), delimiter=';')}
    return ref, tag, sense


def sgm(v, shift):
    v = np.asarray(v, float)
    return math.exp(np.mean(np.log(v + shift))) - shift


def load_dir(d):
    return [parse(os.path.join(LOGS, d, f)) for f in sorted(os.listdir(os.path.join(LOGS, d))) if f.endswith('.log')]


def root_section(ref, tag, sense, P):
    recs = load_dir('root') + load_dir('rootseeds')
    R = defaultdict(dict)
    for r in recs:
        R[(r['inst'], r['seed'])][r['setting']] = r
    P('## Root benchmark (own parser)\n')
    P('runs: %d; return codes: %s; runs with an ERROR line: %d; statuses: %s\n' % (
        len(recs), dict(sorted(_count(r['rc'] for r in recs).items())), sum(r['errmsg'] for r in recs),
        dict(_count(r['status'] for r in recs))))
    # sense check: log objective sense vs instancedata
    mism = [(r['inst']) for r in recs if r['objsense_log'] and sense.get(r['inst']) and
            r['objsense_log'][:3] != sense[r['inst']][:3]]
    P('objective-sense mismatches between log and instancedata.csv: %d\n' % len(set(mism)))
    # validity screen
    bad = []
    for r in recs:
        i = r['inst']
        if i in ref and r['rootdb'] is not None:
            sg = -1 if sense[i] == 'max' else 1
            if sg * (r['rootdb'] - ref[i]) > 1e-6 * max(1, abs(ref[i])):
                bad.append((i, r['setting'], r['seed'], r['rootdb'], ref[i], tag[i]))
    P('root dual bounds beyond the reference by > 1e-6 max(1,|ref|): %s\n' % bad)

    def done(r):
        return r is not None and r['status'] is not None and 'time limit' not in r['status'] and r['rc'] == '0' \
            and not r['errmsg']

    def rgc(r, i):
        sg = -1 if sense[i] == 'max' else 1
        if r['rootdb'] is None or r['firstlp'] is None:
            return None
        den = sg * (ref[i] - r['firstlp'])
        if abs(den) <= 1e-6 * max(1, abs(ref[i])):
            return None
        return sg * (r['rootdb'] - r['firstlp']) / den

    insts = sorted({k[0] for k in R})
    pairs = [('scip', 'off'), ('corner', 'off'), ('eff', 'off'), ('corner', 'scip'), ('eff', 'scip'),
             ('eff', 'corner'), ('scipS', 'scip'), ('cornerS', 'scipS'), ('effS', 'scipS')]
    G = {}
    for sd in (0, 1, 2):
        sets = ['off', 'scip', 'corner', 'eff'] + (['scipS', 'cornerS', 'effS'] if sd == 0 else [])
        ran = [i for i in insts if (i, sd) in R]
        comp = [i for i in ran if all(done(R[(i, sd)].get(s)) for s in sets)]
        withref = [i for i in comp if i in ref]
        g = {s: {} for s in sets}
        flp_diff = 0
        for i in withref:
            flps = {R[(i, sd)][s]['firstlp'] for s in sets}
            if len(flps) > 1:
                flp_diff += 1
            for s in sets:
                v = rgc(R[(i, sd)][s], i)
                if v is not None:
                    g[s][i] = v
        common = [i for i in withref if all(i in g[s] for s in sets)]
        G[sd] = (g, common)
        P('### Seed %d\n' % sd)
        P('instances run: %d; complete in all settings: %d (with a reference: %d); common with RGC defined: %d; '
          'instances whose first LP value differs between settings: %d\n' % (len(ran), len(comp), len(withref),
                                                                              len(common), flp_diff))
        out_of_range = [(i, s, round(g[s][i], 4)) for s in sets for i in common if g[s][i] < -1e-6 or g[s][i] > 1 + 1e-6]
        P('RGC values outside [0,1]: %s\n' % out_of_range)
        P('| setting | n | mean RGC | median RGC | sgm CPU (shift 1) | cuts gen | root-LP cuts | select s | intercut s |')
        P('|---|---|---|---|---|---|---|---|---|')
        for s in sets:
            rr = [R[(i, sd)][s] for i in common]
            v = np.array([g[s][i] for i in common])
            P('| %s | %d | %.4f | %.4f | %.3f | %d | %d | %.1f | %.1f |' % (
                s, len(v), v.mean(), np.median(v), sgm([r['time'] for r in rr], 1),
                sum(r['gencuts'] or 0 for r in rr), sum(r.get('rootappl') or 0 for r in rr),
                sum(r.get('seltime') or 0 for r in rr), sum(r.get('ictime') or 0 for r in rr)))
        P('\n| X vs Y | n | mean D | median D | better>0.01 | worse>0.01 | Wilcoxon p (zeros dropped, |D|>1e-9) | p (zero_method=wilcox on raw D) |')
        P('|---|---|---|---|---|---|---|---|')
        for a, b in pairs:
            if a not in sets or b not in sets:
                continue
            d = np.array([g[a][i] - g[b][i] for i in common])
            nz = d[np.abs(d) > 1e-9]
            p1 = wilcoxon(nz).pvalue
            p2 = wilcoxon(d, zero_method='wilcox').pvalue
            P('| %s vs %s | %d | %+.4f | %+.4f | %d | %d | %.3g | %.3g |' % (
                a, b, len(d), d.mean(), np.median(d), (d > 0.01).sum(), (d < -0.01).sum(), p1, p2))
        P('')
    # seed-averaged corner vs scip on instances common to all three seeds (Section 8.2 "all" row)
    c3 = sorted(set(G[0][1]) & set(G[1][1]) & set(G[2][1]))
    for a, b in [('corner', 'scip'), ('eff', 'scip')]:
        d = np.array([np.mean([G[sd][0][a][i] - G[sd][0][b][i] for sd in (0, 1, 2)]) for i in c3])
        P('seed-averaged D(%s,%s) over %d instances common to all seeds: mean %+.4f, better/worse > 0.01: %d/%d, '
          'Wilcoxon p %.3g' % (a, b, len(c3), d.mean(), (d > 0.01).sum(), (d < -0.01).sum(),
                               wilcoxon(d[np.abs(d) > 1e-9]).pvalue))
    # heavy-tail check: share of the scip-vs-off mean RGC gain from the top 10% instances (seed 0)
    g, common = G[0]
    d = np.sort(np.array([g['scip'][i] - g['off'][i] for i in common]))[::-1]
    k = max(1, len(d) // 10)
    P('\nseed 0 scip vs off: top %d instances contribute %.1f%% of the total RGC gain; median %+.4f' % (
        k, 100 * d[:k].sum() / d.sum(), np.median(d)))
    # seed noise
    P('\n### Seed noise (same setting, two seeds, both complete with defined RGC)\n')
    P('| setting | seeds | n | mean abs diff | n abs diff > 0.01 |')
    P('|---|---|---|---|---|')
    for s in ['off', 'scip', 'corner', 'eff']:
        for a, b in [(0, 1), (0, 2), (1, 2)]:
            d = []
            for i in insts:
                ra, rb = R.get((i, a), {}).get(s), R.get((i, b), {}).get(s)
                if i in ref and done(ra) and done(rb):
                    va, vb = rgc(ra, i), rgc(rb, i)
                    if va is not None and vb is not None:
                        d.append(va - vb)
            d = np.abs(np.array(d))
            P('| %s | %d vs %d | %d | %.4f | %d |' % (s, a, b, len(d), d.mean(), (d > 0.01).sum()))
    P('')


def _count(it):
    c = defaultdict(int)
    for x in it:
        c[x] += 1
    return c


def full_section(ref, tag, sense, P):
    recs = load_dir('full')
    F = {(r['inst'], r['setting'], r['seed']): r for r in recs}
    sets = ['off', 'scip', 'corner', 'eff']
    insts = sorted({r['inst'] for r in recs})
    P('## Full solves (own parser)\n')
    P('runs: %d, instances %d; rc: %s; statuses: %s; runs with ERROR line: %s\n' % (
        len(recs), len(insts), dict(_count(r['rc'] for r in recs)), dict(_count(r['status'] for r in recs)),
        [(r['inst'], r['setting'], r['seed']) for r in recs if r['errmsg']]))
    nonzero = [(k, r['rc'], r['status']) for k, r in F.items() if r['rc'] != '0']
    P('nonzero return codes: %s\n' % nonzero)

    def solved(r):
        return r is not None and r['status'] == 'problem is solved [optimal solution found]' and r['rc'] == '0'

    def cpu(r):
        return min(r['time'], 300.0) if solved(r) else 300.0

    def table(keys, label):
        P('### %s\n' % label)
        P('| setting | solved/runs | CPU sgm | nodes n | nodes sgm | all-solved n | CPU sgm there | nodes sgm there |')
        P('|---|---|---|---|---|---|---|---|')
        nodekeys = [k for k in keys if all(F[(k[0], s, k[1])]['nodes'] is not None for s in sets)]
        allsolved = [k for k in keys if all(solved(F[(k[0], s, k[1])]) for s in sets)]
        for s in sets:
            rr = [F[(i, s, sd)] for i, sd in keys]
            P('| %s | %d/%d | %.3f | %d | %.1f | %d | %.3f | %.1f |' % (
                s, sum(solved(r) for r in rr), len(rr), sgm([cpu(r) for r in rr], 1), len(nodekeys),
                sgm([F[(i, s, sd)]['nodes'] for i, sd in nodekeys], 100), len(allsolved),
                sgm([F[(i, s, sd)]['time'] for i, sd in allsolved], 1),
                sgm([F[(i, s, sd)]['nodes'] for i, sd in allsolved], 100)))
        P('')
        return allsolved

    allkeys = [(i, sd) for i in insts for sd in (1, 2)]
    for sd in (1, 2):
        table([k for k in allkeys if k[1] == sd], 'seed %d' % sd)
    allsolved = table(allkeys, 'seeds 1 + 2')
    table([k for k in allkeys if k != ('ex5_4_2', 1)], 'excluding the pair ex5_4_2 seed 1')
    table([k for k in allkeys if k[0] != 'kall_congruentcircles_c52'], 'excluding kall_congruentcircles_c52')
    # solved-set differences
    P('### Solved-set differences (pairs solved by X but not Y)\n')
    for a in sets:
        for b in sets:
            if a < b or a == b:
                continue
            xa = [k for k in allkeys if solved(F[(k[0], a, k[1])]) and not solved(F[(k[0], b, k[1])])]
            xb = [k for k in allkeys if solved(F[(k[0], b, k[1])]) and not solved(F[(k[0], a, k[1])])]
            P('- %s only: %s; %s only: %s' % (a, xa, b, xb))
    P('')
    # near-limit solves
    near = sorted((round(r['time'], 2), r['inst'], r['setting'], r['seed']) for r in recs if solved(r) and r['time'] > 150)
    P('solved runs with CPU > 150 s (sensitive to the limit): %s\n' % near)
    # paired ratios and instance-averaged Wilcoxon tests
    P('### Paired comparisons (shifted ratios; Wilcoxon on instance-averaged log ratios)\n')
    P('| X vs Y | all-pair CPU ratio | p (60 inst) | common-solved CPU ratio | p | common-solved node ratio | p |')
    P('|---|---|---|---|---|---|---|')
    for a, b in [('scip', 'off'), ('corner', 'off'), ('eff', 'off'), ('corner', 'scip'), ('eff', 'scip'),
                 ('eff', 'corner')]:
        def lr(keys, f, shift):
            return {k: math.log((f(F[(k[0], a, k[1])]) + shift) / (f(F[(k[0], b, k[1])]) + shift)) for k in keys}

        def test(d):
            per = defaultdict(list)
            for (i, sd), v in d.items():
                per[i].append(v)
            x = np.array([np.mean(v) for v in per.values()])
            x = x[np.abs(x) > 1e-12]
            return wilcoxon(x).pvalue, len(per)
        d1 = lr(allkeys, cpu, 1)
        d2 = lr(allsolved, lambda r: r['time'], 1)
        d3 = lr(allsolved, lambda r: r['nodes'], 100)
        P('| %s vs %s | %.4f | %.3g | %.4f | %.3g (n=%d) | %.4f | %.3g |' % (
            a, b, math.exp(np.mean(list(d1.values()))), test(d1)[0], math.exp(np.mean(list(d2.values()))),
            test(d2)[0], test(d2)[1], math.exp(np.mean(list(d3.values()))), test(d3)[0]))
    P('')
    # reference checks
    P('### Reference checks\n')
    for r in recs:
        i = r['inst']
        if i not in ref:
            P('- no reference: %s' % i)
            continue
        sg = -1 if sense[i] == 'max' else 1
        tol = 1e-6 * max(1, abs(ref[i]))
        if r['dual'] is not None and sg * (r['dual'] - ref[i]) > tol:
            P('- dual bound excludes reference: %s %s s%d dual %.12g ref %.12g' % (i, r['setting'], r['seed'], r['dual'], ref[i]))
        if solved(r) and abs(r['primal'] - ref[i]) > tol:
            P('- reported optimum differs: %s %s s%d primal %.13g ref %.10g (%s) diff %.4g' % (
                i, r['setting'], r['seed'], r['primal'], ref[i], tag[i], r['primal'] - ref[i]))
    P('')


def main():
    ref, tag, sense = load_ref()
    out = []
    P = out.append
    root_section(ref, tag, sense, P)
    full_section(ref, tag, sense, P)
    print('\n'.join(out))


if __name__ == '__main__':
    main()
