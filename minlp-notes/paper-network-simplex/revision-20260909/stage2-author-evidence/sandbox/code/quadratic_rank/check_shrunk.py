"""Exact checks of symmetric shrinking after nonorthogonal congruences.

These examples test the coordinate-conversion lemma, not the imported
noncommutative-rank theorem. All arithmetic is exact over the rationals.
"""
import random
import sympy as sp

rng = random.Random(29017)


def colspace(matrix):
    cols = matrix.columnspace()
    return sp.Matrix.hstack(*cols) if cols else sp.zeros(matrix.rows, 0)


def intersection(left, right):
    kernel = left.row_join(-right).nullspace()
    cols = [left * v[:left.cols, :] for v in kernel]
    return colspace(sp.Matrix.hstack(*cols)) if cols else sp.zeros(left.rows, 0)


def perpendicular(matrix):
    cols = matrix.T.nullspace()
    return sp.Matrix.hstack(*cols) if cols else sp.zeros(matrix.rows, 0)


count = 0
for z, w, c in [(2, 1, 1), (3, 1, 2), (3, 2, 2), (4, 1, 0)]:
    n = z + w + c
    for repeat in range(5):
        # Each original H maps U0=Z+R to V0=W+R; the dimensions differ z-w.
        matrices = []
        for j in range(3):
            b = sp.Matrix(z, w, lambda *_: rng.randint(-3, 3))
            cc = sp.Matrix(w, w, lambda *_: rng.randint(-3, 3))
            cc = cc + cc.T
            d = sp.Matrix(w, c, lambda *_: rng.randint(-3, 3))
            e = sp.Matrix(c, c, lambda *_: rng.randint(-3, 3))
            e = e + e.T
            matrices.append(sp.BlockMatrix([
                [sp.zeros(z), b, sp.zeros(z, c)],
                [b.T, cc, d],
                [sp.zeros(c, z), d.T, e],
            ]).as_explicit())
        p = sp.eye(n)
        for _ in range(2*n):
            a, b = rng.sample(range(n), 2)
            p[a, :] = p[a, :] + rng.choice([-2, -1, 1, 2]) * p[b, :]
        hs = [p.T * h * p for h in matrices]
        u0 = sp.eye(n)[:, list(range(z)) + list(range(z+w, n))]
        v0 = sp.eye(n)[:, list(range(z, n))]
        u = p.inv() * u0
        v = p.T * v0
        zz = intersection(u, perpendicular(v))
        ww = intersection(v, perpendicular(u))
        rr = perpendicular(zz.row_join(ww))
        assert zz.cols - ww.cols == z-w
        assert zz.T * ww == sp.zeros(zz.cols, ww.cols)
        q = zz.row_join(ww).row_join(rr)
        assert q.det() != 0
        for h in hs:
            assert colspace(v.row_join(h*u)).cols == v.cols
            assert colspace(ww.row_join(h*zz)).cols == ww.cols
            g = q.T*h*q
            assert g[:zz.cols, :zz.cols] == sp.zeros(zz.cols)
            assert g[:zz.cols, zz.cols+ww.cols:] == sp.zeros(zz.cols, rr.cols)
        assert 2*ww.cols+rr.cols == n-(z-w)
        count += 1
print(f'PASS: {count} exact nonorthogonal congruences; symmetric shrinking, block zeros, and precision sums')
