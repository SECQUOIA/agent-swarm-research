"""Item (1): node conventions of Definition 1.1, checked with my own disjunctive L_2 model.

L_2 = min Phi(beta, B) s.t. [[1, beta'], [beta, B]] PSD, sum z <= k, node fixings on z, and for every pair
T = {a, b}: (z_T, beta_T, B_T) in H_T, written disjunctively over the four patterns zeta in {0,1}^2
(pattern s has weight lam_s and a PSD moment block [[lam_s, x_s'], [x_s, X_s]] supported on s).

Checks, on small random instances:
 (A) forced-in node (0, {j}): root hulls + z_j = 1  versus  the exact hull of the node's own set
     (patterns with zeta_j = 0 removed on pairs containing j). Claim: equal (no column is fixed to 0).
 (B) removal node ({m}, 0): root hulls + z_m = 0  versus  column m deleted (= exact node hull, B_{m.} = 0).
     Claim (node convention): the root-hull value is <= the deleted-column value and can be smaller.
 (C) sanity: every value <= the node's integer optimum (enumeration).
usage: python3 rc_node.py > rc_node.log
"""
import itertools
from rc_common import np, ridge
import cvxpy as cp


def L2(X, y, lam, k, S0=(), S1=(), node_hull=False):
    n, p = X.shape
    Q = X.T @ X + lam * np.eye(p)
    c = X.T @ y
    z = cp.Variable(p)
    M = cp.Variable((p + 1, p + 1), PSD=True)   # [[1, beta'], [beta, B]]
    beta, B = M[1:, 0], M[1:, 1:]
    cons = [M[0, 0] == 1, z >= 0, z <= 1, cp.sum(z) <= k]
    cons += [z[i] == 0 for i in S0] + [z[i] == 1 for i in S1]
    for a, b in itertools.combinations(range(p), 2):
        pats = [(0, 0), (1, 0), (0, 1), (1, 1)]
        if node_hull:
            for i in S1:
                if i == a:
                    pats = [s for s in pats if s[0] == 1]
                if i == b:
                    pats = [s for s in pats if s[1] == 1]
        lams, xs, Xs = [], [], []
        for s in pats:
            W = cp.Variable((3, 3), PSD=True)   # [[lam_s, x_s'], [x_s, X_s]]
            for t, on in enumerate(s):
                if not on:
                    cons += [W[t + 1, :] == 0]
            lams.append((s, W[0, 0])); xs.append(W[1:, 0]); Xs.append(W[1:, 1:])
        cons += [sum(l for _, l in lams) == 1,
                 z[a] == sum(l for s, l in lams if s[0] == 1),
                 z[b] == sum(l for s, l in lams if s[1] == 1),
                 beta[a] == sum(x[0] for x in xs), beta[b] == sum(x[1] for x in xs),
                 B[a, a] == sum(Xm[0, 0] for Xm in Xs), B[b, b] == sum(Xm[1, 1] for Xm in Xs),
                 B[a, b] == sum(Xm[0, 1] for Xm in Xs)]
    obj = y @ y - 2 * c @ beta + cp.trace(Q @ B)
    prob = cp.Problem(cp.Minimize(obj), cons)
    prob.solve(solver="CLARABEL", tol_gap_abs=1e-10, tol_gap_rel=1e-10, tol_feas=1e-10)
    return prob.value


def node_opt(X, y, lam, k, S0=(), S1=()):
    p = X.shape[1]
    free = [i for i in range(p) if i not in S0 and i not in S1]
    best = np.inf
    for s in range(0, k - len(S1) + 1):
        for T in itertools.combinations(free, s):
            best = min(best, ridge(X, y, lam, tuple(S1) + T)[0] if len(S1) + s > 0 else y @ y)
    return best


def main():
    worstA = 0.0
    diffsB = []
    viol = 0
    maxex = -np.inf
    for seed in range(6):
        rng = np.random.default_rng(100 + seed)
        n, p, k = 5, 8, 2
        X = rng.standard_normal((n, p))
        beta = np.zeros(p); beta[:k] = rng.choice([-1.0, 1.0], k) * (0.3 if seed % 2 else 1.0)
        y = X @ beta + 0.5 * rng.standard_normal(n)
        lam = 1.0
        j = int(rng.integers(k, p))       # a null feature forced in
        m = int(rng.integers(0, k))        # a true feature removed
        vA_root = L2(X, y, lam, k, S1=(j,))
        vA_node = L2(X, y, lam, k, S1=(j,), node_hull=True)
        optA = node_opt(X, y, lam, k, S1=(j,))
        vB_root = L2(X, y, lam, k, S0=(m,))
        keep = [i for i in range(p) if i != m]
        vB_del = L2(X[:, keep], y, lam, k)
        optB = node_opt(X, y, lam, k, S0=(m,))
        r = L2(X, y, lam, k)
        opt = node_opt(X, y, lam, k)
        relA = abs(vA_root - vA_node) / optA
        worstA = max(worstA, relA)
        diffsB.append((vB_del - vB_root) / optB)
        for v, o in [(vA_root, optA), (vA_node, optA), (vB_root, optB), (vB_del, optB), (r, opt)]:
            viol += v > o * (1 + 1e-7)
            maxex = max(maxex, (v - o) / o)
        print(f"seed {seed}: forced-in j={j}: root-hull {vA_root:.9f}, node-hull {vA_node:.9f} (rel diff {relA:.1e}), "
              f"node OPT {optA:.6f} | removal m={m}: root-hull {vB_root:.9f}, deleted col {vB_del:.9f} "
              f"(rel diff {(vB_del - vB_root) / optB:.2e}), node OPT {optB:.6f} | root {r:.6f} OPT {opt:.6f}")
    print(f"(A) max rel |root-hull - node-hull| at forced-in nodes: {worstA:.1e}")
    print(f"(B) (deleted - root-hull)/OPT at removal nodes: min {min(diffsB):.2e}, max {max(diffsB):.2e}")
    print(f"(C) values above node OPT (1 + 1e-7): {viol}; max (value - OPT)/OPT = {maxex:.1e} (solver accuracy)")


if __name__ == "__main__":
    main()
