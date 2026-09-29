"""Exact finite checks for affine-recourse conditional-mean repair.

Run: python research-20260928/solver/check_affine_recourse_upper.py
This fixture is not a proof of the general rounding theorem.
"""

from itertools import combinations

import sympy as sp


u, v, y1, y2 = sp.symbols("u v y1 y2", real=True)
z = [sp.Integer(1), y1, y2]
private_matrix = sp.Matrix([
    [1, sp.Rational(1, 2), sp.Rational(1, 2)],
    [sp.Rational(1, 2), 1, 0],
    [sp.Rational(1, 2), 0, 1],
])


def assert_psd(matrix):
    for size in range(1, matrix.rows + 1):
        for indices in combinations(range(matrix.rows), size):
            assert matrix.extract(indices, indices).det() >= 0


def moment(polynomial):
    """Source u=0; private first/second moments need not represent a law."""
    result = 0
    entries = {
        (0, 0): (0, 0), (1, 0): (0, 1), (0, 1): (0, 2),
        (2, 0): (1, 1), (1, 1): (1, 2), (0, 2): (2, 2),
    }
    for (shared, a, b), coefficient in sp.Poly(polynomial, u, y1, y2).terms():
        assert shared <= 4 and a + b <= 2
        if shared == 0:
            row, col = entries[a, b]
            result += coefficient * private_matrix[row, col]
    return sp.expand(result)


def localizer(basis, weight):
    return sp.Matrix([[moment(weight * a * b) for b in basis] for a in basis])


def arcsine_integral(polynomial):
    result = 0
    for (degree,), coefficient in sp.Poly(polynomial, v).terms():
        if degree % 2 == 0:
            result += coefficient * sp.binomial(degree, degree // 2) / 2**degree
    return sp.simplify(result)


# The fiber P(u) = {y in [-1,1]^2 : y1+y2=1+u} is nonempty for all
# u in [-1,1]. It is represented by the two affine rows below.
recourse = [1 + u - y1 - y2, -1 - u + y1 + y2]
assert_psd(private_matrix)
for generators in [0, 1]:
    weight = (1 - u**2)**generators
    basis = [u**i for i in range(2 - generators + 1)]
    joint_basis = [a * private for a in basis for private in z]
    # All moment rows containing a positive source power are zero.
    expected = sp.zeros(len(joint_basis))
    expected[:3, :3] = private_matrix
    assert localizer(joint_basis, weight) == expected
    for private in [y1, y2]:
        assert localizer(basis, weight * (1 - private**2)) == sp.zeros(len(basis))
    recourse_basis = [u**i for i in range(2 - generators)]
    for constraint in recourse:
        assert localizer(recourse_basis, weight * constraint) == sp.zeros(len(recourse_basis))
assert moment(1) == 1
assert moment((y1 + y2 - 1 - u)**2) == 1

# r=2,s=1 gives m=2. Its exact positive kernel is polynomial.
kernel = 1 + sp.Rational(4, 3)*u*v + sp.Rational(1, 3)*(2*u**2 - 1)*(2*v**2 - 1)
h = moment(kernel)
assert h == sp.Rational(4, 3) - sp.Rational(2, 3)*v**2
assert arcsine_integral(h) == 1
source_mean = sp.simplify(moment(kernel*u) / h)
private_mean = sp.Matrix([sp.simplify(moment(kernel*y) / h) for y in [y1, y2]])
assert source_mean == 0
assert private_mean == sp.Matrix([sp.Rational(1, 2), sp.Rational(1, 2)])
assert sp.expand(sum(private_mean) - 1 - source_mean) == 0
assert sp.expand(sum(private_mean) - 1 - v) == -v

# Projection to the new fiber stays within the private box for |v|<=1.
repaired = sp.Matrix([(1 + v)/2, (1 + v)/2])
assert sp.expand(sum(repaired) - 1 - v) == 0
movement = sp.simplify((repaired - private_mean).dot(repaired - private_mean))
assert movement == v**2/2
transport = moment(kernel*(u - v)**2)
assert sp.expand(transport - h*v**2) == 0
assert arcsine_integral(transport) == sp.Rational(5, 12)
assert arcsine_integral(transport) == sp.Rational(3*(4*2 - 3), 2*2*(2*2**2 + 1))

# A shared-dependent, private-linear objective has a positive repair cost.
# The matrix surrogate integrates to the original moment objective zero.
objective = u*(y1 + y2)
surrogate = sp.expand(v*moment(kernel*(y1 + y2)))
repaired_cost = sp.expand(v*sum(repaired))
assert moment(objective) == 0
assert arcsine_integral(surrogate) == 0
assert sp.expand(h*repaired_cost - surrogate) == sp.expand(h*v**2)
assert arcsine_integral(h*repaired_cost) == sp.Rational(5, 12)

# N=m+1=3 is essential for the degree-four displacement polynomial.
for nodes, exact in [([sp.sqrt(2)/2, -sp.sqrt(2)/2], False),
                     ([sp.sqrt(3)/2, sp.Integer(0), -sp.sqrt(3)/2], True)]:
    quadrature = sp.simplify(sum(transport.subs(v, point) for point in nodes) / len(nodes))
    assert (quadrature == arcsine_integral(transport)) is exact

# A genuine zero-density endpoint, with an exactly feasible source atom.
zero_density = sp.expand(kernel.subs(u, 1))
assert zero_density.subs(v, -1) == 0
full_vector = sp.Matrix([1, 1, 1, 1])  # (1,u,y1,y2), source u=1,y=(1,1)
conditional_matrix = zero_density*(full_vector*full_vector.T)
assert conditional_matrix.subs(v, -1) == sp.zeros(4)

print("PASS: every rectangular constraint at r=2 for the affine-recourse fixture (exact)")
print("PASS: nonrepresentable private moments and source/output feasibility distinction (exact)")
print("PASS: projection, sharp transport constant, and positive repair cost (exact)")
print("PASS: insufficient N=2 and sufficient N=3 quadrature, plus zero-density matrix (exact)")
