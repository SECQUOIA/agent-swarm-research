"""Symbolic extremality check for the boundary strata of the family found by
the stratum enumeration (note.md, Proposition 2.10).  Exact (sympy).

Family: q = L^2 + 2 d3 k z (1-x-y) + k (2D+k) x y, L = h - d1 x - d2 y + d3 z,
D = d1 + d2 - h.  Contacts in the five-contact regime:
  a = (h/d1,0,0) [x-edge], b = (0,h/d2,0) [y-edge], c = (1,0,(d1-h)/d3),
  d = (0,1,(d2-h)/d3), e = (1,1,(D+k)/d3) [z-edges].
Boundary strata checked here (d1,d2 >= 0, d3,k > 0; S1 also has
0 < h < min(d1,d2)):
  S1: d3 = D + k            e -> vertex (1,1,1), tangent along z
  S2: h = 0, d3 > D + k     a, b -> vertex (0,0,0), tangent along x and y
  S3: h = d1 < d2, d3 > D+k a, c -> vertex (1,0,0), tangent along x and z
  S4: h = 0, d3 = D + k     S2 and S1 together
  S5: h = d1 < d2, d3 = D+k S3 and S1 together
For each stratum we build the linear contact conditions (values, edge
derivatives at interior edge contacts, derivatives along tangent edges at
vertex contacts), check that q is in the kernel, and find 9 x 9 minors whose
factored numerators have no common zero on the stratum.  Rank 9 plus the
sign argument of the note gives an extreme ray of P3.
"""
import sympy as sp

h = sp.symbols('h', real=True)
d1, d2 = sp.symbols('d1 d2', nonnegative=True)
d3, k = sp.symbols('d3 k', positive=True)
x, y, z = sp.symbols('x y z')
KEYS = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1), (2, 0, 0), (0, 2, 0), (0, 0, 2), (1, 1, 0), (1, 0, 1), (0, 1, 1)]


def value_row(p):
    a, b, c = p
    return [1, a, b, c, a**2, b**2, c**2, a*b, a*c, b*c]


def deriv_row(p, i):
    xx = list(p)
    g = [0] * 10
    g[1 + i] = 1
    g[4 + i] = 2 * xx[i]
    pairs = {(0, 1): 7, (0, 2): 8, (1, 2): 9}
    for (a, b), idx in pairs.items():
        if a == i:
            g[idx] = xx[b]
        if b == i:
            g[idx] = xx[a]
    return g


def family_vec(hh, dd1, dd2, dd3, kk):
    D = dd1 + dd2 - hh
    L = hh - dd1 * x - dd2 * y + dd3 * z
    q = sp.expand(L**2 + 2 * dd3 * kk * z * (1 - x - y) + kk * (2 * D + kk) * x * y)
    P = sp.Poly(q, x, y, z)
    return sp.Matrix([P.coeff_monomial(x**a * y**b * z**c) for a, b, c in KEYS])


def contact_matrix(contacts):
    rows = []
    for p, dirs in contacts:
        rows.append(value_row(p))
        for i in dirs:
            rows.append(deriv_row(p, i))
    return sp.Matrix(rows)


def minors_until_cover(M, region_note, max_minors=6):
    """Collect nonzero 9x9 minors; print their factored forms."""
    out = []
    nr, nc = M.shape
    from itertools import combinations
    for rows_keep in combinations(range(nr), 9):
        for drop_col in range(nc):
            sub = M.extract(list(rows_keep), [c for c in range(nc) if c != drop_col])
            det = sp.factor(sp.together(sub.det(method='berkowitz')))
            if det != 0:
                out.append((rows_keep, drop_col, det))
                print('   minor rows', rows_keep, 'drop col', drop_col, ':', det, flush=True)
                if len(out) >= max_minors:
                    return out
    return out


def stratum(name, subs, contacts, note, expected_minor=None):
    print(name, note, flush=True)
    hh, dd1, dd2, dd3, kk = [sp.sympify(v).subs(subs) for v in (h, d1, d2, d3, k)]
    cs = [(tuple(sp.sympify(c).subs(subs) for c in p), dirs) for p, dirs in contacts]
    M = contact_matrix(cs)
    qv = family_vec(hh, dd1, dd2, dd3, kk)
    assert all(sp.simplify(e) == 0 for e in M * qv), name + ': q not in kernel'
    print('   q in kernel of the %d x 10 contact matrix' % M.shape[0], flush=True)
    if expected_minor is not None:
        # These systems have nine rows. Dropping the z-linear coefficient
        # gives a minor that stays nonzero on the whole stated sub-locus.
        det = sp.factor(M[:, [j for j in range(10) if j != 3]].det())
        assert sp.simplify(det - expected_minor) == 0, (name, det)
        assert expected_minor != 0 and qv[6] != 0
        print('   PASS: rank 9; minor dropping column 3 =', det, flush=True)
        return det
    return minors_until_cover(M, note, max_minors=3)


Dg = d1 + d2 - h
a = ((h / d1, 0, 0), [0])
b = ((0, h / d2, 0), [1])
c = ((1, 0, (d1 - h) / d3), [2])
d = ((0, 1, (d2 - h) / d3), [2])
e = ((1, 1, (Dg + k) / d3), [2])
v111 = ((1, 1, 1), [2])          # vertex (1,1,1), tangent along z

# S1 (d3 = D + k) is checked by check_boundary_rank_symbolic.py
stratum('S2', {h: 0}, [((0, 0, 0), [0, 1]), c, d, e], 'h = 0')
stratum('S3', {h: d1}, [((1, 0, 0), [0, 2]), b, d, e], 'h = d1')
stratum('S4', {h: 0, d3: d1 + d2 + k}, [((0, 0, 0), [0, 1]), c, d, v111], 'h = 0, d3 = D + k')
stratum('S5', {h: d1, d3: d2 + k}, [((1, 0, 0), [0, 2]), b, d, v111], 'h = d1, d3 = D + k')

# At h = d1 = 0, b reaches the origin with a y tangency. No division
# by d1 is used; d2 > 0 follows from the S3/S5 range d1 < d2.
for name, height, last in (('S3', d3, e), ('S5', d2 + k, v111)):
    stratum(name, {h: 0, d1: 0, d3: height},
            [((1, 0, 0), [0, 2]), b, d, last],
            'h = d1 = 0, d2 > 0', expected_minor=-2 * k / height)

# On S2/S4, c or d reaches a vertex with a z tangency. Check each
# zero-parameter boundary, including d1 = d2 = 0, exactly.
for name, last in (('S2', e), ('S4', v111)):
    for zeros in ({d1: 0}, {d2: 0}, {d1: 0, d2: 0}):
        height = d3 if name == 'S2' else (d1 + d2 + k).subs(zeros)
        stratum(name, {h: 0, d3: height, **zeros},
                [((0, 0, 0), [0, 1]), c, d, last],
                str(zeros), expected_minor=2 * k / height)
print('PASS: S2-S5 generic minors and all zero-parameter boundary checks')
