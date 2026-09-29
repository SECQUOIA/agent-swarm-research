"""Square systems (reviewer): s* = lambda_max(-D; K) versus the coordinate heuristic and the
bottom-eigenvector Rayleigh bounds, and how much of the pencil's top eigenvector lies on the
bottom five eigenvectors of K.  Usage: python3 sdp_square_inspect.py > sdp_square_inspect.out"""
import os
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
from scipy.linalg import eigh

print("Square systems: s* = lambda_max(-D;K) vs heuristics (rho = s^2). N seed | s* | s_coord | s_eig1 (bottom eigvec) | "
      "best of bottom-5 eigvecs | lambda_min*N^2 | top eigvec of pencil: K-energy share on bottom-5 K-modes")
for N in (100, 400, 1600):
    for seed in range(6):
        rng = np.random.default_rng(777 + N + seed)
        H = rng.standard_normal((N, N)); xs = rng.choice([-1., 1.], N); w = rng.standard_normal(N)
        K = H.T @ H / N; d = xs * (H.T @ w) / np.sqrt(N)
        s, X = eigh(-np.diag(d), K, subset_by_index=[N - 1, N - 1]); s = s[0]; x = X[:, 0]
        lam, V = np.linalg.eigh(K)
        sc = np.max(-d * np.diag(np.linalg.inv(K)))
        vals = [-(V[:, k] ** 2) @ d / lam[k] for k in range(5)]
        c = V.T @ x; e = lam * c ** 2; part = e[:5].sum() / e.sum()
        print(f"{N} {seed} | {s:.3e} | {sc:.3e} | {vals[0]:+.3e} | {max(vals):.3e} | {lam[0]*N**2:.3f} | {part:.3f}")
