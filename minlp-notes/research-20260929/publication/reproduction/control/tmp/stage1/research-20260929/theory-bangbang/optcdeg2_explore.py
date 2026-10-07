"""Float screening (not rigorous) for a quadratic-in-v discrete calibration of optcdeg2.

S_t(y, v) = py_t y + pv_t v + (q_t / 2) (v - vh_t)^2,
with (py, pv) the discrete costates of the bang-bang primal point and q_t a
stage-dependent curvature. For each stage the residual
  rho_t = (h/2) y^2 + S_{t+1}(f_t(y, v, u)) - S_t(y, v)
is minimized over y in R (closed form), v in the rigorous state interval V_t
(dense grid) and u in [-0.2, 0.2] (closed form); the loss of stage t is
rho_t(z^h_t) - min rho_t. The sum of losses is the gap of the calibration.
"""
import json
import sys

import numpy as np

import os as _os  # repository root, from this file's location (no absolute paths)
_REPO = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "../.."))
OI = _REPO + "/research-20260929/open-instances/"
N = 50000
h = 4e-4


def primal(path=None):
    u = np.load(path or (OI + "logs/optcdeg2_primal_u.npy"))
    y = np.empty(N + 1); v = np.empty(N + 1); y[0] = 10.0; v[0] = 0.0
    for t in range(N):
        y[t + 1] = y[t] + h * v[t]
        v[t + 1] = v[t] + h * (u[t] - 0.02 * y[t] - 0.2 * v[t] ** 2)
    v[N] = 0.0
    return u, y, v


def costates(y, v, nu):
    """p_t = grad of the cost-to-go at x_t along the trajectory; p_{v,N} = nu (free, v_N fixed)."""
    py = np.empty(N + 1); pv = np.empty(N + 1)
    py[N] = h * y[N]; pv[N] = nu
    for t in range(N - 1, -1, -1):
        py[t] = h * y[t] + py[t + 1] - 0.02 * h * pv[t + 1]
        pv[t] = h * py[t + 1] + (1 - 0.4 * h * v[t]) * pv[t + 1]
    return py, pv


def fit_nu(y, v, s2):
    a0 = costates(y, v, 0.0)[1][s2 + 1]
    a1 = costates(y, v, 1.0)[1][s2 + 1]
    return -a0 / (a1 - a0)


def design_q(pv, v, s1, s2, kh, kt, s1_ext=0):
    """Curvature q_t: tangent (q = 0) at the switches, growing on the u = -0.2 arcs so that
    the v-curvature of the residual is 2 * kappa * h per stage.
    Head (t <= s1): q_{s1} = 0, backward q_t = q_{t+1} (1 - 0.4 h v_t)^2 - 0.4 h pv_{t+1} - 2 kh h.
    Middle: q = 0. Tail (t > s2): forward q_{t+1} = (q_t + 0.4 h pv_{t+1} + 2 kt h) / (1 - 0.4 h v_t)^2."""
    q = np.zeros(N + 1)
    if kh is not None:
        for t in range(s1 - 1 + s1_ext, -1, -1):
            q[t] = q[t + 1] * (1 - 0.4 * h * v[t]) ** 2 - 0.4 * h * pv[t + 1] - 2 * kh * h
    if kt is not None:
        for t in range(s2 + 1, N):
            q[t + 1] = (q[t] + 0.4 * h * pv[t + 1] + 2 * kt * h) / (1 - 0.4 * h * v[t]) ** 2
    return q


def stage_losses(y, v, u, py, pv, q, Vb, ngrid=801, ts=None):
    ts = np.arange(1, N) if ts is None else ts
    loss = np.zeros(len(ts))
    chunk = 2000
    for c0 in range(0, len(ts), chunk):
        tt = ts[c0:c0 + chunk]
        # grid over v, including the trajectory value
        g = np.linspace(0, 1, ngrid)[None, :]
        V = Vb[tt, 0][:, None] + (Vb[tt, 1] - Vb[tt, 0])[:, None] * g
        V = np.concatenate([V, v[tt][:, None]], axis=1)
        best = None
        for uu in ("lo", "hi", "stat"):
            val = resid_min_y(tt, V, uu, y, v, u, py, pv, q)
            best = val if best is None else np.minimum(best, val)
        at = resid_min_y(tt, v[tt][:, None], "traj", y, v, u, py, pv, q)[:, 0]
        loss[c0:c0 + chunk] = at - best.min(axis=1)
    return loss


def resid_min_y(tt, V, uu, y, v, u, py, pv, q):
    """min over y in R of rho_t at (v = V, control uu); uu in lo, hi, stat (u-stationary, clipped), traj."""
    P1y, P1v, Q1, vh1 = py[tt + 1][:, None], pv[tt + 1][:, None], q[tt + 1][:, None], v[tt + 1][:, None]
    P0y, P0v, Q0, vh0 = py[tt][:, None], pv[tt][:, None], q[tt][:, None], v[tt][:, None]

    def val(U):
        # rho = h/2 y^2 + P1y (y + h V) + P1v W + Q1/2 (W - vh1)^2 - P0y y - P0v V - Q0/2 (V - vh0)^2,
        # W = w0 - 0.02 h y, w0 = V + h (U - 0.2 V^2)
        w0 = V + h * (U - 0.2 * V ** 2)
        a2 = h / 2 + 0.5 * Q1 * (0.02 * h) ** 2
        a1 = P1y - P0y - 0.02 * h * P1v - 0.02 * h * Q1 * (w0 - vh1)
        c = P1y * h * V + P1v * w0 + 0.5 * Q1 * (w0 - vh1) ** 2 - P0v * V - 0.5 * Q0 * (V - vh0) ** 2
        return c - a1 ** 2 / (4 * a2)

    if uu == "lo":
        return val(-0.2)
    if uu == "hi":
        return val(0.2)
    if uu == "traj":
        return val(u[tt][:, None])
    # stationary u (only meaningful when convex in u): numeric check on a u grid
    best = None
    for U in np.linspace(-0.2, 0.2, 9):
        x = val(U)
        best = x if best is None else np.minimum(best, x)
    return best


def main():
    import os
    u, y, v = primal(os.environ.get("UFILE"))
    s1, s2 = 3091, 47290
    nu = fit_nu(y, v, s2)
    py, pv = costates(y, v, nu)
    lam = np.load(OI + "logs/optcdeg2_lam.npy")
    Vb = np.load(OI + "logs/optcdeg2_vbounds.npy")
    out = dict(nu=nu, pv_s1p1=pv[s1 + 1], pv_s2p1=pv[s2 + 1], pv_s1=pv[s1], pv_s1p2=pv[s1 + 2],
               max_diff_vs_old_lam=float(np.max(np.abs(pv[1:N + 1] + lam))))
    J = h / 2 * np.sum(y ** 2)
    out["J"] = J
    print(json.dumps(out), flush=True)
    configs = [("affine", None, None)] + [(f"kh={kh},kt={kt}", kh, kt) for kh, kt in
                                          [(None, 0.02), (None, 0.05), (None, 0.2), (0.5, 0.05), (1.0, 0.05), (3.0, 0.05), (0.1, 0.01), (0.02, 0.002), (0.0, 0.0)]]
    if len(sys.argv) > 1:
        configs = configs[:int(sys.argv[1])]
    for name, kh, kt in configs:
        q = design_q(pv, v, s1, s2, kh, kt)
        loss = stage_losses(y, v, u, py, pv, q, Vb)
        t = np.arange(1, N)
        rec = dict(cfg=name, total_loss=float(loss.sum()), head=float(loss[t <= s1].sum()),
                   middle=float(loss[(t > s1) & (t <= s2)].sum()), tail=float(loss[t > s2].sum()),
                   worst_t=int(t[np.argmax(loss)]), worst=float(loss.max()), q0=float(q[0]), qN=float(q[N]),
                   neg_losses=float(loss.min()))
        print(json.dumps(rec), flush=True)


if __name__ == "__main__":
    main()
