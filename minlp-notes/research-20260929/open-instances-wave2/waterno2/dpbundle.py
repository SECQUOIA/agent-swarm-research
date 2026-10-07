"""Optimize the multipliers of the level-box DP bound (dpbox.py) by a
disaggregated trust-region cutting-plane method.

D(u) = mu*c + min over box sequences of sum_t phi_t(u; k_{t-1}, k_t) is
concave in u (a minimum of concave functions).  Each phi_t(.; i, j) gets its
own cutting-plane model; the master LP maximizes the DP value of the models
through potential variables:
    pi_{0,j} <= r_{0,.,j};  pi_{t,j} <= pi_{t-1,i} + r_{t,i,j};
    Dv <= pi_{T-2,i} + r_{T-1,i,.};  maximize Dv + c*mu.
SCIP (default settings) is only the oracle; values are corrected downward
whenever a stored incumbent shows that SCIP overestimated a minimum.

usage: python3 dpbundle.py T start.json splits out.json iters [workers]
"""
import os
import sys
import json
import time
import multiprocessing as mp

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix

import period
import bundle
import dpbox

_D = None


def _init(T):
    global _D
    _D = period.setup(T, os.environ.get("WATERNO2_IMPLIED"))


def _task(args):
    t, i, j, bin_, bout, lam, mu = args
    D = _D
    box = dpbox.period_box(D, t, bin_, bout)
    try:
        r = period.solve_window(D, t, t + 1, lam, mu, 120, {}, box)
    except ValueError:
        return (t, i, j, None)
    if r["x"] is None:
        return (t, i, j, None) if r["status"] == "infeasible" else (t, i, j, "fail")
    g = bundle.window_supergradient(D, t, t + 1, r["x"])
    return (t, i, j, (r["dual"], r["primal"], g.tolist()))


def main():
    T = int(sys.argv[1])
    start = json.load(open(sys.argv[2]))
    splits = [[float(p) for p in s.split(",") if p] for s in sys.argv[3].split(";")]
    out = sys.argv[4]
    iters = int(sys.argv[5])
    workers = int(sys.argv[6]) if len(sys.argv) > 6 else 5
    D = period.setup(T, os.environ.get("WATERNO2_IMPLIED"))
    boxes = [dpbox.boxes_for_boundary(D, t, splits) for t in range(T - 1)]
    keys = []
    for t in range(T):
        ins = [None] if t == 0 else list(range(len(boxes[t - 1])))
        outs = [None] if t == T - 1 else list(range(len(boxes[t])))
        keys += [(t, i, j) for i in ins for j in outs]
    kidx = {k: n for n, k in enumerate(keys)}
    n = 3 * (T - 1) + 1
    u = bundle.pack(start["lam"], start["mu"])
    c_hor = float(D["hor_rhs"])
    cuts = {k: [] for k in keys}
    infeasible = set()
    pool = mp.Pool(workers, initializer=_init, initargs=(T,))

    def evaluate(u):
        lam, mu = bundle.unpack(u, T)
        tasks = [(t, i, j, None if i is None else boxes[t - 1][i], None if j is None else boxes[t][j], lam, mu)
                 for (t, i, j) in keys if (t, i, j) not in infeasible]
        res = pool.map(_task, tasks, chunksize=1)
        phi = {}
        for (t, i, j, r) in res:
            if r is None:
                infeasible.add((t, i, j))
                continue
            if r == "fail":
                raise RuntimeError("SCIP found no point for a feasible box pair")
            dual, primal, g = r
            g = np.array(g)
            val = dual
            for (fv, gg, uj) in cuts[(t, i, j)]:
                val = min(val, fv + gg @ (u - uj))
            phi[(t, i, j)] = val
            cuts[(t, i, j)].append((primal, g, u.copy()))
        for k in infeasible:
            phi[k] = np.inf
        v, path = dpbox.dp(T, boxes, phi, u[-1] * c_hor)
        return v, path

    def master(center, delta):
        # variable layout: u (n) | r (K) | pi (sum of boxes) | Dv
        K = len(keys)
        pi_off = []
        off = n + K
        for t in range(T - 1):
            pi_off.append(off)
            off += len(boxes[t])
        dv = off
        N = off + 1
        rows, cols, vals, rhs = [], [], [], []
        m = 0
        for k, cl in cuts.items():
            if k in infeasible:
                continue
            for (fv, g, uj) in cl:
                # r_k - g.u <= fv - g.uj
                rows += [m] * (n + 1)
                cols += list(range(n)) + [n + kidx[k]]
                vals += list(-g) + [1.0]
                rhs.append(fv - g @ uj)
                m += 1
        for (t, i, j) in keys:
            if (t, i, j) in infeasible:
                continue
            r = n + kidx[(t, i, j)]
            if t == 0:
                rows += [m, m]; cols += [pi_off[0] + j, r]; vals += [1.0, -1.0]
            elif t == T - 1:
                rows += [m, m, m]; cols += [dv, pi_off[T - 2] + i, r]; vals += [1.0, -1.0, -1.0]
            else:
                rows += [m, m, m]; cols += [pi_off[t] + j, pi_off[t - 1] + i, r]; vals += [1.0, -1.0, -1.0]
            rhs.append(0.0)
            m += 1
        A = coo_matrix((vals, (rows, cols)), shape=(m, N)).tocsr()
        cvec = np.zeros(N)
        cvec[dv] = -1.0
        cvec[n - 1] = -c_hor
        bounds = [(center[q] - delta, center[q] + delta) for q in range(n)]
        bounds[n - 1] = (max(0.0, center[n - 1] - delta), center[n - 1] + delta)
        bounds += [(None, 1e6)] * (N - n)
        # keep the LP bounded: r and pi are bounded above through cuts; add a loose cap
        sol = linprog(cvec, A_ub=A, b_ub=np.array(rhs), bounds=bounds, method="highs")
        assert sol.status == 0, sol.message
        return sol.x[:n], -sol.fun

    tic = time.time()
    fc, path = evaluate(u)
    center, fcenter = u.copy(), fc
    best = dict(bound=fc, u=u.tolist(), path=path)
    delta = 5.0
    log = []
    print(f"it 0 D={fc:.6f} subproblems={len(keys)} time={time.time()-tic:.0f}", flush=True)
    for it in range(1, iters + 1):
        # re-validate the center value against the newest cuts
        lam, mu = bundle.unpack(center, T)
        unew, model = master(center, delta)
        pred = model - fcenter
        if pred < 1e-3:
            print("stop: predicted increase below tolerance", flush=True)
            break
        fn, path = evaluate(unew)
        rho = (fn - fcenter) / pred
        if rho >= 0.1:
            step = "serious"
            if rho >= 0.5 and np.max(np.abs(unew - center)) >= 0.99 * delta:
                delta *= 2
            center, fcenter = unew.copy(), fn
        else:
            step = "null"
            if rho < 0:
                delta = max(delta / 2, 1e-4)
        if fn > best["bound"]:
            best = dict(bound=fn, u=unew.tolist(), path=path)
        log.append(dict(it=it, D=fn, center=fcenter, pred=pred, delta=delta, step=step, time=time.time() - tic))
        print(f"it {it} D={fn:.6f} center={fcenter:.6f} pred={pred:.3e} delta={delta:.3g} {step} "
              f"path={path} time={time.time()-tic:.0f}", flush=True)
        lam_b, mu_b = bundle.unpack(np.array(best["u"]), T)
        json.dump(dict(T=T, splits=splits, best_bound=best["bound"], lam=lam_b, mu=mu_b, path=best["path"],
                       log=log), open(out, "w"))
    pool.close()


if __name__ == "__main__":
    main()
