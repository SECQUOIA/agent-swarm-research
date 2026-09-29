"""Targeted exact-arithmetic checks for the mixed squared-Fejer construction.

These finite examples check implementation identities and boundary cases;
they do not prove positivity for arbitrary truncated moment functionals.
"""

from fractions import Fraction as Q
from itertools import product


def cheb(k, x):
    if k == 0:
        return Q(1)
    previous, current = Q(1), x
    for _ in range(1, k):
        previous, current = current, 2 * x * current - previous
    return current


def multiply(values):
    answer = Q(1)
    for value in values:
        answer *= value
    return answer


def kernel_coefficients(m):
    b = {j: m - abs(j) for j in range(1 - m, m)}
    a = [sum(value * b.get(j - k, 0) for j, value in b.items())
         for k in range(2 * m - 1)]
    return [Q(value, a[0]) for value in a]


# Each atom specifies (u,v,w,t), (x,s,z), and its probability.
atoms = [
    ((0, 0, 0, 0), (Q(-1), Q(0), Q(1)), Q(1, 10)),
    ((1, 0, 1, 1), (Q(1, 2), Q(-1, 2), Q(0)), Q(2, 10)),
    ((0, 1, 1, 1), (Q(0), Q(1, 2), Q(-1)), Q(3, 10)),
    ((1, 1, 1, 1), (Q(-1, 2), Q(1), Q(1, 2)), Q(4, 10)),
]
# Third bag has no continuous coordinates. v=2 labels in the first bag
# are globally unextendable; additional extendable labels have mass zero.
bags = [
    ((0, 1), (0, 1), list(product(range(2), range(3)))),
    ((1, 2), (1, 2), list(product(range(2), repeat=2))),
    ((), (2, 3), [(0, 0), (0, 1), (1, 1)]),
]


def moment(bag, label, alpha):
    continuous, discrete, _ = bags[bag]
    return sum((weight * multiply(cheb(k, x[i])
                                  for k, i in zip(alpha, continuous))
                for a, x, weight in atoms
                if tuple(a[i] for i in discrete) == label), Q(0))


def density(bag, label, g):
    continuous, _, _ = bags[bag]
    return {alpha: moment(bag, label, alpha)
            * multiply(1 if k == 0 else 2 * g[k] for k in alpha)
            for alpha in product(range(len(g)), repeat=len(continuous))}


def marginal(bag, tables, continuous_separator, discrete_separator):
    continuous, discrete, labels = bags[bag]
    result = {}
    for label in labels:
        s = tuple(label[discrete.index(i)] for i in discrete_separator)
        for alpha, coefficient in tables[label].items():
            if any(k != 0 for i, k in zip(continuous, alpha)
                   if i not in continuous_separator):
                continue
            beta = tuple(alpha[continuous.index(i)]
                         for i in continuous_separator)
            key = (s, beta)
            result[key] = result.get(key, Q(0)) + coefficient
    return {key: value for key, value in result.items() if value != 0}


checks = 0
for r in (2, 4, 6):
    m = r // 2 + 1
    g = kernel_coefficients(m)
    delta = Q(3, 2 * m * m + 1)
    assert 2 * 2 * (m - 1) <= 2 * r
    tables = [{a: density(b, a, g) for a in bag[2]}
              for b, bag in enumerate(bags)]
    assert marginal(0, tables[0], (1,), (1,)) == marginal(
        1, tables[1], (1,), (1,))
    assert marginal(1, tables[1], (), (2,)) == marginal(
        2, tables[2], (), (2,))
    cost_change, weighted_budget = Q(0), Q(0)
    for b, (continuous, _, labels) in enumerate(bags):
        zero = (0,) * len(continuous)
        assert sum(tables[b][a][zero] for a in labels) == 1
        for a in labels:
            tau = moment(b, a, zero)
            if tau == 0:
                assert all(value == 0 for value in tables[b][a].values())
            for y in product((Q(-1), Q(-1, 3), Q(0), Q(1, 2), Q(1)),
                             repeat=len(continuous)):
                value = sum((coefficient * multiply(cheb(k, yi)
                              for k, yi in zip(alpha, y))
                             for alpha, coefficient in tables[b][a].items()),
                            Q(0))
                assert value >= 0
                checks += 1
            costs = {zero: Q(sum(a) + 1)}
            if continuous:
                costs[(r, 0)] = Q((-1) ** sum(a), sum(a) + 1)
                costs[(1, 1)] = Q(2, 3)
            for alpha, coefficient in costs.items():
                original = moment(b, a, alpha)
                # Arcsine orthogonality: int T_k^2=1/2 for k>0.
                smoothed = tables[b][a].get(alpha, Q(0)) / (
                    2 ** sum(k > 0 for k in alpha))
                eigenvalue = multiply(g[k] if k < len(g) else 0
                                      for k in alpha)
                assert smoothed == eigenvalue * original
                assert abs(original) <= tau
                cost_change += coefficient * (smoothed - original)
                weighted_budget += tau * abs(coefficient) * sum(k * k
                                                                  for k in alpha)
    assert abs(cost_change) <= delta * weighted_budget

# Exhaustive finite-state feasibility confirms which labels need pruning.
feasible = [a for a in product(range(2), range(3), range(2), range(2))
            if all(tuple(a[i] for i in discrete) in labels
                   for _, discrete, labels in bags)]
assert len(feasible) == 12
for b, (_, discrete, labels) in enumerate(bags):
    extendable = {tuple(a[i] for i in discrete) for a in feasible}
    removed = set(labels) - extendable
    assert removed == ({(0, 2), (1, 2)} if b == 0 else set())
    for a in removed:
        assert moment(b, a, (0,) * len(bags[b][0])) == 0

# Empty continuous bags form the ordinary exact finite-state tree model.
# Its global feasible labels were enumerated above, and any finite law's
# expected additive objective is at least the minimum over those labels.
objective = lambda a: sum((b + 1) * sum(a[i] for i in bag[1])
                          for b, bag in enumerate(bags))
assert min(map(objective, feasible)) <= sum(weight * objective(a)
                                          for a, _, weight in atoms)
print(f"PASS: {checks} exact density evaluations; three moment orders;")
print("summed mixed separators, label masses, zero masses, diagonalization,")
print("mass-scaled error, unextendable-label pruning, and all-discrete case.")
