"""SCIP's minor set depends on the scaling of the problem variables (note, Proposition 11).

Corner (w = 1): sbar = diag(1, delta) = (1, 0, 0, delta), rays
  p1 = +e_b = (0, 1, 0, 0), p2 = -e_a, p3 = -delta e_d, p4 = -delta e_c.
This is the corner sbar' = I, rays (e_b, -e_a, -e_d, -e_c) after substituting x_{i2} = delta x'_{i2}
(the second row of the minor is multiplied by delta).  Claims (proved in the note):
  z_K = 1;  SCIP's set C_I gives 2 sqrt(delta) (delta <= 1/4);  C_F with F^T = diag(1, 1/delta)
  (point-rule family) gives 1;  in the primed coordinates SCIP's set gives 1.
Prints the exact values next to the numerical family bounds.
"""
import numpy as np
from fractions import Fraction as Fr
from minor_core import zK, family_bounds, bound_of, polar_rotation, mat

print('%-8s %-10s %-12s %-12s %-10s %-10s %-10s %-10s' % ('delta', 'z_K', 'scip', '2sqrt(d)', 'bcm', 'pr', 'orbit', 'C_diag'))
for k in range(1, 7):
    dl = 10.0 ** (-k)
    sb = np.array([1.0, 0.0, 0.0, dl])
    P = np.array([[0, 1, 0, 0], [-1, 0, 0, 0], [0, 0, 0, -dl], [0, 0, -dl, 0]], float).T
    w = np.ones(4)
    zk = zK(sb, P, w)
    fb = family_bounds(sb, P, w, zk, iters=40)
    cd = bound_of(np.diag([1.0, 1.0 / dl]), sb, P, w)
    print('%-8.0e %-10.6f %-12.6e %-12.6e %-10.6f %-10.6f %-10.6f %-10.6f' % (
        dl, zk, fb['scip']['ratio'] * zk, 2 * np.sqrt(dl), fb['bcm']['ratio'], fb['pr']['ratio'], fb['orbit']['ratio'], cd))
# primed coordinates
sb = np.array([1.0, 0, 0, 1.0])
P = np.array([[0, 1, 0, 0], [-1, 0, 0, 0], [0, 0, 0, -1], [0, 0, -1, 0]], float).T
print('primed corner (sbar = I): z_K = %.6f, SCIP set bound = %.6f' % (zK(sb, P, np.ones(4)),
      bound_of(polar_rotation(mat(sb)).T, sb, P, np.ones(4))))
