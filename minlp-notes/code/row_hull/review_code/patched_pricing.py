"""Proposed fix for pricing._compress: states whose (lo, hi) agree up to rounding must keep the
LARGEST profit.  The original sorts by exact lo first, so among sums that are equal in exact arithmetic
but differ by 1 ulp the one with the smaller float survives, whatever its profit."""
import numpy as np
import rowhull.pricing as pricing
from rowhull.pricing import States


def _compress(lo, hi, P, mask, B, kmax, merged):
    scale = max(1.0, abs(B))
    order = np.lexsort((hi, lo))
    lo, hi, P, mask = lo[order], hi[order], P[order], mask[order]
    new = np.ones(len(lo), bool)
    new[1:] = (lo[1:] - lo[:-1] > 1e-11 * scale) | (np.abs(hi[1:] - hi[:-1]) > 1e-11 * scale)
    starts = np.flatnonzero(new)
    grp = np.cumsum(new) - 1
    best = np.maximum.reduceat(P, starts)
    idx = np.flatnonzero(P >= best[grp])
    first = np.unique(grp[idx], return_index=True)[1]
    # outer interval of the group, so that the true sum of every dropped subset stays covered
    lo, hi, P, mask = np.minimum.reduceat(lo, starts), np.maximum.reduceat(hi, starts), best, mask[idx[first]]
    if len(lo) > kmax:
        merged = True
        edges = np.minimum((lo / (B + 1e-300) * kmax).astype(np.int64), kmax - 1)
        starts = np.flatnonzero(np.r_[True, edges[1:] != edges[:-1]])
        grp = np.repeat(np.arange(len(starts)), np.diff(np.r_[starts, len(lo)]))
        best = np.maximum.reduceat(P, starts)
        idx = np.flatnonzero(P >= best[grp])
        first = np.unique(grp[idx], return_index=True)[1]
        lo, hi, P, mask = lo[starts], np.maximum.reduceat(hi, starts), best, mask[idx[first]]
    return States(lo, hi, P, mask, merged)


def install():
    pricing._compress = _compress
