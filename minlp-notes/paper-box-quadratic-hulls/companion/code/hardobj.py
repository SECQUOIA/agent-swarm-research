"""Hard three-variable objectives: the deepest QPB3-separating quadratic at a
random point of PSD+RLT+TRI.

Sampling: x ~ U[0,1]^3, Y = xx' + G G' with G ~ N(0, s^2) of shape (3, r), r in {1,2,3},
s ~ U[0.05, 0.5]; reject unless all McCormick (incl. Y_ii <= x_i) and triangle
inequalities hold; compute (delta, C) = hullsep.depth(M); reject unless delta < -1e-4.
The objective is q_C(x) = [1 x'] C [1 x']' (min form: H = C[1:,1:], g = 2 C[0,1:],
constant C[0,0]).  If plus_only, also reject unless diag(H) > 1e-3 max|C|.
"""
import numpy as np
import hullsep

def rlt_tri_ok(x, Y, tol=1e-9):
    for i in range(3):
        if Y[i, i] > x[i] + tol: return False
        for j in range(i + 1, 3):
            if Y[i, j] < -tol or Y[i, j] < x[i] + x[j] - 1 - tol or Y[i, j] > min(x[i], x[j]) + tol: return False
    i, j, k = 0, 1, 2
    if Y[i, j] + Y[i, k] - x[i] - Y[j, k] > tol: return False
    if Y[i, j] + Y[j, k] - x[j] - Y[i, k] > tol: return False
    if Y[i, k] + Y[j, k] - x[k] - Y[i, j] > tol: return False
    if x[i] + x[j] + x[k] - Y[i, j] - Y[i, k] - Y[j, k] - 1 > tol: return False
    return True

def sample_hard(rng, plus_only=False, maxtry=100000):
    for t in range(maxtry):
        x = rng.random(3)
        r = rng.integers(1, 4)
        s = rng.uniform(0.05, 0.5)
        G = rng.normal(size=(3, r)) * s
        Y = np.outer(x, x) + G @ G.T
        if not rlt_tri_ok(x, Y):
            continue
        M = np.block([[np.ones((1, 1)), x[None]], [x[:, None], Y]])
        d, C, st = hullsep.depth(M)
        if d >= -1e-4:
            continue
        H = C[1:, 1:].copy(); g = 2 * C[0, 1:].copy(); c0 = C[0, 0]
        if plus_only and not (np.diag(H) > 1e-3 * np.abs(C).max()).all():
            continue
        return H, g, c0, {'x': x.tolist(), 'Y': Y.tolist(), 'depth': d, 'tries': t + 1}
    raise RuntimeError('no sample')
