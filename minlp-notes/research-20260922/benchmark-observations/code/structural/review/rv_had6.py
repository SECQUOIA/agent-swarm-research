"""Reviewer checks for hadamard_6.

1. Ehlich-block determinant (survey arXiv:2104.06756, formula before Thm 25) over ALL partitions
   of n = 7: det(C) = (n-3)^(n-s) prod(n-3+4r_i) (1 - sum r_i/(n-3+4r_i)). Max must be 344064.
2. Own exhaustive enumeration of max |det| over 6x6 0/1 matrices, different reduction from the
   author's: rows 1..5 range over all 5-subsets of the 63 nonzero 0/1 row vectors (no column
   normalisation); the last row is optimised exactly via cofactors (det linear in the last row).
   5x5 minors computed in float64 and rounded; the rounding error is asserted < 1e-6
   (entries 0/1, |minor| <= 5, so LU error is ~1e-14).
"""
import itertools
from fractions import Fraction as F

import numpy as np


def partitions(n, maxpart=None):
    if maxpart is None:
        maxpart = n
    if n == 0:
        yield []
        return
    for k in range(min(n, maxpart), 0, -1):
        for rest in partitions(n - k, k):
            yield [k] + rest


n = 7
best = {}
for p in partitions(n):
    s = len(p)
    val = F((n - 3) ** (n - s))
    for r in p:
        val *= (n - 3 + 4 * r)
    val *= 1 - sum(F(r, n - 3 + 4 * r) for r in p)
    best[tuple(p)] = val
mx = max(best.values())
print("max Ehlich-block det over partitions of 7:", mx, [p for p, v in best.items() if v == mx])

vecs = np.array([[(v >> (5 - j)) & 1 for j in range(6)] for v in range(1, 64)], dtype=np.float64)
combos = np.array(list(itertools.combinations(range(63), 5)), dtype=np.int16)
print("5-subsets:", len(combos))
overall = 0
chunk = 500000
for a in range(0, len(combos), chunk):
    top = vecs[combos[a:a + chunk]]  # (m,5,6)
    cof = np.empty((top.shape[0], 6))
    for j in range(6):
        minor = np.delete(top, j, axis=2)
        d = np.linalg.det(minor)
        r = np.rint(d)
        assert np.max(np.abs(d - r)) < 1e-6
        cof[:, j] = (-1) ** (5 + j) * r  # cofactor of entry (6, j+1) with 0-based row index 5
    pos = np.where(cof > 0, cof, 0).sum(axis=1)
    neg = -np.where(cof < 0, cof, 0).sum(axis=1)
    overall = max(overall, int(max(pos.max(), neg.max())))
print("exhaustive max |det| over 6x6 0/1 matrices:", overall)
