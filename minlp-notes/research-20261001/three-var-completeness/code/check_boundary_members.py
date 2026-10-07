"""Exact checks for family members on the boundary stratum d3 = D + k
(note.md, Proposition 2.7).

For rational 0 < h < min(d1, d2), k > 0 and d3 = D + k (D = d1 + d2 - h):
  * q = q_{h,d,k} is nonnegative (polynomial identity of the family note,
    rechecked here symbolically),
  * the twelve edge restrictions are nonnegative and the zero set on the
    cube consists of the four edge contacts a, b, c, d and the vertex (1,1,1),
  * the vertex zero is tangential (the z-edge restriction is d3^2 (z-1)^2);
    the 10 linear contact conditions (values and edge derivatives at the
    five contacts, the z-derivative at the vertex included) have rank 9,
    so q spans an extreme ray of the cone of cube-nonnegative quadratics;
    without the tangency equation the rank is 8,
  * the origin is blocked in the sense of Lemma 2.4, so q is not in D3.
All arithmetic is exact (sympy rationals).
"""
from itertools import combinations, product

import sympy as sp

x, y, z = sp.symbols('x y z')


def family(h, d1, d2, d3, k):
    L = h - d1 * x - d2 * y + d3 * z
    D = d1 + d2 - h
    return sp.expand(L**2 + 2 * d3 * k * z * (1 - x - y) + k * (2 * D + k) * x * y)


def certificate(h, d1, d2, d3, k):
    L = h - d1 * x - d2 * y + d3 * z
    return sp.expand((L - k * x * y)**2 + 2 * d3 * k * z * (1 - x) * (1 - y)
                     + k * (2 * d1 + k) * x * y * (1 - x) + 2 * k * d2 * x * y * (1 - y)
                     + k**2 * x**2 * y * (1 - y))


def edge_min(q, var, fixed):
    e = sp.Poly(q.subs(fixed), var)
    cand = [sp.Integer(0), sp.Integer(1)]
    if e.degree() == 2:
        a, b, _ = e.all_coeffs()
        t = -b / (2 * a)
        if 0 < t < 1:
            cand.append(t)
    vals = [(e.eval(t), t) for t in cand]
    return min(vals, key=lambda v: v[0])


def zeros_on_edges(q):
    out = []
    vars_ = (x, y, z)
    for i in range(3):
        others = [j for j in range(3) if j != i]
        for fv in product((0, 1), repeat=2):
            fixed = {vars_[others[0]]: fv[0], vars_[others[1]]: fv[1]}
            m, t = edge_min(q, vars_[i], fixed)
            assert m >= 0, (i, fv, m)
            if m == 0:
                pt = [None] * 3
                pt[i] = t
                pt[others[0]], pt[others[1]] = fv
                out.append(tuple(pt))
    return sorted(set(out))


def contact_rows(points_dirs):
    mons = [1, x, y, z, x**2, y**2, z**2, x*y, x*z, y*z]
    rows = []
    for pt, dirs in points_dirs:
        sub = dict(zip((x, y, z), pt))
        rows.append([sp.sympify(m).subs(sub) for m in mons])
        for v in dirs:
            rows.append([sp.diff(m, v).subs(sub) for m in mons])
    return sp.Matrix(rows)


def blocked_origin(zero_pts):
    zs = [sp.Matrix(p) for p in zero_pts]
    for kk in range(4):
        for Fr in combinations(range(3), kk):
            vis = [p for p in zs if all(p[j] != 1 for j in range(3) if j not in Fr)]
            if not vis:
                return False
            if not Fr:
                continue
            P = [sp.Matrix([p[i] for i in Fr]) for p in vis]
            base = P[0]
            D = sp.Matrix.hstack(*[q - base for q in P[1:]]) if len(P) > 1 else sp.zeros(len(Fr), 0)
            t = -base
            if D.shape[1] == 0:
                if t != sp.zeros(len(Fr), 1):
                    return False
                continue
            if D.rank() != sp.Matrix.hstack(D, t).rank():
                return False
    return True


def check(h, d1, d2, k):
    D = d1 + d2 - h
    d3 = D + k
    q = family(h, d1, d2, d3, k)
    assert sp.expand(q - certificate(h, d1, d2, d3, k)) == 0
    Q = sp.Matrix([[q.coeff(x, 2), q.coeff(x, 1).coeff(y, 1) / 2, q.coeff(x, 1).coeff(z, 1) / 2],
                   [0, q.coeff(y, 2), q.coeff(y, 1).coeff(z, 1) / 2],
                   [0, 0, q.coeff(z, 2)]])
    Q[1, 0], Q[2, 0], Q[2, 1] = Q[0, 1], Q[0, 2], Q[1, 2]
    for i, j in combinations(range(3), 2):
        assert Q[i, i] * Q[j, j] - Q[i, j]**2 < 0   # no PSD 2x2 principal block
    zs = zeros_on_edges(q)
    expected = sorted({(h / d1, 0, 0), (0, h / d2, 0), (1, 0, (d1 - h) / d3),
                       (0, 1, (d2 - h) / d3), (1, 1, 1)})
    assert zs == expected, (zs, expected)
    rows = contact_rows([((h / d1, 0, 0), [x]), ((0, h / d2, 0), [y]),
                         ((1, 0, (d1 - h) / d3), [z]), ((0, 1, (d2 - h) / d3), [z]),
                         ((1, 1, 1), [z])])
    # the vertex contact is tangential: the z-edge restriction is d3^2 (z-1)^2
    assert sp.expand(q.subs({x: 1, y: 1}) - d3**2 * (z - 1)**2) == 0
    assert rows.rank() == 9
    # without the tangency equation the contact system has rank 8
    assert rows[:9, :].rank() == 8
    assert blocked_origin(zs)
    return q, zs


if __name__ == '__main__':
    R = sp.Rational
    cases = [(R(1, 2), R(1), R(1), R(1)), (R(1, 3), R(2), R(1), R(1, 2)),
             (R(3, 5), R(1), R(7, 4), R(5, 2)), (R(1, 10), R(1, 3), R(1, 2), R(1, 7))]
    for c in cases:
        q, zs = check(*c)
        print('PASS', 'h,d1,d2,k =', c, ' q =', q, ' zeros:', zs)
    print('PASS: boundary members d3 = D + k have a tangential vertex zero at (1,1,1); the contact '
          'system including the tangency has rank 9 (extreme ray, see note.md); the origin is blocked.')
