"""Independent check of Theorem 2.2 (tree Shapley-Folkman) of the coupling note.

Differences from the author's tree_sf_lp.py:
- random tree decompositions with branching (Delta up to 3), bags of 2 or 3
  variables, separators of size 1 or 2 (width 1 and 2);
- random objective vectors on the LP variables, so the basic solutions are
  generic extreme points of K (the theorem claims every extreme point);
- equality rows and inequality rows (<=), counting active rows;
- fractional components computed by union-find on the tree.

LP: variables mu_t(z) >= 0 for bag configurations z; sum_z mu_t(z) = 1;
marginals on S_t agree between t and p(t); k moment rows
sum_t sum_z mu_t(z) (A_t z_{R_t}) (=, <=) b.

Usage: python3 c4_tree_sf.py
"""
import itertools
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import lil_matrix


def random_td(nbags, rng, maxsep=1, maxnew=1, maxdeg=3):
    """Bags as lists of variable ids; parent array; separators."""
    bags = [list(range(1 + maxnew))]
    parent = [-1]
    nv = len(bags[0])
    for t in range(1, nbags):
        while True:
            p = int(rng.integers(0, t))
            if sum(1 for q in parent if q == p) < maxdeg:
                break
        ssz = int(rng.integers(1, min(maxsep, len(bags[p])) + 1))
        sep = sorted(rng.choice(bags[p], size=ssz, replace=False).tolist())
        nnew = int(rng.integers(1, maxnew + 1))
        new = list(range(nv, nv + nnew))
        nv += nnew
        bags.append(sep + new)
        parent.append(p)
    return bags, parent, nv


def run(nbags, d, k, rng, maxsep, maxnew, ineq, objective):
    bags, parent, nv = random_td(nbags, rng, maxsep, maxnew)
    top = {}
    for t, B in enumerate(bags):
        for v in B:
            top.setdefault(v, t)  # first bag in BFS-like order = top (parents precede children)
    grid = np.linspace(0, 1, d)
    confs = [list(itertools.product(range(d), repeat=len(B))) for B in bags]
    off = np.cumsum([0] + [len(c) for c in confs])
    nvar = off[-1]
    A = rng.normal(size=(k, nv))
    # b: image of a mixture of two random global configurations (feasible)
    z1 = rng.integers(0, d, nv); z2 = rng.integers(0, d, nv)
    b = A @ ((grid[z1] + grid[z2]) / 2)
    if ineq:
        b = b + np.abs(rng.normal(size=k)) * 0.3 * (rng.random(k) < 0.5)
    rows_eq, rhs_eq = [], []
    Meq = lil_matrix((nbags + sum(d ** len(set(bags[t]) & set(bags[parent[t]])) for t in range(1, nbags)) + (0 if ineq else k), nvar))
    r = 0
    for t in range(nbags):
        for j in range(len(confs[t])):
            Meq[r, off[t] + j] = 1
        rhs_eq.append(1); r += 1
    for t in range(1, nbags):
        p = parent[t]
        S = sorted(set(bags[t]) & set(bags[p]))
        it = [bags[t].index(v) for v in S]
        ip = [bags[p].index(v) for v in S]
        for sv in itertools.product(range(d), repeat=len(S)):
            for j, z in enumerate(confs[t]):
                if tuple(z[i] for i in it) == sv:
                    Meq[r, off[t] + j] += 1
            for j, z in enumerate(confs[p]):
                if tuple(z[i] for i in ip) == sv:
                    Meq[r, off[p] + j] -= 1
            rhs_eq.append(0); r += 1
    Mom = np.zeros((k, nvar))
    for t in range(nbags):
        R = [i for i, v in enumerate(bags[t]) if top[v] == t]
        for j, z in enumerate(confs[t]):
            for i in R:
                Mom[:, off[t] + j] += A[:, bags[t][i]] * grid[z[i]]
    if not ineq:
        for jj in range(k):
            for col in range(nvar):
                if Mom[jj, col] != 0:
                    Meq[r, col] = Mom[jj, col]
            rhs_eq.append(b[jj]); r += 1
    Meq = Meq[:r]
    cost = rng.normal(size=nvar) if objective == "random" else np.zeros(nvar)
    res = linprog(cost, A_eq=Meq.tocsr(), b_eq=np.array(rhs_eq),
                  A_ub=Mom if ineq else None, b_ub=b if ineq else None,
                  bounds=(0, None), method="highs-ds")
    if res.status != 0:
        return None
    x = res.x
    frac = [np.max(x[off[t]:off[t + 1]]) < 1 - 1e-7 for t in range(nbags)]
    uf = list(range(nbags))

    def find(a):
        while uf[a] != a:
            uf[a] = uf[uf[a]]; a = uf[a]
        return a
    for t in range(1, nbags):
        p = parent[t]
        if frac[t] and frac[p]:
            S = sorted(set(bags[t]) & set(bags[p]))
            it = [bags[t].index(v) for v in S]
            marg = {}
            for j, z in enumerate(confs[t]):
                key = tuple(z[i] for i in it)
                marg[key] = marg.get(key, 0) + x[off[t] + j]
            if max(marg.values()) < 1 - 1e-7:
                uf[find(t)] = find(p)
    comps = len({find(t) for t in range(nbags) if frac[t]})
    active = k if not ineq else int(np.sum(np.abs(Mom @ x - b) < 1e-7))
    nfrac = sum(frac)
    return comps, active, nfrac


if __name__ == "__main__":
    rng = np.random.default_rng(2026)
    print("setting | trials | violations (comps > active rows) | max comps | max active | max #fractional bags")
    settings = [
        ("w=1 tree, eq, random obj", dict(nbags=9, d=3, k=1, maxsep=1, maxnew=1, ineq=False, objective="random")),
        ("w=1 tree, eq, random obj", dict(nbags=9, d=3, k=2, maxsep=1, maxnew=1, ineq=False, objective="random")),
        ("w=1 tree, eq, random obj", dict(nbags=9, d=3, k=3, maxsep=1, maxnew=1, ineq=False, objective="random")),
        ("w=2 tree (sep<=2), eq", dict(nbags=7, d=3, k=2, maxsep=2, maxnew=1, ineq=False, objective="random")),
        ("w=2 tree (2 new vars), eq", dict(nbags=6, d=3, k=3, maxsep=1, maxnew=2, ineq=False, objective="random")),
        ("w=1 tree, ineq, random obj", dict(nbags=9, d=3, k=3, maxsep=1, maxnew=1, ineq=True, objective="random")),
        ("w=1 tree, eq, feasibility vertex", dict(nbags=9, d=3, k=2, maxsep=1, maxnew=1, ineq=False, objective="zero")),
    ]
    for name, kw in settings:
        viol, mc, ma, mf, n_ok = 0, 0, 0, 0, 0
        for trial in range(60):
            out = run(rng=rng, **kw)
            if out is None:
                continue
            q, act, nf = out
            n_ok += 1
            viol += q > act
            mc = max(mc, q); ma = max(ma, act); mf = max(mf, nf)
        print(f"{name} k={kw['k']} | {n_ok} | {viol} | {mc} | {ma} | {mf}")
