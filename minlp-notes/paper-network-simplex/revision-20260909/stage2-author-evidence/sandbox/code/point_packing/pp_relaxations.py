"""Check point-packing RLT / SDP values from Anstreicher (2009), Conjecture 4.
PP: max theta s.t. (x_i-x_j)^2+(y_i-y_j)^2 >= theta, x,y in [0,1]^n.
RLT: McCormick products of bound constraints on X (for x) and Y (for y).  SDP: X - xx^T >= 0 plus X_ii <= x_i.
SYM: x_i in [.5,1] for i < ceil(n/2), y_i in [.5,1] for i < ceil(n/4).
Explicit floor/round conventions are exploratory variants, not published SYM.
The published ORD relaxation is not implemented. Numerical checks are not proofs.
"""
import math

import numpy as np
import cvxpy as cp
import gurobipy as gp
from gurobipy import GRB

def bounds(n, sym=False, conv="ceil"):
    if not isinstance(n, int) or isinstance(n, bool) or n < 2:
        raise ValueError("Point packing requires an integer n >= 2")
    if conv not in ("floor", "ceil", "round"):
        raise ValueError("Unknown symmetry rounding convention: " + str(conv))
    lx = np.zeros(n); ly = np.zeros(n)
    if sym:
        if conv == "floor": nx = n // 2; ny = nx // 2
        elif conv == "ceil": nx = -(-n // 2); ny = -(-nx // 2)
        elif conv == "round": nx = int(round(n / 2)); ny = int(round(nx / 2))
        lx[:nx] = 0.5; ly[:ny] = 0.5
    return lx, np.ones(n), ly, np.ones(n)

def rlt_lp(n, sym=False, conv="ceil"):
    lx, ux, ly, uy = bounds(n, sym, conv)
    m = gp.Model(); m.Params.OutputFlag = 0
    x = m.addVars(n, lb=lx, ub=ux); y = m.addVars(n, lb=ly, ub=uy)
    X = m.addVars(n, n, lb=-GRB.INFINITY); Y = m.addVars(n, n, lb=-GRB.INFINITY)
    th = m.addVar(lb=-GRB.INFINITY)
    for (V, v, l, u) in ((X, x, lx, ux), (Y, y, ly, uy)):
        for i in range(n):
            for j in range(i, n):
                m.addConstr(V[i, j] == V[j, i])
                m.addConstr(V[i, j] - l[i]*v[j] - l[j]*v[i] >= -l[i]*l[j])
                m.addConstr(V[i, j] - u[i]*v[j] - u[j]*v[i] >= -u[i]*u[j])
                m.addConstr(V[i, j] - l[i]*v[j] - u[j]*v[i] <= -l[i]*u[j])
                m.addConstr(V[i, j] - l[j]*v[i] - u[i]*v[j] <= -l[j]*u[i])
    for i in range(n):
        for j in range(i + 1, n):
            m.addConstr(X[i, i] - 2*X[i, j] + X[j, j] + Y[i, i] - 2*Y[i, j] + Y[j, j] >= th)
    m.setObjective(th, GRB.MAXIMIZE); m.optimize()
    status = m.Status
    if status != GRB.OPTIMAL:
        m.dispose()
        raise RuntimeError(f"RLT solve failed for n={n}, sym={sym}: Gurobi status {status}")
    value = float(m.ObjVal)
    m.dispose()
    if not math.isfinite(value):
        raise RuntimeError("RLT solver returned a nonfinite objective")
    return value

def sdp(n, sym=False, conv="ceil", rlt=False):
    lx, ux, ly, uy = bounds(n, sym, conv)
    x = cp.Variable(n); y = cp.Variable(n); X = cp.Variable((n, n), symmetric=True); Y = cp.Variable((n, n), symmetric=True)
    th = cp.Variable()
    cons = [lx <= x, x <= ux, ly <= y, y <= uy]
    for (V, v, l, u) in ((X, x, lx, ux), (Y, y, ly, uy)):
        M = cp.bmat([[np.ones((1, 1)), cp.reshape(v, (1, n), order='C')], [cp.reshape(v, (n, 1), order='C'), V]])
        cons.append(M >> 0)
        cons.append(cp.diag(V) <= cp.multiply(l+u, v) - l*u)
    if rlt:
        for (V, v, l, u) in ((X, x, lx, ux), (Y, y, ly, uy)):
            for i in range(n):
                for j in range(i, n):
                    cons += [V[i, j] - l[i]*v[j] - l[j]*v[i] >= -l[i]*l[j], V[i, j] - u[i]*v[j] - u[j]*v[i] >= -u[i]*u[j],
                             V[i, j] - l[i]*v[j] - u[j]*v[i] <= -l[i]*u[j], V[i, j] - l[j]*v[i] - u[i]*v[j] <= -l[j]*u[i]]
    for i in range(n):
        for j in range(i + 1, n):
            cons.append(X[i, i] - 2*X[i, j] + X[j, j] + Y[i, i] - 2*Y[i, j] + Y[j, j] >= th)
    p = cp.Problem(cp.Maximize(th), cons); p.solve(solver=cp.CLARABEL)
    if p.status != cp.OPTIMAL:
        raise RuntimeError(f"SDP solve failed for n={n}, sym={sym}, rlt={rlt}: {p.status}")
    if th.value is None or not math.isfinite(float(th.value)):
        raise RuntimeError("SDP solver returned no finite objective")
    return float(th.value)


def conjecture_4_values(n):
    """Return the four published values; SYM claims apply only for n >= 5."""
    bounds(n)
    return (
        2.0,
        1 + 1 / (n - 1),
        0.5 if n >= 5 else None,
        0.25 * (1 + 1 / ((n - 1) // 4)) if n >= 5 else None,
    )

if __name__ == "__main__":
    print("Published SYM uses ceilings. Each pair of columns is computed / Conjecture 4.")
    print("SYM formulas are n/a for n < 5; all computed values require optimal solver status.")
    print(" n | RLT / C4(1) | SDP / C4(2) | SDP+RLT | RLT+SYM / C4(3) | SDP+SYM / C4(4) | SDP+SYM+RLT")
    for n in range(2, 15):
        r = rlt_lp(n); s = sdp(n); sr = sdp(n, rlt=True)
        rs = rlt_lp(n, sym=True)
        ss = sdp(n, sym=True)
        ssr = sdp(n, sym=True, rlt=True) if n >= 5 else None
        expected = conjecture_4_values(n)
        comparisons = list(zip(("RLT", "SDP", "RLT+SYM", "SDP+SYM"), (r, s, rs, ss), expected))
        comparisons += [("SDP+RLT", sr, expected[1]), ("SDP+SYM+RLT", ssr, expected[3])]
        for label, actual, target in comparisons:
            if target is not None and not math.isclose(actual, target, rel_tol=1e-6, abs_tol=1e-6):
                raise AssertionError(f"n={n}, {label}: computed {actual}, expected {target}")
        columns = [f"{actual:.6f} / {target:.6f}" if target is not None else f"{actual:.6f} / n/a"
                   for actual, target in zip((r, s, rs, ss), expected)]
        ssr_column = f"{ssr:.6f}" if ssr is not None else "n/a"
        print(f"{n:2d} | {columns[0]} | {columns[1]} | {sr:.6f} | {columns[2]} | {columns[3]} | {ssr_column}", flush=True)
    print("All applicable formula checks passed (absolute and relative tolerances 1e-6).")
