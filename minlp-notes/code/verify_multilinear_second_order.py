"""Numerical checks for the harmonic fixed-point certificate.

These checks supplement the analytic proof; they do not certify its accuracy.
"""

import math

from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.special import lambertw


def scaled_integral(alpha, ell):
    """Return L J_L(alpha/L), with ell=log(L), in log coordinates."""
    lower = math.log(alpha) - ell

    def integrand(s):
        exponent = math.expm1(-s) * math.exp(-ell)
        return math.exp(ell + s) * -math.expm1(-exponent)

    return quad(integrand, lower, 0.0, epsabs=1e-10, epsrel=1e-11)[0]


def check(ell):
    upper = min(math.exp(ell), ell + 2)
    alpha = brentq(
        lambda a: scaled_integral(a, ell) - a,
        1e-8,
        upper,
        xtol=1e-11,
    )
    w = float(lambertw(math.exp(ell - 1)).real)
    if w >= 1:
        certificate = w - 0.5 / w
        assert alpha >= certificate - 1e-9
    if ell >= 4:
        assert alpha >= ell - math.log(ell) - 2 - 1e-9
    residual = alpha - (ell - math.log(ell) - 1) if ell else float("nan")
    print(f"{ell:8.2f} {alpha:14.8f} {w:14.8f} {residual:14.8f}")


if __name__ == "__main__":
    print("log(L)   alpha=L*z       W(L/e)        second-order residual")
    for log_l in [0, 1, 2, 4, 6, 10, 20, 50, 100, 200, 500]:
        check(log_l)
