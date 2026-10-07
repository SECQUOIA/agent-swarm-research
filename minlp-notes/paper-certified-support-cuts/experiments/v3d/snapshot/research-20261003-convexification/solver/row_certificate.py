"""Exact row elimination and conservative binary64 export.

The caller supplies valid original sides ``h_r(v) + d_r * v <= b_r`` and
a verified support inequality ``a * v + sum(lambda_r * h_r(v)) >= beta``.
Nonnegative multipliers imply ``C * v >= R``, where
``C = a - sum(lambda_r * d_r)`` and ``R = beta - sum(lambda_r * b_r)``.

After rounding C to binary64 Chat, put e = Chat - C.  Valid global bounds
give ``e * v >= m = sum(min(e_i * L_i, e_i * U_i))``.  Therefore Chat * v
is at least R + m; rounding that right-hand side downward preserves validity.
All calculations preceding the final exports use exact rational arithmetic.

This module verifies that implication and binds its inputs.  It does not
verify the nonlinear support, the source expressions, or the supplied global
bounds.  The caller must do so, including for an optional objective epigraph.
An objective epigraph is simply another named variable here.  No finite bounds
are inferred.  A nonzero rounding error at a coordinate with either bound
infinite is conservatively rejected.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from fractions import Fraction
import json
import math
from typing import TypeAlias


ExactNumber: TypeAlias = int | float | Fraction | str
Terms: TypeAlias = Mapping[str, ExactNumber] | Sequence[tuple[str, ExactNumber]]
Bounds: TypeAlias = Mapping[str, tuple[ExactNumber | None, ExactNumber | None]]


@dataclass(frozen=True)
class AffineSide:
    """The affine part and identity of one signed source side h + d*v <= b."""

    source_id: str
    affine_terms: Terms
    rhs: ExactNumber

    def __post_init__(self) -> None:
        terms = self.affine_terms
        if isinstance(terms, Mapping):
            terms = tuple(terms.items())
        else:
            terms = tuple(tuple(term) for term in terms)
        object.__setattr__(self, "affine_terms", terms)


@dataclass(frozen=True)
class RowCertificate:
    """Immutable export; to_dict returns a fresh, ordinary JSON-compatible copy."""

    variables: tuple[str, ...]
    coefficients: tuple[float, ...]
    rhs: float
    _json: str

    def to_dict(self) -> dict:
        return json.loads(self._json)


def _rational(value: ExactNumber, label: str) -> Fraction:
    if isinstance(value, bool):
        raise ValueError(f"{label} must be an exact number, not bool")
    if isinstance(value, Fraction):
        return value
    if isinstance(value, int):
        return Fraction(value)
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError(f"{label} must be finite")
        return Fraction(value)
    if isinstance(value, str):
        try:
            return Fraction(value)
        except (ValueError, ZeroDivisionError) as exc:
            raise ValueError(f"{label} must be a finite rational") from exc
    raise ValueError(f"{label} has unsupported number type {type(value).__name__}")


def _finite_float(value: Fraction, label: str) -> float:
    try:
        result = float(value)
    except (ValueError, OverflowError) as exc:
        raise ValueError(f"{label} cannot be exported as finite binary64") from exc
    if not math.isfinite(result):
        raise ValueError(f"{label} cannot be exported as finite binary64")
    return 0.0 if result == 0.0 else result


def _binary64_exact(value: Fraction, label: str) -> Fraction:
    exported = _finite_float(value, label)
    if Fraction(exported) != value:
        raise ValueError(f"{label} must be exactly representable as binary64")
    return value


def _downward(value: Fraction) -> float:
    result = _finite_float(value, "compensated right-hand side")
    if Fraction(result) > value:
        result = math.nextafter(result, -math.inf)
    if not math.isfinite(result):
        raise ValueError("right-hand side has no finite downward binary64 export")
    return 0.0 if result == 0.0 else result


def _bound(value: ExactNumber | None, *, lower: bool, label: str) -> Fraction | None:
    if value is None:
        return None
    infinity = -math.inf if lower else math.inf
    if isinstance(value, float) and value == infinity:
        return None
    if isinstance(value, str) and value.strip().lower() in (
        {"-inf", "-infinity"} if lower else {"inf", "+inf", "infinity", "+infinity"}
    ):
        return None
    return _rational(value, label)


def _terms(terms: Terms, positions: dict[str, int], label: str) -> tuple[list, list[Fraction]]:
    raw = terms.items() if isinstance(terms, Mapping) else terms
    recorded = []
    combined = [Fraction(0) for _ in positions]
    for term in raw:
        if not isinstance(term, (tuple, list)) or len(term) != 2:
            raise ValueError(f"{label} terms must be (variable, coefficient) pairs")
        name, value = term
        if not isinstance(name, str) or name not in positions:
            raise ValueError(f"{label} contains an unknown variable {name!r}")
        coefficient = _rational(value, f"{label}[{name}]")
        recorded.append([name, str(coefficient)])
        combined[positions[name]] += coefficient
    return recorded, combined


def _canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def certify_row_combination(
    *,
    variables: Sequence[str],
    bounds: Bounds,
    linear_terms: Terms,
    multipliers: Sequence[ExactNumber],
    support_rhs: ExactNumber,
    sides: Sequence[AffineSide],
    support_id: str = "",
) -> RowCertificate:
    """Eliminate source sides and certify the actual exported binary64 row.

    Floats denote their exact binary64 rational values, never their printed
    decimal approximations.  Strings and Fractions denote exact rationals.
    The combined support linear coefficients and each multiplier must already
    be binary64-exact; they must match the separately verified support input.
    Duplicate affine terms are accumulated exactly before coefficient export.
    All bounds and source data are retained in the certificate binding.

    Raise ValueError when an input is malformed, a binary64 export overflows,
    or a rounding discrepancy lacks finite bounds on its coordinate.
    """
    names = tuple(variables)
    if any(not isinstance(name, str) or not name for name in names):
        raise ValueError("variables must have nonempty string names")
    if len(set(names)) != len(names):
        raise ValueError("variable names must be unique")
    if set(bounds) != set(names):
        raise ValueError("bounds must specify exactly the named variables")
    if not isinstance(support_id, str):
        raise ValueError("support_id must be a string")
    positions = {name: index for index, name in enumerate(names)}
    exact_bounds = []
    for name in names:
        interval = bounds[name]
        if not isinstance(interval, (tuple, list)) or len(interval) != 2:
            raise ValueError(f"bounds[{name}] must be a (lower, upper) pair")
        lo = _bound(interval[0], lower=True, label=f"lower bound for {name}")
        hi = _bound(interval[1], lower=False, label=f"upper bound for {name}")
        if lo is not None and hi is not None and lo > hi:
            raise ValueError(f"bounds[{name}] has lower > upper")
        exact_bounds.append((lo, hi))

    _, a = _terms(linear_terms, positions, "support linear")
    a = [_binary64_exact(value, f"support linear coefficient {name}") for name, value in zip(names, a)]
    beta = _rational(support_rhs, "support_rhs")
    if len(multipliers) != len(sides):
        raise ValueError("one multiplier is required per source side")
    lambdas = []
    for index, value in enumerate(multipliers):
        exact = _binary64_exact(_rational(value, f"multiplier {index}"), f"multiplier {index}")
        if exact < 0:
            raise ValueError("multipliers must be nonnegative")
        lambdas.append(exact)

    coefficients = a.copy()
    rhs = beta
    recorded_sides = []
    for side, multiplier in zip(sides, lambdas):
        if not isinstance(side, AffineSide):
            raise ValueError("each side must be an AffineSide")
        if not isinstance(side.source_id, str) or not side.source_id:
            raise ValueError("source sides require nonempty string source_id values")
        raw_terms, d = _terms(side.affine_terms, positions, f"side {side.source_id}")
        b = _rational(side.rhs, f"side {side.source_id} rhs")
        recorded_sides.append({"source_id": side.source_id, "affine_terms": raw_terms, "rhs": str(b)})
        coefficients = [c - multiplier * affine for c, affine in zip(coefficients, d)]
        rhs -= multiplier * b

    exported = tuple(_finite_float(c, f"coefficient {name}") for name, c in zip(names, coefficients))
    errors = [Fraction(actual) - exact for actual, exact in zip(exported, coefficients)]
    compensation = Fraction(0)
    for name, error, (lo, hi) in zip(names, errors, exact_bounds):
        if error == 0:
            continue
        if lo is None or hi is None:
            raise ValueError(f"rounding discrepancy at unbounded variable {name}")
        compensation += min(error * lo, error * hi)
    compensated_rhs = rhs + compensation
    exported_rhs = _downward(compensated_rhs)
    record = {
        "schema": "native-row-combination-v1",
        "binding": {
            "variables": list(names),
            "bounds": [["-inf" if lo is None else str(lo), "inf" if hi is None else str(hi)] for lo, hi in exact_bounds],
            "support": {
                "support_id": support_id,
                "linear_coefficients": list(map(str, a)),
                "multipliers": list(map(str, lambdas)),
                "rhs": str(beta),
            },
            "sides": recorded_sides,
        },
        "exact": {
            "coefficients": list(map(str, coefficients)),
            "eliminated_rhs": str(rhs),
            "rounding_errors": list(map(str, errors)),
            "box_compensation": str(compensation),
            "compensated_rhs": str(compensated_rhs),
        },
        "exported": {"coefficients": list(exported), "rhs": exported_rhs, "orientation": ">="},
    }
    return RowCertificate(names, exported, exported_rhs, _canonical_json(record))


def replay_row_certificate(certificate: RowCertificate | dict, **trusted_problem) -> bool:
    """Recompute elimination and rounding against independently supplied inputs.

    The keyword arguments are exactly those of certify_row_combination.  A
    certificate cannot choose its own trusted source sides, support, or bounds.
    Replay shares the exact arithmetic implementation with the constructor;
    it is not an independent proof of that implementation's correctness.
    """
    try:
        expected = certify_row_combination(**trusted_problem)
        if isinstance(certificate, RowCertificate):
            if (certificate.variables, certificate.coefficients, certificate.rhs) != (
                expected.variables, expected.coefficients, expected.rhs
            ):
                return False
            supplied = certificate.to_dict()
        elif isinstance(certificate, dict):
            supplied = certificate
        else:
            return False
        return _canonical_json(supplied) == expected._json
    except (ValueError, TypeError, OverflowError, KeyError):
        return False
