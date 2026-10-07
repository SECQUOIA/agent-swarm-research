"""Exact finite checks of Sections 2--3 and Appendices A--B; no floating point or solver oracle."""
from fractions import Fraction as F
from itertools import combinations


def envelope(points, rho, lam):
    return min(cost + lam * residual + rho * abs(residual)
               for cost, residual in points)


def optimized_envelope(points, rho):
    # With both residual signs, the concave finite envelope reaches its
    # maximum at a breakpoint (possibly also along a flat segment).
    lines = [(cost + rho * abs(residual), residual)
             for cost, residual in points]
    candidates = {F(0)}
    for (a, b), (c, d) in combinations(lines, 2):
        if b != d:
            candidates.add((c - a) / (b - d))
    return max(envelope(points, rho, lam) for lam in candidates)


cases = 0
symmetric_cases = 0
for n in range(1, 11):
    a = [F(1, 2 ** (2 ** i)) for i in range(1, n + 1)]
    delta = a[-1]
    assert a[0] == F(1, 4)
    assert all(a[i] ** 2 == a[i + 1] for i in range(n - 1))
    threshold = 1 / (2 * delta)
    assert threshold.denominator == 1
    assert threshold.numerator.bit_length() == 2 ** n
    one = [(F(0), F(-1)), (F(0), F(0)), (F(0), F(1)),
           (F(-1), delta), (F(-1), F(1))]
    symmetric = one + [(F(-1), -delta), (F(-1), F(-1))]
    for rho in [F(0), F(1, 3), threshold / 2, threshold,
                threshold + 1, 2 * threshold, 3 * threshold]:
        target = min(F(0), (2 * rho * delta - 1) / (1 + delta))
        assert optimized_envelope(one, rho) == target
        lam_star = ((1 + rho * (1 - delta)) / (1 + delta)
                    if rho <= threshold else rho)
        assert envelope(one, rho, lam_star) == target
        balanced = (delta * (rho - lam_star)
                    + (-1 + (rho + lam_star) * delta)) / (1 + delta)
        assert balanced == (2 * rho * delta - 1) / (1 + delta)
        assert optimized_envelope(symmetric, rho) == min(0, -1 + rho * delta)
        for lam in [-3 * threshold, -threshold, F(-1, 3), F(0),
                    F(1, 3), threshold, 3 * threshold]:
            c = rho - abs(lam)
            assert envelope(symmetric, rho, lam) == min(0, -1+c*delta, -1+c)
            symmetric_cases += 1
        if rho > threshold:
            # On each linear branch strict positivity away from zero
            # follows from positive slopes from zero or positive endpoints.
            assert rho - threshold > 0
            assert -1 + (rho + threshold) * delta > 0
        cases += 1
    for eps in [F(0), F(1, 4), F(1, 2), F(9, 10)]:
        needed = max(F(0), (1 - eps * (1 + delta)) / (2 * delta))
        assert -optimized_envelope(one, needed) <= eps
        if needed > 0:
            assert -optimized_envelope(one, needed / 2) > eps
    # Seed, chain, continuous bounds and native link at strict points.
    t = F(3, 8)
    for q, y in [(0, F(0)), (1, F(1, 2))]:
        slacks = [t, 1-t, t-F(1, 4), 1-y, 1+y,
                  y-t+2*(1-q)]
        if n > 1:
            slacks.append(t-t*t)
        assert min(slacks) == F(1, 8)
    for q in [0, 1]:
        for b in [0, 1]:
            y = F(0) if q == 0 else F(2*b-1, 2)
            slacks = [t, 1-t, t-F(1, 4), 1-y, 1+y,
                      y-t+(1-q)+2*(1-b), -t+(1-q)+2*b-y]
            if n > 1:
                slacks.append(t-t*t)
            assert min(slacks) == F(1, 8)
    # Exponent arithmetic for the fractional-power identity; no power evaluation.
    assert F(2 ** n) * F(1, 2 ** n) == 1

# Seed variant a_1 >= 2^-t (Remark rem:seed): separation, thresholds, bits,
# dual formula and strict-point slacks.
seed_cases = 0
for t_seed in [2, 3, 5, 8]:
    for n in range(1, 7):
        a = [F(1, 2 ** t_seed)]
        for _ in range(n - 1):
            a.append(a[-1] ** 2)
        delta = a[-1]
        assert delta == F(1, 2 ** (t_seed * 2 ** (n - 1)))
        threshold = 1 / (2 * delta)
        assert threshold.denominator == 1
        assert threshold.numerator.bit_length() == t_seed * 2 ** (n - 1)
        assert (1 / delta).numerator.bit_length() == t_seed * 2 ** (n - 1) + 1
        one = [(F(0), F(-1)), (F(0), F(0)), (F(0), F(1)),
               (F(-1), delta), (F(-1), F(1))]
        for rho in [F(0), threshold / 2, threshold, 2 * threshold]:
            assert optimized_envelope(one, rho) == min(
                F(0), (2 * rho * delta - 1) / (1 + delta))
        s = F(3, 8)
        for q, y in [(0, F(0)), (1, F(1, 2))]:
            slacks = [s, 1 - s, s - F(1, 2 ** t_seed), 1 - y, 1 + y,
                      y - s + 2 * (1 - q)]
            if n > 1:
                slacks.append(s - s * s)
            assert min(slacks) >= F(1, 8)
        seed_cases += 1

# Scalar balanced-ratio identity, including negative A contributions.
ratio_cases = 0
for a in [F(1, 7), F(1), F(3)]:
    for b in [F(1, 5), F(2), F(7)]:
        for fp in [F(-2), F(0), F(3)]:
            for fm in [F(-4), F(0), F(5)]:
                c = (b*fp+a*fm)/(a+b)
                s = 2*a*b/(a+b)
                assert -c/s == (-fp/a-fm/b)/2
                ratio_cases += 1

# Completed-square identity for the cited source's continuous (z=0) branch.
for t in [F(1, 2), F(3, 4), F(1), F(2), F(10)]:
    u = -1/(2*t)
    assert -1 <= u <= 1
    assert u + t*u*u == -1/(4*t)
    for v in [F(-1), F(-1, 3), F(0), F(1, 2), F(1)]:
        assert v+t*v*v+1/(4*t) == t*(v+1/(2*t))**2
print(f"PASS: {cases} exact projected-envelope cases, {symmetric_cases} symmetric multiplier cases,")
print(f"      {ratio_cases} scalar mixture identities, accuracy thresholds, strict margins,")
print("      chain/encoding and exponent arithmetic, and the source continuous-branch identity;")
print(f"      {seed_cases} seed-variant cases (separation, thresholds, bits, dual formula, slacks).")
