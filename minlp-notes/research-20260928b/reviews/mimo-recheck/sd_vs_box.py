"""Item (5): natural-order Fincke-Pohst versus box static-order B&B on the
same instances (beta = 1, rho = 4 log N, seeds 0-5).

Fincke-Pohst: QR of A, enumerate x_N, x_{N-1}, ..., x_1 depth first,
radius^2 = f(x*) (with a 1e-12 relative slack so that x* survives).  A node
is a partial vector whose partial distance is evaluated; the count is the root
plus both children of every surviving partial vector (same convention as the
box tree below).

Box B&B: variable order 1, 2, ..., N (static), incumbent value UB = f(x*)
fixed (x* is checked to be the ML point by the FP enumeration, so the
incumbent never changes and the tree does not depend on node order).  A node
is branched iff its certified lower bound is < UB (1 - 1e-9); the count is
the root plus both children of every branched node.  Node relaxations are
solved by scipy's BVLS (not by NNLS as in the note's code).

Usage: python3 sd_vs_box.py N [N ...]
"""
import os
os.environ["OMP_NUM_THREADS"] = "1"; os.environ["OPENBLAS_NUM_THREADS"] = "1"
import sys
import numpy as np
from rc_common import make_instance, box_value


def _fp_rec(R, z, x, i, pd, thr):
    """x[i:] fixed with partial distance pd; enumerate below.  Returns the
    number of children evaluated in the subtree and the leaves reached."""
    if i == 0:
        return 0, [(pd, x.copy())]
    j = i - 1
    base = z[j] - R[j, i:] @ x[i:]
    cnt = 0
    sols = []
    for val in (1.0, -1.0):
        cnt += 1
        d = pd + (base - R[j, j] * val) ** 2
        if d <= thr:
            x[j] = val
            c2, s2 = _fp_rec(R, z, x, j, d, thr)
            cnt += c2
            sols += s2
    x[j] = 0.0
    return cnt, sols


def fp_count(A, y, r2):
    N = A.shape[1]
    Q, R = np.linalg.qr(A)
    z = Q.T @ y
    thr = (r2 - (y @ y - z @ z)) * (1 + 1e-12)
    x = np.zeros(N)
    c, sols = _fp_rec(R, z, x, N, 0.0, thr)
    return 1 + c, sols


def box_static(B, w, UB, cap=2_000_000):
    N = B.shape[1]
    count = 1
    stack = [dict()]
    max_wrong = 0
    while stack:
        fx = stack.pop()
        fixed = np.array(sorted(fx), dtype=int)
        free = np.setdiff1d(np.arange(N), fixed)
        v = w.copy()
        if len(fixed):
            v = v + B[:, fixed] @ np.array([fx[i] for i in fixed])
        val, lb, u = box_value(B[:, free], v)
        if lb >= UB * (1 - 1e-9) or len(free) == 0:
            continue
        max_wrong = max(max_wrong, sum(1 for t in fx.values() if t == 2.0))
        j = int(free[0])
        for t in (2.0, 0.0):
            f2 = dict(fx); f2[j] = t
            stack.append(f2)
            count += 1
            if count > cap:
                return count, max_wrong
    return count, max_wrong


def main():
    Ns = [int(a) for a in sys.argv[1:]] or [32]
    for N in Ns:
        rho = 4 * np.log(N)
        fps, boxes = [], []
        for s in range(6):
            A, y, xs = make_instance(N, N, rho, s)
            w = y - A @ xs
            W = float(w @ w)
            B = A * xs
            nfp, sols = fp_count(A, y, W)
            better = [p for p, x in sols if not np.array_equal(x, xs)]
            nbox, mw = box_static(B, w, W)
            fps.append(nfp); boxes.append(nbox)
            print("N=%d seed=%d  W=%.4f  FP nodes %d (leaves within radius %d, other than x*: %d)  box static nodes %d (max wrong fixings at a branched node %d)"
                  % (N, s, W, nfp, len(sols), len(better), nbox, mw), flush=True)
        gm = lambda a: float(np.exp(np.mean(np.log(a))))
        print("N=%d  FP geo mean %.0f  %s | box static geo mean %.0f  %s" % (N, gm(fps), fps, gm(boxes), boxes), flush=True)


if __name__ == "__main__":
    main()
