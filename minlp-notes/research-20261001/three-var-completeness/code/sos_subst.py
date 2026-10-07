"""Numerical test: is m(x_1^{2d},...,x_n^{2d}) a sum of squares, for a
copositive matrix M?  Uses sign-symmetry (parity) block diagonalization.
Discovery only; an infeasible SDP is not a proof without a checked dual."""
import sys, itertools, time, warnings
import numpy as np, cvxpy as cp
warnings.filterwarnings("ignore")

def monomials(n, deg):
    if n == 1:
        yield (deg,); return
    for i in range(deg + 1):
        for rest in monomials(n - 1, deg - i):
            yield (i,) + rest

def sos_test(M, d, solver='CLARABEL', verbose=False):
    n = M.shape[0]
    # target polynomial: sum_ij M_ij x_i^{2d} x_j^{2d}
    target = {}
    for i in range(n):
        for j in range(n):
            e = [0] * n; e[i] += 2 * d; e[j] += 2 * d
            target[tuple(e)] = target.get(tuple(e), 0) + M[i, j]
    basis = list(monomials(n, 2 * d))
    # Newton polytope pruning: exponents must lie in conv{2d e_i (i with M_ii>0)} = all (diag>0)
    blocks = {}
    for b in basis:
        blocks.setdefault(tuple(x % 2 for x in b), []).append(b)
    grams = []; coef = {}
    cons = []
    for key, mons in blocks.items():
        G = cp.Variable((len(mons), len(mons)), symmetric=True)
        grams.append((G, mons))
        for a in range(len(mons)):
            for b in range(len(mons)):
                e = tuple(x + y for x, y in zip(mons[a], mons[b]))
                coef.setdefault(e, []).append(G[a, b])
    for e, terms in coef.items():
        cons.append(cp.sum(cp.hstack(terms)) == target.get(e, 0))
    for e in target:
        assert e in coef
    # maximize the smallest eigenvalue margin to get a robust certificate
    # smallest uniform shift t with G + t I PSD in every block:
    # t <= 0 (numerically) means SOS; t > 0 measures failure.
    t = cp.Variable()
    cons2 = list(cons)
    for G, mons in grams:
        cons2.append(G + t * np.eye(len(mons)) >> 0)
    prob = cp.Problem(cp.Minimize(t), cons2 + [t >= -1])
    prob.solve(solver=solver, verbose=verbose)
    return prob.status, t.value, len(basis), len(blocks)

if __name__ == '__main__':
    # Shaked-Monderer fan matrix (apex = index 2, negative path 0-1-2-3-4)
    A = np.array([[1,-1,1,0,0],[-1,1,-1,1,0],[1,-1,1,-1,1],[0,1,-1,1,-1],[0,0,1,-1,1]], float)
    H = np.array([[1,-1,1,1,-1],[-1,1,-1,1,1],[1,-1,1,-1,1],[1,1,-1,1,-1],[-1,1,1,-1,1]], float)
    which = sys.argv[1]; d = int(sys.argv[2])
    M = A if which == 'A' else H
    t0 = time.time()
    print(which, 'd', d, sos_test(M, d), 'time', time.time() - t0, flush=True)
