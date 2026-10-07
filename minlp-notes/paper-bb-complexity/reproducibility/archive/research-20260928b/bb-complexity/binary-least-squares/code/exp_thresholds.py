"""E4: first-order thresholds from the exact single-coordinate law (Lemma 0.1):
given w, g_i = <h~_i, w/|w|> iid N(0,1) and |h~_i^perp|^2 iid chi^2_{M-1}, so
    zeta_i = sqrt(rho/N) |w| g_i,   |b_i|^2 = (rho/N)(g_i^2 + chi^2_{M-1}).
Events (for rho = c log N / beta):
  ML1   : some one-bit flip beats x*:        zeta_i + |b_i|^2 < 0     (c* = 2)
  HALF  : some half move gives a midpoint below f(x*): 2 zeta_i + |b_i|^2 < 0 (c* = 8)
Box-decoder success is not simulated here (Hu-Lu: 2 log N/(beta - 1/2)).
Part 2 (real instances): pair half-moves c = e_i + e_j and single ones,
to check that multi-coordinate midpoint conflicts do not appear before
single ones.
Usage: python3 exp_thresholds.py OUT.jsonl
"""
import sys, json, os
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
from core import instance

rng = np.random.default_rng(2026)


def sample_events(N, M, rho, trials):
    ml = half = 0
    for t in range(trials):
        W = rng.chisquare(M)
        g = rng.standard_normal(N)
        perp = rng.chisquare(M - 1, N)
        zeta = np.sqrt(rho / N) * np.sqrt(W) * g
        bb = (rho / N) * (g ** 2 + perp)
        ml += bool(np.any(zeta + bb < 0))
        half += bool(np.any(2 * zeta + bb < 0))
    return ml / trials, half / trials


def pairs_check(N, beta, c, seeds):
    """Returns counts of instances with a single half-move conflict and with a
    pair half-move conflict (c = e_i + e_j), relative to f(x*)."""
    M = int(beta * N); rho = c * np.log(N) / beta
    s1 = s2 = s2only = 0
    for s in range(seeds):
        A, y, xs, B, w = instance(N, M, rho, s)
        zeta = B.T @ w
        Gm = B.T @ B
        d = np.diag(Gm)
        single = 2 * zeta + d
        pair = 2 * (zeta[:, None] + zeta[None, :]) + d[:, None] + d[None, :] + 2 * Gm
        np.fill_diagonal(pair, np.inf)
        a = bool(single.min() < 0); b = bool(pair.min() < 0)
        s1 += a; s2 += b; s2only += (b and not a)
    return s1, s2, s2only


if __name__ == "__main__":
    with open(sys.argv[1], "w") as out:
        for beta in (1, 2):
            for N in (10**2, 10**3, 10**4, 10**5):
                M = beta * N
                for c in (1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 12.0):
                    rho = c * np.log(N) / beta
                    trials = 2000 if N <= 10**3 else (400 if N == 10**4 else 100)
                    if M > 2 * 10**5:
                        trials = 60
                    pml, phalf = sample_events(N, M, rho, trials)
                    out.write(json.dumps(dict(part="law", N=N, beta=beta, c=c, rho=rho, trials=trials,
                                              p_ml_fail=pml, p_half_conflict=phalf)) + "\n")
                    out.flush()
        for beta in (1, 2):
            for N in (200, 800):
                for c in (4.0, 6.0, 7.0, 8.0, 9.0, 10.0):
                    s1, s2, s2only = pairs_check(N, beta, c, 20)
                    out.write(json.dumps(dict(part="pairs", N=N, beta=beta, c=c, seeds=20,
                                              single=s1, pair=s2, pair_without_single=s2only)) + "\n")
                    out.flush()
