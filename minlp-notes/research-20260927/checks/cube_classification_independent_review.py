"""Independent finite and symbolic checks for the strict cube classification.

This does not import the construction's checker or its table of orbit indices.
It closes contact sets under all equal sums of three edge-slack rows.
"""

from collections import Counter, defaultdict
from itertools import combinations, permutations

import sympy as s


# The bits of a vertex are x, y, z, in that order of increasing significance.
vertices = tuple(range(8))
edges = tuple((a, a ^ (1 << i), i) for a in vertices for i in range(3)
              if not (a >> i) & 1)
edge_index = {frozenset((a, b)): j for j, (a, b, _) in enumerate(edges)}
rows = []
for a, b, i in edges:
    row = [0] * 11
    row[a] = row[b] = 1
    row[8 + i] = -1
    rows.append(tuple(row))

# Every equality sum_{e in A} lambda_e = sum_{e in B} lambda_e
# with |A|=|B|=3 is discovered independently by exact row summation.
equal_sums = defaultdict(list)
for triple in combinations(range(12), 3):
    total = tuple(sum(rows[e][j] for e in triple) for j in range(11))
    equal_sums[total].append(frozenset(triple))
forcing = [group for group in equal_sums.values() if len(group) > 1]


def close_contacts(contacts):
    contacts = set(contacts)
    while True:
        old = set(contacts)
        for group in forcing:
            if any(triple <= contacts for triple in group):
                contacts.update(set().union(*group))
        if old == contacts:
            return frozenset(contacts)


def forbidden(contacts):
    degree = Counter(v for e in contacts for v in edges[e][:2])
    if max(degree.values()) >= 3:
        return True
    return any(sum(((edges[e][0] >> i) & 1) == b
                   and ((edges[e][1] >> i) & 1) == b for e in contacts) >= 3
               for i in range(3) for b in (0, 1))


maps = []
for permutation in permutations(range(3)):
    for complement in range(8):
        vertex_map = {
            a: sum(((a >> permutation[i]) & 1) << i for i in range(3))
            ^ complement for a in vertices
        }
        maps.append({e: edge_index[frozenset((vertex_map[a], vertex_map[b]))]
                     for e, (a, b, _) in enumerate(edges)})


def canonical(contacts):
    return min(tuple(sorted(mapping[e] for e in contacts)) for mapping in maps)


def from_endpoints(pairs):
    return frozenset(edge_index[frozenset(pair)] for pair in pairs)


family = from_endpoints(((0, 1), (0, 2), (1, 5), (2, 6), (3, 7)))
cycle = from_endpoints(((0, 1), (0, 2), (1, 5), (2, 6), (5, 7), (6, 7)))
orbit_sizes = Counter()
survivors = Counter()
for contacts in combinations(range(12), 5):
    orbit_sizes[canonical(contacts)] += 1
    closed = close_contacts(contacts)
    if forbidden(closed):
        continue
    pattern = canonical(closed)
    assert pattern in (canonical(family), canonical(cycle))
    survivors[len(closed)] += 1
assert len(orbit_sizes) == 24
assert sum(orbit_sizes.values()) == 792
assert survivors == {5: 24, 6: 24}

x, y, z, h, a, b, c, k, K = s.symbols('x y z h a b c k K')
L = h - a*x - b*y + c*z
D = a + b - h
T = z + x*y - x*z - y*z
family_polynomial = L**2 + 2*c*k*z*(1-x-y) + k*(2*D+k)*x*y
cycle_polynomial = L**2 + 2*K*T
assert s.expand(T - (z*(1-x)*(1-y) + x*y*(1-z))) == 0

family_contacts = [
    ((h/a, 0, 0), x), ((0, h/b, 0), y),
    ((1, 0, (a-h)/c), z), ((0, 1, (b-h)/c), z),
    ((1, 1, (D+k)/c), z),
]
cycle_contacts = [
    ((h/a, 0, 0), x), ((0, h/b, 0), y),
    ((1, 0, (a-h)/c), z), ((0, 1, (b-h)/c), z),
    (((h-b+c)/a, 1, 1), x), ((1, (h-a+c)/b, 1), y),
]
for polynomial, contacts in ((family_polynomial, family_contacts),
                              (cycle_polynomial, cycle_contacts)):
    for point, direction in contacts:
        values = dict(zip((x, y, z), point))
        assert s.factor(polynomial.subs(values)) == 0
        assert s.factor(s.diff(polynomial, direction).subs(values)) == 0

# This exact rational six-cycle witness checks feasibility in the strict regime.
cycle_witness = s.expand(cycle_polynomial.subs(
    {h: s.Rational(1, 2), a: 1, b: 1, c: 1, K: s.Rational(1, 2)}))
Q = s.hessian(cycle_witness, (x, y, z)) / 2
assert all(Q[i, i] > 0 for i in range(3))
assert all(Q.extract(pair, pair).det() < 0 for pair in combinations(range(3), 2))
assert all(cycle_witness.subs({x: (v & 1), y: ((v >> 1) & 1), z: ((v >> 2) & 1)}) > 0
           for v in vertices)

# Exact ranks are illustrative checks at rational parameter points, not a
# replacement for the argument covering every strict parameter tuple.
basis = [s.Integer(1), x, y, z, x*x, y*y, z*z, x*y, x*z, y*z]
for contacts, parameters, expected in (
    (family_contacts, {h: s.Rational(1, 2), a: 1, b: 1, c: 3, k: 1}, 9),
    (cycle_contacts, {h: s.Rational(1, 2), a: 1, b: 1, c: 1}, 8),
):
    constraint_rows = []
    for point, direction in contacts:
        values = dict(zip((x, y, z), point))
        constraint_rows.append([term.subs(values).subs(parameters) for term in basis])
        constraint_rows.append([s.diff(term, direction).subs(values).subs(parameters)
                                for term in basis])
    assert s.Matrix(constraint_rows).rank() == expected

print('PASS: independent closure of all 792 patterns; 24 symmetry orbits.')
print('PASS: 24 surviving five-edge patterns and 24 patterns forcing a six-cycle.')
print('PASS: symbolic family/cycle contacts, triangle identity, strict cycle witness.')
print('PASS: exact illustrative contact ranks: family 9, six-cycle 8.')
