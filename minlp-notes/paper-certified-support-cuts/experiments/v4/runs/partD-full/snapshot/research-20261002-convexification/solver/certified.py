"""Replayable support cuts on bounded one- and two-variable domains.

The public cut is ``sum(coefficients[j] * features[j]) >= rhs``.  Both
coefficients and rhs denote the *exact binary floats* exported to a solver.
Polynomial witnesses use rational Bernstein bounds; elementary univariate
witnesses use exact rational interval arithmetic and optional python-flint.
The checker takes the expected model as input and never parses certificate
strings as Python or SymPy code.  A failed search is not a hull-membership test.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import product
from math import comb, isfinite, nextafter, prod
from typing import Any

import sympy as sp


Q = Fraction
Box = tuple[tuple[Q, Q], ...]


class UnsupportedExpression(ValueError):
    pass


class UnresolvedDomain(ValueError):
    pass


def rational(value) -> Q:
    """Preserve exact numeric input, including binary floating-point values."""
    if isinstance(value, Q):
        return value
    if isinstance(value, sp.Rational):
        return Q(int(value.p), int(value.q))
    if isinstance(value, sp.Float):
        return rational(sp.Rational(value))
    if hasattr(value, "as_integer_ratio"):
        n, d = value.as_integer_ratio()
        return Q(int(n), int(d))
    return Q(value)


def downward_float(value: Q) -> float:
    """Largest binary64 value no greater than the exact rational value."""
    result = float(value)
    if not isfinite(result):
        raise OverflowError("support bound is outside finite binary64 range")
    if Q.from_float(result) > value:
        result = nextafter(result, float("-inf"))
    if not isfinite(result):
        raise OverflowError("support bound is outside finite binary64 range")
    return result


@dataclass(frozen=True)
class SupportCut:
    coefficients: tuple[float, ...]
    rhs: float

    @property
    def rhs_float(self) -> float:
        return self.rhs

    @property
    def rhs_exact(self) -> Q:
        return Q.from_float(self.rhs)


@dataclass(frozen=True)
class SupportResult:
    status: str
    cut: SupportCut | None
    witness: dict[str, Any] | None
    stats: dict[str, Any]


_FUNCTIONS = {sp.exp: "exp", sp.log: "log", sp.sin: "sin", sp.cos: "cos",
              sp.sinh: "sinh", sp.cosh: "cosh", sp.tanh: "tanh",
              sp.atan: "atan", sp.Abs: "abs"}


def _encode(expr, symbols):
    """Typed, JSON-native expression identity; no evaluator reads source text."""
    if expr in symbols:
        return ["variable", symbols.index(expr)]
    if isinstance(expr, (sp.Rational, sp.Float)):
        return ["rational", str(rational(expr))]
    if expr == sp.pi:
        return ["pi"]
    if expr == sp.E:
        return ["e"]
    if expr.is_Add or expr.is_Mul:
        return ["add" if expr.is_Add else "mul", *[_encode(a, symbols) for a in expr.args]]
    if expr.is_Pow and isinstance(expr.args[1], sp.Rational):
        return ["pow", _encode(expr.args[0], symbols), str(rational(expr.args[1]))]
    if expr.func in _FUNCTIONS and len(expr.args) == 1:
        return [_FUNCTIONS[expr.func], _encode(expr.args[0], symbols)]
    raise UnsupportedExpression(f"unsupported expression node: {expr.func}")


def _polynomial_tree(expr, symbols):
    if expr in symbols or isinstance(expr, (sp.Rational, sp.Float)):
        return True
    if expr.is_Add or expr.is_Mul:
        return all(_polynomial_tree(a, symbols) for a in expr.args)
    return (expr.is_Pow and isinstance(expr.args[1], sp.Integer)
            and 0 <= int(expr.args[1]) <= 32 and _polynomial_tree(expr.args[0], symbols))


def _prepare(features, symbols, box, coefficients, rows):
    symbols = tuple(symbols)
    if not symbols or len(set(symbols)) != len(symbols):
        raise ValueError("distinct symbols are required")
    if not all(isinstance(s, sp.Symbol) for s in symbols):
        raise ValueError("symbols must be SymPy Symbol objects")
    features = tuple(sp.sympify(e) if isinstance(e, (int, float, Q)) else e for e in features)
    if not features or any(not isinstance(e, sp.Expr) for e in features):
        raise ValueError("features must be nonempty SymPy expressions, never source strings")
    if any(not e.free_symbols.issubset(symbols) for e in features):
        raise ValueError("feature contains an unbound symbol")
    encoded = [_encode(e, symbols) for e in features]
    b = tuple((rational(lo), rational(hi)) for lo, hi in box)
    if len(b) != len(symbols) or any(lo > hi for lo, hi in b):
        raise ValueError("box dimensions or bounds are invalid")
    cf = tuple(float(v) for v in coefficients)
    if len(cf) != len(features) or not all(isfinite(c) for c in cf):
        raise ValueError("one finite solver coefficient is required per feature")
    cq = tuple(Q.from_float(c) for c in cf)
    rr = tuple((tuple(rational(v) for v in a), rational(rhs)) for a, rhs in rows)
    if any(len(a) != len(symbols) for a, _ in rr):
        raise ValueError("row dimension is invalid")
    binding = {"features": encoded, "dimension": len(symbols),
               "box": [[str(lo), str(hi)] for lo, hi in b],
               "coefficients": [c.hex() for c in cf],
               "rows": [[[str(v) for v in a], str(rhs)] for a, rhs in rr]}
    return features, symbols, b, cf, cq, rr, binding


def _polynomial(features, symbols, coefficients):
    if not all(_polynomial_tree(e, symbols) for e in features):
        return None
    expression = sp.S.Zero
    for c, e in zip(coefficients, features):
        # Every original tree was checked before simplifying the scalar support.
        exact = e.xreplace({v: sp.Rational(v) for v in e.atoms(sp.Float)})
        expression += sp.Rational(c.numerator, c.denominator) * exact
    polynomial = sp.Poly(expression, *symbols, domain=sp.QQ)
    terms = {powers: rational(c) for powers, c in polynomial.terms()}
    degrees = tuple(max(p[i] for p in terms) for i in range(len(symbols)))
    if max(degrees) > 32:
        raise UnsupportedExpression("polynomial exceeds the supported degree")
    return terms


def bernstein_lower(terms: dict[tuple[int, ...], Q], box: Box) -> Q:
    """Exact tensor Bernstein lower bound after x_i = lo_i + width_i*t_i."""
    dimension = len(box)
    degrees = tuple(max(p[i] for p in terms) for i in range(dimension))
    power: dict[tuple[int, ...], Q] = {}
    for exponent, coefficient in terms.items():
        for k in product(*(range(v + 1) for v in exponent)):
            value = coefficient
            for i, ki in enumerate(k):
                lo, hi = box[i]
                value *= comb(exponent[i], ki) * lo ** (exponent[i] - ki) * (hi - lo) ** ki
            power[k] = power.get(k, Q(0)) + value
    lower = None
    for j in product(*(range(d + 1) for d in degrees)):
        value = Q(0)
        for k, coefficient in power.items():
            if all(ki <= ji for ki, ji in zip(k, j)):
                value += coefficient * prod(Q(comb(ji, ki), comb(di, ki))
                                            for ji, ki, di in zip(j, k, degrees))
        lower = value if lower is None else min(lower, value)
    assert lower is not None
    return lower


def _arb_library():
    try:
        from flint import arb, ctx, fmpq
    except ImportError as exc:
        raise UnsupportedExpression("elementary expressions require python-flint") from exc
    return arb, ctx, fmpq


def _arb_rational(q, arb, fmpq):
    return arb(fmpq(q.numerator, q.denominator))


def _arb_bounds(ball):
    if not ball.is_finite():
        raise UnresolvedDomain("Arb returned a nonfinite enclosure")
    def endpoint(value):
        m, e = value.man_exp()
        return Q(int(m)) * Q(2) ** int(e)
    return endpoint(ball.lower()), endpoint(ball.upper())


def _multiply(a, b):
    values = [x * y for x in a for y in b]
    return min(values), max(values)


def _integer_power(value, n):
    lo, hi = value
    if n < 0:
        low, high = _integer_power(value, -n)
        if low <= 0 <= high:
            raise UnresolvedDomain("denominator interval contains zero")
        return Q(1) / high, Q(1) / low
    if n == 0:
        return Q(1), Q(1)
    if n % 2:
        return lo ** n, hi ** n
    return (Q(0) if lo <= 0 <= hi else min(lo ** n, hi ** n), max(lo ** n, hi ** n))


def elementary_interval(expr, symbol, interval, precision=128):
    """Enclose a stored expression on the *entire* exact rational interval.

    Rational algebra and interval endpoints are exact. Arb is only used for
    transcendental endpoint/range evaluations. No unknown sliver is omitted.
    Fractional powers require a nonnegative base, strictly positive for
    negative exponents; no complex branch or odd-root extension is inferred.
    """
    arb, ctx, fmpq = _arb_library()

    def endpoint_function(q, name):
        return _arb_bounds(getattr(_arb_rational(q, arb, fmpq), name)())

    def ev(e):
        if e == symbol:
            return interval
        if isinstance(e, (sp.Rational, sp.Float)):
            q = rational(e)
            return q, q
        if e == sp.pi:
            return _arb_bounds(arb.pi())
        if e == sp.E:
            return _arb_bounds(arb(1).exp())
        if e.is_Add:
            args = [ev(a) for a in e.args]
            return sum((a for a, _ in args), Q(0)), sum((b for _, b in args), Q(0))
        if e.is_Mul:
            result = (Q(1), Q(1))
            for a in e.args:
                result = _multiply(result, ev(a))
            return result
        if e.is_Pow:
            value = ev(e.args[0])
            p = rational(e.args[1])
            if p.denominator == 1:
                return _integer_power(value, p.numerator)
            lo, hi = value
            if lo < 0 or (p < 0 and lo <= 0):
                raise UnresolvedDomain("fractional-power base domain is not established")
            def root_endpoint(q):
                if q == 0 and p > 0:
                    return Q(0), Q(0)
                ball = _arb_rational(q, arb, fmpq).root(p.denominator) ** p.numerator
                return _arb_bounds(ball)
            left, right = root_endpoint(lo), root_endpoint(hi)
            return (left[0], right[1]) if p > 0 else (right[0], left[1])
        name = _FUNCTIONS.get(e.func)
        if name is None:
            raise UnsupportedExpression(f"unsupported elementary function {e.func}")
        lo, hi = ev(e.args[0])
        if name == "abs":
            return (Q(0) if lo <= 0 <= hi else min(abs(lo), abs(hi)), max(abs(lo), abs(hi)))
        if name == "log" and lo <= 0:
            raise UnresolvedDomain("log argument is not strictly positive on its full interval")
        if name in ("exp", "log", "sinh", "tanh", "atan"):
            return endpoint_function(lo, name)[0], endpoint_function(hi, name)[1]
        ball = _arb_rational(lo, arb, fmpq).union(_arb_rational(hi, arb, fmpq))
        return _arb_bounds(getattr(ball, name)())

    with ctx.workprec(precision):
        return ev(expr)


def feature_intervals(features, symbols, point, precision=128):
    """Reevaluate graph features at an exact point for membership witnesses.

    Polynomial values are evaluated in rational arithmetic, without Arb.
    General expressions currently require one variable and python-flint.
    This function does not validate a caller's box or affine model rows.
    """
    symbols = tuple(symbols)
    point = tuple(rational(v) for v in point)
    if len(point) != len(symbols):
        raise ValueError("point dimension is invalid")
    values = []
    for e in features:
        _encode(e, symbols)
        if _polynomial_tree(e, symbols):
            exact = e.xreplace({v: sp.Rational(v) for v in e.atoms(sp.Float)})
            value = exact.subs({s: sp.Rational(q.numerator, q.denominator)
                                for s, q in zip(symbols, point)}, simultaneous=True)
            value = rational(value)
            values.append((value, value))
        elif len(symbols) == 1:
            values.append(elementary_interval(e, symbols[0], (point[0], point[0]), precision))
        else:
            raise UnsupportedExpression("elementary features require one variable")
    return tuple(values)


def _row_exclusion(box, rows):
    for i, (a, rhs) in enumerate(rows):
        lower = sum((c * (lo if c >= 0 else hi) for c, (lo, hi) in zip(a, box)), Q(0))
        if lower > rhs:
            return i
    return None


def _split(box, axis):
    lo, hi = box[axis]
    mid = (lo + hi) / 2
    return (box[:axis] + ((lo, mid),) + box[axis + 1:],
            box[:axis] + ((mid, hi),) + box[axis + 1:])


def _elementary_data(features, symbols, coefficients):
    if len(symbols) != 1:
        return None
    scalar = sum((sp.Rational(c.numerator, c.denominator)
                  * e.xreplace({v: sp.Rational(v) for v in e.atoms(sp.Float)})
                  for c, e in zip(coefficients, features)), sp.S.Zero)
    try:
        derivative = sp.diff(scalar, symbols[0], 2)
        _encode(derivative, symbols)
    except (UnsupportedExpression, ValueError, NotImplementedError):
        derivative = None
    return scalar, derivative


def _leaf_bound(features, symbols, box, coefficients, terms, precision, elementary=None):
    if terms is not None:
        if len(symbols) > 2 or prod(max(p[i] for p in terms) + 1 for i in range(len(symbols))) > 1024:
            raise UnsupportedExpression("Bernstein fallback supports only small 1D/2D tensors")
        return bernstein_lower(terms, box)
    if len(symbols) != 1:
        raise UnsupportedExpression("elementary expressions are supported only in one variable")
    lower = Q(0)
    for e, c in zip(features, coefficients):
        # Even a zero-weight feature must be defined throughout the domain.
        lo, hi = elementary_interval(e, symbols[0], box[0], precision)
        lower += c * (lo if c >= 0 else hi)
    # Cancellation in the scalar direction is safe only after every original
    # feature has passed whole-cell domain evaluation, including zero weights.
    if elementary is None:
        elementary = _elementary_data(features, symbols, coefficients)
    scalar, derivative = elementary
    try:
        lower = max(lower, elementary_interval(scalar, symbols[0], box[0], precision)[0])
    except (UnsupportedExpression, UnresolvedDomain, ZeroDivisionError):
        pass
    if derivative is not None:
        a, b = box[0]
        try:
            curvature_upper = elementary_interval(derivative, symbols[0], (a, b), precision)[1]
            left = elementary_interval(scalar, symbols[0], (a, a), precision)[0]
            right = elementary_interval(scalar, symbols[0], (b, b), precision)[0]
            chord = min(left, right) - max(Q(0), curvature_upper) * (b - a)**2 / 8
            lower = max(lower, chord)
        except (UnsupportedExpression, UnresolvedDomain, ZeroDivisionError):
            # A derivative singularity never licenses removing an endpoint.
            pass
    return lower


def _quadratic_data(terms, dimension):
    if terms is None or dimension != 2 or any(sum(p) > 2 for p in terms):
        return None
    return tuple(terms.get(p, Q(0)) for p in ((0, 0), (1, 0), (0, 1), (2, 0), (1, 1), (0, 2)))


def _quadratic_oracle():
    # This directory is a standalone research package, not installed globally.
    # Both supported invocation styles have the research directory on sys.path.
    from theory.quadratic_polygon import support_quadratic, replay_quadratic
    return support_quadratic, replay_quadratic


def _star_center(terms, rows, dimension):
    if terms is None or dimension < 3 or any(sum(p) > 2 for p in terms):
        return None
    edges = [tuple(i for i, power in enumerate(p) if power) for p, c in terms.items()
             if c and sum(power != 0 for power in p) == 2]
    for center in range(dimension):
        if (all(center in edge for edge in edges)
                and all(sum(c != 0 for i, c in enumerate(a) if i != center) <= 1 for a, _ in rows)):
            return center
    return None


def _star_oracle():
    from theory.quadratic_star import support_star, replay_star
    return support_star, replay_star


def certify_support(features, symbols, box, coefficients, *, rows=(), target=None,
                    max_cells=2048, max_depth=24, precision=128,
                    quadratic_fast_path=True) -> SupportResult:
    """Certify a support inequality, optionally requiring ``rhs >= target``.

    Without target, any finite whole-domain bound suffices. With target, the
    actual downward-rounded binary64 rhs must reach it. Budgets bound visited
    boxes. Exhaustion returns ``incomplete`` and no cut. Rows have the form
    ``(coefficient_tuple, rhs)`` for ``a*x <= rhs`` and must be valid model rows.
    The returned witness is JSON serializable and carries the entire binding.
    """
    if (type(max_cells) is not int or not 1 <= max_cells <= 1000000
            or type(max_depth) is not int or not 0 <= max_depth <= 256
            or type(precision) is not int or not 32 <= precision <= 4096):
        raise ValueError("invalid certification budget or precision")
    stats = {"cells": 0, "leaves": 0, "method": None, "reason": None}
    try:
        features, symbols, box, cf, cq, rows, binding = _prepare(features, symbols, box, coefficients, rows)
        target_q = None if target is None else rational(target)
        terms = _polynomial(features, symbols, cq)
        elementary = _elementary_data(features, symbols, cq) if terms is None else None
        stats["method"] = "bernstein" if terms is not None else "arb"
        if terms is None:
            _arb_library()
        quadratic = _quadratic_data(terms, len(symbols)) if quadratic_fast_path else None
        center = _star_center(terms, rows, len(symbols)) if quadratic_fast_path else None
        proof = None
        lower = None
        if quadratic is not None:
            oracle, _ = _quadratic_oracle()
            exact_rows = tuple((*a, rhs) for a, rhs in rows)
            certificate = oracle(box, exact_rows, quadratic)
            stats.update(method="quadratic_polygon", cells=1, leaves=1)
            proof = {"quadratic": certificate}
            if certificate["status"] == "complete":
                lower = rational(certificate["bound"])
                stats.update(minimizer=certificate["minimizer"], exact_support=certificate["bound"])
        elif center is not None:
            oracle, _ = _star_oracle()
            certificate = oracle(box, rows, terms, center)
            stats.update(method="quadratic_star", cells=1, leaves=1)
            proof = {"star": certificate, "center": center}
            if certificate["status"] == "complete":
                lower = rational(certificate["bound"])
                stats.update(minimizer=certificate["minimizer"], exact_support=certificate["bound"])
        else:
            proof = {}
            queue = [(box, proof, 0)]
            bounds = []
            while queue:
                if stats["cells"] >= max_cells:
                    stats["reason"] = "cell budget exhausted"
                    return SupportResult("incomplete", None, None, stats)
                current, node, depth = queue.pop()
                stats["cells"] += 1
                excluded = _row_exclusion(current, rows)
                if excluded is not None:
                    node["excluded_by"] = excluded
                    stats["leaves"] += 1
                    continue
                try:
                    value = _leaf_bound(features, symbols, current, cq, terms, precision, elementary)
                    reached = target_q is None or rational(downward_float(value)) >= target_q
                except (UnresolvedDomain, ZeroDivisionError, OverflowError):
                    value, reached = None, False
                if reached:
                    node["lower"] = str(value)
                    bounds.append(value)
                    stats["leaves"] += 1
                    continue
                widths = [hi - lo for lo, hi in current]
                if depth >= max_depth or max(widths) == 0:
                    stats["reason"] = "depth budget or unresolved domain/target"
                    return SupportResult("incomplete", None, None, stats)
                axis = max(range(len(current)), key=widths.__getitem__)
                left, right = _split(current, axis)
                node.update(split=axis, children=[{}, {}])
                queue.extend(((right, node["children"][1], depth + 1),
                              (left, node["children"][0], depth + 1)))
            lower = min(bounds) if bounds else None
        witness = {"format": "support-cut-v1", "model": binding,
                   "method": stats["method"], "precision": precision, "proof": proof}
        if lower is None:
            witness["status"] = "empty"
            return SupportResult("empty", None, witness, stats)
        rhs = downward_float(lower)
        if target_q is not None and Q.from_float(rhs) < target_q:
            stats["reason"] = "requested separation target not certified"
            return SupportResult("incomplete", None, None, stats)
        witness.update(status="complete", lower_bound=str(lower), rhs=rhs.hex())
        return SupportResult("complete", SupportCut(cf, rhs), witness, stats)
    except UnsupportedExpression as exc:
        stats["reason"] = str(exc)
        return SupportResult("unsupported", None, None, stats)
    except OverflowError as exc:
        stats["reason"] = str(exc)
        return SupportResult("incomplete", None, None, stats)


def replay_support(features, symbols, box, coefficients, rows, witness) -> bool:
    """Recheck the expected model, exact cover, local bounds, and exported rhs.

    This checks witness values rather than trusting generator status or stats.
    The expected feature expressions/rows must come from the model being checked.
    No model text from the witness is evaluated, imported, or sympified.
    """
    try:
        features, symbols, box, cf, cq, rows, binding = _prepare(features, symbols, box, coefficients, rows)
        if not isinstance(witness, dict) or witness.get("format") != "support-cut-v1":
            return False
        if witness.get("model") != binding or witness.get("status") not in ("complete", "empty"):
            return False
        precision = witness["precision"]
        if type(precision) is not int or not 32 <= precision <= 4096:
            return False
        terms = _polynomial(features, symbols, cq)
        elementary = _elementary_data(features, symbols, cq) if terms is None else None
        proof = witness["proof"]
        method = witness["method"]
        bounds = []
        if method == "quadratic_polygon":
            quadratic = _quadratic_data(terms, len(symbols))
            if quadratic is None or set(proof) != {"quadratic"}:
                return False
            _, checker = _quadratic_oracle()
            certificate = proof["quadratic"]
            if not checker(box, tuple((*a, rhs) for a, rhs in rows), quadratic, certificate):
                return False
            if certificate["status"] == "complete":
                bounds.append(rational(certificate["bound"]))
        elif method == "quadratic_star":
            if terms is None or set(proof) != {"star", "center"}:
                return False
            center = proof["center"]
            if type(center) is not int or not 0 <= center < len(symbols):
                return False
            _, checker = _star_oracle()
            certificate = proof["star"]
            if not checker(box, rows, terms, center, certificate):
                return False
            if certificate["status"] == "complete":
                bounds.append(rational(certificate["bound"]))
        else:
            if method != ("bernstein" if terms is not None else "arb"):
                return False
            queue = [(box, proof, 0)]
            visited = 0
            while queue:
                current, node, depth = queue.pop()
                visited += 1
                if visited > 1000000 or depth > 256 or not isinstance(node, dict):
                    return False
                if set(node) == {"split", "children"}:
                    axis, children = node["split"], node["children"]
                    if (type(axis) is not int or not 0 <= axis < len(box)
                            or not isinstance(children, list) or len(children) != 2
                            or current[axis][0] == current[axis][1]):
                        return False
                    left, right = _split(current, axis)
                    queue.extend(((left, children[0], depth + 1), (right, children[1], depth + 1)))
                elif set(node) == {"excluded_by"}:
                    i = node["excluded_by"]
                    if type(i) is not int or not 0 <= i < len(rows):
                        return False
                    if _row_exclusion(current, (rows[i],)) != 0:
                        return False
                elif set(node) == {"lower"}:
                    claimed = rational(node["lower"])
                    recomputed = _leaf_bound(features, symbols, current, cq, terms, precision, elementary)
                    if claimed > recomputed:
                        return False
                    bounds.append(claimed)
                else:
                    return False
        if witness["status"] == "empty":
            return not bounds and "rhs" not in witness and "lower_bound" not in witness
        if not bounds:
            return False
        lower = rational(witness["lower_bound"])
        rhs = float.fromhex(witness["rhs"])
        return isfinite(rhs) and Q.from_float(rhs) <= lower <= min(bounds)
    except (ValueError, TypeError, KeyError, AttributeError, ZeroDivisionError,
            OverflowError, ImportError, RecursionError):
        return False
