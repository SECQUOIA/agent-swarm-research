"""Example A, continuous Lyapunov family Q_eps (eps = .02): (W5) margin |sigma| - Delta |beta|^2 / (2 mu), mu = 2 eps,
on the last arc and before the switch (Lyapunov with u = +1 continued through tau)."""
import numpy as np
from scipy.integrate import solve_ivp
import v_riccati as R

tau, siga, sigb, par, rec = R.sigma_funcs("A")
eps = 0.02
w = -np.array([par["k1"], par["k2"]]); Hxx = np.diag([par["q"], -par["c"]])
f = lambda t, y: (-(R.A.T @ y.reshape(2, 2) + y.reshape(2, 2) @ R.A + Hxx) + 2 * eps * np.eye(2)).ravel()
sol = solve_ivp(f, (2.0, 0.0), (np.diag([0, par["rho"]]) - 2 * eps * np.eye(2)).ravel(), dense_output=True, rtol=1e-11, atol=1e-13)
bad = []
for t in np.linspace(0.01, 1.99, 199):
    P = sol.sol(t).reshape(2, 2); beta = P @ R.b - w
    sig = siga(t) if t < tau else sigb(t)
    margin = abs(sig) - 2.0 * (beta @ beta) / (2 * 2 * eps)
    bad.append((t, margin))
bad = np.array(bad)
neg = bad[bad[:, 1] <= 0, 0]
print("tau=%.4f; (W5) violated for t in [%.3f, %.3f] (%d of %d grid points); max margin %.3g, min margin %.3g"
      % (tau, neg.min(), neg.max(), len(neg), len(bad), bad[:, 1].max(), bad[:, 1].min()))
print("|beta| on last arc: min %.3f max %.3f" % (min(np.linalg.norm(sol.sol(t).reshape(2,2) @ R.b - w) for t in np.linspace(tau, 2, 50)),
                                                  max(np.linalg.norm(sol.sol(t).reshape(2,2) @ R.b - w) for t in np.linspace(tau, 2, 50))))
