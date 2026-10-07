"""Independent recheck of (i) the (leaf, cell) pair counts and (ii) the theta
threshold of Remark 3.6, for the path family with c = 0 (x* = 0, zero slopes).

Own code: shell partitions of Lemma 3.1 built in exact integer units, and a
bottom-up certificate DP (Lemma 1.5 with zero slopes) in which every convex
program min{Rel_{t,B}(z) : z in B, z_S in D} is solved by golden-section
search in z_1 over the exactly (or, for the last bag, bisection-) minimized
z_2. Closed intersections are used throughout, as in the model.

Usage:
  python3 shell_dp.py pairs MU J1 J2 ...     (theta = 2^-MU, h = 2^-J)
  python3 shell_dp.py gap N MU J             (root gap f* - l_r = -l_r)
"""
import sys
from bisect import bisect_left, bisect_right
from itertools import product

import numpy as np

B, KAPPA, ALPHA = 0.8, 0.1, 0.4


def shells(kk, j, mu):
    """Shell partition of [-1,1]^kk around p = 0, h = 2^-j, theta = 2^-mu.

    Returns a list of boxes (lo, hi) with integer coordinates in units
    u = theta*h = 2^-(j+mu); X = [-R, R]^kk with R = 2^(j+mu).
    """
    R = 2 ** (j + mu)
    h = 2 ** mu                      # h in units
    J = 0                            # J = ceil(log2(s0/h)), s0 = 2 = 2R units
    while h * 2 ** J < 2 * R:
        J += 1
    boxes = []
    # central 2^kk cubes of side h with vertex p = 0
    for signs in product([0, 1], repeat=kk):
        lo = tuple(-h if s == 0 else 0 for s in signs)
        hi = tuple(0 if s == 0 else h for s in signs)
        boxes.append((lo, hi))
    for lev in range(1, J + 1):
        g = 2 ** (lev - 1)           # theta * 2^(lev-1) * h in units
        outer = 2 ** lev * h         # half-width of Q(p, 2^lev h)
        inner = 2 ** (lev - 1) * h
        ticks = list(range(-outer, outer, g))
        for corner in product(ticks, repeat=kk):
            lo = corner
            hi = tuple(c + g for c in corner)
            if all(-inner <= a and b <= inner for a, b in zip(lo, hi)):
                continue             # contained in Q(p, 2^(lev-1) h)
            clo = tuple(max(a, -R) for a in lo)
            chi = tuple(min(b, R) for b in hi)
            if all(a < b for a, b in zip(clo, chi)):
                boxes.append((clo, chi))
    return boxes, R


def pairs(mu, j):
    leaves, R = shells(2, j, mu)
    cells, _ = shells(1, j, mu)
    cells.sort()
    clo = [c[0][0] for c in cells]
    chi = [c[1][0] for c in cells]
    tot, mx = 0, 0
    for lo, hi in leaves:
        a, b = lo[0], hi[0]          # separator = first coordinate
        # cells D = [c, d] with c <= b and d >= a (closed intersection)
        k = bisect_right(clo, b) - bisect_left(chi, a)
        tot += k
        mx = max(mx, k)
    return len(leaves), len(cells), tot, mx


def phi(t):
    return t * t - KAPPA * t ** 4


def dphi(t):
    return 2 * t - 4 * KAPPA * t ** 3


def solve_pairs(l1, u1, l2, u2, a1, b1, const, last):
    """min over z1 in [a1,b1], z2 in [l2,u2] of
    phi(z1) + [last] phi(z2) + B z1 z2 - ALPHA((z1-l1)(u1-z1) + (z2-l2)(u2-z2)) + const."""
    def inner(z1):
        if not last:
            z2 = np.clip((l2 + u2) / 2 - (B / (2 * ALPHA)) * z1, l2, u2)
        else:
            lo, hi = l2.copy(), u2.copy()
            for _ in range(60):      # derivative in z2 is increasing
                m = (lo + hi) / 2
                d = dphi(m) + B * z1 - ALPHA * (l2 + u2) + 2 * ALPHA * m
                pos = d > 0
                hi = np.where(pos, m, hi)
                lo = np.where(pos, lo, m)
            z2 = (lo + hi) / 2
        v = phi(z1) + B * z1 * z2 - ALPHA * ((z1 - l1) * (u1 - z1) + (z2 - l2) * (u2 - z2)) + const
        if last:
            v = v + phi(z2)
        return v
    gr = (np.sqrt(5) - 1) / 2
    lo, hi = a1.copy(), b1.copy()
    for _ in range(80):              # golden-section search; the reduced function is convex
        m1 = lo + (1 - gr) * (hi - lo)
        m2 = lo + gr * (hi - lo)
        left = inner(m1) < inner(m2)
        hi = np.where(left, m2, hi)
        lo = np.where(left, lo, m1)
    return np.minimum(inner((lo + hi) / 2), np.minimum(inner(a1), inner(b1)))


def gap(n, mu, j):
    leaves, R = shells(2, j, mu)
    cells, _ = shells(1, j, mu)
    cells.sort()
    u = 1.0 / R                       # unit length
    L = np.array([[lo[0], lo[1], hi[0], hi[1]] for lo, hi in leaves], dtype=float) * u
    C = np.array([[c[0][0], c[1][0]] for c in cells], dtype=float) * u
    clo, chi = list(C[:, 0]), list(C[:, 1])
    # (leaf, cell) pairs on the first coordinate (the bag's own separator)
    pi, pc = [], []
    # child-cell ranges on the second coordinate
    rlo, rhi = [], []
    for k, (l1, l2, u1, u2) in enumerate(L):
        lo_idx = bisect_left(chi, l1)
        hi_idx = bisect_right(clo, u1)
        for c in range(lo_idx, hi_idx):
            pi.append(k)
            pc.append(c)
        rlo.append(bisect_left(chi, l2))
        rhi.append(bisect_right(clo, u2))
    pi, pc = np.array(pi), np.array(pc)
    rlo, rhi = np.array(rlo), np.array(rhi)
    # bags t = 1..n-1 (bag t = {t, t+1}); bag n-1 is the last (it also carries phi(x_n)).
    beta_child = None
    for t in range(n - 1, 0, -1):
        last = (t == n - 1)
        if beta_child is None:
            psi = np.zeros(len(L))
        else:
            # psi_{t+1,B} = min of beta over child cells meeting B's second coordinate
            psi = np.array([beta_child[a:b].min() for a, b in zip(rlo, rhi)])
        if t == 1:
            # root: l_r = min over leaves of min over the leaf
            v = solve_pairs(L[:, 0], L[:, 2], L[:, 1], L[:, 3], L[:, 0], L[:, 2], psi, last)
            return -v.min(), len(L) * (n - 1) + len(C) * (n - 2)
        a1 = np.maximum(L[pi, 0], C[pc, 0])
        b1 = np.minimum(L[pi, 2], C[pc, 1])
        v = solve_pairs(L[pi, 0], L[pi, 2], L[pi, 1], L[pi, 3], a1, b1, psi[pi], last)
        beta = np.full(len(C), np.inf)
        np.minimum.at(beta, pc, v)
        beta_child = beta


def main():
    if sys.argv[1] == "pairs":
        mu = int(sys.argv[2])
        print("# theta = 2^-%d; interior bag; h, leaves, cells, pairs, pairs/leaves, max cells per leaf" % mu)
        for j in map(int, sys.argv[3:]):
            l, c, p, m = pairs(mu, j)
            print("2^-%-3d %7d %5d %8d %.3f %4d" % (j, l, c, p, p / l, m))
    elif sys.argv[1] == "gap":
        n, mu, j = map(int, sys.argv[2:5])
        g, size = gap(n, mu, j)
        print("n=%d theta=2^-%d h=2^-%d: gap f*-l_r = %.4e, size %d" % (n, mu, j, g, size))


if __name__ == "__main__":
    main()
