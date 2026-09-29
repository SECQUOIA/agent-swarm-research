"""Counterexample family to the global-Voronoi conjecture C1.

Q = M w w^T + eps I on Z^3 with w = (1, -alpha, -beta).  The equality
constraint x3 = 0 (two inequalities, Delta(A) = 1) restricts the problem to
the coordinate sublattice Z^2 x {0}, where the relevant invariant is
rho_inf(Q_SS) for the 2x2 principal block.  Simultaneous Diophantine
approximation makes rho_inf(Q) on Z^3 grow like (M/eps)^(1/6) while
rho_inf(Q_SS) grows like (M/eps)^(1/4).  Since the constrained problem with
x3 = 0 is exactly the unconstrained 2-D problem with Hessian Q_SS, its
proximity (sup over c) equals rho_inf(Q_SS) (existence version), so the ratio
prox / (Delta * rho_inf(Q)) is unbounded.
"""
import math
import numpy as np
from voronoi import rho_inf

import sys
if len(sys.argv) > 1 and sys.argv[1] == "sqrt":
    alpha, beta = 2 ** 0.5, 3 ** 0.5  # alpha badly approximable (quadratic irrational)
else:
    alpha, beta = 2 ** (1 / 3), 4 ** (1 / 3)  # basis of a cubic field
print(" M/eps    rho(Q,Z^3)  rho(Q_SS,Z^2)  ratio   #relevant(3D)")
for e in range(2, 11):
    R = 10.0 ** e
    w = np.array([1.0, -alpha, -beta])
    Q = R * np.outer(w, w) + np.eye(3)
    r3, nv3, mu3 = rho_inf(Q)
    r2, nv2, mu2 = rho_inf(Q[:2, :2])
    print(f" 1e{e:<3d}  {r3:10.3f}  {r2:12.3f}  {r2 / r3:6.2f}   {nv3}")
