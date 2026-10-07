"""Exact, replayable bound propagation from original affine constraints.

The input is duck typed as ``uenv.osil.Instance``.  Constraint index ``r`` in
certificates means ``instance.rows[r + 1]``; the objective is never a constraint.
All finite input scalars have their binary64 values interpreted as exact
rationals.  Only rows with no nonlinear tree and no quadratic terms are used.
Returned binary64 bounds are rounded outward, including on overflow/underflow.

Replay establishes validity of the recorded box deductions, not completeness
of propagation or feasibility of the original nonlinear model.  Its trusted
input is the original instance, not a model embedded in the certificate.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import math
from typing import Any


Bound = Fraction | float  # Floats here are only signed infinities.
_SCHEMA = "original-affine-bounds-v1"


@dataclass(frozen=True)
class BoundPropagation:
    lower: tuple[Bound, ...]
    upper: tuple[Bound, ...]
    float_lower: tuple[float, ...]
    float_upper: tuple[float, ...]
    certificate: dict[str, Any]
    infeasible: bool
    status: str


def _input(value: Any) -> Bound:
    value = float(value)
    if math.isnan(value):
        raise ValueError("NaN is not a model scalar")
    return Fraction(value) if math.isfinite(value) else value


def _text(value: Bound) -> str:
    return str(value)


def _outward(value: Bound, *, lower: bool) -> float:
    if not isinstance(value, Fraction):
        return value
    try:
        result = float(value)
    except OverflowError:
        result = math.inf if value > 0 else -math.inf
    if lower and result > value:
        return math.nextafter(result, -math.inf)
    if not lower and result < value:
        return math.nextafter(result, math.inf)
    return result


def _model(instance: Any) -> tuple[list[Bound], list[Bound], list[str], list[dict], dict]:
    lower = [_input(x) for x in instance.var_lb]
    upper = [_input(x) for x in instance.var_ub]
    types = list(instance.var_type)
    if not len(lower) == len(upper) == len(types):
        raise ValueError("inconsistent variable array lengths")
    if any(x == math.inf for x in lower) or any(x == -math.inf for x in upper):
        raise ValueError("lower +inf and upper -inf are not supported model bounds")
    if any(not isinstance(t, str) for t in types):
        raise ValueError("variable types must be strings")
    rows = []
    for index, row in enumerate(instance.rows[1:]):
        if row.get("nl") is not None or row.get("quad"):
            continue
        coefficients = []
        for j, value in row.get("lin", {}).items():
            if type(j) is not int or not 0 <= j < len(lower):
                raise ValueError("invalid affine variable index")
            coefficient = _input(value)
            if not isinstance(coefficient, Fraction):
                raise ValueError("affine coefficients must be finite")
            if coefficient:
                coefficients.append((j, coefficient))
        coefficients.sort()
        lb = _input(row.get("lb") if row.get("lb") is not None else -math.inf)
        ub = _input(row.get("ub") if row.get("ub") is not None else math.inf)
        if lb == math.inf or ub == -math.inf:
            raise ValueError("lower +inf and upper -inf are not supported row bounds")
        rows.append({"row": index, "coefficients": coefficients, "lower": lb, "upper": ub})
    binding = {
        "lower": list(map(_text, lower)), "upper": list(map(_text, upper)), "types": types,
        "rows": [{"row": r["row"],
                  "coefficients": [[j, _text(a)] for j, a in r["coefficients"]],
                  "lower": _text(r["lower"]), "upper": _text(r["upper"])} for r in rows],
    }
    return lower, upper, types, rows, binding


def _sides(row: dict):
    """Yield each finite side in the common form sum a_j x_j <= rhs."""
    if isinstance(row["upper"], Fraction):
        yield "upper", row["coefficients"], row["upper"]
    if isinstance(row["lower"], Fraction):
        yield "lower", [(j, -a) for j, a in row["coefficients"]], -row["lower"]


def _minimum(coefficients, lower, upper, *, exclude=None) -> Fraction | None:
    total = Fraction(0)
    for j, a in coefficients:
        if j == exclude:
            continue
        bound = lower[j] if a > 0 else upper[j]
        if not isinstance(bound, Fraction):
            return None
        total += a * bound
    return total


def _crossed(lower, upper) -> bool:
    return any(lo > hi for lo, hi in zip(lower, upper))


def _type_steps(lower, upper, types, round_integers):
    for j, typ in enumerate(types):
        if typ == "B":
            if lower[j] < 0:
                yield {"kind": "binary", "variable": j, "bound": "lower",
                       "old": _text(lower[j]), "new": "0"}
            if upper[j] > 1:
                yield {"kind": "binary", "variable": j, "bound": "upper",
                       "old": _text(upper[j]), "new": "1"}
        if round_integers and typ in ("B", "I"):
            if isinstance(lower[j], Fraction):
                rounded = Fraction(math.ceil(lower[j]))
                if rounded > lower[j]:
                    yield {"kind": "integer", "variable": j, "bound": "lower",
                           "old": _text(lower[j]), "new": _text(rounded)}
            if isinstance(upper[j], Fraction):
                rounded = Fraction(math.floor(upper[j]))
                if rounded < upper[j]:
                    yield {"kind": "integer", "variable": j, "bound": "upper",
                           "old": _text(upper[j]), "new": _text(rounded)}


def _row_steps(row, lower, upper):
    # This generator deliberately reads the updated box after every yield.
    for side, coefficients, rhs in _sides(row):
        minimum = _minimum(coefficients, lower, upper)
        if minimum is not None and minimum > rhs:
            yield {"kind": "contradiction", "row": row["row"], "side": side,
                   "minimum": _text(minimum), "rhs": _text(rhs)}
            return
        for j, a in coefficients:
            minimum = _minimum(coefficients, lower, upper, exclude=j)
            if minimum is None:
                continue
            candidate = (rhs - minimum) / a
            direction = "upper" if a > 0 else "lower"
            old = upper[j] if a > 0 else lower[j]
            if (a > 0 and candidate < old) or (a < 0 and candidate > old):
                yield {"kind": "affine", "row": row["row"], "side": side,
                       "variable": j, "bound": direction,
                       "old": _text(old), "new": _text(candidate)}


def _apply(step, lower, upper):
    if step["kind"] != "contradiction":
        target = lower if step["bound"] == "lower" else upper
        target[step["variable"]] = Fraction(step["new"])


def _available(lower, upper, types, rows, round_integers) -> bool:
    if next(_type_steps(lower, upper, types, round_integers), None) is not None:
        return True
    return any(next(_row_steps(r, lower, upper), None) is not None for r in rows)


def propagate_bounds(instance: Any, *, max_passes: int = 8, max_steps: int = 10000,
                     round_integers: bool = True) -> BoundPropagation:
    """Tighten a box by exact affine deductions, with bounded passes and steps.

    A budget exit is safe: all completed deductions remain valid.  Infeasibility
    is reported only for an exact contradiction in bounds or affine activity.
    ``max_steps`` includes binary/integer deductions and contradiction records.
    """
    if any(type(v) is not int or v < 0 for v in (max_passes, max_steps)):
        raise ValueError("budgets must be nonnegative integers")
    if type(round_integers) is not bool:
        raise ValueError("round_integers must be boolean")
    lower, upper, types, rows, binding = _model(instance)
    steps = []
    infeasible = _crossed(lower, upper)
    exhausted = False
    for _ in range(max_passes):
        if infeasible or exhausted:
            break
        start = len(steps)
        generators = [_type_steps(lower, upper, types, round_integers)]
        generators.extend(_row_steps(row, lower, upper) for row in rows)
        for generator in generators:
            for step in generator:
                if len(steps) >= max_steps:
                    exhausted = True
                    break
                _apply(step, lower, upper)
                steps.append(step)
                infeasible = step["kind"] == "contradiction" or _crossed(lower, upper)
                if infeasible:
                    break
            if infeasible or exhausted:
                break
        if len(steps) == start:
            break
    status = ("infeasible" if infeasible else
              "budget" if _available(lower, upper, types, rows, round_integers) else "fixed_point")
    float_lower = tuple(_outward(x, lower=True) for x in lower)
    float_upper = tuple(_outward(x, lower=False) for x in upper)
    result = {"lower": list(map(_text, lower)), "upper": list(map(_text, upper)),
              "float_lower": [x.hex() for x in float_lower],
              "float_upper": [x.hex() for x in float_upper],
              "infeasible": infeasible, "status": status}
    certificate = {"schema": _SCHEMA, "binding": binding, "round_integers": round_integers,
                   "steps": steps, "result": result}
    return BoundPropagation(tuple(lower), tuple(upper), float_lower, float_upper,
                            certificate, infeasible, status)


def replay_bounds(instance: Any, certificate: dict) -> bool:
    """Check every deduction against the original instance and preceding box.

    The checker does not rerun the search or trust certificate-provided row
    coefficients.  It recomputes the one bound formula named by each step.
    Invalid, malformed, mismatched, or edited certificates return ``False``.
    """
    try:
        if set(certificate) != {"schema", "binding", "round_integers", "steps", "result"}:
            return False
        if certificate["schema"] != _SCHEMA or type(certificate["round_integers"]) is not bool:
            return False
        lower, upper, types, rows, binding = _model(instance)
        if certificate["binding"] != binding or not isinstance(certificate["steps"], list):
            return False
        rows_by_index = {r["row"]: r for r in rows}
        infeasible = _crossed(lower, upper)
        for step in certificate["steps"]:
            if infeasible or not isinstance(step, dict):
                return False
            kind = step.get("kind")
            if kind in ("affine", "contradiction"):
                if type(step.get("row")) is not int or step["row"] not in rows_by_index:
                    return False
                row = rows_by_index[step["row"]]
                sides = {side: (coefs, rhs) for side, coefs, rhs in _sides(row)}
                if step.get("side") not in sides:
                    return False
                coefficients, rhs = sides[step["side"]]
                if kind == "contradiction":
                    minimum = _minimum(coefficients, lower, upper)
                    expected = {"kind": kind, "row": step["row"], "side": step["side"],
                                "minimum": _text(minimum), "rhs": _text(rhs)}
                    if minimum is None or minimum <= rhs or step != expected:
                        return False
                    infeasible = True
                    continue
            if kind not in ("affine", "binary", "integer"):
                return False
            j, direction = step.get("variable"), step.get("bound")
            if type(j) is not int or not 0 <= j < len(lower) or direction not in ("lower", "upper"):
                return False
            old = lower[j] if direction == "lower" else upper[j]
            if kind == "binary":
                if types[j] != "B":
                    return False
                candidate = Fraction(0 if direction == "lower" else 1)
            elif kind == "integer":
                if not certificate["round_integers"] or types[j] not in ("B", "I"):
                    return False
                if not isinstance(old, Fraction):
                    return False
                candidate = Fraction(math.ceil(old) if direction == "lower" else math.floor(old))
            else:
                coefficient = dict(coefficients).get(j)
                if coefficient is None or direction != ("upper" if coefficient > 0 else "lower"):
                    return False
                minimum = _minimum(coefficients, lower, upper, exclude=j)
                if minimum is None:
                    return False
                candidate = (rhs - minimum) / coefficient
            if not (candidate > old if direction == "lower" else candidate < old):
                return False
            expected = {"kind": kind, "variable": j, "bound": direction,
                        "old": _text(old), "new": _text(candidate)}
            if kind == "affine":
                expected.update(row=step["row"], side=step["side"])
            if step != expected:
                return False
            _apply(step, lower, upper)
            infeasible = _crossed(lower, upper)
        result = certificate["result"]
        status = result["status"]
        if status not in ("infeasible", "fixed_point", "budget"):
            return False
        if (status == "infeasible") != infeasible:
            return False
        if status == "fixed_point" and _available(lower, upper, types, rows,
                                                  certificate["round_integers"]):
            return False
        expected = {"lower": list(map(_text, lower)), "upper": list(map(_text, upper)),
                    "float_lower": [_outward(x, lower=True).hex() for x in lower],
                    "float_upper": [_outward(x, lower=False).hex() for x in upper],
                    "infeasible": infeasible, "status": status}
        return result == expected
    except (AttributeError, IndexError, KeyError, OverflowError, TypeError, ValueError, ZeroDivisionError):
        return False
