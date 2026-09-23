"""Independent finite checks. Rational probability checks are exact.

The random-sign bound uses floating-point log/sqrt only for its final comparison.
No finite check here establishes a universal envelope or graph theorem.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import combinations, product
from math import log, sqrt


def threshold(means):
    cuts = sorted({F(0), F(1), *means})
    law = defaultdict(F)
    for left, right in zip(cuts, cuts[1:]):
        u = (left + right) / 2
        law[tuple(int(u < p) for p in means)] += right - left
    return law


def circle(means):
    starts, lengths, cuts = [], [], {F(0), F(1)}
    cursor = F(0)
    for p in means:
        starts.append(cursor % 1)
        lengths.append(1 - p)
        cuts.update({cursor % 1, (cursor + 1 - p) % 1})
        cursor += 1 - p
    law = defaultdict(F)
    cuts = sorted(cuts)
    for left, right in zip(cuts, cuts[1:]):
        u = (left + right) / 2
        law[tuple(int((u - a) % 1 >= d) for a, d in zip(starts, lengths))] += right - left
    return law


def independent(means):
    law = {}
    for x in product((0, 1), repeat=len(means)):
        mass = F(1)
        for z, p in zip(x, means):
            mass *= p if z else 1 - p
        law[x] = mass
    return law


def expect(law, fn):
    return sum((mass * fn(x) for x, mass in law.items()), F(0))


def check_marginals(law, means):
    assert sum(law.values()) == 1
    assert all(mass >= 0 for mass in law.values())
    assert tuple(expect(law, lambda x, i=i: x[i]) for i in range(len(means))) == means


count = 0
for n in range(1, 5):
    for means in product((F(0), F(1, 4), F(1, 2), F(3, 4), F(1)), repeat=n):
        upper, lower, indep = threshold(means), circle(means), independent(means)
        for law in (upper, lower, indep):
            check_marginals(law, means)
        assert expect(lower, lambda x: int(all(x))) == max(F(0), sum(means) - n + 1)
        mixture = defaultdict(F)
        for weight, law in ((F(1, 6), upper), (F(1, 3), lower), (F(1, 2), indep)):
            for x, mass in law.items():
                mixture[x] += weight * mass
        check_marginals(mixture, means)
        for k in range(1, n + 1):
            for support in combinations(range(n), k):
                anchor = min(support, key=lambda i: means[i])
                success = lambda x: int(all(x[i] for i in support))
                deficiency = lambda x: x[anchor] - success(x)
                assert expect(upper, success) == min(means[i] for i in support)
                assert all(deficiency(x) >= 0 for x in mixture)
                assert expect(mixture, deficiency) == means[anchor] - expect(mixture, success)
                assert expect(mixture, deficiency) == (
                    F(1, 6) * expect(upper, deficiency)
                    + F(1, 3) * expect(lower, deficiency)
                    + F(1, 2) * expect(indep, deficiency)
                )
        count += 1
print(f'EXACT: normalized circle, threshold, independent, and mixture laws at {count} mean vectors; all singleton means and all threshold joint-success probabilities passed.')

# f(x)=x1*x2*x3 on [1,2]^3 at physical means 3/2.
# Endpoint values are 2**k. The affine minorant 2*k is tight at k=1,2.
law = {x: F(1, 6) for x in product((0, 1), repeat=3) if sum(x) in (1, 2)}
means = (F(1, 2),) * 3
check_marginals(law, means)
assert all(2 ** sum(x) >= 2 * sum(x) for x in product((0, 1), repeat=3))
lower = expect(law, lambda x: 2 ** sum(x))
upper = expect(threshold(means), lambda x: 2 ** sum(x))
expanded_lower = F(1) + sum(means)  # All degree >=2 monomial lower envelopes vanish.
assert (lower, upper, upper - lower, upper - expanded_lower) == (F(3), F(9, 2), F(3, 2), F(2))
print('EXACT: original positive-box gap 3/2 < expanded termwise gap 2; common upper value 9/2.')

edges = list(combinations(range(4), 2))
signs = list(product((-1, 1), repeat=4))
graphs = 0
for mask in range(1, 1 << len(edges)):
    active = [e for k, e in enumerate(edges) if mask >> k & 1]
    values = []
    for weights in product((-1, 1), repeat=len(active)):
        q = [sum(a * s[i] * s[j] for (i, j), a in zip(active, weights)) for s in signs]
        values.append(max(map(abs, q)))
        # Antipodal pairing preserves zero means and the selected Q value exactly.
        for s, qvalue in zip(signs, q):
            assert sum(a * (-s[i]) * (-s[j]) for (i, j), a in zip(active, weights)) == qvalue
    expected_z = F(sum(values), len(values))
    assert float(expected_z) <= sqrt(2 * len(active) * 4 * log(2)) + 1e-12
    graphs += 1
print(f'NUMERICAL FINAL COMPARISON: exact enumerated E[Z] satisfies the displayed random-sign bound for all {graphs} nonempty labeled graphs on 4 vertices; sign averaging itself is exact.')
