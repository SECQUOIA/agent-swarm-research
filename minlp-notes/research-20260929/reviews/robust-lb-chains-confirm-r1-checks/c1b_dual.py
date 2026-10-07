"""Dual bound for the fixed balanced split on the adjacent-pair box H_j of WALL (affine shifts ly, lz):
LB(H_j) >= min_y[phi(-1,y)+ly y] + min_{y,z}[phi(y,z)-ly y+lz z] + min_z[phi(z,-1)-lz z] + constants.
Inner minima: 1-D by dense grid + bounded Brent and endpoints; 2-D middle minimum by its four edges (1-D) and
interior local minima (801^2 grid, polish of the 20 best grid points). Outer: Nelder-Mead. Floating point."""
import numpy as np
from numpy.polynomial import polynomial as P
from scipy.optimize import minimize_scalar, minimize, brentq
UC = np.array([0.0, 1.022, 0.189, 1.774, 1.086]); B = 0.962
u = lambda t: P.polyval(t, UC)
c = brentq(lambda t: P.polyval(t, P.polyder(UC)) - 2 * B, -1, 1, xtol=1e-15)
ph = lambda x, y: 0.5 * (u(x) + u(y)) + B * x * y
def min1(fun, lo=-1.0, hi=c):
    g = np.linspace(lo, hi, 20001); v = fun(g); k = int(v.argmin())
    r = minimize_scalar(fun, bounds=(g[max(k-1,0)], g[min(k+1,len(g)-1)]), method="bounded", options={"xatol": 1e-15})
    return min(float(v.min()), float(r.fun))
G = np.linspace(-1, c, 801); Yg, Zg = np.meshgrid(G, G, indexing="ij"); PH = ph(Yg, Zg)
def min2(ly, lz):
    F = lambda y, z: ph(y, z) - ly * y + lz * z
    vals = [min1(lambda z: F(-1.0, z)), min1(lambda z: F(c, z)), min1(lambda y: F(y, -1.0)), min1(lambda y: F(y, c))]
    V = (PH - ly * Yg + lz * Zg).ravel(); idx = np.argsort(V)[:20]
    vals.append(float(V.min()))
    for k in idx:
        i, j = divmod(int(k), len(G))
        r = minimize(lambda v: F(v[0], v[1]), [G[i], G[j]], bounds=[(-1, c), (-1, c)], method="L-BFGS-B", options={"ftol": 1e-16, "gtol": 1e-13})
        vals.append(float(r.fun))
    return min(vals)
true = ph(-1.0, -1.0) + 2 * ph(-1.0, c)
def LB(v):
    ly, lz = v
    return min1(lambda y: ph(-1.0, y) + ly * y) + min2(ly, lz) + min1(lambda z: ph(z, -1.0) - lz * z)
best = None
for ly in np.linspace(0.20, 0.27, 15):
    for lz in np.linspace(-0.27, -0.20, 15):
        v = LB((ly, lz))
        if best is None or v > best[0]:
            best = (v, ly, lz)
print(f"grid search best: LB - f* = {best[0]-true:+.10f} at ({best[1]:.4f}, {best[2]:.4f})", flush=True)
r = minimize(lambda v: -LB(v), [best[1], best[2]], method="Nelder-Mead", options={"xatol": 1e-9, "fatol": 1e-13, "maxiter": 600})
print(f"Nelder-Mead: LB - f* = {-r.fun - true:+.10f} at ({r.x[0]:.7f}, {r.x[1]:.7f})")
print("family value (closed form, 30 digits): LB <= f* - 0.0113432715072")
