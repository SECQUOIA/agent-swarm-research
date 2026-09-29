"""Targeted exact checks, not verification of the imported representation theorems."""
from fractions import Fraction as F
import sympy as s

A = [
    [F(1,272), F(1,272), F(14,272), F(1,17), F(1,17), F(14,17), F(0), F(0)],
    [F(16,17), F(16,17), F(0), F(18,17), F(18,17), F(140), F(56), F(56)],
    [F(16,17), F(0), F(0), F(1,17), F(9), F(126), F(36), F(84)],
]
w = [252, 3, -2]
dual = [sum(w[i] * A[i][j] for i in range(3)) for j in range(8)]
assert dual == [F(127,68), F(15,4), F(441,34), F(304,17), F(0), F(6384,17), F(96), F(0)]
assert all(value >= 0 for value in dual)
q_values = [F(1,4), F(64), F(128)]
r_values = [F(1), F(256), F(256)]
assert sum(a*b for a,b in zip(w, q_values)) == -1
assert sum(a*b for a,b in zip(w, r_values)) == 508
assert sum(w[i]*(q_values[i]+r_values[i]/1016) for i in range(3)) == F(-1,2)
u,z,t = s.symbols('u z t')
assert s.det(s.Matrix([[z,u],[u,1]])) == z-u**2
assert s.det(s.Matrix([[t,z],[z,1]])) == t-z**2
for n in (1,2,5):
    X=s.Matrix(s.symbols(f'x0:{n}'))
    r2=(X.T*X)[0]
    assert s.hessian(r2**2,X) == 4*r2*s.eye(n)+8*X*X.T
print('PASS: exact dual row, perturbation margin, quartic power lift, radial Hessian')
