"""Primal improvement for waterno2_T by window re-optimization (large
neighbourhood search): all periods outside a window of consecutive periods
are fixed at the incumbent, and SCIP solves the window MINLP with the true
objective, the link rows to the fixed neighbours, and the horizon row
restricted to the window.  Accepted points are re-checked exactly
(evalpt.evaluate, rational arithmetic).

usage: python3 primal.py T start.(sol|json) out.json wsize [timelimit] [passes]
"""
import sys
import json
import time
from fractions import Fraction

import pyscipopt as ps

import period
import evalpt


def window_reopt(D, x, t0, t1, tl, feastol=1e-9):
    M, S, T = D["M"], D["S"], D["T"]
    objc = period.window_objective(D, t0, t1, [[0.0] * 3 for _ in range(T - 1)], 0.0)
    m, X = period.build(D, t0, t1, objc, {"numerics/feastol": feastol, "limits/time": tl})
    if t0 > 0:
        for (i, a, b) in S["link"][t0 - 1]:
            m.addCons(X[b] == x[a])
    if t1 < T:
        for (i, a, b) in S["link"][t1 - 1]:
            m.addCons(X[a] == x[b])
    rest = sum(float(a) * x[v] for v, a in D["hor"].items() if not (t0 <= D["per_of"][v] < t1))
    m.addCons(ps.quicksum(float(a) * X[v] for v, a in D["hor"].items() if t0 <= D["per_of"][v] < t1)
              >= float(D["hor_rhs"]) - rest)
    s = m.createSol()
    for v in X:
        m.setSolVal(s, X[v], x[v])
    m.addSol(s, free=True)
    m.optimize()
    out = None
    if m.getNSols() > 0:
        sol = m.getBestSol()
        out = {v: m.getSolVal(sol, X[v]) for v in X}
        for v in X:
            if M["vt"][v] == "B":
                out[v] = float(round(out[v]))
    res = dict(status=m.getStatus(), primal=m.getPrimalbound() if m.getNSols() else None,
               dual=m.getDualbound())
    m.freeProb()
    return out, res


def exact_eval(M, x):
    return evalpt.evaluate(M, [Fraction(v) for v in x])


def run(T, start, out, wsize, tl=120.0, passes=2, maxviol=1e-8):
    D = period.setup(T)
    M = D["M"]
    if start.endswith(".json"):
        x = [float(v) for v in json.load(open(start))["x"]]
    else:
        xs, _ = evalpt.read_sol(start, M["names"])
        x = [float(v) for v in xs]
    e = exact_eval(M, x)
    best = float(e["obj"])
    print(f"start obj={best:.9f} maxrow={float(e['maxrow']):.2e}", flush=True)
    tic = time.time()
    for p in range(passes):
        improved = False
        for t0 in range(0, T - wsize + 1):
            t1 = t0 + wsize
            xw, r = window_reopt(D, x, t0, t1, tl)
            if xw is None:
                continue
            y = list(x)
            for v, val in xw.items():
                y[v] = val
            e = exact_eval(M, y)
            ok = float(e["maxrow"]) <= maxviol and float(e["maxbnd"]) <= maxviol and e["int_ok"]
            if ok and float(e["obj"]) < best - 1e-9:
                x, best, improved = y, float(e["obj"]), True
            print(f"pass {p} window {t0}-{t1-1}: {r['status']} win_primal={r['primal']} "
                  f"win_dual={r['dual']:.6f} total={float(e['obj']):.9f} viol={float(e['maxrow']):.1e} "
                  f"{'ACCEPT' if ok and x is y else ''} best={best:.9f} t={time.time()-tic:.0f}", flush=True)
            json.dump(dict(T=T, obj=best, x=[repr(v) for v in x]), open(out, "w"))
        if not improved:
            break
    return best


if __name__ == "__main__":
    T = int(sys.argv[1])
    run(T, sys.argv[2], sys.argv[3], int(sys.argv[4]),
        float(sys.argv[5]) if len(sys.argv) > 5 else 120.0,
        int(sys.argv[6]) if len(sys.argv) > 6 else 2)
