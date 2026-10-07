"""Embedding check (note, Corollary 7): a bilinear corner of the sfree note (S = {w <= xy}, apex in
R^3, rays in R^3) is the minor corner with apex (w, x, y, 1) and rays (p_w, p_x, p_y, 0) in the
coordinates (a, b, c, d) of M = [[w, x], [y, h]].  The minor z_K and orbit bound must equal the
sfree z_K and family-(A) bound.  Instances: sfree Theorem 14 (z_A = 0.97539), the second rational
instance (0.83477) and Proposition 16 (0.98385).
"""
import numpy as np
from minor_core import zK, FamilySolver, precondition

INST = {
    'Thm14': ([-4.5, 0, 1.5], [[-1, -6, 18], [-5, 6, -18], [0, 2.5, 2.5]], 0.97539),
    'second': ([-0.5, 0.5, 1], [[0.5, -4, -0.5], [-10, 3, 24], [4.5, 0.5, 7.5]], 0.83477),
    'Prop16': ([-2, 3, 2], [[0, 0, 0], [6, -2, 0.25], [1, -2.5, 0.5]], 0.98385),
}
for name, (sb3, vs, ref) in INST.items():
    sb3 = np.array(sb3, float)
    sb = np.array([sb3[2], sb3[0], sb3[1], 1.0])
    P = np.stack([np.array([v[2] - sb3[2], v[0] - sb3[0], v[1] - sb3[1], 0.0]) for v in vs], 1)
    w = np.ones(3)
    zk = zK(sb, P, w)
    sI, PI = precondition(sb, P)
    c, h, _ = FamilySolver('orbit', sI, PI, w).best(zk, iters=40)
    print('%-7s z_K = %.8f   orbit (minor model) = %.5f   sfree family (A) = %.5f' % (name, zk, c / zk, ref))
