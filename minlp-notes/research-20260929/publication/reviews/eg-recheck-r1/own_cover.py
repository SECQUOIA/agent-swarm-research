"""Verifier's own exact coverage proof for the eg_disc2_s run G leaves (review r1).

Input: leaves_p<k>.npz written by own_bookkeeping.py (boxes identical, box for box, to the
boxes certified in the eg-recheck chunks), and the cached OSIL file (own_model.py).

Claim proved per part k: every point of the root box R_k (integer coordinates restricted to
integers) lies in at least one leaf.  Method (no tree data used, exact float comparisons only):
recursive guillotine decomposition.  For a node (box B, leaf set I, all leaves of I inside B):
  * |I| = 1: the single leaf must contain B;
  * otherwise find a coordinate d and a cut after position j of the leaves sorted by lo_d such
    that every leaf left of the cut has hi_d <= v (continuous) or hi_d <= v - 1 (integer) and
    every leaf right of it has lo_d >= v, where v = smallest lo_d on the right; recurse on
    B_left = B with hi_d = v (or v - 1) and B_right = B with lo_d = v.  B_left u B_right = B
    (integer: all integer points), and the leaves stay inside their node boxes.
If a node has no such cut, the proof fails (reported).  Any subset of the leaves of a guillotine
partition has such a cut (the lowest common tree ancestor's split), so failure would indicate
a non-guillotine leaf set or a coverage hole.
Then: every root box contains the exact OSIL domain in the continuous coordinates and spans the
full i5, i6 ranges; the i7 ranges of the 8 parts are integral, disjoint, consecutive and span
the OSIL range of i7.  Together: the leaves of the 8 parts cover the whole OSIL domain.
"""
import os
import sys
from fractions import Fraction as Fr

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from own_model import OsilModel  # noqa: E402


def prove_cover(lo, hi, isint, rlo, rhi):
    n = len(lo)
    # leaves inside the root, nonempty, integral integer ends
    assert np.all(lo <= hi), "empty leaf"
    assert np.all(lo >= rlo) and np.all(hi <= rhi), "leaf outside root"
    ii = np.flatnonzero(isint)
    assert np.all(lo[:, ii] == np.round(lo[:, ii])) and np.all(hi[:, ii] == np.round(hi[:, ii]))
    stack = [(np.arange(n), rlo.copy(), rhi.copy())]
    nodes = 0
    maxdepth = 0
    depth_of = {0: 0}
    while stack:
        I, L, U = stack.pop()
        nodes += 1
        if len(I) == 1:
            j = I[0]
            if not (np.all(lo[j] <= L) and np.all(hi[j] >= U)):
                return False, f"leaf {j} does not contain its node box {L.tolist()} {U.tolist()}", nodes
            continue
        best = None
        m = len(I)
        for d in range(7):
            a = lo[I, d]
            order = np.argsort(a, kind="stable")
            a_s = a[order]
            cm = np.maximum.accumulate(hi[I, d][order])
            valid = (cm[:-1] < a_s[1:]) if isint[d] else (cm[:-1] <= a_s[1:])
            pos = np.flatnonzero(valid)
            if len(pos):
                j = pos[np.argmin(np.abs(pos - (m - 1) / 2))]
                score = abs(j - (m - 1) / 2)
                if best is None or score < best[0]:
                    best = (score, d, j, order, a_s[j + 1])
        if best is None:
            return False, f"no guillotine cut for a node with {m} leaves, box {L.tolist()} {U.tolist()}", nodes
        _, d, j, order, v = best
        Il, Ir = I[order[:j + 1]], I[order[j + 1:]]
        Ul = U.copy(); Ul[d] = v - 1 if isint[d] else v
        Lr = L.copy(); Lr[d] = v
        stack.append((Il, L.copy(), Ul))
        stack.append((Ir, Lr, U.copy()))
    return True, "covered", nodes


def main():
    O = OsilModel()
    vlb, vub, vint = O.vlb[:7], O.vub[:7], O.vint[:7]
    allok = True
    i7 = []
    for p in range(8):
        z = np.load(os.path.join(HERE, f"leaves_p{p}.npz"))
        lo, hi, isint, rlo, rhi = z["lo"], z["hi"], z["isint"], z["root_lo"], z["root_hi"]
        assert list(isint) == vint
        dom_ok = True
        for i in range(7):
            if vint[i]:
                dom_ok &= rlo[i] == int(rlo[i]) and rhi[i] == int(rhi[i])
                if i != 6:
                    dom_ok &= Fr(rlo[i]) == vlb[i] and Fr(rhi[i]) == vub[i]
            else:
                dom_ok &= Fr(rlo[i]) <= vlb[i] and Fr(rhi[i]) >= vub[i]      # exact comparison
        i7.append((int(rlo[6]), int(rhi[6])))
        ok, msg, nodes = prove_cover(lo, hi, isint, rlo, rhi)
        allok &= ok and dom_ok
        print(f"part {p}: i7 in [{int(rlo[6])}, {int(rhi[6])}]; root contains the OSIL continuous box and full "
              f"i5/i6 ranges: {dom_ok}; leaves {len(lo)}; guillotine proof: {ok} ({msg}; {nodes} nodes)", flush=True)
    i7.sort()
    span_ok = (i7[0][0] == vlb[6] and i7[-1][1] == vub[6] and all(a <= b for a, b in i7)
               and all(i7[t + 1][0] == i7[t][1] + 1 for t in range(7)))
    print(f"i7 ranges {i7}: disjoint, consecutive, span [{vlb[6]}, {vub[6]}]: {span_ok}")
    allok &= span_ok
    print("COVERAGE PROVED: the leaves of the 8 parts cover the OSIL domain" if allok else "COVERAGE PROOF FAILED")


if __name__ == "__main__":
    main()
