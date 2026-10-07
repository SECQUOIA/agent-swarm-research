"""Checks for the revision after review (items F1-F4 of reviews/rlct-review.md).

F1  sharp optimal vertex: the level bound 1 + log2(s0 (alpha' + M/2)/g) of
    Lemma 3.3a for m = x + y - 0.4(x^2+y^2) on [0,1]^2 (g = 1, M = 0.8).
F2  m = (x+y)^2 + (x-y)^4 on [0,1]^2: V(t)/t -> 1/2, so the box RLCT is
    (1, 1) although the Newton distance in the coordinates u = x+y, v = x-y
    gives 1/l = 3/4; the edge integral grows like (1/2) log(1/eps).
F3  m = x(1-x) + y^4 + z^4 + w^4 on [0,0.9] x [-0.4,0.5]^3: the face x = 0
    integral grows like eps^(-3/4), the full 4D integral like eps^(-1/4).
    Both are computed as one-dimensional Laplace-transform integrals:
      integral (h + eps)^(-a) = Gamma(a)^(-1) int_0^inf s^(a-1) e^(-s eps) Z(s) ds.
F4  m = xy + x^3 + y^3 on [0,a]^2: the edge y = 0 carries m = x^3, whose
    integral is ~ c eps^(-1/6), which dominates the face's log^2.
Usage: python3 revision_checks.py > logs/revision_checks.log
"""
import math

from scipy.integrate import quad
from scipy.special import dawsn, gamma, gammainc

Q = dict(limit=400, epsabs=0.0, epsrel=1e-10)


def G4(s, b):
    """int_0^b exp(-s y^4) dy"""
    if s == 0:
        return b
    return 0.25 * s ** -0.25 * gamma(0.25) * gammainc(0.25, s * b ** 4)


def Gq(s):
    return G4(s, 0.4) + G4(s, 0.5)


def H(s):
    """int_0^0.9 exp(-s x(1-x)) dx in closed form (Dawson function D):
    x(1-x) = 1/4 - (x-1/2)^2 gives s^(-1/2) [D(sqrt(s)/2) + e^(-0.09 s) D(0.4 sqrt(s))].
    (The first version used one quad call with a single breakpoint at 1/s and
    lost the part beyond it for s >= 1e6; see Section 11 of the note.)"""
    if s < 1e-12:
        return 0.9
    r = math.sqrt(s)
    return (dawsn(r / 2) + math.exp(-0.09 * s) * dawsn(0.4 * r)) / r


def H_split(s):
    """the same integral by quadrature on a geometric grid 1/s, 4/s, ... (independent check)"""
    pts, x = [0.0], 1.0 / max(s, 1e-12)
    while x < 0.9:
        pts.append(x)
        x *= 4
    pts.append(0.9)
    return sum(quad(lambda t: math.exp(-s * t * (1 - t)), pts[i], pts[i + 1], **Q)[0]
               for i in range(len(pts) - 1))


def I_full_xouter(e):
    """third route: integrate over x outside, the cube inside by its Laplace transform"""
    K = lambda a: laplace_integral(2.0, lambda s: Gq(s) ** 3, a)
    pts, x = [0.0], e
    while x < 0.9:
        pts.append(x)
        x *= 10
    pts.append(0.9)
    return sum(quad(lambda x: K(x * (1 - x) + e), pts[i], pts[i + 1], limit=200, epsrel=1e-9)[0]
               for i in range(len(pts) - 1))


def laplace_integral(a, Z, e):
    """int (h + e)^(-a) from the Laplace transform Z of the sublevel measure"""
    f = lambda u: math.exp(a * u - math.exp(u) * e) * Z(math.exp(u))
    lo, hi = math.log(1e-8), math.log(60 / e)
    grid = [lo + (hi - lo) * i / 40 for i in range(41)]
    return sum(quad(f, grid[i], grid[i + 1], **Q)[0] for i in range(40)) / gamma(a)


def main():
    print("F1: sharp optimal vertex, m = x + y - 0.4(x^2+y^2) on [0,1]^2, g = 1, M = 0.8")
    for ap in (1.0, 8.0):
        print(f"  alpha' = {ap}: corner cell non-pruned only at levels with s_j > g/(alpha'+M/2) = "
              f"{1 / (ap + 0.4):.4f}; at most {1 + math.log2(1.0 * (ap + 0.4) / 1.0):.2f} levels j >= 1")

    print("\nF2: m = (x+y)^2 + (x-y)^4 on [0,1]^2")
    for t in [1e-2, 1e-4, 1e-6, 1e-8]:
        st = math.sqrt(t)
        # u = x + y in [0, sqrt t], |v| <= min(u, (t-u^2)^(1/4)), area element du dv / 2
        V = quad(lambda u: min(u, max(t - u * u, 0.0) ** 0.25), 0, st, **Q)[0]
        print(f"  t = {t:.0e}: V(t)/t = {V / t:.5f}")
    for e in [1e-4, 1e-8, 1e-12]:
        Ie = quad(lambda x: (x * x + x ** 4 + e) ** -0.5, 0, 1, points=[math.sqrt(e)], **Q)[0]
        print(f"  eps = {e:.0e}: edge integral = {Ie:.4f}, (1/2)log(1/eps) = {0.5 * math.log(1 / e):.4f}")

    print("\nF3: m = x(1-x) + y^4 + z^4 + w^4 on [0,0.9] x [-0.4,0.5]^3, alpha = 1.05")
    alpha = 1.05
    print(f"{'eps':>9} {'I_face':>13} {'face LB':>11} {'slope':>7} {'I_full':>11} {'slope':>7} "
          f"{'I_full (H by split quad)':>24}")
    prev = None
    for k in range(2, 21):
        e = 10.0 ** (-k / 2)
        If = laplace_integral(1.5, lambda s: Gq(s) ** 3, e)
        Ifull = laplace_integral(2.0, lambda s: H(s) * Gq(s) ** 3, e)
        Ifull2 = laplace_integral(2.0, lambda s: H_split(s) * Gq(s) ** 3, e)
        lb = (alpha * 3 / math.pi ** 2) ** 1.5 * If
        sl = ("", "") if prev is None else (
            f"{math.log(If / prev[1]) / math.log(prev[0] / e):7.4f}",
            f"{math.log(Ifull / prev[2]) / math.log(prev[0] / e):7.4f}")
        print(f"{e:9.1e} {If:13.6g} {lb:11.5g} {sl[0]:>7} {Ifull:11.6g} {sl[1]:>7} {Ifull2:24.6g}")
        prev = (e, If, Ifull)
    print("  predicted slopes: face 3/2 - 3/4 = 0.75; full 2 - 7/4 = 0.25")
    lead_face = 8 * gamma(1.25) ** 3 * gamma(0.75) / gamma(1.5)
    lead_full = 8 * gamma(1.25) ** 3 * gamma(0.25)
    print(f"  leading constants (Lemma 2.2(i), c_Z = (2 Gamma(5/4))^3 for the face and "
          f"(2 Gamma(5/4))^3 for the full integral after H(s) ~ 1/s):")
    for e in (1e-6, 1e-8, 1e-10):
        If = laplace_integral(1.5, lambda s: Gq(s) ** 3, e)
        Ifull = laplace_integral(2.0, lambda s: H(s) * Gq(s) ** 3, e)
        print(f"  eps = {e:.0e}: I_face eps^(3/4) / {lead_face:.6f} = {If * e ** 0.75 / lead_face:.5f}; "
              f"I_full eps^(1/4) / {lead_full:.4f} = {Ifull * e ** 0.25 / lead_full:.5f}")
    e = 1e-8
    print(f"  third route (x outside, cube by Laplace transform) at eps = 1e-8: I_full = {I_full_xouter(e):.6g}")

    print("\nF4: edge of xy + x^3 + y^3: int_0^1 (x^3 + eps)^(-1/2) dx * eps^(1/6)")
    c = quad(lambda u: (u ** 3 + 1) ** -0.5, 0, math.inf)[0]
    for e in [1e-4, 1e-8, 1e-12]:
        Ie = quad(lambda x: (x ** 3 + e) ** -0.5, 0, 1, points=[e ** (1 / 3)], **Q)[0]
        print(f"  eps = {e:.0e}: {Ie * e ** (1 / 6):.5f}  (limit int_0^inf (u^3+1)^(-1/2) du = {c:.5f})")


if __name__ == "__main__":
    main()
