"""Check of the report's Section 5 statement (not part of any proof): the entrywise hull of
sampled Hessians over the price box [0, pmax] fails the lambda_max(mid) + rho(radius) test
(report: -0.109 + 0.119 > 0, 4,000 samples)."""
import os
import pickle
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import own_psi as P  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
RG = pickle.load(open(os.path.join(HERE, "ranges.pkl"), "rb"))
pmax = np.array([float(v) for v in RG["pmaxq"]])
K = 0.5 * (P.K_LO + P.K_HI)
CT = [float(c) for c in P.MOD.CT]


def theta_float(p):
    td, s, cs, R = 18.0, 6.5, 0.0, 500.0
    th = {g: np.zeros(16) for g in P.GR}
    for t in range(16):
        td = 0.87 * td - 0.13 * p[t] + CT[t]
        E = np.exp(-K * cs)
        beta = (1.1 + 0.1 * p[t]) * E
        a = 0.75 * s
        y = a + beta
        for _ in range(50):
            y -= (y - a - beta * np.exp(-K * y)) / (1 + K * beta * np.exp(-K * y))
        s = y
        cs += s
        d = td - s
        R -= d
        for g, v in zip(P.GR, [beta, E, np.exp(-K * s), d, p[t] - 250 / R, R ** -2, R ** -3]):
            th[g][t] = v
    return th


out = open(os.path.join(HERE, "logs", "hull_claim.log"), "w")
for label, seed, mode in [("uniform", 3, "u"), ("corners only", 5, "c"), ("half corners, half uniform", 6, "h")]:
    rng = np.random.default_rng(seed)
    Hs = []
    for k in range(4000):
        corner = mode == "c" or (mode == "h" and k % 2)
        p = rng.choice([0.0, 1.0], size=16) * pmax if corner else rng.uniform(0, pmax)
        Hs.append(P.psi_float(theta_float(p)))
    Hs = np.array(Hs)
    lo, hi = Hs.min(0), Hs.max(0)
    mid, rad = 0.5 * (lo + hi), 0.5 * (hi - lo)
    lm, rr = np.linalg.eigvalsh(mid)[-1], np.linalg.eigvalsh(rad)[-1]
    msg = (f"sampled hull over [0, pmax], 4000 samples ({label}): lambda_max(mid) = {lm:.4f}, rho(rad) = {rr:.4f}, "
           f"sum = {lm + rr:.4f}; largest sampled lambda_max = {max(np.linalg.eigvalsh(H)[-1] for H in Hs):.4f}")
    print(msg)
    out.write(msg + "\n")
