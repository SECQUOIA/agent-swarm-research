"""Worker tasks: SCIP estimates (planning only) and rbb bounds (certificates)
for one period on one (entry cell, exit cell) pair."""
import math
import time

import numpy as np

import core
import terminal

INF = math.inf
_W = {}


def init(T, implied, term):
    D = core.setup(T, implied)
    if term:
        terminal.add_terminal_row(D)
    _W["D"] = D
    _W["PB"] = {}


def _box(D, t, cin, cout):
    S = D["S"]
    box = {}
    if cin is not None:
        for k, (i, va, vb) in enumerate(S["link"][t - 1]):
            box[vb] = (float(cin[0][k]), float(cin[1][k]))
    if cout is not None:
        for k, (i, va, vb) in enumerate(S["link"][t]):
            box[va] = (float(cout[0][k]), float(cout[1][k]))
    return box


def scip_task(a):
    """SCIP (no propagation) on the pair: value of its incumbent and the
    incumbent's start / end levels.  Planning only, never a bound."""
    import period
    import bundle
    key, t, cin, cout, lam_in, lam_out, mu, tl = a
    D = _W["D"]
    T = D["T"]
    lam = [[0.0, 0.0, 0.0] for _ in range(T - 1)]
    if t > 0:
        lam[t - 1] = list(lam_in)
    if t < T - 1:
        lam[t] = list(lam_out)
    tic = time.time()
    est, s, e, st = INF, None, None, "none"
    try:
        r = period.solve_window(D, t, t + 1, lam, mu, tl, bundle.NOPROP, _box(D, t, cin, cout))
        st = r["status"]
        if r["x"] is not None:
            est = float(r["primal"])
            x = r["x"]
            S = D["S"]
            s = [x[b] for (i, a_, b) in S["link"][t - 1]] if t > 0 else None
            e = [x[a_] for (i, a_, b) in S["link"][t]] if t < T - 1 else None
        elif st == "infeasible":
            est = INF
        else:
            est = math.nan  # no solution and no proof: unknown
    except ValueError:
        st = "empty"
    return key, dict(est=est, status=st, s=s, e=e, time=time.time() - tic)


def rbb_task(a):
    """Rigorous lower bound on the pair (core.PeriodBounder -> rbb.solve)."""
    key, t, cin, cout, lam_in, lam_out, mu, target, node_limit, time_limit = a
    D = _W["D"]
    if t not in _W["PB"]:
        _W["PB"][t] = core.PeriodBounder(D, t)
    PB = _W["PB"][t]
    ci = None if cin is None else (np.array(cin[0]), np.array(cin[1]))
    co = None if cout is None else (np.array(cout[0]), np.array(cout[1]))
    tic = time.time()
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        res = PB.bound(ci, co, lam_in, lam_out, mu, target, node_limit=node_limit, time_limit=time_limit)
        retry = None
        if res["bound"] < target and res.get("nodes", 0) < node_limit and time.time() - tic < time_limit:
            # rbb keeps the bound of a node it cannot branch on; this happens when
            # reduced-cost tightening shrinks the box around the LP point.  Retry
            # without reduced-cost tightening and keep the larger (valid) bound.
            r2 = PB.bound(ci, co, lam_in, lam_out, mu, target, node_limit=node_limit,
                          time_limit=time_limit, rc=False)
            retry = dict(bound=float(r2["bound"]), status=r2["status"], nodes=int(r2.get("nodes", 0)))
            if r2["bound"] > res["bound"]:
                res = dict(r2, nodes=res.get("nodes", 0) + r2.get("nodes", 0))
    return key, dict(bound=float(res["bound"]), status=res["status"], nodes=int(res.get("nodes", 0)), retry=retry,
                     time=time.time() - tic, target=float(target), lam_in=[float(v) for v in lam_in],
                     lam_out=[float(v) for v in lam_out], mu=float(mu), cin_box=cin, cout_box=cout)
