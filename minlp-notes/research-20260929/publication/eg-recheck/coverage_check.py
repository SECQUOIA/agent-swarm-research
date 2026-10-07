"""Second coverage check of the eg_disc2_s run-G leaves, independent of the tree logic of
verify_tree.py / recheck_leaves.py (it uses only the leaf lists saved in res/ and the root boxes).

Per part k (leaves = closed processed boxes + domain-reduction slabs, from res/p<k>_c*.npz):
  1. every leaf lies in the part's root box, has lo <= hi, and has integral integer bounds;
  2. exact volume identity (Python integers, no rounding): with continuous coordinates scaled by
     2^54 (every coordinate is >= 0.25, so every float coordinate is a multiple of 2^-54; this is
     asserted), the measure  prod_cont (hi - lo) * prod_int (hi - lo + 1)  summed over the leaves
     must equal the measure of the root box.  If the leaves have pairwise disjoint interiors
     (true for a bisection tree with slabs; checked statistically by test 3), equality means
     that the leaves cover the root box;
  3. random points (seeded; continuous coordinates uniform in the root box, integer coordinates
     uniform over the integers of the root range): every point must lie in at least one leaf,
     and a point in general position should lie in exactly one leaf (more than one would mean
     overlapping interiors).  Evidence, not proof.

    python3 coverage_check.py [points_per_part] [drop]

With the second argument "drop", the largest leaf of each part is removed first (negative
control: the volume identity must then fail).
"""
import glob
import os
import sys
from math import prod

import numpy as np

OUT = os.path.dirname(os.path.abspath(__file__))
SC = 2.0 ** 54


def ints(a):
    """exact integer representation of float coordinates scaled by 2^54 (asserts exactness)."""
    v = a * SC                                   # power-of-two scaling: exact
    assert np.all(v == np.floor(v)) and np.all(np.abs(v) < 2.0 ** 62)
    return v.astype(np.int64)


def main():
    npts = int(sys.argv[1]) if len(sys.argv) > 1 else 200_000
    drop = len(sys.argv) > 2 and sys.argv[2] == "drop"
    rng = np.random.default_rng(20261002)
    allok = True
    tot_leaves = 0
    for k in range(8):
        files = sorted(glob.glob(os.path.join(OUT, "res", f"p{k}_c*.npz")))
        Z = [np.load(f) for f in files]
        isint = np.load(os.path.join(OUT, "rec", f"rec_disc2_p{k}.npz"))["isint"].astype(bool)
        rlo, rhi = Z[0]["root_lo"], Z[0]["root_hi"]
        assert all(np.array_equal(z["root_lo"], rlo) and np.array_equal(z["root_hi"], rhi) for z in Z)
        lo = np.concatenate([z["lo"] for z in Z]); hi = np.concatenate([z["hi"] for z in Z])
        if drop:                                     # negative control: remove the largest leaf
            j = int(np.argmax(np.prod((hi - lo + isint) / (rhi - rlo + isint), axis=1)))
            lo, hi = np.delete(lo, j, axis=0), np.delete(hi, j, axis=0)
        n = len(lo)
        tot_leaves += n
        ci, ii = np.where(~isint)[0], np.where(isint)[0]
        # 1. containment, nonempty, integral integer bounds
        inside = bool(np.all(lo >= rlo) and np.all(hi <= rhi))
        nonempty = bool(np.all(lo <= hi))
        integral = bool(np.all(lo[:, ii] == np.floor(lo[:, ii])) and np.all(hi[:, ii] == np.floor(hi[:, ii])))
        # 2. exact volume identity
        wl = ints(hi[:, ci]) - ints(lo[:, ci])                       # int64 widths, < 2^54
        cnt = (hi[:, ii] - lo[:, ii] + 1).astype(np.int64)
        vol = sum(prod(int(w) for w in wl[j]) * prod(int(c) for c in cnt[j]) for j in range(n))
        rvol = prod(int(w) for w in (ints(rhi[ci]) - ints(rlo[ci]))) * prod(int(c) for c in (rhi[ii] - rlo[ii] + 1))
        vol_ok = vol == rvol
        # 3. random points, grouped by integer coordinates
        P = np.empty((npts, len(rlo)))
        P[:, ci] = rlo[ci] + rng.random((npts, len(ci))) * (rhi[ci] - rlo[ci])
        for i in ii:
            P[:, i] = rng.integers(int(rlo[i]), int(rhi[i]) + 1, npts)
        hits = np.zeros(npts, np.int64)
        keys = {}
        for p, row in enumerate(P[:, ii].astype(np.int64)):
            keys.setdefault(tuple(row), []).append(p)
        for key, pts in keys.items():
            kv = np.array(key)
            cand = np.where(np.all((lo[:, ii] <= kv) & (kv <= hi[:, ii]), axis=1))[0]
            Q = P[pts][:, ci]
            L, H = lo[cand][:, ci], hi[cand][:, ci]
            for s in range(0, len(pts), 256):
                q = Q[s:s + 256, None, :]
                hits[np.array(pts[s:s + 256])] = np.all((L[None] <= q) & (q <= H[None]), axis=2).sum(1)
        miss, multi = int((hits == 0).sum()), int((hits > 1).sum())
        ok = inside and nonempty and integral and vol_ok and miss == 0
        allok &= ok
        print(f"part {k}: {n} leaves; root i7 [{rlo[6]:g}, {rhi[6]:g}]; inside root {inside}; lo <= hi {nonempty}; "
              f"integral integer bounds {integral}", flush=True)
        print(f"   exact volume (units 2^-216 x integer points): leaves {vol}, root {rvol}, equal {vol_ok}", flush=True)
        print(f"   random points {npts}: in no leaf {miss}, in more than one leaf {multi}, "
              f"in exactly one {int((hits == 1).sum())}", flush=True)
    print(f"TOTAL leaves {tot_leaves}; {'ALL COVERAGE CROSS-CHECKS PASSED' if allok else 'A COVERAGE CROSS-CHECK FAILED'}")


if __name__ == "__main__":
    main()
