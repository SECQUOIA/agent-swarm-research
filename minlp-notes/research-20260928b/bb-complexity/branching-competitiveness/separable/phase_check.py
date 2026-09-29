"""Exact check of the Type-0 Lemma and the Phase Lemma on random 1D knot instances.

Pruned R_min tree on A = [0,1]: split D iff F(D) < -beta and w(D) >= tau (same minimizer choice
as everywhere else).  b' = beta + kappa*tau > 0.  Checks:
  (T0) inside every leaf l of the unpruned R_min tree at budget b', the number of split nodes
       of the pruned tree contained in l is <= c_kappa = kappa (2 kappa (kappa+1) + 1);
  (PL) |S1| <= (4N - 5) + c_kappa (4N - 4) for N = N(b') >= 2, and |S1| <= c_kappa if N = 1.
Instances: random convex H (max of lines) and random non-convex H (random knot values of m >= 0).
usage: python3 phase_check.py TRIALS SEED"""
import random
import sys
from fractions import Fraction as Fr
from sepexact import Coord
from search import coord_from_lines, rand_line


def rand_nonconvex(rng, K):
    xs = sorted({Fr(0), Fr(1)} | {Fr(rng.randint(1, 999), 1000) for _ in range(K)})
    ms = [Fr(rng.choice([0, 0, 1, 2, 5, 20, 100]), 1000) * Fr(rng.randint(1, 9), 9) for _ in xs]
    return Coord.from_m(xs, ms)


def pruned(c, beta, tau, cap=200000):
    S1, st = [], [(c.L, c.U)]
    while st:
        l, u = st.pop()
        F, y, w = c.node(l, u)
        if F < -beta and w >= tau and w > 0:
            S1.append((l, u))
            if len(S1) > cap:
                return None
            st += [(l, y), (y, u)]
    return S1


def leaves_at(c, b, cap=200000):
    L, st = [], [(c.L, c.U)]
    while st:
        l, u = st.pop()
        F, y, w = c.node(l, u)
        if F < -b and w > 0:
            st += [(l, y), (y, u)]
            if len(st) > cap:
                return None
        else:
            L.append((l, u))
    return L


if __name__ == "__main__":
    trials, seed = int(sys.argv[1]), int(sys.argv[2])
    rng = random.Random(seed)
    worst_t0 = {1: 0, 2: 0, 3: 0}
    worst_ratio = 0
    done = 0
    for t in range(trials):
        c = coord_from_lines([rand_line(rng) for _ in range(rng.randint(3, 12))]) if rng.random() < 0.5 \
            else rand_nonconvex(rng, rng.randint(3, 15))
        kappa = rng.choice([1, 1, 2, 3])
        tau = Fr(1, rng.choice([10, 100, 1000, 10 ** 4, 10 ** 5]))
        bprime = Fr(1, rng.choice([10, 100, 1000, 10 ** 4, 10 ** 5, 10 ** 6]))
        beta = bprime - kappa * tau
        S1 = pruned(c, beta, tau)
        Ls = leaves_at(c, bprime)
        if S1 is None or Ls is None:
            continue
        N = len(c.greedy(bprime)) - 1
        ck = kappa * (2 * kappa * (kappa + 1) + 1)
        inside = max([sum(1 for (l, u) in S1 if a <= l and u <= b) for (a, b) in Ls] + [0])
        worst_t0[kappa] = max(worst_t0[kappa], inside)
        assert inside <= ck, (inside, ck)
        bound = ck if N == 1 else (4 * N - 5) + ck * (4 * N - 4)
        assert len(S1) <= bound, (len(S1), bound)
        worst_ratio = max(worst_ratio, len(S1) / N)
        done += 1
    print(f"instances {done}: max split nodes inside one b'-leaf by kappa {worst_t0} "
          f"(bounds 5, 26, 75); max |S1|/N(b') = {worst_ratio:.2f}; all assertions passed")
