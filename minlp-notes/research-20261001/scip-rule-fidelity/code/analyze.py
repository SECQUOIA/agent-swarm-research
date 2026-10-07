"""Recompute every dumped SCIP intersection cut and compute z_C / z_K.

For each record of each dump (logs/runs_*/NAME.jsonl.gz):
  * rebuild S, sbar, P, w in the space SCIP uses (dumpio);
  * check the reconstruction (q(sbar) vs SCIP's violation, kappa and case vs SCIP's values);
  * model step lengths: 'fixed' (SCIP's formulas, model_vec, amax 1e12) and 'note'
    (scout_sfree.ms_set as used in the earlier note, amax 1e7), compared ray by ray with SCIP's
    interpoints;
  * z_C of SCIP's set (from SCIP's interpoints), of both models, and of the actual cut
    coefficients (monoidal / minimal-representation coefficients included);
  * z_K by zk_fast in the reduced space: exact (support <= 2) when rho = n_+ + 1 <= 2; for rho = 3
    the generic KKT value over 3-supports is added when the number of triples is moderate;
    otherwise the support-<=2 value is only an upper bound (flag zK_kind).
Rays of nonbasic equality rows and fixed columns are dropped (their lambda is 0 on the LP).
Zero objective rates are floored at 1e-9 max(w) for both z_C and z_K (as in exp_mccormick.py).
Output: one JSON line per record.
Usage: python3 analyze.py [--max-records K | --second-sample K] OUT.jsonl DUMP.jsonl.gz [...]
(--max-records: analyze a uniform random sample, seed 12345, of at most K records per dump;
 --second-sample K: K further records, seed 54321, disjoint from the '--max-records 50' sample.)
"""
import sys, json, math, os
import numpy as np
import dumpio as D
import model_vec as M
import zk_fast as Z

REL = 1e-6


def compare(ts, tm):
    """Classify SCIP step ts against model step tm."""
    if np.isnan(ts) or np.isnan(tm):
        return 'na', np.nan
    if np.isinf(ts) and np.isinf(tm):
        return 'match', 0.0
    if np.isinf(ts) != np.isinf(tm):
        return ('scip_inf' if np.isinf(ts) else 'model_inf'), np.inf
    rel = abs(ts - tm) / max(abs(tm), 1e-300)
    return ('match' if rel <= REL else 'diff'), rel


def zc_of(w, t):
    fin = np.isfinite(t) & (t >= 0)
    return float(np.min(w[fin] * t[fin])) if fin.any() else np.inf


def analyze_record(rec):
    out = {k: rec.get(k) for k in ('lp', 'node', 'depth', 'cons', 'over', 'isroot', 'nquad', 'nlin',
                                    'gen', 'cleanup', 'added', 'highre', 'fail', 'kappa', 'case4', 'case2', 'nrays')}
    out['aux'] = rec.get('auxvar') is not None
    if rec.get('fail') == 'numerics':
        out['fail_phi0'] = int(rec.get('nphinonneg1', 0) - rec.get('nphinonneg0', 0))
        out['fail_dyn'] = int(rec.get('nbadray1', 0) - rec.get('nbadray0', 0))
        for e in rec.get('perray', []):
            if e.get('fail'):
                dyn = []
                for key in ('c1234a', 'c4b'):
                    if key in e:
                        v = np.abs(np.array(e[key][:3], float)); nz = v[v != 0]
                        dyn.append(float(nz.max() / nz.min()) if nz.size else 0.0)
                        if key == 'c1234a':
                            out['fail_minabc'] = float(nz.min()) if nz.size else 0.0
                            out['fail_maxabc'] = float(nz.max()) if nz.size else 0.0
                out['fail_dynratio'] = dyn
                out['fail_ray'] = e['i']
    if 'nrays' not in rec or 'kappa' not in rec:
        out['status'] = 'norays' if 'nrays' not in rec else 'nocommon'
        return out
    Q, b, c = D.quadratic(rec)
    P, w, stat, lppos = D.rays(rec)
    fx = D.fixed_rays(rec)
    out['nfixedrays'] = int(fx.sum())
    keep = ~fx
    Pall = P
    P, w, stat, lppos = P[:, keep], w[keep], stat[keep], lppos[keep]
    sbar = np.array(rec['zlp'], float)
    qs = float(sbar @ Q @ sbar + b @ sbar + c)
    out['q_sbar'] = qs
    out['viol_scip'] = rec['violation']
    dd = M.setup(Q, b, c, sbar)
    kap, cs = dd['kappa'], dd['case']
    th = np.linalg.eigvalsh(Q)
    npos = int(np.sum(th > 1e-9)); nneg = int(np.sum(th < -1e-9))
    out.update(kappa_py=kap, case_py=cs, npos=npos, nneg=nneg, nv=int(rec['nv']))
    scase = 4 if rec['case4'] else (2 if rec['kappa'] > 0 else (3 if rec['kappa'] < 0 else 1))
    out['case_scip'] = scase
    out['wneg'] = int(np.sum(w < -1e-7 * max(1.0, np.abs(w).max())))
    out['wmax'] = float(w.max()) if w.size else 0.0
    out['nrays_corner'] = int(P.shape[1])
    wpos = np.maximum(w, 1e-9 * max(1e-300, w.max()))
    tsall, coef, mono = D.scip_steps(rec)
    ts, coef, mono = tsall[keep], coef[keep], mono[keep]
    out['nmono'] = int(mono.sum())
    out['nperray'] = int(np.sum(~np.isnan(ts)))
    if qs <= 0:
        out['status'] = 'sbar_feasible_in_reconstruction'
        return out
    res = {}
    for var, amax in (('fixed', 1e12), ('note', 1e7)):
        d = M.prepare(Q, b, c, sbar, var)
        tmall, g0 = M.steps(d, Pall, amax=amax)      # fidelity: all rays SCIP used
        res[var] = tmall
        tm = tmall[keep]                              # bounds: rays of the LP corner
        cls = {}
        mx = 0.0
        mxall = 0.0
        for j in range(Pall.shape[1]):
            k, rel = compare(tsall[j], tmall[j])
            cls[k] = cls.get(k, 0) + 1
            if k == 'diff':
                mx = max(mx, rel)
            if k in ('match', 'diff'):
                mxall = max(mxall, rel)
        out['maxrelall_' + var] = mxall
        out['cmp_' + var] = cls
        out['maxrel_' + var] = mx
        out['g0_' + var] = float(g0)
        out['zC_' + var] = zc_of(wpos, tm) if g0 < 0 else None
    # details of mismatching rays (fixed model)
    det = []
    for j in range(Pall.shape[1]):
        k, rel = compare(tsall[j], res['fixed'][j])
        if k not in ('match', 'na'):
            det.append([j, tsall[j], res['fixed'][j], res['note'][j], k])
    out['mismatch_fixed'] = det[:20]
    out['zC_scip'] = zc_of(wpos, ts) if out['nperray'] == P.shape[1] else None
    # actual cut coefficients a_j (cut sum a_j lam_j >= 1): bound min_{a_j > 0} w_j / a_j
    if out['nperray'] == P.shape[1] or np.all(~np.isnan(coef)):
        pos = coef > 0
        out['zcut'] = float(np.min(wpos[pos] / coef[pos])) if pos.any() else np.inf
        out['nnegcoef'] = int(np.sum(coef < 0))
    # corner bound
    Qr, br, cr, sr, Pr, rho, _ = Z.reduce_space(Q, b, c, sbar, P)
    out['rho'] = rho
    out['zK_tiny'] = bool(np.any((w <= 1e-9 * max(1e-300, w.max())) & np.isfinite(Z.one_ray_vec(Qr, br, cr, sr, Pr)[0])))
    z2, arg = Z.zK_upto2(Qr, br, cr, sr, Pr, wpos)
    out['zK2'] = z2
    out['zK_support'] = list(arg)
    if rho <= 2:
        out['zK'] = z2; out['zK_kind'] = 'exact'
    else:
        z3 = Z.zK_kkt3(Qr, br, cr, sr, Pr, wpos) if rho == 3 else None
        if z3 is not None:
            out['zK'] = min(z2, z3); out['zK_kind'] = 'kkt3'
        else:
            out['zK'] = z2; out['zK_kind'] = 'upper'
    # dual degeneracy: does the face of zero-rate rays meet S?  Then z_K(w) = z_C = 0 for every
    # S-free set and the ratio z_C/z_K is undefined.  Exact for rho <= 2 (supports <= 2 suffice);
    # for rho >= 3 'finite' is certain, 'inf' only means no support <= 2 meets S.
    zr = w <= 1e-9 * max(1e-300, w.max())
    out['nzerorate'] = int(zr.sum())
    if zr.any():
        z0, _ = Z.zK_upto2(Qr, br, cr, sr, Pr[:, zr], np.ones(int(zr.sum())))
        out['zeroface_meets_S'] = bool(np.isfinite(z0))
    else:
        out['zeroface_meets_S'] = False
    # cut coefficients vs 1/t (rays without monoidal coefficient)
    # finite t: coef must be 1/t; t = inf: coef must be <= 0 (0, or the negative minimal-representation
    # coefficient of Case 2)
    okc = ~np.isnan(ts) & ~mono & np.isfinite(ts)
    if okc.any():
        inv = 1.0 / ts[okc]; cc = coef[okc]
        out['coef_vs_inv_t'] = float(np.max(np.abs(cc - inv) / np.maximum(1e-300, np.maximum(np.abs(cc), np.abs(inv)))))
    infr = ~np.isnan(ts) & ~mono & np.isinf(ts)
    out['n_inf_t'] = int(infr.sum()); out['n_inf_t_negcoef'] = int(np.sum(coef[infr] < 0)); out['n_inf_t_poscoef'] = int(np.sum(coef[infr] > 0))
    out['status'] = 'ok'
    return out


def main():
    args = sys.argv[1:]
    maxrec = None; second = False
    if args[0] == '--max-records':          # uniform sample of at most K attempt records per file
        maxrec = int(args[1]); args = args[2:]
    if args[0] == '--second-sample':        # K further records, disjoint from the '--max-records 50' sample
        maxrec = int(args[1]); args = args[2:]; second = True
    outp = args[0]
    with open(outp, 'w') as fo:
        for path in args[1:]:
            inst = os.path.basename(path).split('.')[0]
            keepidx = None
            if maxrec is not None:
                n = sum(1 for rec in D.records(path) if 'v' in rec)
                if not second:
                    if n > maxrec:
                        keepidx = set(np.random.default_rng(12345).choice(n, maxrec, replace=False).tolist())
                    fo.write(json.dumps(dict(inst=inst, sampling=dict(nrecords=n, analyzed=min(n, maxrec)))) + '\n')
                else:
                    first = set(np.random.default_rng(12345).choice(n, 50, replace=False).tolist()) if n > 50 else set(range(n))
                    rest = np.array(sorted(set(range(n)) - first), int)
                    pick = np.random.default_rng(54321).choice(rest, min(maxrec, rest.size), replace=False) if rest.size else rest
                    keepidx = set(pick.tolist())
                    fo.write(json.dumps(dict(inst=inst, sampling=dict(nrecords=n, analyzed=len(keepidx), second=True))) + '\n')
            k = -1
            for rec in D.records(path):
                if 'v' in rec:
                    k += 1
                    if keepidx is not None and k not in keepidx:
                        continue
                if 'counters' in rec or 'nlhdlrstats' in rec:
                    fo.write(json.dumps(dict(inst=inst, **rec)) + '\n')
                    continue
                if rec.get('corrupt'):
                    fo.write(json.dumps(dict(inst=inst, status='corrupt')) + '\n')
                    continue
                try:
                    r = analyze_record(rec)
                    r['k'] = k
                except Exception as e:     # keep going, report
                    r = dict(status='error', error=repr(e)[:300], lp=rec.get('lp'), cons=rec.get('cons'))
                r['inst'] = inst
                fo.write(json.dumps(r, default=lambda x: None if (isinstance(x, float) and math.isnan(x)) else float(x)) + '\n')
                fo.flush()


if __name__ == '__main__':
    main()
