"""Prototype: joint hull of bilinear terms t_i = x_i y_i with x on an equal-width row
(sum x_i = k w + r, 0 <= x_i <= w) and independent factors y_i in [0,1].
Compares, for random linear objectives: exact hull (vertex enumeration), state extended form (EF),
McCormick + row (MC), and MC plus level-1 RLT of the row and bounds with all cross products (RLT)."""
import itertools, sys
import numpy as np
import gurobipy as gp

rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 0)


def exact(n, k, w, r, cx, cy, ct):
    best = np.inf
    for S in itertools.combinations(range(n), k):
        for j in set(range(n)) - set(S):
            x = np.zeros(n); x[list(S)] = w; x[j] = r
            val = cx @ x + sum(min(0.0, cy[i] + ct[i] * x[i]) for i in range(n))   # y_i in {0,1} chosen freely
            best = min(best, val)
    return best


def lp(n, k, w, r, cx, cy, ct, mode):
    m = gp.Model(); m.Params.OutputFlag = 0
    x = m.addVars(n, lb=0, ub=w); y = m.addVars(n, lb=0, ub=1); t = m.addVars(n, lb=0, ub=w)
    B = k * w + r
    m.addConstr(x.sum() == B)
    for i in range(n):
        m.addConstr(t[i] <= x[i]); m.addConstr(t[i] <= w * y[i]); m.addConstr(t[i] >= x[i] + w * y[i] - w)
    if mode == "EF":
        s = m.addVars(n, 6, lb=0)      # states: (zero,y0),(zero,y1),(full,y0),(full,y1),(res,y0),(res,y1)
        for i in range(n):
            m.addConstr(gp.quicksum(s[i, q] for q in range(6)) == 1)
            m.addConstr(x[i] == w * (s[i, 2] + s[i, 3]) + r * (s[i, 4] + s[i, 5]))
            m.addConstr(y[i] == s[i, 1] + s[i, 3] + s[i, 5])
            m.addConstr(t[i] == w * s[i, 3] + r * s[i, 5])
        m.addConstr(gp.quicksum(s[i, 2] + s[i, 3] for i in range(n)) == k)
        m.addConstr(gp.quicksum(s[i, 4] + s[i, 5] for i in range(n)) == 1)
    if mode == "RLT":
        p = m.addVars(n, n, lb=0, ub=w)           # p[i,j] ~ x_i y_j ; p[i,i] = t_i
        for i in range(n):
            m.addConstr(p[i, i] == t[i])
            for j in range(n):
                m.addConstr(p[i, j] <= x[i]); m.addConstr(p[i, j] <= w * y[j]); m.addConstr(p[i, j] >= x[i] + w * y[j] - w)
        for j in range(n):                         # row times y_j and times (1-y_j)
            m.addConstr(gp.quicksum(p[i, j] for i in range(n)) == B * y[j])
    m.setObjective(gp.quicksum(cx[i] * x[i] + cy[i] * y[i] + ct[i] * t[i] for i in range(n)))
    m.optimize()
    return m.ObjVal


tot = {"MC": 0, "RLT": 0, "EF": 0}; cnt = 0
for trial in range(40):
    n = int(rng.integers(3, 7)); k = int(rng.integers(1, n)); k = min(k, n - 1)
    w = 1.0; r = float(rng.uniform(0.15, 0.85))
    cx, cy, ct = rng.normal(size=n), rng.normal(size=n), rng.normal(size=n)
    ex = exact(n, k, w, r, cx, cy, ct)
    vals = {mode: lp(n, k, w, r, cx, cy, ct, mode) for mode in ("MC", "RLT", "EF")}
    assert vals["EF"] <= ex + 1e-7 and abs(vals["EF"] - ex) < 1e-6, (vals, ex)
    cnt += 1
    for mode in vals:
        tot[mode] += (ex - vals[mode]) > 1e-6
    if trial < 8:
        print(f"n={n} k={k} r={r:.2f}: exact {ex:.4f}  MC {vals['MC']:.4f}  RLT {vals['RLT']:.4f}  EF {vals['EF']:.4f}")
print("instances with a gap:", tot, "of", cnt)
