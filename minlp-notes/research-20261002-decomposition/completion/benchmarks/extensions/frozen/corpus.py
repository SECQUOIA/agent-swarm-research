"""Eleven bounded extension diagnostics with explicit independent references."""
from fractions import Fraction as F
from itertools import product
from math import ceil, floor, prod
from random import Random


def factor(scope, terms):
    return {"scope": list(scope), "terms": [[str(c), list(p)] for c, p in terms]}


def polynomial(bounds, factors, integers=()):
    return {"kind": "polynomial", "bounds": [[str(a), str(b)] for a, b in bounds],
            "factors": factors, "integers": list(integers)}


def qp(A, b, bounds=None, integers=(), constant=0):
    return {"kind": "qp", "A": [[str(v) for v in row] for row in A],
            "b": list(map(str, b)), "constant": str(constant),
            "bounds": [[str(a), str(b)] for a, b in (bounds or [(0, 1)] * len(b))],
            "integers": list(integers)}


def cases():
    quartic = factor((0,), [(1, (4,)), (-1, (2,)), (F(1, 4), (0,))])
    zero_growth = polynomial([(0, 1)], [factor((0,), [
        (1, (4,)), (F(-4, 3), (3,)), (F(2, 3), (2,)), (F(-4, 27), (1,)), (F(1, 81), (0,))])])
    mixed = polynomial([(1, 2), (1, 2), (0, 2)], [
        factor((0,), [(1, (4,)), (-4, (2,)), (4, (0,))]),
        factor((0, 1), [(1, (2, 0)), (-2, (1, 1)), (1, (0, 2))]),
        factor((2,), [(1, (2,)), (-2, (1,)), (1, (0,))])], (2,))
    irrational = polynomial([(0, 1)] * 2, [quartic,
        factor((0, 1), [(1, (0, 1)), (1, (1, 2))])])
    weak = polynomial([(0, 1), (0, F(1, 2))], [
        factor((0,), [(1, (2,)), (F(-1, 2), (1,)), (F(1, 16), (0,))]),
        factor((1,), [(1, (1,)), (-1, (2,))])])
    symmetric = polynomial([(-1, 1)], [quartic])
    mixture = qp([[-2, F(-3, 2), F(-1, 2)], [F(-3, 2), -2, F(-1, 2)],
                  [F(-1, 2), F(-1, 2), 2]], [2, 2, F(-1, 2)], constant=F(1, 16))
    rng, n = Random(12803), 6
    signs = [rng.choice((-1, 1)) for _ in range(n)]
    A = [[F(0)] * n for _ in range(n)]
    for i in range(n):
        for j in range(i):
            A[i][j] = A[j][i] = -signs[i] * signs[j] * F(rng.randint(1, 3), 5)
        A[i][i] = F(-rng.randint(1, 3), 2) if i < 4 else F(3)
    fresh = qp(A, [F(rng.randint(-4, 5), 3) for _ in range(n)],
               [(-1, 2), (0, 1), (-1, 1), (0, 2), (0, 1), (-1, 2)], integers=(0, 2))
    unsupported = qp([[-1, 1, 1], [1, -1, 1], [1, 1, -1]], [0, 0, 0])
    lattice = polynomial([(-3, 6), (-2, 7), (F(1, 3), F(1, 3))], [factor((0, 1, 2), [
        (F(c, 2), powers + (2,)) for c, powers in
        [(-3, (0, 0)), (-3, (0, 1)), (3, (0, 2)), (7, (1, 0)), (-2, (1, 1)), (-5, (2, 0))]])], (0, 1))
    specs = [
        ("quartic_zero_growth", "polynomial", zero_growth, {"epsilon": "1/4096"},
         "Analytic example: (x-1/3)^4. Minimum 0; quadratic growth fails."),
        ("mixed_sparse_quartic", "polynomial", mixed, {"epsilon": "1/256"},
         "Analytic example: (x^2-2)^2+(y-x)^2+(z-1)^2, integer z. Minimum 0 at (sqrt(2),sqrt(2),1)."),
        ("polynomial_table_cap", "polynomial", mixed, {"epsilon": "1/256", "max_table_states": 1},
         "Same unmodified mixed polynomial with an explicit one-state table cap."),
        ("integer_polynomial_lattice", "polynomial", lattice, {"epsilon": "0"},
         "All varying coordinates native integer, with t fixed to 1/3: (t^2/2)(-3-3y+3y^2+7x-2xy-5x^2). Exact finite-label reference over 100 assignments; nonzero raw gap closed using the value lattice."),
        ("irrational_boundary", "boundary", irrational, {},
         "Analytic example: (x^2-1/2)^2+y+xy^2. Minimum 0 at (1/sqrt(2),0); exact output is implicit."),
        ("weak_boundary", "boundary", weak, {},
         "Analytic example: (x-1/4)^2+y-y^2, y in [0,1/2]. Minimum 0 at (1/4,0); full Hessian indefinite."),
        ("unresolved_symmetric_boundary", "boundary", symmetric, {"max_rounds": 2},
         "Analytic example: (x^2-1/2)^2 on [-1,1]. Two irrational minimizers; two rounds need not yield a unique patch."),
        ("mixed_two_cut", "submodular", mixture, {},
         "Existing two-cut regression: genuine convex combination of greedy bases; independent full-face reference."),
        ("fresh_signed_mixed_6", "submodular", fresh, {},
         "Fresh seed 12803; signed dense QP with four concave and two coupled convex coordinates, including two native integer variables. No planted optimum."),
        ("submodular_cut_cap", "submodular", mixture, {"max_cuts": 1},
         "Unmodified two-cut model with a one-cut cap; strongest completed bound is retained."),
        ("unbalanced_signed_triangle", "submodular", unsupported, {},
         "Positive-edge triangle has no sign flips making every interaction nonpositive. Backend should refuse its structural class."),
    ]
    return {name: {"name": name, "method": method, "model": model,
                   "options": options, "description": description}
            for name, method, model, options, description in specs}


def objective(model, point):
    x = tuple(map(F, point))
    if model["kind"] == "polynomial":
        return sum((F(c) * prod(x[i] ** e for i, e in zip(f["scope"], powers))
                    for f in model["factors"] for c, powers in f["terms"]), F(0))
    return F(model["constant"]) + sum((F(b) * v for b, v in zip(model["b"], x)), F(0)) + sum(
        (F(model["A"][i][j]) * x[i] * x[j] / 2 for i in range(len(x)) for j in range(len(x))), F(0))


def feasible(model, point):
    x = tuple(map(F, point))
    return len(x) == len(model["bounds"]) and all(
        F(a) <= v <= F(b) for v, (a, b) in zip(x, model["bounds"])) and all(
        x[i].denominator == 1 for i in model["integers"])


def nonsingular_solve(matrix, rhs):
    n = len(rhs)
    augmented = [[F(v) for v in row] + [F(b)] for row, b in zip(matrix, rhs)]
    for column in range(n):
        pivot = next((i for i in range(column, n) if augmented[i][column]), None)
        if pivot is None:
            return None
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        scale = augmented[column][column]
        augmented[column] = [v / scale for v in augmented[column]]
        for i in range(n):
            if i != column:
                scale = augmented[i][column]
                augmented[i] = [a - scale * b for a, b in zip(augmented[i], augmented[column])]
    return tuple(row[-1] for row in augmented)


def exact_qp_reference(model):
    """Independent rational stationary-face enumeration, including integer labels.

    A bounded QP has an optimizer on a minimum-dimensional optimal face with
    nonsingular restricted Hessian, or at a vertex: a null direction can
    otherwise be followed at constant value to the boundary. Thus skipping
    singular free systems does not remove every global optimizer.
    """
    n, integer = len(model["b"]), set(model["integers"])
    bounds = [tuple(map(F, pair)) for pair in model["bounds"]]
    choices = [tuple(F(v) for v in range(ceil(lo), floor(hi) + 1)) if i in integer
               else (lo,) if lo == hi else (lo, None, hi) for i, (lo, hi) in enumerate(bounds)]
    best, witness, checked = None, None, 0
    for face in product(*choices):
        free = [i for i, v in enumerate(face) if v is None]
        point = list(face)
        if free:
            matrix = [[F(model["A"][i][j]) for j in free] for i in free]
            rhs = [-F(model["b"][i]) - sum((F(model["A"][i][j]) * v
                    for j, v in enumerate(face) if v is not None), F(0)) for i in free]
            solution = nonsingular_solve(matrix, rhs)
            if solution is None:
                continue
            for i, value in zip(free, solution):
                point[i] = value
        if feasible(model, point):
            checked += 1
            value = objective(model, point)
            if best is None or value < best:
                best, witness = value, point
    assert best is not None
    return {"value": str(best), "point": list(map(str, witness)),
            "method": "independent exact stationary-face and integer-label enumeration",
            "feasible_stationary_candidates": checked}


def references():
    output = {}
    for name, spec in cases().items():
        model = spec["model"]
        if model["kind"] == "qp":
            output[name] = exact_qp_reference(model)
        elif name == "integer_polynomial_lattice":
            labels = [tuple(F(v) for v in range(ceil(F(a)), floor(F(b)) + 1)) if i in model["integers"]
                      else (F(a),) for i, (a, b) in enumerate(model["bounds"])]
            candidates = [(objective(model, point), point) for point in product(*labels)]
            value, point = min(candidates)
            output[name] = {"value": str(value), "point": list(map(str, point)),
                            "method": "independent exact enumeration of all native-integer assignments",
                            "assignments": len(candidates)}
        else:
            output[name] = {"value": "0", "method": "analytic nonnegative identity", "identity": spec["description"]}
    return output
