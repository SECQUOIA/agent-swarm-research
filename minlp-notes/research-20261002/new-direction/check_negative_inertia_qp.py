#!/usr/bin/env python3
"""Small exact tests for negative-inertia-qp.md, not a polynomial QP solver.

The auxiliary algorithm really evaluates corner recourse, prunes cells, and
reconstructs rationals. Its convex QP oracle enumerates stationary active
faces, exponentially in dimension. Denominator bounds are fixture data, not
an implementation of the theorem's universal determinant bound. No spectral
normalization or production complexity claim is tested here.
"""

from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import combinations, product
import json


def dot(x, y):
    return sum((a * b for a, b in zip(x, y)), Q(0))


def matvec(matrix, vector):
    return tuple(dot(row, vector) for row in matrix)


def norm2(vector):
    return dot(vector, vector)


def inverse(matrix):
    n = len(matrix)
    rows = [list(row) + [Q(i == j) for j in range(n)]
            for i, row in enumerate(matrix)]
    for col in range(n):
        pivot = next((i for i in range(col, n) if rows[i][col]), None)
        if pivot is None:
            return None
        rows[col], rows[pivot] = rows[pivot], rows[col]
        scale = rows[col][col]
        rows[col] = [v / scale for v in rows[col]]
        for i in range(n):
            if i != col:
                scale = rows[i][col]
                rows[i] = [v - scale * w for v, w in zip(rows[i], rows[col])]
    return tuple(tuple(row[n:]) for row in rows)


def quadratic(matrix, linear, constant, x):
    return dot(x, matvec(matrix, x)) / 2 + dot(linear, x) + constant


class FaceQP:
    """Exact stationary-face enumeration for the small bounded fixtures.

    A minimizer on a smallest-dimensional face has nonsingular restricted
    Hessian unless that face is a vertex. Thus enumerating nonsingular KKT
    systems includes a global minimizer, even with singular ambient Hessian
    or paired inequalities representing an affine hull. Feasible candidates
    need no multiplier-sign filter: their least objective is selected.
    """

    def __init__(self, matrix, constraints, rhs):
        self.matrix, self.constraints, self.rhs = matrix, constraints, rhs
        self.n = len(matrix)
        self.systems = []
        for size in range(self.n + 1):
            for active in combinations(range(len(rhs)), size):
                rows = [list(matrix[i]) + [constraints[j][i] for j in active]
                        for i in range(self.n)]
                rows += [list(constraints[j]) + [Q(0)] * size for j in active]
                inv = inverse(rows)
                if inv is not None:
                    self.systems.append((active, inv[:self.n]))

    def feasible(self, x):
        return all(dot(row, x) <= bound
                   for row, bound in zip(self.constraints, self.rhs))

    def solve(self, linear, constant=Q(0)):
        candidates = []
        for active, rows in self.systems:
            rhs = tuple(-v for v in linear) + tuple(self.rhs[j] for j in active)
            x = matvec(rows, rhs)
            if self.feasible(x):
                candidates.append((quadratic(self.matrix, linear, constant, x), x))
        assert candidates, "No feasible stationary-face candidate"
        return min(candidates)


@dataclass(frozen=True)
class Fixture:
    name: str
    A: tuple
    P: tuple
    b: tuple
    c: Q
    T: tuple
    alpha: Q
    M: tuple
    d: tuple
    optimum: Q
    image: tuple
    g_projected: Q
    value_denominator: int
    image_denominator: int
    g_full: Q | None = None
    beta2: Q | None = None


def matrix(rows):
    return tuple(tuple(Q(v) for v in row) for row in rows)


def fixtures():
    scalar_box = matrix([[-1], [1]])
    line_box = matrix([[-1, 0], [1, 0], [-2, 1], [2, -1]])
    line_rhs = (Q(0), Q(1), Q(0), Q(0))
    return [
        Fixture("scalar_nondyadic", matrix([[2]]), matrix([[4]]), (Q(-2, 3),),
                Q(1, 9), matrix([[1]]), Q(2), scalar_box, (Q(0), Q(1)),
                Q(0), (Q(1, 3),), Q(1), 1, 3, Q(1), Q(1)),
        Fixture("indefinite_line_singular_P", matrix([[-2, 0], [0, 2]]),
                matrix([[0, 0], [0, 2]]), (Q(-2), Q(0)), Q(0),
                matrix([[1, 0]]), Q(2), line_box, line_rhs,
                Q(-1, 3), (Q(1, 3),), Q(3), 3, 3, Q(3, 5), Q(1)),
        Fixture("continuum_original_optima", matrix([[-2, 0, 0], [0, 2, 0], [0, 0, 0]]),
                matrix([[0, 0, 0], [0, 2, 0], [0, 0, 0]]),
                (Q(-2), Q(0), Q(0)), Q(0), matrix([[1, 0, 0]]), Q(2),
                matrix([[-1, 0, 0], [1, 0, 0], [-2, 1, 0], [2, -1, 0],
                        [0, 0, -1], [0, 0, 1]]),
                (Q(0), Q(1), Q(0), Q(0), Q(0), Q(1)),
                Q(-1, 3), (Q(1, 3),), Q(3), 3, 3),
        Fixture("two_auxiliary_coordinates_clipped", matrix([[-2, 0], [0, 2]]),
                matrix([[0, 0], [0, Q(13, 2)]]), (Q(-2), Q(0)), Q(0),
                matrix([[1, 0], [0, Q(3, 2)]]), Q(2), line_box, line_rhs,
                Q(-1, 3), (Q(1, 3), Q(1)), Q(3, 10), 3, 3,
                Q(3, 5), Q(9, 4)),
        Fixture("nonsmooth_inner_tie", matrix([[-2]]), matrix([[0]]), (Q(1, 2),),
                Q(0), matrix([[1]]), Q(2), scalar_box, (Q(0), Q(1)),
                Q(-1, 2), (Q(1),), Q(1, 2), 2, 1, Q(1, 2), Q(1)),
    ]


class Auxiliary:
    def __init__(self, fixture):
        self.f = fixture
        self.qp = FaceQP(fixture.P, fixture.M, fixture.d)
        self.cache = {}
        self.strict_witness_gaps = 0
        n = len(fixture.b)
        zeros = matrix([[0] * n for _ in range(n)])
        lp = FaceQP(zeros, fixture.M, fixture.d)
        self.box = tuple((lp.solve(row)[0], -lp.solve(tuple(-v for v in row))[0])
                         for row in fixture.T)
        assert all(lo < hi for lo, hi in self.box)

    def objective(self, x):
        return quadratic(self.f.A, self.f.b, self.f.c, x)

    def evaluate(self, a):
        if a not in self.cache:
            f = self.f
            linear = tuple(f.b[j] - f.alpha * sum(a[i] * f.T[i][j]
                                                  for i in range(len(a)))
                           for j in range(len(f.b)))
            inner, witness = self.qp.solve(linear, f.c)
            value = inner + f.alpha * norm2(a) / 2
            original = self.objective(witness)
            distance = tuple(v - w for v, w in zip(a, matvec(f.T, witness)))
            assert value == original + f.alpha * norm2(distance) / 2
            assert original >= f.optimum and original <= value
            if original < value:
                self.strict_witness_gaps += 1
            gW = f.g_projected * f.alpha / (2 * f.g_projected + f.alpha)
            error2 = norm2(tuple(v - w for v, w in zip(a, f.image)))
            assert value - f.optimum >= gW * error2
            if f.g_full is not None:
                full_gW = f.g_full * f.alpha / (2 * f.g_full + f.alpha * f.beta2)
                assert value - f.optimum >= full_gW * error2
            self.cache[a] = value, witness
        return self.cache[a]


def bounded_rationals(lo, hi, denominator):
    values = set()
    for d in range(1, denominator + 1):
        for numerator in range((lo * d).__ceil__(), (hi * d).__floor__() + 1):
            values.add(Q(numerator, d))
    return sorted(values)


def corners(cell):
    return product(*[(lo, hi) for lo, hi in cell])


def contains(cell, point):
    return all(lo <= v <= hi for (lo, hi), v in zip(cell, point))


def refine(cell, box, spacing):
    partitions = []
    for (lo, hi), (origin, _) in zip(cell, box):
        split = origin + (((lo - origin) / spacing).__floor__() + 1) * spacing
        assert split + spacing >= hi
        partitions.append([(lo, split), (split, hi)] if split < hi else [(lo, hi)])
    return product(*partitions)


def branch_and_bound(aux, exact, gap=Q(1, 4096)):
    """Execute the note's algorithm; known answers are used only in assertions."""
    f = aux.f
    rank = len(f.T)
    width = max(hi - lo for lo, hi in aux.box)
    cells = [aux.box]
    incumbent = None
    best_auxiliary = None
    isolated_value = None
    stats = dict(level=0, corner_requests=0, generated_cells=0, pruned_cells=0,
                 max_survivors=0, reconstruction_rejections=0,
                 reconstruction_missing=0, clipped_cells=0)
    for level in range(25):
        spacing = width / 2**level
        delta = rank * f.alpha * spacing**2 / 8
        records = []
        for cell in cells:
            stats["generated_cells"] += 1
            stats["clipped_cells"] += any(hi - lo < spacing for lo, hi in cell)
            evaluated = []
            for a in corners(cell):
                stats["corner_requests"] += 1
                value, witness = aux.evaluate(a)
                candidate = (aux.objective(witness), witness)
                incumbent = candidate if incumbent is None else min(incumbent, candidate)
                pair = (value, a)
                best_auxiliary = pair if best_auxiliary is None else min(best_auxiliary, pair)
                evaluated.append(pair)
            minimum, point = min(evaluated)
            correction = f.alpha * sum((hi - lo)**2 for lo, hi in cell) / 8
            lower = minimum - correction
            midpoint = tuple((lo + hi) / 2 for lo, hi in cell)
            assert lower <= aux.evaluate(midpoint)[0]
            if contains(cell, f.image):
                assert lower <= f.optimum
            records.append((lower, cell, minimum, point))
        surviving = [item for item in records if item[0] < incumbent[0]]
        stats["pruned_cells"] += len(records) - len(surviving)
        stats["max_survivors"] = max(stats["max_survivors"], len(surviving))
        stats["level"] = level
        if not surviving:
            assert incumbent[0] == f.optimum
            stats["termination"] = "no_surviving_cells"
            return stats
        lower = min(item[0] for item in surviving)
        upper = incumbent[0]
        assert lower <= f.optimum <= upper
        assert upper - lower <= delta
        assert upper <= f.optimum + delta
        gW = f.g_projected * f.alpha / (2 * f.g_projected + f.alpha)
        kappa = f.alpha / gW
        root_bound = 0
        while root_bound**2 < rank * kappa:
            root_bound += 1
        assert len(surviving) <= 2**rank * (root_bound + 4)**rank
        for bound, cell, minimum, point in surviving:
            assert minimum < f.optimum + 2 * delta
            assert norm2(tuple(v - w for v, w in zip(point, f.image))) < 2 * delta / gW
        if upper > f.optimum:
            assert any(contains(item[1], f.image) for item in surviving)
            assert best_auxiliary[0] - f.optimum <= delta
        if not exact and upper - lower <= gap:
            stats["termination"] = "certified_gap"
            stats["gap"] = str(upper - lower)
            return stats
        if exact and isolated_value is None and upper - lower < Q(1, 2 * f.value_denominator**2):
            candidates = bounded_rationals(lower, upper, f.value_denominator)
            assert candidates == [f.optimum]
            isolated_value = candidates[0]
        if exact and isolated_value is not None:
            if upper == isolated_value:
                stats["termination"] = "exact_incumbent"
                return stats
            radius = Q(1, 4 * f.image_denominator**2)
            reconstructed = [bounded_rationals(v - radius, v + radius, f.image_denominator)
                             for v in best_auxiliary[1]]
            assert all(len(values) <= 1 for values in reconstructed)
            if all(reconstructed):
                a = tuple(values[0] for values in reconstructed)
                _, witness = aux.evaluate(a)
                if aux.objective(witness) == isolated_value:
                    assert matvec(f.T, witness) == f.image
                    stats["termination"] = "exact_reconstruction"
                    stats["reconstructed_image"] = [str(v) for v in a]
                    return stats
                stats["reconstruction_rejections"] += 1
            else:
                stats["reconstruction_missing"] += 1
        cells = [child for _, cell, _, _ in surviving
                 for child in refine(cell, aux.box, spacing / 2)]
    raise AssertionError("Fixture did not terminate within 25 levels")


def verify_fixture(f, aux):
    n = len(f.b)
    for i in range(n):
        for j in range(n):
            assert f.A[i][j] == f.P[i][j] - f.alpha * sum(row[i] * row[j] for row in f.T)
    # All supplied P matrices are diagonal; nonnegative diagonal proves PSD.
    assert all(f.P[i][i] >= 0 for i in range(n))
    assert all(f.P[i][j] == 0 for i in range(n) for j in range(n) if i != j)
    reference, point = FaceQP(f.A, f.M, f.d).solve(f.b, f.c)
    assert reference == f.optimum and matvec(f.T, point) == f.image
    assert aux.evaluate(f.image)[0] == f.optimum
    coordinates = [sorted({lo - 1, lo, (lo + hi) / 2, hi, hi + 1, optimum})
                   for (lo, hi), optimum in zip(aux.box, f.image)]
    sample_count = 0
    for a in product(*coordinates):
        value, witness = aux.evaluate(a)
        if f.name == "nonsmooth_inner_tie":
            expected = a[0]**2 + min(Q(0), Q(1, 2) - 2 * a[0])
        elif f.name == "scalar_nondyadic":
            x = min(Q(1), max(Q(0), (a[0] + Q(1, 3)) / 2))
            assert witness == (x,)
            expected = (x - Q(1, 3))**2 + (a[0] - x)**2
        else:
            x = ((1 + a[0] + 3 * a[1]) / 13 if len(a) == 2
                 else (1 + a[0]) / 4)
            x = min(Q(1), max(Q(0), x))
            assert witness[:2] == (x, 2 * x)
            expected = 3 * x**2 - 2 * x + (a[0] - x)**2
            if len(a) == 2:
                expected += (a[1] - 3 * x)**2
        assert value == expected
        sample_count += 1
    # The growth-transfer constant is attained in these interior quadratic
    # examples. In the two-coordinate case, use the image-line direction.
    if f.name != "nonsmooth_inner_tie":
        direction = (Q(1), Q(3)) if len(f.T) == 2 else (Q(1),)
        gW = f.g_projected * f.alpha / (2 * f.g_projected + f.alpha)
        for step in (Q(-1, 12), Q(0), Q(1, 12)):
            a = tuple(v + step * d for v, d in zip(f.image, direction))
            assert aux.evaluate(a)[0] - f.optimum == gW * step**2 * norm2(direction)
    # Feasible samples prove neither growth nor uniqueness; the formulas below
    # also verify the fixture-specific exact gap identities.
    if n == 1:
        for x in (Q(i, 12) for i in range(13)):
            image_error = norm2(tuple(v - w for v, w in zip(matvec(f.T, (x,)), f.image)))
            assert aux.objective((x,)) - f.optimum >= f.g_projected * image_error
    else:
        for x in (Q(i, 12) for i in range(13)):
            for z in ([Q(0), Q(1, 2), Q(1)] if n == 3 else [None]):
                point = (x, 2 * x) if z is None else (x, 2 * x, z)
                assert aux.qp.feasible(point)
                gap = aux.objective(point) - f.optimum
                image_error = norm2(tuple(v - w for v, w in zip(matvec(f.T, point), f.image)))
                assert gap == 3 * (x - Q(1, 3))**2
                assert gap == f.g_projected * image_error
                if f.g_full is not None:
                    assert gap == f.g_full * ((x - Q(1, 3))**2 + (2*x - Q(2, 3))**2)
        if n == 3:
            assert all(aux.objective((Q(1, 3), Q(2, 3), z)) == f.optimum
                       for z in (Q(0), Q(1, 2), Q(1)))
    if f.name == "nonsmooth_inner_tie":
        value, _ = aux.evaluate((Q(1, 4),))
        assert value == Q(1, 16)
        assert quadratic(f.P, (Q(0),), f.c, (Q(0),)) == quadratic(f.P, (Q(0),), f.c, (Q(1),))
    return sample_count


def main():
    report = {}
    for f in fixtures():
        aux = Auxiliary(f)
        samples = verify_fixture(f, aux)
        approximate = branch_and_bound(aux, exact=False)
        exact = branch_and_bound(aux, exact=True)
        assert aux.strict_witness_gaps > 0
        if f.image_denominator == 3:
            assert exact["termination"] == "exact_reconstruction" and exact["level"] > 0
        if len(f.T) == 2:
            assert approximate["clipped_cells"] > 0
            assert any(a[1] != 3 * a[0] for a in aux.cache)
        report[f.name] = dict(auxiliary_growth_samples=samples,
                              distinct_auxiliary_evaluations=len(aux.cache),
                              strict_auxiliary_witness_gaps=aux.strict_witness_gaps,
                              approximate=approximate, exact=exact)
    assert report["scalar_nondyadic"]["exact"]["reconstruction_rejections"] > 0
    print(json.dumps({"result": "PASS", "fixtures": report}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
