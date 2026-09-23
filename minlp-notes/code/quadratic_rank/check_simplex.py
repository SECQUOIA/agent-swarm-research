"""Exact rational checks supporting the quadratic-rank geometric lemma.

These checks exercise all Hessian signatures, maximal-simplex enclosure,
the polarization identity, and rank-deficient principal-minor restriction.
They do not replace the general proof.
"""
from itertools import combinations
import random
import sympy as sp

rng = random.Random(20260905)
checked = 0
for d in range(1, 5):
    for negative in range(d + 1):
        for trial in range(3):
            while True:
                transform = sp.Matrix(d, d, lambda i, j: rng.randint(-3, 3))
                if transform.det():
                    break
            diagonal = sp.diag(*[-(i + 1) if i < negative else i + 1 for i in range(d)])
            hessian = transform.T * diagonal * transform
            pts = [sp.zeros(d, 1)] + [sp.eye(d)[:, i] for i in range(d)]
            pts += [sp.Matrix([rng.randint(-4, 4) for _ in range(d)]) for _ in range(3)]
            best = None
            for ids in combinations(range(len(pts)), d + 1):
                origin = pts[ids[0]]
                basis = sp.Matrix.hstack(*(pts[i] - origin for i in ids[1:]))
                determinant = abs(basis.det())
                if best is None or determinant > best[0]:
                    best = determinant, origin, basis
            determinant, origin, basis = best
            assert determinant > 0
            inverse = basis.inv()
            for point in pts:
                assert all(abs(c) <= 1 for c in inverse * (point - origin))
            quadratic = lambda v: (v.T * hessian * v)[0] / 2
            delta = max(abs(quadratic(u - v)) for u, v in combinations(pts, 2))
            gram = basis.T * hessian * basis
            assert gram.det() == basis.det() ** 2 * hessian.det()
            assert all(abs(gram[i, j]) <= (2 if i == j else 3) * delta
                       for i in range(d) for j in range(d))
            row_square_product = sp.prod(sum(gram[i, j] ** 2 for j in range(d))
                                         for i in range(d))
            assert gram.det() ** 2 <= row_square_product <= (9 * d * delta ** 2) ** d
            checked += 1

restricted = 0
for n in range(2, 7):
    for rank in range(1, n):
        while True:
            basis = sp.Matrix(n, rank, lambda i, j: rng.randint(-3, 3))
            if basis.rank() == rank:
                break
        diagonal = sp.diag(*[(-1) ** i * (i + 1) for i in range(rank)])
        hessian = basis * diagonal * basis.T
        assert hessian.rank() == rank
        principal = [ids for ids in combinations(range(n), rank)
                     if hessian.extract(ids, ids).det()]
        assert principal
        ids = principal[0]
        core = hessian.extract(ids, ids)
        columns = hessian[:, list(ids)]
        assert hessian == columns * core.inv() * columns.T
        restricted += 1

print(f"PASS: {checked} exact maximal-simplex cases across all signatures in dimensions 1..4")
print(f"PASS: {restricted} exact rank-deficient principal-minor and factorization cases")
