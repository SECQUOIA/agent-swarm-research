import numpy as np
from cg4 import *
rng = np.random.default_rng(5); worst = 0
for trial in range(300):
    C = rng.normal(size=(3, 3)) * (np.add.outer(np.arange(3), np.arange(3)) <= 2)
    A = PP.poly(rng.normal(size=5)); B = PP.poly(rng.normal(size=5))
    lx, ly = rng.uniform(-1, 0.5, 2); ux, uy = min(1, lx + rng.uniform(0.02, 1.5)), min(1, ly + rng.uniform(0.02, 1.5))
    v, xa, ya = min_factor(C, A, B, lx, ux, ly, uy)
    gx = np.linspace(lx, ux, 1201); gy = np.linspace(ly, uy, 1201); X, Y = np.meshgrid(gx, gy, indexing="ij")
    Z = sum(C[i, j] * X**i * Y**j for i in range(3) for j in range(3)) + A(X) + B(Y)
    worst = max(worst, v - Z.min())
print("cg4 quartic self-test: max(claimed - grid) =", worst)
# consistency with cg on the chiral chain root gap n = 7
cb = ClassBound(chiral_chain(7, 0.6, 0.3, 0.05), poly_tests(2), K=7)
print("chiral n=7 P2 gap via cg4:", -cb.bound(np.full(7, -1.0), np.full(7, 1.0), None, maxit=300, tol=1e-10)[1])
