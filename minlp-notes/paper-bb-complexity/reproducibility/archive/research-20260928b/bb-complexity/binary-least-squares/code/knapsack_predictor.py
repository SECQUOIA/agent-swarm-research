"""Large-N extrapolation of the exact-law tree predictor (heuristic, not a
certified computation; Section 7.3).

predict_trees.py prunes a static-order node (d, Wr) when
f(x^Wr)(1 - (N-d)/(2M)) >= W.  Dropping the cross terms b_i'b_j (i != j) of
f(x^Wr) - W (relative size O(N^{-1/2} + 1/rho)), the node survives iff
sum_{i in Wr} delta_i < L_d := W (N-d)/(2M - N + d), with
delta_i = f(x^{i}) - W = 4(zeta_i + ||b_i||^2).  Survival is monotone, so the
number of processed nodes is 1 + 2 sum_{d<N} U_d with
U_d = #{Wr ⊆ [d] : sum_{Wr} delta < L_d}, a knapsack count computed by a DP
over discretized weights (in log scale).  The delta_i are drawn from the exact
single-coordinate law of Lemma 0.1, so no matrices are needed.
Usage: python3 knapsack_predictor.py OUT.jsonl
"""
import sys, json
import numpy as np


def log_tree(N, beta, rho, rng, bins_per_min=8):
    M = int(round(beta * N))
    W = rng.chisquare(M)
    g = rng.standard_normal(N)
    chi = rng.chisquare(M - 1, N)
    delta = 4 * (np.sqrt(rho / N) * np.sqrt(W) * g + (rho / N) * (g ** 2 + chi))
    if delta.min() <= 0:
        return None, float(delta.min())
    d_idx = np.arange(N + 1)
    L = W * (N - d_idx) / (2 * M - N + d_idx)
    h = delta.min() / bins_per_min
    nb = int(np.ceil(L[0] / h)) + 2
    wts = np.maximum(1, np.round(delta / h).astype(int))
    # log-domain counts (a float DP normalized by its maximum loses the low
    # bins and leaves stuck denormals; see Section 7.3 of the note)
    la = np.full(nb, -np.inf); la[0] = 0.0
    logs = []
    for d in range(N):
        lim = int(np.floor(L[d] / h - 1e-12))
        if lim < 0:
            break
        la = la[:lim + 1]                      # later depths never need higher bins
        m = la.max()
        logs.append(np.log(2.0) + m + np.log(np.exp(la - m).sum()))
        wi = wts[d]
        if wi <= lim:
            la[wi:] = np.logaddexp(la[wi:], la[:lim + 1 - wi].copy())
    logs = np.array(logs)
    m = logs.max()
    # log(1 + sum_d 2 U_d), computed without overflow
    return float(np.logaddexp(0.0, m + np.log(np.exp(logs - m).sum()))), float(delta.min())


if __name__ == "__main__":
    rng = np.random.default_rng(99)
    with open(sys.argv[1], "w") as out:
        for beta in (1.0, 2.0):
            for N in (100, 300, 1000, 3000, 10000, 30000, 100000):
                tags = [("c", 4.0), ("c", 8.0), ("r", 8.0), ("r", 32.0), ("r", 128.0)]
                for kind, val in tags:
                    rho = val * np.log(N) if kind == "c" else N / val
                    if rho * beta < 2.2 * np.log(N):
                        continue
                    ns = 5 if N <= 10000 else 2
                    res = []
                    for s in range(ns):
                        lt, dmin = log_tree(N, beta, rho, rng)
                        res.append(lt)
                    ok = [r for r in res if r is not None]
                    rec = dict(beta=beta, N=N, tag="%s%g" % (kind, val), rho=rho, runs=ns,
                               log_tree=ok, n_not_ml=len(res) - len(ok),
                               pred_const=N / (4 * (2 * beta - 1) * rho) * np.log(rho))
                    out.write(json.dumps(rec) + "\n"); out.flush()
