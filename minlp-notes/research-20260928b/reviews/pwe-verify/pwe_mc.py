"""Monte Carlo: probability that the PWE relaxation (19) is exact (P_IR = P*), rho = sqrt n.

Usage: python3 pwe_mc.py NOISE N_INST n1,n2,...   (NOISE = entry | total)

Exactness is decided exactly for each instance:
  - if the Corollary 2 certificate holds at the true support S, then P_IR = f(S) = P* (weak duality
    at alpha = M_S y), so the relaxation is exact;
  - otherwise P* and S_opt come from full enumeration, and exactness is the certificate at S_opt
    (PWE Corollary 2; ties have probability zero).
Also reported: the conditional (Rao-Blackwellized) probability of the certificate at the true
support, E[(1 - 2 Phibar(m0/||M y||))^{d-k}], and the n -> infinity limit for per-entry noise.
"""
import sys
import numpy as np
from scipy.special import ndtr
from pwe_lib import instance, enumerate_opt, cert, limit_prob

noise, N = sys.argv[1], int(sys.argv[2])
ns = [int(v) for v in sys.argv[3].split(",")]
d, k, b, gam = 50, 5, 1.0, 0.5
print(f"noise={noise} d={d} k={k} |w*_j|={b} gamma={gam} rho=sqrt(n) instances/row={N}")
if noise == "entry":
    print(f"n->inf limit of P(cert at true S) = (1-2 Phibar(b/gamma))^(d-k) = {limit_prob(b, gam, d, k):.4f}")
print("n | c0_implied | P(exact) [95% CI] | P(S_opt=S_true) | mean cond. P(cert at S_true) | "
      "median m0/sqrt(n) | median max|a_l|/sqrt(n) | enumerations")
for n in ns:
    rho = np.sqrt(n)
    c0 = n * b * b / ((gam ** 2 + k * b * b) * np.log(d))
    ex, same, condp, m0s, Ms, nenum = [], [], [], [], [], 0
    for s in range(N):
        X, y, S, w = instance(n, d, k, b, gam, 10 ** 6 * n + s, noise)
        a, m0, M0, My = cert(X, y, rho, S)
        condp.append((1 - 2 * (1 - ndtr(m0 / np.linalg.norm(My)))) ** (d - k))
        m0s.append(m0 / np.sqrt(n)); Ms.append(M0 / np.sqrt(n))
        if M0 <= m0:
            ex.append(True); same.append(True)
            continue
        nenum += 1
        Pstar, Sopt, _ = enumerate_opt(X, y, rho, k)
        eq = np.array_equal(np.sort(Sopt), S)
        same.append(eq)
        if eq:
            ex.append(False)
        else:
            _, m1, M1, _ = cert(X, y, rho, Sopt)
            ex.append(M1 <= m1)
    p = np.mean(ex)
    h = 1.96 * np.sqrt(max(p * (1 - p), 1e-12) / N)
    print(f"{n} | {c0:.1f} | {p:.3f} [{max(0, p - h):.3f}, {min(1, p + h):.3f}] | {np.mean(same):.3f} | "
          f"{np.mean(condp):.3f} | {np.median(m0s):.3f} | {np.median(Ms):.3f} | {nenum}", flush=True)
