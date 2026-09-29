"""Reviewer check of Proposition 0 (exact): with full node information the
greedy split b(l) = max{b : [l,b] valid} gives T = 2 N_opt - 1.
Also checks that the left and right greedy certificates have the same size.

Usage: python3 prop0_check.py NINST SEED
"""
import random
import sys
from fractions import Fraction as Fr

from thm1_check import make


def main():
    n, seed = int(sys.argv[1]), int(sys.argv[2])
    rng = random.Random(seed)
    kinds = ["convex", "nonconvex", "flat", "endpoint", "manymin", "ties", "rigid"]
    cnt = 0
    for t in range(n):
        I = make(rng, kinds[t % len(kinds)])
        if I is None:
            continue
        N = len(I.greedy()) - 1
        assert N == len(I.rgreedy()) - 1
        internal = I.run(lambda l, u, v, a: I.bmax(l))
        T = 2 * len(internal) + 1
        assert T == 2 * N - 1, (t, T, N)
        cnt += 1
    print(f"{cnt} instances: greedy-split rule gives T = 2 N_opt - 1 on all; left/right greedy sizes agree")


if __name__ == "__main__":
    main()
