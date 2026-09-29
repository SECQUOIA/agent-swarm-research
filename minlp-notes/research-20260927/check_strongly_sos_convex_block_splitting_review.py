"""Independent exact checks for the affine-coordinate convexification lemma.

These finite checks support the displayed identities. They do not establish
the general degree, positivity, or encoding bounds, which are reviewed in
strongly-sos-convex-block-splitting-review.md.
"""

import sympy as sp


def tensor(x, y):
    return sp.Matrix([xi * yj for xi in x for yj in y])


def extension_gram(r, s, epsilon):
    u = sp.Matrix(sp.symbols(f"u0:{r}"))
    v = sp.Matrix(sp.symbols(f"v0:{s}"))
    a = sp.Matrix(sp.symbols(f"a0:{r}"))
    b = sp.Matrix(sp.symbols(f"b0:{s}"))
    er = sp.Matrix([int(i == j) for i in range(r) for j in range(r)])
    es = sp.Matrix([int(i == j) for i in range(s) for j in range(s)])
    old = sp.diag(2 * sp.eye(r), 4 * sp.eye(r * r) + 8 * er * er.T)
    new = sp.diag(
        2 * epsilon * sp.eye(s),
        2 * epsilon * sp.eye(r * s),
        2 * epsilon * sp.eye(s * r),
        4 * epsilon * sp.eye(s * s) + 8 * epsilon * es * es.T,
    )
    cross = sp.zeros(old.rows, new.rows)
    start = s + 2 * r * s
    cross[r:, start:] = 4 * epsilon * er * es.T
    gram = old.row_join(cross).col_join(cross.T.row_join(new))
    basis = a.col_join(tensor(u, a)).col_join(b)
    basis = basis.col_join(tensor(u, b)).col_join(tensor(v, a))
    basis = basis.col_join(tensor(v, b))
    polynomial = (u.dot(u) + u.dot(u) ** 2
                  + epsilon * v.dot(v) * (1 + u.dot(u) + v.dot(v)))
    return u, v, a, b, old, gram, basis, polynomial


def quadratic_form(matrix, vector):
    return sum(matrix[i, j] * vector[i] * vector[j]
               for i, j in matrix.todok())


for r, s in [(1, 1), (2, 3), (4, 5)]:
    epsilon = sp.Symbol("epsilon", positive=True)
    u, v, a, b, old, gram, basis, polynomial = extension_gram(r, s, epsilon)
    variables = list(u) + list(v)
    directions = a.col_join(b)
    differentiated = quadratic_form(sp.hessian(polynomial, variables), directions)
    assert sp.expand(differentiated - quadratic_form(gram, basis)) == 0
    assert len(basis) == (r + s) + (r + s) ** 2

    if (r, s) == (2, 3):
        rho = old.det() / sp.trace(old) ** (old.rows - 1)
        chosen = min(sp.Integer(1), rho / (16 * r * s))
        concrete = gram.subs(epsilon, chosen)
        lower, diagonal = concrete.LDLdecomposition(hermitian=False)
        assert all(diagonal[i, i] > 0 for i in range(diagonal.rows))
        assert lower * diagonal * lower.T == concrete

print("PASS: independently differentiated Gram identities in dimensions 2, 5, 9")
print("PASS: exact positive LDL pivots with the prescribed epsilon in dimension 5")

w = sp.Matrix(sp.symbols("y1 y2 y3 z11 z12 z13 z22 z23 z33"))
y1, y2, y3, z11, z12, z13, z22, z23, z33 = w
image = sp.Matrix([
    y1, y2, y3, z13,
    z11 - y2, z12 - y3, z22 - z13, z23 - 2, z33 - 2 * y1,
])
linear = image.jacobian(w)
translation = image.subs(dict.fromkeys(w, 0))
assert abs(linear.det()) == 1
assert linear.inv() * (image - translation) == w

root = sp.Symbol("root")
w0 = [root, root ** 2, root ** 3, root ** 2, root ** 3,
      root ** 4, root ** 4, 2, 2 * root]
target = sp.Matrix([root, root ** 2, root ** 3, root ** 4, 0, 0, 0, 0, 0])
assert image.subs(dict(zip(w, w0))) == target
for i, j, coordinate in [(0, 0, 3), (0, 1, 4), (0, 2, 5),
                         (1, 1, 6), (1, 2, 7), (2, 2, 8)]:
    assert sp.rem(w0[i] * w0[j] - w0[coordinate], root ** 5 - 2, root) == 0

# Check the Hessian chain rule through the actual nonzero affine translation.
u, v, a, b, old, gram, basis, polynomial = extension_gram(4, 5, sp.Rational(1, 1000))
source = list(u) + list(v)
substitution = dict(zip(source, image))
composed = polynomial.subs(substitution, simultaneous=True)
expected = linear.T * sp.hessian(polynomial, source).subs(substitution) * linear
actual = sp.hessian(composed, list(w))
assert all(sp.expand(entry) == 0 for entry in actual - expected)
print("PASS: affine inverse, quintic lifted point, and translated Hessian congruence")
