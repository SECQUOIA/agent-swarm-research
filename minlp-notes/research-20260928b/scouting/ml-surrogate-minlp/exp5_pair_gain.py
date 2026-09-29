"""Experiment 5: how much does the exact 2-neuron hull tighten the intersection of the
two exact single-neuron hulls (Anderson et al.), for dense Gaussian weights on [0,1]^n?
Both hulls are written as Balas disjunctive extended formulations and solved with HiGHS.
Reported: relative excess (single - joint) / (max - min of the objective over the graph)."""
import numpy as np
from scipy.optimize import linprog
from itertools import product

rng = np.random.default_rng(11)

def balas_max(n, W, b, pieces_of, obj_x, obj_y):
    """max obj_x.x + obj_y.y over conv of graph restricted to given neuron groups.
    pieces_of: list of groups (tuples of neuron indices); for each group a Balas
    formulation over its 2^|group| activation patterns; groups share x."""
    k = len(W)
    # variables: x (n), y (k), and for each group g and pattern s: lambda_gs, x_gs (n)
    idx = {}; nv = n + k
    for g, grp in enumerate(pieces_of):
        for s in product([0, 1], repeat=len(grp)):
            idx[(g, s)] = nv; nv += 1 + n
    c = np.zeros(nv); c[:n] = -obj_x; c[n:n+k] = -obj_y
    Aeq, beq, Aub, bub = [], [], [], []
    for g, grp in enumerate(pieces_of):
        # sum lambda = 1 ; sum x_gs = x ; y_j = sum_s [s_j] (w_j x_gs + b_j lambda)
        r = np.zeros(nv)
        for s in product([0, 1], repeat=len(grp)): r[idx[(g, s)]] = 1
        Aeq.append(r); beq.append(1)
        for i in range(n):
            r = np.zeros(nv); r[i] = -1
            for s in product([0, 1], repeat=len(grp)): r[idx[(g, s)] + 1 + i] = 1
            Aeq.append(r); beq.append(0)
        for t, j in enumerate(grp):
            r = np.zeros(nv); r[n + j] = -1
            for s in product([0, 1], repeat=len(grp)):
                if s[t]:
                    base = idx[(g, s)]; r[base] += b[j]; r[base+1:base+1+n] += W[j]
            Aeq.append(r); beq.append(0)
        for s in product([0, 1], repeat=len(grp)):
            base = idx[(g, s)]
            for i in range(n):  # 0 <= x_gs <= lambda
                r = np.zeros(nv); r[base+1+i] = 1; r[base] = -1; Aub.append(r); bub.append(0)
            for t, j in enumerate(grp):  # sign constraints of the pattern
                r = np.zeros(nv); sign = -1 if s[t] else 1
                r[base] = sign * b[j]; r[base+1:base+1+n] = sign * W[j]
                Aub.append(r); bub.append(0)
    bounds = [(0, 1)] * n + [(None, None)] * k + [(0, None)] * (nv - n - k)
    res = linprog(c, A_ub=np.array(Aub), b_ub=np.array(bub), A_eq=np.array(Aeq), b_eq=np.array(beq),
                  bounds=bounds, method="highs")
    assert res.status == 0, res.message
    return -res.fun

print("n  trials  mean_rel_excess  median  max  frac>1%")
for n in [3, 5, 10, 20]:
    ex = []
    for trial in range(60):
        W = rng.normal(size=(2, n)); b = rng.normal(size=2) * 0.5 + (-W.clip(min=0).sum(1) - W.clip(max=0).sum(1)) / 2 * 0  # centered-ish
        # make both neurons unstable on the box
        lo = W.clip(max=0).sum(1); hi = W.clip(min=0).sum(1)
        b = -(lo + (hi - lo) * rng.uniform(0.2, 0.8, size=2))
        if rng.uniform() < 0.5:  # correlated pair
            W[1] = W[0] + 0.5 * rng.normal(size=n); lo2 = W[1].clip(max=0).sum(); hi2 = W[1].clip(min=0).sum(); b[1] = -(lo2 + (hi2 - lo2) * rng.uniform(0.2, 0.8))
        ox = rng.normal(size=n) * 0.3; oy = rng.normal(size=2)
        single = balas_max(n, W, b, [(0,), (1,)], ox, oy)
        joint = balas_max(n, W, b, [(0, 1)], ox, oy)
        jmin = -balas_max(n, W, b, [(0, 1)], -ox, -oy)
        ex.append((single - joint) / max(joint - jmin, 1e-9))
    ex = np.array(ex)
    print(f"{n:2d}  {len(ex):6d}  {ex.mean():15.4f}  {np.median(ex):6.4f}  {ex.max():.4f}  {np.mean(ex > 0.01):.2f}")
