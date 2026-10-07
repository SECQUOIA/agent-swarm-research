"""k = 1 core with sign-consistent core couplings: minimal residual minimizers
are nested in v (Topkis), so V has at most r+1 quadratic pieces.

Energy E_v(y) = sum_i (mu_i + v beta_i) y_i + sum_{i<j} w_ij y_i y_j,
w_ij <= 0.  With all beta_i <= 0, the minimal minimizer is nondecreasing in v.
Brute force over labels on 401 rational values of v; also shows that mixed
signs of beta can break nestedness.
"""
import random
from fractions import Fraction as Fr
from itertools import product

def minimal_minimizer(mu, beta, w, v, r):
    best = None; sets = []
    for y in product((0, 1), repeat=r):
        val = sum((mu[i] + v * beta[i]) * y[i] for i in range(r)) + sum(wij * y[i] * y[j] for (i, j), wij in w.items())
        if best is None or val < best:
            best = val; sets = [y]
        elif val == best:
            sets.append(y)
    # minimal minimizer = intersection of all minimizers (minimizers form a lattice)
    inter = tuple(min(s[i] for s in sets) for i in range(r))
    assert inter in sets
    return inter

def trial(rng, consistent):
    r = rng.randint(2, 6)
    mu = [Fr(rng.randint(-10, 10), rng.randint(1, 3)) for _ in range(r)]
    beta = [Fr(rng.randint(-10, 10), rng.randint(1, 3)) for _ in range(r)]
    if consistent:
        beta = [-abs(b) for b in beta]
    w = {(i, j): -Fr(rng.randint(0, 8), rng.randint(1, 3)) for i in range(r) for j in range(i + 1, r) if rng.random() < 0.6}
    seq = [minimal_minimizer(mu, beta, w, Fr(t, 400), r) for t in range(401)]
    nested = all(all(a[i] <= b[i] for i in range(r)) for a, b in zip(seq, seq[1:]))
    return nested, len(set(seq)), r

if __name__ == "__main__":
    rng = random.Random(5)
    for _ in range(150):
        nested, cnt, r = trial(rng, True)
        assert nested and cnt <= r + 1
    print("sign-consistent couplings: minimal minimizers nested and <= r+1 distinct in 150 trials")
    broken = sum(1 for _ in range(150) if not trial(rng, False)[0])
    print("mixed-sign couplings: nestedness failed in %d of 150 trials" % broken)
    print("ALL MONOTONE CHECKS PASSED")
