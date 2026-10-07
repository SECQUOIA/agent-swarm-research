#!/usr/bin/env python3
"""Exact finite diagnostics for global affine-selector recognition.

Requires SymPy for exact linear algebra. Each central QP optimizer is supplied and independently
KKT-checked; this script does not implement an exact convex-QP solver. The
recognizer partitions by the central gradient and uses one LP with
absolute-value auxiliaries. A separate exhaustive active-pattern check
uses parameter-box vertices, solely as a small-instance diagnostic. Linear
feasibility uses a tiny exact Fourier--Motzkin routine. Neither this routine
nor the exhaustive check is claimed to run in polynomial time.
"""

from dataclasses import dataclass
from itertools import product
import json

from sympy import Eq, Matrix, Rational as Q, S, linear_eq_to_matrix, linsolve, symbols


COUNTS = {
    "exact_linear_feasibility_calls": 0,
    "constant_inconsistent_systems": 0,
    "exhaustive_active_patterns": 0,
    "pointwise_kkt_checks": 0,
}


@dataclass
class Case:
    name: str
    C: Matrix
    D: Matrix
    c: Matrix
    yhat: Matrix
    zbox: tuple
    ybox: tuple
    expected: bool
    fixed: tuple

    @property
    def r(self):
        return self.C.rows

    @property
    def k(self):
        return self.D.cols

    @property
    def z0(self):
        return Matrix([(lo + hi) / 2 for lo, hi in self.zbox])

    @property
    def radii(self):
        return [(hi - lo) / 2 for lo, hi in self.zbox]

    @property
    def h0(self):
        return self.D * self.z0 + self.c


def case(name, C, D, c, yhat, zbox, ybox, expected, fixed):
    return Case(name, Matrix(C), Matrix(D), Matrix(c), Matrix(yhat),
                tuple(tuple(map(Q, pair)) for pair in zbox),
                tuple(tuple(map(Q, pair)) for pair in ybox), expected,
                tuple(fixed))


def is_psd(matrix):
    """Exact Schur-complement test, including singular PSD matrices."""
    if matrix != matrix.T:
        return False
    while matrix.rows:
        if any(matrix[i, i] < 0 for i in range(matrix.rows)):
            return False
        pivot = next((i for i in range(matrix.rows) if matrix[i, i] > 0), None)
        if pivot is None:
            return matrix.is_zero_matrix
        others = [i for i in range(matrix.rows) if i != pivot]
        matrix = Matrix(len(others), len(others), lambda i, j:
                        matrix[others[i], others[j]]
                        - matrix[others[i], pivot] * matrix[pivot, others[j]]
                        / matrix[pivot, pivot])
    return True


def fourier_motzkin(rows, dimension):
    """Find a rational point in A x <= b; exhaustive small-instance method."""
    normalized = {}
    for coefficients, rhs in rows:
        scale = next((abs(value) for value in coefficients if value != 0), None)
        if scale is None:
            if rhs < 0:
                return None
            continue
        coefficients = tuple(value / scale for value in coefficients)
        rhs /= scale
        normalized[coefficients] = min(rhs, normalized.get(coefficients, rhs))
    rows = list(normalized.items())
    if not rows:
        return [S.Zero] * dimension
    if all(rhs >= 0 for _, rhs in rows):
        return [S.Zero] * dimension
    index = min(range(dimension), key=lambda j:
                sum(bool(a[j] > 0) for a, _ in rows)
                * sum(bool(a[j] < 0) for a, _ in rows))
    positive = [(a, b) for a, b in rows if a[index] > 0]
    negative = [(a, b) for a, b in rows if a[index] < 0]
    remaining = [j for j in range(dimension) if j != index]
    reduced = [(tuple(a[j] for j in remaining), b) for a, b in rows if a[index] == 0]
    for a, b in positive:
        for c, d in negative:
            reduced.append((tuple(a[j] / a[index] - c[j] / c[index] for j in remaining),
                            b / a[index] - d / c[index]))
    point = fourier_motzkin(reduced, dimension - 1)
    if point is None:
        return None
    bounds = lambda group: [(b - sum((a[j] * value for j, value in zip(remaining, point)),
                                     S.Zero)) / a[index] for a, b in group]
    lower = max(bounds(negative)) if negative else None
    upper = min(bounds(positive)) if positive else None
    value = max(S.Zero, lower) if lower is not None else S.Zero
    if upper is not None:
        value = min(value, upper)
    assert lower is None or value >= lower
    point.insert(index, value)
    assert all(sum((x * y for x, y in zip(a, point)), S.Zero) <= b for a, b in rows)
    return point


def solve(objective, constraints):
    """Exact feasibility, with every resulting input constraint rechecked."""
    assert objective == 0
    constraints = [item for item in constraints if item != S.true]
    if S.false in constraints:
        COUNTS["constant_inconsistent_systems"] += 1
        return None
    all_symbols = sorted(set().union(*(item.free_symbols for item in constraints)), key=str)
    equalities = [item.lhs - item.rhs for item in constraints if isinstance(item, Eq)]
    # SymPy's simplex backend returned invalid points on the singular fixture
    # in 1.14.0. Use exact algebra plus finite elimination instead.
    substitution = {}
    if equalities:
        solutions = linsolve(equalities, all_symbols)
        if solutions == S.EmptySet:
            COUNTS["constant_inconsistent_systems"] += 1
            return None
        substitution = dict(zip(all_symbols, next(iter(solutions))))
    reduced = [item.subs(substitution, simultaneous=True) for item in constraints]
    reduced = [item for item in reduced if item != S.true]
    if S.false in reduced:
        COUNTS["constant_inconsistent_systems"] += 1
        return None
    variables = sorted(set().union(*(item.free_symbols for item in reduced)), key=str)
    expressions = [item.lhs - item.rhs if item.rel_op == "<=" else item.rhs - item.lhs
                   for item in reduced]
    matrix, rhs = linear_eq_to_matrix(expressions, variables)
    COUNTS["exact_linear_feasibility_calls"] += 1
    point = fourier_motzkin([(tuple(matrix.row(i)), rhs[i]) for i in range(matrix.rows)],
                           len(variables))
    if point is None:
        return None
    solution = dict(zip(variables, point))
    for variable in all_symbols:
        solution.setdefault(variable, S.Zero)
    solution = {key: S(value) for key, value in solution.items()}
    solution.update({key: value.subs(solution, simultaneous=True)
                     for key, value in substitution.items()})
    assert all(value.is_Rational for value in solution.values())
    assert all(item.subs(solution) == S.true for item in constraints), \
        "exact LP returned a point that fails an input constraint"
    return S.Zero, solution


def kkt(item, y, z):
    gradient = item.C * y + item.D * z + item.c
    for i, (lo, hi) in enumerate(item.ybox):
        assert lo <= y[i] <= hi, (item.name, "primal bounds", i)
        if y[i] == lo:
            assert gradient[i] >= 0, (item.name, "lower-bound sign", i)
        elif y[i] == hi:
            assert gradient[i] <= 0, (item.name, "upper-bound sign", i)
        else:
            assert gradient[i] == 0, (item.name, "interior gradient", i)
    COUNTS["pointwise_kkt_checks"] += 1


def central_gradient_partition(item):
    assert item.C.shape == (item.r, item.r)
    assert item.D.shape == (item.r, item.k)
    assert item.c.shape == item.yhat.shape == (item.r, 1)
    assert len(item.zbox) == item.k and len(item.ybox) == item.r
    assert all(lo < hi for lo, hi in item.zbox + item.ybox), \
        "fixed coordinates must first be substituted"
    assert all(value.is_Rational for matrix in
               (item.C, item.D, item.c, item.yhat) for value in matrix)
    assert is_psd(item.C), "private Hessian is not PSD"
    kkt(item, item.yhat, item.z0)
    gradient = item.C * item.yhat + item.h0
    pattern = tuple("lower" if value > 0 else "upper" if value < 0 else "free"
                    for value in gradient)
    return pattern, gradient


def selector_lp(item, pattern, robust_mode):
    """Search a fixed global active pattern, using one of two robust forms."""
    a = Matrix(symbols(f"a0:{item.r}"))
    B = Matrix(item.r, item.k, symbols(f"b0:{item.r * item.k}"))
    gradient0 = item.C * a + item.h0
    gradientB = item.C * B + item.D
    constraints = []
    for i, label in enumerate(pattern):
        if label == "free":
            constraints.append(Eq(gradient0[i], 0))
            constraints += [Eq(gradientB[i, j], 0) for j in range(item.k)]
        else:
            bound = item.ybox[i][0 if label == "lower" else 1]
            constraints.append(Eq(a[i], bound))
            constraints += [Eq(B[i, j], 0) for j in range(item.k)]

    if robust_mode == "absolute_values":
        for i, (lo, hi) in enumerate(item.ybox):
            t = symbols(f"t{i}_0:{item.k}")
            constraints += [bound for j in range(item.k)
                            for bound in (t[j] >= B[i, j], t[j] >= -B[i, j])]
            radius = sum((item.radii[j] * t[j] for j in range(item.k)), S.Zero)
            constraints += [a[i] - radius >= lo, a[i] + radius <= hi]
            if pattern[i] != "free":
                u = symbols(f"u{i}_0:{item.k}")
                constraints += [bound for j in range(item.k) for bound in
                                (u[j] >= gradientB[i, j],
                                 u[j] >= -gradientB[i, j])]
                radius = sum((item.radii[j] * u[j] for j in range(item.k)), S.Zero)
                constraints.append(gradient0[i] - radius >= 0 if pattern[i] == "lower"
                                   else gradient0[i] + radius <= 0)
    elif robust_mode == "vertices":
        for vertex in product(*item.zbox):
            delta = Matrix(vertex) - item.z0
            y = a + B * delta
            gradient = gradient0 + gradientB * delta
            constraints += [bound for i, (lo, hi) in enumerate(item.ybox)
                            for bound in (y[i] >= lo, y[i] <= hi)]
            constraints += [gradient[i] >= 0 if label == "lower" else gradient[i] <= 0
                            for i, label in enumerate(pattern) if label != "free"]
    else:
        raise ValueError(robust_mode)
    result = solve(0, constraints)
    if result is None:
        return None
    solution = result[1]
    return (a.subs(solution), B.subs(solution))


def verify_selector(item, selector):
    """Check exact polynomial complementarity and pointwise KKT independently."""
    a, B = selector
    gradient0 = item.C * a + item.h0
    gradientB = item.C * B + item.D
    for i, (lo, hi) in enumerate(item.ybox):
        constant = all(B[i, j] == 0 for j in range(item.k))
        zero_gradient = gradient0[i] == 0 and all(
            gradientB[i, j] == 0 for j in range(item.k))
        assert zero_gradient or (constant and a[i] in (lo, hi))
    # Vertices suffice for all affine primal and dual inequalities. Interior
    # checks additionally exercise evaluation at nonboundary rational points.
    fractions = [Q(0), Q(1, 3), Q(1, 2), Q(2, 3), Q(1)]
    for weights in product(fractions, repeat=item.k):
        z = Matrix([lo + weight * (hi - lo)
                    for weight, (lo, hi) in zip(weights, item.zbox)])
        kkt(item, a + B * (z - item.z0), z)


def exhaustive_reference(item):
    for pattern in product(("free", "lower", "upper"), repeat=item.r):
        COUNTS["exhaustive_active_patterns"] += 1
        selector = selector_lp(item, pattern, "vertices")
        if selector is not None:
            verify_selector(item, selector)
            return True
    return False


def examples():
    unit = [(0, 1)]
    return [
        case("positive_definite_affine", [[2]], [[-2]], [0], [Q(1, 2)],
             unit, unit, True, ["free"]),
        case("positive_definite_clipped", [[2]], [[-4]], [1], [Q(1, 2)],
             unit, unit, False, ["free"]),
        case("singular_sum_bad_central_vertex", [[2, 2], [2, 2]], [[-2], [-2]],
             [0, 0], [0, 1], [(0, 2)], unit * 2, True, ["free", "free"]),
        case("all_flat_two_parameters", [[0, 0], [0, 0]], [[0, 0], [0, 0]],
             [0, 0], [0, 1], [(-2, 4), (3, 5)], unit * 2,
             True, ["free", "free"]),
        case("nonzero_central_linear_face", [[0, 0], [0, 0]], [[0], [0]],
             [1, 0], [0, 1], unit, unit * 2, True, ["lower", "free"]),
        case("lower_active_positive_gradient", [[2]], [[1]], [1], [0],
             unit, unit, True, ["lower"]),
        case("upper_active_negative_gradient", [[2]], [[-1]], [-3], [1],
             unit, unit, True, ["upper"]),
        case("lower_gradient_zero_at_parameter_endpoint", [[2]], [[1]], [0], [0],
             unit, unit, True, ["lower"]),
        case("flat_center_changing_linear_sign", [[0]], [[1]], [-Q(1, 2)], [0],
             unit, unit, False, ["free"]),
        case("lower_gradient_changes_sign", [[2]], [[4]], [-1], [0],
             unit, unit, False, ["lower"]),
        case("upper_gradient_changes_sign", [[2]], [[4]], [-5], [1],
             unit, unit, False, ["upper"]),
        case("two_parameter_affine", [[2]], [[-Q(1, 2), -Q(1, 2)]],
             [-Q(1, 2)], [Q(1, 2)], unit * 2, unit, True, ["free"]),
        case("mixed_free_and_active", [[4, 1], [1, 2]], [[-1], [0]],
             [-1, 2], [Q(3, 8), 0], unit, unit * 2, True, ["free", "lower"]),
        case("singular_sum_with_nonzero_linear_face",
             [[2, 2, 0], [2, 2, 0], [0, 0, 0]], [[-2], [-2], [0]],
             [0, 0, 1], [0, 1, 0], [(0, 2)], unit * 3,
             True, ["free", "free", "lower"]),
        case("unique_weakly_active_center_uses_zero_gradient_class", [[2]], [[0]],
             [0], [0], unit, unit, True, ["free"]),
    ]


def main():
    records = []
    for item in examples():
        pattern, gradient = central_gradient_partition(item)
        assert pattern == item.fixed, (item.name, pattern, item.fixed)
        selector = selector_lp(item, pattern, "absolute_values")
        assert (selector is not None) == item.expected, item.name
        assert exhaustive_reference(item) == item.expected, item.name
        if selector is not None:
            verify_selector(item, selector)
        if item.name == "singular_sum_bad_central_vertex":
            assert selector == (Matrix([Q(1, 2), Q(1, 2)]),
                                Matrix([[Q(1, 2)], [Q(1, 2)]]))
            assert selector_lp(item, ("lower", "upper"), "absolute_values") is None
        records.append({
            "name": item.name,
            "central_gradient": [str(value) for value in gradient],
            "global_pattern": list(pattern),
            "affine_selector_exists": selector is not None,
            "center_intercept": [str(value) for value in selector[0]] if selector else None,
            "slope_rows": [[str(value) for value in row] for row in selector[1].tolist()]
                          if selector else None,
        })

    invalid = case("invalid_central_qp_solution", [[2]], [[-2]], [0], [0],
                   [(0, 1)], [(0, 1)], True, ["free"])
    try:
        central_gradient_partition(invalid)
    except AssertionError:
        invalid_rejected = 1
    else:
        raise AssertionError("failed to reject incorrect supplied central optimizer")

    print(json.dumps({
        "arithmetic": "exact SymPy rationals",
        "scope": "finite targeted diagnostic; supplied central QP solutions; no solver benchmark",
        "instances": len(records),
        "recognized_affine": sum(record["affine_selector_exists"] for record in records),
        "recognized_non_affine": sum(not record["affine_selector_exists"] for record in records),
        "invalid_central_optimizers_rejected": invalid_rejected,
        "naive_central_vertex_false_negative_demonstrations": 1,
        "defects": 0,
        **COUNTS,
        "cases": records,
    }, indent=2))


if __name__ == "__main__":
    main()
