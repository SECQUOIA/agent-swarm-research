"""Review r2, item m5: exact single-ray tests on zero-rate rays of the low-ratio records.

No stream code is imported. Selection of the 371 table records with ratio < 0.5 is
reimplemented from the definition in summarize.ratio_of (analysis rows + logs/gurobi_zk.jsonl).
For each selected record the raw dump is read and, in exact rational arithmetic on the dumped
floats, q(s + t p) = q0 + L t + M t^2 is formed for every non-fixed ray p with rate w <= 1e-9 max w.
The ray reaches S = {q <= 0} for some t > 0 iff M < 0, or M = 0 and L < 0, or M > 0, L < 0 and
L^2 >= 4 M q0. Also reports |L| relative to the sum of absolute values of its terms.
For generated cuts the determining ray j* = argmin max(w, floor) * t_SCIP is computed as well.

Usage: python3 -B zero_rate_exact.py
"""
import gzip
import json
import math
from collections import Counter, defaultdict
from fractions import Fraction as F
from multiprocessing import Pool
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LOGS = ROOT / 'logs'

GUR = {}
for line in open(LOGS / 'gurobi_zk.jsonl'):
    g = json.loads(line)
    GUR[(g['inst'], g['k'])] = g


def ratio(r):
    zc = r['zC_scip'] if r['zC_scip'] is not None else r['zC_fixed']
    zk = r['zK']
    if r['zK_kind'] == 'upper' and (r['inst'], r['k']) in GUR:
        g = GUR[(r['inst'], r['k'])]
        if g.get('obj') is not None:
            zk = min(zk, g['obj'])
    if zc is None or zk is None or not math.isfinite(zk) or zk <= 0:
        return None
    return zc / zk


def select():
    sel = defaultdict(dict)
    n_table = 0
    for d in ('an_minlplib', 'an_minlplib2'):
        for p in sorted((LOGS / d).glob('*.jsonl')):
            for line in p.open():
                r = json.loads(line)
                if 'k' not in r or r.get('status') != 'ok' or r['wmax'] <= 0 or r.get('zeroface_meets_S'):
                    continue
                q = ratio(r)
                if q is None:
                    continue
                n_table += 1
                if q < 0.5:
                    sel[r['inst']][r['k']] = (d, r)
    return sel, n_table


def exact_quadratic(rec):
    nq, nl = rec['nquad'], rec['nlin']
    aux = rec['auxvar'] is not None
    nv = nq + nl + (1 if aux else 0)
    sf = -1 if rec['over'] else 1
    Q = defaultdict(F)
    for i, a in enumerate(rec['qsqr']):
        if a:
            Q[(i, i)] += sf * F(a)
    for i, j, a in rec['bilin']:
        Q[(i, j)] += sf * F(a) / 2
        Q[(j, i)] += sf * F(a) / 2
    b = [F(0)] * nv
    for i, v in enumerate(rec['qlin']):
        b[i] = sf * F(v)
    for i, v in enumerate(rec['lincoefs']):
        b[nq + i] = sf * F(v)
    if aux:
        b[-1] = F(-sf)
        c = sf * F(rec['constant'])
    else:
        c = (F(rec['constant']) - F(rec['rhs'])) if sf > 0 else (F(rec['lhs']) - F(rec['constant']))
    return {k: v for k, v in Q.items() if v != 0}, b, c, nv


def rates(rec):
    w = []
    for st, lp, rt in zip(rec['raystat'], rec['raylppos'], rec['rayrate']):
        w.append(-rt if st == 2 else rt)   # SCIP_BASESTAT_UPPER = 2
    return w


def work(job):
    inst, recs = job
    out = []
    last = max(recs)
    k = -1
    with gzip.open(LOGS / 'runs_minlplib' / (inst + '.jsonl.gz'), 'rt') as f:
        for line in f:
            if not line.startswith('{"v":'):
                continue
            k += 1
            if k > last:
                break
            if k not in recs:
                continue
            rec = json.loads(line)
            r = recs[k][1]
            assert rec['lp'] == r['lp'] and rec['cons'] == r['cons']
            Q, b, c, nv = exact_quadratic(rec)
            s = [F(x) for x in rec['zlp']]
            q0 = sum(s[i] * v * s[j] for (i, j), v in Q.items()) + sum(bi * si for bi, si in zip(b, s)) + c
            g = [F(0)] * nv                          # gradient 2 Q s + b
            for (i, j), v in Q.items():
                g[i] += 2 * v * s[j]
            g = [gi + bi for gi, bi in zip(g, b)]
            gabs = [0.0] * nv
            for (i, j), v in Q.items():
                gabs[i] += abs(2 * float(v) * rec['zlp'][j])
            gabs = [ga + abs(float(bi)) for ga, bi in zip(gabs, b)]
            width = rec.get('raywidth')
            keep = [not (width is not None and width[j] <= 1e-9) for j in range(rec['nrays'])]
            w = rates(rec)
            wmax = max(wj for wj, kp in zip(w, keep) if kp)
            floor = 1e-9 * wmax
            reach = []
            nzero = 0
            for j in range(rec['nrays']):
                if not keep[j] or w[j] > floor:
                    continue
                nzero += 1
                p = dict((i, F(v)) for i, v in rec['rays'][j])
                L = sum(g[i] * v for i, v in p.items())
                M = sum(p.get(i, 0) * v * p.get(jj, 0) for (i, jj), v in Q.items())
                hit = M < 0 or (M == 0 and L < 0) or (M > 0 and L < 0 and L * L >= 4 * M * q0)
                if hit:
                    lscale = sum(gabs[i] * abs(float(v)) for i, v in p.items())
                    reach.append({'ray': j, 'M': float(M), 'L': float(L), 'L_rel': abs(float(L)) / lscale
                                  if lscale else None, 'raw_rate': w[j]})
            jstar = None
            if r['zC_scip'] is not None:
                best = math.inf
                for e in rec['perray']:
                    if e.get('fail') or not keep[e['i']]:
                        continue
                    t = e['t']
                    if t is None or t >= 1e20 or t < 0:
                        continue
                    v = max(w[e['i']], floor) * t
                    if v < best:
                        best, jstar = v, e['i']
            out.append({'inst': inst, 'k': k, 'q0': float(q0), 'nzero': nzero, 'reach': reach,
                        'jstar': jstar, 'jstar_zero': (jstar is not None and w[jstar] <= floor),
                        'jstar_reaches': any(x['ray'] == jstar for x in reach) if jstar is not None else None})
    return out


def main():
    sel, n_table = select()
    print('table ratio records', n_table, '; ratio < 0.5:', sum(map(len, sel.values())))
    jobs = sorted(sel.items(), key=lambda x: -len(x[1]))
    res = []
    with Pool(4) as pool:
        for o in pool.imap_unordered(work, jobs):
            res.extend(o)
    res.sort(key=lambda x: (x['inst'], x['k']))
    with open(ROOT / 'reviews/r2-logs/zero_rate_exact.jsonl', 'w') as f:
        for x in res:
            f.write(json.dumps(x) + '\n')
    anyhit = [x for x in res if x['reach']]
    print('records with at least one zero-rate ray reaching S exactly (single ray):', len(anyhit))
    for x in anyhit:
        print('  ', x['inst'], x['k'], 'jstar', x['jstar'], 'jstar zero-rate', x['jstar_zero'],
              [(h['ray'], h['M'], h['L'], h['L_rel'], h['raw_rate']) for h in x['reach']])
    gen = [x for x in res if x['jstar'] is not None]
    print('generated-cut records', len(gen), '; j* zero-rate', sum(x['jstar_zero'] for x in gen),
          '; j* zero-rate and reaching S exactly', sum(bool(x['jstar_reaches']) for x in gen))
    print('records by instance with exact zero-rate hit:', Counter(x['inst'] for x in anyhit))


if __name__ == '__main__':
    main()
