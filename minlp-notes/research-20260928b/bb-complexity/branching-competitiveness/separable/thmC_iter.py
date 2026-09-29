"""Iterated coordinate ambiguity (Theorem C', revision after the review; the result is the review's).

Instances A_i of Theorem C (lb_coord.py, r0 = 1/4 - 1/(5n), eps = 1/100).
A node is a *corner node* if each of its intervals contains 0 or 1; S(v) = coordinates whose
interval is not [0,1].  Checks and computations:
  (1) on random corner nodes, for every free i (i not in S(v)): identical node value and minimizer
      across the A_i, and the node is invalid;
  (2) G(n) = min over reference trees of max_i #{corner nodes free of i}, by an exact Pareto DP;
      the averaging bound (2^(n+1) - n - 2)/n;
  (3) an explicit rule that follows an optimal reference tree, simulated exactly on every A_i:
      T(A_i) = 2 #{corner nodes free of i} + 1 and max_i T = 2 G(n) + 1.
usage: python3 thmC_iter.py NMAX_DP NMAX_SIM SAMPLES"""
import itertools
import random
import sys
from fractions import Fraction as Fr
from functools import lru_cache
from lb_coord import lines, coord

HALF, QUART, EPS = Fr(1, 2), Fr(1, 4), Fr(1, 100)


def instances(n):
    r0 = QUART - Fr(1, 5 * n)
    sL, sR = 1 - EPS / (4 * (n - 1)), 1 + EPS / (4 * (n - 1))
    return coord(lines(n, EPS, r0, sL, sR, +1)[0]), coord(lines(n, EPS, r0, sL, sR, -1)[0])


def check_corner_nodes(n, samples, rng):
    R, N = instances(n)
    bad = 0
    for _ in range(samples):
        k = rng.randrange(0, n)                      # |S| < n
        S = rng.sample(range(n), k)
        box = [(Fr(0), Fr(1))] * n
        for j in S:
            t = Fr(rng.randint(1, 999), 1000)
            box[j] = (Fr(0), t) if rng.random() < 0.5 else (t, Fr(1))
        data = []
        for i in range(n):
            if i in S:
                continue
            cs = [N] * n
            cs[i] = R
            nd = [cs[j].node(*box[j]) for j in range(n)]
            val = sum(d[0] for d in nd) + EPS
            data.append((val, tuple(d[1] for d in nd), tuple(d[2] for d in nd)))
        if len(set(data)) != 1 or data[0][0] >= 0:
            bad += 1
    return bad


def pareto(vs):
    vs = sorted(set(vs))
    out = []
    for v in vs:
        if not any(all(a <= b for a, b in zip(u, v)) for u in out):
            out.append(v)
    return out


def G(n):
    @lru_cache(maxsize=None)
    def V(S):                          # S: frozenset of cut coordinates; vectors indexed 0..n-1
        if len(S) == n:
            return ((0,) * n,)
        free1 = tuple(0 if j in S else 1 for j in range(n))
        res = []
        for j in range(n):
            if j in S:
                continue
            ch = V(S | frozenset([j]))
            for a in ch:
                for b in ch:
                    res.append(tuple(f + x + y for f, x, y in zip(free1, a, b)))
        return tuple(pareto(res))
    best = min(V(frozenset()), key=max)
    return max(best), best


def best_tree(n):
    """an explicit reference tree attaining G(n): nested dict {coord: (left subtree, right subtree)}"""
    @lru_cache(maxsize=None)
    def solve(S, target):              # a subtree for set S whose vector is <= target (tuple), or None
        if len(S) == n:
            return ("leaf",)
        free1 = tuple(0 if j in S else 1 for j in range(n))
        rem = tuple(t - f for t, f in zip(target, free1))
        if min(rem) < 0:
            return None
        for j in range(n):
            if j in S:
                continue
            S2 = S | frozenset([j])
            # split the remaining budget between the two children (enumerate integer splits)
            for a in itertools.product(*[range(r + 1) for r in rem]):
                b = tuple(r - x for r, x in zip(rem, a))
                t1 = solve(S2, a)
                if t1 is None:
                    continue
                t2 = solve(S2, b)
                if t2 is not None:
                    return (j, t1, t2)
        return None
    g, vec = G(n)
    return solve(frozenset(), vec), vec


def simulate(n, tree, i):
    """rule: at a corner node follow the reference tree (cut the prescribed coordinate at 1/2)."""
    R, N = instances(n)
    cs = [N] * n
    cs[i] = R
    T = 0
    stack = [(tuple((Fr(0), Fr(1)) for _ in range(n)), tree)]
    while stack:
        box, t = stack.pop()
        T += 1
        val = sum(c.node(*b)[0] for c, b in zip(cs, box)) + EPS
        if val >= 0:
            continue
        assert t[0] != "leaf", "reference tree exhausted on an invalid node"
        j, t1, t2 = t
        assert box[j] == (Fr(0), Fr(1))
        b1 = list(box); b1[j] = (Fr(0), HALF)
        b2 = list(box); b2[j] = (HALF, Fr(1))
        stack += [(tuple(b1), t1), (tuple(b2), t2)]
    return T


if __name__ == "__main__":
    nmax_dp, nmax_sim, samples = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    rng = random.Random(7)
    for n in range(2, 6):
        print(f"n={n}: random corner nodes with identical data and invalid in every free A_i: "
              f"{samples - check_corner_nodes(n, samples, rng)}/{samples}", flush=True)
    for n in range(2, nmax_dp + 1):
        g, vec = G(n)
        avg = Fr(2 ** (n + 1) - n - 2, n)
        print(f"n={n}: G(n) = {g} (vector {vec}); deterministic T >= {2 * g + 1}, ratio >= {Fr(2 * g + 1, 3)}; "
              f"averaging: sum_i N_i >= {2 ** (n + 1) - n - 2}, randomized E[T] >= {2 * avg + 1} = {float(2 * avg + 1):.3f}, "
              f"ratio >= {(2 * avg + 1) / 3} = {float((2 * avg + 1) / 3):.3f}", flush=True)
    for n in range(2, nmax_sim + 1):
        tree, vec = best_tree(n)
        Ts = [simulate(n, tree, i) for i in range(n)]
        print(f"n={n}: explicit rule following an optimal reference tree: T(A_i) = {Ts}, 2*vector+1 = "
              f"{[2 * v + 1 for v in vec]}, max = {max(Ts)}", flush=True)
