"""Checks for the joint weighted cactus proof's local resistance elimination.

The LP checks use exact rational arithmetic and exhaustive box vertices with
one free coordinate, independently of the threshold formula. The circulation
checks use floating-point quadratics, certify neither exact global optima nor
the full parameter-space compiler, and compare with independently sampled
physical resistance scenarios. No third-party packages are required.
"""

from fractions import Fraction as F
from itertools import product
import math
import random


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def thresholds(f, weights, lower, upper):
    """Yield the dual value and a primal witness for every feasible threshold."""
    for lam in sorted(set(weights)):
        tied = [i for i, w in enumerate(weights) if w == lam]
        beta = [upper[i] if (weights[i] - lam) * f[i] > 0 else lower[i]
                for i in range(len(f))]
        for i in tied:
            beta[i] = lower[i] if f[i] >= 0 else upper[i]
        residual = -sum(a * b for a, b in zip(f, beta))
        available = sum(abs(f[i]) * (upper[i] - lower[i]) for i in tied)
        if not 0 <= residual <= available:
            continue
        for i in tied:
            amount = min(residual, abs(f[i]) * (upper[i] - lower[i]))
            if f[i]:
                beta[i] += amount / f[i]
            residual -= amount
        require(residual == 0, "tie fill did not finish")
        require(sum(a * b for a, b in zip(f, beta)) == 0, "balance failed")
        require(all(l <= b <= u for l, b, u in zip(lower, beta, upper)),
                "box feasibility failed")
        dual = sum((weights[i] - lam) * f[i] * beta[i]
                   for i in range(len(f)))
        primal = sum(weights[i] * f[i] * beta[i] for i in range(len(f)))
        require(primal == dual, "primal-dual equality failed")
        yield dual, beta


def exhaustive_lp(f, weights, lower, upper):
    """Enumerate vertices by picking at most one free box coordinate."""
    if not any(f):
        return F(0)
    best = None
    n = len(f)
    for free in range(n):
        if not f[free]:
            continue
        other = [i for i in range(n) if i != free]
        for bits in product((0, 1), repeat=n - 1):
            beta = list(lower)
            for i, bit in zip(other, bits):
                beta[i] = upper[i] if bit else lower[i]
            beta[free] = -sum(f[i] * beta[i] for i in other) / f[free]
            if lower[free] <= beta[free] <= upper[free]:
                value = sum(w * a * b for w, a, b in zip(weights, f, beta))
                best = value if best is None else max(best, value)
    return best


def exact_lp_checks(rng):
    cases = 0
    feasible = 0
    for n in range(2, 8):
        for trial in range(36):
            x = [F(rng.randrange(-4, 5), rng.randrange(1, 4)) for _ in range(n)]
            if trial == 0:
                x = [F(0)] * n
            f = [v * abs(v) for v in x]
            weights = [F(rng.randrange(-2, 3)) for _ in range(n)]
            if trial == 1:
                weights = [F(2)] * n
            lower = [F(rng.randrange(1, 4), 3) for _ in range(n)]
            upper = [l + F(rng.randrange(0, 5), 2) for l in lower]
            expected = exhaustive_lp(f, weights, lower, upper)
            candidates = list(thresholds(f, weights, lower, upper))
            require(bool(candidates) == (expected is not None), "feasibility mismatch")
            if expected is not None:
                require(all(value == expected for value, _ in candidates),
                        "threshold differs from exact vertex optimum")
                feasible += 1
            cases += 1
    return cases, feasible


def polynomial(ell, sign, multipliers):
    return (
        sum(mult * sign[i] for i, mult in enumerate(multipliers)),
        sum(2 * mult * sign[i] * ell[i] for i, mult in enumerate(multipliers)),
        sum(mult * sign[i] * ell[i] ** 2 for i, mult in enumerate(multipliers)),
    )


def evaluate(poly, q):
    a, b, c = poly
    return (a * q + b) * q + c


def roots(poly):
    a, b, c = poly
    if abs(a) < 1e-13:
        return [-c / b] if abs(b) >= 1e-13 else []
    disc = b * b - 4 * a * c
    if disc < -1e-10:
        return []
    disc = math.sqrt(max(0.0, disc))
    return [(-b - disc) / (2 * a), (-b + disc) / (2 * a)]


def local_candidates(ell, weights, lower, upper):
    """Boundary/stationary enumeration, at one fixed nomination parameter."""
    best = -math.inf
    cuts = sorted(set(-v for v in ell))
    for left, right in zip(cuts, cuts[1:]):
        middle = (left + right) / 2
        sign = [1 if middle + v >= 0 else -1 for v in ell]
        for lam in sorted(set(weights)):
            tied = [i for i, w in enumerate(weights) if w == lam]
            endpoints = [upper[i] if (weights[i] - lam) * sign[i] > 0 else lower[i]
                         for i in range(len(ell))]
            low = list(endpoints)
            high = list(endpoints)
            for i in tied:
                low[i] = lower[i] if sign[i] > 0 else upper[i]
                high[i] = upper[i] if sign[i] > 0 else lower[i]
            lo_poly = polynomial(ell, sign, low)
            hi_poly = polynomial(ell, sign, high)
            objective = polynomial(ell, sign,
                                   [(w - lam) * beta for w, beta in zip(weights, endpoints)])
            candidates = [left, right] + roots(lo_poly) + roots(hi_poly)
            a, b, _ = objective
            if abs(a) > 1e-13:
                candidates.append(-b / (2 * a))
            elif abs(b) < 1e-13:
                candidates.append(middle)
            for q in candidates:
                if (left - 1e-9 <= q <= right + 1e-9
                        and evaluate(lo_poly, q) <= 1e-7
                        and evaluate(hi_poly, q) >= -1e-7):
                    best = max(best, evaluate(objective, q))
    if len(cuts) == 1:
        return 0.0
    return best


def physical_objective(ell, weights, beta):
    left, right = min(-v for v in ell), max(-v for v in ell)
    for _ in range(90):
        q = (left + right) / 2
        total = sum(b * (q + a) * abs(q + a) for a, b in zip(ell, beta))
        if total > 0:
            right = q
        else:
            left = q
    q = (left + right) / 2
    return sum(w * b * (q + a) * abs(q + a) for a, w, b in zip(ell, weights, beta))


def circulation_checks(rng):
    scenarios = 0
    worst_violation = 0.0
    for trial in range(90):
        n = rng.randrange(3, 9)
        ell = [float(rng.randrange(-5, 6)) for _ in range(n)]
        weights = [float(rng.randrange(-2, 3)) for _ in range(n)]
        if trial % 9 == 0:
            weights = [1.0] * n
        lower = [float(rng.randrange(1, 4)) for _ in range(n)]
        upper = [l + rng.randrange(0, 5) for l in lower]
        optimum = local_candidates(ell, weights, lower, upper)
        require(math.isfinite(optimum), "candidate list unexpectedly empty")
        profiles = [[rng.uniform(l, u) for l, u in zip(lower, upper)] for _ in range(70)]
        profiles.extend([[u if bit else l for l, u, bit in zip(lower, upper, bits)]
                         for bits in product((0, 1), repeat=n)])
        for beta in profiles:
            value = physical_objective(ell, weights, beta)
            violation = value - optimum
            worst_violation = max(worst_violation, violation)
            require(violation <= 1e-6 * (1 + abs(optimum)),
                    "physical scenario exceeds candidate maximum")
            scenarios += 1
    return 90, scenarios, worst_violation


if __name__ == "__main__":
    rng = random.Random(260906)
    print("Exact threshold LP checks:", exact_lp_checks(rng))
    print("Circulation cases, physical scenarios, maximum violation:", circulation_checks(rng))
