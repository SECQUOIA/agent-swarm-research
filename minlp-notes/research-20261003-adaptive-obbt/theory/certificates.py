"""Exact witness checks for a fixed rational, lifted McCormick LP family.

Floating point LP solves may propose witnesses. Only rational row checks issue
certificates. These utilities do not certify native solver rows or choose an
optimal runtime policy. See remaining-benefit.md for their precise contracts.
"""

from dataclasses import dataclass
from fractions import Fraction
from math import isfinite
from typing import Callable, Iterable, Sequence


Q = Fraction


def rational(value):
    """Read intended exact data; floating point belongs only in proposals."""
    if isinstance(value, float):
        raise TypeError("Use an integer, Fraction, or rational string for exact data")
    return Q(value)


def vector(values):
    return tuple(rational(value) for value in values)


def dot(left, right):
    if len(left) != len(right):
        raise ValueError("Vector dimensions differ")
    return sum((a * b for a, b in zip(left, right)), Q(0))


@dataclass(frozen=True)
class Box:
    lower: tuple
    upper: tuple

    def __post_init__(self):
        object.__setattr__(self, "lower", vector(self.lower))
        object.__setattr__(self, "upper", vector(self.upper))
        if not self.lower or len(self.lower) != len(self.upper):
            raise ValueError("A box needs equally sized, nonempty endpoints")
        if any(a > b for a, b in zip(self.lower, self.upper)):
            raise ValueError("Empty box")

    def contains(self, other):
        return len(self.lower) == len(other.lower) and all(
            lo <= clo <= chi <= hi
            for lo, hi, clo, chi in zip(
                self.lower, self.upper, other.lower, other.upper
            )
        )


@dataclass(frozen=True)
class Row:
    """One exact inequality coefficients @ point <= rhs."""

    coefficients: tuple
    rhs: Q

    def __post_init__(self):
        object.__setattr__(self, "coefficients", vector(self.coefficients))
        object.__setattr__(self, "rhs", rational(self.rhs))

    def holds(self, point):
        return dot(self.coefficients, point) <= self.rhs


@dataclass(frozen=True)
class Model:
    """Linear rows and objective in (x, w), with w_k = x_i*x_j relaxed.

    Rows are fixed throughout the certificate's lifetime; each listed product
    adds one auxiliary variable. Repeated indices implement the finite LP
    relaxation of a square, not its exact convex epigraph. Integer restrictions
    are not enforced by this LP checker. The caller establishes row validity
    and node-local scope; equality of Model data is not a provenance proof.
    """

    n: int
    products: tuple
    rows: tuple
    objective: tuple
    objective_constant: Q = Q(0)

    def __post_init__(self):
        object.__setattr__(self, "products", tuple(tuple(p) for p in self.products))
        object.__setattr__(self, "rows", tuple(self.rows))
        object.__setattr__(self, "objective", vector(self.objective))
        object.__setattr__(self, "objective_constant", rational(self.objective_constant))
        if self.n < 1 or any(
            len(p) != 2 or any(not isinstance(i, int) or not 0 <= i < self.n for i in p)
            for p in self.products
        ):
            raise ValueError("Invalid original-variable dimension or product")
        if len(self.objective) != self.dimension or any(
            len(row.coefficients) != self.dimension for row in self.rows
        ):
            raise ValueError("Lifted row/objective dimension mismatch")

    @property
    def dimension(self):
        return self.n + len(self.products)

    def value(self, point):
        return self.objective_constant + dot(self.objective, point)

    def relaxation_rows(self, box, cutoff=None):
        if len(box.lower) != self.n:
            raise ValueError("Box dimension mismatch")
        rows = list(self.rows)

        def append(entries, rhs):
            coefficients = [Q(0)] * self.dimension
            for index, value in entries:
                coefficients[index] += value
            rows.append(Row(tuple(coefficients), rhs))

        for i, (lo, hi) in enumerate(zip(box.lower, box.upper)):
            append(((i, -1),), -lo)
            append(((i, 1),), hi)
        for k, (i, j) in enumerate(self.products, self.n):
            li, ui = box.lower[i], box.upper[i]
            lj, uj = box.lower[j], box.upper[j]
            append(((i, lj), (j, li), (k, -1)), li * lj)
            append(((i, uj), (j, ui), (k, -1)), ui * uj)
            append(((i, -lj), (j, -ui), (k, 1)), -ui * lj)
            append(((i, -uj), (j, -li), (k, 1)), -li * uj)
        if cutoff is not None:
            rows.append(Row(self.objective, rational(cutoff) - self.objective_constant))
        return tuple(rows)

    def feasible(self, box, point, cutoff=None):
        point = vector(point)
        return len(point) == self.dimension and all(
            row.holds(point) for row in self.relaxation_rows(box, cutoff)
        )


@dataclass(frozen=True)
class ProtectedBox:
    """A certificate belongs to exactly this model and relaxation construction."""

    model: Model
    box: Box
    witnesses: tuple

    def __post_init__(self):
        witnesses = tuple(vector(w) for w in self.witnesses)
        object.__setattr__(self, "witnesses", witnesses)
        if not witnesses or not all(self.model.feasible(self.box, w) for w in witnesses):
            raise ValueError("Need feasible witnesses on the protected box")
        if any(
            min(w[i] for w in witnesses) != lo or max(w[i] for w in witnesses) != hi
            for i, (lo, hi) in enumerate(zip(self.box.lower, self.box.upper))
        ):
            raise ValueError("Witnesses do not attain all protected-box faces")

    @property
    def required_cutoff(self):
        return max(self.model.value(w) for w in self.witnesses)

    @property
    def objective_ceiling(self):
        return min(self.model.value(w) for w in self.witnesses)

    def reusable(self, model, current_box, cutoff):
        return (
            model == self.model
            and current_box.contains(self.box)
            and rational(cutoff) >= self.required_cutoff
        )

    def ceilings(self, model, current_box, cutoff):
        if not self.reusable(model, current_box, cutoff):
            raise ValueError("Certificate is not valid for this model, box, or cutoff")
        return (
            tuple(p - b for p, b in zip(self.box.lower, current_box.lower)),
            tuple(b - p for b, p in zip(current_box.upper, self.box.upper)),
        )


def verify_protected_box(model, outer, candidate, cutoff, witnesses):
    """Issue an all-future-round certificate, or raise ValueError.

    Each witness must be feasible in the relaxation rebuilt on candidate.
    Their original-variable coordinates must attain every candidate face.
    """
    if not outer.contains(candidate):
        raise ValueError("Candidate box must be contained in the current box")
    certificate = ProtectedBox(model, candidate, tuple(witnesses))
    if certificate.required_cutoff > rational(cutoff):
        raise ValueError("A witness exceeds the requested cutoff")
    return certificate


def current_round_ceilings(model, box, cutoff, witnesses):
    """Bound this frozen LP round's coordinate improvements using primals."""
    witnesses = tuple(vector(w) for w in witnesses)
    if not witnesses or not all(model.feasible(box, w, cutoff) for w in witnesses):
        raise ValueError("Need feasible witnesses in the current relaxation")
    return (
        tuple(min(w[i] for w in witnesses) - lo for i, lo in enumerate(box.lower)),
        tuple(hi - max(w[i] for w in witnesses) for i, hi in enumerate(box.upper)),
    )


def mix_for_cutoff(model, box, witness, anchor, cutoff):
    """Adapt a witness by convex mixing in the same frozen relaxation.

    This certifies only the returned point on box. It does not certify a new
    protected box or assert original nonlinear feasibility of either point.
    """
    witness, anchor, cutoff = vector(witness), vector(anchor), rational(cutoff)
    if not model.feasible(box, witness) or not model.feasible(box, anchor, cutoff):
        raise ValueError("Need a feasible witness and an anchor below the cutoff")
    if model.value(witness) <= cutoff:
        return witness
    theta = (cutoff - model.value(anchor)) / (model.value(witness) - model.value(anchor))
    mixed = tuple(a + theta * (w - a) for w, a in zip(witness, anchor))
    if not model.feasible(box, mixed, cutoff):
        raise AssertionError("Exact convexity check failed")
    return mixed


def cutoff_frontier(model, box, witnesses, cutoff):
    """Generate the exact cutoff frontier of a finite convex witness pool.

    Coordinate extrema of conv(witnesses) intersected with the cutoff are
    attained among the returned old points and pairwise mixtures. This costs
    O(k^2) mixtures for k cached points and does not optimize over the whole LP.
    Empty output means only that the cached convex hull misses the cutoff.
    """
    witnesses = tuple(vector(w) for w in witnesses)
    cutoff = rational(cutoff)
    if not all(model.feasible(box, w) for w in witnesses):
        raise ValueError("Every cached witness must pass the current domain rows")
    eligible = [w for w in witnesses if model.value(w) <= cutoff]
    above = [w for w in witnesses if model.value(w) > cutoff]
    points = list(eligible)
    for anchor in eligible:
        if model.value(anchor) < cutoff:
            for witness in above:
                points.append(mix_for_cutoff(model, box, witness, anchor, cutoff))
    return tuple(dict.fromkeys(points))


def scipy_proposal(model, box, cutoff, coordinate, side):
    """Uncertified LP proposal; coordinate=None minimizes the model objective."""
    from scipy.optimize import linprog

    rows = model.relaxation_rows(box, cutoff)
    if coordinate is None:
        objective = [float(value) for value in model.objective]
    else:
        objective = [0.0] * model.dimension
        objective[coordinate] = 1.0 if side == "lower" else -1.0
    result = linprog(
        objective,
        A_ub=[[float(v) for v in row.coefficients] for row in rows],
        b_ub=[float(row.rhs) for row in rows],
        bounds=[(None, None)] * model.dimension,
        method="highs",
    )
    return result.x if result.success else None


def discover_protected_box(
    model, outer, cutoff, proposal_solver: Callable = scipy_proposal,
    max_denominator=10**9, improve_objective=False
):
    """Propose a hull of endpoint LP points, then check self-consistency exactly.

    Returns None when the proposal cannot be certified. No failed proposal
    proves that a protected box does not exist. At most 2*n endpoint calls are
    made; improve_objective requests one additional LP on a certified box.
    Their full cost must be charged to screening. This is not inherently
    cheaper than an OBBT round, and is intended also for already available LP
    points supplied by a callback.
    """
    def recover(point):
        if point is None or len(point) != model.dimension:
            return None
        proposed = []
        for value in point:
            if isinstance(value, (int, Q, str)):
                proposed.append(rational(value))
            else:
                if not isfinite(float(value)):
                    return None
                proposed.append(Q(str(float(value))).limit_denominator(max_denominator))
        return tuple(proposed)

    witnesses = []
    for coordinate in range(model.n):
        for side in ("lower", "upper"):
            proposed = recover(proposal_solver(model, outer, cutoff, coordinate, side))
            if proposed is None:
                return None
            witnesses.append(proposed)
    candidate = Box(
        tuple(min(w[i] for w in witnesses) for i in range(model.n)),
        tuple(max(w[i] for w in witnesses) for i in range(model.n)),
    )
    try:
        certificate = verify_protected_box(model, outer, candidate, cutoff, witnesses)
    except ValueError:
        return None
    if improve_objective:
        proposed = recover(proposal_solver(model, candidate, cutoff, None, "objective"))
        if proposed is not None and model.feasible(candidate, proposed, cutoff):
            certificate = verify_protected_box(model, outer, candidate, cutoff, (*witnesses, proposed))
    return certificate


def check_tail_majorant(matrix: Sequence[Sequence], residual: Iterable, majorant: Iterable):
    """Verify residual + M e <= e exactly; does not establish a Lipschitz M."""
    residual, majorant = vector(residual), vector(majorant)
    matrix = tuple(vector(row) for row in matrix)
    n = len(residual)
    if n == 0 or len(majorant) != n or len(matrix) != n or any(len(row) != n for row in matrix):
        raise ValueError("Tail-bound dimension mismatch")
    if any(value < 0 for value in (*residual, *majorant)) or any(
        value < 0 for row in matrix for value in row
    ):
        return False
    return all(d + dot(row, majorant) <= e for d, row, e in zip(residual, matrix, majorant))
