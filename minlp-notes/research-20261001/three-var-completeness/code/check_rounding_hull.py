"""Numerical check of Corollary 2.4 (iv): for y in R_D, rounding coordinate i
(Y_ii -> m_i) gives a point of H3plus; points of R_D outside H3plus satisfy
Y_ii < m_i for all i.

Points: optimal points of the D3 relaxation for (a) random objectives with
nonnegative square coefficients and (b) family members composed with random
cube symmetries (these optima typically lie outside H3plus).  For each point
we compute the exact-hull separation value
    sep(y) = min { p(y) : p in P3plus, p(u) = 1 }
before and after rounding each coordinate (negative = outside H3plus).

usage: python check_rounding_hull.py SEED N
"""
import sys
import warnings

import numpy as np

warnings.filterwarnings("ignore")
from check_rounding_numeric import rho_vector  # noqa: E402
from cube3 import GROUP, MINDEX, QKEYS, compose, family_member, vector_from_quad  # noqa: E402
from sdp3 import Relaxation, Separation  # noqa: E402


def quad_moments(yv):
    return np.array([yv[MINDEX[k]] for k in QKEYS])


if __name__ == '__main__':
    seed, n = int(sys.argv[1]), int(sys.argv[2])
    rng = np.random.default_rng(seed)
    R0 = Relaxation(use_family=False)
    S = Separation()
    stats = dict(points=0, outside=0, outside_with_cap_violation=0)
    worst_after = np.inf
    worst_before = np.inf
    min_gap_outside = np.inf   # min over outside points of min_i (m_i - Y_ii)
    for it in range(n):
        if it % 2 == 0:
            c = rng.normal(size=10)
            c[4:7] = np.abs(c[4:7])
        else:
            d1, d2 = rng.uniform(0.3, 2, 2)
            h = rng.uniform(0.05, 0.95) * min(d1, d2)
            k = rng.uniform(0.05, 2)
            d3 = (d1 + d2 - h + k) * rng.uniform(1.05, 3)
            c = vector_from_quad(compose(family_member(h, d1, d2, d3, k), GROUP[rng.integers(48)]))
            c = c / np.abs(c).max()
        try:
            val, st, yv = R0.solve(c)
            if yv is None:
                continue
            yq = quad_moments(yv)
            sb = S.solve(yq)[0]
        except BaseException as e:
            if isinstance(e, KeyboardInterrupt):
                raise
            continue
        stats['points'] += 1
        worst_before = min(worst_before, sb)
        if sb < -1e-6:
            stats['outside'] += 1
            gaps = [yq[1 + i] - yq[4 + i] for i in range(3)]
            min_gap_outside = min(min_gap_outside, min(gaps))
            if min(gaps) <= 0:
                stats['outside_with_cap_violation'] += 1
        for i in range(3):
            try:
                sa = S.solve(quad_moments(rho_vector(yv, i)))[0]
            except BaseException as e:
                if isinstance(e, KeyboardInterrupt):
                    raise
                continue
            worst_after = min(worst_after, sa)
    print(stats, 'min sep before %.2e' % worst_before, 'min sep after rounding %.2e' % worst_after,
          'min over outside points of min_i (m_i - Y_ii) %.3e' % min_gap_outside, flush=True)
