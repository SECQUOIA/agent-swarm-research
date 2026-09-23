"""Numerical phase I with independently checked exact rational Farkas cuts.

This is a certificate-recovery implementation of classical linear projection
duality, not a new separation theorem. Failure to recover a certificate is
explicit and never converted into a claim of exact infeasibility.
"""

from dataclasses import dataclass
from fractions import Fraction as F

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix

from network_simplex.separator import Cut
from .model import rational


@dataclass
class CertificateResult:
    status: str
    cut: Cut | None = None
    multipliers: tuple | None = None
    phase_one_value: float | None = None
    reconstruction: str | None = None


def inequalities(model):
    """All exact model inequalities a_orig*v+a_aux*h <= rhs."""
    rows = list(model.ub)
    for terms, rhs in model.eq:
        rows.append((terms, rhs))
        rows.append(({k: -v for k, v in terms.items()}, -rhs))
    for k, (lo, hi) in enumerate(model.bounds):
        if hi is not None:
            rows.append(({k: F(1)}, hi))
        if lo is not None:
            rows.append(({k: F(-1)}, -lo))
    return rows


def _repair_kernel(columns, approximate):
    """Exact RREF, keeping numerical free coordinates when the kernel is large."""
    count = len(columns)
    auxiliary = sorted({k for column in columns for k in column})
    rows = [[column.get(k, F(0)) for column in columns] + [F(0)] for k in auxiliary]
    rows.append([F(1)] * count + [F(1)])
    rank, pivots = 0, []
    for column in range(count):
        pivot = next((i for i in range(rank, len(rows)) if rows[i][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        scale = rows[rank][column]
        rows[rank] = [v/scale for v in rows[rank]]
        for i in range(len(rows)):
            if i != rank and rows[i][column]:
                scale = rows[i][column]
                rows[i] = [v-scale*w for v, w in zip(rows[i], rows[rank])]
        pivots.append(column); rank += 1
    if any(not any(row[:-1]) and row[-1] for row in rows):
        return None
    free = set(range(count)) - set(pivots)
    result = [rational(float(v)).limit_denominator(10**8) if i in free else F(0)
              for i, v in enumerate(approximate)]
    for i, p in enumerate(pivots):
        result[p] = rows[i][-1] - sum((rows[i][j]*result[j] for j in free), F(0))
    return result


def separate(model, point):
    """Return a verified violated cut, or an explicit noncertifying status.

    Exactness applies only to a returned cut and its checked nonnegative
    multipliers. ``numerically_feasible`` is not an exact membership statement.
    Fractions represent the caller's decimal float text when floats are passed.
    """
    E, m = len(model.arcs), model.simplex_size
    if len(point.x) != E or len(point.y) != m or set(point.z) != set(model.observations):
        raise ValueError("Point dimensions or observation keys do not match")
    values = tuple(map(rational, tuple(point.x)+tuple(point.y)+tuple(point.z[o] for o in model.observations)))
    rows = inequalities(model)
    auxiliary_n = model.n-model.original_n
    ii, jj, vv, residual = [], [], [], []
    for i, (terms, rhs) in enumerate(rows):
        residual.append(rhs-sum((a*values[k] for k, a in terms.items() if k < model.original_n), F(0)))
        for k, a in terms.items():
            if k >= model.original_n:
                ii.append(i); jj.append(k-model.original_n); vv.append(float(a))
        ii.append(i); jj.append(auxiliary_n); vv.append(-1.)
    matrix = coo_matrix((vv, (ii, jj)), shape=(len(rows), auxiliary_n+1)).tocsr()
    objective = np.zeros(auxiliary_n+1); objective[-1] = 1.
    lp = linprog(objective, A_ub=matrix, b_ub=np.asarray(residual, dtype=float),
                 bounds=[(None, None)]*auxiliary_n+[(0., None)], method="highs")
    if not lp.success:
        return CertificateResult("solver_failure")
    if lp.fun <= 0:
        return CertificateResult("numerically_feasible", phase_one_value=lp.fun)
    numerical = -lp.ineqlin.marginals
    support = [i for i, v in enumerate(numerical) if v > 0]
    multipliers = [rational(float(numerical[i])).limit_denominator(10**8) for i in support]
    columns = [{k: a for k, a in rows[i][0].items() if k >= model.original_n} for i in support]

    def valid(weights):
        if weights is None or any(w < 0 for w in weights):
            return False
        total = {}
        for column, w in zip(columns, weights):
            for k, a in column.items():
                total[k] = total.get(k, F(0)) + a*w
        return not any(total.values()) and sum((w*residual[i] for i, w in zip(support, weights)), F(0)) < 0

    reconstruction = "rationalized dual"
    if not valid(multipliers):
        multipliers = _repair_kernel(columns, [numerical[i] for i in support])
        reconstruction = "exact kernel repair"
    if not valid(multipliers):
        return CertificateResult("uncertified_outside", phase_one_value=lp.fun)
    coefficients, constant = {}, F(0)
    for i, weight in zip(support, multipliers):
        terms, rhs = rows[i]; constant -= weight*rhs
        for k, a in terms.items():
            if k >= model.original_n:
                continue
            key = ("x", k) if k < E else (("y", k-E) if k < E+m else ("z", *model.observations[k-E-m]))
            coefficients[key] = coefficients.get(key, F(0)) + weight*a
    cut = Cut({k: a for k, a in coefficients.items() if a}, constant, "exact verified phase-I Farkas cut")
    exact_point = type("ExactPoint", (), {"x": values[:E], "y": values[E:E+m],
                                         "z": dict(zip(model.observations, values[E+m:]))})()
    assert cut.evaluate(exact_point) > 0
    return CertificateResult("certified_outside", cut, tuple(zip(support, multipliers)), lp.fun, reconstruction)
