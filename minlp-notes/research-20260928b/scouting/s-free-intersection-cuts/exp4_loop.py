"""E4: pure intersection-cut loops (one cut per round at the LP optimal vertex)
for  min c^T x  s.t.  x in P (polytope, R^k),  q(x) <= 0.
Cuts from SCIP's constant-Gamma maximal quadratic-free set.  Tracks the LP
value against z* = min over P cap S (SCIP) to see convergence or stalling."""
import numpy as np, json, sys
import highspy
import pyscipopt as ps
from sfree import ms_set, step_length, qval


def solve_lp(c, A, b, lo, hi):
    h = highspy.Highs(); h.setOptionValue('output_flag', False)
    n = len(c); m_ = A.shape[0]
    inf = highspy.kHighsInf
    lp = highspy.HighsLp()
    lp.num_col_ = n; lp.num_row_ = m_
    lp.col_cost_ = list(c); lp.col_lower_ = list(lo); lp.col_upper_ = list(hi)
    lp.row_lower_ = [-inf] * m_; lp.row_upper_ = list(b)
    lp.a_matrix_.format_ = highspy.MatrixFormat.kRowwise
    starts, idxs, vals = [0], [], []
    for k_ in range(m_):
        for v in range(n):
            if A[k_, v] != 0:
                idxs.append(v); vals.append(float(A[k_, v]))
        starts.append(len(idxs))
    lp.a_matrix_.start_ = starts; lp.a_matrix_.index_ = idxs; lp.a_matrix_.value_ = vals
    h.passModel(lp); h.run()
    x = np.array(h.getSolution().col_value)
    B = h.getBasis()
    rows, rhs = [], []
    for v in range(n):
        st = B.col_status[v]
        if st == highspy.HighsBasisStatus.kLower:
            e = np.zeros(n); e[v] = -1; rows.append(e); rhs.append(-lo[v])
        elif st == highspy.HighsBasisStatus.kUpper:
            e = np.zeros(n); e[v] = 1; rows.append(e); rhs.append(hi[v])
    for k_ in range(m_):
        if B.row_status[k_] != highspy.HighsBasisStatus.kBasic:
            rows.append(A[k_].copy()); rhs.append(b[k_])
    return x, np.array(rows), h.getInfo().objective_function_value


def global_opt(c, A, b, lo, hi, Q, bq, cq):
    m = ps.Model(); m.hideOutput(); m.setParam('limits/time', 60)
    n = len(c)
    xs = [m.addVar(lb=lo[v], ub=hi[v]) for v in range(n)]
    for k_ in range(A.shape[0]):
        m.addCons(ps.quicksum(A[k_, v] * xs[v] for v in range(n)) <= b[k_])
    m.addCons(ps.quicksum(Q[i, j] * xs[i] * xs[j] for i in range(n) for j in range(n))
              + ps.quicksum(bq[i] * xs[i] for i in range(n)) + cq <= 0)
    m.setObjective(ps.quicksum(c[v] * xs[v] for v in range(n)))
    m.optimize()
    return m.getObjVal()


def loop(c, A, b, lo, hi, Q, bq, cq, rounds=200):
    zstar = global_opt(c, A, b, lo, hi, Q, bq, cq)
    A = A.copy(); b = b.copy()
    hist = []
    for t in range(rounds):
        x, Ab, z = solve_lp(c, A, b, lo, hi)
        hist.append(z)
        if qval(Q, bq, cq, x) <= 1e-9 or zstar - z < 1e-9:
            break
        n = len(c)
        if Ab.shape[0] != n or abs(np.linalg.det(Ab)) < 1e-12:
            break
        R = -np.linalg.inv(Ab)
        G, cs = ms_set(Q, bq, cq, x)
        al = np.array([step_length(G, x, R[:, j]) for j in range(n)])
        a = np.array([1 / v if np.isfinite(v) else 0.0 for v in al])
        # cut: sum_j a_j lam_j >= 1 with lam = -Ab (x' - x)  ->  a^T Ab x' <= a^T Ab x - 1
        row = a @ Ab
        rhs = row @ x - 1.0
        nr = np.linalg.norm(row)
        A = np.vstack([A, row / nr]); b = np.append(b, rhs / nr)
    return zstar, hist


if __name__ == '__main__':
    rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 5)
    k = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    results = []
    for trial in range(int(sys.argv[3]) if len(sys.argv) > 3 else 10):
        while True:
            M = rng.normal(size=(k, k)); Q = (M + M.T) / 2
            th = np.linalg.eigvalsh(Q)
            if th.min() < -0.2 and th.max() > 0.2:
                break
        bq = rng.normal(size=k); cq = rng.normal()
        lo, hi = -np.ones(k) * 2, np.ones(k) * 2
        A = rng.normal(size=(k + 2, k)); b = np.abs(rng.normal(size=k + 2)) + 0.5
        c = rng.normal(size=k)
        x, Ab, z = solve_lp(c, A, b, lo, hi)
        if qval(Q, bq, cq, x) <= 0:
            continue
        try:
            zstar, hist = loop(c, A, b, lo, hi, Q, bq, cq)
        except Exception as ex:
            print('err', ex); continue
        g0 = zstar - hist[0]
        gaps = [(zstar - h) / g0 for h in hist]
        rec = dict(rounds=len(hist), gap_after=[round(gaps[i], 5) for i in (1, 5, 20, 50, 100, len(gaps) - 1) if i < len(gaps)],
                   final_gap=gaps[-1])
        results.append(rec)
        print(trial, rec, flush=True)
    json.dump(results, open('exp4_loop_k%d_s%s.json' % (k, sys.argv[1] if len(sys.argv) > 1 else '5'), 'w'), indent=1)
