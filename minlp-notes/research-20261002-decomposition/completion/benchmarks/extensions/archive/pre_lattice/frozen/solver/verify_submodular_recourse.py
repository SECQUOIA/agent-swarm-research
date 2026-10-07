"""Replay mixed submodular recourse certificates without an optimizer.

Only rational arithmetic, PSD elimination, conditional box KKT checks, and
convex combinations of checked greedy bases are used. No LP, QP, label search,
or submodular-minimization routine is called.
"""
from fractions import Fraction as F
from math import ceil, floor

from certified_grid import BoxQP, rational


def _psd(a):
    a = [list(row) for row in a]
    while a:
        if any(a[i][i] < 0 for i in range(len(a))):
            return False
        pivot = next((i for i in range(len(a)) if a[i][i] > 0), None)
        if pivot is None:
            return all(v == 0 for row in a for v in row)
        rest = [i for i in range(len(a)) if i != pivot]
        a = [[a[i][j] - a[i][pivot] * a[pivot][j] / a[pivot][pivot]
              for j in rest] for i in rest]
    return True


def _coarse_bound(problem):
    result = problem.constant
    for i, (lo, hi) in enumerate(problem.bounds):
        a, b = problem.A[i][i], problem.b[i]
        candidates = [lo, hi]
        if a > 0:
            v = max(lo, min(hi, -b / a))
            candidates.extend((F(floor(v)), F(ceil(v))) if i in problem.integers else (v,))
        result += min(a * x * x / 2 + b * x for x in candidates)
    for i in range(len(problem.b)):
        for j in range(i):
            result += min(problem.A[i][j] * x * y
                          for x in problem.bounds[i] for y in problem.bounds[j])
    return result


def _indices(values, allowed):
    values = tuple(values)
    if len(set(values)) != len(values) or any(type(i) is not int or i not in allowed for i in values):
        raise ValueError("invalid coordinate indices")
    return values


def verify_submodular(certificate, problem=None):
    """Return whether the bound certificate is valid for the embedded/expected QP.

    An unsupported or capped result can still prove a useful interval. Status
    descriptions of unsupported subclasses and performance statistics are not
    mathematical claims checked by this function; its global bounds are.
    """
    try:
        if certificate["schema"] != "submodular-recourse-qp-v1":
            return False
        model = BoxQP.from_dict(certificate["problem"])
        if problem is not None and model.to_dict() != problem.to_dict():
            return False
        epsilon = rational(certificate["epsilon"])
        if epsilon < 0 or type(certificate["exact_requested"]) is not bool:
            return False
        point = tuple(map(rational, certificate["point"]))
        lower, upper, gap = (rational(certificate[key]) for key in ("lower", "upper", "gap"))
        if not model.feasible(point) or model.value(point) != upper or gap != upper - lower or gap < 0:
            return False
        certified_lower = _coarse_bound(model)
        proof = certificate["proof"]
        if proof is not None:
            active = {i for i, (lo, hi) in enumerate(model.bounds) if lo < hi}
            D = _indices(proof["concave"], active)
            C = tuple(i for i in sorted(active) if i not in D)
            if any(model.A[i][i] > 0 for i in D) or any(i in model.integers for i in C):
                return False
            if not _psd([[model.A[i][j] for j in C] for i in C]):
                return False
            entries = proof["flips"]
            if any(len(pair) != 2 for pair in entries):
                return False
            indices = _indices([pair[0] for pair in entries], active)
            if set(indices) != active:
                return False
            signs = dict(entries)
            if any(type(v) is not int or v not in (-1, 1) for v in signs.values()):
                return False
            if any(signs[i] * signs[j] * model.A[i][j] > 0
                   for i in active for j in active if i != j):
                return False
            queries = {}
            for item in proof["queries"]:
                label = _indices(item["label"], set(D))
                if tuple(sorted(label)) != label or label in queries:
                    return False
                chosen = set(label)
                x = tuple(map(rational, item["point"]))
                value = rational(item["value"])
                if not model.feasible(x) or model.value(x) != value:
                    return False
                if any(x[i] != model.bounds[i][int((i in chosen) == (signs[i] == 1))] for i in D):
                    return False
                for i in C:
                    gradient = model.b[i] + sum((a * v for a, v in zip(model.A[i], x)), F(0))
                    lo, hi = model.bounds[i]
                    if x[i] == lo:
                        if gradient < 0:
                            return False
                    elif x[i] == hi:
                        if gradient > 0:
                            return False
                    elif gradient:
                        return False
                queries[label] = value
            mixture = proof["mixture"]
            if mixture:
                if () not in queries:
                    return False
                positions = {i: j for j, i in enumerate(D)}
                w = [F(0)] * len(D)
                total = F(0)
                for entry in mixture:
                    permutation = _indices(entry["permutation"], set(D))
                    if set(permutation) != set(D):
                        return False
                    weight = rational(entry["weight"])
                    if weight <= 0:
                        return False
                    total += weight
                    label, previous = [], queries[()]
                    for i in permutation:
                        label.append(i)
                        value = queries[tuple(sorted(label))]
                        w[positions[i]] += weight * (value - previous)
                        previous = value
                if total != 1:
                    return False
                candidate = queries[()] + sum((min(F(0), v) for v in w), F(0))
                certified_lower = max(certified_lower, candidate)
        if lower != certified_lower:
            return False
        status = certificate["status"]
        if status == "exact":
            return gap == 0
        if status == "epsilon_optimal":
            return not certificate["exact_requested"] and gap <= epsilon
        return status in ("resource_limit", "unsupported")
    except (ValueError, TypeError, KeyError, IndexError, AttributeError, ZeroDivisionError, OverflowError):
        return False
