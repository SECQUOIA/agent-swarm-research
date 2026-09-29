"""Seeded hill-climb for large worst-over-ties T/(2N-1) of R_min (exact).

Starts from the reviewer's T = 11, N = 3 instance refined onto a grid of
n = 32 intervals (values interpolated from H, which keeps the instance), then
applies random single-knot and symmetric moves on a rational value grid,
accepting non-decreasing ratio.  Convexity of H optional.

Usage: python3 search_seeded.py SEED ITERS CONVEX(0/1)
"""
import random
import sys
from fractions import Fraction as Fr

from exact1d import Inst
from search_grid import ratio, untie
from worst_rmin import unique_run

X0 = [Fr(s) for s in ['0', '1/16', '3/16', '7/16', '1/2', '9/16', '13/16', '15/16', '1']]
M0 = [Fr(s) for s in ['41/1600', '41/1600', '33/800', '1/100', '1/100', '1/100', '33/800', '41/1600', '41/1600']]


def main():
    seed, iters, cvx = map(int, sys.argv[1:4])
    rng = random.Random(seed)
    base = Inst(X0, M0)
    n = 32
    xs = [Fr(i, n) for i in range(n + 1)]
    ms = [base.mat(x) for x in xs]
    eps = Fr(1, 100)
    grid = sorted(set([eps * j / 4 for j in range(4, 60)]))
    cur = ratio(Inst(xs, ms))
    best = cur
    for it in range(iters):
        m2 = list(ms)
        for _ in range(rng.choice([1, 1, 2, 3])):
            k = rng.randrange(n + 1)
            m2[k] = rng.choice(grid)
            if rng.random() < 0.5:
                m2[n - k] = m2[k]
        mn = min(m2)
        J = Inst(xs, [m - mn + eps for m in m2])
        if cvx and not J.convex():
            continue
        sc = ratio(J)
        if sc is None:
            continue
        if sc[0] >= cur[0]:
            cur, ms = sc, [m - mn + eps for m in m2]
            if sc[0] > best[0]:
                best = sc
                U = untie(J, sc[3])
                k, uniq = unique_run(U)
                NU = len(U.greedy()) - 1
                print(f"it {it}: worst-over-ties T={sc[2]} N={sc[1]} ratio={float(sc[0]):.4f}; "
                      f"untied: unique={uniq} T={2*k+1} N={NU} convexH={U.convex()}", flush=True)
                print("   m =", [str(m) for m in J.m], flush=True)
    print(f"final best ratio {float(best[0]):.4f} (T={best[2]}, N={best[1]})")


if __name__ == "__main__":
    main()
