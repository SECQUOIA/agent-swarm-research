"""Lot-sizing (study, 1.2 and 6): at the prototype's certified optimum, compare
  (a) the full Hessian of F in the inventory variables s_1..s_T,
  (b) the reduced Hessian Z' H Z on the tangent space of the active constraints
      (p_t = 0, p_t = P, |s_t| = S), which is what second-order optimality conditions concern,
  (c) the Hessian restricted to s_t with no incident active constraint.
Also reports the multipliers of the active band constraints (strict complementarity).
"""
import sys, os, json
import numpy as np
from scipy.linalg import null_space
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../computation"))
import lotsizing as LS
import chain_bb as CB

for T, seed in json.loads(sys.argv[1]):
    d = LS.demands(T, seed)
    pr = LS.LotSizingChain(d)
    r = CB.chain_bb(pr, 1e-6, mode="split", time_limit=300, max_pairs_iter=40_000_000)
    x = r["x"]; s = x[1:]
    p = np.diff(x) + d
    g2 = LS.g2(p)
    H = np.diag(2 * LS.ETA * np.ones(T))
    for t in range(T):          # p_t depends on s_t (+1) and s_{t-1} (-1), t >= 1
        H[t, t] += g2[t]
        if t + 1 < T:
            H[t, t] += g2[t + 1]
            H[t, t + 1] -= g2[t + 1]; H[t + 1, t] -= g2[t + 1]
    tol = 1e-7
    rows, free = [], np.ones(T, bool)
    for t in range(T):
        if p[t] < tol or p[t] > LS.PCAP - tol:
            a = np.zeros(T); a[t] = 1.0
            if t > 0: a[t - 1] = -1.0
            rows.append(a); free[t] = False
            if t > 0: free[t - 1] = False
        if abs(s[t]) > LS.SCAP - tol:
            a = np.zeros(T); a[t] = 1.0; rows.append(a); free[t] = False
    Z = null_space(np.array(rows)) if rows else np.eye(T)
    red = Z.T @ H @ Z
    mu = pr.pair_multipliers(x)  # band multipliers from the KKT recursion
    act = [t for t in range(T) if p[t] < tol]
    print(json.dumps(dict(T=T, seed=seed, status=r["status"], LB=r["LB"], UB=r["UB"],
                          n_active_band=len(rows), n_idle=int((p < tol).sum()),
                          lmin_full=float(np.linalg.eigvalsh(H)[0]),
                          lmin_reduced=float(np.linalg.eigvalsh(red)[0]) if red.size else None,
                          dim_tangent=int(Z.shape[1]),
                          lmin_free_vars=float(np.linalg.eigvalsh(H[np.ix_(free, free)])[0]) if free.any() else None,
                          n_free_vars=int(free.sum()),
                          min_abs_band_multiplier=float(np.min(np.abs(mu[act]))) if act else None)), flush=True)
