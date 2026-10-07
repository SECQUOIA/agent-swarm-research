"""Window law on the optcdeg2 transcription family (float screening, not rigorous).

Problem family: T = 20, h = T/N, the optcdeg2 dynamics and cost; N = 6250 ... 100000
(N = 50000 is the MINLPLib instance). For each N:
  1. the bang-bang discrete KKT point (fractional controls at two switching stages) is found by
     secant iterations (v_N = 0 and p_v = 0 at both fractional stages);
  2. stage losses rho_t(z_t) - min_{Omega_t} rho_t are screened (closed-form minimization in y,
     dense grid in v over the rigorous-style box V_t, closed form in u) for four families
       S_t = py_t y + pv_t v + q_t/2 (v - v_t)^2:
     A  affine (q = 0): the costate calibration;
     B  tangential: q = 0 at both switches, growth 2 kappa h per stage on the u = -0.2 arcs;
     C  non-tangential: B plus a constant offset QBAR on all stages after the first switch;
     D  O(h) tangency defect: B with the tail profile shifted K0 stages earlier.
   A stage "fails" if its loss exceeds 1e-12.
The state boxes V_t are recomputed for each N by forward-backward interval propagation in
float (sufficient for screening).
"""
import json
import sys
import time

import numpy as np

T = 20.0


def simulate(u, h):
    N = len(u)
    y = np.empty(N + 1); v = np.empty(N + 1); y[0] = 10.0; v[0] = 0.0
    for t in range(N):
        y[t + 1] = y[t] + h * v[t]
        v[t + 1] = v[t] + h * (u[t] - 0.02 * y[t] - 0.2 * v[t] ** 2)
    return y, v


def controls(s1, s2, N):
    u = np.full(N, -0.2)
    k1, f1 = int(s1), s1 - int(s1); k2, f2 = int(s2), s2 - int(s2)
    u[k1 + 1:k2] = 0.2
    u[k1] = -0.2 + 0.4 * (1 - f1)
    u[k2] = 0.2 - 0.4 * (1 - f2)
    return u


def secant(f, a, b, tol=1e-13, it=60):
    fa, fb = f(a), f(b)
    for _ in range(it):
        if fb == fa:
            break
        c = b - fb * (b - a) / (fb - fa)
        a, fa, b, fb = b, fb, c, f(c)
        if abs(fb) < tol or abs(b - a) < 1e-11:
            break
    return b


def costates(y, v, nu, h):
    N = len(y) - 1
    py = np.empty(N + 1); pv = np.empty(N + 1)
    py[N] = h * y[N]; pv[N] = nu
    for t in range(N - 1, -1, -1):
        py[t] = h * y[t] + py[t + 1] - 0.02 * h * pv[t + 1]
        pv[t] = h * py[t + 1] + (1 - 0.4 * h * v[t]) * pv[t + 1]
    return py, pv


def kkt_point(N):
    h = T / N
    s1 = 3091.3954427737285 * N / 50000.0
    s2g = 47290.73782103672 * N / 50000.0

    def solve_s2(s1_):
        return secant(lambda s: simulate(controls(s1_, s, N), h)[1][N], s2g, s2g + 0.5)

    def resid(s1_):
        s2 = solve_s2(s1_)
        y, v = simulate(controls(s1_, s2, N), h)
        v[N] = 0.0
        k1, k2 = int(s1_), int(s2)
        a0 = costates(y, v, 0.0, h)[1]; a1 = costates(y, v, 1.0, h)[1]
        nu = -a0[k2 + 1] / (a1[k2 + 1] - a0[k2 + 1])
        return (a0 + nu * (a1 - a0))[k1 + 1]
    s1 = secant(resid, s1, s1 + 0.01, tol=1e-12)
    s2 = solve_s2(s1)
    u = controls(s1, s2, N)
    y, v = simulate(u, h)
    v[N] = 0.0
    k1, k2 = int(s1), int(s2)
    a0 = costates(y, v, 0.0, h)[1]; a1 = costates(y, v, 1.0, h)[1]
    nu = -a0[k2 + 1] / (a1[k2 + 1] - a0[k2 + 1])
    py, pv = costates(y, v, nu, h)
    return dict(N=N, h=h, u=u, y=y, v=v, py=py, pv=pv, k1=k1, k2=k2, s1=s1, s2=s2, nu=nu,
                J=h / 2 * np.sum(y ** 2), kkt1=pv[k1 + 1], kkt2=pv[k2 + 1])


def vbounds(N, h, passes=1):
    """Forward-backward interval propagation of v (float; for screening only)."""
    Ylo = np.full(N + 1, -1e6); Yhi = np.full(N + 1, 1e6); Vlo = np.full(N + 1, -1.0); Vhi = np.full(N + 1, 1e6)
    Ylo[0] = Yhi[0] = 10.0; Vlo[0] = Vhi[0] = 0.0; Vlo[N] = Vhi[N] = 0.0
    g = lambda x: x - 0.2 * h * x * x  # noqa: E731
    ginv = lambda z: 2 * z / (1 + np.sqrt(1 - 0.8 * h * z))  # noqa: E731
    for _ in range(passes):
        for t in range(N):
            Vlo[t + 1] = max(Vlo[t + 1], g(Vlo[t]) - 0.2 * h - 0.02 * h * Yhi[t])
            Vhi[t + 1] = min(Vhi[t + 1], g(Vhi[t]) + 0.2 * h - 0.02 * h * Ylo[t])
            Ylo[t + 1] = max(Ylo[t + 1], Ylo[t] + h * Vlo[t]); Yhi[t + 1] = min(Yhi[t + 1], Yhi[t] + h * Vhi[t])
        for t in range(N - 1, 0, -1):
            Ylo[t] = max(Ylo[t], Ylo[t + 1] - h * Vhi[t]); Yhi[t] = min(Yhi[t], Yhi[t + 1] - h * Vlo[t])
            Vlo[t] = max(Vlo[t], ginv(Vlo[t + 1] - 0.2 * h + 0.02 * h * Ylo[t]))
            Vhi[t] = min(Vhi[t], ginv(Vhi[t + 1] + 0.2 * h + 0.02 * h * Yhi[t]))
    return Vlo, Vhi


def q_profile(K, kind, kh=1.0, kt=0.05, qbar=0.05, k0=5):
    N, h, v, pv, k1, k2 = K["N"], K["h"], K["v"], K["pv"], K["k1"], K["k2"]
    q = np.zeros(N + 1)
    if kind == "A":
        return q
    for t in range(k1 - 1, -1, -1):
        q[t] = q[t + 1] * (1 - 0.4 * h * v[t]) ** 2 - 0.4 * h * pv[t + 1] - 2 * kh * h
    start = k2 + 1 - (k0 if kind == "D" else 0)
    for t in range(start, N):
        q[t + 1] = (q[t] + 0.4 * h * pv[t + 1] + 2 * kt * h) / (1 - 0.4 * h * v[t]) ** 2
    if kind == "C":
        q[k1 + 1:] += qbar
    return q


def losses(K, q, Vlo, Vhi, ngrid=1601):
    N, h, y, v, u, py, pv = K["N"], K["h"], K["y"], K["v"], K["u"], K["py"], K["pv"]
    ts = np.arange(1, N)
    out = np.empty(len(ts))
    for c0 in range(0, len(ts), 2000):
        tt = ts[c0:c0 + 2000]
        g = np.linspace(0, 1, ngrid)[None, :]
        V = Vlo[tt][:, None] + (Vhi[tt] - Vlo[tt])[:, None] * g
        V = np.concatenate([V, v[tt][:, None]], axis=1)
        P1y, P1v, Q1, c1 = py[tt + 1][:, None], pv[tt + 1][:, None], q[tt + 1][:, None], v[tt + 1][:, None]
        P0y, P0v, Q0, c0v = py[tt][:, None], pv[tt][:, None], q[tt][:, None], v[tt][:, None]

        def val(Vx, U):
            w0 = Vx + h * (U - 0.2 * Vx ** 2)
            a2 = h / 2 + 0.5 * Q1 * (0.02 * h) ** 2
            a1 = P1y - P0y - 0.02 * h * P1v - 0.02 * h * Q1 * (w0 - c1)
            c = P1y * h * Vx + P1v * w0 + 0.5 * Q1 * (w0 - c1) ** 2 - P0v * Vx - 0.5 * Q0 * (Vx - c0v) ** 2
            return c - a1 ** 2 / (4 * a2)
        best = np.minimum.reduce([val(V, U) for U in np.linspace(-0.2, 0.2, 9)])
        at = val(v[tt][:, None], u[tt][:, None])[:, 0]
        out[c0:c0 + 2000] = at - best.min(axis=1)
    return ts, out


def main():
    Ns = [int(a) for a in sys.argv[1:]] or [6250, 12500, 25000, 50000, 100000]
    for N in Ns:
        t0 = time.time()
        K = kkt_point(N)
        Vlo, Vhi = vbounds(N, K["h"])
        rec = dict(N=N, h=K["h"], J=K["J"], s1=K["s1"], s2=K["s2"], kkt1=K["kkt1"], kkt2=K["kkt2"])
        for kind in "ABCD":
            q = q_profile(K, kind)
            ts, L = losses(K, q, Vlo, Vhi)
            fail = ts[L > 1e-12]
            near1 = fail[np.abs(fail - K["k1"]) <= N // 10]
            near2 = fail[np.abs(fail - K["k2"]) <= N // 10]
            rec[kind] = dict(fail=int(len(fail)), fail_near_s1=int(len(near1)), fail_near_s2=int(len(near2)),
                             fail_duration=float(len(fail) * K["h"]), loss=float(L.sum()),
                             fail_range_s2=[int(near2.min() - K["k2"]), int(near2.max() - K["k2"])] if len(near2) else None)
        rec["seconds"] = time.time() - t0
        print(json.dumps(rec), flush=True)
        with open("logs/optcdeg2_family_windows.jsonl", "a") as f:
            f.write(json.dumps(rec) + "\n")


if __name__ == "__main__":
    main()
