"""Checks of (G5) and of the Beta Chernoff bound in Lemma 4.1."""
import numpy as np
from scipy import integrate
from scipy.stats import norm, beta
# (G5): m(tau) = E exp((|Z|-tau)_+^2/4) - 1 = 2 sqrt2 e^{tau^2/2} Phibar(sqrt2 tau) - 2 Phibar(tau) <= 2 phi(tau)/tau
for tau in [0.5, 1.0, 2.0, 3.0, 4.0]:
    num = 2 * integrate.quad(lambda z: (np.exp((z - tau) ** 2 / 4 - z * z / 2) - np.exp(-z * z / 2)) / np.sqrt(2 * np.pi), tau, tau + 60)[0]
    form = 2 * np.sqrt(2) * np.exp(tau ** 2 / 2) * norm.sf(np.sqrt(2) * tau) - 2 * norm.sf(tau)
    print("G5 tau=%.1f  quadrature %.6e  formula %.6e  bound 2phi/tau %.6e" % (tau, num, form, 2 * norm.pdf(tau) / tau))
# Lemma 4.1: P(Beta(k/2,(n-k)/2) >= rho) <= exp(-(n/2) d(q||rho)), q = k/n
def d(q, r): return q * np.log(q / r) + (1 - q) * np.log((1 - q) / (1 - r))
worst = -np.inf
for n in [20, 50, 200]:
    for k in [1, 3, 10]:
        if k >= n: continue
        q = k / n
        for rho in np.linspace(q + 0.01, 0.95, 30):
            exact = beta.sf(rho, k / 2, (n - k) / 2); bound = np.exp(-(n / 2) * d(q, rho))
            worst = max(worst, exact / bound)
print("max over grid of exact Beta tail / Chernoff bound: %.4f (must be <= 1)" % worst)
