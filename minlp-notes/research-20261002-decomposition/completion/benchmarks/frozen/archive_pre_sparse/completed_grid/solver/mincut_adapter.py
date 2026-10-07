"""Certified minimum-cut recourse for a small continuous core of a BoxQP.

Residual diagonals must be nonpositive and residual edge signs must become
nonpositive after endpoint flips. Fixed variables are eliminated first. A
bounded search can find a continuous core by branching on conflicting signed
cycles; integer variables are never discretized as continuous core variables.
All nonfixed core intervals are normalized to [0, 1]. Residual integers use
their actual integer endpoints, so this supports arbitrary rational boxes.

The JSON-safe proof contains the original model, exact flow witnesses and the
complete adaptive-cell trace. Verification rebuilds normalization from that
model and checks witnesses without an optimization call. To bind a certificate
to an externally supplied instance, pass that instance to verify_mincut.
An unsupported class or exhausted budget returns a valid coarse enclosure.
Exact mode uses the recourse module's rational value-separation theorem; its
conservative height bound can require substantially more levels than additive
accuracy. This adapter makes no general small-core discovery or runtime claim.
"""

from __future__ import annotations

from collections import deque
from fractions import Fraction as F
import importlib.util
from itertools import product
from pathlib import Path
import sys

from certified_grid import BoxQP, interval_lower_bound, rational


def _load_recourse():
    name = "_minlp_endpoint_recourse"
    if name not in sys.modules:
        path = Path(__file__).resolve().parents[1] / "conditional-messages" / "mincut_recourse.py"
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
    return sys.modules[name]


_recourse = _load_recourse()
SCHEMA = "mincut-adapter-v1"


def _conflict_cycle(problem, core, check=None):
    """Return flips if balanced, otherwise vertices of one conflicting cycle."""
    residual = {i for i, (lo, hi) in enumerate(problem.bounds) if lo < hi and i not in core}
    adjacency = {i: [] for i in residual}
    for edge_index, (i, j, value) in enumerate(problem.interactions):
        if check is not None and edge_index % 256 == 0:
            check()
        if i in residual and j in residual:
            relation = -1 if value > 0 else 1
            adjacency[i].append((j, relation))
            adjacency[j].append((i, relation))
    flips, parents = {}, {}
    for root in sorted(residual):
        if root in flips:
            continue
        flips[root], parents[root] = 1, None
        pending = deque([root])
        while pending:
            if check is not None:
                check()
            i = pending.popleft()
            for j, relation in adjacency[i]:
                required = flips[i] * relation
                if j not in flips:
                    flips[j], parents[j] = required, i
                    pending.append(j)
                elif flips[j] != required:
                    left, right = [], []
                    node = i
                    while node is not None:
                        left.append(node)
                        node = parents[node]
                    node = j
                    while node not in left:
                        right.append(node)
                        node = parents[node]
                    return None, tuple(left[:left.index(node) + 1] + right)
    return flips, ()


def _discover(problem, max_core, max_nodes, check=None):
    active = {i for i, (lo, hi) in enumerate(problem.bounds) if lo < hi}
    mandatory = frozenset(i for i in active if problem.A[i][i] > 0)
    if mandatory & problem.integers:
        return None, None, "positive_diagonal_integer_residual"
    if len(mandatory) > max_core:
        return None, None, "core_size_limit"
    visited, exhausted = set(), False
    degree = {}
    for i in active:
        if check is not None:
            check()
        degree[i] = sum(bool(problem.A[i][j]) for j in active if j != i)

    def visit(core):
        nonlocal exhausted
        if check is not None:
            check()
        if core in visited:
            return None
        if len(visited) >= max_nodes:
            exhausted = True
            return None
        visited.add(core)
        flips, cycle = _conflict_cycle(problem, core, check)
        if flips is not None:
            return tuple(sorted(core)), flips
        if len(core) == max_core:
            return None
        candidates = sorted((i for i in cycle if i not in problem.integers),
                            key=lambda i: (-degree[i], i))
        for i in candidates:
            answer = visit(core | {i})
            if answer is not None:
                return answer
            if exhausted:
                break
        return None

    found = visit(mandatory)
    if found is None:
        return None, None, "core_search_limit" if exhausted else "no_supported_core"
    return *found, None


def _normalize(problem, core, check=None):
    if check is not None:
        check()
    active = tuple(i for i, (lo, hi) in enumerate(problem.bounds) if lo < hi)
    positions = {i: j for j, i in enumerate(active)}
    core_set = set(core)
    offsets = [lo if lo == hi or i in core_set else F(0)
               for i, (lo, hi) in enumerate(problem.bounds)]
    scales = {i: problem.bounds[i][1] - problem.bounds[i][0] if i in core_set else F(1)
              for i in active}
    diagonal = tuple(problem.A[i][i] * scales[i] ** 2 / 2 for i in active)
    linear = []
    for i in active:
        if check is not None:
            check()
        linear.append(scales[i] * (problem.b[i] + sum(
            (problem.A[i][j] * offsets[j] for j in range(len(offsets))), F(0))))
    edges = tuple((positions[i], positions[j], value * scales[i] * scales[j])
                  for i, j, value in problem.interactions if i in positions and j in positions)
    model = _recourse.Quadratic(diagonal, tuple(linear), edges, problem.value(offsets))
    bounds = tuple((F(0), F(1)) if i in core_set else problem.bounds[i] for i in active)
    integer_indices = tuple(positions[i] for i in active if i in problem.integers)
    return model, tuple(positions[i] for i in core), bounds, integer_indices, active, offsets, scales


def _lift(point, active, offsets, scales):
    original = list(offsets)
    for i, value in zip(active, point):
        original[i] += scales[i] * value
    return tuple(original)


def _bounded_search(model, core, bounds, flips, tolerance, max_levels, max_queries, integers, check=None):
    """The reference cell search with a check before each entire query batch."""
    k = len(core)
    if 2 ** k > max_queries:
        return None, "query_limit"
    curvature = max([F(0)] + [2 * model.diagonal[i] for i in core])
    offsets = tuple(product((0, 1), repeat=k))
    candidates, cache, trace = {tuple(0 for _ in core)}, {}, []
    lower, incumbent = None, None
    stop = "level_limit"
    for level in range(max_levels + 1):
        if check is not None:
            check()
        denominator = 2 ** level
        needed = set()
        over_budget = False
        for cell in candidates:
            if check is not None:
                check()
            for bits in offsets:
                corner = tuple(F(i + d, denominator) for i, d in zip(cell, bits))
                if corner not in cache:
                    needed.add(corner)
                    if len(cache) + len(needed) > max_queries:
                        over_budget = True
                        break
            if over_budget:
                break
        if over_budget:
            stop = "query_limit"
            break
        for corner in sorted(needed):
            if check is not None:
                check()
            certificate = _recourse.solve_recourse(
                model, dict(zip(core, corner)), bounds, flips, integers)
            if check is not None:
                check()
            cache[corner] = certificate
            if incumbent is None or certificate.value < incumbent.value:
                incumbent = certificate
        cell_values = {
            cell: min(cache[tuple(F(i + d, denominator) for i, d in zip(cell, bits))].value
                      for bits in offsets) for cell in candidates}
        error = F(k) * curvature / (8 * denominator ** 2)
        candidate_lower = min(cell_values.values()) - error
        lower = candidate_lower if lower is None else max(lower, candidate_lower)
        retained = {cell for cell, value in cell_values.items() if value - error <= incumbent.value}
        trace.append({"level": level, "generated": len(candidates), "retained": len(retained),
                      "new_queries": len(needed), "error": error, "lower": lower,
                      "upper": incumbent.value, "retained_cells": sorted(retained)})
        if incumbent.value - lower <= tolerance:
            stop = "complete"
            break
        if level != max_levels:
            # Check corners while generating children. A cell's lower corner
            # identifies it injectively, so this also caps the stored cells by
            # max_queries, even when a user permits a much larger core.
            next_candidates, next_needed = set(), set()
            over_budget = False
            for cell in sorted(retained):
                if check is not None:
                    check()
                for bits in offsets:
                    child = tuple(2 * i + d for i, d in zip(cell, bits))
                    for corner_bits in offsets:
                        corner = tuple(F(i + d, 2 * denominator)
                                       for i, d in zip(child, corner_bits))
                        if corner not in cache:
                            next_needed.add(corner)
                            if len(cache) + len(next_needed) > max_queries:
                                over_budget = True
                                break
                    if over_budget:
                        break
                    next_candidates.add(child)
                if over_budget:
                    break
            if over_budget:
                stop = "query_limit"
                break
            candidates = next_candidates
    if not trace:
        return None, stop
    return {"complete": incumbent.value - lower <= tolerance,
            "lower": lower, "upper": incumbent.value, "incumbent": incumbent,
            "trace": trace, "certificates": cache}, stop


def _serialize_search(search):
    certificates, incumbent_corner = [], None
    for corner, cert in sorted(search["certificates"].items()):
        certificates.append({"corner": list(map(str, corner)), "point": list(map(str, cert.point)),
                             "value": str(cert.value),
                             "flow": [[i, j, str(value)] for (i, j), value in sorted(cert.flow.items())],
                             "source_side": sorted(cert.source_side)})
        if cert is search["incumbent"]:
            incumbent_corner = list(map(str, corner))
    trace = []
    for row in search["trace"]:
        trace.append({**row, **{key: str(row[key]) for key in ("error", "lower", "upper")},
                      "retained_cells": [list(cell) for cell in row["retained_cells"]]})
    return {"complete": search["complete"], "lower": str(search["lower"]),
            "upper": str(search["upper"]), "incumbent_corner": incumbent_corner,
            "trace": trace, "certificates": certificates}


def _deserialize_search(data):
    if type(data["complete"]) is not bool:
        raise ValueError("invalid completion flag")
    certificates = {}
    for record in data["certificates"]:
        corner = tuple(map(rational, record["corner"]))
        if corner in certificates:
            raise ValueError("duplicate corner")
        flow = {}
        for i, j, value in record["flow"]:
            if type(i) is not int or type(j) is not int or (i, j) in flow:
                raise ValueError("invalid flow key")
            flow[i, j] = rational(value)
        side = record["source_side"]
        if any(type(i) is not int for i in side) or len(set(side)) != len(side):
            raise ValueError("invalid cut")
        certificates[corner] = _recourse.Certificate(tuple(map(rational, record["point"])),
            rational(record["value"]), flow, frozenset(side))
    trace = []
    for row in data["trace"]:
        for key in ("level", "generated", "retained", "new_queries"):
            if type(row[key]) is not int or row[key] < 0:
                raise ValueError("invalid trace counter")
        if any(any(type(i) is not int for i in cell) for cell in row["retained_cells"]):
            raise ValueError("invalid retained cell")
        trace.append({**row, **{key: rational(row[key]) for key in ("error", "lower", "upper")},
                      "retained_cells": [tuple(cell) for cell in row["retained_cells"]]})
    return {"complete": data["complete"], "lower": rational(data["lower"]),
            "upper": rational(data["upper"]), "trace": trace, "certificates": certificates,
            "incumbent": certificates[tuple(map(rational, data["incumbent_corner"]))]}


def _verify_search(model, core, bounds, flips, tolerance, result, integers):
    """Replay the reference proof, without allocating unused final children."""
    cache = result["certificates"]
    if not result["trace"] or 2 ** len(core) > len(cache):
        return False
    for corner, cert in cache.items():
        if len(corner) != len(core) or not _recourse.verify_recourse(
                model, dict(zip(core, corner)), bounds, flips, cert, integers):
            return False
    offsets = tuple(product((0, 1), repeat=len(core)))
    curvature = max([F(0)] + [2 * model.diagonal[i] for i in core])
    candidates, seen = {tuple(0 for _ in core)}, set()
    lower, upper = None, None
    for level, row in enumerate(result["trace"]):
        if row["level"] != level or row["generated"] != len(candidates):
            return False
        values, before = {}, len(seen)
        for cell in candidates:
            corners = [tuple(F(i + d, 2 ** level) for i, d in zip(cell, bits)) for bits in offsets]
            if any(corner not in cache for corner in corners):
                return False
            seen.update(corners)
            values[cell] = min(cache[corner].value for corner in corners)
            upper = values[cell] if upper is None else min(upper, values[cell])
        error = F(len(core)) * curvature / (8 * 2 ** (2 * level))
        candidate_lower = min(values.values()) - error
        lower = candidate_lower if lower is None else max(lower, candidate_lower)
        retained = {cell for cell, value in values.items() if value - error <= upper}
        if (row["error"] != error or row["lower"] != lower or row["upper"] != upper
                or row["new_queries"] != len(seen) - before or row["retained"] != len(retained)
                or row["retained_cells"] != sorted(retained)):
            return False
        if level + 1 < len(result["trace"]):
            candidates = set()
            for cell in retained:
                for bits in offsets:
                    candidates.add(tuple(2 * i + d for i, d in zip(cell, bits)))
                    # Every cell needs its distinct lower corner in the cache.
                    if len(candidates) > len(cache):
                        return False
    return (set(cache) == seen and result["incumbent"] in cache.values()
            and result["incumbent"].value == upper and result["lower"] == lower
            and result["upper"] == upper and result["complete"] == (upper - lower <= tolerance))


def _coarse(problem, epsilon, exact, core, flips, status, reason):
    point = tuple(lo for lo, _ in problem.bounds)
    lower, upper = interval_lower_bound(problem), problem.value(point)
    return {"schema": SCHEMA, "problem": problem.to_dict(), "core": list(core),
            "flips": [[i, sign] for i, sign in sorted(flips.items())],
            "epsilon": str(epsilon), "exact_requested": exact, "point": list(map(str, point)),
            "lower": str(lower), "upper": str(upper), "gap": str(upper - lower),
            "status": status, "reason": reason, "queries": 0, "proof": {"kind": "interval"}}


def solve_mincut(problem, epsilon, core=None, max_core=4, max_levels=12,
                 max_queries=10000, exact=False, check=None):
    """Return a JSON-safe exact or additive proof, or a bounded unfinished run.

    Optional check() runs between structural and oracle operations. Its
    exceptions propagate to the caller. A reference maxflow call and the final
    3^k exact face enumeration are each atomic.
    """
    if not isinstance(problem, BoxQP):
        raise TypeError("problem must be a BoxQP")
    epsilon = rational(epsilon)
    if epsilon < 0 or (epsilon == 0 and not exact):
        raise ValueError("positive epsilon required unless exact=True")
    if type(exact) is not bool:
        raise ValueError("exact must be boolean")
    if any(type(v) is not int or v < 0 for v in (max_core, max_levels)):
        raise ValueError("max_core and max_levels must be nonnegative integers")
    if type(max_queries) is not int or max_queries < 1:
        raise ValueError("max_queries must be positive")
    if check is not None:
        if not callable(check):
            raise ValueError("check must be callable")
        check()
    if core is None:
        core, flips, reason = _discover(problem, max_core, max_queries, check)
        if core is None:
            status = "resource_limit" if reason == "core_search_limit" else "unsupported"
            return _coarse(problem, epsilon, exact, (), {}, status, reason)
    else:
        core = tuple(core)
        if (any(type(i) is not int or not 0 <= i < len(problem.b) for i in core)
                or len(set(core)) != len(core) or set(core) & problem.integers):
            raise ValueError("core must contain distinct continuous coordinate indices")
        core = tuple(i for i in core if problem.bounds[i][0] < problem.bounds[i][1])
        if len(core) > max_core:
            return _coarse(problem, epsilon, exact, core, {}, "unsupported", "core_size_limit")
        if any(problem.A[i][i] > 0 and i not in core and lo < hi
               for i, (lo, hi) in enumerate(problem.bounds)):
            return _coarse(problem, epsilon, exact, core, {}, "unsupported", "positive_residual_diagonal")
        flips, cycle = _conflict_cycle(problem, set(core), check)
        if cycle:
            return _coarse(problem, epsilon, exact, core, {}, "unsupported", "residual_sign_conflict")
    model, normalized_core, bounds, integers, active, offsets, scales = _normalize(problem, core, check)
    positions = {i: j for j, i in enumerate(active)}
    normalized_flips = {positions[i]: sign for i, sign in flips.items()}
    denominator = _recourse.optimum_denominator_bound(model, normalized_core, bounds) if exact else None
    tolerance = F(1, 2 * denominator ** 2) if exact else epsilon
    search, reason = _bounded_search(model, normalized_core, bounds, normalized_flips,
                                     tolerance, max_levels, max_queries, integers, check)
    if search is None:
        return _coarse(problem, epsilon, exact, core, flips, "resource_limit", reason)
    point, lower, upper = search["incumbent"].point, search["lower"], search["upper"]
    status = "resource_limit"
    if search["complete"]:
        status = "epsilon_optimal"
        if exact:
            if check is not None:
                check()
            point, upper = _recourse._minimize_core_faces(model, normalized_core, point)
            if check is not None:
                check()
            lower, status = upper, "exact"
        elif lower == upper:
            status = "exact"
    proof = {"kind": "search", "tolerance": str(tolerance), "search": _serialize_search(search)}
    if denominator is not None:
        proof["denominator_bound"] = str(denominator)
    lifted = _lift(point, active, offsets, scales)
    return {"schema": SCHEMA, "problem": problem.to_dict(), "core": list(core),
            "flips": [[i, sign] for i, sign in sorted(flips.items())], "epsilon": str(epsilon),
            "exact_requested": exact, "point": list(map(str, lifted)), "lower": str(lower),
            "upper": str(upper), "gap": str(upper - lower), "status": status, "reason": reason,
            "queries": len(search["certificates"]), "proof": proof}


def verify_mincut(certificate, problem=None):
    """Return bool; never call maxflow, face enumeration, or another optimizer.

    With problem supplied, its canonical serialized model must match exactly.
    Without it, verification certifies only the instance embedded in the proof.
    """
    try:
        return _verify_mincut(certificate, problem)
    except (ValueError, TypeError, KeyError, IndexError, ZeroDivisionError, OverflowError):
        return False


def _verify_mincut(cert, expected):
    if cert["schema"] != SCHEMA or type(cert["exact_requested"]) is not bool:
        return False
    problem = BoxQP.from_dict(cert["problem"])
    if expected is not None and problem.to_dict() != expected.to_dict():
        return False
    epsilon, exact = rational(cert["epsilon"]), cert["exact_requested"]
    if epsilon < 0 or (epsilon == 0 and not exact):
        return False
    point = tuple(map(rational, cert["point"]))
    lower, upper, gap = (rational(cert[key]) for key in ("lower", "upper", "gap"))
    if not problem.feasible(point) or problem.value(point) != upper or gap != upper - lower or gap < 0:
        return False
    if type(cert["queries"]) is not int or cert["queries"] < 0:
        return False
    proof = cert["proof"]
    if proof["kind"] == "interval":
        return (cert["status"] in ("unsupported", "resource_limit") and cert["queries"] == 0
                and lower == interval_lower_bound(problem))
    if proof["kind"] != "search":
        return False
    core = tuple(cert["core"])
    if (any(type(i) is not int or not 0 <= i < len(problem.b) for i in core)
            or len(set(core)) != len(core) or set(core) & problem.integers
            or any(problem.bounds[i][0] == problem.bounds[i][1] for i in core)):
        return False
    flips = {}
    for i, sign in cert["flips"]:
        if type(i) is not int or type(sign) is not int or i in flips or sign not in (-1, 1):
            return False
        flips[i] = sign
    model, normalized_core, bounds, integers, active, offsets, scales = _normalize(problem, core)
    positions = {i: j for j, i in enumerate(active)}
    if set(flips) != set(active) - set(core):
        return False
    normalized_flips = {positions[i]: sign for i, sign in flips.items()}
    tolerance = rational(proof["tolerance"])
    denominator = _recourse.optimum_denominator_bound(model, normalized_core, bounds) if exact else None
    if exact:
        if rational(proof["denominator_bound"]) != denominator or tolerance != F(1, 2 * denominator ** 2):
            return False
    elif tolerance != epsilon:
        return False
    search = _deserialize_search(proof["search"])
    if cert["queries"] != len(search["certificates"]) or not _verify_search(
            model, normalized_core, bounds, normalized_flips, tolerance, search, integers):
        return False
    normalized_point = tuple((point[i] - offsets[i]) / scales[i] for i in active)
    if exact and search["complete"]:
        # Both an optimum and this feasible value have denominator at most D.
        # Distinct such rationals are separated by at least 1/D^2.
        return (cert["status"] == "exact" and lower == upper
                and model.value(normalized_point) == upper and upper.denominator <= denominator
                and search["lower"] <= upper <= search["upper"]
                and search["upper"] - search["lower"] < F(1, denominator ** 2))
    if point != _lift(search["incumbent"].point, active, offsets, scales):
        return False
    if lower != search["lower"] or upper != search["upper"]:
        return False
    status = "resource_limit" if not search["complete"] else "exact" if gap == 0 else "epsilon_optimal"
    return cert["status"] == status
