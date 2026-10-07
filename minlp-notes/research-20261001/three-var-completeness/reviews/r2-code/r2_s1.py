"""Review round 2: independent exact check of Proposition 2.10 on S1
(0 < h < min(d1, d2), k > 0, d3 = D + k), without the stream's code.

Contacts: a = (h/d1,0,0) [x], b = (0,h/d2,0) [y], c = (1,0,(d1-h)/d3) [z],
d = (0,1,(d2-h)/d3) [z], vertex (1,1,1) [z tangency]; 10 rows.
Checks: q in kernel; 9 x 9 minors (drop one row, one column), factored,
until the zero sets of the minors found do not meet the open region; also
exact rank at random rational points, including points with d1 = 2h.
"""
import random

import sympy as sp

h, d1, d2, k = sp.symbols('h d1 d2 k', positive=True)
x, y, z = sp.symbols('x y z')
MONS = [sp.Integer(1), x, y, z, x**2, y**2, z**2, x*y, x*z, y*z]
VARS = (x, y, z)
D = d1 + d2 - h
d3 = D + k


def coeffs(p):
    P = sp.Poly(sp.expand(p), x, y, z)
    return sp.Matrix([P.coeff_monomial(m) for m in MONS])


L = h - d1*x - d2*y + d3*z
q = L**2 + 2*d3*k*z*(1 - x - y) + k*(2*D + k)*x*y
contacts = [((h/d1, 0, 0), [0]), ((0, h/d2, 0), [1]), ((1, 0, (d1 - h)/d3), [2]),
            ((0, 1, (d2 - h)/d3), [2]), ((1, 1, 1), [2])]
# Rows are scaled by the square (value rows) or first power (derivative
# rows) of the denominator of the contact point, so that all entries are
# polynomials. Scaling rows by nonzero factors does not change the rank.
scales = [d1, d2, d3, d3, sp.Integer(1)]
rows = []
for (pt, dirs), sc in zip(contacts, scales):
    s = dict(zip(VARS, pt))
    rows.append([sp.expand(sp.cancel(sc**2 * m.subs(s))) for m in MONS])
    for j in dirs:
        rows.append([sp.expand(sp.cancel(sc * sp.diff(m, VARS[j]).subs(s))) for m in MONS])
M = sp.Matrix(rows)
assert all(e.is_polynomial(h, d1, d2, k) for e in M)
print('rows', M.shape, '| q in kernel:',
      all(sp.simplify(e) == 0 for e in M * coeffs(q)), flush=True)

found = []
for r in range(10):
    for c in range(10):
        sub = M.copy()
        sub.row_del(r)
        sub.col_del(c)
        det = sp.factor(sub.det(method='berkowitz'))
        if det != 0:
            found.append((r, c, det))
            print('   minor drop row %d col %d: %s' % (r, c, det), flush=True)
        if len(found) >= 3:
            break
    if len(found) >= 3:
        break

rng = random.Random(11)
ranks = {}
for trial in range(40):
    kk = sp.Rational(rng.randint(1, 30), rng.randint(1, 30))
    hh = sp.Rational(rng.randint(1, 30), rng.randint(1, 30))
    a1 = hh + sp.Rational(rng.randint(1, 30), rng.randint(1, 30))
    a2 = hh + sp.Rational(rng.randint(1, 30), rng.randint(1, 30))
    if trial % 2:
        a1 = 2 * hh  # the special line d1 = 2h
    r = M.subs({h: hh, d1: a1, d2: a2, k: kk}).rank()
    ranks.setdefault('d1=2h' if trial % 2 else 'generic', set()).add(r)
print('exact rank at rational points:', {kk: sorted(v) for kk, v in ranks.items()})
