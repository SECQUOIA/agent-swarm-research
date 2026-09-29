"""Reviewer check of Theorem 1, the N = 2 refinement, the incumbent remark and
Corollary 1 (exact rationals, alpha = 1, root [0,1]).

For every instance:
  * N = size of the left-greedy certificate (also checked against right-greedy);
  * WORST-CASE tree of R_min over ALL tie-breaking choices (memoized recursion
    over nodes; nodes are knot pairs), plus leftmost/rightmost runs;
  * Theorem 1 per-interval counts (<= 3 inside, <= 1 in end intervals, classes
    Y^L, Y^R, Y^LR each <= 1) against both greedy certificates, for the
    leftmost and rightmost runs;
  * T <= 8N - 9, and the reviewer's refinement T <= 5 when N = 2;
  * incumbent gap g < eps: T <= 8 N(eps - g) - 9;
  * delta-minimizers (worst case over all choices with phi <= min + delta):
    compared with 8 N(eps - delta) - 9 (note's Corollary 1) and
    8 N(eps - 2 delta) - 9 (reviewer's corrected statement, delta < eps/2).

Families: random convex, random NON-convex H, flat regions (m = eps on an
interval), minimizers at an endpoint, many local minima, coarse grids that
create ties, rigid chord breakpoints.

Usage: python3 thm1_check.py NINST SEED
"""
import random
import sys
from fractions import Fraction as Fr
from functools import lru_cache

from exact1d import Inst, per_interval, classes


def rnd(rng, den=997):
    return Fr(rng.randint(1, den - 1), den)


def convexify(xs, ms):
    pts = sorted(zip(xs, ms))
    hull = []
    for x, m in pts:
        h = m + x * x
        while len(hull) >= 2:
            (x1, h1), (x2, h2) = hull[-2], hull[-1]
            if (h2 - h1) * (x - x1) >= (h - h1) * (x2 - x1):
                hull.pop()
            else:
                break
        hull.append((x, h))
    return [p[0] for p in hull], [p[1] - p[0] ** 2 for p in hull]


def normalize(xs, ms, eps):
    mn = min(ms)
    return Inst(xs, [m - mn + eps for m in ms])


def make(rng, kind):
    K = rng.randint(3, 22)
    eps = Fr(1, 10 ** rng.randint(2, 7))
    xs = sorted(set([Fr(0), Fr(1)] + [rnd(rng) for _ in range(K)]))
    if kind == "convex":
        ms = [Fr(rng.randint(0, 10 ** 6), 10 ** 6) ** rng.choice([1, 2, 3]) for _ in xs]
        xs, ms = convexify(xs, ms)
        return normalize(xs, ms, eps)
    if kind == "nonconvex":
        ms = [Fr(rng.randint(0, 10 ** 6), 10 ** 6) ** rng.choice([1, 2, 3]) / rng.choice([1, 4, 16]) for _ in xs]
        return normalize(xs, ms, eps)
    if kind == "flat":
        a, b = sorted([rnd(rng), rnd(rng)])
        ms = [Fr(0) if a <= x <= b else Fr(rng.randint(0, 10 ** 4), 10 ** 4) for x in xs]
        extra = [a + (b - a) * Fr(i, 7) for i in range(8)]
        xs2 = sorted(set(xs + extra))
        ms2 = [Fr(0) if a <= x <= b else Fr(rng.randint(0, 10 ** 4), 10 ** 4) for x in xs2]
        if rng.random() < 0.5:
            xs2, ms2 = convexify(xs2, ms2)
        return normalize(xs2, ms2, eps)
    if kind == "endpoint":
        ms = [Fr(0) if x == 0 else Fr(rng.randint(1, 10 ** 4), 10 ** 4) * x for x in xs]
        if rng.random() < 0.5:
            xs, ms = convexify(xs, ms)
        return normalize(xs, ms, eps)
    if kind == "manymin":
        ms = [Fr(0) if rng.random() < 0.5 else Fr(rng.randint(1, 100), 1000) for _ in xs]
        if rng.random() < 0.5:
            xs, ms = convexify(xs, ms)
        return normalize(xs, ms, eps)
    if kind == "ties":
        # coarse dyadic grid and symmetric values: many exact ties
        n = rng.choice([4, 8, 16])
        xs = [Fr(i, n) for i in range(n + 1)]
        half = [Fr(rng.randint(0, 4), 64) for _ in range(n // 2 + 1)]
        ms = [half[min(i, n - i)] for i in range(n + 1)]
        if rng.random() < 0.5:
            xs, ms = convexify(xs, ms)
        return normalize(xs, ms, eps)
    if kind == "rigid":
        k = rng.randint(1, 4)
        S = sorted(set([Fr(0), Fr(1)] + [rnd(rng, 97) for _ in range(k)]))
        lines = [(S[j] + S[j + 1], -S[j] * S[j + 1]) for j in range(len(S) - 1)]
        for _ in range(rng.randint(0, 12)):
            p = rnd(rng, 991)
            lines.append((2 * p, -p * p + Fr(rng.randint(0, 1000), 10 ** 5)))
        for p in S:
            lines.append((2 * p, -p * p + eps))
        # knots of the upper envelope (exact, brute force)
        cand = {Fr(0), Fr(1)}
        for i, (s1, b1) in enumerate(lines):
            for s2, b2 in lines[i + 1:]:
                if s1 != s2:
                    x = (b2 - b1) / (s1 - s2)
                    if 0 < x < 1:
                        cand.add(x)
        env = lambda y: max(s * y + b for s, b in lines)
        xs = sorted(cand)
        ms = [env(x) - x * x for x in xs]
        xs, ms = convexify(xs, ms)
        if min(ms) <= 0:
            return None
        return Inst(xs, ms)          # eps = min m (not renormalized: m >= eps by the floors)
    raise ValueError(kind)


def worst_tree(I, delta=0, prune=0, cap=5000):
    """max #internal nodes over all rules that split at a knot y with
    phi_B(y) <= min phi_B + delta; node pruned iff min phi_B >= prune."""
    calls = [0]

    @lru_cache(maxsize=None)
    def W(l, u):
        calls[0] += 1
        if calls[0] > cap:
            raise RuntimeError("cap")
        v, _ = I.node(l, u)
        if v >= prune:
            return 0
        cands = [I.x[k] for k in I.interior(l, u)
                 if I.m[k] - (I.x[k] - l) * (u - I.x[k]) <= v + delta]
        return 1 + max(W(l, s) + W(s, u) for s in cands)
    return W(Fr(0), Fr(1))


def main():
    n, seed = int(sys.argv[1]), int(sys.argv[2])
    rng = random.Random(seed)
    kinds = ["convex", "nonconvex", "flat", "endpoint", "manymin", "ties", "rigid"]
    stats = {k: [0, 0.0, 0, 0] for k in kinds}  # count, max ratio, max inside, max end
    ties_seen = 0
    cor_viol, cor2_viol, n_delta = 0, 0, 0
    worst_delta_example = None
    for t in range(n):
        kind = kinds[t % len(kinds)]
        I = make(rng, kind)
        if I is None:
            continue
        S = I.greedy()
        N = len(S) - 1
        assert N == len(I.rgreedy()) - 1
        if N == 1:
            continue
        runs = {}
        for name, pick in (("left", lambda l, u, v, a: a[0]), ("right", lambda l, u, v, a: a[-1])):
            runs[name] = I.run(pick)
        for name, internal in runs.items():
            for cert in (S, I.rgreedy()):
                cnt, at_bp = per_interval(cert, internal)
                assert at_bp <= N - 1
                for j in range(1, N + 1):
                    inside, YL, YR, YLR = classes(cert, internal, j)
                    assert len(inside) == len(YL) + len(YR) + len(YLR), "Lemma 1(iii) fails"
                    assert len(YL) <= 1 and len(YR) <= 1 and len(YLR) <= 1, (kind, t, j)
                    lim = 1 if j in (1, N) else 3
                    assert len(inside) <= lim, (kind, t, j, len(inside))
                    st = stats[kind]
                    if j in (1, N):
                        st[3] = max(st[3], len(inside))
                    else:
                        st[2] = max(st[2], len(inside))
        Wmax = worst_tree(I)
        if Wmax > max(len(r) for r in runs.values()):
            ties_seen += 1
        T = 2 * Wmax + 1
        assert T <= 8 * N - 9, (kind, t, T, N)
        if N == 2:
            assert T <= 5, (kind, t, T)
        st = stats[kind]
        st[0] += 1
        st[1] = max(st[1], T / (2 * N - 1))
        # incumbent gap g in (0, eps): prune iff min(m - q) >= g
        for frac in (Fr(1, 3), Fr(9, 10)):
            g = I.eps * frac
            Ng = len(I.greedy(shift=g)) - 1
            Tg = 2 * worst_tree(I, prune=g) + 1
            assert Ng == 1 and Tg == 1 or Tg <= 8 * Ng - 9, (kind, t, "incumbent", Tg, Ng)
        # delta-minimizers
        for frac in (Fr(1, 4), Fr(1, 2), Fr(9, 10)):
            d = I.eps * frac
            try:
                Td = 2 * worst_tree(I, delta=d) + 1
            except (RuntimeError, RecursionError):
                Td = None
            n_delta += 1
            N1 = len(I.greedy(shift=d)) - 1
            b1 = 1 if N1 == 1 else 8 * N1 - 9
            if Td is None or Td > b1:
                cor_viol += 1
                if worst_delta_example is None:
                    worst_delta_example = (kind, t, str(frac), Td, N1)
            if frac < Fr(1, 2):
                N2 = len(I.greedy(shift=2 * d)) - 1
                b2 = 1 if N2 == 1 else 8 * N2 - 9
                if Td is None or Td > b2:
                    cor2_viol += 1
    for k, (c, r, mi, me) in stats.items():
        print(f"{k:10s} instances(N>=2)={c:5d}  max T/(2N-1) (worst over ties)={r:.4f}  "
              f"max splits inside interior interval={mi}  inside end interval={me}")
    print(f"instances where some tie-breaking gave a larger tree than leftmost/rightmost: {ties_seen}")
    print(f"delta-minimizer runs: {n_delta}; T > 8N(eps-delta)-9 (note's Cor. 1 form): {cor_viol}"
          f"{'' if worst_delta_example is None else ' first: ' + str(worst_delta_example)}; "
          f"T > 8N(eps-2delta)-9 with delta < eps/2 (corrected form): {cor2_viol}")
    print("all Theorem 1 / N=2 / incumbent assertions passed")


if __name__ == "__main__":
    main()
