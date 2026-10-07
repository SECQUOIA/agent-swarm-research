"""Root bounds of the E2, E3 and E4 certificates with PAIR_TOL = 0 and 1e-12, computed without
dense (leaf, cell) arrays and without the row-chunked copy in
decomposition-nondyadic-confirm-r2-checks/all_roots.py.

Pairs are found by binary search: the cells of a 1D separator partition are sorted by lower
edge, and the script asserts that both edge arrays are then strictly increasing. The closed test
  lo_k <= u + tol  and  hi_k >= l - tol
then selects the contiguous index range [searchsorted(hi, l - tol, 'left'),
searchsorted(lo, u + tol, 'right')). The bounds u + tol and l - tol are the same floating-point
numbers as in dp_certificate.certificate(), so the pair set equals the dense test's pair set.
The DP (min_subbox, min over pairs) is otherwise the same as certificate(); min is exact, so the
order of the pairs does not matter.

Validation: every case of theory-decomposition/compare_pair_tol.py (all E2, E3 and E4 with
mu <= 5; roots there come from the original certificate()) must give bit-identical roots.
Then E4 at theta = 1/64 (mu = 6), both slopes, both tolerances. Pair counts summed over both
tests are printed for comparison with logs/check_pairs_exact.log.
Usage: python3 ranges_roots.py
"""
import os
import re
import sys
import time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TD = os.path.join(HERE, "..", "..", "theory-decomposition")
sys.path.insert(0, TD)
import dp_certificate as dc  # noqa: E402
from run_experiments import c_vec, B, KAPPA  # noqa: E402


def range_pairs(l, u, clo, chi, tol):
    """(leaf index, cell index) pairs with clo <= u + tol and chi >= l - tol."""
    order = np.argsort(clo, kind="stable")
    lo_s, hi_s = clo[order], chi[order]
    assert np.all(np.diff(lo_s) > 0) and np.all(np.diff(hi_s) > 0)
    end = np.searchsorted(lo_s, u + tol, side="right")
    start = np.searchsorted(hi_s, l - tol, side="left")
    cnt = np.maximum(end - start, 0)
    bi = np.repeat(np.arange(len(l)), cnt)
    first = np.repeat(start, cnt)
    offs = np.arange(cnt.sum()) - np.repeat(np.cumsum(cnt) - cnt, cnt)
    di = order[first + offs]
    return bi, di


def cert(n, b, kappa, c, xstar, h, mu, slopes, tol):
    lam = np.zeros(n)
    if slopes == "affine":
        for t in range(1, n - 1):
            lam[t] = dc.dphi(xstar[t], kappa) + c[t] + b * xstar[t + 1]
    child = None
    size = 0
    npairs = 0
    info = {}
    for t in range(n - 2, -1, -1):
        last = (t == n - 2)
        L, U = dc.shells(xstar[t:t + 2], h, mu, 2)
        size += len(L)
        info["leaves_bag%d" % t] = len(L)
        l1, u1, l2, u2 = L[:, 0], U[:, 0], L[:, 1], U[:, 1]
        if child is not None:
            clo, chi, cbeta = child
            qi, ki = range_pairs(l2, u2, clo, chi, tol)
            npairs += len(qi)
            off = np.full(len(L), np.inf)
            np.minimum.at(off, qi, cbeta[ki])
            lin2 = np.full(len(L), lam[t + 1])
        else:
            off = np.zeros(len(L))
            lin2 = np.zeros(len(L))
        cz2 = c[n - 1]
        if t == 0:
            vals = dc.min_subbox(l1, u1, l2, u2, l1.copy(), u1.copy(), np.full(len(L), c[0]), lin2,
                                 b, kappa, last, cz2) + off
            return float(vals.min()), size, npairs, info
        Pl, Pu = dc.shells(xstar[t:t + 1], h, mu, 1)
        size += len(Pl)
        info["cells_sep%d" % t] = len(Pl)
        plo, phi_ = Pl[:, 0], Pu[:, 0]
        bi, di = range_pairs(l1, u1, plo, phi_, tol)
        npairs += len(bi)
        L1 = np.maximum(l1[bi], plo[di])
        U1 = np.minimum(u1[bi], phi_[di])
        vals = dc.min_subbox(l1[bi], u1[bi], l2[bi], u2[bi], L1, U1, np.full(len(bi), c[t] - lam[t]),
                             lin2[bi], b, kappa, last, cz2) + off[bi]
        beta = np.full(len(plo), np.inf)
        np.minimum.at(beta, di, vals)
        child = (plo, phi_, beta)


def cases():
    c = c_vec(8, 0)
    xs = dc.global_min(8, B, KAPPA, c)[0]
    for j in range(2, 17, 2):
        for s in ["affine", "zero"]:
            yield "E2 h=2^-%d %s" % (j, s), 8, c, xs, 2.0 ** -j, 3, s
    for n, seed, mu, j in [(4, 0, 3, 6), (6, 0, 3, 8), (6, 1, 2, 5), (5, None, 1, 4)]:
        c = c_vec(n, seed)
        xs = dc.global_min(n, B, KAPPA, c)[0]
        for s in ["affine", "zero"]:
            yield "E3 n=%d seed=%s %s" % (n, seed, s), n, c, xs, 2.0 ** -j, mu, s
    c = c_vec(3, 0)
    xs = dc.global_min(3, B, KAPPA, c)[0]
    for mu in range(1, 7):
        for s in ["affine", "zero"]:
            yield "E4 theta=2^-%d %s" % (mu, s), 3, c, xs, 2.0 ** -14, mu, s


ref = {}
with open(os.path.join(TD, "logs", "compare_pair_tol.log")) as f:
    for line in f:
        m = re.match(r"(E\d .*?)\s+x\*=0:\S+\s+root\(tol=0\)=(\S+) root\(tol=1e-12\)=(\S+)", line)
        if m:
            ref[m.group(1).strip()] = (float(m.group(2)), float(m.group(3)))
print("# reference roots read from compare_pair_tol.log: %d cases" % len(ref), flush=True)

cnt = {"same": 0, "higher": 0, "lower": 0}
nmatch = 0
fstar = dc.global_min(3, B, KAPPA, c_vec(3, 0))[1]
for name, n, c, xs, h, mu, s in cases():
    t0 = time.time()
    r0, size, p0, info = cert(n, B, KAPPA, c, xs, h, mu, s, 0.0)
    r1, size1, p1, _ = cert(n, B, KAPPA, c, xs, h, mu, s, 1e-12)
    assert size == size1
    tag = "same" if r0 == r1 else ("higher" if r0 > r1 else "lower")
    nd = bool(np.any(xs))
    if nd:
        cnt[tag] += 1
    if name in ref:
        ok = ref[name] == (r0, r1)
        nmatch += ok
        cmp = "equals compare_pair_tol.log: %s" % ok
    else:
        cmp = "not in compare_pair_tol.log; gap(1e-12)=%.3e size=%d %s" % (fstar - r1, size, info)
    print("%-22s nondyadic=%-5s root0=%.17g root1=%.17g %-6s pairs0=%d pairs1=%d lost=%d  %s  %.0fs" % (
        name, nd, r0, r1, tag, p0, p1, p1 - p0, cmp, time.time() - t0), flush=True)
print("matched %d of %d reference cases; non-dyadic: same %d, higher %d, lower %d" % (
    nmatch, len(ref), cnt["same"], cnt["higher"], cnt["lower"]))
