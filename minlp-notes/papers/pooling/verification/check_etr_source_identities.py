"""Exact checks of the two algebraic diagrams used by the singleton route.

Requires SymPy. Equations were transcribed from the original PDF of
Abrahamsen--Miltzow, arXiv:1912.08674v1, Figures 2 and 3, pp.16,18.
This checks source identities and interval bounds, not pooling feasibility.
"""
import sympy as sp

x, y = sp.symbols("x y")
half, three_quarters = sp.Rational(1, 2), sp.Rational(3, 4)


def check_box(values, variables, radius):
    """Enclose each rational function on the entire rational input box."""
    for value in values:
        numerator, denominator = sp.fraction(sp.cancel(value))

        def enclosure(poly):
            poly = sp.Poly(poly, *variables)
            center = poly.coeff_monomial((0,) * len(variables))
            error = sum(
                abs(coefficient) * radius ** sum(powers)
                for powers, coefficient in poly.terms()
                if any(powers)
            )
            return center - error, center + error

        plo, phi = enclosure(numerator)
        qlo, qhi = enclosure(denominator)
        if qhi < 0:
            plo, phi, qlo, qhi = -phi, -plo, -qhi, -qlo
        assert plo > 0 and qlo > 0, value
        assert plo / qhi >= half, value
        assert phi / qlo <= 2, value


# Figure 2: additions, halvings and squares replace multiplication.
ax, ay = x + 1, y + 1
bx, by = ax + half, ay + half
cx, cy = bx / 2, by / 2
summed = cx + cy
average = summed - half
average_squared = average**2
raised = average_squared + half
square_x, square_y = ax**2, ay**2
raised_x, raised_y = square_x + half, square_y + half
halved_x, halved_y = raised_x / 2, raised_y / 2
sum_squares = halved_x + halved_y
quarter_squares = sum_squares / 2
difference = raised - quarter_squares
doubled = 2 * difference
product = doubled - half
assert sp.expand(product - ax * ay) == 0
check_box(
    [ax, ay, bx, by, cx, cy, summed, average, average_squared,
     raised, square_x, square_y, raised_x, raised_y, halved_x,
     halved_y, sum_squares, quarter_squares, difference, doubled, product],
    (x, y), sp.Rational(1, 10**6),
)

# Figure 3: additions and inversions replace the square of x+1.
g0 = x + 1
g1 = g0 + half
g2 = 1 / g1
g3 = 1 / g0
g4 = g3 + half
g5 = g4 - sp.Rational(2, 3)
g6 = g5 + half
g7 = g6 - g2
g8 = 2 * g7
g9 = g8 - sp.Rational(2, 3)
g10 = 1 / g9
g11 = g10 - half
g12 = g11 + three_quarters
g13 = g1 / 2
g14 = g12 - g13
assert sp.cancel(g7 - (2*x*x + 5*x + 6)/(6*x*x + 15*x + 9)) == 0
assert sp.cancel(g9 - 2/(2*x*x + 5*x + 3)) == 0
assert sp.cancel(sp.together(g14 - (x + 1)**2)) == 0
check_box(
    [g0, g1, g2, g3, g4, g5, g6, g7, g8, g9, g10, g11, g12, g13, g14],
    (x,), sp.Rational(1, 10**6),
)
print("PASS: both source diagram identities, nonzero denominators, and exact full-box range bounds")
