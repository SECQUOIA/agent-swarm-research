"""Arithmetic checks: (1) the corner box behind the 1.063 ceiling (exact V for every class),
(2) a parameter-free cap on mu, (3) the crossover estimates of Section 5."""
import numpy as np
from scipy.optimize import brentq
y1, eta, epsv = 0.38, 0.05, 0.02
b, bp, c = 2 * y1, 2 * eta + 2 * (1 - eta) * (1 - y1), 1 + eta + epsv
z1, k = 2 * eta * y1 / bp, 2 * (1 - eta) * y1
A_ = 1 + epsv - (1 - eta) * (1 - y1) ** 2
gam = y1 ** 2 * (1 - A_) / A_
u = lambda z: bp**2*z**2/(4*eta) if abs(z) <= z1 else (bp*abs(z)+k)**2/4 - (1-eta)*y1**2
g = lambda x, y, z: y1**2*x**2 + b*x*y + c*y**2 + u(z) + bp*y*z
# (1) corner box: every term of both factors is nondecreasing in |x|,|y|,|z| when x, y, z <= 0, so both factor
# minima (split r = 0) sit at the vertex nearest 0, and V_S = min_B g = g(vertex) for EVERY class S.
l = np.array([-1, -1, -1.]); uu = np.array([-0.48, -0.873, -0.813])
V = g(*uu); vol8 = np.prod((uu - l) / 2)
f = lambda mu: vol8 * np.exp(mu * V)
mu0 = brentq(lambda m: f(m) - 1, 1, 4)
print("(1) gamma = %.7f; corner V = %.6f, vol/8 = %.6e" % (gam, V, vol8))
for mu in (2.3, 2.4, 2.5):
    print("    mu=%.1f: (vol/8) exp(mu V) = %.4f" % (mu, f(mu)))
print("    threshold mu0 = %.4f; ceiling exp(mu0 gamma) = %.4f per gadget, %.4f per variable; with mu = 2.4: %.4f, %.4f"
      % (mu0, np.exp(mu0 * gam), np.exp(mu0 * gam / 3), np.exp(2.4 * gam), np.exp(2.4 * gam / 3)))
print("    computed base 1.05156 vs ceiling: ratio %.4f" % (np.exp(2.4 * gam / 3) / 1.05156))
for gd, name in [(0.0077701, "b4 ref"), (0.0023727, "b6 ref"), (0.0247400, "b4 (0.30,0.005,0.002)")]:
    print("    %s: exp(2.4 gamma_d) = %.4f per gadget, %.4f per variable" % (name, np.exp(2.4 * gd), np.exp(2.4 * gd / 3)))
print("    y1=0.30: 2E_4 = 2*0.01306 -> exp(2.4*2E_4/3) = %.4f per variable" % np.exp(2.4 * 2 * 0.01306 / 3))
# (2) parameter-free cap: on [-1,-1/2]^3, x,y,z <= 0, both factors >= their share of c y^2 >= c/4 > 1/4.
print("(2) box [-1,-1/2]^3: V >= c/4 >= 1/4 for all parameters; (1/64) exp(mu/4) >= 1 once mu >= %.2f" % (4 * np.log(64)))
# (3) crossovers.  Theorem 3.4 of the decomposition note with k = 2, Delta = 1, w = 1, K_1 = 1, s0 = 2.
cg, Ma, alph, A = 7.22e-4 / 2, 16.4, bp / 2, 2
Q = Ma**2 * 1 * 2 / cg + Ma / 2 + alph * A
mu = 0
while (2.0**-mu)**2 * 2 * (48 * 1 * 2 * Q + alph * A) > cg / 2: mu += 1
th = 2.0**-mu
eps = 1e-4
Ndec = lambda n: 2 * (n - 1) * (4 / th)**2 * (0.5 * np.log2(4 * (n - 1) * 4 * (768 * Q + 3 * alph * A) / eps) + 2)
print("(3) Q = %.4e, theta = 2^-%d, (4/theta)^2 = %.3e, N_dec(850)/850 = %.2e" % (Q, mu, (4 / th)**2, Ndec(850) / 850))
for base, nm in [(1.1627806 ** (1 / 3), "computed"), (np.exp(gam / (2 * max(2*y1**2+2*y1, 2*y1+2*c+bp, 2*bp)) / 3), "analytic")]:
    n1 = brentq(lambda n: n * np.log(base) - np.log(Ndec(n)), 10, 1e6)
    n2 = brentq(lambda n: n * np.log(base) - np.log(4e15 * n), 10, 1e6)
    n3 = brentq(lambda n: n * np.log(base) - np.log(22 / 3 * n), 10, 1e6)
    print("    %s base %.5f per variable: vs Theorem 3.4 formula n = %.0f (with 4e15 n: %.0f); vs gadget bags 22 n/3: n = %.0f"
          % (nm, base, n1, n2, n3))
