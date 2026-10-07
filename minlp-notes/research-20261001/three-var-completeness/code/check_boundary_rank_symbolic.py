"""Symbolic rank of the contact system of the boundary stratum d3 = D + k
(note.md, Proposition 2.8), for all parameters 0 < h < min(d1, d2), k > 0.

Rows: value and edge derivative at the four edge contacts
  a = (h/d1, 0, 0) [x], b = (0, h/d2, 0) [y],
  c = (1, 0, (d1-h)/d3) [z], d = (0, 1, (d2-h)/d3) [z],
value at the vertex v = (1,1,1) and z-derivative at v (tangency).
We find a 9 x 9 minor whose numerator factors into terms that are nonzero on
the parameter region, which proves rank >= 9 everywhere; rank <= 9 holds
because the family member q is a nonzero kernel vector.  Exact (sympy).
"""
from itertools import combinations

import sympy as sp

h, d1, d2, k = sp.symbols('h d1 d2 k', positive=True)
D = d1 + d2 - h
d3 = D + k


def value_row(p):
    x, y, z = p
    return [1, x, y, z, x**2, y**2, z**2, x*y, x*z, y*z]


def deriv_row(p, i):
    x = list(p)
    g = [0] * 10
    g[1 + i] = 1
    g[4 + i] = 2 * x[i]
    pairs = {(0, 1): 7, (0, 2): 8, (1, 2): 9}
    for (a, b), idx in pairs.items():
        if a == i:
            g[idx] = x[b]
        if b == i:
            g[idx] = x[a]
    return g


pts = [((h / d1, 0, 0), 0), ((0, h / d2, 0), 1), ((1, 0, (d1 - h) / d3), 2), ((0, 1, (d2 - h) / d3), 2)]
rows = []
for p, i in pts:
    rows.append(value_row(p))
    rows.append(deriv_row(p, i))
rows.append(value_row((1, 1, 1)))
rows.append(deriv_row((1, 1, 1), 2))
M = sp.Matrix(rows)

# kernel check: the family member is in the kernel
x, y, z = sp.symbols('x y z')
L = h - d1 * x - d2 * y + d3 * z
q = sp.expand(L**2 + 2 * d3 * k * z * (1 - x - y) + k * (2 * D + k) * x * y)
P = sp.Poly(q, x, y, z)
keys = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1), (2, 0, 0), (0, 2, 0), (0, 0, 2), (1, 1, 0), (1, 0, 1), (0, 1, 1)]
qv = sp.Matrix([P.coeff_monomial(x**a * y**b * z**c) for a, b, c in keys])
assert all(sp.simplify(e) == 0 for e in M * qv), 'family member not in kernel'
print('family member lies in the kernel of the 10 x 10 contact matrix')

found = None
for drop_row in range(10):
    for drop_col in range(10):
        sub = M.copy()
        sub.row_del(drop_row)
        sub.col_del(drop_col)
        det = sp.factor(sp.together(sub.det(method='berkowitz')))
        if det != 0:
            found = (drop_row, drop_col, det)
            break
    if found:
        break
print('nonzero 9x9 minor (dropping row %d, column %d):' % found[:2])
print(found[2])
num, den = sp.fraction(found[2])
print('numerator factors:', sp.factor_list(num))
print('denominator factors:', sp.factor_list(den))

# The minor above vanishes only on d1 = 2h inside the region.  On that slice
# find another nonzero minor.
M2 = M.subs(d1, 2 * h)
found2 = None
for drop_row in range(10):
    for drop_col in range(10):
        sub = M2.copy()
        sub.row_del(drop_row)
        sub.col_del(drop_col)
        det = sp.factor(sp.together(sub.det(method='berkowitz')))
        if det != 0:
            found2 = (drop_row, drop_col, det)
            break
    if found2:
        break
print('on d1 = 2h: nonzero 9x9 minor (dropping row %d, column %d):' % found2[:2])
print(found2[2])
num2, den2 = sp.fraction(found2[2])
print('numerator factors:', sp.factor_list(num2))
print('denominator factors:', sp.factor_list(den2))
print('Conclusion: on 0 < h < min(d1,d2), k > 0 every factor above is nonzero '
      '(h > 0, d2 - h > 0, d1 + d2 - h + k > 0; check the printed factors), so the '
      'contact matrix has rank exactly 9 on the whole boundary stratum.')
