"""Targeted exact algebra checks for the CP-base face and Petersen example.

These checks do not prove SDP nonrepresentability or novelty.
"""

from itertools import combinations

import sympy as sp


n = 5
x = sp.symbols("x0:5")
slack = sp.symbols("s0:5")
exposing = (
    1
    - 2 * sum(x)
    + sum(xi**2 + si for xi, si in zip(x, slack))
    + 2 * sum(x[i] * x[j] for i, j in combinations(range(n), 2))
)
assert sp.expand(exposing - ((1 - sum(x)) ** 2 + sum(slack))) == 0

vectors = [
    sp.Matrix([1, 2, 0, 0, 0]),
    sp.Matrix([0, 1, 1, 0, 1]),
    sp.Matrix([0, 0, 0, 2, 0]),
]
Q = sum((v * v.T for v in vectors), sp.zeros(n))
e = sp.ones(n, 1)
scale = (e.T * Q * e)[0]
Y = Q / scale
weights = [(e.T * v)[0] ** 2 / scale for v in vectors]
points = [v / (e.T * v)[0] for v in vectors]
mean = sum((w * z for w, z in zip(weights, points)), sp.zeros(n, 1))
assert sum(weights) == 1
assert sum((w * z * z.T for w, z in zip(weights, points)), sp.zeros(n)) == Y
assert Y * e == mean
assert (e.T * Y * e)[0] == 1
assert 1 - 2 * sum(mean) + sum(Y) == 0

# Petersen vertices (i, 0) and (i, 1) are joined by the five spokes.
# Outer edges join distance-one indices; inner edges join distance-two.
spokes = {frozenset(((i, 0), (i, 1))) for i in range(5)}
outer = {frozenset(((i, 0), ((i + 1) % 5, 0))) for i in range(5)}
inner = {frozenset(((i, 1), ((i + 2) % 5, 1))) for i in range(5)}
edges = spokes | outer | inner
assert len(edges) == 15
assert all(
    sum((i, layer) in edge for edge in edges) == 3
    for i in range(5)
    for layer in range(2)
)
contracted = {frozenset(i for i, _ in edge) for edge in outer | inner}
assert contracted == {frozenset(pair) for pair in combinations(range(5), 2)}

print("PASS: symbolic exposing identity and exact CP-to-simplex normalization")
print("PASS: Petersen graph is cubic and contracting its spokes yields K5")
