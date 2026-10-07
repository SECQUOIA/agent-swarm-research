"""optcdeg2: model data, MINLPLib solution loader, adjoint (costate) computation.
Model (checked in optcdeg2_check.py):
  min (h/2) sum_{t=0}^{N} y_t^2
  y_{t+1} = y_t + h v_t,  v_{t+1} = v_t + h (u_t - 0.02 y_t - 0.2 v_t^2),  t = 0..N-1
  y_0 = 10, v_0 = 0, v_N = 0, v_t >= -1, |u_t| <= 0.2, h = 4e-4, N = 50000."""
import numpy as np
N = 50000; h = 4e-4

def osil_index_maps():
    # 0-based OSIL variable indices
    u_idx = np.concatenate([np.arange(0, N - 1), [N]])          # x2..x50000, x50002
    y_idx = np.arange(N + 1, 2 * N + 2)                          # x50003..x100003
    v_idx = np.concatenate([np.arange(2 * N + 2, 3 * N + 2), [N - 1]])  # x100004..x150003, x50001
    return u_idx, y_idx, v_idx

def load_minlplib(fname="minlplib_sol/optcdeg2.p1.sol"):
    from osil_eval import load
    I = load("optcdeg2"); idx = {nm: j for j, nm in enumerate(I["names"])}
    x = np.zeros(len(I["names"]))
    for line in open(fname):
        p = line.split()
        if len(p) >= 2 and p[0] in idx: x[idx[p[0]]] = float(p[1])
    ui, yi, vi = osil_index_maps()
    return x[ui], x[yi], x[vi]

def to_osil(u, y, v):
    ui, yi, vi = osil_index_maps()
    x = np.zeros(3 * N + 2); x[ui] = u; x[yi] = y; x[vi] = v
    return x

def costates(y, v, lamN1):
    """Backward adjoint recursion given lambda_{N-1}; returns mu, lam (length N)."""
    mu = np.zeros(N); lam = np.zeros(N)
    mu[N - 1] = -h * y[N]; lam[N - 1] = lamN1
    for t in range(N - 1, 0, -1):
        mu[t - 1] = mu[t] - h * y[t] - 0.02 * h * lam[t]
        lam[t - 1] = lam[t] + h * mu[t] - 0.4 * h * lam[t] * v[t]
    return mu, lam
