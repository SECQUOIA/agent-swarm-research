"""Print one explicit, exactly verified failure of the caterpillar in the proof of Theorem 1.7(b),
together with the reviewer's halfspace/open-complement binary tree for the same partition.
Uses the exact machinery of binary_realization.py.  Usage: python3 caterpillar_example.py [seed]
"""
import sys
import random
from fractions import Fraction as F
from itertools import permutations
import binary_realization as br


def pts(mask):
    return [(int(br.PTS[i][0]), int(br.PTS[i][1])) for i in range(br.NP) if mask >> i & 1]


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    rnd = random.Random(seed)
    while True:
        A = [[F(rnd.randint(-3, 3)) for _ in range(2)] for _ in range(2)]
        if A[0][0] * A[1][1] - A[0][1] * A[1][0] == 0:
            continue
        t = (F(rnd.randint(0, 21), 7), F(rnd.randint(0, 14), 7))
        y = (A[0][0] * t[0] + A[0][1] * t[1] + F(rnd.randint(-3, 3), 5),
             A[1][0] * t[0] + A[1][1] * t[1] + F(rnd.randint(-3, 3), 5))
        eps = F(rnd.choice([1, 5, 20]), 100)
        I = br.Inst(A, y, eps)
        if I.tau <= I.phi(I.xs):
            continue
        k, parts = br.kappa_and_partitions(I)
        if k < 3:
            continue
        for part in parts:
            for order in permutations(range(k)):
                if not br.caterpillar_ok(I, part, order):
                    cls = [part[i] for i in order]
                    rest = 0
                    for c in cls[1:]:
                        rest |= c
                    content = I.hc[rest]
                    cov = I.hc[cls[1]] | I.hc[rest ^ cls[1]]
                    bad = content & ~cov
                    print(f"phi(x) = ||A x - y||^2, A = {[[str(v) for v in r] for r in A]}, y = {[str(v) for v in y]}")
                    print(f"P = {{0..3}}x{{0..2}}, OPT = {I.OPT}, eps = {eps}, tau = {I.tau}, kappa = {k}")
                    for j, c in enumerate(cls):
                        print(f"   I_{j+1} = {pts(c)}   min over conv I_{j+1} = {I.min_over(br.hull([br.PTS[i] for i in range(br.NP) if c >> i & 1]))[0]}")
                    print(f"   caterpillar node conv(I_2 u ... u I_{k}) contains P-points {pts(content)}")
                    print(f"   its children conv(I_2), conv(I_3 u ...) miss {pts(bad)}  -> covering condition of Definition 1.1 fails")
                    bad_i = [i for i in range(br.NP) if bad >> i & 1][0]
                    for j, c in enumerate(cls):
                        if c >> bad_i & 1:
                            print(f"   the missed point belongs to I_{j+1}")
                    ok, why = br.halfspace_tree_ok(I, cls)
                    print(f"   reviewer's halfspace/open-complement binary tree with {k} leaves for this partition: {ok} ({why})")
                    for j, c in enumerate(cls):
                        xh = I.argmin[c]
                        g = I.grad(xh)
                        print(f"      H_{j+1} = {{ {g[0]}*(x1 - {xh[0]}) + {g[1]}*(x2 - {xh[1]}) >= 0 }},  min phi over H_{j+1} = {I.min_over_halfspace(g, xh)}")
                    return


if __name__ == "__main__":
    main()
