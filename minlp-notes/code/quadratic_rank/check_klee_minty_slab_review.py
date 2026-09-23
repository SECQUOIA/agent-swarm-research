"""Independent exact quadratic minimization on clipped Klee-Minty cubes.

Enumerates original vertices and every edge intersection with each slab
boundary, giving all vertices of the clipped polytope. A concave quadratic
attains its minimum at one of these vertices.
"""

from fractions import Fraction as F
from itertools import product
from random import Random

import sympy as sp


def vertex(bits, epsilon):
    values = []
    previous = F(0)
    for bit in bits:
        previous = bit+(1-2*bit)*epsilon*previous
        values.append(previous)
    return tuple(values)


def objective(x, epsilon):
    n = len(x)
    linear = x[-1]-(1-epsilon)*sum(
        epsilon**(2*(n-i)-1)*x[i-1] for i in range(1, n))
    return linear-x[-1]**2


def solve(weights, target):
    n = len(weights)
    epsilon = F(1, 8*sum(weights))
    bits = list(product((0, 1), repeat=n))
    vertices = {u: vertex(u, epsilon) for u in bits}
    scalar = lambda x: sum(w*t for w, t in zip(weights, x))
    low, high = F(target)-F(1, 4), F(target)+F(1, 4)
    candidates = {x for x in vertices.values() if low <= scalar(x) <= high}
    for u, x in vertices.items():
        assert objective(x, epsilon) == 0
        for i, bit in enumerate(u):
            if bit:
                continue
            other = u[:i]+(1,)+u[i+1:]
            y = vertices[other]
            ax, ay = scalar(x), scalar(y)
            if ax == ay:
                continue
            for bound in (low, high):
                ratio = (bound-ax)/(ay-ax)
                if 0 <= ratio <= 1:
                    candidates.add(tuple(a+ratio*(b-a) for a, b in zip(x, y)))
    assert candidates
    values = [objective(x, epsilon) for x in candidates]
    assert min(values) >= 0
    subset_yes = any(sum(w*b for w, b in zip(weights, u)) == target for u in bits)
    assert (min(values) == 0) == subset_yes
    return len(candidates)


def main():
    epsilon = sp.Symbol("epsilon")
    for n in range(1, 7):
        x = (sp.Integer(0),)+sp.symbols(f"x1:{n+1}")
        left = x[n]-(1-epsilon)*sum(
            epsilon**(2*(n-i)-1)*x[i] for i in range(1, n))-x[n]**2
        right = sum(epsilon**(2*(n-j))*(x[j]-epsilon*x[j-1])
                    *(1-epsilon*x[j-1]-x[j]) for j in range(1, n+1))
        assert sp.expand(left-right) == 0
    rng = Random(79)
    count = 0
    for n in range(2, 8):
        for _ in range(12):
            weights = [rng.randrange(1, 10) for _ in range(n)]
            target = rng.randrange(sum(weights)+1)
            count += solve(weights, target)
    print(f"PASS: six symbolic identities; 72 exact clipped-polytope QPs; {count} candidate vertices")


if __name__ == "__main__":
    main()
