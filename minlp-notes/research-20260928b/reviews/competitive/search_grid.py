"""Hill-climb for large T/(2N-1) of R_min on grid instances (exact rationals).

Knots on a uniform grid of n intervals; m values on a coarse rational grid, so
exact ties occur.  Objective: worst tree over all tie-breaking choices.  Every
record instance is then perturbed (the chosen split knots are lowered by a tiny
amount, step by step) to test whether the same T is reached with UNIQUE
minimizers.  Optionally require H = m + y^2 convex.

Usage: python3 search_grid.py SEED ITERS RESTARTS CONVEX(0/1)
"""
import random
import sys
from fractions import Fraction as Fr

from exact1d import Inst
from worst_rmin import adversarial_tree, unique_run


def ratio(I):
    N = len(I.greedy()) - 1
    if N < 2:
        return None
    W, tree = adversarial_tree(I)
    return Fr(2 * W + 1, 2 * N - 1), N, 2 * W + 1, tree


def untie(I, tree, d=Fr(1, 10 ** 9)):
    """lower m at the adversarial split knots by d (distinct small amounts)."""
    ms = list(I.m)
    for r, (l, u, s) in enumerate(tree):
        k = I.x.index(s)
        ms[k] -= d * (r + 1)
    return Inst(I.x, ms)


def main():
    seed, iters, restarts, cvx = map(int, sys.argv[1:5])
    rng = random.Random(seed)
    records = {}
    for rs in range(restarts):
        n = rng.choice([8, 12, 16, 20])
        xs = [Fr(i, n) for i in range(n + 1)]
        eps = Fr(1, 100)
        grid = [eps * j for j in range(1, 13)] + [Fr(j, 64) for j in range(1, 9)]
        ms = [eps for _ in xs] if cvx else [rng.choice(grid) for _ in xs]
        cur = None
        for it in range(iters):
            m2 = list(ms) if cur else ms
            if cur:
                k = rng.randrange(len(m2))
                m2[k] = rng.choice(grid)
                if rng.random() < 0.3:          # symmetric move
                    m2[n - k] = m2[k]
            mm = min(m2)
            J = Inst(xs, [m - mm + eps for m in m2])
            if cvx and not J.convex():
                continue
            sc = ratio(J)
            if sc is None:
                continue
            if cur is None or sc[0] >= cur[0]:
                cur, ms = sc, m2
                Jbest = J
        if cur is None:
            continue
        r, N, T, tree = cur
        U = untie(Jbest, tree)
        k, uniq = unique_run(U)
        NU = len(U.greedy()) - 1
        key = N
        entry = (r, T, uniq, 2 * k + 1, NU, U.convex(), [str(x) for x in Jbest.m], n)
        if key not in records or r > records[key][0]:
            records[key] = entry
    for N in sorted(records):
        r, T, uniq, TU, NU, cv, m, n = records[N]
        print(f"N={N}: worst-over-ties T={T} ratio={float(r):.4f}; after untie: unique={uniq} T={TU} N={NU} "
              f"ratio={TU/(2*NU-1):.4f} convexH={cv}; grid n={n}; m={m}")


if __name__ == "__main__":
    main()
