"""Targeted exact checks for the independent partial-kernel proof review.

Run with: python research-20260928/solver/check_partial_kernel_review.py
These are finite algebraic checks, not a proof of the general theorem.
"""

from itertools import combinations

import sympy as sp


u, v, y1, y2 = sp.symbols("u v y1 y2", real=True)
z = sp.Matrix([1, y1, y2])


def atom_matrix(x):
    """First moments obey y1+y2=1; second moments need not obey it."""
    t = (1 + x) / 2
    return sp.Matrix([[1, t, 1 - t], [t, 1, 0], [1 - t, 0, 1]])


atoms = [sp.Integer(-1), sp.Integer(0), sp.Integer(1)]


def moment(polynomial):
    result = 0
    for (shared, a, b), coefficient in sp.Poly(polynomial, u, y1, y2).terms():
        assert a + b <= 2
        row, col = {
            (0, 0): (0, 0),
            (1, 0): (0, 1),
            (0, 1): (0, 2),
            (2, 0): (1, 1),
            (1, 1): (1, 2),
            (0, 2): (2, 2),
        }[a, b]
        result += coefficient * sum(x**shared * atom_matrix(x)[row, col] for x in atoms) / 3
    return sp.expand(result)


def assert_psd(matrix):
    """All principal minors characterize PSD for this exact rational matrix."""
    for size in range(1, matrix.rows + 1):
        for indices in combinations(range(matrix.rows), size):
            assert matrix.extract(indices, indices).det() >= 0


def localizer(basis, weight):
    return sp.Matrix([[moment(weight * a * b) for b in basis] for a in basis])


def arcsine_integral(polynomial):
    result = 0
    for (degree,), coefficient in sp.Poly(polynomial, v).terms():
        if degree % 2 == 0:
            result += coefficient * sp.binomial(degree, degree // 2) / 2**degree
    return sp.simplify(result)


# Every constraint at shared order r=1, k=1, p=2 is covered below.
# P is the segment {y1+y2=1} intersected with [-1,1]^2.
private_constraints = [1 - y1, 1 + y1, 1 - y2, 1 + y2,
                       1 - y1 - y2, -1 + y1 + y2]
for shared_basis, box_weight in [([1, u], 1), ([1], 1 - u**2)]:
    affine_basis = [q * a for q in shared_basis for a in z]
    assert_psd(localizer(affine_basis, box_weight))
    for constraint in private_constraints + [1 - y1**2, 1 - y2**2]:
        assert_psd(localizer(shared_basis, box_weight * constraint))
assert moment(1) == 1
assert moment((y1 + y2 - 1)**2) == 1  # No representing measure on P.

# Explicit squared-Fejer kernel for m=2.
kernel = 1 + sp.Rational(4, 3) * u * v + sp.Rational(1, 3) * (2*u*u - 1) * (2*v*v - 1)
M = sp.Matrix([[moment(kernel * a * b) for b in z] for a in z])
h = M[0, 0]
ell = M[1:, 0]
Y = M[1:, 1:]
assert sp.expand(h - (2*v*v + 8)/9) == 0
assert sp.expand(ell[0] - (v + 2)**2/9) == 0
assert sp.expand(ell[1] - (v - 2)**2/9) == 0
assert sp.expand(sum(ell) - h) == 0
assert sp.simplify(Y - h * sp.eye(2)) == sp.zeros(2)
assert arcsine_integral(h) == 1

# A nonconstant convex private quadratic, including mixed linear terms.
f = (1 + u)*y1**2 + (1 - u)*y2**2 + u*(y1 - 2*y2) + u/3
Q = sp.diag(1 + v, 1 - v)
a = sp.Matrix([v, -2*v])
surrogate = sp.expand(v*h/3 + (a.T * ell)[0] + sp.trace(Q*Y))
rounded = (v/3 + (a.T * ell)[0]/h + (ell.T*Q*ell)[0]/h**2)
gap_times_h = sp.factor(h * (surrogate - h * rounded))
assert sp.expand(gap_times_h - 2*(48 - 24*v**2 - 5*v**4)/81) == 0
# The gap polynomial is positive on [-1,1], since 48-24-5 > 0.
assert 48 - 24 - 5 > 0
assert moment(f) == 3
assert arcsine_integral(surrogate) == sp.Rational(8, 3)
assert abs(arcsine_integral(surrogate) - moment(f)) <= sp.Rational(16, 9)

# N=2 Gauss-Chebyshev quadrature exactly integrates both polynomials.
nodes = [sp.sqrt(2)/2, -sp.sqrt(2)/2]
for polynomial in [h, surrogate]:
    quadrature = sum(polynomial.subs(v, point) for point in nodes) / 2
    assert sp.simplify(quadrature - arcsine_integral(polynomial)) == 0

# A genuine zero-density case: one input atom at u=1.
zero_case = sp.expand(kernel.subs(u, 1)) * atom_matrix(sp.Integer(1))
assert zero_case.subs(v, -1) == sp.zeros(3)
assert sp.factor(kernel.subs(u, 1)) == sp.Rational(2, 3) * (v + 1)**2

# Discrete checks of the two integer degree budgets, including empty bags.
degree_cases = 0
for r in range(1, 13):
    for s in range(1, r + 1):
        m = r // s + 1
        for k in range(s + 1):
            for generators in range(k + 1):
                assert k*(m - 1) - generators <= r - generators
                degree_cases += 1
        for degree in range(r + 1):
            N = m + degree // 2
            assert 2*(m - 1) + degree <= 2*N - 1

# Exact coefficient eliminations used in the all-order Motzkin obstruction.
x1, x2, x3 = sp.symbols("x1 x2 x3")
aa, bb, cc, dd, ee, ff, gg, hh = sp.symbols("aa bb cc dd ee ff gg hh")
cubic = (aa*x1**2*x2 + bb*x1*x2**2 + cc*x1**2*x3 + dd*x2**2*x3
         + ee*x1*x3**2 + ff*x2*x3**2 + gg*x1*x2*x3 + hh*x3**3)
cubic_square = sp.Poly(cubic**2, x1, x2, x3)
assert cubic_square.coeff_monomial(x1**4*x3**2) == cc**2
assert cubic_square.coeff_monomial(x2**4*x3**2) == dd**2
assert cubic_square.coeff_monomial(x1**2*x3**4) == ee**2 + 2*cc*hh
assert cubic_square.coeff_monomial(x2**2*x3**4) == ff**2 + 2*dd*hh
assert cubic_square.coeff_monomial(x1**2*x2**2*x3**2) == gg**2 + 2*aa*ff + 2*bb*ee + 2*cc*dd

# Nonconvexity breaks the hierarchy's constant-shared-coefficient conclusion.
triangle_M = sp.Matrix([[1, sp.Rational(1, 2), sp.Rational(1, 2)],
                        [sp.Rational(1, 2), 1, 1],
                        [sp.Rational(1, 2), 1, 1]])
assert_psd(triangle_M)
assert 1 - triangle_M[0, 1] - triangle_M[0, 2] == 0
assert triangle_M[0, 1] >= 0 and triangle_M[0, 2] >= 0
assert triangle_M[1, 1] == triangle_M[2, 2] == 1
assert -sum(triangle_M[i, j] for i in [1, 2] for j in [1, 2]) == -4

print("PASS: all order-one rectangular localizers and normalization (exact)")
print("PASS: nonrepresenting private moments, conditional equality, and convex gap (exact)")
print("PASS: objective damping, grid quadrature, and zero-density case (exact)")
print(f"PASS: {degree_cases} integer kernel-certificate degree cases")
print("PASS: Motzkin non-SOS coefficient eliminations and nonconvex triangle example (exact)")
