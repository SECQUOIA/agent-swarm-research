"""Exact interval tubes for polynomial ODEs on a fixed time grid.

Raw tubes pass a strict Picard inclusion test. Valid global state bounds and
affine invariants supplied by PolynomialModel can then contract the tube and
its endpoint. The caller establishes these physical metadata assumptions.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as Q
import json

from extended_rpd import PolynomialModel, rational


Box = tuple[tuple[Q, Q], ...]


@dataclass(frozen=True)
class Interval:
    lower: Q
    upper: Q

    def __post_init__(self):
        object.__setattr__(self, "lower", rational(self.lower))
        object.__setattr__(self, "upper", rational(self.upper))
        if self.lower > self.upper:
            raise ValueError("Interval lower endpoint exceeds upper endpoint")

    @staticmethod
    def convert(value):
        if isinstance(value, Interval):
            return value
        value = rational(value)
        return Interval(value, value)

    def __add__(self, other):
        other = self.convert(other)
        return Interval(self.lower + other.lower, self.upper + other.upper)

    __radd__ = __add__

    def __neg__(self):
        return Interval(-self.upper, -self.lower)

    def __sub__(self, other):
        return self + (-self.convert(other))

    def __rsub__(self, other):
        return self.convert(other) + (-self)

    def __mul__(self, other):
        other = self.convert(other)
        products = (self.lower * other.lower, self.lower * other.upper,
                    self.upper * other.lower, self.upper * other.upper)
        return Interval(min(products), max(products))

    __rmul__ = __mul__

    def magnitude(self):
        return max(abs(self.lower), abs(self.upper))


def _box(intervals) -> Box:
    return tuple((interval.lower, interval.upper) for interval in intervals)


def _intersect(left, right, context):
    lo, hi = max(left.lower, right.lower), min(left.upper, right.upper)
    if lo > hi:
        raise ValueError(f"Empty interval during {context}; check physical metadata")
    return Interval(lo, hi)


def _round_outward(interval, denominator):
    if denominator is None:
        return interval
    lo, hi = interval.lower * denominator, interval.upper * denominator
    return Interval(Q(lo.numerator // lo.denominator, denominator),
                    Q(-((-hi.numerator) // hi.denominator), denominator))


def _rhs(model, parameters, states):
    result = tuple(Interval.convert(value) for value in model.rhs(parameters, states))
    if len(result) != len(states):
        raise ValueError("RHS dimension differs from state dimension")
    return result


def _contract(model, parameters, intervals, row_sweeps):
    """Sound finite Gauss-Seidel interval propagation of A x = b + D p."""
    result = [_intersect(value, Interval(*bound), "physical-box intersection")
              for value, bound in zip(intervals, model.state_box)]
    for _ in range(row_sweeps):
        for row, constant, parameter_row in zip(
                model.invariant_A, model.invariant_b, model.invariant_D):
            right = Interval.convert(constant)
            for coefficient, parameter in zip(parameter_row, parameters):
                right += coefficient * parameter
            for j, divisor in enumerate(row):
                if divisor == 0:
                    continue
                candidate = right
                for k, coefficient in enumerate(row):
                    if k != j:
                        candidate -= coefficient * result[k]
                candidate *= 1 / divisor
                result[j] = _intersect(result[j], candidate, "invariant propagation")
    return tuple(result)


@dataclass(frozen=True)
class TubeSlab:
    start: Q
    duration: Q
    initial: Box
    raw_box: Box
    raw_rhs: Box
    picard_image: Box
    refined_box: Box
    refined_rhs: Box
    endpoint_image: Box
    endpoint: Box
    inflations: int


@dataclass(frozen=True)
class TubeCertificate:
    parameter_box: Box
    physical_box: Box
    initial_coefficients: tuple[tuple[Q, ...], ...]
    invariant_A: tuple[tuple[Q, ...], ...]
    invariant_b: tuple[Q, ...]
    invariant_D: tuple[tuple[Q, ...], ...]
    initial: Box
    duration: Q
    steps: int
    inflation: Q
    margin: Q
    row_sweeps: int
    grid_denominator: int | None
    slabs: tuple[TubeSlab, ...]


class TubeFailure(RuntimeError):
    """The fixed grid failed to produce a tube; carries its last attempt."""

    def __init__(self, slab_index, raw_box, picard_image, max_inflations):
        self.slab_index = slab_index
        self.raw_box = raw_box
        self.picard_image = picard_image
        self.max_inflations = max_inflations
        super().__init__(f"Strict Picard inclusion failed at slab {slab_index} "
                         f"after {max_inflations + 1} attempts; use a finer grid")


def certify_tubes(
    model: PolynomialModel,
    duration,
    steps: int,
    *,
    inflation="1/4",
    margin="1/1000",
    max_inflations: int = 12,
    row_sweeps: int = 2,
    grid_denominator: int | None = 10**12,
) -> TubeCertificate:
    """Certify tubes and endpoints on a fixed uniform time grid.

    The positive ``margin`` is a rate: initial padding is
    ``h*((1+inflation)*magnitude(f(P,Y))+margin)`` in each coordinate.
    Failed coordinates double their padding, up to ``max_inflations`` rounds.
    Coordinates that already satisfy inclusion keep their current padding.
    Physical bounds and affine invariants are used only after a raw tube has
    passed strict inclusion. Their validity is an assumption on the model.

    Endpoints are rounded outward before physical/invariant contraction.
    Set ``grid_denominator=None`` to omit rounding. This preserves exact
    validity but can cause substantial rational-denominator growth.
    """
    duration, inflation, margin = map(rational, (duration, inflation, margin))
    if duration <= 0 or inflation < 0 or margin <= 0:
        raise ValueError("Require positive duration and margin, nonnegative inflation")
    for value, name, minimum in ((steps, "steps", 1),
                                 (max_inflations, "max_inflations", 0),
                                 (row_sweeps, "row_sweeps", 0)):
        if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
            raise ValueError(f"{name} must be an integer >= {minimum}")
    if (grid_denominator is not None
            and (isinstance(grid_denominator, bool)
                 or not isinstance(grid_denominator, int) or grid_denominator < 1)):
        raise ValueError("Grid denominator must be a positive integer or None")
    parameters = tuple(Interval(*pair) for pair in model.parameter_box)
    initial = []
    for row in model.initial:
        value = Interval.convert(row[-1])
        for coefficient, parameter in zip(row[:-1], parameters):
            value += coefficient * parameter
        initial.append(value)
    current = _contract(model, parameters, initial, row_sweeps)
    initial_box = _box(current)
    h = duration / steps
    records = []
    for index in range(steps):
        seed_rhs = _rhs(model, parameters, current)
        radii = tuple(h * ((1 + inflation) * rate.magnitude() + margin)
                      for rate in seed_rhs)
        for attempt in range(max_inflations + 1):
            raw = tuple(Interval(value.lower - radius, value.upper + radius)
                        for value, radius in zip(current, radii))
            raw_rhs = _rhs(model, parameters, raw)
            image = tuple(value + Interval(0, h) * rate
                          for value, rate in zip(current, raw_rhs))
            if all(bound.lower < inner.lower and inner.upper < bound.upper
                   for bound, inner in zip(raw, image)):
                break
            radii = tuple(radius if bound.lower < inner.lower and inner.upper < bound.upper
                          else 2*radius for radius,bound,inner in zip(radii,raw,image))
        else:
            raise TubeFailure(index, _box(raw), _box(image), max_inflations)
        refined = _contract(model, parameters, raw, row_sweeps)
        refined_rhs = _rhs(model, parameters, refined)
        endpoint_image = tuple(value + h * rate
                               for value, rate in zip(current, refined_rhs))
        endpoint = tuple(_round_outward(value, grid_denominator)
                         for value in endpoint_image)
        endpoint = _contract(model, parameters, endpoint, row_sweeps)
        # Intersection with the established tube is also valid at its endpoint.
        endpoint = tuple(_intersect(value, bound, "endpoint/tube intersection")
                         for value, bound in zip(endpoint, refined))
        records.append(TubeSlab(index * h, h, _box(current), _box(raw),
                                _box(raw_rhs), _box(image), _box(refined),
                                _box(refined_rhs), _box(endpoint_image),
                                _box(endpoint), attempt))
        current = endpoint
    return TubeCertificate(model.parameter_box, model.state_box, model.initial,
                           model.invariant_A, model.invariant_b, model.invariant_D, initial_box,
                           duration, steps, inflation, margin, row_sweeps,
                           grid_denominator, tuple(records))


def _diagnostics():
    """Exact inclusion checks, plus non-certifying numerical trajectory checks."""
    from dataclasses import replace
    from time import perf_counter

    import numpy as np
    from scipy.integrate import solve_ivp

    from extended_rpd import dimerization, shift_methanation

    start = perf_counter()
    records = []
    checks = 0
    for name, factory in (("dimerization", dimerization),
                          ("shift_methanation", shift_methanation)):
        model = factory()
        for width in (Q(1), Q(1, 4), Q(0)):
            box = tuple(((lo + hi) / 2 - width * (hi - lo) / 2,
                         (lo + hi) / 2 + width * (hi - lo) / 2)
                        for lo, hi in model.parameter_box)
            narrowed = replace(model, parameter_box=box)
            certificate = certify_tubes(narrowed, Q(1, 2), 50)
            for slab in certificate.slabs:
                assert all(lo < ylo <= yhi < hi
                           for (lo, hi), (ylo, yhi) in zip(slab.raw_box, slab.picard_image))
                assert all(lo <= ylo <= yhi <= hi
                           for (lo, hi), (ylo, yhi) in zip(slab.raw_box, slab.refined_box))
            p = np.array([float((lo + hi) / 2) for lo, hi in box])
            solution = solve_ivp(lambda t, x: narrowed.physical_rhs(p, x),
                                 (0, 0.5), narrowed.initial_state(p),
                                 rtol=1e-11, atol=1e-13, dense_output=True)
            assert solution.success
            for slab in certificate.slabs:
                for t in np.linspace(float(slab.start), float(slab.start + slab.duration), 5):
                    x = solution.sol(t)
                    for value, (lo, hi) in zip(x, slab.refined_box):
                        assert float(lo) - 1e-10 <= value <= float(hi) + 1e-10
                    checks += 1
            records.append({"model": name, "relative_parameter_width": str(width),
                            "final_widths": [float(hi - lo) for lo, hi in
                                             certificate.slabs[-1].endpoint],
                            "max_inflations": max(s.inflations for s in certificate.slabs)})
    # Exact singleton equilibrium also checks the positive strict-inclusion margin.
    equilibrium = PolynomialModel((), ((Q(-1), Q(1)),), lambda p, x: [0], ((Q(0),),))
    checked = certify_tubes(equilibrium, 1, 3, grid_denominator=None)
    assert all(s.endpoint == ((Q(0), Q(0)),) for s in checked.slabs)
    # A deliberately coarse step must fail explicitly instead of issuing a tube.
    explosive = PolynomialModel((), ((Q(-100), Q(100)),),
                                lambda p, x: [x[0] * x[0]], ((Q(1),),))
    try:
        certify_tubes(explosive, 1, 1, max_inflations=3)
    except TubeFailure as failure:
        assert failure.slab_index == 0 and failure.max_inflations == 3
    else:
        raise AssertionError("A nonexisting-horizon solution received a tube")
    return {"exact_inclusion_slabs": 300, "trajectory_sample_checks": checks,
            "cases": records, "equilibrium_check": "passed",
            "explicit_failure_check": "passed", "elapsed_seconds": perf_counter() - start}


if __name__ == "__main__":
    print(json.dumps(_diagnostics(), indent=2))
