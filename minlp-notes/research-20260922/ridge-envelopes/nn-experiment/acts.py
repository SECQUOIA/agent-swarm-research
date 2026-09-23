"""Activations: value, derivative, interval range and certified derivative bounds.

M2 is an upper bound on |sigma''| over R (analytic, times 1.0001) and L1 an upper
bound on |sigma'| over R; both are used only to make cuts provably valid.
"""
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "code"))  # verified code (used by tests)
from scipy.special import expit as sigmoid  # noqa: E402  (same function as code/activations.py, faster)
from scipy.special import erf  # noqa: E402  (double-precision erf; math.erf in the verified code is slower)

SQ2 = math.sqrt(2.0)
INV_SQ2PI = 1.0 / math.sqrt(2.0 * math.pi)


def _silu(z):
    z = np.asarray(z, float)
    return z * sigmoid(z)


def _dsilu(z):
    s = sigmoid(z)
    return s + z * s * (1 - s)


def _gelu(z):
    z = np.asarray(z, float)
    return 0.5 * z * (1.0 + erf(z / SQ2))


def _dgelu(z):
    z = np.asarray(z, float)
    return 0.5 * (1.0 + erf(z / SQ2)) + z * INV_SQ2PI * np.exp(-0.5 * z * z)


def _bisect_root(g, lo, hi, it=200):
    for _ in range(it):
        mid = 0.5 * (lo + hi)
        if g(mid) > 0:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


class Act:
    def __init__(self, name, f, df, M2, L1, zmin=None, tail=None):
        self.name, self.f, self.df, self.M2, self.L1, self.zmin = name, f, df, M2 * 1.0001, L1 * 1.0001, zmin
        self.tail = tail  # decreasing majorant g(r) of |sigma''(s)| for |s| >= r

    def M2_on(self, a, b):
        """Upper bound of |sigma''| on each interval [a, b] (vectorized)."""
        a, b = np.asarray(a, float), np.asarray(b, float)
        if self.name == "sin":  # |sin''| = |sin|
            lo, hi = self.range(a, b)
            return np.minimum(np.maximum(np.abs(lo), np.abs(hi)) * 1.0001, self.M2)
        r = np.where((a <= 0) & (b >= 0), 0.0, np.minimum(np.abs(a), np.abs(b)))
        return np.minimum(self.M2, self.tail(r) * 1.0001)

    def range(self, L, U):
        """Interval [min, max] of sigma over [L, U] (vectorized), rounded outward by 1e-12."""
        L, U = np.asarray(L, float), np.asarray(U, float)
        fL, fU = self.f(L), self.f(U)
        lo, hi = np.minimum(fL, fU), np.maximum(fL, fU)
        if self.name == "sin":
            # max 1 at pi/2 + 2k pi, min -1 at -pi/2 + 2k pi
            kmax = np.ceil((L - math.pi / 2) / (2 * math.pi))
            hi = np.where(math.pi / 2 + 2 * math.pi * kmax <= U, 1.0, hi)
            kmin = np.ceil((L + math.pi / 2) / (2 * math.pi))
            lo = np.where(-math.pi / 2 + 2 * math.pi * kmin <= U, -1.0, lo)
        elif self.zmin is not None:
            fm = float(self.f(np.array([self.zmin]))[0])
            lo = np.where((L <= self.zmin) & (self.zmin <= U), fm, lo)
        return lo - 1e-12, hi + 1e-12


_zsilu = _bisect_root(lambda z: float(_dsilu(np.array([z]))[0]), -3.0, 0.0)
_zgelu = _bisect_root(lambda z: float(_dgelu(np.array([z]))[0]), -3.0, 0.0)

ACTS = {
    # |tanh''| = 2|t|(1-t^2) <= 4/(3 sqrt 3)
    # tails: |tanh''| <= 2 sech^2 <= 8 e^{-2|s|}; |sigmoid''| <= s(1-s) <= e^{-|s|};
    # |silu''| <= s'(z)(2+|z|) <= (2+|z|) e^{-|z|}; |gelu''| <= phi(z)(2+z^2), all decreasing in |z|
    "tanh": Act("tanh", np.tanh, lambda z: 1.0 - np.tanh(z) ** 2, 4 / (3 * math.sqrt(3)), 1.0,
                tail=lambda r: 8.0 * np.exp(-2.0 * r)),
    # |s''| = s(1-s)|1-2s| <= sqrt(3)/18
    "sigmoid": Act("sigmoid", sigmoid, lambda z: sigmoid(z) * (1 - sigmoid(z)), math.sqrt(3) / 18, 0.25,
                   tail=lambda r: np.exp(-r)),
    # silu'' = s'(z) (2 - z tanh(z/2)); |.| <= 1/4 * 2 = 0.5 (the negative lobe is < 0.04); max silu' = 1.0998
    "silu": Act("silu", _silu, _dsilu, 0.5, 1.0999, zmin=_zsilu, tail=lambda r: (2.0 + r) * np.exp(-r)),
    # gelu'' = phi(z)(2 - z^2); |.| <= 2 phi(0); max gelu' = 1.1289 at sqrt 2
    "gelu": Act("gelu", _gelu, _dgelu, 2 * INV_SQ2PI, 1.129, zmin=_zgelu,
                tail=lambda r: (2.0 + r * r) * INV_SQ2PI * np.exp(-0.5 * r * r)),
    "sin": Act("sin", np.sin, np.cos, 1.0, 1.0),
}

if __name__ == "__main__":
    _sg = sigmoid
    D2 = {  # analytic second derivatives, for the check below
        "tanh": lambda z: -2 * np.tanh(z) * (1 - np.tanh(z) ** 2),
        "sigmoid": lambda z: _sg(z) * (1 - _sg(z)) * (1 - 2 * _sg(z)),
        "silu": lambda z: _sg(z) * (1 - _sg(z)) * (2 + z * (1 - 2 * _sg(z))),
        "gelu": lambda z: INV_SQ2PI * np.exp(-0.5 * z * z) * (2 - z * z),
        "sin": lambda z: -np.sin(z),
    }
    # sanity check of the analytic constants on a dense grid
    z = np.linspace(-40, 40, 800001)
    h = z[1] - z[0]
    for k, a in ACTS.items():
        f = a.f(z)
        d1 = np.gradient(f, h)
        d2 = np.gradient(d1, h)
        print(k, "max|f'|=%.6f (L1 %.6f)  max|f''|=%.6f (M2 %.6f)" % (np.abs(d1).max(), a.L1, np.abs(d2[5:-5]).max(), a.M2),
              "zmin", a.zmin)
        L = np.random.default_rng(0).uniform(-6, 6, 2000)
        U = L + np.random.default_rng(1).uniform(0, 8, 2000)
        lo, hi = a.range(L, U)
        for i in range(0, 2000, 97):
            s = np.linspace(L[i], U[i], 20001)
            v = a.f(s)
            assert lo[i] <= v.min() + 1e-9 and hi[i] >= v.max() - 1e-9, (k, L[i], U[i])
            assert v.min() - lo[i] < 1e-6 and hi[i] - v.max() < 1e-6
        # local curvature bounds on random intervals
        for i in range(0, 2000, 7):
            s = np.linspace(L[i], U[i], 4001)
            assert np.abs(D2[k](s)).max() <= a.M2_on(L[i], U[i]), (k, L[i], U[i])
    print("range and local curvature checks ok")
