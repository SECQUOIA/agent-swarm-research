"""Best-first B&B with the perspective relaxation (Clarabel node solves, certified dual bounds).
Branching rules: 'maxfrac' (most fractional), 'maxz' (fractional variable with largest z).
Pruning: LB >= UB - rtol*UB, or relaxation integral (then its support is a feasible point)."""
import heapq, numpy as np
from core import solve_node, ridge

def forward_greedy(X, y, lam, k):
    S = []
    for _ in range(k):
        best = None
        for j in range(X.shape[1]):
            if j in S: continue
            v = ridge(X, y, lam, S + [j])[0]
            if best is None or v < best[0]: best = (v, j)
        S.append(best[1])
    return tuple(sorted(S))

def bnb(X, y, lam, k, S_init=(), rule='maxfrac', max_nodes=20000, rtol=1e-7, tol_int=1e-6, pool=None):
    p = X.shape[1]
    UB, bestS = np.inf, None
    for S in S_init:
        v = ridge(X, y, lam, S)[0]
        if v < UB: UB, bestS = v, tuple(sorted(S))
    heap = [(-np.inf, 0, (), ())]; tie = 1; nodes = 0; root = None
    while heap:
        plb, _, S0, S1 = heapq.heappop(heap)
        if plb >= UB - rtol * abs(UB): continue
        nodes += 1
        if nodes > max_nodes:
            return dict(nodes=nodes, done=False, opt=UB, support=bestS, root=root)
        LB, val, z, a = solve_node(X, y, lam, k, S0, S1)
        if root is None: root = LB
        if z is None: continue
        free = np.ones(p, bool); free[list(S0)] = False; free[list(S1)] = False
        F = np.nonzero(free)[0]; kp = k - len(S1)
        cand = tuple(sorted(set(S1) | set(F[np.argsort(-z[F])][:kp].tolist())))
        v = ridge(X, y, lam, cand)[0]
        if pool is not None: pool[cand] = v
        if v < UB: UB, bestS = v, cand
        if LB >= UB - rtol * abs(UB): continue
        zF = z[F]; frac = np.minimum(zF, 1 - zF)
        if frac.max() <= tol_int: continue
        leaves_hint = None
        if rule == 'maxfrac':
            i = int(F[np.argmax(frac)])
        elif rule == 'maxz':
            c = F[frac > tol_int]; i = int(c[np.argmax(z[c])])
        else:
            raise ValueError(rule)
        heapq.heappush(heap, (LB, tie, S0 + (i,), S1)); tie += 1
        heapq.heappush(heap, (LB, tie, S0, S1 + (i,))); tie += 1
    return dict(nodes=nodes, done=True, opt=UB, support=bestS, root=root)
