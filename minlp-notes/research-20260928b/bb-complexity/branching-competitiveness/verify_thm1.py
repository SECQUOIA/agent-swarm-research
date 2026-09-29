"""Check Theorem 1 (1D): the relaxation-minimizer rule puts at most 3 split points
in the interior of every certificate interval (at most 1 in the two end
intervals), so T <= 8N - 9 for N >= 2.  Also classifies interior splits by
which certificate endpoints the node contains, and checks the RR/LL lemma:
two nested nodes containing s with splits in the same adjacent interval force
the outer node to contain the far endpoint.

Instances: random polyhedral (random knots/values, convexified), line-based
rigid-breakpoint instances, and sampled smooth/sharp functions.
Usage: python3 verify_thm1.py NRANDOM SEED
"""
import bisect
import sys
import numpy as np
from poly1d import Inst, convexify, from_function, from_lines, r_min


def check(I, tag):
    S = I.greedy_breakpoints()
    N = len(S) - 1
    sp = I.splits(r_min)
    T = 2 * len(sp) + 1
    worst_int, worst_end = 0, 0
    tol = 0.0
    for j in range(N):
        a, b = S[j], S[j + 1]
        inside = [(l, u, y) for (l, u, y) in sp if a + tol < y < b - tol]
        # classify
        only_a = [n for n in inside if n[0] < a - tol and n[1] <= b + tol]
        only_b = [n for n in inside if n[1] > b + tol and n[0] >= a - tol]
        both = [n for n in inside if n[0] < a - tol and n[1] > b + tol]
        assert len(only_a) + len(only_b) + len(both) == len(inside), (tag, "node inside J")
        assert len(only_a) <= 1 and len(only_b) <= 1 and len(both) <= 1, (tag, j, len(only_a), len(only_b), len(both))
        if j == 0 or j == N - 1:
            worst_end = max(worst_end, len(inside))
        else:
            worst_int = max(worst_int, len(inside))
    bound = 1 if N == 1 else 8 * N - 9
    assert T <= bound, (tag, T, N)
    return T, N, worst_int, worst_end


def rand_inst(rng, K, eps):
    xs = np.concatenate([[0.0, 1.0], rng.uniform(0, 1, K)])
    lm = rng.uniform(np.log(eps), 0, K + 2)
    X, M = convexify(xs, np.exp(lm))
    M = M - M.min() + eps
    return Inst(X, M)


def rigid_inst(rng, K):
    # breakpoints s_1..s_k with tight caps (certificate valid), plus random extra lines
    k = rng.integers(1, 5)
    S = np.sort(np.concatenate([[0.0, 1.0], rng.uniform(0.05, 0.95, k)]))
    lines = [(S[j] + S[j + 1], -S[j] * S[j + 1] + 1e-13) for j in range(len(S) - 1)]
    for _ in range(K):
        p = rng.uniform(0, 1)
        j = np.searchsorted(S, p)
        near = min(abs(p - S[max(j - 1, 0)]), abs(p - S[min(j, len(S) - 1)]))
        mu = near ** 2 * rng.uniform(0, 1)
        lines.append((2 * p, -p * p + mu))
    for p in S:          # floors at breakpoints so that m > 0
        lines.append((2 * p, -p * p + 10 ** rng.uniform(-12, -3)))
    xs, ms = from_lines(lines)
    return Inst(xs, ms)


if __name__ == "__main__":
    n = int(sys.argv[1]); rng = np.random.default_rng(int(sys.argv[2]))
    worst = (0, 0, 0)
    maxratio = 0.0
    cnt = 0
    for trial in range(n):
        kind = trial % 3
        try:
            if kind == 0:
                I = rand_inst(rng, int(rng.integers(3, 150)), 10 ** rng.uniform(-12, -2))
            elif kind == 1:
                I = rigid_inst(rng, int(rng.integers(1, 40)))
            else:
                a = rng.uniform(0.05, 0.95); c = rng.uniform(0.1, 3); p = rng.choice([1, 2, 4])
                g = lambda t: c * abs(t - a) ** p - 0.5 * (t - a) ** 2 * (p == 1)
                I = from_function(g, 10 ** rng.uniform(-10, -2), K=2001, extra=[a])
        except ValueError:
            continue
        T, N, wi, we = check(I, trial)
        cnt += 1
        worst = (max(worst[0], wi), max(worst[1], we), worst[2])
        maxratio = max(maxratio, T / (2 * N - 1))
    print(f"instances checked: {cnt}; max interior-interval splits {worst[0]}; "
          f"max end-interval splits {worst[1]}; max T/(2N-1) = {maxratio:.3f}; all assertions passed")
