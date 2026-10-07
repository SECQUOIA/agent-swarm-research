"""Per-bond (translation-invariant) LP: min int W dnu over nu on a grid of [-1,1]^2 with the two marginals agreeing
on P_d (moments 1..d).  Reviewer's code; grid of N points; continuum check of the dual: the dual polynomial rho
(from LP duals) gives  min_{[-1,1]^2} W + rho(x) - rho(y)  (a valid lower bound if the min is exact; computed by cg.min_factor)."""
import numpy as np
from scipy.optimize import linprog
from cg import PP, min_factor

def run(b, g, ev, m, dmax, N=241):
    a = b + ev
    G = np.linspace(-1, 1, N); X, Y = np.meshgrid(G, G, indexing="ij")
    W = 0.5 * a * (X**2 + Y**2) + b * X * Y + 0.5 * g * (X * Y**(2 * m) - X**(2 * m) * Y)
    C = np.zeros((2 * m + 1, 2 * m + 1)); C[2, 0] = C[0, 2] = a / 2; C[1, 1] = b; C[1, 2 * m] = g / 2; C[2 * m, 1] = -g / 2
    for d in range(1, dmax + 1):
        A = [np.ones(N * N)] + [(X**k - Y**k).ravel() for k in range(1, d + 1)]
        res = linprog(W.ravel(), A_eq=np.array(A), b_eq=np.r_[1.0, np.zeros(d)], bounds=(0, None), method="highs")
        y = res.eqlin.marginals
        # dual: W(x,y) - y0 - sum_k y_k (x^k - y^k) >= 0 ; continuum lower bound = y0 + min(W - sum y_k x^k + sum y_k y^k)
        rho = np.r_[0.0, y[1:]]
        # min_factor handles degree <= 3 in y; for m = 2 the coupling is degree 4 in y -> use a dense grid check instead
        if 2 * m <= 3 and d <= 3:
            lb, _, _ = min_factor(C, PP.poly(-rho), PP.poly(rho), -1, 1, -1, 1, Nx=401)
        else:
            Gf = np.linspace(-1, 1, 4001); Xf, Yf = np.meshgrid(Gf, Gf, indexing="ij")
            Wf = 0.5 * a * (Xf**2 + Yf**2) + b * Xf * Yf + 0.5 * g * (Xf * Yf**(2 * m) - Xf**(2 * m) * Yf)
            lb = float((Wf - np.polynomial.polynomial.polyval(Xf, rho) + np.polynomial.polynomial.polyval(Yf, rho)).min())
        print(f"  b={b} g={g} ev={ev} chirality deg {2*m+1}: P{d} per-bond LP value {res.fun:+.6f}; dual continuum value {lb:+.6f}", flush=True)

run(0.6, 0.3, 0.05, 1, 3)
run(0.6, 0.3, 0.1, 1, 3)
run(0.6, 0.15, 0.02, 2, 5)
run(0.6, 0.15, 0.005, 2, 5)
