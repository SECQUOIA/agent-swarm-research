"""Exact nonlinear checks of pinning, primal components, and weighted work.

The fixtures have separable convex cubics after fixing their integer labels.
This gives an independent exact whole-instance oracle with square-root
values.  It is not an implementation of the general component solver.
"""

from fractions import Fraction as Q
from functools import lru_cache
from itertools import combinations, product
from math import isqrt, prod


@lru_cache(None)
def square_part(n):
    outside, inside, divisor = 1, 1, 2
    while divisor * divisor <= n:
        exponent = 0
        while n % divisor == 0:
            n //= divisor
            exponent += 1
        outside *= divisor ** (exponent // 2)
        if exponent % 2:
            inside *= divisor
        divisor += 1
    return outside, inside * n


class Radical:
    """A rational linear combination of distinct squarefree square roots."""

    def __init__(self, value=0, terms=None):
        self.terms = {1: Q(value)} if value else {}
        for radicand, coefficient in (terms or {}).items():
            factor, squarefree = square_part(radicand)
            self.terms[squarefree] = self.terms.get(squarefree, Q(0)) + coefficient * factor
        self.terms = {key: value for key, value in self.terms.items() if value}

    @staticmethod
    def sqrt(value):
        value = Q(value)
        assert value >= 0
        if not value:
            return Radical()
        return Radical(terms={value.numerator * value.denominator: Q(1, value.denominator)})

    def __add__(self, other):
        other = other if isinstance(other, Radical) else Radical(other)
        terms = dict(self.terms)
        for key, value in other.terms.items():
            terms[key] = terms.get(key, Q(0)) + value
        return Radical(terms=terms)

    __radd__ = __add__

    def __neg__(self):
        return Radical(terms={key: -value for key, value in self.terms.items()})

    def __sub__(self, other):
        return self + (-other if isinstance(other, Radical) else -Q(other))

    def __mul__(self, other):
        other = other if isinstance(other, Radical) else Radical(other)
        terms = {}
        for left, a in self.terms.items():
            for right, b in other.terms.items():
                key = left * right
                terms[key] = terms.get(key, Q(0)) + a * b
        return Radical(terms=terms)

    __rmul__ = __mul__

    def __pow__(self, exponent):
        result = Radical(1)
        for _ in range(exponent):
            result *= self
        return result

    def enclosure(self, bits):
        denominator = 1 << bits
        lower = upper = Q(0)
        for radicand, coefficient in self.terms.items():
            floor = isqrt(radicand * denominator * denominator)
            lo = Q(floor, denominator)
            hi = lo if floor * floor == radicand * denominator * denominator else lo + Q(1, denominator)
            lower += coefficient * (lo if coefficient > 0 else hi)
            upper += coefficient * (hi if coefficient > 0 else lo)
        return lower, upper

    def sign(self):
        # Distinct squarefree square roots are linearly independent over Q.
        if not self.terms:
            return 0
        for bits in (4, 8, 16, 32, 64, 128, 256):
            lower, upper = self.enclosure(bits)
            if lower > 0:
                return 1
            if upper < 0:
                return -1
        raise AssertionError("Fixture comparison exceeded its exact precision budget")

    def __eq__(self, other):
        return (self - other).terms == {}

    def __lt__(self, other):
        return (self - other).sign() < 0


def add_term(polynomial, powers, coefficient):
    polynomial[powers] = polynomial.get(powers, Q(0)) + coefficient
    if not polynomial[powers]:
        del polynomial[powers]


def with_noise(polynomial, noise):
    result = dict(polynomial)
    for i, coefficient in enumerate(noise):
        powers = tuple(int(j == i) for j in range(len(noise)))
        add_term(result, powers, coefficient)
    return result


def substitute(polynomial, pinned):
    result = {}
    for powers, coefficient in polynomial.items():
        remaining = list(powers)
        for i, value in pinned.items():
            coefficient *= value ** remaining[i]
            remaining[i] = 0
        add_term(result, tuple(remaining), coefficient)
    return result


def evaluate(polynomial, point):
    return sum((coefficient * prod(point[i] ** power for i, power in enumerate(powers))
                for powers, coefficient in polynomial.items()), Radical())


def power_range(lower, upper, exponent):
    if exponent == 0:
        return Q(1), Q(1)
    values = [lower**exponent, upper**exponent]
    if exponent % 2 == 0 and lower <= 0 <= upper:
        values.append(Q(0))
    return min(values), max(values)


def multiply_intervals(left, right):
    values = [x * y for x in left for y in right]
    return min(values), max(values)


def derivative(polynomial, coordinate):
    result = {}
    for powers, coefficient in polynomial.items():
        if powers[coordinate]:
            target = list(powers)
            target[coordinate] -= 1
            add_term(result, tuple(target), coefficient * powers[coordinate])
    return result


def interval(polynomial, bounds):
    lower = upper = Q(0)
    for powers, coefficient in polynomial.items():
        term = (coefficient, coefficient)
        for (lo, hi), exponent in zip(bounds, powers):
            term = multiply_intervals(term, power_range(lo, hi, exponent))
        lower += term[0]
        upper += term[1]
    return lower, upper


def primal_graph(polynomial, n):
    graph = [set() for _ in range(n)]
    for powers in polynomial:
        for i, j in combinations([i for i, power in enumerate(powers) if power], 2):
            graph[i].add(j)
            graph[j].add(i)
    return graph


def components(graph, bad):
    remaining, result = set(bad), []
    while remaining:
        todo, found = [remaining.pop()], []
        while todo:
            vertex = todo.pop()
            found.append(vertex)
            neighbors = graph[vertex] & remaining
            remaining.difference_update(neighbors)
            todo.extend(neighbors)
        result.append(sorted(found))
    return result


def exact_oracle(polynomial, bounds, integer, active):
    """Integer enumeration + exact conditional separable-cubic minimization."""
    discrete = [i for i in active if integer[i]]
    continuous = [i for i in active if not integer[i]]
    labels = [range(int(bounds[i][0]), int(bounds[i][1]) + 1) for i in discrete]
    best = None
    for assignment in product(*labels):
        pinned = dict(zip(discrete, map(Q, assignment)))
        reduced = substitute(polynomial, pinned)
        point = {i: Radical(value) for i, value in pinned.items()}
        constant = reduced.get((0,) * len(bounds), Q(0))
        value = Radical(constant)
        covered = {(0,) * len(bounds)}
        for i in continuous:
            assert bounds[i] == (Q(0), Q(1))
            linear_key = tuple(int(j == i) for j in range(len(bounds)))
            cubic_key = tuple(3 * int(j == i) for j in range(len(bounds)))
            linear, cubic = reduced.get(linear_key, Q(0)), reduced.get(cubic_key, Q(0))
            assert cubic >= 0
            covered.update([linear_key, cubic_key])
            if linear >= 0:
                point[i], local_value = Radical(), Radical()
            elif linear <= -3 * cubic:
                point[i], local_value = Radical(1), Radical(cubic + linear)
            else:
                point[i] = Radical.sqrt(-linear / (3 * cubic))
                local_value = 2 * linear * point[i] * Q(1, 3)
            value += local_value
        assert set(reduced) <= covered, "The diagnostic oracle has a restricted scope"
        if best is None or value < best[0]:
            best = value, point
    assert best is not None
    return best


def component_optimizer(polynomial, bounds, integer, noise):
    ranges = [interval(derivative(polynomial, i), bounds) for i in range(len(bounds))]
    pinned, bad, equalities = {}, [], 0
    for i, ((lower, upper), gamma) in enumerate(zip(ranges, noise)):
        if gamma > -lower:
            pinned[i] = bounds[i][0]
        elif gamma < -upper:
            pinned[i] = bounds[i][1]
        else:
            bad.append(i)
            equalities += gamma in (-lower, -upper)
    sampled = with_noise(polynomial, noise)
    reduced = substitute(sampled, pinned)
    graph = primal_graph(polynomial, len(bounds))
    partition = components(graph, bad)
    constant = reduced.get((0,) * len(bounds), Q(0))
    value, point = Radical(constant), {i: Radical(v) for i, v in pinned.items()}
    for component in partition:
        local = {}
        for powers, coefficient in reduced.items():
            support = {i for i, exponent in enumerate(powers) if exponent}
            if support & set(component):
                assert support <= set(component), "A surviving hyperedge crossed components"
                local[powers] = coefficient
        local_value, local_point = exact_oracle(local, bounds, integer, component)
        value += local_value
        point.update(local_point)
    assert evaluate(sampled, point) == value
    return value, point, len(pinned), equalities, len(partition)


def fixtures():
    return [
        ({(3, 0, 0, 0): Q(1), (1, 1, 1, 0): Q(1, 4),
          (1, 1, 0, 0): -Q(1, 2), (1, 0, 0, 0): -Q(1, 2),
          (0, 4, 0, 0): Q(1, 12), (0, 2, 0, 0): -Q(1, 2),
          (0, 0, 4, 0): Q(1, 16), (0, 0, 1, 0): -Q(1, 3),
          (0, 0, 2, 1): Q(1, 5), (0, 0, 0, 4): Q(1, 7)},
         [(Q(0), Q(1)), (Q(0), Q(2)), (Q(-1), Q(1)), (Q(0), Q(1))],
         [False, True, True, True], Q(3)),
        ({(3, 0, 0): Q(1), (0, 3, 0): Q(1), (1, 0, 0): -Q(1, 2),
          (0, 1, 0): -Q(1, 3), (1, 0, 1): Q(1, 3),
          (0, 1, 1): -Q(1, 4), (0, 0, 4): Q(1, 5)},
         [(Q(0), Q(1))] * 3, [False, False, True], Q(1)),
        ({(1, 1, 1): Q(1, 3), (4, 0, 0): Q(1, 7),
          (0, 4, 0): -Q(1, 5), (0, 0, 3): Q(1, 9)},
         [(Q(0), Q(2)), (Q(-1), Q(1)), (Q(0), Q(1))],
         [True] * 3, Q(2)),
        ({(3,): Q(1), (1,): -Q(1)}, [(Q(0), Q(1))], [False], Q(1)),
    ]


def atom_count(lower, upper, sigma, count):
    low_index = ((lower + sigma) * (count - 1) / (2 * sigma))
    high_index = ((upper + sigma) * (count - 1) / (2 * sigma))
    first = max(0, -((-low_index.numerator) // low_index.denominator))
    last = min(count - 1, high_index.numerator // high_index.denominator)
    return max(0, last - first + 1)


def main():
    counts = dict(draws=0, pins=0, equality_atoms=0, split_draws=0,
                  derivative_probes=0, refinements=0, probability_patterns=0)
    for polynomial, bounds, integer, sigma in fixtures():
        n = len(bounds)
        ranges = [interval(derivative(polynomial, i), bounds) for i in range(n)]
        probes = [[lo, (lo + hi) / 2, hi] for lo, hi in bounds]
        for probe in product(*probes):
            point = {i: Radical(x) for i, x in enumerate(probe)}
            for i, (lower, upper) in enumerate(ranges):
                exact = evaluate(derivative(polynomial, i), point)
                assert not exact < lower and not Radical(upper) < exact
                counts["derivative_probes"] += 1
        atoms = [-sigma + 2 * sigma * j / 3 for j in range(4)]
        for lower, upper in ranges:
            direct = sum(-upper <= gamma <= -lower for gamma in atoms)
            assert direct == atom_count(-upper, -lower, sigma, 4)
        for noise in product(atoms, repeat=n):
            value, point, pins, equalities, pieces = component_optimizer(polynomial, bounds, integer, noise)
            want, _ = exact_oracle(with_noise(polynomial, noise), bounds, integer, range(n))
            assert value == want
            for i, (lo, hi) in enumerate(bounds):
                assert not point[i] < lo and not Radical(hi) < point[i]
            counts["draws"] += 1
            counts["pins"] += pins
            counts["equality_atoms"] += equalities
            counts["split_draws"] += pieces > 1
            # Feasible numerical evaluation uses rational bounds only.
            if counts["draws"] % 13 == 0:
                rational_point = {i: Radical(max(bounds[i][0], min(bounds[i][1], x.enclosure(48)[0])))
                                  for i, x in point.items()}
                gap = evaluate(with_noise(polynomial, noise), rational_point) - value
                assert gap.sign() >= 0 and not Radical(Q(1, 1 << 30)) < gap
                lower, upper = value.enclosure(48)
                assert upper - lower <= Q(1, 1 << 30)
                counts["refinements"] += 1

        # Put one derivative threshold exactly at the left noise endpoint.
        # Each bad event then has probability 1/M, including the equality atom.
        sigma, grid_count = Q(1000), 256
        shifted = with_noise(polynomial, [sigma - lower for lower, _ in ranges])
        shifted_ranges = [interval(derivative(shifted, i), bounds) for i in range(n)]
        probabilities = [Q(atom_count(-hi, -lo, sigma, grid_count), grid_count)
                         for lo, hi in shifted_ranges]
        assert probabilities == [Q(1, grid_count)] * n
        weights = [7 if not integer[i] else int(bounds[i][1] - bounds[i][0] + 1)
                   for i in range(n)]
        graph = primal_graph(polynomial, n)
        degree = max(1, max(map(len, graph)))
        beta = max(a * q for a, q in zip(weights, probabilities))
        assert 4 * degree * beta < 1
        expectation = Q(0)
        for pattern in product([False, True], repeat=n):
            probability = prod(q if bad else 1 - q for bad, q in zip(pattern, probabilities))
            cost = sum(prod(weights[i] for i in component)
                       for component in components(graph, [i for i, bad in enumerate(pattern) if bad]))
            expectation += probability * cost
            counts["probability_patterns"] += 1
        bound = sum(a * q for a, q in zip(weights, probabilities)) / (1 - 4 * degree * beta)
        assert expectation <= bound
    assert counts["equality_atoms"] and counts["split_draws"] and counts["refinements"]
    print("Exact strong-field polynomial diagnostics passed:", counts)


if __name__ == "__main__":
    main()
