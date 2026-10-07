"""Classify every ray on which SCIP's step t_scip and the model step t_model (fixed variant) differ.

Input: analysis outputs (logs/an_*/...jsonl, field mismatch_fixed) and the raw dumps.
For each mismatching ray, SCIP's computeIntersectionPoint is replayed in Python from the dumped
restriction coefficients (A, B, C, D, E of piece 4a/1-3, of piece 4b, and the case-4 condition):
  root  : smallest t >= 0 with (A - D^2) t^2 + (B - 2DE) t >= E^2 - C (stable quadratic formula;
          SCIP uses outward-rounded interval arithmetic), t = inf if sqrt(A) <= D, t = 1e20
          (SCIPinfinity) if the solution set is empty (negative discriminant);
  bisect: if phi(root) > 1e-10, SCIP's doBinarySearch (lb = 0, ub = root, 120 iterations, stop when
          |phi| <= 1e-6 or ub, lb equal up to relative 1e-6), returning lb.
Classes:
  cutoff      : model reports inf (no exit before amax = 1e12) and t_scip >= 1e11;
  scip_inf_far: SCIP reports inf, model finite with t_model >= 1e9;
  bisection   : the replay takes the bisection branch and reproduces t_scip (rel 1e-9);
  root_rounding: no bisection; the replay reproduces t_scip (rel 1e-9), so the difference to the
                model is rounding in SCIP's quadratic formula or in the model's bisection;
  other       : anything else (printed in full).
Usage: python3 explain_mismatch.py ANALYSIS.jsonl [...]   (dump paths derived from the file names)
"""
import sys, os, json, glob, collections, math
import numpy as np
import dumpio as D
import model_vec as M
import analyze as A

FEASTOL = 1e-6


def phi(t, a, b, c, d, e):
    return math.sqrt(max(a * t * t + b * t + c, 0.0)) - (d * t + e)


def root(co):
    a, b, c, d, e = co
    if math.sqrt(max(a, 0.0)) <= d:
        return math.inf
    qa, qb, qc = a - d * d, b - 2 * d * e, c - e * e        # qa t^2 + qb t + qc = 0, qc < 0
    if qa == 0:
        return -qc / qb if qb > 0 else 1e20
    disc = qb * qb - 4 * qa * qc
    if disc < 0:
        return 1e20          # empty interval result: SCIP sets sol = SCIPinfinity, then bisects
    s = math.sqrt(disc)
    r1 = (-qb - s) / (2 * qa); r2 = (-qb + s) / (2 * qa)
    # stable form of the positive root
    rr = [x for x in (r1, r2, (2 * qc) / (-qb - s) if (-qb - s) != 0 else math.nan,
                      (2 * qc) / (-qb + s) if (-qb + s) != 0 else math.nan) if x == x and x >= 0]
    return min(rr) if rr else 1e20


def feaseq(x, y):
    return abs(x - y) / max(abs(x), abs(y), 1.0) <= FEASTOL


def compute_root(co):
    t = root(co)
    if math.isinf(t):
        return t, False
    if phi(t, *co) <= 1e-10:
        return t, False
    lb, ub = 0.0, t
    for _ in range(120):
        cur = (lb + ub) / 2
        pv = phi(cur, *co)
        if pv <= 0:
            lb = cur
            if abs(pv) <= FEASTOL or feaseq(ub, lb):
                break
        else:
            ub = cur
    return lb, True


def is4a(t, co, cond):
    a, b, c = co[:3]
    return cond[0] * math.sqrt(max(a * t * t + b * t + c, 0)) + cond[1] * t + cond[2] <= 0


def replay(e, case4):
    t1, bis1 = compute_root(e['c1234a'])
    if not case4:
        return t1, bis1
    if math.isinf(t1):
        return t1, bis1
    if is4a(t1, e['c1234a'], e['cond']):
        return t1, bis1
    t2, bis2 = compute_root(e['c4b'])
    return max(t1, t2), (bis2 if t2 >= t1 else bis1)


def main():
    files = sys.argv[1:]
    cls = collections.Counter(); bycls = collections.defaultdict(list); nrec_rays = [0]
    for f in files:
        want = collections.defaultdict(dict)
        dumpdir = None
        for l in open(f):
            r = json.loads(l)
            if r.get('status') != 'ok' or not r.get('mismatch_fixed'):
                continue
            for j, ts, tm, tn, kind in r['mismatch_fixed']:
                want[(r['inst'], r['k'])][j] = (ts, tm, kind, r['case_scip'], r['kappa'])
        if not want:
            continue
        # locate dumps
        insts = {i for i, _ in want}
        for inst in insts:
            for d in ('runs_minlplib', 'runs_mc11', 'runs_mc12'):
                path = os.path.join(os.path.dirname(f), '..', d, inst + '.jsonl.gz')
                if not os.path.exists(path):
                    path = os.path.join(os.path.dirname(f), d, inst + '.jsonl.gz')
                if os.path.exists(path):
                    break
            k = -1
            for rec in D.records(path):
                if 'v' not in rec:
                    continue
                k += 1
                if (inst, k) not in want:
                    continue
                per = {e['i']: e for e in rec.get('perray', [])}
                # analyze.py stores at most 20 mismatching rays per record: recompute the model steps
                # ('fixed', amax 1e12, as analyze.py) for all rays and classify every mismatching ray
                Q, b, c = D.quadratic(rec); Pall, _, _, _ = D.rays(rec)
                sbar = np.array(rec['zlp'], float)
                dm = M.prepare(Q, b, c, sbar, 'fixed')
                tmall, _ = M.steps(dm, Pall, amax=1e12)
                tsall, _, _ = D.scip_steps(rec)
                cs0, kap0 = next(iter(want[(inst, k)].values()))[3:5]
                allm = {}
                for j in range(Pall.shape[1]):
                    kind, _ = A.compare(tsall[j], tmall[j])
                    if kind not in ('match', 'na'):
                        allm[j] = (float(tsall[j]), float(tmall[j]), kind, cs0, kap0)
                nrec_rays[0] += len(allm)
                for j, (ts, tm, kind, cs, kap) in allm.items():
                    ts = math.inf if ts is None else ts
                    tm = math.inf if tm is None else tm
                    e = per.get(j)
                    rep, bis = (None, None) if (e is None or 'c1234a' not in e) else replay(e, bool(rec['case4']))
                    if kind == 'model_inf' and ts >= 1e11:
                        c = 'cutoff'
                    elif kind == 'scip_inf' and tm >= 1e9:
                        c = 'scip_inf_far'
                    elif kind == 'diff' and rep is not None and bis and abs(rep - ts) <= 1e-9 * max(1.0, abs(ts)):
                        c = 'bisection'
                    elif kind == 'diff' and rep is not None and not bis and abs(rep - ts) <= 1e-9 * max(1.0, abs(ts)):
                        c = 'root_rounding'
                    else:
                        c = 'other'
                    cls[c] += 1
                    bycls[c].append(dict(inst=inst, k=k, j=j, case=cs, kappa=kap, t_scip=ts, t_model=tm, replay=rep, bisect=bis,
                                         rel=(abs(ts - tm) / tm if math.isfinite(ts) and math.isfinite(tm) and tm > 0 else None)))
    print('classes', dict(cls), 'total mismatching rays', nrec_rays[0])
    for c, L in bycls.items():
        rels = [x['rel'] for x in L if x['rel'] is not None]
        ts = [x['t_scip'] for x in L]; tm = [x['t_model'] for x in L]
        print('==', c, len(L), 'instances', dict(collections.Counter(x['inst'] for x in L)))
        if rels:
            print('   rel diff max %.3g median %.3g; t_scip < t_model in %d of %d' % (max(rels), float(np.median(rels)),
                  sum(1 for x in L if x['t_scip'] < x['t_model']), len(L)))
        if c == 'cutoff':
            print('   min t_scip %.3g' % min(ts))
        if c == 'scip_inf_far':
            print('   min t_model %.3g' % min(tm))
        if c == 'other':
            for x in L:
                print('  ', json.dumps(x))


if __name__ == '__main__':
    main()
