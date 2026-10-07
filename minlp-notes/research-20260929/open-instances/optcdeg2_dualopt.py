"""optcdeg2: numerical (float) maximization of the Lagrangian dual function over the
multipliers of the head window, starting from the KKT multipliers. The resulting
multipliers are then evaluated rigorously by optcdeg2_bound.dual_value / blockdp code."""
import numpy as np, sys, time
from scipy.optimize import minimize
from optcdeg2_common import N, h

vb = np.load("logs/optcdeg2_vbounds.npy")
VLO, VHI = vb[:, 0], vb[:, 1]

def dual_and_grad(mu, lam):
    # y terms
    b = np.empty(N + 1); b[1:N] = mu[:-1] - mu[1:] + 0.02 * h * lam[1:]; b[N] = mu[N - 1]
    yhat = np.zeros(N + 1); yhat[0] = 10.0; yhat[1:] = -b[1:] / h
    d = h / 2 * 100 - 10 * mu[0] + 0.02 * h * lam[0] * 10 - np.sum(b[1:] ** 2) / (2 * h)
    uhat = 0.2 * np.sign(lam)
    d -= 0.2 * h * np.sum(np.abs(lam))
    A = 0.2 * h * lam[1:]; B = np.concatenate([[0.0], lam[:-1]])[1:] - lam[1:] - h * mu[1:]
    lo, hi = VLO[1:N], VHI[1:N]
    with np.errstate(divide="ignore", invalid="ignore"):
        st = np.where(A > 0, np.clip(-B / (2 * A), lo, hi), lo)
    cand = np.stack([lo, hi, st])
    vals = A * cand ** 2 + B * cand
    k = np.argmin(vals, axis=0)
    vh = cand[k, np.arange(N - 1)]
    d += np.sum(vals[k, np.arange(N - 1)])
    vhat = np.zeros(N + 1); vhat[1:N] = vh
    gmu = yhat[1:] - yhat[:-1] - h * vhat[:-1]
    glam = vhat[1:] - vhat[:-1] - h * uhat + 0.02 * h * yhat[:-1] + 0.2 * h * vhat[:-1] ** 2
    return d, gmu, glam

if __name__ == "__main__":
    W = int(sys.argv[1]) if len(sys.argv) > 1 else 3400
    mu0, lam0 = np.load("logs/optcdeg2_mu.npy"), np.load("logs/optcdeg2_lam.npy")
    d0 = dual_and_grad(mu0, lam0)[0]; print("start dual (float)", d0, flush=True)
    idx_tail = np.arange(46800, N)
    def unpack(z):
        mu, lam = mu0.copy(), lam0.copy()
        mu[:W] = z[:W]; lam[:W] = z[W:2 * W]
        mu[idx_tail] = z[2 * W:2 * W + len(idx_tail)]; lam[idx_tail] = z[2 * W + len(idx_tail):]
        return mu, lam
    def f(z):
        mu, lam = unpack(z)
        d, gm, gl = dual_and_grad(mu, lam)
        g = np.concatenate([gm[:W], gl[:W], gm[idx_tail], gl[idx_tail]])
        return -d, -g
    z0 = np.concatenate([mu0[:W], lam0[:W], mu0[idx_tail], lam0[idx_tail]])
    t = time.time()
    res = minimize(f, z0, jac=True, method="L-BFGS-B", options=dict(maxiter=int(sys.argv[2]) if len(sys.argv) > 2 else 3000, maxcor=50))
    mu, lam = unpack(res.x)
    print("opt dual (float)", -res.fun, res.message, res.nit, time.time() - t, flush=True)
    np.save("logs/optcdeg2_mu_opt.npy", mu); np.save("logs/optcdeg2_lam_opt.npy", lam)
