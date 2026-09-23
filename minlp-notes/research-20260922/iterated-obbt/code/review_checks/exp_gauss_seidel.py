"""Jacobi rounds (theory.md's T_U) vs sequential (Gauss-Seidel) OBBT rounds
that rebuild the McCormick relaxation after each variable, for x^2+y^2+a x y."""
import numpy as np
from obbt2d import Quad, affine_pieces, inner_min
e = (Quad(1.), Quad(1.))
def tighten(a, lo, hi, i, U):
    P = affine_pieces(a, lo, hi); F = lambda t: inner_min(e, P, i, t, lo, hi) - U
    out = []
    for end in (hi[i], lo[i]):
        if F(end) <= 0: out.append(end); continue
        g, b = 0.0, end
        for _ in range(200):
            m = 0.5*(g+b)
            if m in (g, b): break
            g, b = (m, b) if F(m) <= 0 else (g, m)
        out.append(g)
    lo, hi = lo.copy(), hi.copy(); hi[i], lo[i] = out; return lo, hi
for a in [1.0, 1.9]:
    rho = (np.sqrt(2*a*a+4*a)-a)/2
    for mode in ["jacobi", "gauss-seidel"]:
        lo, hi = np.array([-1., -1.2]), np.array([1.3, 1.])
        logs = []
        for k in range(300):
            s = (hi-lo).max()
            if mode == "jacobi":
                l0, h0 = tighten(a, lo, hi, 0, 0.0); l1, h1 = tighten(a, lo, hi, 1, 0.0)
                nlo, nhi = np.array([l0[0], l1[1]]), np.array([h0[0], h1[1]])
            else:
                nlo, nhi = tighten(a, lo, hi, 0, 0.0); nlo, nhi = tighten(a, nlo, nhi, 1, 0.0)
            ns = (nhi-nlo).max(); logs.append(ns/s); lo, hi = nlo/ns, nhi/ns
        print(f"a={a} {mode:12s} ratio per round (k=300) {logs[-1]:.6f}   rho(a)={rho:.6f}  rho^2={rho**2:.6f}")
