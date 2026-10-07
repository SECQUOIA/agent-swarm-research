"""Validity check of the implemented constraint families at genuine moment points.

For random finite mixtures of points of [0,1]^n (n = 4, triples (0,1,2) and
(1,2,3), so that auxiliary moments are shared between triples), build the base
relaxation plus all triangle inequalities, Khajavirad (17) (method K) and
Anstreicher-Puges (14)-(16) (method A) on both triples, set every moment
variable to the exact mixture moment, and report the largest cone violation.
Every variable of these families is a monomial moment, so no auxiliary has to
be solved for.  Family blocks and the exact lift contain auxiliaries (N, W);
their validity is a theorem (family note; Anstreicher-Burer Theorem 7) and is
checked separately in test_basic.py through the copositivity test.
Usage: python check_validity.py ntrials seed"""
import sys

import numpy as np

sys.path.insert(0, '.')
from relax import Relax
from conic import primal_violation


def main():
    ntr, seed = int(sys.argv[1]), int(sys.argv[2])
    rng = np.random.default_rng(seed)
    n = 4
    worst = 0.0
    for t in range(ntr):
        H = rng.normal(size=(n, n)); H = H + H.T
        R = Relax(H, rng.normal(size=n))
        for T in [(0, 1, 2), (1, 2, 3)]:
            for k in range(4):
                R.add_triangle(*T, k)
            R.add_K(T)
            R.add_A(T)
        npts = int(rng.integers(1, 6))
        P = rng.random((npts, n))
        # push some coordinates to the bounds (faces of the cube are where cuts are tight)
        mask = rng.random(P.shape) < 0.3
        P[mask] = rng.integers(0, 2, size=mask.sum())
        w = rng.random(npts); w /= w.sum()
        xv = np.zeros(R.m.nvar)
        for key, v in R.mon.items():
            xv[v] = float(w @ np.prod(P[:, list(key)], axis=1))
        A, b, q, cones = R.m.build('clarabel')
        viol = primal_violation(A, b, cones, xv, 'clarabel')
        worst = max(worst, viol)
    print('trials %d  K and A constraints on two overlapping triples  max violation at genuine moment points %.3e' % (ntr, worst))


if __name__ == '__main__':
    main()
