"""Certificate-backed weak separation for compact rational polynomial graphs.

The distance convention is L1 in feature coordinates, so normals have infinity
norm at most one.  ``complete=True`` exhausts a proved finite net if shortcuts
fail.  Its complexity can be enormous.  A bounded run may return ``unresolved``.
Rational cuts are authoritative; a separately rounded binary64 export is optional.
"""

from fractions import Fraction
from math import ceil, comb, isfinite, nextafter, inf
from pathlib import Path
import importlib.util
import sys

import sympy as sp


SCHEMA = "polynomial-graph-separation-v1"


def rational(value):
    if isinstance(value, bool):
        raise ValueError("booleans are not rational data")
    if isinstance(value, float) and not isfinite(value):
        raise ValueError("finite rational data required")
    try:
        return Fraction(value)
    except (TypeError, ValueError, OverflowError, ZeroDivisionError) as exc:
        raise ValueError("finite rational data required") from exc


def _oracle_module():
    name = "_v2_separation_quadratic_polytope"
    if name not in sys.modules:
        path = Path(__file__).resolve().parents[1] / "theory" / "quadratic_polytope.py"
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        try:
            spec.loader.exec_module(module)
        except BaseException:
            del sys.modules[name]
            raise
    return sys.modules[name]


def _exact_poly(expression, symbols):
    if isinstance(expression, (str, bytes)):
        raise ValueError("feature expression strings are not accepted")
    expression = sp.sympify(expression)
    def polynomial_syntax(node):
        if node in symbols or isinstance(node, (sp.Integer, sp.Rational, sp.Float)):
            return True
        if isinstance(node, (sp.Add, sp.Mul)):
            return all(polynomial_syntax(arg) for arg in node.args)
        if isinstance(node, sp.Pow):
            return isinstance(node.exp, sp.Integer) and node.exp >= 0 and polynomial_syntax(node.base)
        return False
    if not polynomial_syntax(expression):
        raise ValueError("source feature syntax must be polynomial, without hidden function domains")
    expression = expression.xreplace({v: sp.Rational(v) for v in expression.atoms(sp.Float)})
    if expression.free_symbols - set(symbols):
        raise ValueError("unbound feature variable")
    try:
        return sp.Poly(expression, *symbols, domain=sp.QQ)
    except (sp.PolynomialError, sp.CoercionFailed) as exc:
        raise ValueError("features must be rational polynomials") from exc


def _prepare(features, symbols, box, query, rows, epsilon, nonnegative=()):
    symbols = tuple(symbols)
    if not symbols or any(not isinstance(s, sp.Symbol) for s in symbols) or len(set(symbols)) != len(symbols):
        raise ValueError("one or more distinct variables required")
    if len(box) != len(symbols) or any(len(v) != 2 for v in box):
        raise ValueError("one finite bound pair per variable required")
    box = tuple(tuple(rational(v) for v in pair) for pair in box)
    if any(lo > hi for lo, hi in box):
        raise ValueError("reversed variable bounds")
    rows = tuple(tuple(rational(v) for v in row) for row in rows)
    if any(len(row) != len(symbols) + 1 for row in rows):
        raise ValueError("rows contain variable coefficients followed by rhs")
    polys = tuple(_exact_poly(f, symbols) for f in features)
    query = tuple(rational(v) for v in query)
    epsilon = rational(epsilon)
    if not polys or len(polys) != len(query) or epsilon <= 0:
        raise ValueError("nonempty matching features/query and positive epsilon required")
    nonnegative = tuple(nonnegative)
    if (any(isinstance(i, bool) or not isinstance(i, int) or i < 0 or i >= len(polys) for i in nonnegative)
            or len(set(nonnegative)) != len(nonnegative)):
        raise ValueError("nonnegative normal coordinates must be distinct feature indices")
    identity = {
        "variables": [str(v) for v in symbols],
        "features": [[[list(powers), str(rational(c))] for powers, c in poly.terms()] for poly in polys],
        "box": [[str(v) for v in pair] for pair in box],
        "rows": [[str(v) for v in row] for row in rows],
        "query": [str(v) for v in query], "epsilon": str(epsilon), "norm": "1",
        "nonnegative": sorted(nonnegative),
    }
    return polys, symbols, box, query, rows, epsilon, identity


def _power_interval(lo, hi, power):
    if power == 0:
        return Fraction(1), Fraction(1)
    values = (lo ** power, hi ** power)
    return (Fraction(0) if power % 2 == 0 and lo <= 0 <= hi else min(values), max(values))


def _poly_interval(poly, box):
    lower = upper = Fraction(0)
    for powers, coefficient in poly.terms():
        lo = hi = rational(coefficient)
        for bounds, power in zip(box, powers):
            a, b = _power_interval(*bounds, power)
            values = (lo * a, lo * b, hi * a, hi * b)
            lo, hi = min(values), max(values)
        lower += lo
        upper += hi
    return lower, upper


def _evaluate(polys, point):
    answer = []
    for poly in polys:
        total = Fraction(0)
        for powers, coefficient in poly.terms():
            term = rational(coefficient)
            for x, power in zip(point, powers):
                term *= x ** power
            total += term
        answer.append(total)
    return tuple(answer)


def _dot(a, b):
    return sum((x * y for x, y in zip(a, b)), Fraction(0))


def _feasible(point, box, rows):
    return (len(point) == len(box)
            and all(lo <= x <= hi for x, (lo, hi) in zip(point, box))
            and all(_dot(row[:-1], point) <= row[-1] for row in rows))


def _compositions(total, count):
    # Iterative weak compositions avoid a recursion-depth restriction on vertices.
    parts = [0] * (count - 1) + [total]
    while True:
        yield tuple(parts)
        index = count - 1
        while index > 0 and parts[index] == 0:
            index -= 1
        if index == 0:
            return
        remaining = parts[index] - 1
        parts[index - 1] += 1
        for j in range(index, count):
            parts[j] = 0
        parts[-1] = remaining


def _domain_net(vertices, denominator):
    seen = set()
    for weights in _compositions(denominator, len(vertices)):
        point = tuple(sum((w * v[j] for w, v in zip(weights, vertices)), Fraction(0)) / denominator
                      for j in range(len(vertices[0])))
        if point not in seen:
            seen.add(point)
            yield point


def _normal_net(dimension, intervals, nonnegative=()):
    # Lazy coordinate enumeration is essential: even a zero-work bounded request
    # can have an astronomically large theoretical net.  itertools.product would
    # materialize its coordinate pools before the first budget check.
    def coordinates(positive):
        priorities = set()
        for denominator in range(1, 17):
            for numerator in range(0 if positive else -denominator, denominator + 1):
                value = Fraction(numerator, denominator)
                index = value * intervals if positive else (value + 1) * intervals / 2
                if index.denominator == 1:
                    priorities.add(int(index))
        scale, shift = (1, 0) if positive else (2, -1)
        ordered = sorted(priorities, key=lambda i: (
            (Fraction(scale * i, intervals) + shift).denominator,
            abs((Fraction(scale * i, intervals) + shift).numerator),
            (Fraction(scale * i, intervals) + shift).numerator))
        for index in ordered:
            yield Fraction(scale * index, intervals) + shift
        for index in range(intervals + 1):
            if index not in priorities:
                yield Fraction(scale * index, intervals) + shift

    def grid():
        values = [None] * dimension
        iterators = [None] * dimension
        index = 0
        iterators[0] = coordinates(0 in nonnegative)
        while index >= 0:
            try:
                values[index] = next(iterators[index])
                if index == dimension - 1:
                    yield tuple(values)
                else:
                    index += 1
                    iterators[index] = coordinates(index in nonnegative)
            except StopIteration:
                index -= 1
    return grid()


def _quadratic_coefficients(polys, symbols, normal):
    scalar = sp.Poly(sum((sp.Rational(c.numerator, c.denominator) * p.as_expr()
                         for c, p in zip(normal, polys)), sp.Integer(0)), *symbols, domain=sp.QQ)
    d = len(symbols)
    powers = [(0,) * d]
    powers += [tuple(int(j == i) for j in range(d)) for i in range(d)]
    powers += [tuple(int(k == i) + int(k == j) for k in range(d))
               for i in range(d) for j in range(i, d)]
    return tuple(rational(scalar.coeff_monomial(p)) for p in powers)


def _float_export(normal, rhs, feature_bounds, query):
    """Outward support correction for the coefficients actually exported."""
    try:
        coefficients = tuple(float(v) for v in normal)
        if not all(isfinite(v) for v in coefficients):
            return {"available": False, "reason": "coefficient overflow"}
        correction = Fraction(0)
        for old, new, (lo, hi) in zip(normal, coefficients, feature_bounds):
            delta = Fraction(new) - old
            correction += min(delta * lo, delta * hi)
        exact_rhs = rhs + correction
        exported_rhs = float(exact_rhs)
        if not isfinite(exported_rhs):
            return {"available": False, "reason": "rhs overflow"}
        if Fraction(exported_rhs) > exact_rhs:
            exported_rhs = nextafter(exported_rhs, -inf)
        if not isfinite(exported_rhs):
            return {"available": False, "reason": "rhs underflow beyond finite range"}
        return {"available": True, "coefficients": list(coefficients), "rhs": exported_rhs,
                "separates": _dot(tuple(Fraction(c) for c in coefficients), query) < Fraction(exported_rhs)}
    except OverflowError:
        return {"available": False, "reason": "binary64 overflow"}


def _distance(value, query, nonnegative):
    return sum((max(a - b, Fraction(0)) if i in nonnegative else abs(a - b)
                for i, (a, b) in enumerate(zip(value, query))), Fraction(0))


def _combination_certificate(points, polys, query, epsilon, nonnegative=()):
    """Numerical proposal, then exact rational verification; no solver trust."""
    if not points:
        return None, None
    values = [_evaluate(polys, point) for point in points]
    for i, value in enumerate(values):
        distance = _distance(value, query, nonnegative)
        if distance <= epsilon:
            return {"kind": "convex_combination", "points": [[str(x) for x in points[i]]],
                    "weights": ["1"], "distance": str(distance)}, None
    try:
        import numpy as np
        from scipy.optimize import linprog
        matrix = np.asarray([[float(v) for v in value] for value in values], dtype=float).T
        q = np.asarray([float(v) for v in query], dtype=float)
        m, n = matrix.shape
        result = linprog(np.r_[np.zeros(n), np.ones(m)],
                         A_ub=np.r_[np.c_[matrix, -np.eye(m)], np.c_[-matrix, -np.eye(m)]],
                         b_ub=np.r_[q, -q], A_eq=np.r_[np.ones(n), np.zeros(m)][None, :],
                         b_eq=[1.0], bounds=(0, None), method="highs")
        if not result.success:
            return None, None
        weights = [Fraction(max(0.0, float(w))) for w in result.x[:n]]
        total = sum(weights)
        if not total:
            return None, None
        weights = [w / total for w in weights]
        combination = tuple(sum((w * value[j] for w, value in zip(weights, values)), Fraction(0)) for j in range(m))
        distance = _distance(combination, query, nonnegative)
        if distance <= epsilon:
            active = [(p, w) for p, w in zip(points, weights) if w]
            return {"kind": "convex_combination", "points": [[str(x) for x in p] for p, _ in active],
                    "weights": [str(w) for _, w in active], "distance": str(distance)}, None
        dual = result.ineqlin.marginals
        normal = tuple(Fraction(max(0.0 if j in nonnegative else -1.0,
                                    min(1.0, float(dual[m + j] - dual[j])))) for j in range(m))
        return None, normal
    except (ImportError, ValueError, TypeError, OverflowError, FloatingPointError):
        return None, None


def separate_graph(features, symbols, box, query, *, rows=(), epsilon=Fraction(1, 100),
                   complete=False, max_directions=256, max_samples=20000,
                   proposal_rounds=8, initial_points=(), use_quadratic_oracle=True,
                   nonnegative=()):
    """Return ``cut``, ``within_tolerance``, ``empty_domain``, or ``unresolved``.

    ``cut`` means an exactly verified rational support inequality separates the
    rational query.  ``within_tolerance`` means distance_1(query,conv(F(P))) <=
    epsilon, not exact membership.  With ``nonnegative`` feature indices this is
    distance to conv(F(P)) plus the nonnegative cone in those coordinates.
    ``complete=True`` removes enumeration
    budgets; the rational algorithm terminates for every input in this contract.
    No complexity bound makes that exhaustive mode generally practical.
    """
    polys, symbols, box, query, rows, epsilon, identity = _prepare(features, symbols, box, query, rows, epsilon, nonnegative)
    nonnegative = tuple(identity["nonnegative"])
    if not isinstance(complete, bool) or any(isinstance(v, bool) or not isinstance(v, int) or v < 0
                                           for v in (max_directions, max_samples, proposal_rounds)):
        raise ValueError("nonnegative integer budgets and boolean complete required")
    module = _oracle_module()
    vertices = tuple(tuple(rational(x) for x in point) for point in module.polytope_vertices(box, rows))
    stats = {"support_calls": 0, "proposal_calls": 0, "normal_grid_calls": 0,
             "domain_net_points": 0, "complete_requested": complete}

    def finish(status, witness, **extra):
        return {"schema": SCHEMA, "status": status, "problem": identity,
                "witness": witness, "stats": dict(stats), **extra}

    if not vertices:
        return finish("empty_domain", {"kind": "empty_polytope"})
    points = list(vertices)
    center = tuple(sum((p[j] for p in vertices), Fraction(0)) / len(vertices) for j in range(len(box)))
    if center not in points:
        points.append(center)
    for item in initial_points:
        point = tuple(rational(x) for x in item)
        if not _feasible(point, box, rows):
            raise ValueError("initial point is outside the exact domain")
        if point not in points:
            points.append(point)
    feature_bounds = tuple(_poly_interval(p, box) for p in polys)
    radius = sum(max(abs(lo - q), abs(hi - q)) for (lo, hi), q in zip(feature_bounds, query))
    if radius == 0:
        return finish("within_tolerance", {"kind": "convex_combination",
                      "points": [[str(x) for x in vertices[0]]], "weights": ["1"], "distance": "0"})
    quadratic = use_quadratic_oracle and all(poly.total_degree() <= 2 for poly in polys)
    domain_values = None
    domain_points = None
    domain_denominator = None
    support_error = Fraction(0)
    if not quadratic:
        lipschitz = sum(max(abs(lo), abs(hi)) for p in polys for x in symbols
                        for lo, hi in [_poly_interval(p.diff(x), box)])
        diameter = max((max(p[j] for p in vertices) - min(p[j] for p in vertices)
                        for j in range(len(box))), default=Fraction(0))
        cover_numerator = lipschitz * diameter * (len(vertices) - 1)
        domain_denominator = max(1, ceil(2 * cover_numerator / epsilon))
        support_error = cover_numerator / domain_denominator
        stats["domain_net_candidate_count"] = comb(domain_denominator + len(vertices) - 1, len(vertices) - 1)
        stats["domain_net_denominator"] = domain_denominator
    margin = epsilon - support_error
    intervals = max(1, ceil(2 * radius / margin))
    stats["normal_grid_intervals"] = intervals
    stats["normal_grid_size"] = (intervals + 1) ** len(polys)

    def support(normal):
        nonlocal domain_values, domain_points
        if not complete and stats["support_calls"] >= max_directions:
            return None
        if quadratic:
            coefficients = _quadratic_coefficients(polys, symbols, normal)
            certificate = module.support_quadratic(box, rows, coefficients)
            lower = rational(certificate["bound"])
            point = tuple(rational(v) for v in certificate["minimizer"])
            evidence = {"kind": "quadratic_support", "certificate": certificate}
        else:
            if domain_values is None:
                if not complete and stats["domain_net_candidate_count"] > max_samples:
                    return None
                domain_points = list(_domain_net(vertices, domain_denominator))
                domain_values = [_evaluate(polys, p) for p in domain_points]
                stats["domain_net_points"] = len(domain_points)
            i = min(range(len(domain_values)), key=lambda j: _dot(normal, domain_values[j]))
            point = domain_points[i]
            lower = _dot(normal, domain_values[i]) - support_error
            evidence = {"kind": "polynomial_net_support", "denominator": domain_denominator,
                        "error": str(support_error), "minimizer": [str(v) for v in point]}
        stats["support_calls"] += 1
        return lower, point, evidence

    def cut_result(normal, answer):
        lower, _, evidence = answer
        return finish("cut", evidence,
                      cut={"coefficients": [str(v) for v in normal], "rhs": str(lower),
                           "orientation": ">=", "query_gap": str(lower - _dot(normal, query)),
                           "binary64": _float_export(normal, lower, feature_bounds, query)})

    for _ in range(proposal_rounds):
        combination, normal = _combination_certificate(points, polys, query, epsilon, nonnegative)
        if combination is not None:
            return finish("within_tolerance", combination)
        if normal is None or not any(normal):
            break
        stats["proposal_calls"] += 1
        answer = support(normal)
        if answer is None:
            return finish("unresolved", {"kind": "budget", "stage": "proposal_support"})
        if answer[0] > _dot(normal, query):
            return cut_result(normal, answer)
        if answer[1] in points:
            break
        points.append(answer[1])
    witnesses = []
    for normal in _normal_net(len(polys), intervals, nonnegative):
        if not any(normal):
            # The zero normal requires no support query; every feasible point suffices.
            point = vertices[0]
        else:
            answer = support(normal)
            if answer is None:
                return finish("unresolved", {"kind": "budget", "stage": "finite_normal_net"})
            stats["normal_grid_calls"] += 1
            if answer[0] > _dot(normal, query):
                return cut_result(normal, answer)
            point = answer[1]
        witnesses.append([str(x) for x in point])
    return finish("within_tolerance", {"kind": "finite_normal_net", "intervals": intervals,
                                      "support_error": str(support_error), "points": witnesses})


def replay_separation(result, features, symbols, box, query, *, rows=(), epsilon=Fraction(1, 100), nonnegative=()):
    """Check a certificate against trusted model/query/tolerance data.

    The numerical LP is not replayed or trusted.  Exact primitive polynomial and
    polytope routines are shared with generation; this is not formal verification.
    ``unresolved`` has no geometric assertion and is deliberately not a certificate.
    """
    try:
        if not isinstance(result, dict):
            return False
        polys, symbols, box, query, rows, epsilon, identity = _prepare(features, symbols, box, query, rows, epsilon, nonnegative)
        nonnegative = tuple(identity["nonnegative"])
        if result.get("schema") != SCHEMA or result.get("problem") != identity:
            return False
        witness = result["witness"]
        status = result["status"]
        module = _oracle_module()
        vertices = tuple(tuple(rational(x) for x in p) for p in module.polytope_vertices(box, rows))
        if status == "empty_domain":
            return witness == {"kind": "empty_polytope"} and not vertices
        if not vertices:
            return False
        feature_bounds = tuple(_poly_interval(p, box) for p in polys)
        if status == "within_tolerance" and witness["kind"] == "convex_combination":
            points = [tuple(rational(x) for x in p) for p in witness["points"]]
            weights = [rational(w) for w in witness["weights"]]
            if not points or len(points) != len(weights) or any(w < 0 for w in weights) or sum(weights) != 1:
                return False
            if not all(_feasible(p, box, rows) for p in points):
                return False
            values = [_evaluate(polys, p) for p in points]
            combination = tuple(sum((w * v[j] for w, v in zip(weights, values)), Fraction(0))
                                for j in range(len(polys)))
            distance = _distance(combination, query, nonnegative)
            return rational(witness["distance"]) == distance and distance <= epsilon
        if status == "within_tolerance" and witness["kind"] == "finite_normal_net":
            intervals = witness["intervals"]
            error = rational(witness["support_error"])
            if isinstance(intervals, bool) or not isinstance(intervals, int) or intervals < 1 or error < 0:
                return False
            radius = sum(max(abs(lo - q), abs(hi - q)) for (lo, hi), q in zip(feature_bounds, query))
            if error + 2 * radius / intervals > epsilon:
                return False
            if len(witness["points"]) != (intervals + 1) ** len(polys):
                return False
            for normal, encoded in zip(_normal_net(len(polys), intervals, nonnegative), witness["points"]):
                point = tuple(rational(x) for x in encoded)
                if not _feasible(point, box, rows) or _dot(normal, _evaluate(polys, point)) - _dot(normal, query) > error:
                    return False
            return True
        if status != "cut":
            return False
        cut = result["cut"]
        normal = tuple(rational(c) for c in cut["coefficients"])
        rhs = rational(cut["rhs"])
        if len(normal) != len(polys) or max(abs(c) for c in normal) > 1 or cut["orientation"] != ">=":
            return False
        if any(normal[i] < 0 for i in nonnegative):
            return False
        gap = rhs - _dot(normal, query)
        if gap <= 0 or rational(cut["query_gap"]) != gap:
            return False
        if witness["kind"] == "quadratic_support":
            if any(p.total_degree() > 2 for p in polys):
                return False
            coefficients = _quadratic_coefficients(polys, symbols, normal)
            certificate = witness["certificate"]
            if not module.replay_quadratic(box, rows, coefficients, certificate) or rational(certificate["bound"]) != rhs:
                return False
        elif witness["kind"] == "polynomial_net_support":
            denominator = witness["denominator"]
            if isinstance(denominator, bool) or not isinstance(denominator, int) or denominator < 1:
                return False
            lipschitz = sum(max(abs(lo), abs(hi)) for p in polys for x in symbols
                            for lo, hi in [_poly_interval(p.diff(x), box)])
            diameter = max(max(p[j] for p in vertices) - min(p[j] for p in vertices) for j in range(len(box)))
            error = lipschitz * diameter * (len(vertices) - 1) / denominator
            minimum = min(_dot(normal, _evaluate(polys, p)) for p in _domain_net(vertices, denominator))
            point = tuple(rational(x) for x in witness["minimizer"])
            if (rational(witness["error"]) != error or rhs != minimum - error
                    or not _feasible(point, box, rows) or _dot(normal, _evaluate(polys, point)) != minimum):
                return False
        else:
            return False
        return cut["binary64"] == _float_export(normal, rhs, feature_bounds, query)
    except (KeyError, TypeError, ValueError, OverflowError, ZeroDivisionError, IndexError, AttributeError):
        return False
