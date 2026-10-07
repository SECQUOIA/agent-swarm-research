"""Exact mixed-recourse diagnostics; small enumerations are reference checks.

Reuse the previously checked cell driver, but supply a new scalar oracle
that searches integer ranges and extracts global separable critical regions.
The independent reference enumerates integer labels and continuous piece
boxes. This is not a production implementation or a runtime benchmark.
"""

from itertools import product
import json

import sympy as sp

from check_smoothed_cell_closure import Piece, Q, box_quadratic_min, run, scalar


def poly(piece, x):
    _, _, p, b, c = piece
    return p * x * x / 2 + b * x + c


def one_piece(lo, hi, p, b=0, c=0):
    return [(Q(lo), Q(hi), Q(p), Q(b), Q(c))]


class MixedRecourse:
    def __init__(self, name, T, alpha, pieces, integers, residual=None):
        self.name, self.T, self.alpha = name, sp.Matrix(T), Q(alpha)
        self.k, self.n = self.T.shape
        self.data = [[tuple(map(Q, piece)) for piece in coordinate] for coordinate in pieces]
        self.integers = set(integers)
        self.continuous = [i for i in range(self.n) if i not in self.integers]
        self.lo = tuple(coordinate[0][0] for coordinate in self.data)
        self.hi = tuple(coordinate[-1][1] for coordinate in self.data)
        self.residual = tuple(map(Q, residual or [0] * self.n))
        self.pieces, self.cache, self.references = {}, {}, {}
        self.counts = {"query_checks": 0, "integer_comparisons": 0,
                       "extracted_formulas": 0, "integer_ties": 0,
                       "knot_states": 0}
        for coordinate in self.data:
            assert all(lo < hi and p >= 0 for lo, hi, p, _, _ in coordinate)
            for left, right in zip(coordinate, coordinate[1:]):
                v = left[1]
                assert v == right[0] and poly(left, v) == poly(right, v)
                assert left[2] * v + left[3] <= right[2] * v + right[3]

    def phi(self, i, x):
        return next(poly(piece, x) for piece in self.data[i] if piece[0] <= x <= piece[1])

    def delta(self, i, z):
        return self.phi(i, z + 1) - self.phi(i, z)

    def scalar_state(self, i, lam):
        if i in self.integers:
            left, right = int(self.lo[i]), int(self.hi[i])
            while left < right:
                middle = (left + right) // 2
                self.counts["integer_comparisons"] += 1
                if self.delta(i, middle) >= lam:
                    right = middle
                else:
                    left = middle + 1
            z = Q(left)
            lower = self.delta(i, z - 1) if z > self.lo[i] else None
            upper = self.delta(i, z) if z < self.hi[i] else None
            assert lower is None or lower <= lam
            assert upper is None or lam <= upper
            if lower == lam or upper == lam:
                self.counts["integer_ties"] += 1
            return ("integer", z), z, lower, upper, None

        coordinate = self.data[i]
        knots = [coordinate[0][0]] + [piece[1] for piece in coordinate]
        for j, v in enumerate(knots):
            lower = coordinate[j - 1][2] * v + coordinate[j - 1][3] if j else None
            upper = coordinate[j][2] * v + coordinate[j][3] if j < len(coordinate) else None
            if (lower is None or lower <= lam) and (upper is None or lam <= upper):
                self.counts["knot_states"] += 1
                return ("knot", j), v, lower, upper, None
        for j, piece in enumerate(coordinate):
            lo, hi, p, b, _ = piece
            if p and p * lo + b <= lam <= p * hi + b:
                return ("free", j), (lam - b) / p, p * lo + b, p * hi + b, piece
        raise AssertionError("Scalar states did not cover the query")

    def original(self, x, noise):
        image = self.T * sp.Matrix(x)
        return (sum(self.phi(i, v) + self.residual[i] * v for i, v in enumerate(x))
                - self.alpha * scalar(image.T * image) / 2
                + sum(c * v for c, v in zip(noise, image)))

    def inner(self, point):
        point = tuple(map(Q, point))
        if point in self.cache:
            return self.cache[point]
        a = sp.Matrix(point)
        states = [self.scalar_state(i, self.alpha * scalar(self.T[:, i].T * a) - self.residual[i])
                  for i in range(self.n)]
        key = tuple(state[0] for state in states)
        x = tuple(state[1] for state in states)
        if key not in self.pieces:
            H, X, x0, rows, e = self.alpha * sp.eye(self.k), sp.zeros(self.n, self.k), sp.zeros(self.n, 1), [], Q(0)
            for i, (_, v, lower, upper, free_piece) in enumerate(states):
                column = self.T[:, i]
                if free_piece is None:
                    x0[i] = v
                    e += self.phi(i, v) + self.residual[i] * v
                else:
                    _, _, p, b, c = free_piece
                    X[i, :] = (self.alpha / p) * column.T
                    x0[i] = -(b + self.residual[i]) / p
                    H -= (self.alpha**2 / p) * column * column.T
                    e += p * x0[i] ** 2 / 2 + (b + self.residual[i]) * x0[i] + c
                if lower is not None:
                    rows.append((-self.alpha * column, -lower - self.residual[i]))
                if upper is not None:
                    rows.append((self.alpha * column, upper + self.residual[i]))
            self.pieces[key] = Piece(H, -self.alpha * self.T * x0, e, rows, X, x0)
            self.counts["extracted_formulas"] += 1
        branch = self.pieces[key]
        assert branch.contains(a) and tuple(branch.X * a + branch.x0) == x
        image = self.T * sp.Matrix(x)
        value = self.alpha * scalar(a.T * a) / 2
        value += sum(self.phi(i, v) + self.residual[i] * v for i, v in enumerate(x))
        value -= self.alpha * scalar(a.T * image)
        polynomial = scalar(a.T * branch.H * a) / 2 + scalar(branch.p.T * a) + branch.e
        assert value == polynomial
        assert branch.H * a + branch.p == self.alpha * (a - image)
        self.counts["query_checks"] += 1
        self.cache[point] = value, branch, x
        return self.cache[point]

    def reference(self, noise):
        noise = tuple(noise)
        if noise in self.references:
            return self.references[noise]
        integer_indices = sorted(self.integers)
        best = None
        ranges = [range(int(self.lo[i]), int(self.hi[i]) + 1) for i in integer_indices]
        for labels in product(*ranges):
            x = sp.zeros(self.n, 1)
            for i, z in zip(integer_indices, labels):
                x[i] = z
            image = self.T * x
            constant = sum(self.phi(i, x[i]) + self.residual[i] * x[i] for i in integer_indices)
            constant += sum(c * v for c, v in zip(noise, image)) - self.alpha * scalar(image.T * image) / 2
            choices = [self.data[i] for i in self.continuous]
            for chosen in product(*choices):
                if self.continuous:
                    TC = self.T[:, self.continuous]
                    H = sp.diag(*[piece[2] for piece in chosen]) - self.alpha * TC.T * TC
                    linear = sp.Matrix([piece[3] + self.residual[i] for i, piece in zip(self.continuous, chosen)])
                    linear += TC.T * sp.Matrix(noise) - self.alpha * TC.T * image
                    e = constant + sum(piece[4] for piece in chosen)
                    value, values = box_quadratic_min(H, linear, e, [p[0] for p in chosen], [p[1] for p in chosen])
                    for i, v in zip(self.continuous, values):
                        x[i] = v
                else:
                    value = constant
                candidate = value, tuple(x)
                assert self.original(candidate[1], noise) == value
                if best is None or candidate < best:
                    best = candidate
        assert best is not None
        self.references[noise] = best
        return best


def check_all_active_ties(model):
    """The upper-model bound applies to every active witness, not one choice."""
    point, noise = (Q(0),), (Q(0),)
    value, _, _ = model.inner(point)
    optimum, _ = model.reference(noise)
    checks = 0
    for integer in range(-2, 3):
        for continuous in (Q(-1), Q(-1, 2), Q(0), Q(1, 2), Q(1)):
            x = sp.Matrix([integer, continuous])
            assert sum(model.phi(i, v) for i, v in enumerate(x)) == value
            g = model.alpha * (sp.Matrix(point) - model.T * x)
            assert scalar(g.T * g) <= 2 * model.alpha * (value - optimum)
            for target in (Q(-3, 4), Q(1, 3)):
                actual, _, _ = model.inner((target,))
                bound = value + g[0] * target + model.alpha * target**2 / 2
                assert actual <= bound
            checks += 1
    return checks


def main():
    stats = dict.fromkeys(("cases", "levels", "processed_cells", "exact_closures",
                          "ordinary_prunes", "retained_unresolved", "closure_solved_cases",
                          "same_draw_fallbacks", "facet_image_checks", "singular_image_checks"), 0)
    T = [[Q(1, 2), Q(1, 4), 0], [0, Q(1, 4), Q(1, 2)]]
    quadratic = MixedRecourse("quadratic_mixed", T, 4,
                             [one_piece(-2, 2, 1), one_piece(-1, 1, 1), one_piece(-1, 1, 1)],
                             {0, 1})
    many = MixedRecourse("five_integer_coordinates",
                        [[Q(1, 4), Q(1, 4), 0, Q(-1, 4), 0],
                         [0, Q(1, 4), Q(1, 4), 0, Q(1, 4)]],
                        8, [one_piece(-1, 1, Q(1, 2)) for _ in range(5)], set(range(5)))
    pw = [
        [(-2, 0, Q(1, 2), Q(-1, 4), 0), (0, 2, Q(1, 2), Q(1, 4), 0)],
        [(-1, 0, 0, 0, 0), (0, 1, 1, 0, 0)],
        [(-1, 0, 1, 0, 0), (0, 1, 2, 0, 0)],
    ]
    piecewise = MixedRecourse("piecewise_mixed", T, 4, pw, {0})
    residual = MixedRecourse("piecewise_residual_tilt", T, 4, pw, {0},
                            [Q(1, 8), Q(-1, 4), Q(1, 3)])
    ties = MixedRecourse("affine_integer_and_continuous_ties", [[Q(1, 4), Q(1, 4)]], 4,
                        [one_piece(-2, 2, 0), one_piece(-1, 1, 0)], {0})
    for model in (quadratic, many, piecewise, residual):
        for noise in ((Q(0), Q(0)), (Q(1, 2), Q(-1, 3))):
            run(model, noise, 3, stats)
    for noise in ((Q(0),), (Q(1, 2),)):
        run(ties, noise, 3, stats)
    # Explicit integer tie in the kinked convex function.
    piecewise.inner((Q(1, 4), Q(0)))
    active_tie_checks = check_all_active_ties(ties)
    # Binary range size is huge; this diagnostic never enumerates its labels.
    wide = MixedRecourse("binary_encoded_wide_domain", [[Q(1, 2)]], 1,
                        [one_piece(-(2**39), 2**39, 1)], {0})
    _, _, x = wide.inner((Q(13, 7),))
    assert x == (Q(1),) and wide.counts["integer_comparisons"] <= 41
    assert stats["exact_closures"] > 0 and stats["ordinary_prunes"] > 0
    assert stats["closure_solved_cases"] > 0
    print(json.dumps({"status": "passed", **stats,
                      "all_active_tie_checks": active_tie_checks,
                      "wide_domain_integer_comparisons": wide.counts["integer_comparisons"],
                      "fixtures": {model.name: model.counts for model in
                                   (quadratic, many, piecewise, residual, ties)}}, indent=2))


if __name__ == "__main__":
    main()
