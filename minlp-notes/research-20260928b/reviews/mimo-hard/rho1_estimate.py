"""Rough size of rho_1(beta) in Theorem 5.1(b) (fixed-rho midpoint cliques).
The proof needs eta*mu*m/4 >= 4 N e^{-0.148 beta rho} (+ lower order), with
mu ~ rho beta, m ~ eta n_T / e^2, n_T ~ N P(g in [-(1+4eta)s, -(1+2eta)s]),
s = sqrt(rho beta)/2, and eta <= 0.04 (so that (1+2eta)^2/8 < 0.148).
We ignore the eps_1 N/rho cap on m (it only lowers m) and the o(1) terms, so
the printed value is a lower estimate of what the proof as written needs."""
import numpy as np
from scipy.stats import norm
for beta in (1.0, 2.0, 4.0):
    best = None
    for eta in np.linspace(0.002, 0.04, 200):
        for rho in np.arange(1.0, 20000.0, 1.0):
            s = np.sqrt(rho * beta) / 2
            # log P(g in [-(1+4eta)s, -(1+2eta)s])
            lp = np.log(max(norm.sf((1 + 2 * eta) * s) - norm.sf((1 + 4 * eta) * s), 1e-300))
            lhs = np.log(eta / 4) + np.log(rho * beta) + np.log(eta / np.e ** 2) + lp
            rhs = np.log(4) - 0.148 * beta * rho
            if lhs >= rhs:
                if best is None or rho < best[0]:
                    best = (rho, eta)
                break
    print("beta=%g: proof of Theorem 5.1(b) needs rho >= ~%d (best eta = %.3f)" % (beta, best[0], best[1]))
