"""Exact certificates for a scalar-parametric positive-definite box QP.

Numerical optimization proposes active patterns; Fraction arithmetic accepts them.
The prototype can explicitly fail to recover a pattern on large difficult inputs.
No numerical result is ever returned as a certified response path.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import product


def rational(value):
    if isinstance(value, float):
        raise TypeError("Use integers, Fraction, or decimal strings for exact input")
    return F(value)


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), F(0))


def linear_solve(matrix, rhs):
    """Gauss-Jordan solve, including the empty 0-by-0 case."""
    n = len(rhs)
    a = [list(row) + [rhs[i]] for i, row in enumerate(matrix)]
    for j in range(n):
        p = next((i for i in range(j, n) if a[i][j]), None)
        if p is None:
            raise ValueError("Singular system")
        a[j], a[p] = a[p], a[j]
        q = a[j][j]
        a[j] = [v / q for v in a[j]]
        for i in range(n):
            if i != j and a[i][j]:
                q = a[i][j]
                a[i] = [v - q * w for v, w in zip(a[i], a[j])]
    return tuple(row[-1] for row in a)


def positive_semidefinite(matrix, strict=False):
    """Exact symmetric elimination; zero PSD pivots must have a zero row."""
    a = [list(row) for row in matrix]
    for j in range(len(a)):
        pivot = a[j][j]
        if pivot < 0 or (strict and pivot == 0):
            return False
        if pivot == 0:
            if any(a[i][j] for i in range(j + 1, len(a))):
                return False
            continue
        for i in range(j + 1, len(a)):
            for h in range(i, len(a)):
                a[h][i] -= a[i][j] * a[h][j] / pivot
                a[i][h] = a[h][i]
    return True


@dataclass(frozen=True)
class Problem:
    """min_z .5 z'Qz+(c+C*x)'z, 0<=z<=1, lo<=x<=hi.

    Q=diag(d)+U H U'; all input coefficients must be exact rationals.
    Positive definiteness is verified, with a dense fallback when H is indefinite.
    """
    d: tuple
    U: tuple
    H: tuple
    c: tuple
    C: tuple
    lo: F = F(0)
    hi: F = F(1)

    def __post_init__(self):
        for name in ("d", "c", "C"):
            object.__setattr__(self, name, tuple(map(rational, getattr(self, name))))
        for name in ("U", "H"):
            object.__setattr__(self, name, tuple(tuple(map(rational, row)) for row in getattr(self, name)))
        object.__setattr__(self, "lo", rational(self.lo))
        object.__setattr__(self, "hi", rational(self.hi))
        n, k = len(self.d), len(self.H)
        if not (len(self.c) == len(self.C) == len(self.U) == n):
            raise ValueError("Inconsistent dimensions")
        if any(len(row) != k for row in self.U + self.H):
            raise ValueError("Inconsistent rank dimension")
        if self.lo > self.hi or any(v <= 0 for v in self.d):
            raise ValueError("Invalid bounds or diagonal")
        if any(self.H[i][j] != self.H[j][i] for i in range(k) for j in range(k)):
            raise ValueError("H must be symmetric")
        if not positive_semidefinite(self.H):
            if k == 1:
                if 1 + self.H[0][0] * sum((row[0] ** 2 / di for row, di in zip(self.U, self.d)), F(0)) <= 0:
                    raise ValueError("Q must be positive definite")
                return
            q = [[(self.d[i] if i == j else F(0)) + dot(self.U[i], self.hmul(self.U[j]))
                  for j in range(n)] for i in range(n)]
            if not positive_semidefinite(q, strict=True):
                raise ValueError("Q must be positive definite")

    def hmul(self, v):
        return tuple(dot(row, v) for row in self.H)

    def qmul(self, v):
        w = tuple(sum((self.U[i][j] * v[i] for i in range(len(self.d))), F(0)) for j in range(len(self.H)))
        hw = self.hmul(w)
        return tuple(self.d[i] * v[i] + dot(self.U[i], hw) for i in range(len(self.d)))


@dataclass(frozen=True)
class Segment:
    lo: F
    hi: F
    intercept: tuple
    slope: tuple
    pattern: tuple  # 0 lower, 1 free, 2 upper

    def __post_init__(self):
        object.__setattr__(self, "lo", rational(self.lo))
        object.__setattr__(self, "hi", rational(self.hi))
        object.__setattr__(self, "intercept", tuple(map(rational, self.intercept)))
        object.__setattr__(self, "slope", tuple(map(rational, self.slope)))
        object.__setattr__(self, "pattern", tuple(self.pattern))

    def response(self, x):
        x = rational(x)
        return tuple(a + b * x for a, b in zip(self.intercept, self.slope))


def clip_interval(lo, hi, intercept, slope):
    """Intersect [lo,hi] with intercept+slope*x <= 0; keep singletons."""
    if slope > 0:
        hi = min(hi, -intercept / slope)
    elif slope < 0:
        lo = max(lo, -intercept / slope)
    elif intercept > 0:
        return None
    return (lo, hi) if lo <= hi else None


def pattern_segment(problem, pattern):
    p, n, k = problem, len(problem.d), len(problem.H)
    if len(pattern) != n or any(s not in (0, 1, 2) for s in pattern):
        raise ValueError("Invalid active pattern")
    free = [i for i, s in enumerate(pattern) if s == 1]
    upper = [i for i, s in enumerate(pattern) if s == 2]
    aggregate = tuple(sum((p.U[i][j] for i in upper), F(0)) for j in range(k))
    hagg = p.hmul(aggregate)
    gram = [[sum((p.U[i][j] * p.U[i][h] / p.d[i] for i in free), F(0))
             for h in range(k)] for j in range(k)]
    small = [[F(j == h) + sum((gram[j][v] * p.H[v][h] for v in range(k)), F(0))
              for h in range(k)] for j in range(k)]

    def solve_free(rhs):
        t = tuple(sum((p.U[i][j] * rhs[i] / p.d[i] for i in free), F(0)) for j in range(k))
        hw = p.hmul(linear_solve(small, t))
        return {i: (rhs[i] - dot(p.U[i], hw)) / p.d[i] for i in free}

    a_free = solve_free(tuple(-p.c[i] - dot(p.U[i], hagg) for i in range(n)))
    b_free = solve_free(tuple(-v for v in p.C))
    a = tuple(a_free[i] if pattern[i] == 1 else F(pattern[i] == 2) for i in range(n))
    b = tuple(b_free.get(i, F(0)) for i in range(n))
    ga = tuple(v + c for v, c in zip(p.qmul(a), p.c))
    gb = tuple(v + c for v, c in zip(p.qmul(b), p.C))
    interval = (p.lo, p.hi)
    for i, state in enumerate(pattern):
        inequalities = ((-a[i], -b[i]), (a[i] - 1, b[i])) if state == 1 else (
            ((-ga[i], -gb[i]),) if state == 0 else ((ga[i], gb[i]),))
        for alpha, beta in inequalities:
            interval = clip_interval(*interval, alpha, beta)
            if interval is None:
                return None
    return Segment(*interval, a, b, tuple(pattern))


def verify_segment(p, s):
    """Check affine box KKT identities and inequalities without re-solving."""
    n = len(p.d)
    if not (p.lo <= s.lo <= s.hi <= p.hi):
        return False
    if any(len(v) != n for v in (s.intercept, s.slope, s.pattern)):
        return False
    ga = tuple(v + c for v, c in zip(p.qmul(s.intercept), p.c))
    gb = tuple(v + c for v, c in zip(p.qmul(s.slope), p.C))
    for i, state in enumerate(s.pattern):
        if state not in (0, 1, 2):
            return False
        if state in (0, 2) and (s.intercept[i] != F(state == 2) or s.slope[i]):
            return False
        for x in (s.lo, s.hi):
            z, g = s.intercept[i] + s.slope[i] * x, ga[i] + gb[i] * x
            if not 0 <= z <= 1:
                return False
            if (state == 0 and g < 0) or (state == 2 and g > 0) or (state == 1 and g != 0):
                return False
    return True


def uncovered_gaps(p, segments):
    ordered = sorted((s.lo, s.hi) for s in segments)
    cursor, gaps = p.lo, []
    for lo, hi in ordered:
        if lo > cursor:
            gaps.append((cursor, lo))
        cursor = max(cursor, hi)
    if cursor < p.hi:
        gaps.append((cursor, p.hi))
    return gaps


def verify_path(p, segments):
    return (bool(segments) and all(verify_segment(p, s) for s in segments)
            and min(s.lo for s in segments) == p.lo
            and max(s.hi for s in segments) == p.hi
            and not uncovered_gaps(p, segments))


def recover_segment(p, x, exhaustive_limit=9, stats=None):
    import numpy as np
    from scipy.optimize import minimize
    n = len(p.d)
    if n == 0:
        return pattern_segment(p, ())
    d, u, h = np.array(p.d, float), np.array(p.U, float), np.array(p.H, float)
    lin = np.array(p.c, float) + float(x) * np.array(p.C, float)

    def qmul(z):
        return d * z + (u @ (h @ (u.T @ z)) if len(p.H) else 0)

    def fun(z):
        qz = qmul(z)
        return .5 * z @ qz + lin @ z, qz + lin

    result = minimize(fun, np.clip(-lin / d, 0, 1), jac=True, bounds=[(0, 1)] * n,
                      method="L-BFGS-B", options={"ftol": 1e-15, "gtol": 1e-11, "maxiter": 5000})
    if stats is not None:
        stats["numeric_qps"] = stats.get("numeric_qps", 0) + 1
    attempted = set()
    for tol in (1e-9, 1e-7, 1e-5, 1e-3, 0):
        pattern = tuple(0 if z <= tol else 2 if z >= 1 - tol else 1 for z in result.x)
        if pattern in attempted:
            continue
        attempted.add(pattern)
        s = pattern_segment(p, pattern)
        if stats is not None:
            stats["patterns_tried"] = stats.get("patterns_tried", 0) + 1
        if s is not None and s.lo <= x <= s.hi and verify_segment(p, s):
            return s
    if n <= exhaustive_limit:
        if stats is not None:
            stats["exhaustive_recoveries"] = stats.get("exhaustive_recoveries", 0) + 1
        for pattern in product((0, 1, 2), repeat=n):
            if pattern in attempted:
                continue
            s = pattern_segment(p, pattern)
            if s is not None and s.lo <= x <= s.hi and verify_segment(p, s):
                return s
    raise RuntimeError(f"No exact active pattern recovered at x={x}; no certified answer returned")


def solve_response_path(p, exhaustive_limit=9, max_segments=10000, stats=None):
    segments = []
    while True:
        gaps = uncovered_gaps(p, segments)
        if not gaps:
            if segments:
                break
            x = p.lo  # Singleton leader domain.
        else:
            lo, hi = max(gaps, key=lambda interval: interval[1] - interval[0])
            x = (lo + hi) / 2
        s = recover_segment(p, x, exhaustive_limit, stats)
        if s in segments:
            raise RuntimeError("Coverage made no progress")
        segments.append(s)
        if len(segments) > max_segments:
            raise RuntimeError("Segment limit reached; no certified answer returned")
    segments.sort(key=lambda s: (s.lo, s.hi))
    if not verify_path(p, segments):
        raise RuntimeError("Response path failed exact verification")
    return segments


def exhaustive_path(p):
    """Small-instance oracle: enumerate all 3^N active patterns."""
    segments = [s for pattern in product((0, 1, 2), repeat=len(p.d))
                if (s := pattern_segment(p, pattern)) is not None]
    if not verify_path(p, segments):
        raise RuntimeError("Exhaustive path failed verification")
    return segments


def quadratic_interval_minimum(lo, hi, alpha, beta, gamma):
    """Exact minimum of alpha+beta*x+gamma*x^2 on a rational interval."""
    candidates = [lo, hi]
    if gamma > 0:
        stationary = -beta / (2 * gamma)
        if lo <= stationary <= hi:
            candidates.append(stationary)
    return min(((alpha + beta * x + gamma * x * x, x) for x in candidates))


def optimize_path(p, segments, objective_x, objective_z, constraints=(), *,
                  objective_xx=0, objective_xz=None):
    """Minimize ox*x+oz'z+oxx*x^2+x*oxz'z over a verified response path.

    constraints is an iterable of (coefficient_x, coefficients_z, rhs) triples,
    interpreted as coefficient_x*x+coefficients_z'z <= rhs. Returns None iff
    infeasible, else a dict with exact x, z, objective, feasible_intervals.
    Equalities are encoded as two weak inequalities; isolated points survive.
    """
    if not verify_path(p, segments):
        raise ValueError("Expected a complete exact response certificate")
    ox, oz = rational(objective_x), tuple(map(rational, objective_z))
    oxx = rational(objective_xx)
    oxz = ((F(0),) * len(p.d) if objective_xz is None else tuple(map(rational, objective_xz)))
    cons = [(rational(cx), tuple(map(rational, cz)), rational(rhs)) for cx, cz, rhs in constraints]
    if len(oz) != len(p.d) or len(oxz) != len(p.d) or any(len(cz) != len(p.d) for _, cz, _ in cons):
        raise ValueError("Inconsistent upper-level dimensions")
    best, intervals = None, []
    for s in segments:
        interval = (s.lo, s.hi)
        for cx, cz, rhs in cons:
            interval = clip_interval(*interval, dot(cz, s.intercept) - rhs, cx + dot(cz, s.slope))
            if interval is None:
                break
        if interval is None:
            continue
        intervals.append(interval)
        alpha = dot(oz, s.intercept)
        beta = ox + dot(oz, s.slope) + dot(oxz, s.intercept)
        gamma = oxx + dot(oxz, s.slope)
        value, x = quadratic_interval_minimum(*interval, alpha, beta, gamma)
        if best is None or (value, x) < (best["objective"], best["x"]):
            best = {"x": x, "z": s.response(x), "objective": value}
    if best is not None:
        best["feasible_intervals"] = sorted(set(intervals))
    return best


def optimize_aligned_rank_one(p, objective_x, objective_z, constraints=(), *,
                              objective_xx=0, objective_xz=None, gamma=1):
    """Complete exact sorted sweep when rank=1 and C=gamma*U, gamma>0.

    Same upper objective and result contract as optimize_path. Does not build an
    N-vector for every response interval: O(N log N+N*(m+1)) rational operations and
    O(N*(m+1)) storage for m explicit affine upper constraints (excluding bit cost).
    Q positive definiteness has already been checked by Problem.
    """
    gamma, n = rational(gamma), len(p.d)
    if len(p.H) != 1 or gamma <= 0:
        raise ValueError("Require rank one and gamma>0")
    u = tuple(row[0] for row in p.U)
    if any(ci != gamma * ui for ci, ui in zip(p.C, u)):
        raise ValueError("Require C=gamma*U[:,0]")
    ox, oz = rational(objective_x), tuple(map(rational, objective_z))
    oxx = rational(objective_xx)
    oxz = ((F(0),) * n if objective_xz is None else tuple(map(rational, objective_xz)))
    cons = [(rational(cx), tuple(map(rational, cz)), rational(rhs)) for cx, cz, rhs in constraints]
    if len(oz) != n or len(oxz) != n or any(len(cz) != n for _, cz, _ in cons):
        raise ValueError("Inconsistent upper-level dimensions")
    weights = [u, oz, oxz] + [cz for _, cz, _ in cons]
    h = p.H[0][0]
    a, b, events = [], [F(0)] * n, {}
    for i, ui in enumerate(u):
        if ui == 0:
            a.append(min(F(1), max(F(0), -p.c[i] / p.d[i])))
            continue
        a.append(F(ui > 0))
        entry, departure = sorted((-p.c[i] / ui, -(p.c[i] + p.d[i]) / ui))
        events.setdefault(entry, []).append((i, -p.c[i] / p.d[i], -ui / p.d[i]))
        events.setdefault(departure, []).append((i, F(ui < 0), F(0)))
    wa, wb = [dot(w, a) for w in weights], [F(0)] * len(weights)
    previous, best, intervals, visited = None, None, [], 0
    for event in sorted(events) + [None]:
        denominator = 1 - h * wb[0]
        if denominator <= 0:
            raise ValueError("Effective-price map is not increasing; SPD contract violated")
        lo = p.lo if previous is None else max(p.lo, (denominator * previous - h * wa[0]) / gamma)
        hi = p.hi if event is None else min(p.hi, (denominator * event - h * wa[0]) / gamma)
        if lo <= hi:
            visited += 1
            intercept = [v + slope * h * wa[0] / denominator for v, slope in zip(wa, wb)]
            slope = [v * gamma / denominator for v in wb]
            interval = (lo, hi)
            for j, (cx, _, rhs) in enumerate(cons, 3):
                interval = clip_interval(*interval, intercept[j] - rhs, cx + slope[j])
                if interval is None:
                    break
            if interval is not None:
                intervals.append(interval)
                value, x = quadratic_interval_minimum(*interval, intercept[1],
                                                      ox + slope[1] + intercept[2], oxx + slope[2])
                if best is None or (value, x) < (best["objective"], best["x"]):
                    best = {"x": x, "objective": value,
                            "effective_price": (gamma * x + h * wa[0]) / denominator}
        if event is None:
            break
        for i, new_a, new_b in events[event]:
            delta_a, delta_b = new_a - a[i], new_b - b[i]
            for j, weight in enumerate(weights):
                wa[j] += weight[i] * delta_a
                wb[j] += weight[i] * delta_b
            a[i], b[i] = new_a, new_b
        previous = event
    if best is not None:
        t = best["effective_price"]
        best["z"] = tuple(min(F(1), max(F(0), -(ci + ui * t) / di))
                          for ci, ui, di in zip(p.c, u, p.d))
        best["feasible_intervals"] = sorted(set(intervals))
        best["response_intervals_visited"] = visited
        best["thresholds"] = len(events)
    return best
