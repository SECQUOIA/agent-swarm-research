"""Exploratory search near the conjectured uniform two-switch worst case.

The threshold oracle is exact up to floating-point arithmetic when all mode
masses <= E and the two largest masses sum to < 1-2E: every repeated-mode
three-block schedule is then impossible, and positive discrepancies are automatic.
This script seeks counterexamples; failure to find one is not a proof.
"""
import argparse
import numpy as np
from scipy.optimize import differential_evolution


def threshold_margin(a, E):
    """Return largest feasibility slack among three distinct ordered modes."""
    n, N = a.shape
    A = np.column_stack((np.zeros(n), np.cumsum(a, axis=1) / N))
    masses = A[:, -1]
    times = np.arange(N + 1) / N
    F = times - A
    # R_i is the latest feasible endpoint for the initial mode.
    first_bad = np.argmax(F > E, axis=1)
    left = np.maximum(0, first_bad - 1)
    R = (left / N + (E - F[np.arange(n), left]) /
         (1 - a[np.arange(n), np.minimum(left, N - 1)]))
    R[first_bad == 0] = 1.0
    L = 1 - masses - E
    cell = np.clip(np.floor(L * N).astype(int), 0, N - 1)
    Alate = A[:, cell] + a[:, cell] * (L - cell / N)
    order = np.argsort(R)[::-1][:3]
    best = -np.inf
    for r in range(n):
        for q in range(n):
            if q == r:
                continue
            p = next(p for p in order if p != q and p != r)
            best = max(best, R[p] + Alate[q, r] - L[r] + E)
    return best, masses


def run(n, N, iterations, seed, group_size=0):
    E = 1 / (n * ((n / (n - 1)) ** 3 - 1))
    E = max(E, 1 / n, 1 / 4)
    def decode(x):
        if group_size:
            u = 1 / (1 + np.exp(-x))
            return np.vstack((np.tile(u / group_size, (group_size, 1)),
                              np.tile((1 - u) / (n - group_size), (n - group_size, 1))))
        logits = np.vstack((x.reshape(n - 1, N), np.zeros(N)))
        z = np.exp(logits - logits.max(axis=0))
        return z / z.sum(axis=0)
    def objective(x):
        margin, masses = threshold_margin(decode(x), E)
        # The oracle reduction requires these two structural assumptions.
        penalty = max(0, masses.max() - E) + max(0, np.sort(masses)[-2:].sum() - (1 - 2 * E) + 1e-9)
        return margin + 10 * penalty
    dimension = N if group_size else (n - 1) * N
    initial = np.full(N, np.log(group_size / (n - group_size))) if group_size else np.zeros(dimension)
    result = differential_evolution(objective, [(-6, 6)] * dimension,
                                    maxiter=iterations, popsize=6, seed=seed,
                                    x0=initial, polish=True, tol=1e-8)
    a = decode(result.x)
    margin, masses = threshold_margin(a, E)
    print({'n': n, 'N': N, 'uniform_error': E, 'margin': margin,
           'max_mass': masses.max(), 'top_two_mass': np.sort(masses)[-2:].sum(),
           'evaluations': result.nfev, 'seed': seed, 'group_size': group_size}, flush=True)
    print(a.tolist(), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--n', type=int, default=8)
    parser.add_argument('--intervals', type=int, default=4)
    parser.add_argument('--iterations', type=int, default=200)
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--group-size', type=int, default=0)
    args = parser.parse_args()
    run(args.n, args.intervals, args.iterations, args.seed, args.group_size)
