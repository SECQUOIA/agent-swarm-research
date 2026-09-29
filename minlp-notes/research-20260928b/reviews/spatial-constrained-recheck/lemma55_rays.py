"""Recheck of Lemma 5.5 ((OD) near KKT points) and why its proof needs P_ex polyhedral near z*.

Instance: n = 3, X0 = [-2,2]^3, f(y) = |y - c|^2 with c = (0.5, -0.3, 0),
non-exact reverse-convex constraint g(y) = 1 - |y|^2 <= 0, and an exact constraint in P_ex.
  Case A: P_ex = {y_2 >= 0}              (polyhedral)
  Case B: P_ex = {y_2 >= 4 (y_1 - 1)^2}   (nonlinear, same gradient at z*)
z* = (1,0,0) is the global minimizer in both cases, with multipliers mu_g = 0.5, mu_P = 0.6,
LICQ, active stratum {|y| = 1, y_2 = 0} (d = 1).
Lemma 5.5 construction: grad g . e_hat = 1, grad P . e_hat = 0 -> e = (-1, 0, 0), mu_0 = 1/2.
"""
import numpy as np

rng = np.random.default_rng(0)
c = np.array([0.5, -0.3, 0.0])
zs = np.array([1.0, 0.0, 0.0])
f = lambda Y: np.sum((Y - c) ** 2, axis=-1)
g = lambda Y: 1 - np.sum(Y ** 2, axis=-1)
v = lambda Y: np.maximum(0.0, g(Y))

# KKT at z*
gf = 2 * (zs - c)
gg = -2 * zs
gP = np.array([0.0, -1.0, 0.0])  # P(y) = -y_2 (+ 4(y_1-1)^2 in case B) <= 0; same gradient at z*
A = np.vstack([gg, gP]).T
mu = np.linalg.lstsq(A, -gf, rcond=None)[0]
print("multipliers (mu_g, mu_P) =", mu, " KKT residual =", np.linalg.norm(gf + A @ mu))
# e_hat: minimal-norm solution of [gg; gP] e = [1; 0]
ehat = np.linalg.lstsq(np.vstack([gg, gP]), np.array([1.0, 0.0]), rcond=None)[0]
e = ehat / np.linalg.norm(ehat)
mu0 = -gf @ e / 2
print("e =", e, " mu_0 =", mu0, " (-(mu_g)/|e_hat| / 2 =", mu[0] / np.linalg.norm(ehat) / 2, ")")

# constants from the proof: Hessian bound M = 2, rho with M rho <= mu_0, C_2 = M/2
M = 2.0
rho = mu0 / M
t1 = 0.1
c1 = abs(gg @ e) + M * rho + M * t1 / 2
C2 = M / 2
print(f"rho = {rho}, t1 = {t1}, c_1 = {c1}, C_2 = {C2}")


def sample_F(Pfun, N):
    """Points of F near z*: |y| >= 1, P(y) <= 0, |y - z*| <= rho.

    A quarter of the candidates are put on the stratum {|y| = 1, y_2 = 0}, a quarter on
    {y_2 = 0}, a quarter on {|y| = 1}; the rest are generic. Infeasible candidates are dropped.
    """
    out = []
    while sum(len(o) for o in out) < N:
        Y = zs + rng.uniform(-rho, rho, size=(4 * N, 3))
        q = len(Y) // 4
        Y[:2 * q, 1] = 0.0
        Y[:q] /= np.linalg.norm(Y[:q], axis=1)[:, None]
        Y[2 * q:3 * q] /= np.linalg.norm(Y[2 * q:3 * q], axis=1)[:, None]
        ok = ((np.linalg.norm(Y - zs, axis=1) <= rho) & (np.sum(Y**2, axis=1) >= 1 - 1e-15)
              & (Pfun(Y) <= 1e-15))
        out.append(Y[ok])
    return np.vstack(out)[:N]


for name, Pfun in [("A (polyhedral)", lambda Y: -Y[..., 1]),
                   ("B (nonlinear)", lambda Y: -Y[..., 1] + 4 * (Y[..., 0] - 1) ** 2)]:
    Y = sample_F(Pfun, 20000)
    ts = np.linspace(0, t1, 201)[1:]
    worst_P, worst_v, worst_f = -np.inf, -np.inf, -np.inf
    for t in ts:
        Z = Y + t * e
        worst_P = max(worst_P, np.max(Pfun(Z)))
        worst_v = max(worst_v, np.max(v(Z) - c1 * t))
        worst_f = max(worst_f, np.max(f(Z) - (f(Y) - mu0 * t + C2 * t * t)))
    print(f"case {name}: {len(Y)} points of F near z*; max P(y+te) = {worst_P:.3e} (must be <= 0); "
          f"max v - c1 t = {worst_v:.3e} (<= 0); max f excess = {worst_f:.3e} (<= 0)")
    # at z* itself
    t = 1e-3
    print(f"   at z*: P(z* + 1e-3 e) = {Pfun(zs + t * e):.3e}")
