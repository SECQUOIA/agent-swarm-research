"""Numerical sanity check of Lemma 2.3 on SDP output.

Take optimal pseudo-moment vectors l (20 monomials) of the D3 relaxation for
random objectives, apply the rounding map l -> l o rho_i, and report the
smallest eigenvalue over the 27 localizing matrices before and after, and the
change of the quadratic moments (only Y_ii may change, to m_i).

usage: python check_rounding_numeric.py SEED N
"""
import sys
import warnings

import numpy as np

warnings.filterwarnings("ignore")
from cube3 import MINDEX, MKEYS, QKEYS, STATUSES, localizing_polys  # noqa: E402
from sdp3 import Relaxation  # noqa: E402


def rho_vector(yv, i):
    """(l o rho_i)(x^a) = l(x^a') with a'_i = min(a_i, 1)."""
    out = np.zeros_like(yv)
    for k, idx in MINDEX.items():
        kk = list(k)
        if kk[i] >= 1:
            kk[i] = 1
        out[idx] = yv[MINDEX[tuple(kk)]]
    return out


def min_eig(yv):
    worst = np.inf
    for status in STATUSES:
        polys = localizing_polys(status)
        n = len(polys)
        M = np.array([[sum(v * yv[MINDEX[k]] for k, v in polys[a][b].items()) for b in range(n)]
                      for a in range(n)])
        worst = min(worst, np.linalg.eigvalsh(M)[0])
    return worst


if __name__ == '__main__':
    seed, n = int(sys.argv[1]), int(sys.argv[2])
    rng = np.random.default_rng(seed)
    R0 = Relaxation(use_family=False)
    worst_before, worst_after, max_other_change = np.inf, np.inf, 0.0
    count = 0
    for it in range(n):
        c = rng.normal(size=10)
        c[4:7] = np.abs(c[4:7])
        val, st, yv = R0.solve(c)
        if yv is None or st not in ('optimal', 'optimal_inaccurate'):
            continue
        count += 1
        worst_before = min(worst_before, min_eig(yv))
        for i in range(3):
            y2 = rho_vector(yv, i)
            worst_after = min(worst_after, min_eig(y2))
            for k in QKEYS:
                if k == tuple(2 if j == i else 0 for j in range(3)):
                    assert abs(y2[MINDEX[k]] - yv[MINDEX[tuple(1 if j == i else 0 for j in range(3))]]) < 1e-12
                else:
                    max_other_change = max(max_other_change, abs(y2[MINDEX[k]] - yv[MINDEX[k]]))
    print('points', count, 'min eig before %.2e' % worst_before, 'min eig after rounding %.2e' % worst_after,
          'max change of other quadratic moments %.1e' % max_other_change, flush=True)
