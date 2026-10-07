"""Lower bounds on E_d(L) = dist_inf(L, P_d) on [-1,1] for L(y) = y^2 (|y|<=y1), 2 y1|y| - y1^2 (|y|>y1).
Grid LP (a valid lower bound on E_d).  Band bound (Proposition 12): gamma_d >= 2 E_d(L) - max(U-L),
max(U-L) = eps + eta (1-y1)^2 for the bang-bang gadget."""
import sys
import numpy as np
from numpy.polynomial import chebyshev as C
from scipy.optimize import linprog

def Ed(y1, d, M=4001):
    y = np.cos(np.linspace(0, np.pi, M))
    L = np.where(np.abs(y) <= y1, y * y, 2 * y1 * np.abs(y) - y1 * y1)
    V = C.chebvander(y, d)                      # columns T_0..T_d
    k = V.shape[1]
    # variables a (free, k), t >= 0; minimise t;  L - V a <= t,  V a - L <= t
    A = np.vstack([np.hstack([-V, -np.ones((M, 1))]), np.hstack([V, -np.ones((M, 1))])])
    b = np.concatenate([-L, L])
    c = np.zeros(k + 1); c[-1] = 1
    res = linprog(c, A_ub=A, b_ub=b, bounds=[(None, None)] * k + [(0, None)], method="highs")
    return res.fun

if __name__ == "__main__":
    for y1 in [0.3, 0.38, 0.5]:
        print("y1=%.2f  " % y1 + "  ".join("E_%d=%.5f" % (d, Ed(y1, d)) for d in [2, 3, 4, 5, 6, 8, 10, 12]))
