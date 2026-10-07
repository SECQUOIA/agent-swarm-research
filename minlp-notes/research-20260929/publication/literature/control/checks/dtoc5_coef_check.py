"""Floating-point provenance check (evidence, not proof).

CUTEst DTOC5.SIF (N periods, h = 1/N):
  min (1/N) sum_{t=1}^{N-1} (y_t^2 + x_t^2)
  s.t. y_t - y_{t+1} - h x_t + c*h*y_t^2 = 0, t = 1..N-1, y_1 = 1,
with c = 1 in the SIF and c = 4 in QPLIB_8585 / MINLPLib dtoc5.
Eliminate x_t = (y_t + c h y_t^2 - y_{t+1})/h and minimize over y_2..y_N
by damped Newton with the exact tridiagonal Hessian (local solve).
Compare with the SIF *LO SOLUTION lines and with the MINLPLib primal
value 5.38967212 (N = 50000, c = 4).
"""
import numpy as np
from scipy.linalg import solve_banded

def F(y, h, c):
    x = (y[:-1] + c * h * y[:-1] ** 2 - y[1:]) / h
    return h * np.sum(y[:-1] ** 2 + x ** 2)

def solve(N, c):
    h = 1.0 / N
    y = np.ones(N)  # y_1..y_N, y[0] fixed = 1
    for it in range(200):
        a = y[:-1]; b = y[1:]
        r = a + c * h * a ** 2 - b           # = h x_t
        da = 1 + 2 * c * h * a                # dr/da
        g = np.zeros(N); H0 = np.zeros(N); H1 = np.zeros(N - 1)
        # term_t = h a^2 + r^2 / h
        g[:-1] += 2 * h * a + 2 * r * da / h
        g[1:] += -2 * r / h
        H0[:-1] += 2 * h + (2 * da ** 2 + 2 * r * 2 * c * h) / h
        H0[1:] += 2 / h
        H1 += -2 * da / h                      # d2/da db
        gg = g[1:]; d0 = H0[1:]; off = H1[1:]
        ab = np.zeros((3, N - 1))
        ab[0, 1:] = off; ab[1, :] = d0; ab[2, :-1] = off
        step = solve_banded((1, 1), ab, -gg)
        f0 = F(y, h, c); s = 1.0
        while True:
            yn = y.copy(); yn[1:] += s * step
            if F(yn, h, c) <= f0 + 1e-4 * s * gg.dot(step) or s < 1e-12:
                break
            s *= 0.5
        y = yn
        if np.max(np.abs(gg)) < 1e-13 and s == 1.0:
            break
    return F(y, h, c), it, np.max(np.abs(gg))

for N in (10, 50, 100, 500, 1000, 5000, 50000):
    for c in (1, 4):
        v, it, gn = solve(N, c)
        print(f"N={N:6d} c={c}: value={v:.12f} newton_iters={it} max|grad|={gn:.1e}", flush=True)
