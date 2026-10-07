"""Small exact diagnostics for algebraic closure, not a production QP solver.

The inner Hessians are diagonal, so clipping gives independent recourse
answers. Extracted active-basis KKT systems and their critical regions are
checked with rational algebra. The original objective has nonpositive
diagonal curvature, so complete original-box vertex enumeration supplies
an independent exact reference and same-draw fallback.
"""

from dataclasses import dataclass
from itertools import product
import json

import sympy as sp


Q = sp.Rational


def scalar(x):
    return x[0] if isinstance(x, sp.MatrixBase) else x


def quadratic(H, p, e, x):
    x = sp.Matrix(x)
    return scalar(x.T * H * x) / 2 + scalar(p.T * x) + e


def corners(lo, hi):
    return list(product(*[(a, b) if a != b else (a,) for a, b in zip(lo, hi)]))


def box_quadratic_min(H, p, e, lo, hi):
    """Exact face-stationarity enumeration, including singular-face descent."""
    candidates = []
    k = len(lo)
    for status in product((-1, 0, 1), repeat=k):
        free = [i for i, tag in enumerate(status) if tag == 0]
        fixed = [i for i, tag in enumerate(status) if tag != 0]
        point = sp.zeros(k, 1)
        for i in fixed:
            point[i] = lo[i] if status[i] == -1 else hi[i]
        if free:
            block = H.extract(free, free)
            if block.det() == 0:
                continue
            rhs = -p.extract(free, [0])
            if fixed:
                rhs -= H.extract(free, fixed) * point.extract(fixed, [0])
            solution = block.inv() * rhs
            for pos, i in enumerate(free):
                point[i] = solution[pos]
        if all(a <= x <= b for a, x, b in zip(lo, point, hi)):
            candidates.append((quadratic(H, p, e, point), tuple(point)))
    assert candidates
    return min(candidates)


@dataclass
class Piece:
    H: sp.Matrix
    p: sp.Matrix
    e: sp.Rational
    rows: list
    X: sp.Matrix
    x0: sp.Matrix

    def contains(self, point):
        z = sp.Matrix(point)
        return all(scalar(row.T * z) <= rhs for row, rhs in self.rows)


class Recourse:
    def __init__(self, name, T, alpha, diagonal, lo, hi, redundant=False):
        self.name, self.T, self.alpha = name, sp.Matrix(T), Q(alpha)
        self.k, self.n = self.T.shape
        self.P = sp.diag(*map(Q, diagonal))
        self.A = self.P - self.alpha * self.T.T * self.T
        self.lo, self.hi = tuple(map(Q, lo)), tuple(map(Q, hi))
        self.b = sp.zeros(self.n, 1)
        self.pieces = {}
        self.cache = {}
        self.counts = {"basis_formulas": 0, "region_checks": 0,
                       "singular_piece_queries": 0, "private_flat_queries": 0,
                       "lower_dimensional_region_queries": 0}
        rows, rhs = [], []
        for i in range(self.n):
            unit = sp.eye(self.n)[:, i]
            rows.extend((unit.T, -unit.T))
            rhs.extend((self.hi[i], -self.lo[i]))
        if redundant:
            rows.append(2 * sp.eye(self.n)[0, :])
            rhs.append(2 * self.hi[0])
        self.M, self.d = sp.Matrix.vstack(*rows), sp.Matrix(rhs)
        assert all(self.A[i, i] <= 0 for i in range(self.n))
        assert all(self.T * v == sp.zeros(self.k, 1) for v in self.P.nullspace())

    def original(self, x, noise):
        return quadratic(self.A, self.T.T * sp.Matrix(noise), Q(0), x)

    def reference(self, noise):
        return min((self.original(x, noise), x) for x in corners(self.lo, self.hi))

    def inner(self, point):
        point = tuple(map(Q, point))
        if point in self.cache:
            return self.cache[point]
        a = sp.Matrix(point)
        linear = self.b - self.alpha * self.T.T * a
        x, status = [], []
        for i in range(self.n):
            if self.P[i, i] == 0:
                assert linear[i] == 0
                v = self.lo[i]
                self.counts["private_flat_queries"] += 1
            else:
                v = min(self.hi[i], max(self.lo[i], -linear[i] / self.P[i, i]))
            x.append(v)
            if v == self.lo[i] == self.hi[i]:
                status.append(-1 if self.P[i, i] * v + linear[i] >= 0 else 1)
            else:
                status.append(-1 if v == self.lo[i] else 1 if v == self.hi[i] else 0)
        x, status = sp.Matrix(x), tuple(status)
        if status not in self.pieces:
            self.pieces[status] = self.extract(status)
            self.counts["basis_formulas"] += 1
        piece = self.pieces[status]
        assert piece.contains(point)
        assert piece.X * a + piece.x0 == x
        value = quadratic(self.A, self.b, Q(0), x)
        value += self.alpha * scalar((a - self.T * x).T * (a - self.T * x)) / 2
        assert value == quadratic(piece.H, piece.p, piece.e, a)
        assert piece.H * a + piece.p == self.alpha * (a - self.T * x)
        if piece.H.det() == 0:
            self.counts["singular_piece_queries"] += 1
        if self.name == "lower_dimensional_critical" and point == (Q(0),):
            assert not piece.contains((Q(-1, 100),))
            assert not piece.contains((Q(1, 100),))
            self.counts["lower_dimensional_region_queries"] += 1
        self.counts["region_checks"] += 1
        self.cache[point] = value, piece, tuple(x)
        return self.cache[point]

    def extract(self, status):
        active = [i for i, tag in enumerate(status) if tag]
        J = sp.zeros(len(active), self.n)
        rhs = []
        for pos, i in enumerate(active):
            J[pos, i] = status[i]
            rhs.append(self.hi[i] if status[i] == 1 else -self.lo[i])
        K = self.P.row_join(J.T).col_join(J.row_join(sp.zeros(len(active))))
        assert K.det() != 0
        const = K.inv() * sp.Matrix(list(-self.b) + rhs)
        slopes = K.inv() * (self.alpha * self.T.T).col_join(sp.zeros(len(active), self.k))
        X, x0 = slopes[:self.n, :], const[:self.n, :]
        lambdas, lambda0 = slopes[self.n:, :], const[self.n:, :]
        assert J * X == sp.zeros(len(active), self.k)
        H = self.alpha * (sp.eye(self.k) - self.T * X)
        p = -self.alpha * self.T * x0
        e = quadratic(self.A, self.b, Q(0), x0) + self.alpha * scalar((self.T * x0).T * (self.T * x0)) / 2
        assert H == H.T
        assert H == X.T * self.P * X - self.alpha * (self.T * X + X.T * self.T.T) + self.alpha * sp.eye(self.k)
        assert p == X.T * (self.P * x0 + self.b) - self.alpha * self.T * x0
        rows = []
        for row, bound in zip((self.M * X).tolist(), self.d - self.M * x0):
            rows.append((sp.Matrix(row), bound))
        for row, bound in zip((-lambdas).tolist(), lambda0):
            rows.append((sp.Matrix(row), bound))
        return Piece(H, p, e, rows, X, x0)


def check_hyperplane(model, piece, v, cell_corners, noise, value, optimum, target, stats):
    gradient = piece.H * sp.Matrix(v) + piece.p + sp.Matrix(noise)
    norm2 = scalar(gradient.T * gradient)
    assert norm2 <= 2 * model.alpha * (value - optimum)
    if piece.H.det() == 0:
        normal = piece.H.nullspace()[0]
        residual = scalar(normal.T * (sp.Matrix(noise) + piece.p))
        stats["singular_image_checks"] += 1
    else:
        violated = next((row, rhs) for row, rhs in piece.rows
                        if any(scalar(row.T * sp.Matrix(c)) > rhs for c in cell_corners))
        row, rhs = violated
        assert scalar(row.T * row) > 0
        distance = (scalar(row.T * sp.Matrix(v)) - rhs) ** 2 / scalar(row.T * row)
        assert distance <= model.k * target**2
        normal = piece.H.inv().T * row
        residual = scalar(normal.T * sp.Matrix(noise)) + rhs + scalar(normal.T * piece.p)
        stats["facet_image_checks"] += 1
    # Entrywise absolute sum is a rational upper bound on the spectral norm.
    Hbound = sum(abs(entry) for entry in piece.H)
    assert residual**2 / scalar(normal.T * normal) <= model.k * (model.alpha + Hbound) ** 2 * target**2


def run(model, noise, cap, stats):
    noise = tuple(map(Q, noise))
    sigma = Q(1, 2)
    projections = [tuple(model.T * sp.Matrix(x)) for x in corners(model.lo, model.hi)]
    lower = tuple(min(x[i] for x in projections) - sigma / model.alpha for i in range(model.k))
    upper = tuple(max(x[i] for x in projections) + sigma / model.alpha for i in range(model.k))
    widths = tuple(b - a for a, b in zip(lower, upper))
    reference, _ = model.reference(noise)
    shift = sum(c * c for c in noise) / (2 * model.alpha)
    optimum = reference - shift
    incumbent, witness = None, None
    active, old_m = [tuple(0 for _ in widths)], [1] * model.k

    def update(value, x):
        nonlocal incumbent, witness
        if incumbent is None or value < incumbent:
            incumbent, witness = value, x

    for level in range(cap + 1):
        target = max(widths) / 2**level
        m = []
        for width in widths:
            count = 1
            while width / count > target:
                count *= 2
            m.append(count)
        spacing = tuple(w / count for w, count in zip(widths, m))
        B = model.alpha * sum(h * h for h in spacing) / 8
        if level:
            active = [child for index in active for child in product(*[
                (2 * pos, 2 * pos + 1) if count == 2 * old else (pos,)
                for pos, count, old in zip(index, m, old_m)
            ])]
        unresolved = []
        for index in active:
            stats["processed_cells"] += 1
            lo = tuple(a + pos * h for a, pos, h in zip(lower, index, spacing))
            hi = tuple(a + h for a, h in zip(lo, spacing))
            cell_corners = corners(lo, hi)
            records = []
            for v in cell_corners:
                val, piece, x = model.inner(v)
                val += sum(c * a for c, a in zip(noise, v))
                update(val, x)
                records.append((val, v, piece))
            closed = next((piece for _, _, piece in records
                           if all(piece.contains(v) for v in cell_corners)), None)
            if closed is not None:
                val, point = box_quadratic_min(closed.H, closed.p + sp.Matrix(noise), closed.e, lo, hi)
                actual, _, x = model.inner(point)
                assert actual + sum(c * a for c, a in zip(noise, point)) == val
                assert all(closed.contains(v) for v in cell_corners)
                update(val, x)
                stats["exact_closures"] += 1
            else:
                best = min(records, key=lambda item: item[0])
                unresolved.append((index, best[0] - B, best, cell_corners))
        assert optimum <= incumbent <= optimum + B
        active = []
        for index, bound, (val, v, piece), cell_corners in unresolved:
            if bound <= incumbent:
                assert val - optimum <= 2 * B
                check_hyperplane(model, piece, v, cell_corners, noise, val, optimum, target, stats)
                active.append(index)
                stats["retained_unresolved"] += 1
            else:
                stats["ordinary_prunes"] += 1
        stats["levels"] += 1
        if not active:
            assert incumbent == optimum
            assert model.original(witness, noise) == reference
            stats["closure_solved_cases"] += 1
            break
        old_m = m
    else:
        fallback_value, fallback_x = model.reference(noise)
        assert fallback_value == reference
        assert model.original(fallback_x, noise) == reference
        stats["same_draw_fallbacks"] += 1
    stats["cases"] += 1


def main():
    stats = dict.fromkeys(("cases", "levels", "processed_cells", "exact_closures",
                          "ordinary_prunes", "retained_unresolved", "closure_solved_cases",
                          "same_draw_fallbacks", "facet_image_checks", "singular_image_checks"), 0)
    axis = Recourse("negative_three", sp.eye(3), 2, [1] * 3, [-1] * 3, [1] * 3)
    coupled = Recourse("coupled_negative_three",
                       [[Q(1, 2), Q(1, 4), 0], [0, Q(1, 2), Q(1, 4)], [Q(1, 4), 0, Q(1, 2)]],
                       4, [Q(1, 4)] * 3, [-1] * 3, [1] * 3)
    private = Recourse("private_flat_redundant", sp.eye(3).row_join(sp.zeros(3, 1)),
                       2, [1, 1, 1, 0], [-1] * 4, [1] * 4, redundant=True)
    fixed = Recourse("lower_dimensional_domain", sp.eye(3).row_join(sp.zeros(3, 1)),
                     2, [1, 1, 1, 0], [-1, -1, -1, 0], [1, 1, 1, 0], redundant=True)
    flat = Recourse("singular_gradient_piece", [[1]], 2, [2], [-1], [1])
    critical = Recourse("lower_dimensional_critical", [[Q(1, 2), Q(1, 2)]],
                        4, [1, 1], [-1, 0], [0, 1])
    assert (-axis.A).is_positive_definite
    assert (-coupled.A).is_positive_definite
    # Explicitly query a lower-dimensional region even if closure later
    # chooses a neighboring full-dimensional region for the same point.
    critical.inner((Q(0),))
    for model in (axis, coupled):
        for noise in ((0, 0, 0), (Q(1, 2), Q(-1, 4), Q(1, 3)),
                      (Q(-1, 2), Q(1, 2), Q(-1, 2))):
            run(model, noise, 3, stats)
    for model in (private, fixed):
        run(model, (Q(1, 2), Q(-1, 4), Q(1, 3)), 3, stats)
    for model in (flat, critical):
        for noise in ((Q(0),), (Q(1, 2),)):
            run(model, noise, 3, stats)
    # Force one early cap to exercise fallback on the original sampled draw.
    run(coupled, (Q(1, 2), Q(-1, 4), Q(1, 3)), 0, stats)
    assert stats["exact_closures"] > 0 and stats["ordinary_prunes"] > 0
    assert stats["same_draw_fallbacks"] > 0 and stats["closure_solved_cases"] > 0
    assert flat.counts["singular_piece_queries"] > 0
    assert critical.counts["lower_dimensional_region_queries"] > 0
    print(json.dumps({"status": "passed", **stats,
                      "fixtures": {model.name: model.counts for model in
                                   (axis, coupled, private, fixed, flat, critical)}}, indent=2))


if __name__ == "__main__":
    main()
