"""Independent check of the (leaf, cell) pair tests in dp_certificate.certificate().

Differs from theory-decomposition/check_pairs_exact.py in method:
- exact edges are built with fractions.Fraction from the formulas of shells() (central box
  p + (corner - 1) h, level-j edges p - 2^j h + 2^(j-1-mu) h k, exact clipping at +-1, exact
  'ok' and 'keep' filters), not by rounding float edges to a lattice; the exact boxes are then
  aligned with the float output of dp_certificate.shells (same count, |float - exact| checked);
- pair sets are counted as index ranges over the cells sorted by exact lower edge (cells
  partition [-1, 1]), not by dense matrices.
For every partition it prints the exact closed pair count, how many only touch, how many the
unwidened float test loses (and how many of those overlap with positive length), spurious
pairs, and pairs where the test widened by PAIR_TOL differs from the exact closed test.
Usage: python3 pairs_ranges.py [max_mu_E4]
"""
import sys, os, math, itertools
from fractions import Fraction
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "theory-decomposition"))
import dp_certificate as dc
from run_experiments import c_vec, B, KAPPA

TOL = dc.PAIR_TOL
ONE = Fraction(1)


def clip(v):
    return min(max(v, -ONE), ONE)


def exact_shells(p, h, mu, dim):
    """Exact counterpart of dc.shells: returns lists of (Fraction lower, Fraction upper) per axis
    as integer indices into a value table, plus the table."""
    P = [Fraction(float(x)) for x in p]
    H = Fraction(h)
    J = max(0, math.ceil(math.log2(2.0 / h)))
    corners = list(itertools.product([0, 1], repeat=dim))
    boxes = []  # list of tuples of (lo, hi) Fractions per axis, unclipped
    for cor in corners:
        boxes.append(tuple((P[a] + (cor[a] - 1) * H, P[a] + cor[a] * H) for a in range(dim)))
    Nax = 2 ** (mu + 2)
    grid = [g for g in itertools.product(range(Nax), repeat=dim)
            if not all(Nax // 4 <= gi < 3 * Nax // 4 for gi in g)]
    for j in range(1, J + 1):
        R = 2 ** j * H
        g = Fraction(1, 2 ** mu) * 2 ** (j - 1) * H
        edges = [[P[a] - R + g * k for k in range(Nax + 1)] for a in range(dim)]
        for gi in grid:
            lo = [edges[a][gi[a]] for a in range(dim)]
            hi = [edges[a][gi[a] + 1] for a in range(dim)]
            if all(hi[a] > -1 and lo[a] < 1 for a in range(dim)):
                boxes.append(tuple((lo[a], hi[a]) for a in range(dim)))
    out = []
    for bx in boxes:
        cb = tuple((clip(l), clip(u)) for l, u in bx)
        if all(u - l > Fraction(1e-15) for l, u in cb):
            out.append(cb)
    return out


def aligned(p, h, mu, dim):
    """Float boxes from dc.shells and exact boxes; checks that they correspond one to one."""
    L, U = dc.shells(np.asarray(p, float), h, mu, dim)
    ex = exact_shells(p, h, mu, dim)
    assert len(ex) == len(L), (len(ex), len(L))
    err = 0.0
    for i, bx in enumerate(ex):
        for a in range(dim):
            err = max(err, abs(float(bx[a][0] - Fraction(float(L[i, a])))),
                      abs(float(bx[a][1] - Fraction(float(U[i, a])))))
    assert err < 1e-14, err
    return L, U, ex, err


def count(lf, uf, lx, ux, clo_f, chi_f, clo_x, chi_x, acc):
    """lf, uf: float leaf edges in one coordinate; lx, ux: exact (Fractions). Same for cells."""
    vals = sorted(set(lx) | set(ux) | set(clo_x) | set(chi_x))
    rk = {v: i for i, v in enumerate(vals)}
    rl = np.array([rk[v] for v in lx]); ru = np.array([rk[v] for v in ux])
    rlo = np.array([rk[v] for v in clo_x]); rhi = np.array([rk[v] for v in chi_x])
    o = np.argsort(rlo)
    rlo, rhi, flo, fhi = rlo[o], rhi[o], clo_f[o], chi_f[o]
    assert np.all(rhi[:-1] == rlo[1:]), "cells do not tile"
    assert np.all(np.diff(flo) > 0) and np.all(np.diff(fhi) > 0), "float cell edges not monotone"
    rng = lambda a, b: (a, np.maximum(a, b))
    E = rng(np.searchsorted(rhi, rl, "left"), np.searchsorted(rlo, ru, "right"))
    Pp = rng(np.searchsorted(rhi, rl, "right"), np.searchsorted(rlo, ru, "left"))
    C = rng(np.searchsorted(fhi, lf, "left"), np.searchsorted(flo, uf, "right"))
    W = rng(np.searchsorted(fhi, lf - TOL, "left"), np.searchsorted(flo, uf + TOL, "right"))
    size = lambda R: R[1] - R[0]
    inter = lambda R, S: np.maximum(0, np.minimum(R[1], S[1]) - np.maximum(R[0], S[0]))
    acc["exact"] += int(size(E).sum())
    acc["touch"] += int((size(E) - size(Pp)).sum())
    acc["lost"] += int((size(E) - inter(E, C)).sum())
    acc["lost_pos"] += int((size(Pp) - inter(Pp, C)).sum())
    acc["spurious"] += int((size(C) - inter(C, E)).sum())
    acc["wid_ne_exact"] += int((size(W) + size(E) - 2 * inter(W, E)).sum())
    # smallest float gap between a leaf and a cell that does not meet it (exactly)
    left = E[0] - 1
    m = left >= 0
    if m.any():
        acc["min_gap"] = min(acc["min_gap"], float((lf[m] - fhi[left[m]]).min()))
    right = E[1]
    m = right < len(flo)
    if m.any():
        acc["min_gap"] = min(acc["min_gap"], float((flo[right[m]] - uf[m]).min()))


def partition(n, xs, h, mu):
    acc = dict(exact=0, touch=0, lost=0, lost_pos=0, spurious=0, wid_ne_exact=0, err=0.0, min_gap=math.inf)
    cells = {}
    for t in range(1, n - 1):
        Pl, Pu, pex, e = aligned(xs[t:t + 1], h, mu, 1)
        acc["err"] = max(acc["err"], e)
        cells[t] = (Pl[:, 0], Pu[:, 0], [b[0][0] for b in pex], [b[0][1] for b in pex])
    for t in range(n - 1):
        L, U, lex, e = aligned(xs[t:t + 2], h, mu, 2)
        acc["err"] = max(acc["err"], e)
        if t >= 1:
            count(L[:, 0], U[:, 0], [b[0][0] for b in lex], [b[0][1] for b in lex], *cells[t], acc)
        if t <= n - 3:
            count(L[:, 1], U[:, 1], [b[1][0] for b in lex], [b[1][1] for b in lex], *cells[t + 1], acc)
    return acc


def main():
    max_mu = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    print("# PAIR_TOL = %g; columns as in theory-decomposition/logs/check_pairs_exact.log" % TOL)
    runs = [("E2", 8, 0, 3, j) for j in range(2, 17, 2)]
    runs += [("E3", n, s, mu, j) for n, s, mu, j in [(4, 0, 3, 6), (6, 0, 3, 8), (6, 1, 2, 5), (5, None, 1, 4)]]
    runs += [("E4", 3, 0, mu, 14) for mu in range(1, max_mu + 1)]
    runs += [("x*=0", 4, None, 4, 7), ("x*=0", 9, None, 4, 8)]
    xcache = {}
    for name, n, seed, mu, j in runs:
        if seed is None and name != "E3":
            xs = np.zeros(n)
        else:
            if (n, seed) not in xcache:
                xcache[(n, seed)] = dc.global_min(n, B, KAPPA, c_vec(n, seed))[0]
            xs = xcache[(n, seed)]
        a = partition(n, xs, 2.0 ** -j, mu)
        print("%-4s n=%d seed=%s theta=2^-%d h=2^-%-2d exact=%8d touch=%7d lost=%5d lost_pos=%d "
              "spurious=%d wid!=exact=%d edge_err=%.1e min_gap=%.2e" % (
                  name, n, seed, mu, j, a["exact"], a["touch"], a["lost"], a["lost_pos"],
                  a["spurious"], a["wid_ne_exact"], a["err"], a["min_gap"]), flush=True)


if __name__ == "__main__":
    main()
