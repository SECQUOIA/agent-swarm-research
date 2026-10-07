"""dtoc5 primal: minimize the reduced objective F(y) = sum_t g(y_t, y_{t+1}),
g(y,z) = (y + 4h y^2 - z)^2/h + h y^2, y_0 = 1, h = 2e-5, T = 49999, by Newton's
method with a banded (tridiagonal) Hessian. Controls are recovered from the
dynamics, u_t = (y_t + 4h y_t^2 - y_{t+1})/h, so the equality rows hold up to rounding."""
import json, sys
import numpy as np
from scipy.linalg import solveh_banded, solve_banded

h = 2e-5; T = 49999

def F_grad_hess(y):  # y has length T+1, y[0] fixed
    yt, yn = y[:-1], y[1:]
    r = yt + 4*h*yt**2 - yn            # residual = h u_t
    f = np.sum(r**2)/h + h*np.sum(yt**2)
    dr_dyt = 1 + 8*h*yt
    g = np.zeros_like(y)
    g[:-1] += 2*r*dr_dyt/h + 2*h*yt
    g[1:] += -2*r/h
    # Hessian (tridiagonal): d2/dyt2 = 2(dr^2 + r*8h)/h + 2h ; d2/dyn2 = 2/h ; d2/dyt dyn = -2 dr/h
    d = np.zeros_like(y); d[:-1] += 2*(dr_dyt**2 + r*8*h)/h + 2*h; d[1:] += 2/h
    off = -2*dr_dyt/h
    return f, g, d, off

def newton(y, iters=50):
    for it in range(iters):
        f, g, d, off = F_grad_hess(y)
        gg = g[1:]; dd = d[1:]; oo = off[1:]   # free variables y_1..y_T
        ab = np.zeros((3, T)); ab[0,1:] = oo; ab[1,:] = dd; ab[2,:-1] = oo
        step = solve_banded((1,1), ab, -gg)
        # backtracking
        a = 1.0
        while True:
            yn = y.copy(); yn[1:] += a*step
            fn = F_grad_hess(yn)[0]
            if fn <= f + 1e-4*a*gg.dot(step) or a < 1e-12: break
            a *= 0.5
        y = yn
        print(it, f, fn, np.abs(gg).max(), a, flush=True)
        if np.abs(gg).max() < 1e-12 and a == 1.0: break
    return y

if __name__ == "__main__":
    y = np.ones(T+1)*1.0
    tt = np.arange(T+1)*h
    y = np.exp(-3*tt)  # rough start
    y[0] = 1.0
    y = newton(y)
    np.save("logs/dtoc5_y.npy", y)
    f = F_grad_hess(y)[0]
    print("F", repr(f), "y range", y.min(), y.max(), "y at t=0.1,0.5,1", y[5000], y[25000], y[-1])
