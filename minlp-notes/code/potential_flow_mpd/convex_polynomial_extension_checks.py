"""Exact diagnostics for the cube perspective Lipschitz extension."""
from fractions import Fraction as F
from random import Random
import sympy as sp


def run():
    rng = Random(293510)
    total = 0
    for dimension in range(1, 5):
        symbols = sp.symbols('z:'+str(dimension))
        for case in range(5):
            expression = sp.Integer(-17)
            if case == 0:
                # Convex on the cube, but not globally convex.
                expression += sum(6*z*z-z**4 for z in symbols)
            else:
                for _ in range(3):
                    affine = rng.randrange(-2, 3)+sum(rng.randrange(-2, 3)*z for z in symbols)
                    expression += rng.randrange(1, 4)*affine**(2+2*(case % 4))
            expression += sum(rng.randrange(-4, 5)*z for z in symbols)
            terms = [(powers, F(int(coefficient))) for powers, coefficient in sp.Poly(expression, *symbols).terms()]
            v = sum(abs(c) for _, c in terms)
            g = max(F(1), max(sum(abs(c)*power[i] for power, c in terms) for i in range(dimension)))
            m = 1+v+dimension*g
            bound = g+1+2*(v+dimension*g)

            def value(z):
                return sum(c*sp_product(x**p for x, p in zip(z, powers)) for powers, c in terms)

            def extension(z):
                t = max(F(1), max(map(abs, z)))
                return t*value([x/t for x in z])+m*(t-1)

            for _ in range(80):
                x = [F(rng.randrange(-40, 41), rng.randrange(1, 6)) for _ in symbols]
                y = [F(rng.randrange(-40, 41), rng.randrange(1, 6)) for _ in symbols]
                theta = F(rng.randrange(0, 9), 8)
                z = [theta*a+(1-theta)*b for a, b in zip(x, y)]
                assert extension(z) <= theta*extension(x)+(1-theta)*extension(y)
                assert abs(extension(x)-extension(y)) <= bound*sum(abs(a-b) for a, b in zip(x, y))
                inside = [F(rng.randrange(-8, 9), 8) for _ in symbols]
                assert extension(inside) == value(inside)
                total += 1
    print(f'PASS: {total} exact Jensen, global-Lipschitz, and cube-agreement checks; '
          '20 polynomials including cube-only convex examples')


def sp_product(values):
    result = F(1)
    for value in values:
        result *= value
    return result


if __name__ == '__main__':
    run()
