"""Small checks quoted in robust-chains.md (floating point).
1. UD chain: coefficients of u, x* for n = 8, the best value with x_1 restricted to [-1, 0.45] (left end not in
   the second well) by grid DP, and the smallest Hessian eigenvalue of f_8 at x* (u'' is piecewise constant).
2. Chiral chain, class P2, k = 7: which term of the computed bound binds at the reported mu, and the corner
   suprema sup_d ((1-d)/2) exp(mu c_j d^2).
"""
import sys, json
import numpy as np
sys.path.insert(0, "..")
from uniform_design import make_pw, dp_fstar, G
from run_uniform import PARAMS, B
from chiral_bounds import computed_base, sup_corner

u = make_pw(PARAMS[0], B, *PARAMS[1:])
print("UD u pieces (breakpoints, coefficients in powers of x):", u.bps.tolist(), [c.round(6).tolist() for c in u.coefs])
n = 8
fs, xs = dp_fstar(u, B, n)
# restricted DP: x_1 <= 0.45
uG = u(G); V = np.where(G <= 0.45, uG, np.inf)
for _ in range(1, n):
    M = V[:, None] + B * G[:, None] * G[None, :]
    V = M.min(axis=0) + uG
print(f"UD n=8: f* = {fs:.6f}, x* = {np.round(xs, 4).tolist()}, best grid value with x_1 <= 0.45: {V.min():.6f} (margin {V.min()-fs:.4f})")
upp = np.array([6.0 if x <= 0.3 else (-3.0 if x <= 0.6 else 4.0) for x in xs])
H = np.diag(upp) + B * (np.eye(n, k=1) + np.eye(n, k=-1))
print("UD n=8: u'' at x* =", upp.tolist(), " smallest Hessian eigenvalue =", round(float(np.linalg.eigvalsh(H).min()), 4))

b, g, ev = 0.6, 0.3, 0.05; a = b + ev; k = 7
rec = [json.loads(l) for l in open("logs/chiral_bounds_P2.log") if '"k": 7' in l][0]
th = np.array([float(t) for t in rec["gamma_theta"]]); gam = np.array(list(rec["gamma_theta"].values()))
mu, th1 = rec["computed_at"]
start = int(np.where(np.isclose(th, th1))[0][0])
cvec = np.array([a + (b + g) / 2] + [a + b + g] * (k - 2) + [a + (b + g) / 2])
terms = [("full cube", np.exp(-mu * gam[-1]))]
for i in range(start, len(th) - 1):
    terms.append((f"core {th[i]} not {th[i+1]}", (1 + th[i + 1]) / 2 * np.exp(-mu * max(gam[i], 0))))
H_ = [max(1.0, sup_corner(mu, c)) for c in cvec]
Hp = [max((1 + th1) / 2, sup_corner(mu, c)) for c in cvec]
psi = max(Hp[j0] * np.prod([H_[j] for j in range(k) if j != j0]) for j0 in range(k))
terms.append(("Psi (point masses)", psi))
best = max(terms, key=lambda t: t[1])
print(f"chiral P2 k=7 at mu={mu}: binding term = {best[0]} value {best[1]:.5f}; Phi = {computed_base(gam[start:], th[start:], cvec, mu):.5f}")
print("  corner suprema:", {round(float(c), 3): round(sup_corner(mu, c), 4) for c in set(cvec)})
print("  all terms:", [(t, round(float(v), 4)) for t, v in terms])
