"""Evidence for Conjecture 3.3: largest NNLS coefficient in the
single-wrong-fixing node problems at rho = theta N (upper bounds dropped),
for square (beta = 1) and tall (beta = 2) systems.  20 nodes per instance
(every (N/20)-th coordinate), 4 instances per cell.
Usage: python3 check_node_inactivity.py
"""
import os
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
from scipy.optimize import nnls
from core import instance

theta = 0.25
for beta in (1, 2):
    for N in (50, 100, 200, 400, 800):
        M = beta * N
        mu = []; root = []
        for s in range(4):
            A, y, xs, B, w = instance(N, M, theta * N, s)
            u, _ = nnls(B, -w, maxiter=50 * N)
            root.append(u.max() * np.sqrt(theta * N))
            for i in range(0, N, max(1, N // 20)):
                v = w + 2 * B[:, i]
                u, _ = nnls(np.delete(B, i, axis=1), -v, maxiter=50 * N)
                mu.append(u.max())
        print("beta=%d N=%4d theta=%.2f  node max u: mean %.3f  max %.3f  (u>2 in %d/%d nodes)   root max u(1)=max u*sqrt(rho): mean %.2f"
              % (beta, N, theta, np.mean(mu), np.max(mu), int(np.sum(np.array(mu) > 2)), len(mu), np.mean(root)))
