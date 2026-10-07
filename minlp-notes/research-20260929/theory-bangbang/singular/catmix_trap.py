"""COPS catmix (trapezoidal transcription) in the projective coordinate:
(a) the smooth ("singular-like") KKT point, which is a saddle, versus the
chattering optimum stored in open-instances-wave2/cops/logs; comparison of
the saddle's negative reduced-Hessian eigenvalue and of the chattering gain
with the predictions from the accessory symbol f(pi) (catmix_schemes.py);
(b) float screening of stage-wise calibration families on the chattering
optimum: affine (costate) and quadratic (maximal quadratic-model recursion).

Reduced form (exact): y_i = Q(u_i) x_i, y_{i+1} = C(u_{i+1}) y_i with the
Cayley map C(u) = (I - h/2 A(u))^{-1} (I + h/2 A(u)); theta = y2/(y1+y2),
log(J+1) = sum_{i=1}^{N-1} log c(theta_{i-1}, u_i) + log p(theta_{N-1}, u_N),
theta_0 = h u_0 / 2, c = (1,1) C(u) (1-theta, theta)^T,
p = (1,1) P(u)^{-1} (1-theta, theta)^T, P(u) = I - h/2 A(u).
Usage: python3 catmix_trap.py N [N ...]
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[3])

import json
import sys
import time

import numpy as np
from scipy.optimize import minimize

COPS = (_PUBLIC_REPO + '/research-20260929/open-instances-wave2/cops/logs/catmix%d_u.npy')


def _analytic(N):
    """numpy functions for F, L = log c, T = log p and their first partials."""
    import sympy as sp
    th, u = sp.symbols("th u")
    h = sp.Rational(1, N)
    A = sp.Matrix([[-u, 10 * u], [u, -1 - 9 * u]])
    P = sp.eye(2) - h / 2 * A
    Q = sp.eye(2) + h / 2 * A
    yv = sp.Matrix([1 - th, th])
    z = P.inv() * (Q * yv)
    c = z[0] + z[1]
    F = z[1] / c
    L = sp.log(c)
    wv = P.inv() * yv
    T = sp.log(wv[0] + wv[1])
    exprs = [F, sp.diff(F, th), sp.diff(F, u), L, sp.diff(L, th), sp.diff(L, u),
             sp.diff(T, th), sp.diff(T, u)]
    return sp.lambdify((th, u), exprs, "numpy")


class Red:
    def __init__(self, N):
        self.N = N
        self.h = 1.0 / N
        self._an = _analytic(N)

    def mats(self, u):
        """elements of P(u) = I - h/2 A(u) and Qm = I + h/2 A(u) (vectorized)."""
        a = self.h / 2
        # A(u) = [[-u, 10u], [u, -1 - 9u]]
        P11, P12, P21, P22 = 1 + a * u, -10 * a * u, -a * u, 1 + a * (1 + 9 * u)
        Q11, Q12, Q21, Q22 = 1 - a * u, 10 * a * u, a * u, 1 - a * (1 + 9 * u)
        return (P11, P12, P21, P22), (Q11, Q12, Q21, Q22)

    def step(self, th, u):
        """returns (F, log c) for theta -> theta' under C(u)."""
        (P11, P12, P21, P22), (Q11, Q12, Q21, Q22) = self.mats(u)
        y1, y2 = 1 - th, th
        z1, z2 = Q11 * y1 + Q12 * y2, Q21 * y1 + Q22 * y2
        det = P11 * P22 - P12 * P21
        w1 = (P22 * z1 - P12 * z2) / det
        w2 = (-P21 * z1 + P11 * z2) / det
        c = w1 + w2
        return w2 / c, np.log(c)

    def term(self, th, u):
        (P11, P12, P21, P22), _ = self.mats(u)
        y1, y2 = 1 - th, th
        det = P11 * P22 - P12 * P21
        w1 = (P22 * y1 - P12 * y2) / det
        w2 = (-P21 * y1 + P11 * y2) / det
        return np.log(w1 + w2)

    def simulate(self, u):
        N = self.N
        th = np.zeros(N)
        th[0] = self.h / 2 * u[0]
        cost = 0.0
        for i in range(1, N):
            th[i], lc = self.step(th[i - 1], u[i])
            cost += lc
        cost += self.term(th[N - 1], u[N])
        return th, cost

    def J(self, u):
        return np.exp(self.simulate(u)[1]) - 1

    def grad_logJ(self, u):
        """gradient of log(J+1) by the discrete adjoint with analytic partials."""
        N = self.N
        th, cost = self.simulate(u)
        g = np.zeros(N + 1)
        F, Ft, Fu, L, Lt, Lu, Tt, Tu = self._an(th[N - 1], u[N])
        g[N] = Tu
        q = Tt
        for i in range(N - 1, 0, -1):
            F, Ft, Fu, L, Lt, Lu, _, _ = self._an(th[i - 1], u[i])
            g[i] = Lu + q * Fu
            q = Lt + q * Ft
        g[0] = q * self.h / 2
        return cost, g

    def grad_logJ_fd(self, u, eps=1e-7):
        """gradient of log(J+1) w.r.t. u by the discrete adjoint with
        central-difference partials of step/term (accurate to ~1e-12)."""
        N = self.N
        th, cost = self.simulate(u)
        g = np.zeros(N + 1)
        # terminal
        Tt = (self.term(th[N - 1] + eps, u[N]) - self.term(th[N - 1] - eps, u[N])) / (2 * eps)
        g[N] = (self.term(th[N - 1], u[N] + eps) - self.term(th[N - 1], u[N] - eps)) / (2 * eps)
        q = Tt  # d cost / d theta_{N-1}
        for i in range(N - 1, 0, -1):
            Fp, Lp = self.step(th[i - 1] + eps, u[i])
            Fm, Lm = self.step(th[i - 1] - eps, u[i])
            Fu, Lu = self.step(th[i - 1], u[i] + eps)
            Fd, Ld = self.step(th[i - 1], u[i] - eps)
            g[i] = (Lu - Ld) / (2 * eps) + q * (Fu - Fd) / (2 * eps)
            q = (Lp - Lm) / (2 * eps) + q * (Fp - Fm) / (2 * eps)
        g[0] = q * self.h / 2
        return cost, g


def smooth_kkt_as(R, outer=6):
    """smooth_kkt with a simple active-set loop: free controls that end at or
    beyond a bound are fixed there and Newton is rerun."""
    N = R.N
    u, cost, g, free, ev, Hm = smooth_kkt(R)
    for ot in range(outer):
        bad = [j for j in free if u[j] <= 1e-12 or u[j] >= 1 - 1e-12]
        if not bad and np.max(np.abs(g[free])) < 1e-14:
            break
        for j in bad:
            u[j] = 0.0 if u[j] <= 0.5 else 1.0
        free = np.array([j for j in free if j not in bad])
        u, cost, g, free, ev, Hm = smooth_kkt(R, u0=u, free0=free)
    return u, cost, g, free, ev, Hm


def smooth_kkt(R, iters=60, u0=None, free0=None):
    """KKT point with the continuous (bang-singular-bang) structure.  Free set:
    the arc stages of the stored chattering optimum (first stage below 1 to
    last stage above 0); start: pairwise averages of the chattering controls;
    damped Newton on grad = 0 over the free set (finite-difference Hessian of
    the analytic gradient).  The result is a saddle when the accessory symbol
    of the scheme is negative at the alternating frequency."""
    N = R.N
    uc = np.load(COPS % N)
    i0 = int(np.argmax(uc < 1 - 1e-9))
    i1 = int(np.max(np.where(uc > 1e-9)[0]))
    free = np.arange(i0, i1 + 1)
    u = uc.copy()
    for j in range(i0, i1, 2):
        m = 0.5 * (uc[j] + uc[j + 1])
        u[j] = u[j + 1] = m
    u[i1] = uc[i1]
    if u0 is not None:
        u, free = u0.copy(), np.array(free0)

    def gfree(v):
        return R.grad_logJ(v)[1][free]

    for it in range(iters):
        g = gfree(u)
        Hm = np.zeros((len(free), len(free)))
        e = 1e-6
        for jj, j in enumerate(free):
            up, um = u.copy(), u.copy()
            up[j] += e
            um[j] -= e
            Hm[:, jj] = (gfree(up) - gfree(um)) / (2 * e)
        Hm = (Hm + Hm.T) / 2
        du = np.linalg.solve(Hm, -g)
        lam = 1.0
        n0 = np.linalg.norm(g)
        while lam > 1e-6:
            un = u.copy()
            un[free] += lam * du
            un[free] = np.clip(un[free], -1e-3, 1 + 1e-3)
            if np.linalg.norm(gfree(un)) < n0 * (1 - 1e-4 * lam) + 1e-15:
                break
            lam /= 2
        u = un
        if np.max(np.abs(lam * du)) < 1e-13 or np.linalg.norm(gfree(u)) < 1e-14:
            break
    cost, g = R.grad_logJ(u)
    ev = np.linalg.eigvalsh(Hm)
    return u, cost, g, free, ev, Hm


def main():
    out = []
    for N in [int(v) for v in sys.argv[1:]]:
        t0 = time.time()
        R = Red(N)
        uc = np.load(COPS % N)
        _, logc = R.simulate(uc)
        Jc = np.exp(logc) - 1
        us, logs_, g, free, ev, Hm = smooth_kkt_as(R)
        Js = np.exp(logs_) - 1
        # eigenvector of the most negative eigenvalue: alternation check
        w, V = np.linalg.eigh(Hm)
        v = V[:, 0]
        alt = np.mean(np.sign(v[1:]) != np.sign(v[:-1]))
        rec = dict(N=N, J_chatter=Jc, J_smooth=Js, dJ=Js - Jc, n_free_smooth=len(free),
                   free_range=[int(free[0]), int(free[-1])],
                   smooth_free_u=[float(us[free].min()), float(us[free].max())],
                   max_grad_free=float(np.max(np.abs(g[free]))),
                   hess_min_eig_logJ=float(ev[0]), hess_min_eig_J=float(ev[0] * (Js + 1)),
                   n_neg_eig=int(np.sum(ev < 0)), sign_alternation_of_min_eigvec=float(alt),
                   seconds=time.time() - t0)
        print(json.dumps(rec), flush=True)
        out.append(rec)
        np.save("logs/catmix%d_smooth_u.npy" % N, us)
    return out


if __name__ == "__main__":
    main()
