"""Period (or window) Lagrangian subproblems of waterno2_T, solved by SCIP.

Relaxed rows: the 3(T-1) tank-level link rows  -x_end(t) + x_start(t+1) = 0
(multiplier lam[t][k], free) and the horizon row  sum_t a_t h_t >= c
(multiplier mu >= 0).  The Lagrangian

  L(lam, mu) = mu*c + sum_W  min_{x_W in X_W} [ f_W(x_W) + (linear terms) ]

splits over windows W of consecutive periods (a window keeps the link rows
between its own periods).  Each window problem is solved by SCIP.
"""
import math
import time
from fractions import Fraction

import pyscipopt as ps

import wmodel


def setup(T, implied=None):
    """implied: optional JSON file of implied variable bounds (implied.py);
    they are intersected with the OSIL bounds of the window models."""
    M = wmodel.load(T)
    S = wmodel.structure(M)
    assert len(S["horizon"]) == 1
    h = M["rows"][S["horizon"][0]]
    assert h["ub"].upper() in ("INF", "+INF")
    hor = {mono[0]: Fraction(a) for mono, a in h["poly"].items()}
    per_of = {}
    for t, vs in enumerate(S["per_vars"]):
        for v in vs:
            per_of[v] = t
    extra = {}
    if implied:
        import json
        B = json.load(open(implied))
        assert B["T"] == T
        idx = {n: i for i, n in enumerate(M["names"])}
        extra = {idx[n]: (float(a), float(b)) for n, (a, b) in B["bounds"].items()}
    D = dict(M=M, S=S, T=T, hor=hor, hor_rhs=Fraction(h["lb"]), per_of=per_of, extra=extra, nogood={})
    import os
    ng = os.environ.get("WATERNO2_NOGOOD")
    if ng:
        import json
        import probe_config
        K = json.load(open(ng))
        assert K["T"] == T
        for t in range(T):
            keep = {tuple(c) for c in K["keep"][str(t)]}
            D["nogood"][t] = [box for counts, box in probe_config.configs(D, t) if counts not in keep]
    return D


def window_objective(D, t0, t1, lam, mu):
    """Linear objective of window periods t0..t1-1: {var: coef(float)}."""
    M, S = D["M"], D["S"]
    c = {}
    for t in range(t0, t1):
        for v in S["per_vars"][t]:
            if v in M["obj"]:
                c[v] = c.get(v, 0.0) + float(Fraction(M["obj"][v]))
    # link rows entering/leaving the window: -x_a + x_b, a in t, b in t+1
    for t in range(max(t0 - 1, 0), min(t1, D["T"] - 1)):
        inside_a = t0 <= t < t1
        inside_b = t0 <= t + 1 < t1
        if inside_a and inside_b:
            continue  # kept as a constraint
        for k, (i, a, b) in enumerate(S["link"][t]):
            if inside_a:
                c[a] = c.get(a, 0.0) - lam[t][k]
            if inside_b:
                c[b] = c.get(b, 0.0) + lam[t][k]
    for v, a in D["hor"].items():
        if t0 <= D["per_of"][v] < t1:
            c[v] = c.get(v, 0.0) - mu * float(a)
    return c


def build(D, t0, t1, objc, params=None, box=None):
    """SCIP model of window t0..t1-1 with linear objective objc.
    box: optional {var: (lo, hi)} intersected with the variable bounds."""
    M, S = D["M"], D["S"]
    m = ps.Model()
    m.hideOutput()
    m.setParam("parallel/maxnthreads", 1)
    m.setParam("lp/threads", 1)
    for k, v in (params or {}).items():
        m.setParam(k, v)
    vs = [v for t in range(t0, t1) for v in S["per_vars"][t]]
    X = {}
    for v in vs:
        lb = M["lb"][v]
        ub = M["ub"][v]
        lb = None if lb.upper() in ("-INF", "INF") else float(lb)
        ub = None if ub.upper() in ("INF", "+INF") else float(ub)
        for src in (D.get("extra", {}), box or {}):
            if v in src:
                el, eu = src[v]
                lb = el if lb is None else max(lb, el)
                ub = eu if ub is None else min(ub, eu)
        if lb is not None and ub is not None and lb > ub:
            raise ValueError("empty variable domain")
        X[v] = m.addVar(name=M["names"][v], vtype="B" if M["vt"][v] == "B" else "C", lb=lb, ub=ub)
    rows = [i for t in range(t0, t1) for i in S["per_rows"][t]]
    rows += [i for t in range(t0, t1 - 1) for (i, a, b) in S["link"][t]]
    for i in rows:
        r = M["rows"][i]
        e = 0
        for mono, a in r["poly"].items():
            term = float(a)
            for v in mono:
                term = term * X[v]
            e = e + term
        lb, ub = r["lb"], r["ub"]
        lbf = None if lb.upper() in ("-INF",) else float(lb)
        ubf = None if ub.upper() in ("INF", "+INF") else float(ub)
        if lbf is not None and ubf is not None and lbf == ubf:
            m.addCons(e == lbf, name=r["name"])
        else:
            if lbf is not None:
                m.addCons(e >= lbf, name=r["name"] + "_lo")
            if ubf is not None:
                m.addCons(e <= ubf, name=r["name"] + "_up")
    # no-good rows excluding pump configurations (Lagrangian probing, probe_config.py)
    for t in range(t0, t1):
        for box in D.get("nogood", {}).get(t, []):
            m.addCons(ps.quicksum((1 - X[v]) if lohi[0] == 1.0 else X[v] for v, lohi in box.items()) >= 1)
    m.setObjective(ps.quicksum(a * X[v] for v, a in objc.items()), "minimize")
    return m, X


def solve_window(D, t0, t1, lam, mu, timelimit=600.0, params=None, box=None):
    objc = window_objective(D, t0, t1, lam, mu)
    m, X = build(D, t0, t1, objc, params, box)
    m.setParam("limits/time", timelimit)
    tic = time.time()
    m.optimize()
    el = time.time() - tic
    st = m.getStatus()
    db = m.getDualbound()
    pb = m.getPrimalbound() if m.getNSols() > 0 else math.inf
    xs = None
    if m.getNSols() > 0:
        sol = m.getBestSol()
        xs = {v: m.getSolVal(sol, X[v]) for v in X}
    res = dict(t0=t0, t1=t1, status=st, dual=db, primal=pb, time=el,
               nodes=m.getNNodes(), x=xs)
    m.freeProb()
    return res


def lagrangian(D, lam, mu, windows=None, timelimit=600.0, params=None):
    """Return (bound, subgradient info, per-window results)."""
    T = D["T"]
    if windows is None:
        windows = [(t, t + 1) for t in range(T)]
    res = [solve_window(D, a, b, lam, mu, timelimit, params) for a, b in windows]
    val = mu * float(D["hor_rhs"]) + sum(r["dual"] for r in res)
    return val, res, windows


def subgradient(D, res, windows):
    """Subgradient of L at the subproblem minimizers (rows' residuals)."""
    S = D["S"]
    x = {}
    for r in res:
        x.update(r["x"])
    T = D["T"]
    g_lam = []
    for t in range(T - 1):
        g_lam.append([x[b] - x[a] if (a in x and b in x) else 0.0 for (i, a, b) in S["link"][t]])
    g_mu = float(D["hor_rhs"]) - sum(float(a) * x[v] for v, a in D["hor"].items())
    # links inside a window are kept, their residual is 0 by feasibility
    return g_lam, g_mu, x
