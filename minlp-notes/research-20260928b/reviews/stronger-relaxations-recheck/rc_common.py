"""Shared helpers for the recheck scripts (own code; mirrors the documented generators only).
Threads are pinned to 1 before NumPy is imported."""
import os
for _v in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "RAYON_NUM_THREADS",
           "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"]:
    os.environ[_v] = "1"
import numpy as np

DATA = os.path.join(os.path.dirname(__file__), "..", "..", "bb-complexity", "sparse-regression",
                    "stronger-relaxations", "data")


def make_nested(n, k, pmax, p, seed, b=1.0, sigma=0.5):
    """Nested design of Section 7.2 (same RNG call order as the documented generator)."""
    rng = np.random.default_rng(seed)
    Xf = rng.standard_normal((n, pmax))
    beta = np.zeros(pmax); beta[:k] = b * rng.choice([-1.0, 1.0], k)
    y = Xf @ beta + sigma * rng.standard_normal(n)
    lam = 1.5 * sigma * np.sqrt(2 * n * np.log(200)) / b
    return Xf[:, :p], y, lam, tuple(range(k))


def make_pt(n, p, k, seed, tau0=1.5, b=1.0, sigma=0.5):
    """Parent-note family of Section 7.5 (same RNG call order as [PT] core.instance)."""
    rng = np.random.default_rng(seed)
    X = rng.standard_normal((n, p))
    S = np.sort(rng.choice(p, k, replace=False))
    beta = np.zeros(p); beta[S] = b * rng.choice([-1.0, 1.0], k)
    y = X @ beta + sigma * rng.standard_normal(n)
    lam = tau0 * sigma * np.sqrt(2 * n * np.log(p)) / b
    return X, y, float(lam), tuple(S.tolist())


def ridge(X, y, lam, S):
    S = list(S)
    XS = X[:, S]
    bS = np.linalg.solve(XS.T @ XS + lam * np.eye(len(S)), XS.T @ y)
    r = y - XS @ bS
    return float(r @ r + lam * bS @ bS), bS, r


def pwe_ratio(X, y, lam, S):
    """max_{l not in S} |x_l' r_S| / (lam min_i |beta^S_i|)  (PT Corollary 2.4: root exact iff <= 1)."""
    _, bS, r = ridge(X, y, lam, S)
    a = np.abs(X.T @ r)
    mask = np.ones(X.shape[1], bool); mask[list(S)] = False
    return float(a[mask].max() / (lam * np.abs(bS).min()))
