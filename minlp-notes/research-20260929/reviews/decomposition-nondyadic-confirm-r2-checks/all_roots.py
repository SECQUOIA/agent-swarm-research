"""Full-precision roots of every certificate built by run_experiments.E2, E3 and E4, with
PAIR_TOL = 0 (first version) and 1e-12 (current), including E4 at theta = 1/64.

The certificates are enumerated by running the unchanged E2(), E3() and E4() of
run_experiments.py with its `certificate` replaced by a recorder; the case list is therefore
not copied from compare_pair_tol.py. The recorder evaluates each certificate with a row-chunked
copy of dp_certificate.certificate (same comparisons, same pair order, same min_subbox calls),
which keeps memory small at theta = 1/64. For every certificate except E4 at theta = 1/64 it
also calls the original dp_certificate.certificate at both tolerances and asserts that the
roots are bit-identical to the chunked ones. The printed E2/E3/E4 output (current tolerance)
goes to logs/E*_widened.log for diffing against the note's logs.

Usage: python3 all_roots.py
"""
import contextlib
import os
import sys
import time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "theory-decomposition"))
import dp_certificate as dc  # noqa: E402
import run_experiments as rx  # noqa: E402

assert dc.PAIR_TOL == 1e-12


def chunked(n, b, kappa, c, xstar, h, mu, slopes="affine", keep=False, tol=1e-12, chunk=20000):
    lam = np.zeros(n)
    if slopes == "affine":
        for t in range(1, n - 1):
            lam[t] = dc.dphi(xstar[t], kappa) + c[t] + b * xstar[t + 1]
    child = None
    size = 0
    store = {}
    for t in range(n - 2, -1, -1):
        last = (t == n - 2)
        L, U = dc.shells(xstar[t:t + 2], h, mu, 2)
        size += len(L)
        l1, u1, l2, u2 = L[:, 0], U[:, 0], L[:, 1], U[:, 1]
        if child is not None:
            clo, chi, cbeta = child
            off = np.empty(len(L))
            for a in range(0, len(L), chunk):
                s = slice(a, a + chunk)
                meet = (clo[None, :] <= u2[s, None] + tol) & (chi[None, :] >= l2[s, None] - tol)
                off[s] = np.where(meet, cbeta[None, :], np.inf).min(axis=1)
            lin2 = np.full(len(L), lam[t + 1])
        else:
            off = np.zeros(len(L))
            lin2 = np.zeros(len(L))
        cz2 = c[n - 1]
        if t == 0:
            vals = dc.min_subbox(l1, u1, l2, u2, l1.copy(), u1.copy(), np.full(len(L), c[0]), lin2,
                                 b, kappa, last, cz2) + off
            if keep:
                store[t] = (L, U, None)
            return float(vals.min()), size, store, lam
        Pl, Pu = dc.shells(xstar[t:t + 1], h, mu, 1)
        size += len(Pl)
        plo, phi_ = Pl[:, 0], Pu[:, 0]
        bis, dis = [], []
        for a in range(0, len(L), chunk):
            s = slice(a, a + chunk)
            meet = (plo[None, :] <= u1[s, None] + tol) & (phi_[None, :] >= l1[s, None] - tol)
            bi, di = np.nonzero(meet)
            bis.append(bi + a)
            dis.append(di)
        bi = np.concatenate(bis)
        di = np.concatenate(dis)
        L1 = np.maximum(l1[bi], plo[di])
        U1 = np.minimum(u1[bi], phi_[di])
        vals = dc.min_subbox(l1[bi], u1[bi], l2[bi], u2[bi], L1, U1, np.full(len(bi), c[t] - lam[t]),
                             lin2[bi], b, kappa, last, cz2) + off[bi]
        beta = np.full(len(plo), np.inf)
        np.minimum.at(beta, di, vals)
        child = (plo, phi_, beta)
        if keep:
            store[t] = (Pl, Pu, beta)


records = []
current = [""]
out = sys.__stdout__


def recorder(n, b, kappa, c, xstar, h, mu, slopes="affine", keep=False):
    t0 = time.time()
    r0 = chunked(n, b, kappa, c, xstar, h, mu, slopes, tol=0.0)[0]
    res = chunked(n, b, kappa, c, xstar, h, mu, slopes, keep=keep, tol=1e-12)
    r1 = res[0]
    orig = "not run"
    if not (current[0] == "E4" and mu == 6):
        o = []
        for tol in (0.0, 1e-12):
            dc.PAIR_TOL = tol
            o.append(dc.certificate(n, b, kappa, c, xstar, h, mu, slopes)[0])
        dc.PAIR_TOL = 1e-12
        assert o[0] == r0 and o[1] == r1, (o, r0, r1)
        orig = "bit-identical"
    tag = "same" if r0 == r1 else ("higher" if r0 > r1 else "lower")
    nd = bool(np.any(xstar))
    records.append((current[0], n, h, mu, slopes, nd, r0, r1, tag))
    print("%s n=%d h=2^%d mu=%d %-6s nondyadic=%-5s root0=%.17g root1=%.17g diff=%.4e %-6s "
          "original code: %s  %.0fs" % (current[0], n, int(np.log2(h)), mu, slopes, nd, r0, r1,
                                        r0 - r1, tag, orig, time.time() - t0), file=out, flush=True)
    return res


rx.certificate = recorder
for name, fn in [("E2", rx.E2), ("E3", rx.E3), ("E4", rx.E4)]:
    current[0] = name
    with open(os.path.join(HERE, "logs", name + "_widened.log"), "w") as f, contextlib.redirect_stdout(f):
        fn()

for label, sel in [("all", lambda r: True),
                   ("excluding E4 theta=1/64", lambda r: not (r[0] == "E4" and r[3] == 6))]:
    rs = [r for r in records if sel(r)]
    nd = [r for r in rs if r[5]]
    cnt = {k: sum(1 for r in nd if r[8] == k) for k in ("same", "higher", "lower")}
    print("%s: %d certificates, %d non-dyadic: same %d, higher %d, lower %d; dyadic all same: %s" % (
        label, len(rs), len(nd), cnt["same"], cnt["higher"], cnt["lower"],
        all(r[8] == "same" for r in rs if not r[5])), file=out, flush=True)
