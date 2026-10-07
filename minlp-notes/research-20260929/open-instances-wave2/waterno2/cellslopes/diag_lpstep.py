"""Diagnosis of the first rejected local LP step of planB (planning values only).

Re-solves the LP that planB solved at its first iteration (state logs/planA.pkl,
120 cells nearest the optimum, trust region (0.75, 0.75, 1.875)), sets its slopes,
and compares the pool-model values before evaluation (planA's points) with the
values after evaluation (planB's points, which include SCIP runs at these
slopes) along the minimizing path after evaluation.
usage: python3 diag_lpstep.py
"""
import copy
import pickle

import numpy as np

import cs

A = cs.load("logs/planA.pkl.gz")
B = cs.load("logs/planB.pkl.gz")
T = 6
inc = A.incidence_full()
tab = A.tables(inc)
M = A.model(tab)
V, f, g = A.dp(M)
cand = []
for link in range(T - 1):
    psi = f[link] + g[link]
    for pos in np.nonzero(psi < V + 0.3)[0]:
        cand.append((float(psi[pos]), link, int(pos)))
cand.sort()
active = [np.zeros(len(A.leaves[l]), bool) for l in range(T - 1)]
for (p, l, pos) in cand[:120]:
    active[l][pos] = True
z, new, info = cs.slope_lp(A, tab, inc, [0.75, 0.75, 1.875], active=active, pmargin=5.0)
print("planning value before the step", round(V, 4), "LP value z", round(z, 4))
A2 = copy.deepcopy(A)
cs.set_slopes(A2, new)
tabp = A2.tables(inc)
Mp = A2.model(tabp)
print("pool model at the new slopes before evaluation", round(A2.dp(Mp)[0], 4))
A2.pts, A2.evals, A2.scip_inf = B.pts, B.evals, B.scip_inf
inc2 = A2.incidence_full()
tabq = A2.tables(inc2)
Mq = A2.model(tabq)
Vq, fq, gq = A2.dp(Mq)
print("after the SCIP evaluations of planB at these slopes", round(Vq, 4))
path = A2.best_path(Mq, fq, gq)
print("minimizing path after evaluation (leaf positions)", path)
for t in range(T):
    r = 0 if t == 0 else path[t - 1]
    c = 0 if t == T - 1 else path[t]
    print(f"  period {t}: predicted {Mp[t][r, c]:.3f}  after evaluation {Mq[t][r, c]:.3f}  "
          f"(old slopes {M[t][r, c]:.3f})")
