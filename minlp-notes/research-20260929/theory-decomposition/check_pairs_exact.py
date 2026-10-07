"""Targeted check of the (leaf, cell) pair test of dp_certificate.certificate (Section 5 and
Section 8.2 of decomposition-certificates.md).

For the certificates of E2, E3 and E4 (non-dyadic x*) and two certificates at x* = 0, the pairs
are computed with three tests on the separator coordinate:
  closed   closed test on the rounded edges (first version, PAIR_TOL = 0)
  widened  closed test widened by PAIR_TOL (current dp_certificate.py)
  exact    closed test on the exact edges (Definition 1.2 and Lemma 1.5)
Exact edges: every unclipped shell edge around p is p + m * theta * h for an integer m (Lemma 3.1),
evaluated with fractions.Fraction from the same double p; clipped edges are exactly +-1.
Both tests of certificate() are covered: leaves of bag t against the cells of S_t, and leaves
of bag t against the cells of the child separator S_{t+1}. Leaves and cells share the centre
coordinate, so their edges lie on one lattice.
Usage: python3 check_pairs_exact.py
"""
import math
from fractions import Fraction
import numpy as np
from dp_certificate import shells, global_min, PAIR_TOL
from run_experiments import c_vec, B, KAPPA

CHUNK = 20000


def exact_ranks(p, h, mu, arrays):
    """Ranks of the exact values of the rounded edges in `arrays` (all centred at p)."""
    vals = np.concatenate([a.ravel() for a in arrays])
    uniq, inv = np.unique(vals, return_inverse=True)
    u0 = Fraction(h) / 2 ** mu
    P = Fraction(float(p))
    ex, err, amb = [], 0.0, 0
    for v in uniq:
        m = round((v - p) / float(u0))
        cand = P + m * u0
        if -1.0 < v < 1.0:
            err = max(err, abs(float(cand - Fraction(float(v)))))
            ex.append(cand)
        else:  # clipped at +-1, unless a lattice point lies within rounding of +-1
            if cand != Fraction(float(v)) and abs(cand - Fraction(float(v))) < Fraction(1, 10 ** 14):
                amb += 1
            ex.append(Fraction(float(v)))
    order = sorted(set(ex))
    rank = {e: k for k, e in enumerate(order)}
    r = np.array([rank[e] for e in ex])[inv]
    out, k = [], 0
    for a in arrays:
        out.append(r[k:k + a.size].reshape(a.shape))
        k += a.size
    return out, err, amb


def compare(l, u, lo, hi, p, h, mu, acc):
    (rl, ru, rlo, rhi), err, amb = exact_ranks(p, h, mu, [l, u, lo, hi])
    acc["err"] = max(acc["err"], err)
    acc["amb"] += amb
    for s in range(0, len(l), CHUNK):
        sl = slice(s, s + CHUNK)
        cl = (lo[None, :] <= u[sl, None]) & (hi[None, :] >= l[sl, None])
        wi = (lo[None, :] <= u[sl, None] + PAIR_TOL) & (hi[None, :] >= l[sl, None] - PAIR_TOL)
        ex = (rlo[None, :] <= ru[sl, None]) & (rhi[None, :] >= rl[sl, None])
        pos = (rlo[None, :] < ru[sl, None]) & (rhi[None, :] > rl[sl, None])
        lost = ex & ~cl
        acc["exact"] += int(ex.sum())
        acc["touch"] += int((ex & ~pos).sum())
        acc["lost"] += int(lost.sum())
        acc["lost_pos"] += int((lost & pos).sum())
        acc["spurious"] += int((cl & ~ex).sum())
        acc["wid_ne_exact"] += int((wi != ex).sum())
        gap = np.maximum(lo[None, :] - u[sl, None], l[sl, None] - hi[None, :])
        if (~ex).any():
            acc["min_gap"] = min(acc["min_gap"], float(gap[~ex].min()))


def pairs(n, xs, h, mu):
    acc = dict(exact=0, touch=0, lost=0, lost_pos=0, spurious=0, wid_ne_exact=0,
               err=0.0, amb=0, min_gap=math.inf)
    for t in range(n - 1):
        L, U = shells(xs[t:t + 2], h, mu, 2)
        if t >= 1:  # leaves of bag t against the cells of S_t = {t}
            Pl, Pu = shells(xs[t:t + 1], h, mu, 1)
            compare(L[:, 0], U[:, 0], Pl[:, 0], Pu[:, 0], xs[t], h, mu, acc)
        if t <= n - 3:  # leaves of bag t against the cells of S_{t+1} = {t+1}
            Pl, Pu = shells(xs[t + 1:t + 2], h, mu, 1)
            compare(L[:, 1], U[:, 1], Pl[:, 0], Pu[:, 0], xs[t + 1], h, mu, acc)
    return acc


def main():
    print("# PAIR_TOL = %.0e. Pairs summed over bags and over both tests of certificate()." % PAIR_TOL)
    print("# exact: pairs of Definition 1.2 (touch: of which boxes only touch); lost: exact but not")
    print("# found by the closed test on rounded edges; lost_pos: lost with positive-length overlap;")
    print("# spurious: closed but not exact; wid!=exact: widened test differs from exact;")
    print("# edge_err: max |rounded - exact edge|; amb: ambiguous edges at +-1; min_gap: smallest gap")
    print("# between a leaf and a cell that do not meet (floating point).")
    runs = []
    for j in range(2, 17, 2):
        runs.append(("E2", 8, 0, 3, j))
    for n, seed, mu, j in [(4, 0, 3, 6), (6, 0, 3, 8), (6, 1, 2, 5), (5, None, 1, 4)]:
        runs.append(("E3", n, seed, mu, j))
    for mu in range(1, 7):
        runs.append(("E4", 3, 0, mu, 14))
    runs += [("x*=0", 4, None, 4, 7), ("x*=0", 9, None, 4, 8)]
    xcache = {}
    for name, n, seed, mu, j in runs:
        if name == "x*=0":
            xs = np.zeros(n)
        else:
            if (n, seed) not in xcache:
                xcache[(n, seed)] = global_min(n, B, KAPPA, c_vec(n, seed))[0]
            xs = xcache[(n, seed)]
        a = pairs(n, xs, 2.0 ** -j, mu)
        print("%-4s n=%d seed=%s theta=2^-%d h=2^-%-2d exact=%8d touch=%7d lost=%5d lost_pos=%d "
              "spurious=%d wid!=exact=%d edge_err=%.1e amb=%d min_gap=%.2e" % (
                  name, n, seed, mu, j, a["exact"], a["touch"], a["lost"], a["lost_pos"],
                  a["spurious"], a["wid_ne_exact"], a["err"], a["amb"], a["min_gap"]), flush=True)


if __name__ == "__main__":
    main()
