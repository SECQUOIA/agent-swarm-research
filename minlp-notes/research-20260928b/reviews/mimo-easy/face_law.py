"""Reviewer check of Theorem 1.3 (projection onto a Gaussian cone).

For a fixed v and columns g_1..g_n (n <= M), the projection of v onto
K = cone{g_j} lies in the relative interior of the face F_S; the note claims
  (a) S is uniform over all 2^n subsets,
  (b) given |S| = s, ||Pi_K v||^2/||v||^2 ~ Beta(s/2, (M-s)/2),
  (c) for v ~ N(0, I_M), ||Pi_K v||^2 ~ chi^2_{|S|}, |S| ~ Bin(n, 1/2)
      (mean n/2, variance 5n/4).
The reviewer's claim: (a) needs only that the joint law of the columns is
invariant under flipping the sign of any single column (plus general
position); (b) needs rotation invariance.  Negative controls: a mean shift
(no sign symmetry) and n > M (cone not simplicial).

Projection via NNLS: Pi_K v = G alpha, alpha = argmin_{alpha >= 0} ||v - G alpha||.
Written from scratch by the reviewer; uses only numpy/scipy.
Usage: python3 face_law.py > face_law.out
"""
import os
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
from scipy.optimize import nnls
from scipy import stats


def face_and_ratio(G, v):
    a, _ = nnls(G, v, maxiter=100 * G.shape[1] + 100)
    S = a > 1e-12 * max(1.0, a.max(initial=0.0))
    p = G @ a
    return S, float(p @ p) / float(v @ v)


def run(name, sampler, n, M, T, rng, v=None, check_beta=True):
    if v is None:
        v = np.zeros(M); v[0] = 1.0; v[1] = 0.5  # fixed, not special
    idx = np.empty(T, dtype=np.int64); ratio = np.empty(T); size = np.empty(T, dtype=int)
    w = 1 << np.arange(n)
    for t in range(T):
        G = sampler(rng, M, n)
        S, r = face_and_ratio(G, v)
        idx[t] = int((S * w).sum()); ratio[t] = r; size[t] = S.sum()
    counts = np.bincount(idx, minlength=2 ** n)
    chi = stats.chisquare(counts)
    line = (f"{name:38s} n={n} M={M} T={T}  chi2 p-value(uniform over 2^n faces)={chi.pvalue:.3g}  "
            f"min/max face freq*2^n={counts.min()*2**n/T:.3f}/{counts.max()*2**n/T:.3f}  "
            f"mean|S|={size.mean():.3f} (n/2={n/2})  var|S|={size.var():.3f} (n/4={n/4})")
    print(line)
    if check_beta:
        pv = []
        for s in range(1, min(n, M - 1) + 1):
            rs = ratio[size == s]
            if len(rs) > 50:
                pv.append((s, len(rs), stats.kstest(rs, stats.beta(s / 2, (M - s) / 2).cdf).pvalue))
        print("    KS p-values of Beta(s/2,(M-s)/2) given |S|=s:",
              ", ".join(f"s={s}(n={c}):{p:.3g}" for s, c, p in pv))


def gauss(rng, M, n):
    return rng.standard_normal((M, n))


def laplace(rng, M, n):
    return rng.laplace(size=(M, n))


def make_corr(M, rng0):
    L = np.eye(M) + 0.8 * rng0.standard_normal((M, M))  # fixed non-orthogonal
    return lambda rng, M_, n: L @ rng.standard_normal((M_, n))


def dependent_signsym(rng, M, n):
    # columns strongly dependent (h_j = h_1 + 0.3 z_j) but each column gets an
    # independent random sign: the joint law is invariant under single-column sign flips
    h1 = rng.standard_normal(M)
    H = h1[:, None] + 0.3 * rng.standard_normal((M, n))
    H[:, 0] = h1 * rng.exponential(1.0)
    return H * rng.choice([-1.0, 1.0], n)


def shifted(rng, M, n):
    return rng.standard_normal((M, n)) + 0.7  # not sign symmetric


if __name__ == "__main__":
    rng = np.random.default_rng(20260929)
    T = 64000
    print("== Gaussian columns (Theorem 1.3 setting) ==")
    for (n, M) in [(3, 3), (3, 5), (4, 4), (4, 9), (5, 6), (6, 12)]:
        run("gaussian", gauss, n, M, T, rng)
    print("== sign-symmetric, NOT rotation invariant: face law should hold, Beta law need not ==")
    for (n, M) in [(4, 4), (4, 9)]:
        run("iid Laplace entries", laplace, n, M, T, rng)
        run("N(0, Sigma) columns, Sigma fixed non-identity", make_corr(M, np.random.default_rng(7)), n, M, T, rng)
        run("dependent columns with random signs", dependent_signsym, n, M, T, rng)
    print("== negative controls ==")
    run("mean-shifted Gaussian (no sign symmetry)", shifted, 4, 9, T, rng, check_beta=False)
    for (n, M) in [(5, 3), (6, 3)]:
        run("Gaussian, n > M (not simplicial)", gauss, n, M, T, rng, check_beta=False)

    print("== part (c): v ~ N(0, I_M) independent, larger n ==")
    for (n, M, T2) in [(50, 50, 4000), (100, 100, 2000), (100, 200, 2000), (200, 200, 1000)]:
        sz = np.empty(T2); gi = np.empty(T2)
        for t in range(T2):
            G = rng.standard_normal((M, n)); v = rng.standard_normal(M)
            a, _ = nnls(G, v, maxiter=100 * n)
            p = G @ a
            sz[t] = (a > 0).sum(); gi[t] = p @ p
        print(f"n={n} M={M} T={T2}: mean|S|/n={sz.mean()/n:.4f} (0.5)  var|S|/n={sz.var()/n:.4f} (0.25)  "
              f"mean||Pi v||^2/n={gi.mean()/n:.4f} (0.5)  var/n={gi.var()/n:.4f} (1.25)  "
              f"KS vs chi2-bar mixture p={stats.kstest(gi, lambda x: sum(stats.binom.pmf(k, n, 0.5) * stats.chi2.cdf(x, k) if k > 0 else stats.binom.pmf(0, n, .5) for k in range(n + 1))).pvalue:.3g}")
