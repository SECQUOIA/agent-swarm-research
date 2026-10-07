"""Exact upper bounds on normalized block-cut violation from graph samples.

No optimizer is trusted here.  Proposed weights are made into an exact convex
combination of domain-checked graph points.  A small certified residual permits
skipping support separation at that query.  A large residual proves nothing.

The evaluator passed to SampleCache is part of the trusted graph definition:
it must return enclosures of the ORIGINAL graph at exact rational arguments.
Use replay_screen with that original evaluator to check serialized evidence.
"""

from dataclasses import dataclass, field
from fractions import Fraction
import math


SCHEMA = "graph-hull-distance-screen-v1"


def rational(value):
    """Interpret finite inputs exactly, including binary floating-point inputs."""
    if isinstance(value, bool):
        raise ValueError("boolean is not a rational scalar")
    try:
        return Fraction(value)
    except (TypeError, ValueError, ZeroDivisionError, OverflowError) as exc:
        raise ValueError("expected a finite rational scalar") from exc


@dataclass(frozen=True)
class Interval:
    lower: Fraction
    upper: Fraction

    def __post_init__(self):
        object.__setattr__(self, "lower", rational(self.lower))
        object.__setattr__(self, "upper", rational(self.upper))
        if self.lower > self.upper:
            raise ValueError("reversed feature enclosure")


def _interval(value):
    if isinstance(value, Interval):
        return value
    if isinstance(value, (tuple, list)):
        if len(value) != 2:
            raise ValueError("feature enclosure must have two endpoints")
        return Interval(*value)
    return Interval(value, value)


def _domain(bounds, rows):
    bounds = tuple(tuple(rational(v) for v in pair) for pair in bounds)
    if not bounds or any(len(pair) != 2 or pair[0] > pair[1] for pair in bounds):
        raise ValueError("expected nonempty finite ordered variable bounds")
    rows = tuple(tuple(rational(v) for v in row) for row in rows)
    if any(len(row) != len(bounds) + 1 for row in rows):
        raise ValueError("affine row must contain variable coefficients and rhs")
    return bounds, rows


@dataclass(frozen=True)
class BoundSamples:
    """Immutable in-process result of SampleCache.bind; not serialized trust."""

    bounds: tuple
    rows: tuple
    points: tuple
    values: tuple


class SampleCache:
    """Cache trusted evaluations after exact box and affine-row feasibility.

    Rows mean sum(row[j] * point[j]) <= row[-1].  Supply an equality as two
    opposite inequalities.  The fixed domain must contain only restrictions
    checked here; additional nonlinear restrictions need their own certified
    feasibility check in evaluate, which must reject infeasible arguments.
    Do not reuse a cache after changing the graph or shrinking its domain.
    """

    def __init__(self, *, bounds, evaluate, rows=()):
        self.bounds, self.rows = _domain(bounds, rows)
        if not callable(evaluate):
            raise ValueError("evaluate must be a trusted graph enclosure callable")
        self._evaluate = evaluate
        self._values = {}
        self._dimension = None

    def bind(self, sample_points):
        points, values = [], []
        for raw_point in sample_points:
            point = tuple(rational(v) for v in raw_point)
            if len(point) != len(self.bounds):
                raise ValueError("sample has wrong parameter dimension")
            if not all(lo <= v <= hi for v, (lo, hi) in zip(point, self.bounds)):
                raise ValueError("sample lies outside original graph box")
            if any(
                sum(a * v for a, v in zip(row[:-1], point)) > row[-1]
                for row in self.rows
            ):
                raise ValueError("sample violates an original graph affine row")
            if point not in self._values:
                enclosure = tuple(_interval(v) for v in self._evaluate(point))
                if not enclosure:
                    raise ValueError("graph must have at least one coordinate")
                if self._dimension is not None and len(enclosure) != self._dimension:
                    raise ValueError("graph evaluator changed output dimension")
                self._dimension = len(enclosure)
                self._values[point] = enclosure
            points.append(point)
            values.append(self._values[point])
        if not points:
            raise ValueError("at least one feasible graph sample is required")
        return BoundSamples(self.bounds, self.rows, tuple(points), tuple(values))


def bind_samples(sample_points, *, bounds, evaluate, rows=()):
    """Bind a one-off sample set; use SampleCache for repeated or growing sets."""
    return SampleCache(bounds=bounds, evaluate=evaluate, rows=rows).bind(sample_points)


def normalize_weights(proposed_weights):
    """Clip finite negative proposals to zero, then normalize exactly.

    Clipping repairs floating-point simplex noise but needs no tolerance:
    even inaccurate proposals produce a valid, possibly weak witness.  An
    all-nonpositive vector has no witness and is rejected.
    """
    weights = tuple(max(Fraction(0), rational(v)) for v in proposed_weights)
    total = sum(weights, Fraction(0))
    if total <= 0:
        raise ValueError("weight proposal has no positive mass")
    return tuple(w / total for w in weights)


@dataclass(frozen=True)
class ScreenCertificate:
    samples: BoundSamples = field(repr=False)
    query: tuple
    scales: tuple
    weights: tuple
    combination: tuple
    norm: str
    upper_bound: Fraction
    threshold: Fraction

    @property
    def can_skip(self):
        return self.upper_bound <= self.threshold

    def to_dict(self):
        """Serialize evidence only when needed, avoiding callback-time copies."""
        return {
            "schema": SCHEMA,
            "bounds": [[str(v) for v in pair] for pair in self.samples.bounds],
            "rows": [[str(v) for v in row] for row in self.samples.rows],
            "samples": [
                {
                    "point": [str(v) for v in point],
                    "values": [[str(v.lower), str(v.upper)] for v in values],
                }
                for point, values in zip(self.samples.points, self.samples.values)
            ],
            "query": [str(v) for v in self.query],
            "scales": [str(v) for v in self.scales],
            "weights": [str(v) for v in self.weights],
            "combination": [[str(v.lower), str(v.upper)] for v in self.combination],
            "norm": self.norm,
            "upper_bound": str(self.upper_bound),
            "threshold": str(self.threshold),
            "can_skip": self.can_skip,
        }


def screen_convex_combination(query, samples, proposed_weights, *, scales=None, threshold=0, norm="inf"):
    """Bound distance to the graph hull in a scaled L-infinity or L1 norm.

    Only samples returned by bind_samples/SampleCache.bind are trusted inputs.
    Scales and the threshold are interpreted as their exact input values.
    With norm="inf", can_skip rules out violation STRICTLY GREATER than
    threshold for normals with sum_j scales[j] * abs(normal[j]) <= 1.
    With norm="1", the condition is max_j scales[j] * abs(normal[j]) <= 1,
    matching a direction LP with each scaled coefficient in [-1, 1].
    It is not a hull-membership decision unless the bound is exactly zero.
    """
    if not isinstance(samples, BoundSamples):
        raise ValueError("samples must be bound to the original graph")
    query = tuple(rational(v) for v in query)
    if not query or len(query) != len(samples.values[0]):
        raise ValueError("query has wrong graph dimension")
    scales = tuple(rational(v) for v in scales) if scales is not None else (Fraction(1),) * len(query)
    if len(scales) != len(query) or any(s <= 0 for s in scales):
        raise ValueError("coordinate scales must be positive and match graph dimension")
    threshold = rational(threshold)
    if threshold < 0:
        raise ValueError("threshold must be nonnegative")
    if norm not in ("inf", "1"):
        raise ValueError("norm must be 'inf' or '1'")
    weights = normalize_weights(proposed_weights)
    if len(weights) != len(samples.points):
        raise ValueError("one proposed weight is required per graph sample")
    combination = tuple(
        Interval(
            sum((w * values[j].lower for w, values in zip(weights, samples.values)), Fraction(0)),
            sum((w * values[j].upper for w, values in zip(weights, samples.values)), Fraction(0)),
        )
        for j in range(len(query))
    )
    residuals = tuple(
        max(abs(p - v.lower), abs(p - v.upper)) / s
        for p, v, s in zip(query, combination, scales)
    )
    upper_bound = max(residuals) if norm == "inf" else sum(residuals, Fraction(0))
    return ScreenCertificate(samples, query, scales, weights, combination, norm, upper_bound, threshold)


def replay_screen(query, certificate, *, bounds, evaluate, rows=(), scales=None, threshold=0, norm="inf"):
    """Recompute all evidence against trusted original graph, query and policy.

    Cached or serialized sample enclosures are never trusted by this path.
    Invalid data and infeasible witnesses return False.  Other evaluator
    failures propagate: they are not evidence for skipping separation.
    """
    try:
        if not isinstance(certificate, dict) or certificate.get("schema") != SCHEMA:
            return False
        samples = bind_samples(
            [sample["point"] for sample in certificate["samples"]],
            bounds=bounds,
            rows=rows,
            evaluate=evaluate,
        )
        expected = screen_convex_combination(
            query, samples, certificate["weights"], scales=scales, threshold=threshold, norm=norm
        ).to_dict()
        return certificate == expected
    except (TypeError, ValueError, KeyError, IndexError, ZeroDivisionError, OverflowError):
        return False


def upper_float(value):
    """Round a nonnegative exact bound outward for logging or numerical APIs.

    The exact Fraction comparison in can_skip remains the preferred decision.
    Overflow yields +infinity, which cannot cause an unsafe skip.
    """
    value = rational(value)
    if value < 0:
        raise ValueError("bound must be nonnegative")
    try:
        result = float(value)
    except OverflowError:
        return math.inf
    if math.isfinite(result) and Fraction(result) < value:
        result = math.nextafter(result, math.inf)
    return result
