"""Symbolic rank of the S3 / S5 contact systems on the sub-locus d1 = h = 0
(allowed by the note's range 'h = d1 < d2' since d >= 0), where the minor
quoted in the note, d1^2 (d1 - d2)^2 / (...), vanishes.  Independent code."""
import sympy as sp
x, y, z = sp.symbols('x y z')
d2, d3, k = sp.symbols('d2 d3 k', positive=True)
c = sp.symbols('c0:10')
gen = (c[0] + c[1]*x + c[2]*y + c[3]*z + c[4]*x**2 + c[5]*y**2 + c[6]*z**2 + c[7]*x*y + c[8]*x*z + c[9]*y*z)
def rows(cts):
    R = []
    for pt, dirs in cts:
        s = dict(zip((x, y, z), pt))
        R.append([sp.diff(gen, t).subs(s) for t in c])
        for i in dirs:
            R.append([sp.diff(sp.diff(gen, (x, y, z)[i]), t).subs(s) for t in c])
    return sp.Matrix(R)
for name, D3 in (('S3', d3), ('S5', d2 + k)):
    # h = d1 = 0: D = d2; contacts v100 (x, z tangents), b -> (0,0,0) with y-derivative, d, e or v111
    cts = [((1, 0, 0), [0, 2]), ((0, 0, 0), [1]), ((0, 1, d2 / D3), [2])]
    cts.append(((1, 1, (d2 + k) / D3), [2]) if name == 'S3' else ((1, 1, 1), [2]))
    M = rows(cts)
    L = -d2*y + D3*z
    q = sp.Poly(sp.expand(L**2 + 2*D3*k*z*(1 - x - y) + k*(2*d2 + k)*x*y), x, y, z)
    mons = [1, x, y, z, x**2, y**2, z**2, x*y, x*z, y*z]
    qv = sp.Matrix([q.coeff_monomial(m) for m in mons])
    ker = all(sp.simplify(t) == 0 for t in M*qv)
    minors = []
    for col in range(10):
        det = sp.factor(M[:, [j for j in range(10) if j != col]].det())
        if det != 0:
            minors.append((col, det))
    print(name, 'd1 = h = 0: kernel ok', ker, '| rank', M.rank(simplify=True), '| nonzero 9x9 minors:', minors[:3])
