"""Targeted exact checks for the fixed-integer quartic oracle proof.

This checks finite instances and several exact identities. It does not
verify the general complexity theorem, the flatness theorem, or PosSLP.
Run from the repository root with Python and SymPy available.
"""

from fractions import Fraction as Q
from itertools import combinations, product

import sympy as sp


def psd_by_principal_minors(matrix):
    """Exact PSD test; used only for the small matrices below."""
    for size in range(1, matrix.rows + 1):
        for indices in combinations(range(matrix.rows), size):
            assert matrix.extract(indices, indices).det() >= 0


def check_projected_gradient_cuts():
    # A genuinely coupled quadratic fiber, hence a degree <=4 input.
    b = sp.Matrix([[1, 2, -1, 1], [0, 1, 2, -2], [2, 0, 1, 1]])
    hessian = sp.eye(4) + b.T * b
    linear = sp.Matrix([sp.Rational(1, 3), -2, sp.Rational(2, 5), 1])
    az = hessian[:2, :2]
    cross = hessian[:2, 2:]
    cy = hessian[2:, 2:]
    projected_hessian = az - cross * cy.inv() * cross.T
    projected_linear = linear[:2, :] - cross * cy.inv() * linear[2:, :]
    projected_constant = -(linear[2:, :].T * cy.inv() * linear[2:, :])[0] / 2
    psd_by_principal_minors(projected_hessian - sp.eye(2))
    error = sp.Matrix([sp.Rational(1, 8), -sp.Rational(1, 8)])
    assert (error.T * error)[0] <= sp.Rational(1, 16)

    def value(z):
        return (z.T * projected_hessian * z)[0] / 2 + (projected_linear.T * z)[0] + projected_constant

    points = [sp.Matrix(z) for z in product(range(-2, 3), repeat=2)]
    checks = 0
    improving = 0
    for z in points:
        y = -cy.inv() * (cross.T * z + linear[2:, :])
        x = z.col_join(y)
        assert value(z) == (x.T * hessian * x)[0] / 2 + (linear.T * x)[0]
        gradient = projected_hessian * z + projected_linear
        assert gradient == (hessian * x + linear)[:2, :]
        q = gradient + error
        for w in points:
            if w == z:
                continue
            displacement = w - z
            square_distance = (displacement.T * displacement)[0]
            dot = (q.T * displacement)[0]
            assert value(w) - value(z) >= dot + square_distance / 4
            if value(w) <= value(z):
                assert dot <= -sp.Rational(1, 4)
                improving += 1
            checks += 1
    # The integer-only cut is deliberately not real-sublevel separation.
    a = sp.Rational(1, 10)
    q = sp.Rational(1, 10)
    gradient_at_zero = -a
    assert abs(q - gradient_at_zero) <= sp.Rational(1, 4)
    assert (a - a) ** 2 / 2 < a**2 / 2
    assert q * a > 0  # The better continuous point is excluded by q*x<=0.
    return checks, improving


def check_affine_curvature():
    # Integer substitutions do not preserve the original modulus.
    t = sp.Matrix([[7, 1], [8, 1], [0, 0]])
    gram = t.T * t
    lower = gram.det() / sp.trace(gram)
    assert lower == sp.Rational(1, 115)
    psd_by_principal_minors(gram - lower * sp.eye(2))
    assert (gram - sp.eye(2)).det() < 0
    left_inverse = gram.inv() * t.T
    assert left_inverse * t == sp.eye(2)
    offset = sp.Matrix([11, -5, 3])
    for u in [sp.Matrix(v) for v in product(range(-3, 4), repeat=2)]:
        z = offset + t * u
        assert left_inverse * (z - offset) == u
    augmented = sp.diag(gram, sp.ones(1))
    psd_by_principal_minors(augmented - lower * sp.eye(3))


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def polygon_area(vertices):
    return abs(sum(vertices[i][0] * vertices[(i + 1) % len(vertices)][1]
                   - vertices[(i + 1) % len(vertices)][0] * vertices[i][1]
                   for i in range(len(vertices)))) / 2


def clip(vertices, normal, center):
    """Exact clipping by normal dot (x-center) <= 0."""
    result = []
    bound = dot(normal, center)
    for a, b in zip(vertices, vertices[1:] + vertices[:1]):
        va, vb = dot(normal, a) - bound, dot(normal, b) - bound
        if va <= 0:
            result.append(a)
        if (va < 0 < vb) or (vb < 0 < va):
            fraction = va / (va - vb)
            result.append(tuple(x + fraction * (y - x) for x, y in zip(a, b)))
    return result


def check_geometry():
    triangle = [(Q(0), Q(0)), (Q(4), Q(0)), (Q(0), Q(4))]
    center = (Q(1), Q(1))
    # MILP inset inequalities are x1>=4lambda, x2>=4lambda,
    # x1+x2+4lambda<=4. At this integer point lambda=1/4.
    assert min(center[0] / 4, center[1] / 4, (4 - sum(center)) / 4) == Q(1, 4)
    total = polygon_area(triangle)
    guaranteed_fraction = Q(1, 32)  # d=2, Lambda=1/8.
    normals = [(Q(a, 7), Q(b, 11)) for a, b in product(range(-3, 4), repeat=2) if (a, b) != (0, 0)]
    for normal in normals:
        retained = polygon_area(clip(triangle, normal, center))
        assert guaranteed_fraction * total <= retained <= (1 - guaranteed_fraction) * total

    # Exact minimum-width MILP objective identity for rational vertices.
    vertices = [(Q(0), Q(0)), (Q(2), Q(0)), (Q(0), Q(3))]
    widths = []
    for v in product(range(-3, 4), repeat=2):
        if v == (0, 0):
            continue
        values = [dot(v, p) for p in vertices]
        pair_objective = max(dot(v, tuple(x - y for x, y in zip(a, b))) for a in vertices for b in vertices)
        assert pair_objective == max(values) - min(values)
        widths.append(pair_objective)
    assert min(widths) == 2

    # Counterexample to the printed symmetrized-facet formula.
    v = (1, 1, -1)
    assert all(abs(x) <= 1 for x in v) and abs(sum(v)) <= 1
    assert sum(max(x, 0) for x in v) > 1  # impossible for a-b in the unit simplex.
    # Inclusive slice endpoints: the singleton level zero must not disappear.
    lower, upper = 0, 0
    assert list(range(lower, upper + 1)) == [0]
    return len(normals)


if __name__ == "__main__":
    pairs, improving = check_projected_gradient_cuts()
    check_affine_curvature()
    directions = check_geometry()
    print(f"PASS: {pairs} exact coupled-fiber integer cuts ({improving} no-worse pairs).")
    print("PASS: real-sublevel counterexample and nonisometric lattice curvature bound.")
    print(f"PASS: {directions} exact central cuts, width objective, and inclusive slice endpoints.")
