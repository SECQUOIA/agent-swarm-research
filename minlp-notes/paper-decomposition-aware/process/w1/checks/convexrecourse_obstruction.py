"""Exact checks for the recourse-curvature obstruction and the instability
example.

Family (M >= 1):  F_M(x,y) = M(x-y)^2 - (x+y-2)^2/8 + 2(y-1),
                  x in [0,2], y in [1,3].
Claims:
  * unique minimizer (1,1), F*=0, growth F >= (|x-1|^2+|y-1|^2)/8;
  * Hessian eigenvalues 4M and -1/2, so nu = 1/2 and nu/g <= 4;
  * the only private sets with PSD private Hessian are {}, {x}, {y};
  * eliminating x (retain y): the value has a piece [y_c,3] with
    y_c = 4M/(2M+1/4) on which the response is x=2 and the curvature is
    2M-1/4; eliminating y (retain x): a piece [0,x_c],
    x_c = (2M+9/4)/(2M+1/4), with response y=1 and curvature 2M-1/4;
  * reduced growth constants are at most 3/2 (one retained coordinate)
    or 3/4 (both retained), so every choice has L/g >= (4M-1/2)/3.
Instability: f = M(y-u)^2 + eps*y, y,u in [0,1]: the value function has
curvature 2M on [0, eps/(2M)] for every eps>0.
"""
import random
from fractions import Fraction as Fr
import sympy as sp

random.seed(7)
counts = {}


def bump(k, n=1):
    counts[k] = counts.get(k, 0) + n


def F(M, x, y):
    return M * (x - y) ** 2 - (x + y - 2) ** 2 / 8 + 2 * (y - 1)


def clip(a, lo, hi):
    return lo if a < lo else hi if a > hi else a


# symbolic: the PSD quadratic lower bound used in the growth proof
a, b, Ms = sp.symbols("a b M")
lower = (a - b) ** 2 - (a + b) ** 2 / 8 + b ** 2 - sp.Rational(1, 8) * (a ** 2 + b ** 2)
Q = sp.Matrix([[sp.Rational(3, 4), -sp.Rational(9, 8)], [-sp.Rational(9, 8), sp.Rational(7, 4)]])
assert sp.expand(lower - (Q[0, 0] * a ** 2 + 2 * Q[0, 1] * a * b + Q[1, 1] * b ** 2)) == 0
assert Q[0, 0] > 0 and Q.det() == sp.Rational(3, 64)
bump("symbolic PSD lower bound")

# Hessian eigenvalues
H = sp.Matrix([[2 * Ms - sp.Rational(1, 4), -2 * Ms - sp.Rational(1, 4)],
               [-2 * Ms - sp.Rational(1, 4), 2 * Ms - sp.Rational(1, 4)]])
ev = H.eigenvals()
assert set(sp.simplify(e) for e in ev) == {4 * Ms, -sp.Rational(1, 2)}
bump("symbolic eigenvalues")

for M in [Fr(1), Fr(2), Fr(17, 3), Fr(100), Fr(10 ** 6)]:
    assert F(M, Fr(1), Fr(1)) == 0
    # growth at random rational points
    for _ in range(2000):
        x = Fr(random.randint(0, 2000), 1000)
        y = Fr(random.randint(1000, 3000), 1000)
        if random.random() < 0.5:
            x = 1 + Fr(random.randint(-50, 50), 1000)
            y = 1 + Fr(random.randint(0, 50), 1000)
        assert F(M, x, y) >= ((x - 1) ** 2 + (y - 1) ** 2) / 8
        bump("growth 1/8 checks")
    # private Hessian of {x,y} is not PSD (det < 0)
    det = (2 * M - Fr(1, 4)) ** 2 - (2 * M + Fr(1, 4)) ** 2
    assert det == -2 * M and det < 0

    # eliminate x, retain y
    def phi_y(y):
        xhat = ((2 * M + Fr(1, 4)) * y - Fr(1, 2)) / (2 * M - Fr(1, 4))
        x = clip(xhat, Fr(0), Fr(2))
        return F(M, x, y), x

    yc = 4 * M / (2 * M + Fr(1, 4))
    assert 1 < yc < 2
    for k in range(0, 201):
        y = 1 + Fr(2 * k, 200)
        val, x = phi_y(y)
        # brute-force check of the 1-D convex minimization on a fine grid
        best = min(F(M, Fr(i, 400), y) for i in range(0, 801))
        assert val <= best
        if y >= yc:
            assert x == 2
        bump("phi_y evaluations")
    for (lo, hi) in [(yc, Fr(3))]:
        mid, hs = (lo + hi) / 2, (hi - lo) / 4
        d2 = (phi_y(mid + hs)[0] - 2 * phi_y(mid)[0] + phi_y(mid - hs)[0]) / hs ** 2
        assert d2 == 2 * M - Fr(1, 4)
        bump("stiff piece curvature (retain y)")
    mid, hs = (1 + yc) / 2, (yc - 1) / 4
    d2 = (phi_y(mid + hs)[0] - 2 * phi_y(mid)[0] + phi_y(mid - hs)[0]) / hs ** 2
    assert d2 == -2 * M / (2 * M - Fr(1, 4))
    bump("Schur piece curvature (retain y)")
    assert phi_y(Fr(2))[0] <= Fr(3, 2) and phi_y(Fr(1))[0] == 0

    # eliminate y, retain x
    def phi_x(x):
        yhat = ((2 * M + Fr(1, 4)) * x - Fr(5, 2)) / (2 * M - Fr(1, 4))
        y = clip(yhat, Fr(1), Fr(3))
        return F(M, x, y), y

    xc = (2 * M + Fr(9, 4)) / (2 * M + Fr(1, 4))
    assert 1 < xc <= 2
    for k in range(0, 201):
        x = Fr(2 * k, 200)
        val, y = phi_x(x)
        best = min(F(M, x, 1 + Fr(i, 400)) for i in range(0, 801))
        assert val <= best
        if x <= xc:
            assert y == 1
            assert val == (M - Fr(1, 8)) * (x - 1) ** 2
        bump("phi_x evaluations")
    assert phi_x(Fr(2))[0] <= Fr(3, 2) and phi_x(Fr(1))[0] == 0
    mid, hs = (xc + 2) / 2, (2 - xc) / 4
    d2 = (phi_x(mid + hs)[0] - 2 * phi_x(mid)[0] + phi_x(mid - hs)[0]) / hs ** 2
    assert d2 == -2 * M / (2 * M - Fr(1, 4))
    bump("concave interior piece (retain x)")
    # stiff piece for retain y lies at value >= 3/2 - 1/M
    for k in range(0, 101):
        y = yc + (3 - yc) * Fr(k, 100)
        assert phi_y(y)[0] >= Fr(3, 2) - 1 / M
        bump("stiff piece value gap (retain y)")
    bump("reduced growth upper bounds", 2)
    assert (2 * M - Fr(1, 4)) / Fr(3, 2) >= M
    assert F(M, Fr(2), Fr(2)) == Fr(3, 2)

# instability example
for M in [Fr(1), Fr(50), Fr(10 ** 4)]:
    for eps in [Fr(1), Fr(1, 10), Fr(1, 10 ** 6)]:
        def phi(u):
            y = clip(u - eps / (2 * M), Fr(0), Fr(1))
            return M * (y - u) ** 2 + eps * y
        w = eps / (2 * M)
        for k in range(1, 10):
            u = w * k / 10
            hs = w / 40
            d2 = (phi(u + hs) - 2 * phi(u) + phi(u - hs)) / hs ** 2 if u - hs >= 0 else None
            if d2 is not None:
                assert d2 == 2 * M
                bump("instability stiff-piece curvature")
        if w < Fr(1, 2):
            u = (w + 1) / 2
            hs = (1 - w) / 8
            d2 = (phi(u + hs) - 2 * phi(u) + phi(u - hs)) / hs ** 2
            assert d2 == 0
            bump("instability flat-piece curvature")

for k_, v_ in counts.items():
    print(f"{k_}: {v_}")
print("all obstruction checks passed")
