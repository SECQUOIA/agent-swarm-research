"""Corner-box cap on mu in Theorem 4.2 for several parameter sets.  On a box [-1,a]x[-1,b]x[-1,c] with
a, b, c <= 0 every term of both factors is nondecreasing in |x|, |y|, |z|, so V_S = g(a,b,c) for every
class S.  mu0 = smallest mu at which some such box has (vol/8) exp(mu V) >= 1; then Theorem 4.2 cannot
give more than exp(mu0 gamma) per gadget (gamma = class-(a) root gap)."""
import numpy as np
from scipy.optimize import brentq
def cap(y1, eta, epsv):
    b, bp, c = 2*y1, 2*eta + 2*(1-eta)*(1-y1), 1 + eta + epsv
    z1, k = 2*eta*y1/bp, 2*(1-eta)*y1
    A = 1 + epsv - (1-eta)*(1-y1)**2; gam = y1**2*(1-A)/A
    t = np.linspace(-1, 0, 401)[1:-1]
    X, Y, Z = np.meshgrid(t, t, t, indexing="ij")
    uz = np.where(np.abs(Z) <= z1, bp**2*Z**2/(4*eta), (bp*np.abs(Z)+k)**2/4 - (1-eta)*y1**2)
    V = y1**2*X**2 + b*X*Y + c*Y**2 + uz + bp*Y*Z
    lv = np.log((X+1)/2) + np.log((Y+1)/2) + np.log((Z+1)/2)
    F = lambda mu: np.max(lv + mu*V)          # log of max_box (vol/8) exp(mu V)
    mu0 = brentq(F, 0.5, 20)
    i = np.unravel_index(np.argmax(lv + mu0*V), V.shape)
    return gam, mu0, np.exp(mu0*gam), np.exp(mu0*gam/3), (X[i], Y[i], Z[i])
for p in [(0.38, 0.05, 0.02), (0.38, 0.01, 0.005), (0.38, 0.05, 0.1), (0.30, 0.01, 0.005), (0.45, 0.01, 0.005), (0.30, 0.005, 0.002)]:
    gam, mu0, bg, bv, box = cap(*p)
    print("params %s: gamma_a = %.5f, corner-box mu0 = %.4f (box upper corner %s), cap exp(mu0 gamma) = %.4f per gadget, %.4f per variable"
          % (p, gam, mu0, np.round(box, 3), bg, bv))
