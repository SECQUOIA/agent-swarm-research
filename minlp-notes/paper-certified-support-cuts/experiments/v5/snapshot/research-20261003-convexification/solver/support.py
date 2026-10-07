"""Bounded general quadratic support, with the frozen v1 kernels as fallback.

The public API preserves v1's exact binary64 cut semantics and typed model
binding. The new path expands a *validated polynomial expression tree* using
rational coefficients and solves its support over the supplied affine domain.
All other cases keep v1's supported expression/domain rules.
"""

from fractions import Fraction
from math import isfinite

from . import certified as _legacy
from .certified import SupportCut, SupportResult, downward_float, rational
from theory.quadratic_polytope import (
    EnumerationLimitError, coefficient_pairs, replay_quadratic, support_quadratic,
)


def _quadratic_coefficients(terms, dimension):
    if terms is None or any(sum(powers) > 2 for powers in terms):
        return None
    exponents = [(0,) * dimension]
    for i in range(dimension):
        exponent = [0] * dimension
        exponent[i] = 1
        exponents.append(tuple(exponent))
    for i, j in coefficient_pairs(dimension):
        exponent = [0] * dimension
        exponent[i] += 1
        exponent[j] += 1
        exponents.append(tuple(exponent))
    return tuple(terms.get(powers, Fraction(0)) for powers in exponents)


def certify_support(features, symbols, box, coefficients, *, rows=(), target=None,
                    max_cells=2048, max_depth=24, precision=128,
                    quadratic_fast_path=True, max_polytope_dimension=4,
                    max_polytope_faces=5000):
    """Certify a lower support cut, optionally meeting the given exact target.

    General quadratic enumeration is attempted up to the dimension and face
    budgets. A budget refusal falls back to the reviewed v1 kernels, including
    their polynomial-time constrained-star oracle. No partial enumeration is
    exported as a lower bound. Target failure keeps an exact minimizer in stats
    when one was computed, so a direction search can add a useful sample.
    """
    if (type(max_cells) is not int or not 1 <= max_cells <= 1000000
            or type(max_depth) is not int or not 0 <= max_depth <= 256
            or type(precision) is not int or not 32 <= precision <= 4096
            or type(max_polytope_dimension) is not int or max_polytope_dimension < 0
            or type(max_polytope_faces) is not int or max_polytope_faces < 0):
        raise ValueError("invalid certification budget or precision")
    # Materialize once so the fallback also receives complete generator inputs.
    features, symbols, box, coefficients, rows = (
        tuple(features), tuple(symbols), tuple(tuple(pair) for pair in box),
        tuple(coefficients), tuple((tuple(a), rhs) for a, rhs in rows)
    )
    skip_reason = None
    try:
        ff, ss, bb, cf, cq, rr, binding = _legacy._prepare(
            features, symbols, box, coefficients, rows
        )
        terms = _legacy._polynomial(ff, ss, cq)
        quadratic = _quadratic_coefficients(terms, len(ss))
        if quadratic_fast_path and quadratic is not None and len(ss) <= max_polytope_dimension:
            try:
                certificate = support_quadratic(
                    bb, tuple((*a, rhs) for a, rhs in rr), quadratic,
                    max_faces=max_polytope_faces,
                )
            except EnumerationLimitError as exc:
                skip_reason = str(exc)
            else:
                stats = {"cells": 1, "leaves": 1, "method": "quadratic_polytope",
                         "reason": None, "faces": certificate["enumeration"]["subsets"]}
                witness = {"format": "support-cut-v2", "model": binding,
                           "method": "quadratic_polytope", "precision": precision,
                           "proof": {"quadratic": certificate}, "status": certificate["status"]}
                if certificate["status"] == "empty":
                    return SupportResult("empty", None, witness, stats)
                lower = rational(certificate["bound"])
                stats.update(minimizer=certificate["minimizer"], exact_support=certificate["bound"])
                try:
                    rhs = downward_float(lower)
                except OverflowError as exc:
                    stats["reason"] = str(exc)
                    return SupportResult("incomplete", None, None, stats)
                if target is not None and Fraction.from_float(rhs) < rational(target):
                    stats["reason"] = "requested separation target not certified"
                    return SupportResult("incomplete", None, None, stats)
                witness.update(lower_bound=str(lower), rhs=rhs.hex())
                return SupportResult("complete", SupportCut(cf, rhs), witness, stats)
    except _legacy.UnsupportedExpression:
        # The fallback returns the established structured unsupported outcome.
        pass
    result = _legacy.certify_support(
        features, symbols, box, coefficients, rows=rows, target=target,
        max_cells=max_cells, max_depth=max_depth, precision=precision,
        quadratic_fast_path=quadratic_fast_path,
    )
    if skip_reason is not None:
        result = SupportResult(result.status, result.cut, result.witness,
                               {**result.stats, "polytope_skipped": skip_reason})
    return result


def replay_support(features, symbols, box, coefficients, rows, witness, *, max_polytope_faces=None):
    """Recheck a v2 or frozen v1 witness against the caller's original model.

    The checker never reconstructs features or domains from witness text.
    For v2 it repeats the entire exact enumeration and checks the actual
    exported binary64 intercept. Its optional budget is local checker policy.
    """
    if not isinstance(witness, dict) or witness.get("format") != "support-cut-v2":
        return _legacy.replay_support(features, symbols, box, coefficients, rows, witness)
    try:
        ff, ss, bb, cf, cq, rr, binding = _legacy._prepare(
            features, symbols, box, coefficients, rows
        )
        if (witness.get("model") != binding or witness.get("method") != "quadratic_polytope"
                or witness.get("status") not in ("complete", "empty")
                or type(witness.get("precision")) is not int
                or not 32 <= witness["precision"] <= 4096):
            return False
        quadratic = _quadratic_coefficients(_legacy._polynomial(ff, ss, cq), len(ss))
        proof = witness["proof"]
        if quadratic is None or not isinstance(proof, dict) or set(proof) != {"quadratic"}:
            return False
        certificate = proof["quadratic"]
        if not replay_quadratic(bb, tuple((*a, rhs) for a, rhs in rr), quadratic,
                                certificate, max_faces=max_polytope_faces):
            return False
        if witness["status"] == "empty":
            return (certificate["status"] == "empty" and "rhs" not in witness
                    and "lower_bound" not in witness)
        if certificate["status"] != "complete":
            return False
        rhs = float.fromhex(witness["rhs"])
        lower = rational(witness["lower_bound"])
        return isfinite(rhs) and Fraction.from_float(rhs) <= lower <= rational(certificate["bound"])
    except (ValueError, TypeError, KeyError, AttributeError, ZeroDivisionError,
            OverflowError, ImportError, RecursionError):
        return False
