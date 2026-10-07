"""Independent exact replay and membership for compact box-QP optimal sets.

This verifier imports the input model, but never the producer, optimizer,
grid algorithm, or an LP solver.  Its KKT, PSD, Bellman, and support checks
use rational arithmetic.  Resource caps also apply to untrusted artifacts.
"""

from fractions import Fraction as F
from itertools import product
from math import prod

from certified_grid import BoxQP, rational


class CertificateError(ValueError):
    pass


def _require(condition, message):
    if not condition:
        raise CertificateError(message)


def _psd(matrix, check):
    a = [list(row) for row in matrix]
    for k in range(len(a)):
        check()
        pivot = a[k][k]
        if pivot < 0:
            return False
        if pivot == 0:
            if any(a[i][k] for i in range(k + 1, len(a))):
                return False
            continue
        for i in range(k + 1, len(a)):
            for j in range(i, len(a)):
                a[i][j] -= a[i][k] * a[k][j] / pivot
                a[j][i] = a[i][j]
    return True


def _table(rows, lengths):
    expected = set(product(*(range(length) for length in lengths)))
    table = {}
    for row in rows:
        state = tuple(row["state"])
        _require(all(type(k) is int for k in state), "noninteger table label")
        _require(state in expected and state not in table, "invalid/duplicate table state")
        table[state] = rational(row["value"])
    _require(set(table) == expected, "incomplete table")
    return table


def _verify(certificate, expected_problem, max_table_states, check):
    _require(certificate["schema"] == "box-qp-optimal-set-v1", "unknown schema")
    problem = BoxQP.from_dict(certificate["problem"])
    if expected_problem is not None:
        _require(problem.to_dict() == expected_problem.to_dict(), "certificate binds a different problem")
    point = tuple(map(rational, certificate["point"]))
    _require(problem.feasible(point), "infeasible attaining point")
    minimum = rational(certificate["minimum"])
    _require(problem.value(point) == minimum, "incorrect claimed minimum at attaining point")
    active = tuple(i for i, (lo, hi) in enumerate(problem.bounds) if lo != hi)
    kind = certificate["kind"]
    if kind == "diagonal":
        _require(not (problem.integers & set(active)), "nonfixed integer variable in continuous certificate")
        _require(certificate["active"] == list(active), "incorrect active coordinates")
        diagonal = tuple(map(rational, certificate["diagonal"]))
        _require(len(diagonal) == len(active), "wrong diagonal size")
        for i, shift in zip(active, diagonal):
            check()
            lo, hi = problem.bounds[i]
            grad = problem.b[i] + sum((problem.A[i][j] * point[j]
                                      for j in range(len(point))), F(0))
            if point[i] == lo:
                _require(grad >= 0 and shift == 2 * grad / (hi - lo), "lower-bound KKT/shift failure")
            elif point[i] == hi:
                _require(grad <= 0 and shift == -2 * grad / (hi - lo), "upper-bound KKT/shift failure")
            else:
                _require(grad == 0 and shift == 0, "interior KKT/shift failure")
        matrix = [[problem.A[i][j] + (diagonal[k] if i == j else 0)
                   for j in active] for k, i in enumerate(active)]
        _require(_psd(matrix, check), "shifted Hessian is not positive semidefinite")
        return problem, point, minimum, {"active": active, "diagonal": diagonal, "matrix": matrix}
    _require(kind == "endpoint", "unknown certificate kind")
    _require(all(problem.A[i][i] <= 0 for i in active), "positive active diagonal")
    grids = tuple(tuple(dict.fromkeys(pair)) for pair in problem.bounds)
    work = sum(prod(len(grids[i]) for i in bag) for bag in problem.bags)
    _require(work <= max_table_states, "verification table limit")
    _require(len(certificate["messages"]) == len(problem.bags)
             and len(certificate["residuals"]) == len(problem.bags), "wrong number of bag tables")
    separators, messages, residuals = [], [], []
    for t, bag in enumerate(problem.bags):
        check()
        parent = problem.parents[t]
        separator = tuple(sorted(set(bag) & set(problem.bags[parent]))) if parent is not None else ()
        separators.append(separator)
        messages.append(_table(certificate["messages"][t], [len(grids[i]) for i in separator]))
        residuals.append(_table(certificate["residuals"][t], [len(grids[i]) for i in bag]))
    for t, bag in enumerate(problem.bags):
        attained = {s: False for s in messages[t]}
        for state, residual in residuals[t].items():
            check()
            labels = dict(zip(bag, state))
            values = {i: grids[i][k] for i, k in labels.items()}
            local = problem.constant if t == 0 else F(0)
            for i, home in enumerate(problem.home):
                if home == t:
                    local += problem.A[i][i] * values[i] ** 2 / 2 + problem.b[i] * values[i]
            for (i, j, coefficient), home in zip(problem.interactions, problem.factor_home):
                if home == t:
                    local += coefficient * values[i] * values[j]
            for child in problem.neighbors[t]:
                if problem.parents.get(child) == t:
                    local += messages[child][tuple(labels[i] for i in separators[child])]
            sep = tuple(labels[i] for i in separators[t])
            _require(residual == local - messages[t][sep] and residual >= 0,
                     "incorrect or negative Bellman residual")
            attained[sep] |= residual == 0
        _require(all(attained.values()), "Bellman minimum is not attained")
    _require(messages[0][()] == minimum, "root message differs from claimed minimum")
    return problem, point, minimum, {"grids": grids, "residuals": residuals}


def verify_certificate(certificate, problem=None, *, max_table_states=1000000, check=None):
    """Raise CertificateError on failure; return exact minimum and one optimizer."""
    try:
        _, point, minimum, _ = _verify(certificate, problem, max_table_states, check or (lambda: None))
        return {"valid": True, "minimum": minimum, "point": point}
    except CertificateError:
        raise
    except (KeyError, TypeError, ValueError, IndexError, ZeroDivisionError) as exc:
        raise CertificateError("malformed optimal-set certificate") from exc


def contains(certificate, point, problem=None, *, max_table_states=1000000, check=None):
    """Replay the certificate, then evaluate its factored full-set equations."""
    try:
        model, anchor, _, data = _verify(certificate, problem, max_table_states, check or (lambda: None))
        point = tuple(map(rational, point))
        if not model.feasible(point):
            return False
        if certificate["kind"] == "diagonal":
            active = data["active"]
            displacement = [point[i] - anchor[i] for i in active]
            if any(sum((a * x for a, x in zip(row, displacement)), F(0))
                   for row in data["matrix"]):
                return False
            return all(not shift * (point[i] - model.bounds[i][0]) * (model.bounds[i][1] - point[i])
                       for i, shift in zip(active, data["diagonal"]))
        if any(model.A[i][i] < 0 and lo < point[i] < hi
               for i, (lo, hi) in enumerate(model.bounds)):
            return False
        for bag, rows in zip(model.bags, data["residuals"]):
            for state, residual in rows.items():
                if residual > 0:
                    supported = True
                    for i, label in zip(bag, state):
                        lo, hi = model.bounds[i]
                        if lo != hi and (point[i] == hi if label == 0 else point[i] == lo):
                            supported = False
                            break
                    if supported:
                        return False
        return True
    except CertificateError:
        raise
    except (KeyError, TypeError, ValueError, IndexError, ZeroDivisionError) as exc:
        raise CertificateError("malformed optimal-set certificate or point") from exc
