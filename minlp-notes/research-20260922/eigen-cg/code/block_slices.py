"""Does the BH closure agree with BQP_n on the subspace fixed by a block-permutation group?
If P_BH ∩ Fix = BQP_n ∩ Fix for a block partition, then every E-CG cut with v constant on the
blocks is implied by BH (symmetrisation: a Fix-invariant linear function attains its minimum
over the invariant convex set P_BH at a point of Fix).  We test random invariant objectives
(numerically, LP over P_BH with cutting planes + complete separation)."""
import itertools, sys
import numpy as np
from bh import PBH, pairs


def invariant_objective(n, blocks, rng):
    lab = {}
    for b, B in enumerate(blocks):
        for i in B:
            lab[i] = b
    cx = rng.standard_normal(len(blocks))
    cX = {}
    a = [cx[lab[i]] for i in range(n)]
    for (i, j) in pairs(n):
        key = tuple(sorted((lab[i], lab[j])))
        if key not in cX:
            cX[key] = rng.standard_normal()
        a.append(cX[key])
    return a


def bqp_min(n, a):
    best = np.inf
    for x in itertools.product([0, 1], repeat=n):
        z = list(x) + [x[i] * x[j] for (i, j) in pairs(n)]
        best = min(best, float(np.dot(a, z)))
    return best


if __name__ == "__main__":
    n = int(sys.argv[1])
    trials = int(sys.argv[2])
    rng = np.random.default_rng(0)
    P = PBH(n, W0=1, exact=True)
    parts = {6: [[[0, 1, 2], [3, 4, 5]], [[0, 1, 2, 3], [4, 5]], [[0, 1], [2, 3], [4, 5]],
                 [[0, 1, 2], [3, 4], [5]], [[0, 1, 2, 3, 4], [5]]],
             7: [[[0, 1, 2], [3, 4, 5, 6]], [[0, 1, 2, 3, 4], [5, 6]], [[0, 1], [2, 3], [4, 5, 6]],
                 [[0, 1, 2], [3, 4, 5], [6]]]}[n]
    for blocks in parts:
        worst = 0
        for t in range(trials):
            a = invariant_objective(n, blocks, rng)
            v, z = P.minimize(a)
            worst = min(worst, v - bqp_min(n, a))
        print(blocks, "max gap (P_BH min - BQP min) over", trials, "objectives:", worst, flush=True)
