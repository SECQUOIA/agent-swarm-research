"""Closed-form constants of the bang-bang gadget (Sections 3-4 of robust-lower-bound.md)."""
import numpy as np
from gadget_bound import Gadget, core_gap
from robust_bb import gadget_chain

for (y1, eta, eps) in [(0.38, 0.05, 0.02), (0.38, 0.01, 0.005)]:
    bp = 2 * eta + 2 * (1 - eta) * (1 - y1)
    b = 2 * y1
    c = 1 + eta + eps
    z1 = 2 * eta * y1 / bp
    A = 1 + eps - (1 - eta) * (1 - y1) ** 2
    gam = y1 ** 2 * (1 - A) / A
    tstar = y1 / A
    alpha = eps * min(y1 ** 2 / 4, bp ** 2 / 16)
    Lx, Ly, Lz = 2 * y1 ** 2 + 2 * y1, 2 * y1 + 2 * c + bp, 2 * bp
    Lam = 2 * max(Lx, Ly, Lz)
    fam = gadget_chain(1, y1, eta, eps)
    g = Gadget(lambda x: fam.u[0](x), lambda z: fam.u[2](z), fam.b[0], fam.u[1].coefs[0][2], fam.b[1])
    num = core_gap(g, 1, 1, 1)[0]
    print(f"y1={y1} eta={eta} eps={eps}: b={b:.4f} bp={bp:.4f} c={c:.4f} z1={z1:.4f} A={A:.5f} t*={tstar:.4f}")
    print(f"  gamma closed form = {gam:.6f}, numeric symmetric fooling = {num:.6f}")
    print(f"  alpha = {alpha:.3e}, delta_max = 2 alpha = {2*alpha:.3e}")
    print(f"  Lipschitz x,y,z = {Lx:.4f}, {Ly:.4f}, {Lz:.4f}; Lambda = 2 max = {Lam:.4f}")
    print(f"  analytic base per gadget exp(gamma/Lambda) = {np.exp(gam/Lam):.5f}, per variable = {np.exp(gam/Lam/3):.5f}")
    # Hessian at 0 (smooth part): PD check
    H = np.array([[2 * y1 ** 2, b, 0], [b, 2 * c, bp], [0, bp, bp ** 2 / (2 * eta)]])
    print(f"  Hessian eigenvalues at 0: {np.round(np.linalg.eigvalsh(H), 5)}")
