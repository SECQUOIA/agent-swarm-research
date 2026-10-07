"""Check of decomposition-certificates.md, Sections 5.2-5.3 (certificates centred at a non-dyadic x*),
for leaf-cell pairs lost to rounding of shell-partition edges.

dp_certificate.certificate pairs a leaf with a cell when their closed intervals meet, tested on
rounded floating-point edges. Around a non-dyadic centre, edges that coincide in exact arithmetic
can differ by one rounding unit, and a touching pair can then be dropped.

certificate_mode() below is dp_certificate.certificate with a selectable pairing test:
  closed : closed test on the rounded edges (the original code; checked to give the same pairs)
  tol    : closed test widened by 1e-12 (the fix used in adaptive/rc_lib.py)
  exact  : closed test on the exact rational edges (Definition 1.2 / Lemma 1.5)
  open   : only pairs whose intervals overlap with positive length in exact arithmetic
The exact edges are computed with fractions.Fraction from the same float centre x*, so the boxes
are the same as in dp_certificate.shells up to rounding of their edges.

The experiment functions E2, E3, E4 of theory-decomposition/run_experiments.py are run unchanged
with run_experiments.certificate replaced by certificate_mode.

  python3 nondyadic_check.py MODE EXP      MODE in closed|tol|exact|open, EXP in E2|E3|E4m5|E1x0

Every run also prints, per certificate, the number of (leaf, cell) pairs under all four tests,
the pairs on which they differ, and the largest difference between a float edge and its exact value.
"""
import math
import os
import sys
import itertools
from fractions import Fraction
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "theory-decomposition"))
import dp_certificate as dc  # noqa: E402
import run_experiments as rx  # noqa: E402

TOL = 1e-12
STATS = []  # per certificate: dict of pair counts per mode


def exact_axis(pv, h, mu, J, lo, hi):
    """Exact edges of the shell partition on one axis. Returns (rank function, level-0 ranks,
    per-level rank arrays, rank of lo, rank of hi, sorted exact values)."""
    P, H = Fraction(pv), Fraction(h)
    Nax = 2 ** (mu + 2)
    lev0 = [P - H, P, P + H]
    levs = []
    for j in range(1, J + 1):
        R = Fraction(2) ** j * H
        g = Fraction(1, 2 ** mu) * Fraction(2) ** (j - 1) * H
        levs.append([P - R + g * k for k in range(Nax + 1)])
    vals = sorted(set(lev0 + [v for L in levs for v in L] + [Fraction(lo), Fraction(hi)]))
    rk = {v: i for i, v in enumerate(vals)}
    return ([rk[v] for v in lev0], [np.array([rk[v] for v in L]) for L in levs],
            rk[Fraction(lo)], rk[Fraction(hi)], vals)


def shells_ranked(p, h, mu, dim, lo=-1.0, hi=1.0):
    """dc.shells plus the exact rank of every edge (ranks of one axis are comparable across calls
    with the same centre coordinate). Also returns diagnostics of float versus exact edges."""
    p = np.asarray(p, float)
    J = max(0, math.ceil(math.log2((hi - lo) / h)))
    ax = [exact_axis(p[a], h, mu, J, lo, hi) for a in range(dim)]
    corners = np.array(list(itertools.product([0, 1], repeat=dim)), int)
    RL = [np.stack([np.array(ax[a][0])[corners[:, a]] for a in range(dim)], axis=1)]
    RU = [np.stack([np.array(ax[a][0])[corners[:, a] + 1] for a in range(dim)], axis=1)]
    Nax = 2 ** (mu + 2)
    ar = np.arange(Nax)
    grids = np.stack(np.meshgrid(*([ar] * dim), indexing="ij"), axis=-1).reshape(-1, dim)
    inner = np.all((grids >= Nax // 4) & (grids < 3 * Nax // 4), axis=1)
    grids = grids[~inner]
    ok_mismatch = 0
    for j in range(1, J + 1):
        R = 2.0 ** j * h
        g = 2.0 ** (-mu) * 2.0 ** (j - 1) * h
        edges = p[None, :] - R + g * np.arange(Nax + 1)[:, None]
        cl = np.stack([edges[grids[:, a], a] for a in range(dim)], axis=1)
        cu = np.stack([edges[grids[:, a] + 1, a] for a in range(dim)], axis=1)
        ok = np.all((cu > lo) & (cl < hi), axis=1)
        rl = np.stack([ax[a][1][j - 1][grids[:, a]] for a in range(dim)], axis=1)
        ru = np.stack([ax[a][1][j - 1][grids[:, a] + 1] for a in range(dim)], axis=1)
        ok_ex = np.all((ru > np.array([ax[a][2] for a in range(dim)])) &
                       (rl < np.array([ax[a][3] for a in range(dim)])), axis=1)
        ok_mismatch += int(np.sum(ok != ok_ex))
        RL.append(rl[ok])
        RU.append(ru[ok])
    L, U = dc.shells(p, h, mu, dim, lo, hi)  # the original boxes
    RL, RU = np.concatenate(RL), np.concatenate(RU)
    rlo = np.array([ax[a][2] for a in range(dim)])
    rhi = np.array([ax[a][3] for a in range(dim)])
    RL, RU = np.clip(RL, rlo, rhi), np.clip(RU, rlo, rhi)
    # the float keep-filter of dc.shells, reconstructed, versus the exact one
    keep_ex = np.all(RU > RL, axis=1)
    # recompute the float boxes in the same order as the ranks to align them with dc.shells
    Lf, Uf = _shells_unfiltered(p, h, mu, dim, lo, hi)
    keep_f = np.all(Uf - Lf > 1e-15, axis=1)
    assert np.array_equal(Lf[keep_f], L) and np.array_equal(Uf[keep_f], U)
    diag = dict(ok_mismatch=ok_mismatch, keep_mismatch=int(np.sum(keep_f != keep_ex)))
    RL, RU = RL[keep_f], RU[keep_f]
    # float edge versus exact edge: largest difference in units of 1e-16
    err = 0.0
    for a in range(dim):
        vals = ax[a][4]
        ex_l = np.array([float(vals[r]) for r in RL[:, a]])
        ex_u = np.array([float(vals[r]) for r in RU[:, a]])
        err = max(err, float(np.max(np.abs(ex_l - L[:, a]))), float(np.max(np.abs(ex_u - U[:, a]))))
    diag["max_edge_err"] = err
    return L, U, RL, RU, diag


def _shells_unfiltered(p, h, mu, dim, lo, hi):
    """dc.shells without the final keep filter (same arithmetic, same order)."""
    J = max(0, math.ceil(math.log2((hi - lo) / h)))
    corners = np.array(list(itertools.product([0, 1], repeat=dim)), float)
    Ls = [p[None, :] + (corners - 1) * h]
    Us = [Ls[0] + h]
    Nax = 2 ** (mu + 2)
    ar = np.arange(Nax)
    grids = np.stack(np.meshgrid(*([ar] * dim), indexing="ij"), axis=-1).reshape(-1, dim)
    inner = np.all((grids >= Nax // 4) & (grids < 3 * Nax // 4), axis=1)
    grids = grids[~inner]
    for j in range(1, J + 1):
        R = 2.0 ** j * h
        g = 2.0 ** (-mu) * 2.0 ** (j - 1) * h
        edges = p[None, :] - R + g * np.arange(Nax + 1)[:, None]
        cl = np.stack([edges[grids[:, a], a] for a in range(dim)], axis=1)
        cu = np.stack([edges[grids[:, a] + 1, a] for a in range(dim)], axis=1)
        ok = np.all((cu > lo) & (cl < hi), axis=1)
        Ls.append(cl[ok])
        Us.append(cu[ok])
    return np.clip(np.concatenate(Ls), lo, hi), np.clip(np.concatenate(Us), lo, hi)


def pair_sets(clo, chi, crl, cru, l, u, rl, ru):
    """(leaf, cell) pairs under the four tests. Dense boolean matrices, as in dc.certificate."""
    out = {}
    out["closed"] = (clo[None, :] <= u[:, None]) & (chi[None, :] >= l[:, None])
    out["tol"] = (clo[None, :] <= u[:, None] + TOL) & (chi[None, :] >= l[:, None] - TOL)
    out["exact"] = (crl[None, :] <= ru[:, None]) & (cru[None, :] >= rl[:, None])
    out["open"] = (crl[None, :] < ru[:, None]) & (cru[None, :] > rl[:, None])
    return out


def certificate_mode(n, b, kappa, c, xstar, h, mu, slopes="affine", keep=False, mode="closed"):
    """dc.certificate with the pairing test chosen by `mode` (see module docstring)."""
    lam = np.zeros(n)
    if slopes == "affine":
        for t in range(1, n - 1):
            lam[t] = dc.dphi(xstar[t], kappa) + c[t] + b * xstar[t + 1]
    child = None
    size = 0
    store = {}
    st = dict(n=n, h=h, mu=mu, slopes=slopes, closed=0, tol=0, exact=0, open=0,
              closed_minus_exact=0, exact_minus_closed=0, tol_ne_exact=0, open_minus_closed=0,
              ok_mismatch=0, keep_mismatch=0, max_edge_err=0.0)

    def tally(S):
        for k in ("closed", "tol", "exact", "open"):
            st[k] += int(S[k].sum())
        st["closed_minus_exact"] += int(np.sum(S["closed"] & ~S["exact"]))
        st["exact_minus_closed"] += int(np.sum(S["exact"] & ~S["closed"]))
        st["tol_ne_exact"] += int(np.sum(S["tol"] != S["exact"]))
        st["open_minus_closed"] += int(np.sum(S["open"] & ~S["closed"]))

    def note(diag):
        st["ok_mismatch"] += diag["ok_mismatch"]
        st["keep_mismatch"] += diag["keep_mismatch"]
        st["max_edge_err"] = max(st["max_edge_err"], diag["max_edge_err"])

    for t in range(n - 2, -1, -1):
        last = (t == n - 2)
        L, U, RL, RU, diag = shells_ranked(xstar[t:t + 2], h, mu, 2)
        note(diag)
        size += len(L)
        l1, u1, l2, u2 = L[:, 0], U[:, 0], L[:, 1], U[:, 1]
        if child is not None:
            clo, chi, crl, cru, cbeta = child
            S = pair_sets(clo, chi, crl, cru, l2, u2, RL[:, 1], RU[:, 1])
            tally(S)
            off = np.where(S[mode], cbeta[None, :], np.inf).min(axis=1)
            lin2 = np.full(len(L), lam[t + 1])
        else:
            off = np.zeros(len(L))
            lin2 = np.zeros(len(L))
        cz2 = c[n - 1]
        if t == 0:
            vals = dc.min_subbox(l1, u1, l2, u2, l1.copy(), u1.copy(), np.full(len(L), c[0]), lin2,
                                 b, kappa, last, cz2) + off
            st["root"] = float(vals.min())
            STATS.append(st)
            if keep:
                store[t] = (L, U, None)
            return float(vals.min()), size, store, lam
        Pl, Pu, PRl, PRu, diag = shells_ranked(xstar[t:t + 1], h, mu, 1)
        note(diag)
        size += len(Pl)
        plo, phi_ = Pl[:, 0], Pu[:, 0]
        S = pair_sets(plo, phi_, PRl[:, 0], PRu[:, 0], l1, u1, RL[:, 0], RU[:, 0])
        tally(S)
        bi, di = np.nonzero(S[mode])
        L1 = np.maximum(l1[bi], plo[di])
        U1 = np.minimum(u1[bi], phi_[di])
        vals = dc.min_subbox(l1[bi], u1[bi], l2[bi], u2[bi], L1, U1,
                             np.full(len(bi), c[t] - lam[t]), lin2[bi], b, kappa, last, cz2) + off[bi]
        beta = np.full(len(plo), np.inf)
        np.minimum.at(beta, di, vals)
        child = (plo, phi_, PRl[:, 0], PRu[:, 0], beta)
        if keep:
            store[t] = (Pl, Pu, beta)


def print_stats():
    print("# pair counts summed over bags: closed(rounded) tol exact open; closed\\exact; exact\\closed; "
          "tol!=exact; open\\closed; filter mismatches (ok, keep); max |float edge - exact edge|; root l_r (this mode)")
    for s in STATS:
        print("# n=%d h=2^%d theta=2^-%d %-6s: %d %d %d %d | %d %d %d %d | %d %d | %.1e | %r" % (
            s["n"], round(math.log2(s["h"])), s["mu"], s["slopes"], s["closed"], s["tol"], s["exact"],
            s["open"], s["closed_minus_exact"], s["exact_minus_closed"], s["tol_ne_exact"],
            s["open_minus_closed"], s["ok_mismatch"], s["keep_mismatch"], s["max_edge_err"], s["root"]))


def E1x0():
    """Two c = 0 (x* = 0, dyadic) certificates of Section 5.4, for the pair-set comparison only."""
    for n, j, mu in [(4, 10, 4), (8, 8, 4)]:
        r, size, _, _ = rx.certificate(n, rx.B, rx.KAPPA, np.zeros(n), np.zeros(n), 2.0 ** -j, mu)
        print("n=%d h=2^-%d theta=2^-%d: gap %.3e size %d" % (n, j, mu, -r, size), flush=True)


def E4m5(n=3, seed=0):
    """rx.E4 restricted to theta >= 1/32 (the rows quoted in Section 5.3); same printout."""
    c = rx.c_vec(n, seed)
    xs, fs, _ = rx.global_min(n, rx.B, rx.KAPPA, c)
    lam = [dc.dphi(xs[t], rx.KAPPA) + c[t] + rx.B * xs[t + 1] for t in range(1, n - 1)]
    print("# E4: n=%d seed %d, h=2^-14; slopes %s; x* = %s" % (
        n, seed, np.array2string(np.array(lam), precision=4), np.array2string(xs, precision=4)))
    print("# mu theta gap_affine gap_zero size")
    for mu in range(1, 6):
        ra, size, _, _ = rx.certificate(n, rx.B, rx.KAPPA, c, xs, 2.0 ** -14, mu, "affine")
        rz, _, _, _ = rx.certificate(n, rx.B, rx.KAPPA, c, xs, 2.0 ** -14, mu, "zero")
        print("%d %.4f %.3e %.3e %d" % (mu, 2.0 ** -mu, fs - ra, fs - rz, size), flush=True)


if __name__ == "__main__":
    mode, exp = sys.argv[1], sys.argv[2]
    assert mode in ("closed", "tol", "exact", "open")
    rx.certificate = lambda *a, **k: certificate_mode(*a, mode=mode, **k)
    print("# mode = %s" % mode)
    if exp in ("E1x0", "E4m5"):
        globals()[exp]()
    else:
        getattr(rx, exp)()
    print_stats()
