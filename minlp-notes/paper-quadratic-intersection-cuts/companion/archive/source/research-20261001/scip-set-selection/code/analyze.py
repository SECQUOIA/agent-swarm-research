"""Analysis of the root and full-solve benchmarks.

Usage: python3 analyze.py ROOT.json FULL.json OUT.md [OUT.json]
  ROOT.json, FULL.json : outputs of parse_logs.py (root runs: limits/nodes = 1; full runs)
Writes markdown tables (per-instance and aggregated) and a JSON summary.

Definitions
  ref       best known objective value from MINLPLib (minlplib.solu, =opt= or =best=)
  root gap closed by setting X relative to cuts off:
            gc(X) = (db_X - db_off) / (ref - db_off) for minimization (signs flipped for maximization),
            computed only when |ref - db_off| > 1e-6 max(1, |ref|)
  shifted geometric mean with shift s: exp(mean(log(v + s))) - s  (time s = 1 sec CPU, nodes s = 100)
  unsolved runs enter time means with the time limit and node means with their node count; runs that failed
  without statistics (LP solver error) count as unsolved at the time limit and are left out of node means.
"""
import sys, os, json, math, csv
from collections import defaultdict
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', 'sources')


def load_ref():
    ref, tag = {}, {}
    for line in open(os.path.join(SRC, 'minlplib.solu')):
        p = line.split()
        if len(p) >= 3 and p[0] in ('=opt=', '=best='):
            ref[p[1]] = float(p[2]); tag[p[1]] = p[0]
        elif len(p) >= 2 and p[0] == '=inf=':
            ref[p[1]] = None; tag[p[1]] = '=inf='
    sense = {}
    for x in csv.DictReader(open(os.path.join(SRC, 'instancedata.csv')), delimiter=';'):
        sense[x['name']] = x['objsense']
    return ref, tag, sense


def sgm(v, s):
    v = np.asarray(v, float)
    return float(np.exp(np.mean(np.log(v + s))) - s) if len(v) else float('nan')


def solved(r):
    return r.get('status') is not None and 'optimal solution found' in r['status']


def main():
    rootf, fullf, outmd = sys.argv[1:4]
    outjson = sys.argv[4] if len(sys.argv) > 4 else None
    ref, tag, sense = load_ref()
    root = json.load(open(rootf)) if os.path.exists(rootf) else []
    full = json.load(open(fullf)) if fullf != '-' and os.path.exists(fullf) else []
    L = []
    summary = {}

    # ---------------- root ----------------
    R = defaultdict(dict)
    for r in root:
        R[r['inst']][r['setting']] = r
    settings_root = [s for s in ['off', 'scip', 'corner', 'eff', 'scipS', 'cornerS', 'effS']
                     if any(s in R[i] for i in R)]
    insts = sorted(R)
    L.append('## Root node (limits/nodes = 1, seed 0)\n')
    L.append('Root dual bound and gap closed relative to cuts off; gc = (db_X - db_off)/(ref - db_off).\n')
    hdr = '| instance | ref | db off | ' + ' | '.join('gc %s' % s for s in settings_root if s != 'off') + \
          ' | ' + ' | '.join('cuts %s (appl.)' % s for s in settings_root if s != 'off') + ' |'
    L.append(hdr)
    L.append('|' + '---|' * (3 + 2 * (len(settings_root) - 1)))
    gcs = defaultdict(list)
    better = defaultdict(lambda: [0, 0])
    seltime = defaultdict(list); ictime = defaultdict(list); rtime = defaultdict(list)
    for i in insts:
        off = R[i].get('off')
        if off is None or off.get('rootdual') is None or i not in ref or ref[i] is None:
            continue
        mx = sense.get(i) == 'max'
        sgn = -1.0 if mx else 1.0
        den = sgn * (ref[i] - off['rootdual'])
        row = '| %s | %.6g | %.6g |' % (i, ref[i], off['rootdual'])
        cells_gc, cells_cuts = [], []
        for s in settings_root:
            if s == 'off':
                continue
            r = R[i].get(s)
            if r is None or r.get('rootdual') is None:
                cells_gc.append(' - '); cells_cuts.append(' - ')
                continue
            if abs(den) > 1e-6 * max(1.0, abs(ref[i])):
                g = sgn * (r['rootdual'] - off['rootdual']) / den
                gcs[s].append(g)
                cells_gc.append(' %.3f ' % g)
            else:
                cells_gc.append(' (closed) ')
            cells_cuts.append(' %s (%s) ' % (r.get('gencuts'), r.get('rootapplied')))
            if r.get('seltime') is not None:
                seltime[s].append(r['seltime']); ictime[s].append(r['intercuttime'])
            if r.get('time') is not None:
                rtime[s].append(r['time'])
        L.append(row + '|'.join(cells_gc) + '|' + '|'.join(cells_cuts) + '|')
    L.append('')
    L.append('| setting | n | mean gc | median gc | gc > 0.01 | gc < -0.01 | mean root CPU time | sgm root time (s=1) | total intercut time | total select time |')
    L.append('|---|---|---|---|---|---|---|---|---|---|')
    for s in settings_root:
        if s == 'off':
            if rtime.get('off') is None:
                rtime['off'] = [R[i]['off']['time'] for i in insts if 'off' in R[i] and R[i]['off'].get('time') is not None]
            L.append('| off | %d | 0 | 0 | - | - | %.2f | %.2f | - | - |' % (len(rtime['off']), np.mean(rtime['off']), sgm(rtime['off'], 1)))
            continue
        v = np.array(gcs[s])
        L.append('| %s | %d | %.4f | %.4f | %d | %d | %.2f | %.2f | %.1f | %.1f |' % (
            s, len(v), v.mean() if len(v) else float('nan'), np.median(v) if len(v) else float('nan'),
            int((v > 0.01).sum()), int((v < -0.01).sum()), np.mean(rtime[s]) if rtime[s] else float('nan'),
            sgm(rtime[s], 1) if rtime[s] else float('nan'), sum(ictime[s]), sum(seltime[s])))
        summary['root_' + s] = dict(n=len(v), mean_gc=float(v.mean()) if len(v) else None,
                                    median_gc=float(np.median(v)) if len(v) else None,
                                    n_better=int((v > 0.01).sum()), n_worse=int((v < -0.01).sum()),
                                    intercuttime=float(sum(ictime[s])), seltime=float(sum(seltime[s])))
    # pairwise root comparison of the new rules against SCIP's rule
    L.append('')
    L.append('Pairwise root comparison (difference in gc, same instance):\n')
    L.append('| pair | n | mean diff | better by > 0.01 | worse by > 0.01 |')
    L.append('|---|---|---|---|---|')
    for a, b in [('corner', 'scip'), ('eff', 'scip'), ('cornerS', 'scipS'), ('effS', 'scipS'), ('scipS', 'scip')]:
        d = []
        for i in insts:
            off = R[i].get('off'); ra = R[i].get(a); rb = R[i].get(b)
            if None in (off, ra, rb) or i not in ref or ref[i] is None:
                continue
            if None in (off.get('rootdual'), ra.get('rootdual'), rb.get('rootdual')):
                continue
            sgn = -1.0 if sense.get(i) == 'max' else 1.0
            den = sgn * (ref[i] - off['rootdual'])
            if abs(den) <= 1e-6 * max(1.0, abs(ref[i])):
                continue
            d.append(sgn * (ra['rootdual'] - rb['rootdual']) / den)
        d = np.array(d)
        if len(d):
            L.append('| %s vs %s | %d | %.4f | %d | %d |' % (a, b, len(d), d.mean(), (d > 0.01).sum(), (d < -0.01).sum()))
            summary['rootpair_%s_%s' % (a, b)] = dict(n=len(d), mean=float(d.mean()), better=int((d > 0.01).sum()),
                                                      worse=int((d < -0.01).sum()))

    # ---------------- full ----------------
    if full:
        F = defaultdict(lambda: defaultdict(dict))
        for r in full:
            F[r['inst']][r['setting']][r['seed']] = r
        settings = [s for s in ['off', 'scip', 'corner', 'eff', 'scipS', 'cornerS', 'effS'] if any(s in F[i] for i in F)]
        seeds = sorted({r['seed'] for r in full})
        tl = max(r['time'] for r in full if r.get('time') is not None)
        L.append('\n## Full solves\n')
        L.append('Seeds: %s. Time limit (CPU s): about %.0f. Shifted geometric means over all instance-seed pairs; '
                 'unsolved runs count with the time limit.\n' % (seeds, tl))
        # consistency check of reported optimal values
        incons = []
        for i in F:
            for s in F[i]:
                for sd, r in F[i][s].items():
                    if solved(r) and i in ref and ref[i] is not None and r.get('primal') is not None:
                        tol = 1e-4 * max(1.0, abs(ref[i]))
                        if abs(r['primal'] - ref[i]) > tol:
                            incons.append((i, s, sd, r['primal'], ref[i], tag[i]))
                    if solved(r) and i in ref and ref[i] is None:
                        incons.append((i, s, sd, r.get('primal'), 'infeasible', '=inf='))
        L.append('| setting | runs | solved | errors | sgm time | sgm nodes | sgm time (all solved) | sgm nodes (all solved) | mean intercut time | mean select time | mean cuts gen. | mean cuts appl. |')
        L.append('|---|---|---|---|---|---|---|---|---|---|---|---|')
        allsolved = [(i, sd) for i in F for sd in seeds if all(sd in F[i][s] and solved(F[i][s][sd]) for s in settings)]
        for s in settings:
            rs = [F[i][s][sd] for i in F for sd in seeds if sd in F[i][s]]
            times = [r['time'] if solved(r) else tl for r in rs]     # failed runs (no statistics) count at the limit
            nodes = [r['nodes'] for r in rs if r.get('nodes') is not None]
            ta = [F[i][s][sd]['time'] for (i, sd) in allsolved]
            na = [F[i][s][sd]['nodes'] for (i, sd) in allsolved]
            ict = [r.get('intercuttime') or 0 for r in rs]; st = [r.get('seltime') or 0 for r in rs]
            gc = [r.get('gencuts') or 0 for r in rs]; ap = [r.get('applied') or 0 for r in rs]
            nerr = sum(1 for r in rs if r.get('error') or r.get('returncode') not in ('0', None))
            L.append('| %s | %d | %d | %d | %.2f | %.0f | %.2f | %.0f | %.2f | %.2f | %.1f | %.1f |' % (
                s, len(rs), sum(solved(r) for r in rs), nerr, sgm(times, 1), sgm(nodes, 100), sgm(ta, 1), sgm(na, 100),
                np.mean(ict), np.mean(st), np.mean(gc), np.mean(ap)))
            summary['full_' + s] = dict(runs=len(rs), solved=sum(solved(r) for r in rs), errors=nerr,
                                        sgm_time=sgm(times, 1), sgm_nodes=sgm(nodes, 100),
                                        sgm_time_allsolved=sgm(ta, 1), sgm_nodes_allsolved=sgm(na, 100),
                                        n_allsolved=len(allsolved))
        L.append('\n%d instance-seed pairs solved by all settings.\n' % len(allsolved))
        # per-seed shifted geometric means and seed variation
        L.append('Per-seed shifted geometric mean of CPU time (all instances, time limit for unsolved):\n')
        L.append('| setting | ' + ' | '.join('seed %d' % sd for sd in seeds) + ' |')
        L.append('|---|' + '---|' * len(seeds))
        for s in settings:
            cells = []
            for sd in seeds:
                rs = [F[i][s][sd] for i in F if sd in F[i][s]]
                cells.append('%.2f' % sgm([r['time'] if solved(r) else tl for r in rs], 1))
            L.append('| %s | %s |' % (s, ' | '.join(cells)))
        # ratio to SCIP's rule and to off, per seed, on instances solved by both
        L.append('\nTime ratios (sgm over instance-seed pairs solved by both; > 1 means the first setting is slower):\n')
        L.append('| pair | n | sgm time ratio | sgm node ratio | faster by > 10% | slower by > 10% |')
        L.append('|---|---|---|---|---|---|')
        pairs = [('scip', 'off'), ('corner', 'off'), ('eff', 'off'), ('corner', 'scip'), ('eff', 'scip'),
                 ('scipS', 'off'), ('cornerS', 'off'), ('cornerS', 'scipS'), ('scipS', 'scip')]
        # seed-noise reference: same setting, seed a vs seed b
        if len(seeds) >= 2:
            for s in settings:
                pairs.append(('%s@%d' % (s, seeds[1]), '%s@%d' % (s, seeds[0])))
        for a, b in pairs:
            ratios, nratios = [], []
            for i in F:
                for sd in seeds:
                    if '@' in a:
                        sa, sda = a.split('@'); sb, sdb = b.split('@'); sda, sdb = int(sda), int(sdb)
                        if sd != seeds[0]:
                            continue
                    else:
                        sa, sda, sb, sdb = a, sd, b, sd
                    ra = F[i].get(sa, {}).get(sda); rb = F[i].get(sb, {}).get(sdb)
                    if ra is None or rb is None or not (solved(ra) and solved(rb)):
                        continue
                    ratios.append((ra['time'] + 1) / (rb['time'] + 1))
                    nratios.append((ra['nodes'] + 100) / (rb['nodes'] + 100))
            if ratios:
                ratios = np.array(ratios); nratios = np.array(nratios)
                L.append('| %s vs %s | %d | %.3f | %.3f | %d | %d |' % (
                    a, b, len(ratios), math.exp(np.log(ratios).mean()), math.exp(np.log(nratios).mean()),
                    (ratios < 1 / 1.1).sum(), (ratios > 1.1).sum()))
                summary['ratio_%s_%s' % (a, b)] = dict(n=len(ratios), time=math.exp(np.log(ratios).mean()),
                                                      nodes=math.exp(np.log(nratios).mean()),
                                                      faster=int((ratios < 1 / 1.1).sum()),
                                                      slower=int((ratios > 1.1).sum()))
        # per-instance full table
        L.append('\n### Per-instance full-solve results (CPU s / nodes; "TL" = time limit; seeds %s)\n' % seeds)
        L.append('| instance | ' + ' | '.join(settings) + ' |')
        L.append('|---|' + '---|' * len(settings))
        for i in sorted(F):
            cells = []
            for s in settings:
                c = []
                for sd in seeds:
                    r = F[i][s].get(sd)
                    if r is None:
                        c.append('-')
                    elif solved(r):
                        c.append('%.1f/%d' % (r['time'], r['nodes']))
                    else:
                        c.append('TL(%s)' % (r.get('gap') or '?'))
                cells.append('; '.join(c))
            L.append('| %s | %s |' % (i, ' | '.join(cells)))
        L.append('\n### Reported optimal values that disagree with MINLPLib (tolerance 1e-4 relative)\n')
        if incons:
            L.append('| instance | setting | seed | SCIP value | MINLPLib | tag |')
            L.append('|---|---|---|---|---|---|')
            for t in incons:
                L.append('| %s | %s | %s | %s | %s | %s |' % t)
        else:
            L.append('None.')
        summary['inconsistencies'] = [list(map(str, t)) for t in incons]
    open(outmd, 'w').write('\n'.join(L) + '\n')
    if outjson:
        json.dump(summary, open(outjson, 'w'), indent=1)
    print('\n'.join(L[:5]))


if __name__ == '__main__':
    main()
