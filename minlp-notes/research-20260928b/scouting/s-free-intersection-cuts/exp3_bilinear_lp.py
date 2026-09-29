"""E3: bilinear McCormick LP relaxations.  At an optimal LP vertex violating a
bilinear equation w_e = x_i x_j, compare the one-cut bound increments of
  MS    : SCIP's constant-Gamma maximal quadratic-free set (Chmiela et al.),
  K     : best intersection cut for the violated side, corner K cap S (no bounds),
  KB    : best cut for K cap S cap {bounds of x_i, x_j, w_e} (bound-aware corner),
against the single-constraint bound z1 = min{c^T x : x in P, w_e = x_i x_j}.
All increments are relative to the LP value; gap closed = incr / (z1 - zLP)."""
import numpy as np, json, sys
from scipy.optimize import linprog
import pyscipopt as ps
from sfree import ms_set, ic_bound, corner_bound_scip, qval

rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 3)


def make_instance(p=4, npairs=4, nlin=3):
    pairs = set()
    while len(pairs) < npairs:
        i, j = sorted(rng.choice(p, 2, replace=False))
        pairs.add((i, j))
    pairs = sorted(pairs)
    n = p + len(pairs)
    lo = np.concatenate([rng.uniform(-1, 0.5, p), np.zeros(len(pairs))])
    hi = np.concatenate([lo[:p] + rng.uniform(0.5, 2, p), np.zeros(len(pairs))])
    for e, (i, j) in enumerate(pairs):
        cands = [lo[i] * lo[j], lo[i] * hi[j], hi[i] * lo[j], hi[i] * hi[j]]
        lo[p + e], hi[p + e] = min(cands), max(cands)
    A, bvec = [], []
    for e, (i, j) in enumerate(pairs):  # McCormick
        wv = p + e
        for (xi, xj, s) in [(lo[i], lo[j], -1), (hi[i], hi[j], -1), (lo[i], hi[j], +1), (hi[i], lo[j], +1)]:
            # s=-1: w >= xj*x_i + xi*x_j - xi*xj  ->  xj x_i + xi x_j - w <= xi xj
            row = np.zeros(n)
            if s == -1:
                row[i], row[j], row[wv] = xj, xi, -1.0
                A.append(row); bvec.append(xi * xj)
            else:
                row[i], row[j], row[wv] = -xj, -xi, 1.0
                A.append(row); bvec.append(-xi * xj)
    for _ in range(nlin):
        row = rng.normal(size=n)
        mid = (lo + hi) / 2
        A.append(row); bvec.append(row @ mid + abs(row) @ (hi - lo) * 0.15)
    c = rng.normal(size=n)
    return dict(p=p, pairs=pairs, n=n, lo=lo, hi=hi, A=np.array(A), b=np.array(bvec), c=c)


def lp_vertex(I):
    import highspy
    h = highspy.Highs(); h.setOptionValue('output_flag', False)
    n = I['n']; A = I['A']; m_ = A.shape[0]
    inf = highspy.kHighsInf
    lp = highspy.HighsLp()
    lp.num_col_ = n; lp.num_row_ = m_
    lp.col_cost_ = I['c'].tolist(); lp.col_lower_ = I['lo'].tolist(); lp.col_upper_ = I['hi'].tolist()
    lp.row_lower_ = [-inf] * m_; lp.row_upper_ = I['b'].tolist()
    lp.a_matrix_.format_ = highspy.MatrixFormat.kRowwise
    starts, idxs, vals = [0], [], []
    for k_ in range(m_):
        for v in range(n):
            if A[k_, v] != 0:
                idxs.append(v); vals.append(A[k_, v])
        starts.append(len(idxs))
    lp.a_matrix_.start_ = starts; lp.a_matrix_.index_ = idxs; lp.a_matrix_.value_ = vals
    h.passModel(lp); h.run()
    if h.getModelStatus() != highspy.HighsModelStatus.kOptimal:
        return None
    x = np.array(h.getSolution().col_value)
    B = h.getBasis()
    rows = []
    for v in range(n):
        st = B.col_status[v]
        if st == highspy.HighsBasisStatus.kLower:
            e = np.zeros(n); e[v] = -1; rows.append(e)
        elif st == highspy.HighsBasisStatus.kUpper:
            e = np.zeros(n); e[v] = 1; rows.append(e)
    for k_ in range(m_):
        if B.row_status[k_] != highspy.HighsBasisStatus.kBasic:
            rows.append(A[k_].copy())
    if len(rows) != n:
        return None
    Ab = np.array(rows)
    if abs(np.linalg.det(Ab)) < 1e-10:
        return None
    R = -np.linalg.inv(Ab)
    w = I['c'] @ R
    if np.any(w < -1e-7):
        return None
    return x, R, np.maximum(w, 0), h.getInfo().objective_function_value


def single_constraint_bound(I, e, timelimit=60):
    m = ps.Model(); m.hideOutput(); m.setParam('limits/time', timelimit)
    n = I['n']
    xs = [m.addVar(lb=I['lo'][v], ub=I['hi'][v]) for v in range(n)]
    for k_ in range(len(I['b'])):
        m.addCons(ps.quicksum(I['A'][k_, v] * xs[v] for v in range(n)) <= I['b'][k_])
    i, j = I['pairs'][e]
    m.addCons(xs[I['p'] + e] == xs[i] * xs[j])
    m.setObjective(ps.quicksum(I['c'][v] * xs[v] for v in range(n)))
    m.optimize()
    return m.getDualbound()


res = []
for trial in range(int(sys.argv[2]) if len(sys.argv) > 2 else 40):
    I = make_instance()
    out = lp_vertex(I)
    if out is None:
        continue
    x, R, w, zlp = out
    p = I['p']
    viol = [(abs(x[p + e] - x[i] * x[j]), e) for e, (i, j) in enumerate(I['pairs'])]
    vmax, e = max(viol)
    if vmax < 1e-4:
        continue
    i, j = I['pairs'][e]
    idx = [i, j, p + e]
    sbar = x[idx]
    # violated side: q(s) = sign*(s0*s1 - s2) <= 0 is the constraint violated at sbar
    Q = np.zeros((3, 3)); Q[0, 1] = Q[1, 0] = 0.5
    bq = np.array([0, 0, -1.0])
    if qval(Q, bq, 0, sbar) < 0:  # w > xy: violated side is w <= xy, i.e. xy - w >= 0 -> -(xy-w) <= 0
        Q, bq = -Q, -bq
    assert qval(Q, bq, 0, sbar) > 0
    P = R[idx, :]
    G, cs = ms_set(Q, bq, 0.0, sbar)
    zms, al = ic_bound(G, sbar, P, w)
    zk = corner_bound_scip(Q, bq, 0.0, sbar, P, w)
    zkb = corner_bound_scip(Q, bq, 0.0, sbar, P, w, box=(I['lo'][idx], I['hi'][idx]))
    z1 = single_constraint_bound(I, e) - zlp
    if z1 < 1e-6:
        continue
    rec = dict(zlp=zlp, gap=z1, ms=min(zms, zk) / z1 if np.isfinite(zms) else 0.0,
               K=min(zk, z1) / z1, KB=min(zkb, z1) / z1, nzero_w=int(np.sum(w < 1e-9)))
    res.append(rec)
    print(trial, {k: round(v, 4) if isinstance(v, float) else v for k, v in rec.items()}, flush=True)
ms = np.array([r['ms'] for r in res]); K = np.array([r['K'] for r in res]); KB = np.array([r['KB'] for r in res])
summ = dict(n=len(res), ms_mean=float(ms.mean()), K_mean=float(K.mean()), KB_mean=float(KB.mean()),
            ms_median=float(np.median(ms)), K_median=float(np.median(K)), KB_median=float(np.median(KB)),
            frac_KB_gt_K_plus_0p1=float(np.mean(KB > K + 0.1)), frac_ms_lt_0p5K=float(np.mean(ms < 0.5 * K)))
print('SUMMARY', summ)
json.dump(dict(summary=summ, records=res), open('exp3_bilinear_lp_%s.json' % (sys.argv[1] if len(sys.argv) > 1 else '3'), 'w'), indent=1)
