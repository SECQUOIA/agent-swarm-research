"""Sensitivity of the example-B blow-up distance to the blow-up threshold and the integrator."""
import numpy as np
from scipy.integrate import solve_ivp
import v_riccati as R

tau, siga, sigb, par, r = R.sigma_funcs("B")
for eps in (0.0,):
    f, w = R.rhs_factory(par, sigb, eps)
    PT = np.diag([0.0, par["rho"]]) - 2 * eps * np.eye(2)
    for thr in (1e4, 1e6, 1e8, 1e10):
        ev = lambda t, y: thr - np.abs(y).max()
        ev.terminal = True
        for meth in ("Radau", "LSODA", "DOP853"):
            sol = solve_ivp(f, (2.0, tau + 1e-12), PT.ravel(), method=meth, rtol=1e-11, atol=1e-13, events=ev)
            P = sol.y[:, -1].reshape(2, 2); beta = P @ R.b - w
            print("thr %.0e %-6s s_b=%.6e eta=%.3e status=%d nfev=%d" % (thr, meth, sol.t[-1] - tau, R.b @ beta, sol.status, sol.nfev))
    # log-variable integration: s = exp(lam)
    def g(lam, y):
        s = np.exp(lam); return s * f(tau + s, y)
    for thr in (1e6, 1e8):
        ev = lambda lam, y: thr - np.abs(y).max()
        ev.terminal = True
        sol = solve_ivp(g, (np.log(2.0 - tau), np.log(1e-12)), PT.ravel(), method="DOP853", rtol=1e-12, atol=1e-13, events=ev)
        print("log-var thr %.0e s_b=%.6e status=%d" % (thr, np.exp(sol.t[-1]), sol.status))
print("sigma_b'(tau) =", (sigb(tau + 1e-7) - sigb(tau)) / 1e-7, " sigma_b(tau)=", sigb(tau))
