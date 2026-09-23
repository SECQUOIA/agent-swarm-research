"""Root check: new baseline maps coupled x/y/z rows with free simplex weights."""
from fractions import Fraction as F
import numpy as np
from network_simplex_benchmarks.test_strong_baselines import StrongBaselineTests
from network_simplex_benchmarks.strong_baselines import optimize_ef
from network_simplex_compressed import CompressedNetworkSimplex

checks = 0
for seed in range(30):
    instance, rng = StrongBaselineTests().instance(seed, seed % 6)
    E, m, O = instance.edge_count, instance.simplex_size, instance.observations
    n = E + m + len(O)
    y = [F(1, m + 2)] * m
    reference = list(map(lambda v: F(str(v)), instance.reference))
    point = reference + y + [reference[e] * y[j] for e, j in O]
    rows = []
    for _ in range(3):
        coefficients = rng.integers(-3, 4, size=n)
        rhs = sum(int(c) * v for c, v in zip(coefficients, point)) + F(1, 11)
        rows.append((coefficients, rhs))
    objective = rng.normal(size=n)
    model = CompressedNetworkSimplex(instance.arcs, -instance.balances, m, O,
                                     eliminate_observed=True)
    for coefficients, rhs in rows:
        model.ub.append(({i: F(int(c)) for i, c in enumerate(coefficients) if c}, rhs))
    expected = model.optimize(objective)
    assert expected.success
    for merge in (False, True):
        actual = optimize_ef(instance, objective, merge=merge, extra_rows=rows)
        assert actual.success
        assert abs(actual.fun - expected.fun) < 1e-7, (seed, merge)
        assert all(c @ actual.original_point <= float(rhs) + 1e-7 for c, rhs in rows)
        checks += 1
print(f"PASS: {checks} numerical comparisons with free y and three coupled x/y/z rows")
