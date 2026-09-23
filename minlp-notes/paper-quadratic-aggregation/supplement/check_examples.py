"""Exact checks for the quadratic aggregation paper (Python >= 3.10).

Run: python3 supplement/check_examples.py
Only the standard library is needed. Polynomial identities are checked by
equality of rational coefficients, not by sampling. The finite matrix and
point checks supplement, rather than prove, the manuscript's universal claims.
"""

from fractions import Fraction as F


class Polynomial:
    """Sparse rational polynomials in x, y, a for the displayed identities."""

    def __init__(self, terms):
        self.terms = {e: F(c) for e, c in terms.items() if c}

    @staticmethod
    def constant(c):
        return Polynomial({(0, 0, 0): F(c)})

    def __add__(self, other):
        if not isinstance(other, Polynomial):
            other = self.constant(other)
        terms = dict(self.terms)
        for e, c in other.terms.items():
            terms[e] = terms.get(e, F(0)) + c
        return Polynomial(terms)

    __radd__ = __add__

    def __neg__(self):
        return Polynomial({e: -c for e, c in self.terms.items()})

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return -self + other

    def __mul__(self, other):
        if not isinstance(other, Polynomial):
            other = self.constant(other)
        terms = {}
        for e, c in self.terms.items():
            for f, d in other.terms.items():
                exponent = tuple(ej + fj for ej, fj in zip(e, f))
                terms[exponent] = terms.get(exponent, F(0)) + c * d
        return Polynomial(terms)

    __rmul__ = __mul__

    def __pow__(self, power):
        assert isinstance(power, int) and power >= 0
        result = self.constant(1)
        for _ in range(power):
            result = result * self
        return result

    def __eq__(self, other):
        if not isinstance(other, Polynomial):
            other = self.constant(other)
        return self.terms == other.terms

    def at(self, x=0, y=0, a=0):
        values = (F(x), F(y), F(a))
        return sum(c * values[0] ** e[0] * values[1] ** e[1]
                   * values[2] ** e[2] for e, c in self.terms.items())


x = Polynomial({(1, 0, 0): 1})
y = Polynomial({(0, 1, 0): 1})
a = Polynomial({(0, 0, 1): 1})


def check_polynomial_identities():
    assert (x*x + y*y)**2 == (x*x - y*y)**2 + 4*x*x*y*y
    # The closed-system negative determinant, symbolically in two parameters.
    assert x*(-x) - (F(1, 2)*y)**2 == -x*x - F(1, 4)*y*y

    f1 = x*x + 2*x*y - F(3, 50)
    f2 = 2*y*y - x*y - F(9, 100)
    ell1 = F(4, 5)*x + F(2, 5)*y - F(9, 50)
    ell2 = -x + F(3, 5)*y + F(3, 100)
    assert f1 - ell1 == (x-F(1, 5))**2 + 2*(x-F(1, 5))*(y-F(1, 5))
    assert f2 - ell2 == 2*(y-F(1, 5))**2 + (1-y)*(x-F(1, 5))
    G = 2*f1 + f2
    assert G == 2*x*x + 3*x*y + 2*y*y - F(21, 100)
    assert G == F(1, 2)*x*x + F(1, 2)*y*y + F(3, 2)*(x+y)**2 - F(21, 100)
    assert 2*ell1 + ell2 == F(3, 5)*x + F(7, 5)*y - F(33, 100)
    assert G.at(F(1, 5), F(1, 5)) == F(7, 100)
    tangent = F(7, 100) + F(7, 5)*(x+y-F(2, 5))
    assert tangent == F(7, 5)*(x+y-F(7, 20))
    assert G - tangent == 2*(x-F(1, 5))**2 + 3*(x-F(1, 5))*(y-F(1, 5)) + 2*(y-F(1, 5))**2

    L = a*ell1 + (1-a)*ell2
    ax, ay, d = F(9, 5)*a-1, F(3, 5)-F(1, 5)*a, F(3, 100)-F(21, 100)*a
    assert L == ax*x + ay*y + d
    low = F(1, 20)*(31*a-17)
    high = F(1, 100)*(11*a-5)
    assert ax + F(1, 5)*ay + d == low
    assert F(1, 5)*ax + F(1, 5)*ay + d == high
    assert low.at(a=F(5, 9)) == high.at(a=F(5, 9))
    assert high.at(a=F(5, 7)) == F(1, 35)
    assert high.at(a=F(2, 3)) == F(7, 300)
    assert F(31, 20) > 0 and F(11, 100) > 0
    # Linear DD constraints: solve the four nonnegative-slack inequalities.
    off = F(1, 2)*(3*a-1)
    assert a-off == F(1, 2)*(1-a)
    assert a+off == F(1, 2)*(5*a-1)
    assert 2*(1-a)-off == F(1, 2)*(5-7*a)
    assert 2*(1-a)+off == F(1, 2)*(3-a)
    assert F(1, 5) < F(5, 9) < F(5, 7)
    for point in [(0, 0), (F(1, 5), 0), (0, F(1, 5))]:
        assert f1.at(*point) <= 0 and f2.at(*point) <= 0
    assert ell1.at(F(1, 5), F(1, 5)) == F(3, 50)


def check_lifted_witnesses():
    px = py = F(1, 5)
    sx = sy = F(1, 25)
    w = F(0)
    assert px*px <= sx <= px and py*py <= sy <= py
    assert max(F(0), px+py-1) <= w <= min(px, py)
    assert sx+2*w <= F(3, 50) and 2*sy-w <= F(9, 100)
    assert px+py > F(7, 20)
    assert F(2)*2-F(3, 2)**2 == F(7, 4)
    # Strip counterexample: X=diag(7/2,0,0), x=0.
    assert F(7, 2)-4 == -F(1, 2)
    assert -F(7, 2)+3 == -F(1, 2)
    # Two nonclosed-projection examples. Each rational covariance has
    # positive upper-left entry, nonnegative lower-right, determinant zero.
    for compact in (False, True):
        cross = -F(3, 4) if compact else -F(1, 2)
        for px in (F(1, 4), F(1, 2), F(3, 4)):
            for py in (F(-100), F(0), F(100)):
                X11 = (px*px+px)/2
                Y11, Y12 = X11-px*px, cross-px*py
                Y22 = Y12*Y12/Y11
                assert Y11 > 0 and Y22 >= 0 and Y11*Y22-Y12*Y12 == 0
                assert 2*cross+1 <= 0 and X11-px <= 0
                if compact:
                    assert -2*cross-2 <= 0 and F(1, 4)-px <= 0
    px, py = F(1, 2), -F(3, 2)
    assert all(v < 0 for v in (2*px*py+1, px*px-px, -2*px*py-2, F(1, 4)-px))


def check_geometric_witness_algebra():
    # HHC failures: a midpoint (1,0,0) violates the binary square-cone identity.
    assert 1**2 != 0**2 + 0**2
    # Stable-convexity obstruction: u=0 and norm squared=1 force both
    # squares to 1/2, inconsistent with product zero.
    assert F(1, 2)*F(1, 2) != 0
    # Closed example: the symmetric feasible points span the plane.
    assert F(1)*2 - F(1)*F(1, 2) == F(3, 2)
    for px, py in ((F(1), F(1)), (F(1, 2), F(2)), (F(-1), F(-1)), (F(-1, 2), F(-2))):
        assert px*py == 1 and px*px <= py*py and abs(px) <= 1
    # The three-constraint linear bound's contradiction has a strict gap.
    assert 9 > 4+F(1, 9)


if __name__ == "__main__":
    check_polynomial_identities()
    check_lifted_witnesses()
    check_geometric_witness_algebra()
    print("Exact coefficient identities, rational lifts, margins, and example witnesses: PASS")
