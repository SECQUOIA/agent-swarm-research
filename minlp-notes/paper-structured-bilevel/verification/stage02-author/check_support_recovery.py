"""Exact regression for support-tuple reconstruction, not a QE implementation.

Generate support tuples independently from all ray and pair-of-ray directions
of planar interval-image sums. Test reconstruction of original Cartesian-sum
points and interior targets, including lower-dimensional images and Q(sqrt(2)).
"""
from itertools import combinations, product
import random
import sympy as s


def clean(x):
    return s.simplify(x)


def dot(a, b):
    return clean(sum(x*y for x, y in zip(a, b)))


def aggregate(vectors, z):
    return tuple(clean(sum(v[i]*t for v, t in zip(vectors, z))) for i in range(2))


def support_tuples(vectors):
    rays = [(s.Integer(1), s.Integer(0)), (s.Integer(-1), s.Integer(0))]
    for a, b in vectors:
        if a != 0 or b != 0:
            rays += [(b, -a), (-b, a)]
    directions = rays + [tuple(clean(u[i]+v[i]) for i in range(2))
                         for u, v in combinations(rays, 2)]
    # Lower endpoint breaks a support tie. All comparisons are exact.
    tuples = {tuple(s.Integer(1) if dot(v, u) > 0 else s.Integer(0)
                    for v in vectors) for u in directions}
    return sorted(tuples)


def recover(vectors, tuples, target):
    sums = [aggregate(vectors, z) for z in tuples]
    for q in range(1, 4):
        for ids in combinations(range(len(tuples)), q):
            mat = s.Matrix([[sums[j][i] for j in ids] for i in range(2)]
                           + [[s.Integer(1)]*q])
            rhs = s.Matrix(list(target)+[s.Integer(1)])
            # Independent row subsets avoid solving an underdetermined system.
            for rows in combinations(range(3), q):
                square = mat[list(rows), :]
                if clean(square.det()) == 0:
                    continue
                theta = square.inv()*rhs[list(rows), :]
                theta = theta.applyfunc(clean)
                if any(clean(v) != 0 for v in mat*theta-rhs):
                    break
                if any(v < 0 for v in theta):
                    break
                z = tuple(clean(sum(theta[t]*tuples[j][b]
                                    for t, j in enumerate(ids)))
                          for b in range(len(vectors)))
                assert all(0 <= v <= 1 for v in z)
                assert aggregate(vectors, z) == tuple(map(clean, target))
                assert sum(theta) == 1
                assert len(ids) <= 3
                return z, theta
    raise AssertionError(('target not recovered', vectors, tuples, target))


rng = random.Random(20260907)
cases = [[], [(0, 0)], [(1, 0), (2, 0), (-1, 0)],
         [(1, 0), (0, 1), (1, 1)], [(1, 1), (1, 1), (0, 0)]]
for _ in range(12):
    cases.append([tuple(s.Integer(rng.randint(-3, 3)) for _ in range(2))
                  for _ in range(rng.randint(1, 4))])
count = 0
for vectors in cases:
    tuples = support_tuples(vectors)
    originals = list(product([s.Integer(0), s.Integer(1)], repeat=len(vectors)))
    # Every original Cartesian vertex image must lie in the support-tuple hull.
    for z in originals:
        recover(vectors, tuples, aggregate(vectors, z))
        count += 1
    # Recover targets in the interior of the whole product, not just support sums.
    for _ in range(3):
        z = tuple(s.Rational(rng.randint(0, 7), 7) for _ in vectors)
        recover(vectors, tuples, aggregate(vectors, z))
        count += 1

root = s.sqrt(2)
vectors = [(root, s.Integer(1)), (s.Integer(1), -root), (0, 0)]
tuples = support_tuples(vectors)
for z in [(s.Rational(1, 3), s.Rational(2, 5), s.Rational(4, 7)),
          ((root-1)/2, (3-root)/3, s.Integer(0))]:
    answer, weights = recover(vectors, tuples, aggregate(vectors, z))
    for a in answer + tuple(weights):
        # This checks that recovery has not adjoined unrelated algebraic roots.
        s.to_number_field(a, root)
    count += 1
print(f'PASS: {count} exact support-hull/recovery targets across {len(cases)+1} cases; '
      'empty, singleton, collinear, duplicate, zero-image and Q(sqrt(2)) cases.')
