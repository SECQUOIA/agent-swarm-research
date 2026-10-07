"""After review: second-order check at the lot-sizing optimum (prototype, mode
split, eps 1e-6). Active band constraints p_t = 0 or p_t = P; reduced Hessian of F
(in s) on the tangent space of the active constraints; KKT multipliers of the
bands (backward recursion, LotSizingChain.pair_multipliers)."""
import json, sys
import numpy as np
from scipy.linalg import null_space
import lotsizing as LS
import chain_bb as CB
for T, seed in [(50, 0), (12, 0), (32, 1)]:
    d = LS.demands(T, seed)
    pr = LS.LotSizingChain(d)
    r = CB.chain_bb(pr, 1e-6, mode="split", time_limit=600, max_pairs_iter=40_000_000)
    x = r["x"]; s = x[1:]; p = np.diff(x) + d
    g2 = LS.g2(p)
    H = np.diag(2 * LS.ETA + g2 + np.append(g2[1:], 0.0))
    for t in range(T - 1):
        H[t, t + 1] = H[t + 1, t] = -g2[t + 1]
    act = [t for t in range(T) if p[t] < 1e-7 or p[t] > LS.PCAP - 1e-7]
    A = np.zeros((len(act), T))
    for k, t in enumerate(act):
        A[k, t] = 1.0
        if t > 0:
            A[k, t - 1] = -1.0
    Z = null_space(A) if act else np.eye(T)
    red = np.linalg.eigvalsh(Z.T @ H @ Z).min()
    mu = pr.pair_multipliers(x)
    free = [i for i in range(T) if i not in act and (i + 1 not in act)]
    Hf = np.linalg.eigvalsh(H[np.ix_(free, free)]).min() if free else None
    rec = dict(T=T, seed=seed, status=r["status"], gap=r["UB"] - r["LB"], n_active=len(act),
               lmin_full_hessian=float(np.linalg.eigvalsh(H).min()), lmin_reduced_hessian=float(red),
               min_active_multiplier=float(min(mu[t] for t in act)) if act else None,
               max_inactive_multiplier=float(max(abs(mu[t]) for t in range(T) if t not in act)),
               max_abs_s=float(abs(s).max()), lmin_free_block=Hf)
    print(json.dumps(rec), flush=True)
