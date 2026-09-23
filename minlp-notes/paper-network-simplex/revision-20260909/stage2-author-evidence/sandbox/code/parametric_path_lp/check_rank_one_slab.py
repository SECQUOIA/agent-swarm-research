"""Exact checks of telescoping identity, vertices, and subset-sum slabs."""
from fractions import Fraction as F
from itertools import product
import random
import sympy as sp


def vertex(bits, eps):
    values = []
    previous = F(0)
    for bit in bits:
        previous = bit+(1-2*bit)*eps*previous
        values.append(previous)
    return values


def linear(values, eps):
    n = len(values)
    return values[-1]-(1-eps)*sum(eps**(2*(n-i)-1)*values[i-1] for i in range(1, n))


for n in range(1, 9):
    x = [sp.Integer(0)]+list(sp.symbols(f'x1:{n+1}'))
    e = sp.symbols('e')
    lhs = x[n]-(1-e)*sum(e**(2*(n-i)-1)*x[i] for i in range(1, n))-x[n]**2
    rhs = sum(e**(2*(n-j))*(x[j]-e*x[j-1])*(1-e*x[j-1]-x[j])
              for j in range(1, n+1))
    assert sp.expand(lhs-rhs) == 0
rng = random.Random(103)
slabs = witnesses = 0
for case in range(40):
    n = rng.randint(1, 7)
    weights = [rng.randint(1, 10) for _ in range(n)]
    total = sum(weights)
    eps = F(1, 8*total)
    subsets, vertex_sums = set(), []
    for bits in product([0, 1], repeat=n):
        point = vertex(bits, eps)
        assert linear(point, eps) == point[-1]**2
        subset = sum(a*b for a, b in zip(weights, bits))
        value = sum(a*b for a, b in zip(weights, point))
        assert abs(value-subset) <= F(1, 8)
        subsets.add(subset)
        vertex_sums.append(value)
        witnesses += 1
    for target in range(total+1):
        assert any(abs(value-target) <= F(1, 4) for value in vertex_sums) == (target in subsets)
        slabs += 1
    point = []
    previous = F(0)
    for j in range(n):
        previous = eps*previous+F(1, 3)*(1-2*eps*previous)
        point.append(previous)
    assert linear(point, eps)-point[-1]**2 > 0
print(f'PASS8 symbolic dimensions; {witnesses} rational vertex/rounding checks; '
      f'{slabs} exact subset-sum slab comparisons;40 strict interior controls')
