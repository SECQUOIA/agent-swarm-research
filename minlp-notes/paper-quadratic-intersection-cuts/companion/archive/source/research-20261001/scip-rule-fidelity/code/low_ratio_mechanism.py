"""Why is z_C/z_K small on MINLPLib corners?

For analysed records of class 'ratio' (summarize.py) with z_C/z_K < THRESH, rebuild the corner and
find the ray j* attaining z_C = min_j w_j t_j (SCIP's steps if the cut was generated, else the
validated 'fixed' model).  Classify:
  zero_rate_ray : w_j* <= 1e-9 max w (the floor): SCIP's set has a finite step on a ray of zero
                  objective rate. Usually no single-ray intersection with S is found; the
                  diagnostic below also exposes drift lost by the reduced-space class test;
  small_rate_ray: 1e-9 max w < w_j* <= 1e-3 max w;
  other         : otherwise.
Uses summarize.ratio_of so the selected records match the summary table, including Gurobi
incumbents. For zero-rate j*, checks a finite one-ray candidate with zk_fast._on_boundary;
a finite root from one_ray_vec alone can be spurious. These are floating-point checks.
Usage: python3 low_ratio_mechanism.py THRESH ANALYSIS.jsonl [...]"""
import sys, os, json, collections, gzip
from fractions import Fraction as F
import numpy as np
import dumpio as D
import model_vec as M
import zk_fast as Z
import summarize as S

LOGS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../logs')
thr = float(sys.argv[1])
want = collections.defaultdict(dict); dumpdir = {}
for f in sys.argv[2:]:
    b = os.path.basename(f)
    dd = 'runs_mc11' if b == 'an_mc11.jsonl' else ('runs_mc12' if b == 'an_mc12.jsonl' else 'runs_minlplib')
    for l in open(f):
        r = json.loads(l)
        if r.get('status') != 'ok' or r['wmax'] <= 0 or r.get('zeroface_meets_S'):
            continue
        ratio = S.ratio_of(r)
        if ratio is not None and ratio['r'] < thr:
            want[r['inst']][r['k']] = r; dumpdir[r['inst']] = dd
cls = collections.Counter(); byinst = collections.defaultdict(collections.Counter); alone = collections.Counter()
for inst, recs in want.items():
    k = -1
    last = max(recs)
    with gzip.open(os.path.join(LOGS, dumpdir[inst], inst + '.jsonl.gz'), 'rt') as f:
        for line in f:
            if not line.startswith('{"v":'):
                continue
            k += 1
            if k > last:
                break
            if k not in recs:
                continue
            rec = json.loads(line)
            r = recs[k]
            Q, b, c = D.quadratic(rec); P, w, _, _ = D.rays(rec)
            keep = ~D.fixed_rays(rec); P, w = P[:, keep], w[keep]
            sbar = np.array(rec['zlp'], float)
            floor = 1e-9 * w.max(); wpos = np.maximum(w, floor)
            if r['zC_scip'] is not None:
                t, _, _ = D.scip_steps(rec); t = t[keep]
            else:
                t, _ = M.steps(M.prepare(Q, b, c, sbar, 'fixed'), P, amax=1e12)
            v = np.where(np.isfinite(t) & (t >= 0), wpos * t, np.inf)
            j = int(np.argmin(v))
            if w[j] <= floor:
                c_ = 'zero_rate_ray'
                t1, g0 = Z.one_ray_vec(Q, b, c, sbar, P[:, [j]])
                finite = np.isfinite(t1[0])
                reaches = finite and bool(Z._on_boundary(Q, b, c, sbar, P[:, [j]], t1, g0)[0])
                alone['S reached along j* alone (checked)' if reaches else 'S not reached along j* alone (checked)'] += 1
                if reaches:
                    Qr, br, cr, sr, Pr, _, _ = Z.reduce_space(Q, b, c, sbar, P[:, [j]])
                    tr, gr = Z.one_ray_vec(Qr, br, cr, sr, Pr)
                    checked_reduced = bool(np.isfinite(tr[0]) and Z._on_boundary(Qr, br, cr, sr, Pr, tr, gr)[0])
                    sb, p = list(map(F, sbar)), list(map(F, P[:, j]))
                    nz = [(a, m, F(Q[a, m])) for a, m in zip(*np.nonzero(Q))]
                    q0 = sum(sb[a] * value * sb[m] for a, m, value in nz) + sum(F(v) * x for v, x in zip(b, sb)) + F(c)
                    L = sum(2 * sb[a] * value * p[m] for a, m, value in nz) + sum(F(v) * x for v, x in zip(b, p))
                    A = sum(p[a] * value * p[m] for a, m, value in nz)
                    tf = F(t1[0])
                    qexact = q0 + L * tf + A * tf * tf
                    zc = r['zC_scip'] if r['zC_scip'] is not None else r['zC_fixed']
                    zk_estimate = zc / S.ratio_of(r)['r']
                    print('apparent one-ray intersection', inst, k, 'corner ray', j, 'raw rate', w[j],
                          'full t', t1[0], 'reduced t', tr[0], 'reduced passes boundary check', checked_reduced,
                          'exact q0,L,A', [float(v) for v in (q0, L, A)], 'exact q(candidate)', float(qexact),
                          'exact linear root', float(-q0 / L) if A == 0 and L < 0 else None,
                          'floored one-ray cost', wpos[j] * t1[0], 'table zK estimate', zk_estimate,
                          'table ratio', S.ratio_of(r)['r'])
                if finite and not reaches:
                    pt = sbar + t1[0] * P[:, j]
                    print('rejected one-ray candidate', inst, k, 'corner ray', j,
                          't', t1[0], 'q(candidate)/q(sbar)', (pt @ Q @ pt + b @ pt + c) / g0)
            elif w[j] <= 1e-3 * w.max():
                c_ = 'small_rate_ray'
            else:
                c_ = 'other'
            cls[c_] += 1; byinst[inst][c_] += 1
print('records with z_C/z_K <', thr, ':', sum(cls.values()), dict(cls))
print('zero-rate j*:', dict(alone))
for i in sorted(byinst):
    print('  %-26s %s' % (i, dict(byinst[i])))
