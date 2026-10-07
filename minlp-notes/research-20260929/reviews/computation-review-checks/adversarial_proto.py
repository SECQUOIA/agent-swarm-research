"""Adversarial validity test of chain_bb.py: every iteration's LB must stay <= f*.

Perturbations the validity argument (study, 4.2) claims not to matter:
  - transfers computed at a randomly perturbed incumbent (identity must keep bounds valid),
  - other signs/magnitudes of kappa, b, amp (exercise concave unary pieces, B < 0),
  - modes plain / affine / quad, unary_sub 1 and 16.
f* is bracketed independently by indep_grid_dp.py (semi-concave grid DP), which is valid for
any kappa >= 0 and any b. The test records max over iterations of (LB_it - indep_UB).
"""
import sys, os, json
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../computation"))
import instances as I
import chain_bb as CB
import indep_grid_dp as G

rng = np.random.default_rng(2026)
orig_transfers = CB.transfers


def noisy_transfers(scale):
    def tr(prob, xhat, mode):
        if xhat is None:
            return orig_transfers(prob, xhat, mode)
        xp = np.clip(xhat + scale * rng.standard_normal(len(xhat)), -1, 1)
        return orig_transfers(prob, xp, mode)
    return tr


K = 2001
worst = -np.inf
for kappa, b, amp in [(0.1, 0.8, 0.2), (0.1, -0.8, 0.3), (0.3, 0.9, 0.5), (0.25, -1.2, 0.1), (0.0, 1.5, 0.4)]:
    G.KAPPA, G.B = kappa, b
    for n, seed in [(5, 11), (9, 12), (16, 13)]:
        c = rng.uniform(-amp, amp, n)
        iLB, xg = G.grid_dp(c, K)
        _, iUB = G.polish(xg, c)
        iUB = min(iUB, G.F(xg, c))
        for mode, sub, noise, eps in [("quad", 16, 0.0, 1e-6), ("quad", 1, 0.3, 1e-6), ("affine", 16, 0.3, 1e-5),
                                      ("plain", 1, 0.0, 1e-3), ("quad", 16, 1.0, 1e-6)]:
            CB.transfers = noisy_transfers(noise) if noise > 0 else orig_transfers
            r = CB.chain_bb(I.Probe3Chain(c, kappa=kappa, b=b), eps, mode=mode, unary_sub=sub,
                            max_iter=30, time_limit=60, max_pairs_iter=3_000_000)
            CB.transfers = orig_transfers
            mx = max(h["LB"] for h in r["hist"]) - iUB
            worst = max(worst, mx)
            print(json.dumps(dict(kappa=kappa, b=b, amp=amp, n=n, mode=mode, unary_sub=sub, noise=noise,
                                  eps=eps, status=r["status"], iters=r["iters"],
                                  maxLB_minus_fstarUB=mx, final_LB_minus_indepLB=r["LB"] - iLB,
                                  UB_minus_indepLB=r["UB"] - iLB, indep_gap=iUB - iLB)), flush=True)
print("WORST max_it(LB) - f*_upper =", worst)
