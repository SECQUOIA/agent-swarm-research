"""Second recheck: independent values of the Example 4.3(a) integrals.

m = x(1-x) + y^4 + z^4 + w^4 on [0,0.9] x [-0.4,0.5]^3.
I_full(eps) = int (m + eps)^(-2),  I_face(eps) = int_{[-0.4,0.5]^3} (S + eps)^(-3/2),
S = y^4 + z^4 + w^4.

Route B (no Laplace transform, no Dawson function, no incomplete gamma):
  the x-integral in closed form,
    F(c) = int_0^0.9 (x(1-x) + c)^(-2) dx
         = 0.2/(A^2 (0.09+c)) + 0.25/(A^2 c) + [ln((A+0.4)/(A-0.4)) + ln((A+0.5)^2/c)]/(4 A^3),
    A = sqrt(1/4 + c),
  then a tensor-product composite Gauss-Legendre rule over (y, z, w), with
  y folded to [0, 0.5] (weight 2 on [0, 0.4], 1 on [0.4, 0.5]) and panels
  geometric in eps^(1/4).  Convergence is checked by changing the order and
  the panel refinement.
Route A (Laplace transform, written independently in mpmath):
  I_full = int_0^inf s e^(-s eps) H(s) G(s)^3 ds with
  H(s) = sqrt(pi)/(2 sqrt s) e^(-s/4) [erfi(sqrt(s)/2) + erfi(0.4 sqrt s)]  (erfi, not Dawson)
  G(s) = s^(-1/4)/4 [gamma_lower(1/4, 0.0256 s) + gamma_lower(1/4, 0.0625 s)].
Usage: OMP_NUM_THREADS=1 python3 face4d_integrals2.py > logs/face4d_integrals2.log
"""
import math
import sys

import mpmath as mp
import numpy as np
from scipy.integrate import quad


def F(c):
    A2 = 0.25 + c
    A = np.sqrt(A2)
    return (0.2 / (A2 * (0.09 + c)) + 0.25 / (A2 * c)
            + (np.log((A + 0.4) / (A - 0.4)) + np.log((A + 0.5) ** 2 / c)) / (4 * A2 * A))


def nodes_1d(eps, order, refine):
    """composite Gauss-Legendre nodes and weights for int_{-0.4}^{0.5} phi(y^4) dy, folded"""
    r = eps ** 0.25
    pts = [0.0]
    x = r / 8
    while x < 0.4:
        pts.append(x)
        x *= 2 ** (1.0 / refine)
    pts += [0.4, 0.5]
    g, gw = np.polynomial.legendre.leggauss(order)
    ys, ws = [], []
    for a, b in zip(pts[:-1], pts[1:]):
        ys.append((a + b) / 2 + (b - a) / 2 * g)
        ws.append((b - a) / 2 * gw * (2.0 if b <= 0.4 + 1e-15 else 1.0))
    return np.concatenate(ys), np.concatenate(ws)


def cube_sum(fun, eps, order, refine):
    y, w = nodes_1d(eps, order, refine)
    u = y ** 4
    U2 = u[:, None] + u[None, :]
    W2 = w[:, None] * w[None, :]
    tot = 0.0
    for ui, wi in zip(u, w):
        tot += wi * np.sum(W2 * fun(U2 + ui + eps))
    return tot


def route_b(eps, order=16, refine=1):
    full = cube_sum(F, eps, order, refine)
    face = cube_sum(lambda c: c ** -1.5, eps, order, refine)
    return full, face


mp.mp.dps = 25


def H_mp(s):
    r = mp.sqrt(s)
    return mp.sqrt(mp.pi) / (2 * r) * mp.exp(-s / 4) * (mp.erfi(r / 2) + mp.erfi(mp.mpf('0.4') * r))


def G_mp(s):
    q = mp.mpf(1) / 4
    return s ** (-q) / 4 * (mp.gammainc(q, 0, mp.mpf('0.0256') * s) + mp.gammainc(q, 0, mp.mpf('0.0625') * s))


def route_a(eps):
    eps = mp.mpf(eps)
    f = lambda u: mp.exp(2 * u - mp.exp(u) * eps) * H_mp(mp.exp(u)) * G_mp(mp.exp(u)) ** 3
    lo, hi = mp.log(mp.mpf('1e-6')), mp.log(80 / eps)
    grid = mp.linspace(lo, hi, 60)
    return mp.quad(f, grid)  # Gamma(2) = 1


def main():
    print("Check of F(c) against quad:")
    for c in (1e-2, 1e-6, 1e-10):
        pts = [0.0] + [c * 4.0 ** k for k in range(0, 40) if c * 4.0 ** k < 0.9] + [0.9]
        ref = sum(quad(lambda x: (x * (1 - x) + c) ** -2, a, b, limit=200, epsabs=0, epsrel=1e-13)[0]
                  for a, b in zip(pts[:-1], pts[1:]))
        print(f"  c = {c:.0e}: closed form {F(c):.12g}, quad {ref:.12g}, rel diff {F(c) / ref - 1:.1e}")
    sys.stdout.flush()

    lead_full = 8 * math.gamma(1.25) ** 3 * math.gamma(0.25)
    lead_face = 8 * math.gamma(1.25) ** 3 * math.gamma(0.75) / math.gamma(1.5)
    print(f"\nleading constants: full {lead_full:.6f} eps^(-1/4), face {lead_face:.6f} eps^(-3/4)")

    print("\nRoute B (closed-form x integral, tensor Gauss-Legendre over the cube)")
    print(f"{'eps':>9} {'I_full o16 r1':>15} {'I_full o24 r2':>15} {'rel diff':>9} {'o6 r1 diff':>10} "
          f"{'I_face o24 r2':>15} {'full ratio':>10} {'face ratio':>10}")
    vals = {}
    for k in range(4, 21):
        e = 10.0 ** (-k / 2)
        f1, _ = route_b(e, 16, 1)
        f2, g2 = route_b(e, 24, 2)
        f0, _ = route_b(e, 6, 1)
        vals[k] = (e, f2, g2)
        print(f"{e:9.2e} {f1:15.9g} {f2:15.9g} {f2 / f1 - 1:9.1e} {f0 / f2 - 1:10.1e} {g2:15.9g} "
              f"{f2 * e ** 0.25 / lead_full:10.5f} {g2 * e ** 0.75 / lead_face:10.6f}")
        sys.stdout.flush()
    print("\nSecant slopes -dlog I/dlog eps over the half decade ending at eps:")
    for k in range(5, 21):
        e0, a0, b0 = vals[k - 1]
        e1, a1, b1 = vals[k]
        print(f"  eps = {e1:8.2e}: full {math.log(a1 / a0) / math.log(e0 / e1):.4f}, "
              f"face {math.log(b1 / b0) / math.log(e0 / e1):.4f}")
    print("Derivative slopes (central difference in log eps, step 0.01 decade):")
    for e in (1e-6, 1e-8, 1e-10):
        h = 10 ** 0.005
        ap, bp = route_b(e / h, 24, 2)
        am, bm = route_b(e * h, 24, 2)
        print(f"  eps = {e:.0e}: full {math.log(ap / am) / math.log(h * h):.4f}, "
              f"face {math.log(bp / bm) / math.log(h * h):.4f}")
    sys.stdout.flush()

    print("\nRoute A (Laplace transform in mpmath, erfi form of H)")
    for e in (1e-4, 1e-6, 1e-8):
        a = route_a(e)
        b = vals[{1e-4: 8, 1e-6: 12, 1e-8: 16}[e]][1]
        print(f"  eps = {e:.0e}: I_full = {mp.nstr(a, 12)}; route B {b:.9g}; rel diff {float(a) / b - 1:.1e}")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
