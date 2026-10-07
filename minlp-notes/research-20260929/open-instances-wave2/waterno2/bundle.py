"""Disaggregated trust-region cutting-plane (bundle) method for the window
Lagrangian dual of waterno2_T.

u = (lam[0..T-2][0..2], mu), mu >= 0.  For each window W the function
phi_W(u) = min_{x in X_W} f_W(x) + (Lagrangian terms of W) is concave; its
value is SCIP's dual bound (a lower bound) and its supergradient is read from
SCIP's incumbent (exact when the solve closes the gap).  The master problem is
the LP
    max  sum_W r_W + c*mu
    s.t. r_W <= phi_W(u_j) + g_Wj.(u - u_j)   for all stored cuts j,
         |u - center|_inf <= Delta,  mu >= 0,
solved by HiGHS.  The bound reported is always a function value L(u) at an
evaluated point, never the model value.

usage: python3 bundle.py T windowsize iters out.json [start.json|-] [workers] [timelimit]
"""
import os
import sys
import json
import time
import multiprocessing as mp

import numpy as np
from scipy.optimize import linprog

import period

_D = None


def _init(T):
    global _D
    _D = period.setup(T, os.environ.get("WATERNO2_IMPLIED"))


def _solve(args):
    t0, t1, lam, mu, tl, params = args
    return period.solve_window(_D, t0, t1, lam, mu, tl, params)


def unpack(u, T):
    lam = [list(map(float, u[3 * t:3 * t + 3])) for t in range(T - 1)]
    return lam, float(u[-1])


def pack(lam, mu):
    return np.array([v for l in lam for v in l] + [mu], dtype=float)


def window_supergradient(D, t0, t1, x):
    """Supergradient of phi_W wrt u at minimizer x (dict var -> value)."""
    T = D["T"]
    g = np.zeros(3 * (T - 1) + 1)
    S = D["S"]
    for t in range(max(t0 - 1, 0), min(t1, T - 1)):
        ia = t0 <= t < t1
        ib = t0 <= t + 1 < t1
        if ia and ib:
            continue
        for k, (i, a, b) in enumerate(S["link"][t]):
            if ia:
                g[3 * t + k] -= x[a]
            if ib:
                g[3 * t + k] += x[b]
    for v, a in D["hor"].items():
        if t0 <= D["per_of"][v] < t1:
            g[-1] -= float(a) * x[v]
    return g


def evaluate(pool, D, u, windows, tl, params=None):
    lam, mu = unpack(u, D["T"])
    res = pool.map(_solve, [(a, b, lam, mu, tl, params) for a, b in windows])
    vals = np.array([r["dual"] for r in res])
    # objective value of the incumbent: the cut uses it (valid for any feasible x)
    prims = np.array([r["primal"] for r in res])
    grads = [window_supergradient(D, r["t0"], r["t1"], r["x"]) for r in res]
    total = mu * float(D["hor_rhs"]) + vals.sum()
    return total, vals, prims, grads, res


def master(cuts, center, delta, c_hor, n):
    nw = len(cuts)
    # variables: u (n), r (nw); maximize -> minimize negative
    cvec = np.zeros(n + nw)
    cvec[n - 1] = -c_hor
    cvec[n:] = -1.0
    A, b = [], []
    for w in range(nw):
        for (fv, g, uj) in cuts[w]:
            row = np.zeros(n + nw)
            row[:n] = -g
            row[n + w] = 1.0
            A.append(row)
            b.append(fv - g @ uj)
    bounds = [(center[i] - delta, center[i] + delta) for i in range(n)]
    bounds[n - 1] = (max(0.0, center[n - 1] - delta), center[n - 1] + delta)
    bounds += [(None, None)] * nw
    sol = linprog(cvec, A_ub=np.array(A), b_ub=np.array(b), bounds=bounds, method="highs")
    assert sol.status == 0, sol.message
    return sol.x[:n], -sol.fun


NOPROP = {"propagating/maxrounds": 0, "propagating/maxroundsroot": 0}


def consistent(vals, u, cuts):
    """phi_W(u) <= obj(x_j; u) = cut_j(u) for every stored incumbent x_j; SCIP's
    claimed optimum is replaced by the smallest such value when it is larger
    (SCIP was observed to claim optimality at non-optimal values)."""
    out = vals.copy()
    nfix = 0
    for w in range(len(cuts)):
        for (fv, g, uj) in cuts[w]:
            c = fv + g @ (u - uj)
            if c < out[w] - 1e-7:
                out[w] = c
                nfix += 1
    return out, nfix


def run(T, wsize, iters, out, start=None, workers=6, tl=300.0, delta=5.0, tol=1e-3, params=NOPROP):
    D = period.setup(T, os.environ.get("WATERNO2_IMPLIED"))
    if isinstance(wsize, int):
        windows = [(a, min(a + wsize, T)) for a in range(0, T, wsize)]
    else:
        windows = wsize
    n = 3 * (T - 1) + 1
    cuts = [[] for _ in windows]
    if start:
        s = json.load(open(start))
        u = pack(s["lam"], s["mu"])
        if s.get("windows") == [list(w) for w in windows] and "cuts" in s:
            cuts = [[(c[0], np.array(c[1]), np.array(c[2])) for c in cw] for cw in s["cuts"]]
            delta = s.get("delta", delta)
    else:
        u = np.zeros(n)
    u[-1] = max(u[-1], 0.0)
    pool = mp.Pool(workers, initializer=_init, initargs=(T,))
    c_hor = float(D["hor_rhs"])
    log = []
    tic = time.time()
    fc, vals, prims, grads, res = evaluate(pool, D, u, windows, tl, params)
    vals, nfix = consistent(vals, u, cuts)
    fc = u[-1] * c_hor + vals.sum()
    center, fcenter, cvals = u.copy(), fc, vals.copy()
    best = dict(bound=fc, u=u.tolist(), vals=vals.tolist(), status=[r["status"] for r in res])
    for w in range(len(windows)):
        cuts[w].append((prims[w] if np.isfinite(prims[w]) else vals[w], grads[w], u.copy()))
    print(f"it 0 L={fc:.6f} time={time.time()-tic:.1f}", flush=True)
    for it in range(1, iters + 1):
        # later incumbents may reveal that SCIP overestimated phi at the center
        cvals, _ = consistent(cvals, center, cuts)
        fcenter = center[-1] * c_hor + cvals.sum()
        unew, model_val = master(cuts, center, delta, c_hor, n)
        pred = model_val - fcenter
        if pred < tol:
            print(f"stop: predicted increase {pred:.2e} < tol", flush=True)
            break
        fn, vals, prims, grads, res = evaluate(pool, D, unew, windows, tl, params)
        vals, nfix = consistent(vals, unew, cuts)
        fn = unew[-1] * c_hor + vals.sum()
        for w in range(len(windows)):
            # cut through the incumbent value: phi(u) <= obj(x_j; u) for all u
            cuts[w].append((prims[w] if np.isfinite(prims[w]) else vals[w], grads[w], unew.copy()))
        gaps = [(r_["primal"] - r_["dual"]) for r_ in res]
        rho = (fn - fcenter) / pred
        if rho >= 0.1:
            step = "serious"
            if rho >= 0.5 and np.max(np.abs(unew - center)) >= 0.99 * delta:
                delta *= 2.0
            center, fcenter, cvals = unew.copy(), fn, vals.copy()
        else:
            step = "null"
            if rho < 0:
                delta = max(delta / 2.0, 1e-4)
        bv, _ = consistent(np.array(best["vals"]), np.array(best["u"]), cuts)
        best["vals"] = bv.tolist()
        best["bound"] = best["u"][-1] * c_hor + float(bv.sum())
        if fn > best["bound"]:
            best = dict(bound=fn, u=unew.tolist(), vals=vals.tolist(),
                        status=[r_["status"] for r_ in res], gaps=gaps)
        log.append(dict(it=it, L=fn, center=fcenter, pred=pred, delta=delta, step=step,
                        maxgap=max(gaps), fixes=nfix, time=time.time() - tic))
        print(f"it {it} L={fn:.6f} center={fcenter:.6f} pred={pred:.3e} delta={delta:.3g} {step} "
              f"maxsubgap={max(gaps):.2e} fixes={nfix} time={time.time()-tic:.1f}", flush=True)
        for w in range(len(windows)):
            if len(cuts[w]) > 200:
                cuts[w] = cuts[w][-200:]
        lam, mu = unpack(np.array(best["u"]), T)
        json.dump(dict(T=T, windows=windows, best_bound=best["bound"], lam=lam, mu=mu, best=best,
                       delta=delta, log=log,
                       cuts=[[(float(c[0]), c[1].tolist(), c[2].tolist()) for c in cw] for cw in cuts]),
                  open(out, "w"))
    pool.close()
    return best


if __name__ == "__main__":
    T = int(sys.argv[1])
    ws = int(sys.argv[2])
    iters = int(sys.argv[3])
    out = sys.argv[4]
    start = sys.argv[5] if len(sys.argv) > 5 and sys.argv[5] != "-" else None
    workers = int(sys.argv[6]) if len(sys.argv) > 6 else 6
    tl = float(sys.argv[7]) if len(sys.argv) > 7 else 300.0
    prm = {} if os.environ.get("WATERNO2_SCIP") == "default" else NOPROP
    run(T, ws, iters, out, start, workers, tl, params=prm)
