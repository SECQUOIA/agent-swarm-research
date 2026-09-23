"""Exact rational certificates for piecewise constant affine ODE supports.

For each slab, the supplied affine field is ``B @ ell + A @ p + d``.
``B`` must be Metzler, and the initial coefficients and parameter box are
exact rationals. The caller establishes that these fields are valid lower
supports for its original ODE. No reference trajectory enters this module.

All coefficient matrices have parameter columns first and a constant last.
Only the optional diagnostics use floating point or third-party packages.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import json
from typing import Iterable, Sequence


Rational = int | str | Fraction
Matrix = tuple[tuple[Fraction, ...], ...]


def _rational(value: Rational) -> Fraction:
    if isinstance(value, bool) or not isinstance(value, (int, str, Fraction)):
        raise TypeError("Use int, str or Fraction for exact rational input")
    return Fraction(value)


def _matrix(values: Sequence[Sequence[Rational]], rows: int, cols: int,
            name: str) -> Matrix:
    result = tuple(tuple(_rational(x) for x in row) for row in values)
    if len(result) != rows or any(len(row) != cols for row in result):
        raise ValueError(f"{name} must have shape ({rows}, {cols})")
    return result


def _norm(matrix: Matrix) -> Fraction:
    """Induced infinity norm: largest absolute row sum."""
    return max((sum(map(abs, row), Fraction(0)) for row in matrix),
               default=Fraction(0))


def _multiply(left: Matrix, right: Matrix) -> Matrix:
    columns = tuple(zip(*right))
    return tuple(tuple(sum((x * y for x, y in zip(row, col)), Fraction(0))
                       for col in columns) for row in left)


def _ceil(value: Fraction) -> int:
    return -((-value.numerator) // value.denominator)


def _round_matrix(matrix: Matrix, denominator: int) -> Matrix:
    def nearest(value):
        scaled = value * denominator + Fraction(1, 2)
        return Fraction(scaled.numerator // scaled.denominator, denominator)
    return tuple(tuple(nearest(x) for x in row) for row in matrix)


def _taylor(matrix: Matrix, order: int) -> tuple[Matrix, Fraction]:
    """Return the order-K exponential polynomial and a rational norm bound."""
    size = len(matrix)
    q = _norm(matrix)
    if q >= order + 2:
        raise ValueError("Taylor order must satisfy order + 2 > ||h M||_inf; "
                         "increase order or subdivide the slab")
    term = tuple(tuple(Fraction(i == j) for j in range(size))
                 for i in range(size))
    result = term
    for k in range(1, order + 1):
        product = _multiply(term, matrix)
        term = tuple(tuple(x / k for x in row) for row in product)
        result = tuple(tuple(x + y for x, y in zip(row, addition))
                       for row, addition in zip(result, term))
    # Use the exact first omitted matrix term. Its norm can be much smaller
    # than q**(order+1)/(order+1)!, and detects finite nilpotent expansions.
    next_term = tuple(tuple(x / (order + 1) for x in row)
                      for row in _multiply(term, matrix))
    tail = _norm(next_term) / (1 - q / (order + 2))
    return result, tail


@dataclass(frozen=True)
class Slab:
    duration: Rational
    B: Sequence[Sequence[Rational]]
    A: Sequence[Sequence[Rational]]
    d: Sequence[Rational]


@dataclass(frozen=True)
class SlabRecord:
    duration: Fraction
    scaled_matrix_norm: Fraction
    taylor_tail: Fraction
    rounding_error: Fraction
    coefficient_error: Fraction


@dataclass(frozen=True)
class FlowCertificate:
    approximate: Matrix
    lower: Matrix
    coefficient_error: Fraction
    evaluation_error: Fraction
    parameter_box: tuple[tuple[Fraction, Fraction], ...]
    order: int
    grid_denominator: int
    slabs: tuple[SlabRecord, ...]

    def evaluate(self, parameters: Sequence[Rational]) -> tuple[Fraction, ...]:
        """Evaluate the certified lower affine functions inside their box."""
        p = tuple(_rational(x) for x in parameters)
        if len(p) != len(self.parameter_box):
            raise ValueError("Parameter dimension does not match the box")
        if any(not lo <= x <= hi
               for x, (lo, hi) in zip(p, self.parameter_box)):
            raise ValueError("Parameters must lie inside the certified box")
        vector = p + (Fraction(1),)
        return tuple(sum((a * x for a, x in zip(row, vector)), Fraction(0))
                     for row in self.lower)


def certify_affine_flow(
    slabs: Iterable[Slab],
    initial: Sequence[Sequence[Rational]],
    parameter_box: Sequence[Sequence[Rational]],
    *,
    order: int = 18,
    grid_denominator: int = 10**12,
) -> FlowCertificate:
    """Enclose exact affine-flow coefficients and return a lower affine cut.

    The exact initial affine coefficients are supplied in ``initial``.
    The error bound concerns only integration of the supplied affine fields;
    it cannot establish their validity as supports of another vector field.
    Floating-point inputs are rejected. Convert rounded source coefficients
    with an independently justified support correction before calling this.

    ``coefficient_error`` bounds the induced infinity norm of the difference
    between ``approximate`` and the exact final coefficient matrix. The
    constant column of ``lower`` is shifted down by ``evaluation_error``.
    Both coefficient rounding and upward error-bound rounding use the chosen
    grid after every slab, keeping rational denominators controlled.
    """
    if isinstance(order, bool) or not isinstance(order, int) or order < 0:
        raise ValueError("Taylor order must be a nonnegative integer")
    if (isinstance(grid_denominator, bool)
            or not isinstance(grid_denominator, int) or grid_denominator < 1):
        raise ValueError("Grid denominator must be a positive integer")
    box = tuple(tuple(_rational(x) for x in pair) for pair in parameter_box)
    if any(len(pair) != 2 or pair[0] > pair[1] for pair in box):
        raise ValueError("Each parameter interval must have lower <= upper")
    n = len(initial)
    p = len(box)
    if n == 0:
        raise ValueError("At least one state is required")
    coefficients = _matrix(initial, n, p + 1, "Initial coefficients")
    error = Fraction(0)
    records = []
    bottom = tuple(tuple(Fraction(i == j) for j in range(p + 1))
                   for i in range(p + 1))
    for slab in slabs:
        h = _rational(slab.duration)
        if h < 0:
            raise ValueError("Slab durations must be nonnegative")
        b = _matrix(slab.B, n, n, "B")
        a = _matrix(slab.A, n, p, "A")
        d = tuple(_rational(x) for x in slab.d)
        if len(d) != n:
            raise ValueError("d must have one entry per state")
        if any(b[i][j] < 0 for i in range(n) for j in range(n) if i != j):
            raise ValueError("B must be Metzler (nonnegative off-diagonal)")
        augmented = tuple(tuple(h * x for x in b[i] + a[i] + (d[i],))
                          for i in range(n)) + tuple(
            (Fraction(0),) * (n + p + 1) for _ in range(p + 1))
        taylor, tail = _taylor(augmented, order)
        top_left = tuple(row[:n] for row in taylor[:n])
        next_coefficients = _multiply(taylor[:n], coefficients + bottom)
        rounded = _round_matrix(next_coefficients, grid_denominator)
        rounding_error = _norm(tuple(
            tuple(x - y for x, y in zip(exact_row, rounded_row))
            for exact_row, rounded_row in zip(next_coefficients, rounded)))
        # Bottom rows of the augmented coefficient matrix are exact identity.
        error = (_norm(top_left) * error
                 + tail * (max(_norm(coefficients), Fraction(1)) + error)
                 + rounding_error)
        error = Fraction(_ceil(error * grid_denominator), grid_denominator)
        coefficients = rounded
        records.append(SlabRecord(h, _norm(augmented), tail,
                                  rounding_error, error))
    scale = max((abs(x) for pair in box for x in pair), default=Fraction(1))
    evaluation_error = error * max(Fraction(1), scale)
    lower = tuple(row[:-1] + (row[-1] - evaluation_error,)
                  for row in coefficients)
    return FlowCertificate(coefficients, lower, error, evaluation_error, box,
                           order, grid_denominator, tuple(records))


def _diagnostics() -> dict:
    """Exact scalar tests plus explicitly non-certifying SciPy diagnostics."""
    from math import factorial
    from time import perf_counter

    import numpy as np
    from scipy.linalg import expm

    start = perf_counter()
    # For ell' = ell + 2p + 3, ell(0) = p + 1, the final coefficients
    # are (3e - 2, 4e - 3). Bound e independently by a longer scalar series.
    certificate = certify_affine_flow([Slab(1, [[1]], [[2]], [3])],
                                      [[1, 1]], [[-2, 3]], order=35)
    e_lower = sum((Fraction(1, factorial(k)) for k in range(61)), Fraction(0))
    e_upper = e_lower + Fraction(1, factorial(61)) / (1 - Fraction(1, 62))
    target_intervals = ((3 * e_lower - 2, 3 * e_upper - 2),
                        (4 * e_lower - 3, 4 * e_upper - 3))
    row_error_upper = sum(max(abs(value - lo), abs(value - hi))
                          for value, (lo, hi) in zip(
                              certificate.approximate[0], target_intervals))
    assert row_error_upper <= certificate.coefficient_error
    for p in (-2, 0, 3):
        multiplier = 3 * p + 4
        exact_lower = (multiplier * (e_lower if multiplier >= 0 else e_upper)
                       - 2 * p - 3)
        assert certificate.evaluate([p])[0] <= exact_lower

    # Nilpotent forcing flow is represented exactly when it lies on the grid.
    exact = certify_affine_flow([Slab(2, [[0]], [[3]], [4])], [[1, 2]], [[0, 1]])
    assert exact.approximate == ((Fraction(7), Fraction(10)),)
    assert exact.coefficient_error == 0 and exact.evaluate([1])[0] == 17
    empty = certify_affine_flow([], [["1/3"]], [])
    assert empty.coefficient_error == 0 and empty.evaluate([]) == (Fraction(1, 3),)
    zero = certify_affine_flow([Slab(0, [[-1]], [[]], [2])], [["1/3"]], [],
                               grid_denominator=10)
    assert abs(zero.approximate[0][0] - Fraction(1, 3)) <= zero.coefficient_error

    rng = np.random.default_rng(7811)
    trials = 60
    max_ratio = 0.0
    for trial in range(trials):
        n, p = 1 + trial % 4, trial % 3
        initial = [[Fraction(int(rng.integers(-8, 9)), 5)
                    for _ in range(p + 1)] for _ in range(n)]
        slabs = []
        numerical = np.array(initial, dtype=float)
        for _ in range(1 + trial % 5):
            b = [[Fraction(int(rng.integers(-4, 5) if i == j
                                  else rng.integers(0, 5)), 5)
                  for j in range(n)] for i in range(n)]
            a = [[Fraction(int(rng.integers(-4, 5)), 5) for _ in range(p)]
                 for _ in range(n)]
            d = [Fraction(int(rng.integers(-4, 5)), 5) for _ in range(n)]
            h = Fraction(int(rng.integers(1, 5)), 10)
            slabs.append(Slab(h, b, a, d))
            m = np.zeros((n + p + 1, n + p + 1))
            m[:n] = np.array([b[i] + a[i] + [d[i]] for i in range(n)], dtype=float)
            numerical = (expm(float(h) * m)
                         @ np.vstack((numerical, np.eye(p + 1))))[:n]
        checked = certify_affine_flow(slabs, initial, [[-2, 3]] * p,
                                      order=18, grid_denominator=10**10)
        observed = np.max(np.abs(numerical - np.array(checked.approximate, dtype=float))
                          .sum(axis=1))
        bound = float(checked.coefficient_error)
        # This check allows floating-point noise and is only diagnostic.
        assert observed <= bound + 2e-13 * max(1, np.max(np.abs(numerical)))
        if bound:
            max_ratio = max(max_ratio, observed / bound)

    invalid = 0
    for thunk in (
        lambda: certify_affine_flow([], [[0.1]], []),
        lambda: certify_affine_flow([], [[0]], [[2, 1]]),
        lambda: certify_affine_flow([Slab(-1, [[0]], [[]], [0])], [[0]], []),
        lambda: certify_affine_flow([Slab(1, [[0, -1], [0, 0]], [[], []], [0, 0])],
                                    [[0], [0]], []),
        lambda: certify_affine_flow([Slab(10, [[1]], [[]], [0])], [[1]], [], order=2),
        lambda: certificate.evaluate([4]),
    ):
        try:
            thunk()
        except (ValueError, TypeError):
            invalid += 1
        else:
            raise AssertionError("Malformed input was accepted")
    return {"exact_scalar_interval_test": "passed", "random_expm_diagnostics": trials,
            "max_observed_error_over_bound": max_ratio,
            "invalid_inputs_rejected": invalid,
            "scalar_coefficient_error": str(certificate.coefficient_error),
            "elapsed_seconds": perf_counter() - start}


if __name__ == "__main__":
    print(json.dumps(_diagnostics(), indent=2))
