"""Equal widths: compare the full family (F,T1,T2) of row-hull inequalities with the subfamily that
corresponds to tilted simple generalized flow covers of Lim-Linderoth-Luedtke at z=1 (|F|+|T2| = k+1)."""
import itertools
import numpy as np
import gurobipy as gp

rng = np.random.default_rng(1)
worse = 0
for trial in range(30):
    n = int(rng.integers(3, 7)); k = int(rng.integers(1, n - 1)) if n > 2 else 1
    r = float(rng.uniform(0.15, 0.85)); w = 1.0; B = k * w + r
    delta = rng.uniform(0.2, 1.0, n)
    c = rng.normal(size=n); om = rng.uniform(0.0, 1.0, n)
    vals = []
    for sub in (False, True):
        m = gp.Model(); m.Params.OutputFlag = 0
        z = m.addVars(n, lb=0, ub=w); t = m.addVars(n, lb=0)
        m.addConstr(z.sum() == B)
        for choice in itertools.product(range(3), repeat=n):   # 0: tau/delta, 1: z/r, 2: (w-z)/(w-r)
            F = [i for i in range(n) if choice[i] == 0]; T2 = [i for i in range(n) if choice[i] == 2]
            if sub and len(F) + len(T2) != k + 1:
                continue
            m.addConstr(gp.quicksum(t[i] / delta[i] if choice[i] == 0 else z[i] / r if choice[i] == 1
                                    else (w - z[i]) / (w - r) for i in range(n)) >= 1)
        m.setObjective(gp.quicksum(c[i] * z[i] + om[i] * t[i] for i in range(n)))
        m.optimize(); vals.append(m.ObjVal)
    if vals[1] < vals[0] - 1e-7:
        worse += 1
    print(f"n={n} k={k} r={r:.2f}: hull {vals[0]:.5f}  cover-subfamily {vals[1]:.5f}")
print("subfamily strictly weaker in", worse, "of 30 trials")
