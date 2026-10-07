"""Exact, capped rational LP and convex box-QP oracles.

The LP uses two-phase simplex with Bland's rule. Its output includes primal/dual
or Farkas witnesses checked independently of the pivot algorithm. The QP uses
exact PSD/KKT checks and capped active-face search; no polynomial running-time
claim is made for either implementation. All objectives are minimized.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as F
from itertools import product
from math import isfinite


def _q(x):
    if isinstance(x, bool) or not isinstance(x, (int, str, F)):
        raise ValueError("exact data must be integers, strings, or Fractions")
    return F(x)


def _dot(a, b):
    return sum((x * y for x, y in zip(a, b)), F(0))


def _matrix(a, rows, n, name):
    if a is None:
        if rows:
            raise ValueError(name + " is missing")
        return []
    a = [list(map(_q, row)) for row in a]
    if len(a) != rows or any(len(row) != n for row in a):
        raise ValueError(name + " has wrong dimensions")
    return a


def _lp_data(c, A_ub, b_ub, A_eq, b_eq, bounds):
    c = tuple(map(_q, c))
    n = len(c)
    h = list(map(_q, [] if b_ub is None else b_ub))
    f = list(map(_q, [] if b_eq is None else b_eq))
    g = _matrix(A_ub, len(h), n, "A_ub")
    e = _matrix(A_eq, len(f), n, "A_eq")
    if bounds is None:
        bounds = [(None, None)] * n
    bounds = list(bounds)
    if len(bounds) != n or any(len(pair) != 2 for pair in bounds):
        raise ValueError("bounds have wrong dimensions")
    for i, (lo, hi) in enumerate(bounds):
        # Empty bounds are represented as inequalities, so infeasibility gets
        # a Farkas certificate just like any other contradictory rows.
        for endpoint, sign in ((lo, -1), (hi, 1)):
            if endpoint is not None:
                row = [F(0)] * n
                row[i] = F(sign)
                g.append(row)
                h.append(sign * _q(endpoint))
    return c, g, h, e, f


@dataclass(frozen=True)
class LPResult:
    status: str
    x: tuple | None = None
    value: F | None = None
    certificate: dict | None = None
    pivots: int = 0
    reason: str = ""


class _PivotLimit(Exception):
    pass


class _Simplex:
    def __init__(self, rows, rhs, basis, max_pivots, check):
        self.rows, self.rhs, self.basis = rows, rhs, basis
        self.transform = [[F(i == j) for j in range(len(rows))]
                          for i in range(len(rows))]
        self.max_pivots, self.pivots = max_pivots, 0
        self.check = check

    def pivot(self, r, j):
        if self.check is not None:
            self.check()
        if self.pivots >= self.max_pivots:
            raise _PivotLimit
        self.pivots += 1
        a = self.rows[r][j]
        self.rows[r] = [v / a for v in self.rows[r]]
        self.rhs[r] /= a
        self.transform[r] = [v / a for v in self.transform[r]]
        for i in range(len(self.rows)):
            if i != r and self.rows[i][j]:
                a = self.rows[i][j]
                self.rows[i] = [v - a * w for v, w in zip(self.rows[i], self.rows[r])]
                self.rhs[i] -= a * self.rhs[r]
                self.transform[i] = [v - a * w for v, w in
                                     zip(self.transform[i], self.transform[r])]
        self.basis[r] = j

    def run(self, cost):
        while True:
            if self.check is not None:
                self.check()
            basic = set(self.basis)
            entering = next((j for j in range(len(cost)) if j not in basic
                             and cost[j] - sum((cost[b] * row[j] for b, row in
                                                zip(self.basis, self.rows)), F(0)) < 0), None)
            if entering is None:
                return "optimal", None
            eligible = [i for i, row in enumerate(self.rows) if row[entering] > 0]
            if not eligible:
                return "unbounded", entering
            leaving = min(eligible, key=lambda i: (self.rhs[i] / self.rows[i][entering],
                                                  self.basis[i]))
            self.pivot(leaving, entering)

    def point(self, n):
        x = [F(0)] * n
        for b, v in zip(self.basis, self.rhs):
            x[b] = v
        return x

    def dual(self, cost, m):
        return [sum((cost[b] * row[j] for b, row in
                     zip(self.basis, self.transform)), F(0)) for j in range(m)]


def solve_lp(c, A_ub=None, b_ub=None, A_eq=None, b_eq=None, bounds=None,
             max_pivots=10000, check=None):
    """Minimize c'x with Gx<=h, Ex=f and optional (lower, upper) bounds.

    Missing bounds mean unrestricted variables; None endpoints are allowed.
    Status is optimal, infeasible, unbounded, or limit. A limit is not an
    infeasibility conclusion. Certificates include bound-row multipliers after
    supplied inequality rows, in coordinate order (lower then upper).
    """
    if type(max_pivots) is not int or max_pivots < 0:
        raise ValueError("max_pivots must be a nonnegative integer")
    c, g, h, e, f = _lp_data(c, A_ub, b_ub, A_eq, b_eq, bounds)
    n, k, m = len(c), len(g), len(g) + len(e)
    original = g + e
    rhs = h + f
    signs = [F(1 if v >= 0 else -1) for v in rhs]
    base_cols = 2 * n + k
    rows = []
    for i, row in enumerate(original):
        s = signs[i]
        rows.append([s * v for v in row] + [-s * v for v in row]
                    + [s if j == i else F(0) for j in range(k)]
                    + [F(i == j) for j in range(m)])
    tableau = _Simplex(rows, list(map(abs, rhs)), list(range(base_cols, base_cols + m)),
                       max_pivots, check)
    phase_one = [F(0)] * base_cols + [F(1)] * m

    def multipliers(cost):
        y = tableau.dual(cost, m)
        lam = tuple(-signs[i] * y[i] for i in range(k))
        mu = tuple(-signs[i] * y[i] for i in range(k, m))
        return {"inequality_multipliers": lam, "equality_multipliers": mu}

    try:
        state, _ = tableau.run(phase_one)
        assert state == "optimal", "phase I cannot be unbounded"
        phase_value = sum((phase_one[b] * v for b, v in
                           zip(tableau.basis, tableau.rhs)), F(0))
        if phase_value:
            result = LPResult("infeasible", certificate=multipliers(phase_one),
                              pivots=tableau.pivots)
        else:
            # Zero artificial basics are pivoted out or their redundant row
            # removed. Row transformations retain every original row's column.
            i = 0
            while i < len(tableau.rows):
                if tableau.basis[i] >= base_cols:
                    basic = set(tableau.basis)
                    j = next((j for j in range(base_cols)
                              if j not in basic and tableau.rows[i][j]), None)
                    if j is None:
                        del tableau.rows[i], tableau.rhs[i], tableau.basis[i], tableau.transform[i]
                        continue
                    tableau.pivot(i, j)
                i += 1
            tableau.rows = [row[:base_cols] for row in tableau.rows]
            cost = list(c) + [-v for v in c] + [F(0)] * k
            state, entering = tableau.run(cost)
            canonical_x = tableau.point(base_cols)
            x = tuple(canonical_x[i] - canonical_x[n + i] for i in range(n))
            if state == "optimal":
                result = LPResult("optimal", x, _dot(c, x), multipliers(cost), tableau.pivots)
            else:
                direction = [F(0)] * base_cols
                direction[entering] = F(1)
                for b, row in zip(tableau.basis, tableau.rows):
                    direction[b] = -row[entering]
                ray = tuple(direction[i] - direction[n + i] for i in range(n))
                result = LPResult("unbounded", x, _dot(c, x), {"ray": ray}, tableau.pivots)
    except _PivotLimit:
        return LPResult("limit", pivots=tableau.pivots, reason="max_pivots")
    if not _verify_lp_data(c, g, h, e, f, result):
        raise ArithmeticError("internal simplex certificate verification failed")
    return result


def _verify_lp_data(c, g, h, e, f, result):
    if result.status in ("optimal", "unbounded"):
        if result.x is None or len(result.x) != len(c):
            return False
        x = tuple(map(_q, result.x))
        if any(_dot(row, x) > b for row, b in zip(g, h)):
            return False
        if any(_dot(row, x) != b for row, b in zip(e, f)):
            return False
        if result.value != _dot(c, x):
            return False
    if result.status in ("optimal", "infeasible"):
        lam = tuple(map(_q, result.certificate["inequality_multipliers"]))
        mu = tuple(map(_q, result.certificate["equality_multipliers"]))
        if len(lam) != len(g) or len(mu) != len(e) or any(v < 0 for v in lam):
            return False
        stationarity = [sum((v * row[j] for v, row in zip(lam, g)), F(0))
                        + sum((v * row[j] for v, row in zip(mu, e)), F(0))
                        for j in range(len(c))]
        dual_rhs = _dot(lam, h) + _dot(mu, f)
        if result.status == "infeasible":
            return all(v == 0 for v in stationarity) and dual_rhs < 0
        return (all(v + cj == 0 for v, cj in zip(stationarity, c))
                and result.value == -dual_rhs)
    if result.status == "unbounded":
        ray = tuple(map(_q, result.certificate["ray"]))
        return (len(ray) == len(c) and _dot(c, ray) < 0
                and all(_dot(row, ray) <= 0 for row in g)
                and all(_dot(row, ray) == 0 for row in e))
    return False


def verify_lp_result(c, result, A_ub=None, b_ub=None, A_eq=None, b_eq=None, bounds=None):
    """Check a result without simplex, floating point, or an optimization call."""
    try:
        return _verify_lp_data(*_lp_data(c, A_ub, b_ub, A_eq, b_eq, bounds), result)
    except (ValueError, TypeError, KeyError, AttributeError, ZeroDivisionError):
        return False


def is_psd(matrix, check=None):
    """Exact symmetric Schur-complement test, including singular matrices."""
    a = [list(map(_q, row)) for row in matrix]
    n = len(a)
    if any(len(row) != n for row in a):
        return False
    if any(a[i][j] != a[j][i] for i in range(n) for j in range(n)):
        return False
    while a:
        if check is not None:
            check()
        if any(a[i][i] < 0 for i in range(len(a))):
            return False
        pivot = next((i for i in range(len(a)) if a[i][i] > 0), None)
        if pivot is None:
            return all(v == 0 for row in a for v in row)
        other = [i for i in range(len(a)) if i != pivot]
        a = [[a[i][j] - a[i][pivot] * a[pivot][j] / a[pivot][pivot]
              for j in other] for i in other]
    return True


def _nonsingular_solve(a, b, check=None):
    n = len(b)
    aug = [list(row) + [v] for row, v in zip(a, b)]
    for j in range(n):
        if check is not None:
            check()
        pivot = next((i for i in range(j, n) if aug[i][j]), None)
        if pivot is None:
            return None
        aug[j], aug[pivot] = aug[pivot], aug[j]
        divisor = aug[j][j]
        aug[j] = [v / divisor for v in aug[j]]
        for i in range(n):
            if i != j and aug[i][j]:
                aij = aug[i][j]
                aug[i] = [v - aij * w for v, w in zip(aug[i], aug[j])]
    return tuple(row[-1] for row in aug)


def solve_nonsingular(matrix, rhs, check=None):
    """Solve a square rational system; return None if its matrix is singular.

    Singularity returns None whether the system is consistent or inconsistent.
    Rectangular systems are rejected; use solve_lp for bounded feasibility.
    """
    rhs = tuple(map(_q, rhs))
    matrix = _matrix(matrix, len(rhs), len(rhs), "matrix")
    return _nonsingular_solve(matrix, rhs, check)


@dataclass(frozen=True)
class QPResult:
    status: str
    x: tuple | None = None
    value: F | None = None
    certificate: dict | None = None
    faces: int = 0
    pivots: int = 0
    reason: str = ""


def _qp_data(H, c, bounds, constant):
    c = tuple(map(_q, c))
    h = _matrix(H, len(c), len(c), "H")
    bounds = tuple(tuple(map(_q, pair)) for pair in bounds)
    if len(bounds) != len(c) or any(len(pair) != 2 or pair[0] > pair[1] for pair in bounds):
        raise ValueError("QP requires nonempty finite rational bounds")
    if any(h[i][j] != h[j][i] for i in range(len(c)) for j in range(len(c))):
        raise ValueError("H must be symmetric")
    return h, c, bounds, _q(constant)


def _qp_certificate(h, c, bounds, x):
    grad = tuple(_dot(row, x) + ci for row, ci in zip(h, c))
    lower, upper = [], []
    for xi, (lo, hi), gi in zip(x, bounds, grad):
        if not lo <= xi <= hi:
            return None
        if xi == lo and gi >= 0:
            lower.append(gi)
            upper.append(F(0))
        elif xi == hi and gi <= 0:
            lower.append(F(0))
            upper.append(-gi)
        elif gi == 0:
            lower.append(F(0))
            upper.append(F(0))
        else:
            return None
    return {"lower_multipliers": tuple(lower), "upper_multipliers": tuple(upper)}


def _proposed_faces(h, c, bounds):
    """Untrusted floating coordinate descent only proposes active faces."""
    n = len(c)
    try:
        hf = [[float(v) for v in row] for row in h]
        cf = list(map(float, c))
        bf = [(float(lo), float(hi)) for lo, hi in bounds]
        if not all(isfinite(v) for row in hf for v in row):
            return
        if not all(isfinite(v) for v in cf) or not all(isfinite(v) for pair in bf for v in pair):
            return
        for start in (0, -1, 1):
            x = [(lo + hi) / 2 if start == 0 else lo if start == -1 else hi for lo, hi in bf]
            for _ in range(50):
                old = x[:]
                for i, (lo, hi) in enumerate(bf):
                    linear = cf[i] + sum(hf[i][j] * x[j] for j in range(n) if j != i)
                    if hf[i][i] > 0:
                        x[i] = min(hi, max(lo, -linear / hf[i][i]))
                    elif linear:
                        x[i] = lo if linear > 0 else hi
                if x == old:
                    break
            if all(isfinite(v) for v in x):
                yield tuple(-1 if xi == lo else 1 if xi == hi else 0
                            for xi, (lo, hi) in zip(x, bf))
    except (OverflowError, ZeroDivisionError):
        return


def solve_convex_box_qp(H, c, bounds, constant=0, max_faces=10000, max_pivots=10000, check=None):
    """Solve min 1/2 x'Hx+c'x+constant on a finite rational box, H PSD.

    Numerical proposals are optional hints; acceptance is exact PSD/KKT.
    Active-face enumeration handles singular Hessians using exact LP. Its
    worst-case face count is exponential. Resource caps return status limit.
    """
    if type(max_faces) is not int or max_faces < 0 or type(max_pivots) is not int or max_pivots < 0:
        raise ValueError("caps must be nonnegative integers")
    h, c, bounds, constant = _qp_data(H, c, bounds, constant)
    if not is_psd(h, check):
        return QPResult("not_convex", reason="H is not positive semidefinite")
    n = len(c)
    seen, count, pivots = set(), 0, 0
    from itertools import chain
    choices = [(-1,) if lo == hi else (0, -1, 1) for lo, hi in bounds]
    for face in chain(_proposed_faces(h, c, bounds), product(*choices)):
        if check is not None:
            check()
        # Fixed variables have only one face representation.
        face = tuple(-1 if bounds[i][0] == bounds[i][1] else v for i, v in enumerate(face))
        if face in seen:
            continue
        if count >= max_faces:
            return QPResult("limit", faces=count, pivots=pivots, reason="max_faces")
        seen.add(face)
        count += 1
        free = [i for i, state in enumerate(face) if state == 0]
        active = [i for i, state in enumerate(face) if state != 0]
        x = [F(0)] * n
        for i in active:
            x[i] = bounds[i][0 if face[i] == -1 else 1]
        matrix = [[h[i][j] for j in free] for i in free]
        rhs = [-c[i] - sum((h[i][j] * x[j] for j in active), F(0)) for i in free]
        xf = _nonsingular_solve(matrix, rhs, check)
        if xf is None:
            g, b = [], []
            for i in active:
                if bounds[i][0] == bounds[i][1]:
                    continue  # either multiplier may absorb this gradient
                sign = -1 if face[i] == -1 else 1
                g.append([sign * h[i][j] for j in free])
                b.append(-sign * (c[i] + sum((h[i][j] * x[j] for j in active), F(0))))
            lp = solve_lp([0] * len(free), A_ub=g, b_ub=b, A_eq=matrix, b_eq=rhs,
                          bounds=[bounds[i] for i in free], max_pivots=max_pivots - pivots, check=check)
            pivots += lp.pivots
            if lp.status == "limit":
                return QPResult("limit", faces=count, pivots=pivots, reason="max_pivots")
            if lp.status != "optimal":
                continue
            xf = lp.x
        for i, v in zip(free, xf):
            x[i] = v
        certificate = _qp_certificate(h, c, bounds, x)
        if certificate is not None:
            x = tuple(x)
            value = constant + _dot(c, x) + sum((_dot(row, x) * xi for row, xi in zip(h, x)), F(0)) / 2
            result = QPResult("optimal", x, value, certificate, count, pivots)
            if not verify_convex_box_qp_result(h, c, bounds, result, constant):
                raise ArithmeticError("internal QP certificate verification failed")
            return result
    raise ArithmeticError("all faces exhausted without a convex-box KKT point")


def verify_convex_box_qp_result(H, c, bounds, result, constant=0):
    """Verify PSD, primal feasibility and KKT using exact rational arithmetic."""
    try:
        h, c, bounds, constant = _qp_data(H, c, bounds, constant)
        if result.status != "optimal" or result.x is None or len(result.x) != len(c) or not is_psd(h):
            return False
        x = tuple(map(_q, result.x))
        lower = tuple(map(_q, result.certificate["lower_multipliers"]))
        upper = tuple(map(_q, result.certificate["upper_multipliers"]))
        if len(lower) != len(c) or len(upper) != len(c):
            return False
        for i, ((lo, hi), lmul, umul) in enumerate(zip(bounds, lower, upper)):
            if not lo <= x[i] <= hi or min(lmul, umul) < 0:
                return False
            if lmul * (x[i] - lo) or umul * (hi - x[i]):
                return False
            if _dot(h[i], x) + c[i] != lmul - umul:
                return False
        value = constant + _dot(c, x) + sum((_dot(row, x) * xi for row, xi in zip(h, x)), F(0)) / 2
        return result.value == value
    except (ValueError, TypeError, KeyError, AttributeError, ZeroDivisionError):
        return False
