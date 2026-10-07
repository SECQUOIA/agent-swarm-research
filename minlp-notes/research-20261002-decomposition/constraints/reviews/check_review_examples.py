"""Independent exact finite checks for the TU filtered-grid review.

This script enumerates a small full grid; it does not implement tree DP,
prove asymptotic bounds, or verify general-purpose certificates.
"""
from fractions import Fraction as Q
from itertools import product
import json


def objective(point):
    x, y, z = point
    return (x - Q(2, 3)) ** 2 + (y - Q(4, 3)) ** 2 + 2 * (1 - z)


def grid(lo, hi, h):
    count = (hi - lo) / h
    assert count.denominator == 1
    return [lo + k * h for k in range(int(count) + 1)]


# Continuous A has rows ±(1,1), hence is TU. B has entries ±2.
# Feasibility is x+y=2z, 0<=x,y<=2, z in {0,1}.
# The full matrix [A B] is not TU. The exact unique optimum is
# (2/3,4/3,1), and F(v)>=||v-a||² gives g=1, L=2.
a = (Q(2, 3), Q(4, 3), 1)
box = [(Q(0), Q(2)), (Q(0), Q(2))]
labels = [0, 1]
stages = []
conditional_checks = 0
for j in range(8):
    h = Q(1, 2**j)
    error = h * h / 2  # n_c L h²/8 with n_c=L=2.
    domains = [grid(lo, hi, h) for lo, hi in box] + [labels]
    feasible = [v for v in product(*domains) if v[0] + v[1] == 2 * v[2]]
    assert feasible
    incumbent = min(feasible, key=objective)
    upper = objective(incumbent)
    lower = upper - error
    assert lower <= 0 <= upper and upper - lower == error
    marginals = [{t: None for t in domain} for domain in domains]
    for v in feasible:
        value = objective(v)
        assert value >= sum((v[i] - a[i]) ** 2 for i in range(3))
        for i, t in enumerate(v):
            old = marginals[i][t]
            marginals[i][t] = value if old is None else min(old, value)
    # Every rational sample here is feasible in the current restricted box.
    for k in range(35):
        v = (Q(k, 17), 2 - Q(k, 17), 1)
        if 1 not in labels or not all(lo <= v[i] <= hi for i, (lo, hi) in enumerate(box)):
            continue
        for i in range(2):
            containing = [(s, t) for s, t in zip(domains[i], domains[i][1:]) if s <= v[i] <= t]
            assert containing
            for s, t in containing:
                finite = [marginals[i][w] for w in (s, t) if marginals[i][w] is not None]
                assert finite and min(finite) - error <= objective(v)
                conditional_checks += 1
    next_box = []
    for i in range(2):
        intervals = []
        for s, t in zip(domains[i], domains[i][1:]):
            finite = [marginals[i][w] for w in (s, t) if marginals[i][w] is not None]
            if finite and min(finite) - error <= upper:
                intervals.append((s, t))
        assert intervals
        lo, hi = intervals[0][0], intervals[-1][1]
        assert lo <= a[i] <= hi
        assert lo <= incumbent[i] <= hi
        # (10) bounds next-level states by 5+2sqrt(n_c L/g)=9.
        assert len(grid(lo, hi, h / 2)) <= 9
        next_box.append((lo, hi))
    labels = [z for z in labels if marginals[2][z] is not None and marginals[2][z] - error <= upper]
    assert a[2] in labels and incumbent[2] in labels
    stages.append({"level": j, "feasible_assignments": len(feasible), "gap": str(error), "labels": labels})
    box = next_box

# The full-Hessian rounding bound is tight under equality coupling.
h = Q(1, 2)
mid = 2 * (h / 2) ** 2
mean_corners = (0 + 2 * h * h) / 2
assert mean_corners - mid == h * h / 2

# A bad neighboring endpoint survives if the other endpoint qualifies.
# For F=x² on [0,1], at j=0 E=1/4 and U=0, [0,1] survives,
# but its endpoint 1 has M(1)=1>U+E.
assert min(Q(0), Q(1)) - Q(1, 4) <= 0
assert Q(1) > Q(1, 4)

# Integral-data KKT height cannot be reused unchanged for rational RHS.
# x=1/17 with F=x² has n_c=C=D=1, original R=(4n_cC)^(2n_c)=16.
assert Q(1, 17).denominator > 16
assert Q(1, 17) ** 2 == Q(1, 289)
assert Q(1, 289).denominator > 16**2

# Equality-tangent projection removes normal penalty curvature exactly.
# C=(1,1), x+y=2z, P projects to span(1,-1).
projector = [[Q(1, 2), Q(-1, 2)], [Q(-1, 2), Q(1, 2)]]


def matmul(left, right):
    return [[sum(left[i][k] * right[k][j] for k in range(2))
             for j in range(2)] for i in range(2)]


projected_checks = 0
for rho in (Q(0), Q(1), Q(1000000), Q(3, 17)):
    hessian = [[2 + 2 * rho, 2 * rho], [2 * rho, 2 + 2 * rho]]
    projected = matmul(matmul(projector, hessian), projector)
    assert projected == [[Q(1), Q(-1)], [Q(-1), Q(1)]]
    assert max(sum(abs(v) for v in row) for row in projected) == 2
    for v in ((Q(2, 3), Q(4, 3), 1), (Q(0), Q(0), 0)):
        penalty = rho * (v[0] + v[1] - 2 * v[2]) ** 2
        assert objective(v) + penalty == objective(v)
        projected_checks += 1

print(json.dumps({"status": "passed", "stages": stages, "conditional_checks": conditional_checks,
                  "projected_penalty_checks": projected_checks,
                  "separate_checks": ["coupled-curvature equality", "nonqualifying retained endpoint", "rational-RHS height counterexample"]}, indent=2))
