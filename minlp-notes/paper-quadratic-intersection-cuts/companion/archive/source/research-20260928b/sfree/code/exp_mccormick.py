"""McCormick LP relaxations of random bilinear programs (generator of the scout's E3).

At an optimal LP vertex that violates some w_e = x_i x_j, take the most violated term and
the simplicial cone of the optimal basis.  Compare one cut from
  SCIP  : Chmiela-Munoz-Serrano Case-4 maximal set (SCIP's construction),
  ORBIT : best set of the sliced orbit family (A) (LMI bisection, certified bound),
  CORNER: the corner-optimal cut w^T lam >= z_K (bound-optimal single intersection cut),
against the single-constraint bound z1 = min{c^T x : x in P, w_e = x_i x_j}.
Reported per instance: fraction of the single-constraint gap (z1 - zLP) closed
  (i) by the corner increment z_C(w) (bound over the cone),
  (ii) by re-solving the LP over P with the cut added.
Usage: python3 exp_mccormick.py SEED NTRIALS OUT.json
"""
import sys, json, warnings
import numpy as np
warnings.filterwarnings('ignore')
import highspy
import pyscipopt as ps
from core import corner_bound, qval, best_orbit_bound, bilinear_quadratic
from scout_sfree import ms_set, ic_bound

rng = np.random.default_rng(11)


def make_instance(p=4, npairs=4, nlin=3):
    pairs = set()
    while len(pairs) < npairs:
        i, j = sorted(rng.choice(p, 2, replace=False)); pairs.add((i, j))
    pairs = sorted(pairs); n = p + len(pairs)
    lo = np.concatenate([rng.uniform(-1, 0.5, p), np.zeros(len(pairs))])
    hi = np.concatenate([lo[:p] + rng.uniform(0.5, 2, p), np.zeros(len(pairs))])
    for e, (i, j) in enumerate(pairs):
        cands = [lo[i] * lo[j], lo[i] * hi[j], hi[i] * lo[j], hi[i] * hi[j]]
        lo[p + e], hi[p + e] = min(cands), max(cands)
    A, bvec = [], []
    for e, (i, j) in enumerate(pairs):
        wv = p + e
        for (xi, xj, s) in [(lo[i], lo[j], -1), (hi[i], hi[j], -1), (lo[i], hi[j], +1), (hi[i], lo[j], +1)]:
            row = np.zeros(n)
            if s == -1:
                row[i], row[j], row[wv] = xj, xi, -1.0; A.append(row); bvec.append(xi * xj)
            else:
                row[i], row[j], row[wv] = -xj, -xi, 1.0; A.append(row); bvec.append(-xi * xj)
    for _ in range(nlin):
        row = rng.normal(size=n); mid = (lo + hi) / 2
        A.append(row); bvec.append(row @ mid + abs(row) @ (hi - lo) * 0.15)
    c = rng.normal(size=n)
    return dict(p=p, pairs=pairs, n=n, lo=lo, hi=hi, A=np.array(A), b=np.array(bvec), c=c)


def solve_lp(I, extra_rows=(), extra_rhs=()):
    h = highspy.Highs(); h.setOptionValue('output_flag', False)
    n = I['n']; A = np.vstack([I['A']] + [np.atleast_2d(r) for r in extra_rows]) if extra_rows else I['A']
    bb = np.concatenate([I['b'], np.array(extra_rhs, float)]) if extra_rows else I['b']
    m_ = A.shape[0]; inf = highspy.kHighsInf
    lp = highspy.HighsLp(); lp.num_col_ = n; lp.num_row_ = m_
    lp.col_cost_ = I['c'].tolist(); lp.col_lower_ = I['lo'].tolist(); lp.col_upper_ = I['hi'].tolist()
    lp.row_lower_ = [-inf] * m_; lp.row_upper_ = bb.tolist()
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
    return h, A, bb


def basis_cone(I, h, A, bb):
    n = I['n']; x = np.array(h.getSolution().col_value); B = h.getBasis()
    rows, rhs = [], []
    for v in range(n):
        st = B.col_status[v]
        if st == highspy.HighsBasisStatus.kLower:
            e = np.zeros(n); e[v] = -1; rows.append(e); rhs.append(-I['lo'][v])
        elif st == highspy.HighsBasisStatus.kUpper:
            e = np.zeros(n); e[v] = 1; rows.append(e); rhs.append(I['hi'][v])
    for k_ in range(A.shape[0]):
        if B.row_status[k_] != highspy.HighsBasisStatus.kBasic:
            rows.append(A[k_].copy()); rhs.append(bb[k_])
    if len(rows) != n:
        return None
    Ab = np.array(rows); rhs = np.array(rhs)
    if abs(np.linalg.det(Ab)) < 1e-10:
        return None
    R = -np.linalg.inv(Ab)             # x = xbar + R lam, lam = rhs - Ab x >= 0
    w = I['c'] @ R
    if np.any(w < -1e-7):
        return None
    return x, R, np.maximum(w, 0.0), Ab, rhs, h.getInfo().objective_function_value


def single_constraint_bound(I, e, timelimit=60):
    m = ps.Model(); m.hideOutput(); m.setParam('limits/time', timelimit)
    n = I['n']; xs = [m.addVar(lb=I['lo'][v], ub=I['hi'][v]) for v in range(n)]
    for k_ in range(len(I['b'])):
        m.addCons(ps.quicksum(I['A'][k_, v] * xs[v] for v in range(n)) <= I['b'][k_])
    i, j = I['pairs'][e]
    m.addCons(xs[I['p'] + e] == xs[i] * xs[j])
    m.setObjective(ps.quicksum(I['c'][v] * xs[v] for v in range(n)))
    m.optimize()
    return m.getDualbound()


def lp_with_cut(I, Ab, rhs, a):
    """add sum_j a_j lam_j >= 1 with lam = rhs - Ab x  <=>  (a^T Ab) x <= a^T rhs - 1."""
    out = solve_lp(I, [a @ Ab], [a @ rhs - 1.0])
    return None if out is None else out[0].getInfo().objective_function_value


if __name__ == '__main__':
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 11
    T = int(sys.argv[2]) if len(sys.argv) > 2 else 40
    OUT = sys.argv[3] if len(sys.argv) > 3 else '../logs/exp_mccormick_%d.json' % seed
    rng = np.random.default_rng(seed)
    SIZE = tuple(int(a) for a in sys.argv[4:7]) if len(sys.argv) > 6 else (4, 4, 3)
    res = []
    for trial in range(T):
        I = make_instance(*SIZE)
        out = solve_lp(I)
        if out is None:
            continue
        h, A, bb = out
        bc = basis_cone(I, h, A, bb)
        if bc is None:
            continue
        x, R, w, Ab, rhs, zlp = bc
        p = I['p']
        viol = [(abs(x[p + e] - x[i] * x[j]), e) for e, (i, j) in enumerate(I['pairs'])]
        vmax, e = max(viol)
        if vmax < 1e-4:
            continue
        i, j = I['pairs'][e]; idx = [i, j, p + e]
        sbar = x[idx]
        side = '+' if sbar[2] > sbar[0] * sbar[1] else '-'     # '+': violated side is w <= xy
        Q, bq, cq = bilinear_quadratic(side)
        assert qval(Q, bq, cq, sbar) > 0
        P = R[idx, :]
        nz = int(np.sum(w < 1e-9))
        wpos = np.maximum(w, 1e-9 * max(1.0, w.max()))       # zero reduced costs floored (reported)
        z1 = single_constraint_bound(I, e) - zlp
        if z1 < 1e-6:
            continue
        G, cs = ms_set(Q, bq, cq, sbar)
        zms, al_ms = ic_bound(G, sbar, P, w)
        zk = corner_bound(Q, bq, cq, sbar, P, wpos)
        zorb, _, F = best_orbit_bound(side, sbar, P, wpos, min(zk, 1e6), iters=30)
        from bilinear import step_A
        al_orb = np.array([step_A(F, side, sbar, P[:, jj]) for jj in range(P.shape[1])]) if F is not None else None
        # actual LP bounds with the cut added to P
        a_ms = np.array([0.0 if not np.isfinite(t) else 1.0 / t for t in al_ms])
        lp_ms = lp_with_cut(I, Ab, rhs, a_ms)
        lp_orb = lp_with_cut(I, Ab, rhs, np.array([0.0 if not np.isfinite(t) else 1.0 / t for t in al_orb])) if al_orb is not None else None
        lp_cor = lp_with_cut(I, Ab, rhs, wpos / zk) if np.isfinite(zk) and zk > 0 else None
        fr = lambda v: None if v is None else float(min(max(v, 0.0), z1) / z1)
        rec = dict(trial=trial, side=side, nzero_w=nz, gap=z1, zK=zk,
                   ms_incr=fr(min(zms, zk)), orbit_incr=fr(min(zorb, zk)), corner_incr=fr(zk),
                   ms_lp=fr(None if lp_ms is None else lp_ms - zlp),
                   orbit_lp=fr(None if lp_orb is None else lp_orb - zlp),
                   corner_lp=fr(None if lp_cor is None else lp_cor - zlp),
                   orbit_over_zK=float(min(zorb, zk) / zk) if zk > 0 else None,
                   ms_over_zK=float(min(zms, zk) / zk) if zk > 0 else None)
        res.append(rec)
        print(json.dumps(rec), flush=True)

    keys = ['ms_incr', 'orbit_incr', 'corner_incr', 'ms_lp', 'orbit_lp', 'corner_lp', 'ms_over_zK', 'orbit_over_zK']
    summ = {'n': len(res), 'n_with_zero_reduced_costs': int(sum(r['nzero_w'] > 0 for r in res))}
    for k in keys:
        v = np.array([r[k] for r in res if r[k] is not None], float)
        summ[k] = dict(mean=float(v.mean()), median=float(np.median(v)), q10=float(np.quantile(v, .1)), min=float(v.min()), n=len(v))
    print('SUMMARY', json.dumps(summ))
    json.dump(dict(summary=summ, records=res), open(OUT, 'w'), indent=1)
