"""Check for Proposition 5 (revision round 2): the sufficient condition needs
the cell slopes.

Instance of the confirmation review (item M1): n = 1, one separator
variable s in I = [-1, 1], root bag f_r(s) = -lam s + M s^2/2, leaf bag
f_l(s) = lam s + M s^2/2, so f* = 0, U = f_l, L = lam s - M s^2/2,
w = M s^2.  Leaves are exact (no bag error) and aligned with the cells,
so the certificate value with slopes mu_D and maximal intercepts is

  l_r = min_D [ min_{cl D} (f_r + mu_D s) + min_{cl D} (f_l - mu_D s) ].

Cells: rule R3 adapted to the discount tau' = 1/(3n+1) (proof of Theorem 3
with h = 4r/tau'), tolerance eps/(2n):

  interior (dist(D, dI) >= 4r/tau'): B'(D) = (16/tau' + 1/2) M r^2 - tau' w_min,
  otherwise:                         B'(D) = 2 G r + (5/2) M r^2 - 2 tau' w_min.

Slopes compared on these cells:
  (a) mu_D = 0 (constant minorants);
  (b) the slope of the balanced minimizer of the closed-cell bracket with
      half-width tau' w (here psi' = U - w/2 = lam s, so mu_D = lam);
  (c) mu_D = lam + nu_D with nu_D > 0 the largest perturbation whose
      closed-cell bracket, minimized over the intercept, is <= eps/(2n).
Proposition 5 (with the slope clause) predicts gap <= eps/2 for (b) and
(c) (exact leaves: the bag terms are <= 0).  For (a) it predicts nothing.
All minima of quadratics on intervals are exact.
"""
import numpy as np


def qmin(a, b, lo, hi):
    """min over [lo, hi] of a s^2 + b s with a >= 0."""
    cands = [lo, hi]
    if a > 0:
        v = -b / (2 * a)
        if lo < v < hi:
            cands.append(v)
    return min(a * x * x + b * x for x in cands)


def qmax(a, b, lo, hi):
    """max over [lo, hi] of -a s^2 + b s with a >= 0."""
    return -qmin(a, -b, lo, hi)


def partition(lam, M, eps, n=1):
    tau = 1.0 / (3 * n + 1)
    G = abs(lam) + M
    tol = eps / (2 * n)
    out, stack = [], [(-1.0, 1.0)]
    while stack:
        lo, hi = stack.pop()
        r = (hi - lo) / 2
        wmin = M * (0.0 if lo <= 0 <= hi else min(lo * lo, hi * hi))
        if min(lo + 1, 1 - hi) >= 4 * r / tau:
            B = (16 / tau + 0.5) * M * r * r - tau * wmin
        else:
            B = 2 * G * r + 2.5 * M * r * r - 2 * tau * wmin
        if B > tol:
            mid = (lo + hi) / 2
            stack += [(lo, mid), (mid, hi)]
        else:
            out.append((lo, hi))
    return sorted(out)


def gap(cells, slopes, lam, M):
    lr = min(qmin(M / 2, mu - lam, lo, hi) + qmin(M / 2, lam - mu, lo, hi)
             for (lo, hi), mu in zip(cells, slopes))
    return -lr


def bracket(nu, lo, hi, M, tau):
    # closed-cell bracket of slope lam + nu around psi' = lam s, half-width
    # tau w = tau M s^2, minimized over the intercept
    return qmax(tau * M, nu, lo, hi) + qmax(tau * M, -nu, lo, hi)


def main():
    lam, M, n = 1.0, 1.0, 1
    tau = 1.0 / (3 * n + 1)
    ok = True
    print(f"n = 1, lam = {lam}, M = {M}, I = [-1, 1]; cells by R3 adapted to "
          f"tau' = 1/(3n+1), tolerance eps/(2n)")
    for eps in [1e-2, 1e-3, 1e-4, 1e-5]:
        cells = partition(lam, M, eps, n)
        lens = [hi - lo for lo, hi in cells]
        near0 = [hi - lo for lo, hi in cells if lo <= 0 <= hi]
        g0 = gap(cells, [0.0] * len(cells), lam, M)
        g1 = gap(cells, [lam] * len(cells), lam, M)
        nus = []
        for lo, hi in cells:
            a, b = 0.0, 10.0
            if bracket(b, lo, hi, M, tau) <= eps / (2 * n):
                nus.append(b)
                continue
            for _ in range(200):
                mid = (a + b) / 2
                if bracket(mid, lo, hi, M, tau) <= eps / (2 * n):
                    a = mid
                else:
                    b = mid
            nus.append(a)
        g2 = gap(cells, [lam + v for v in nus], lam, M)
        ok = ok and g1 <= eps / 2 + 1e-12 and g2 <= eps / 2 + 1e-12
        print(f"eps = {eps:g}: {len(cells)} cells, lengths {min(lens):.3e}"
              f"..{max(lens):.3e}, cells at 0 of length {near0[0]:.3e}; "
              f"gap with slope 0 = {g0:.3e} ({g0 / eps:.1f} eps); "
              f"with balanced-minimizer slope lam = {g1:.3e}; "
              f"with perturbed slopes (bracket <= eps/2, "
              f"max nu {max(nus):.3e}) = {g2:.3e} ({g2 / eps:.3f} eps)")
    print("slope-clause cases within eps/2:", ok)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
