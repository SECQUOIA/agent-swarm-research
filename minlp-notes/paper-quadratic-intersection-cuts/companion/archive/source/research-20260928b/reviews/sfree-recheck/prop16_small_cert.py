"""Search for a small-integer PD certificate Y_v (v = sbar, v1, v2, v3) with sum_v M(v) Y_v = 0 for
Proposition 16, via an integral kernel basis and rounding of scaled SDP centres; verified exactly."""
import numpy as np, sympy as sp, cvxpy as cp
R = sp.Rational
verts = [sp.Matrix([-2, 3, 2]), sp.Matrix([0, 0, 0]), sp.Matrix([6, -2, R(1, 4)]), sp.Matrix([1, R(-5, 2), R(1, 2)])]
M = lambda s: sp.Matrix([[s[2], s[0]], [s[1], 1]])
Ms = [M(v) for v in verts]
ys = sp.symbols('y0:12')
Ysym = [sp.Matrix([[ys[3*i], ys[3*i+1]], [ys[3*i+1], ys[3*i+2]]]) for i in range(4)]
A, _ = sp.linear_eq_to_matrix(list(sum((Ms[i]*Ysym[i] for i in range(4)), sp.zeros(2, 2))), ys)
K = [k * sp.ilcm(*[sp.fraction(x)[1] for x in k]) for k in A.nullspace()]   # integral basis
Kn = np.array([[float(x) for x in k] for k in K]).T
c = cp.Variable(len(K)); t = cp.Variable(); y = Kn @ c
cons = [cp.bmat([[y[3*i], y[3*i+1]], [y[3*i+1], y[3*i+2]]]) - t*np.eye(2) >> 0 for i in range(4)]
cons.append(cp.norm(y, 'inf') <= 1)
cp.Problem(cp.Maximize(t), cons).solve(solver='CLARABEL')
best = None
for s in range(1, 3000):
    cr = [int(round(x)) for x in s * c.value]
    yex = sum((cr[k] * K[k] for k in range(len(K))), sp.zeros(12, 1))
    Y = [sp.Matrix([[yex[3*i], yex[3*i+1]], [yex[3*i+1], yex[3*i+2]]]) for i in range(4)]
    if all(Yi[0, 0] > 0 and Yi.det() > 0 for Yi in Y):
        g = sp.igcd(*[int(x) for x in yex]); Y = [Yi / g for Yi in Y]
        mx = max(abs(x) for Yi in Y for x in Yi)
        if best is None or mx < best[0]:
            best = (mx, Y)
        if mx < 200:
            break
mx, Y = best
S = sum((Ms[i]*Y[i] for i in range(4)), sp.zeros(2, 2))
for nm, Yi in zip(('sbar', 'v1', 'v2', 'v3'), Y):
    print('Y_%-4s = %s   Y11 = %s > 0, det = %s > 0' % (nm, Yi.tolist(), Yi[0, 0], Yi.det()))
print('sum_v M(v) Y_v =', S.tolist(), ' -> zero:', S == sp.zeros(2, 2))
print('all PD:', all(Yi[0, 0] > 0 and Yi.det() > 0 for Yi in Y), ' max |entry| =', mx)
