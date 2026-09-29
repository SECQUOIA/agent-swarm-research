"""Exact local identities for the least-SOS-field quintic tower.

The universal real-field lemma and the inherited polynomial-bit quartic
construction are proved in the note, not certified by these finite checks.
"""

import sympy as s

x, y, z, b = s.symbols("x y z b")
q = [x*x-y, x*y-z, y*y-x*z, y*z-b, z*z-b*x]
leading = [x*x, x*y, y*y-x*z, y*z, z*z]
products = [s.Poly(leading[i]*leading[j], x, y, z)
            for i in range(5) for j in range(i, 5)]
monomials = sorted({e for p in products for e in p.monoms()})
matrix = s.Matrix([[p.coeff_monomial(e) for p in products]
                   for e in monomials])
assert matrix.shape == (15, 15) and matrix.det() == -1
print("PASS: homogeneous residual-product coefficient determinant is -1")

a = s.symbols("a")
substitution = {x: a, y: a*a, z: a**3, b: a**5}
assert all(s.expand(r.subs(substitution)) == 0 for r in q)
g = s.Matrix(s.symbols("g0:5"))
w = s.Matrix([0, 0, g[4], 0, -g[2]])
lam, c = s.symbols("lambda c", positive=True)
S0 = g*g.T+s.diag(c, c, 0, c, 0)
perturbation = s.diag(0, 0, 1, 0, 0)
assert s.expand((w.T*S0*w)[0]) == 0
assert s.expand((w.T*(lam*S0-perturbation)*w)[0]) == -g[4]**2
assert s.Poly(sum(g[i]*q[i] for i in range(5)), x,y,z).coeff_monomial(z*z) == g[4]
print("PASS: exact null direction excludes every PSD slice Gram when the z² coefficient is nonzero")

R = y*y-x*z
T = s.hessian(R, (x,y,z))/2
assert sorted(T.eigenvals()) == [s.Rational(-1, 2), s.Rational(1, 2), s.Integer(1)]
assert s.trace(T.T*T) == s.Rational(3, 2)
vec = s.Matrix([T[i,j] for i in range(3) for j in range(3)])
B = 8*vec*vec.T+4*s.kronecker_product(T,T)
u = s.Matrix([x,y,z])
v = s.Matrix(s.symbols("v0:3"))
uv = s.kronecker_product(u,v)
assert s.expand((uv.T*B*uv)[0]-(v.T*s.hessian(R*R,(x,y,z))*v)[0]) == 0
for sign in [-1, 1]:
    _, D = (16*s.eye(9)+sign*B).LDLdecomposition(hermitian=False)
    assert all(D[i,i] > 0 for i in range(9))
print("PASS: perturbation Hessian Gram identity and exact norm margin below 16")
