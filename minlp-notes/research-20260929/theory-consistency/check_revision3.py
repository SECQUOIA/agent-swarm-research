"""Checks for the third revision (after the confirmation; Section 12.3 of the note).

(1) Proposition 5.6: for which n the logged ratio 30 (3 + c) n gap grows with
    c.  Reads section (3) of logs/check_revision2.log (lower estimates) and
    classifies each n as increasing, decreasing or not monotone in
    c = 0.5, 2, 8.
(2) T1 at finite K (Section 3, Remarks): step 3 of the proof that
    gap > 2 E_n.  For the split phi_1 = phi_2 = -p, with p a near-best
    degree-n approximant of |s| and r = |s| - p, the middle-bag minimum
    m_B = min_{s1,s2} [r(s1) - r(s2) + K (s1 - s2)^2] is strictly below
    min_s (r_1 - r_2) = 0.  A lower bound on -m_B is computed by taking
    s1 = s2 + delta over a fine grid of s2 and a finite set of delta (so it
    is a valid lower bound up to rounding); the upper bound is
    Lip(r)^2 / (4K).  This illustrates one step of the proof; the proof
    itself covers all splits.  Floating point, not certified.
"""
import re
import numpy as np
from numpy.polynomial import chebyshev as C
from consistency_lib import grid, cheb_basis, band_gap

out = None


def log(m):
    print(m)
    if out is not None:
        out.write(m + "\n")
        out.flush()


def ratio_monotonicity():
    log("(1) Proposition 5.6 ratio 30 (3+c) n gap (lower estimates, logs/check_revision2.log) against c = 0.5, 2, 8")
    txt = open("logs/check_revision2.log").read().split("(3) Proposition 5.6")[1]
    vals = {}
    for line in txt.splitlines():
        m = re.match(r"\s*c=([\d.]+):", line)
        if m:
            for n, lo in re.findall(r"n=(\d+)(?: \(log\))?: ([\d.]+)/", line):
                vals.setdefault(int(n), []).append(float(lo))
    for n in sorted(vals):
        v = vals[n]
        d = np.diff(v)
        kind = "increasing" if np.all(d > 0) else "decreasing" if np.all(d < 0) else "not monotone"
        log(f"  n={n:3d}: " + ", ".join(f"{x:.1f}" for x in v) + f"  -> {kind} in c")


def t1_step3():
    log("(2) T1, split -p: lower bound on -m_B (middle bag below min(r_1 - r_2) = 0) against Lip(r)^2/(4K)")
    s = grid(-1, 1, 20001, (0.0,))
    sf = np.linspace(-1, 1, 100001)
    for n in [4, 8]:
        g, c, _, _ = band_gap(cheb_basis(s, n), -np.abs(s), -np.abs(s), tight=True)

        def r(x):
            return np.abs(x) + C.chebval(x, c)          # |x| - p(x), p = -(B c)

        rf = r(sf)
        osc = rf.max() - rf.min()
        dp = C.chebval(sf, C.chebder(c))
        lip = np.max(np.abs(np.sign(sf) + dp))
        log(f"  n={n}: 2E_n (grid LP) = {g:.6f}, osc(r) = {osc:.6f}, Lip(r) = {lip:.4f}")
        for K in [10.0, 100.0, 1000.0, 10000.0]:
            dmax = 2 * lip / K
            best = -np.inf
            for delta in np.concatenate([np.linspace(dmax / 400, dmax, 400), -np.linspace(dmax / 400, dmax, 400)]):
                ok = np.abs(sf + delta) <= 1
                val = np.max(rf[ok] - r(sf[ok] + delta)) - K * delta ** 2
                best = max(best, val)
            ub = lip ** 2 / (4 * K)
            log(f"    K={K:7.0f}: -m_B >= {best:.3e} > 0 ({'yes' if best > 0 else 'NO'}); upper bound {ub:.3e}; "
                f"gap(-p)/osc(r) in [{1 + best / osc:.5f}, {1 + ub / osc:.5f}]")


if __name__ == "__main__":
    out = open("logs/check_revision3.log", "w")
    ratio_monotonicity()
    t1_step3()
