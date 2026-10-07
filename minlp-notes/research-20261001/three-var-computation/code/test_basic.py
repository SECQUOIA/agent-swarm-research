"""Basic consistency checks for relax.py / hullsep.py (targeted, small)."""
import itertools, sys
import numpy as np
import sympy as spy
from fractions import Fraction
sys.path.insert(0, '.')
from relax import Relax, family_AB, stqp_min, triple_moment_matrices, ORIENTS, ABAR5, ABAR6, separate_family
import hullsep

# 1. family identity L_y(q) = h^2 + 2h b'v + v'Bv, symbolic, with moments of a point (x,y,z)
x, y, z, h, d1, d2, d3, k = spy.symbols('x y z h d1 d2 d3 k')
L = h - d1*x - d2*y + d3*z
D = d1 + d2 - h
q = spy.expand(L**2 + 2*d3*k*z*(1-x-y) + k*(2*D+k)*x*y)
b = spy.Matrix([-x, -y, z, -x*y])
B = spy.Matrix([[x*x, x*y, -x*z, x*y], [x*y, y*y, -y*z, x*y], [-x*z, -y*z, z*z, z-x*z-y*z], [x*y, x*y, z-x*z-y*z, x*y]])
v = spy.Matrix([d1, d2, d3, k])
assert spy.expand(h**2 + 2*h*(b.T*v)[0] + (v.T*B*v)[0] - q) == 0
print('PASS family identity (rank-one moments)')

# 2. numeric family_AB agrees with the symbolic B for random cube points and orientations
rng = np.random.default_rng(0)
for trial in range(20):
    p = rng.random(3)
    X = np.outer(p, p)
    T = np.array([[0, 1, 2]])
    for o in ORIENTS:
        bv, Bm = family_AB(p, X, T, o)
        A = Bm[0] - np.outer(bv[0], bv[0])
        # A must be copositive at a genuine point: v'Av >= 0 for v >= 0 (q >= 0)
        val, _ = stqp_min(A[None])
        assert val[0] > -1e-12, (p, o, val)
print('PASS family nonnegative at rank-one cube points (480 cases)')

# 3. counterexample moment point is cut by the family and outside QPB3
mom = {(1,0,0): Fraction(4041,10000), (0,1,0): Fraction(4041,10000), (0,0,1): Fraction(1377,10000),
       (2,0,0): Fraction(3392,10000), (0,2,0): Fraction(3392,10000), (0,0,2): Fraction(681,10000),
       (1,1,0): Fraction(771,10000), (1,0,1): Fraction(1025,10000), (0,1,1): Fraction(1025,10000)}
xv = np.array([float(mom[(1,0,0)]), float(mom[(0,1,0)]), float(mom[(0,0,1)])])
Y = np.array([[float(mom[(2,0,0)]), float(mom[(1,1,0)]), float(mom[(1,0,1)])],
              [float(mom[(1,1,0)]), float(mom[(0,2,0)]), float(mom[(0,1,1)])],
              [float(mom[(1,0,1)]), float(mom[(0,1,1)]), float(mom[(0,0,2)])]])
T = np.array([[0, 1, 2]])
viol = separate_family(xv, Y, T)
print('family violations at counterexample point:', [(ORIENTS[o], round(val, 6)) for _, o, val, _, _ in viol])
M = triple_moment_matrices(xv, Y, T)[0]
dlt, C, st = hullsep.depth(M)
print('QPB3 depth at counterexample point:', dlt, st)
assert dlt < -1e-4
# genuine points: depth ~ 0 (rank one) and > 0 for the uniform center
for trial in range(5):
    p = rng.random(3)
    M = np.block([[np.ones((1, 1)), p[None]], [p[:, None], np.outer(p, p)]])
    dlt, C, st = hullsep.depth(M)
    assert dlt > -1e-7, dlt
print('PASS rank-one points have depth >= -1e-7')
from relax import MC
print('depth at uniform center (should be 1):', hullsep.depth(MC)[0])
# 4. both triangulations reproduce cube vertices
for tets in (ABAR5, ABAR6):
    vs = set()
    for Ab in tets:
        for c in range(4):
            vs.add(tuple(Ab[1:, c]))
    assert len(vs) == 8
print('PASS triangulations')
