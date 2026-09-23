"""K=2, box pool qualities [a,b], single bypass quality beta<0 (y = beta z).
Check numerically that conv(T) = conv of the union of the pieces
  zero boxes, per-attribute curves (other attribute at a bound), the ridge (both bind), x=1 face,
by comparing support functions (LP over sampled pieces) with exact max over T (Gurobi)."""
import itertools, json, sys
import numpy as np
import gurobipy as gp
from gurobipy import GRB
ENV = gp.Env(params={"OutputFlag": 0})

def pieces(a, b, beta, n=int(sys.argv[3]) if len(sys.argv) > 3 else 400):
    P = []
    phi = lambda k, t: 1.0 if t <= 0 else min(1.0, -beta[k] / (t - beta[k]))
    for t in itertools.product(*[(a[k], b[k]) for k in range(2)]):
        P.append((0, 0, 0, 0, *t)); P.append((0, 1, 0, 0, *t))
    # x = 1 face: t <= 0
    if all(a <= 0):
        for t in itertools.product(*[(a[k], min(b[k], 0.0)) for k in range(2)]):
            P.append((1, 0, *t, *t))
    for k in range(2):
        o = 1 - k
        for tk in np.linspace(a[k], b[k], n):
            x = phi(k, tk)
            for to in (a[o], b[o]):
                if x * to + beta[o] * (1 - x) <= 1e-12:  # other attribute satisfied
                    t = [0, 0]; t[k] = tk; t[o] = to
                    P.append((x, 1 - x, x * t[0], x * t[1], *t))
    # ridge: both bind, t_k = -beta_k (1-x)/x
    for x in np.linspace(1e-4, 1, n):
        t = [-beta[k] * (1 - x) / x for k in range(2)]
        if all(a[k] - 1e-12 <= t[k] <= b[k] + 1e-12 for k in range(2)):
            P.append((x, 1 - x, x * t[0], x * t[1], *t))
    return np.array(P, float)

def hK(c, a, b, beta):
    m = gp.Model(env=ENV); m.Params.NonConvex = 2; m.Params.MIPGap = 1e-9; m.Params.MIPGapAbs = 1e-9
    x = m.addVar(0, 1); z = m.addVar(0, 1); t = m.addVars(2, lb=list(a), ub=list(b)); u = m.addVars(2, lb=-GRB.INFINITY)
    m.addConstr(x + z <= 1)
    for k in range(2):
        m.addConstr(u[k] == x * t[k]); m.addConstr(u[k] + beta[k] * z <= 0)
    m.setObjective(c[0] * x + c[1] * z + c[2] * u[0] + c[3] * u[1] + c[4] * t[0] + c[5] * t[1], GRB.MAXIMIZE)
    m.optimize(); return m.ObjBound

rng = np.random.default_rng(int(sys.argv[1]))
worst = 0
for trial in range(int(sys.argv[2])):
    a = rng.uniform(-2, 0.5, 2); b = a + rng.uniform(0.5, 3, 2); beta = -rng.uniform(0.2, 2.5, 2)
    Pts = pieces(a, b, beta)
    for _ in range(40):
        c = rng.normal(size=6)
        hp = (Pts @ c).max(); hk = hK(c, a, b, beta)
        worst = max(worst, hk - hp)
    print(trial, "max(h_exact - h_pieces) so far", worst, flush=True)
