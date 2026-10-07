"""Two-state bang-bang example family used in extension-n2.md.

Continuous problem (control-affine, scalar control, n = 2):
    x1' = x2,  x2' = u,  u in [-1, 1],  x(0) = (x10, x20),  horizon T,
    J = int_0^T [ l0(x) + l1(x) u ] dt + Phi(x(T)),
    l0 = e x2 + (q/2) x1^2 - (c/2) x2^2,   l1 = k1 x1 + k2 x2,
    Phi = -a x1 + (rho/2) x2^2 + (nu/4) x2^4.
So b = (0, 1) is constant, the costate switching function is sigma = k1 x1 + k2 x2 + psi2,
and its state gradient at the switch is -w with w = -(k1, k2) != 0.

Everything on an arc with constant control is polynomial in t, so states, costates, the
switching function and the cost are computed exactly with numpy Polynomials (float
coefficients).  One-switch controls u = ua on [0, th), ub on [th, T].
"""
from dataclasses import dataclass, replace

import numpy as np
from numpy.polynomial import Polynomial as Poly
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

B = np.array([0.0, 1.0])
A = np.array([[0.0, 1.0], [0.0, 0.0]])


@dataclass(frozen=True)
class Par:
    T: float = 2.0
    x10: float = 0.0
    x20: float = 0.0
    e: float = 0.0
    q: float = 0.0
    c: float = 0.0
    k1: float = 0.0
    k2: float = 0.0
    a: float = 1.0
    rho: float = 1.0
    nu: float = 0.0
    ua: float = 1.0
    ub: float = -1.0

    @property
    def w(self):
        return -np.array([self.k1, self.k2])

    @property
    def Hxx(self):  # l1 is linear and b constant, so H_xx does not depend on u (N = 0)
        return np.diag([self.q, -self.c])

    def Phi(self, x1, x2):
        return -self.a * x1 + 0.5 * self.rho * x2 ** 2 + 0.25 * self.nu * x2 ** 4

    def dPhi(self, x1, x2):
        return np.array([-self.a, self.rho * x2 + self.nu * x2 ** 3])

    def Phixx(self, x1, x2):
        return np.diag([0.0, self.rho + 3.0 * self.nu * x2 ** 2])


def arcs(p, th):
    """State polynomials on [0, th] (u = ua) and [th, T] (u = ub), in absolute time."""
    t = Poly([0.0, 1.0])
    x2a = p.x20 + p.ua * t
    x1a = p.x10 + p.x20 * t + 0.5 * p.ua * t ** 2
    x1s, x2s = x1a(th), x2a(th)
    x2b = x2s + p.ub * (t - th)
    x1b = x1s + x2s * (t - th) + 0.5 * p.ub * (t - th) ** 2
    return (x1a, x2a), (x1b, x2b)


def solve_arcs(p, th):
    """States, costates and switching function on both arcs; cost J(th)."""
    (x1a, x2a), (x1b, x2b) = arcs(p, th)
    T = p.T
    xT = (x1b(T), x2b(T))
    pT = p.dPhi(*xT)
    out = {}
    # costates backward: psi1' = -(q x1 + k1 u), psi2' = -(e - c x2 + k2 u + psi1)
    segs = [("b", x1b, x2b, p.ub, th, T), ("a", x1a, x2a, p.ua, 0.0, th)]
    end = pT
    for name, x1, x2, u, t0, t1 in segs:
        d1 = -(p.q * x1 + p.k1 * u)
        I1 = d1.integ()
        psi1 = end[0] + I1 - I1(t1)
        d2 = -(p.e - p.c * x2 + p.k2 * u + psi1)
        I2 = d2.integ()
        psi2 = end[1] + I2 - I2(t1)
        sig = p.k1 * x1 + p.k2 * x2 + psi2
        run = (p.e * x2 + 0.5 * p.q * x1 ** 2 - 0.5 * p.c * x2 ** 2 + (p.k1 * x1 + p.k2 * x2) * u).integ()
        out[name] = dict(x1=x1, x2=x2, u=u, psi1=psi1, psi2=psi2, sig=sig, t0=t0, t1=t1,
                         run=run(t1) - run(t0))
        end = (psi1(t0), psi2(t0))
    out["J"] = out["a"]["run"] + out["b"]["run"] + p.Phi(*xT)
    out["xT"] = np.array(xT)
    out["th"] = th
    return out


def J_of(p, th):
    return solve_arcs(p, th)["J"]


def find_switch(p, lo=1e-6, hi=None):
    """Switching time th in (lo, hi) with sigma(th) = 0 (brentq on the switching function)."""
    hi = p.T - 1e-6 if hi is None else hi
    f = lambda th: solve_arcs(p, th)["a"]["sig"](th)
    grid = np.linspace(lo, hi, 401)
    vals = np.array([f(g) for g in grid])
    roots = []
    for i in range(len(grid) - 1):
        if vals[i] == 0.0 or vals[i] * vals[i + 1] < 0:
            roots.append(brentq(f, grid[i], grid[i + 1], xtol=1e-15, rtol=1e-15, maxiter=200))
    return roots


def pmp_check(p, sol, npts=4001):
    """Largest violation of the PMP sign rule on both arcs (u = -1 where sigma > 0)."""
    viol = 0.0
    for name in ("a", "b"):
        d = sol[name]
        tt = np.linspace(d["t0"], d["t1"], npts)
        s = d["sig"](tt)
        # u = +1 needs sigma <= 0; u = -1 needs sigma >= 0
        v = np.maximum(0.0, s) if d["u"] > 0 else np.maximum(0.0, -s)
        viol = max(viol, float(v.max()))
    return viol


def lyapunov_Q(p, sol, eps=0.0, t_eval=None):
    """Q' = -(A^T Q + Q A + H_xx) + 2 eps I backward from Q(T) = Phi_xx - 2 eps I on (tau, T]."""
    QT = p.Phixx(*sol["xT"]) - 2 * eps * np.eye(2)
    Hxx = p.Hxx

    def rhs(t, y):
        Q = y.reshape(2, 2)
        return (-(A.T @ Q + Q @ A + Hxx) + 2 * eps * np.eye(2)).ravel()

    r = solve_ivp(rhs, (p.T, sol["th"]), QT.ravel(), rtol=1e-12, atol=1e-14, dense_output=True)
    return r


def switch_quantities(p, sol, eps=0.0):
    """eta_L, beta_L, D, and F''(tau) = D + Delta^2 eta_L (derived in extension-n2.md)."""
    th = sol["th"]
    r = lyapunov_Q(p, sol, eps)
    Qp = r.sol(th).reshape(2, 2)
    beta = Qp @ B - p.w
    eta = float(B @ beta)
    Delta = abs(p.ub - p.ua)
    sdot = sol["a"]["sig"].deriv()(th)
    sdot_b = sol["b"]["sig"].deriv()(th)
    D = abs(sdot) * Delta
    return dict(th=th, Qplus=Qp, beta_L=beta, eta_L=eta, D=D, sigdot=sdot, sigdot_b=sdot_b,
                Fpp_formula=D + Delta ** 2 * eta, Delta=Delta)


def Fpp_fd(p, th, hs=(1e-2, 5e-3, 2.5e-3)):
    out = []
    for hh in hs:
        out.append((J_of(p, th + hh) - 2 * J_of(p, th) + J_of(p, th - hh)) / hh ** 2)
    # Richardson on the last two
    return out, (4 * out[-1] - out[-2]) / 3


def singular_riccati_after(p, sol, eps, s_min=1e-14, s_top=None, delta0=None):
    """Maximal solution of the singular Riccati equation on (tau, T]:
        P' = -(A^T P + P A + H_xx) + 2 eps I + (Delta / (2 |sigma(t)|)) beta beta^T,  beta = P b - w,
    backward from P(T) = Phi_xx - 2 eps I.  Integrated in lam = log(t - tau) near tau.
    Returns samples (s, P(tau + s), beta) and a blow-up flag."""
    th = sol["th"]
    sig = sol["b"]["sig"]
    Delta = abs(p.ub - p.ua)
    Hxx = p.Hxx
    w = p.w
    PT = p.Phixx(*sol["xT"]) - 2 * eps * np.eye(2)

    def F(t, P):
        beta = P @ B - w
        lin = -(A.T @ P + P @ A + Hxx) + 2 * eps * np.eye(2)
        if delta0 is not None and t - th > delta0:   # local version: singular term only in the layer
            return lin
        return lin + Delta / (2 * abs(sig(t))) * np.outer(beta, beta)

    # phase 1: t from T down to tau + s_top in plain time
    s_top = min(0.5 * (p.T - th), 0.1) if s_top is None else s_top
    big = 1e8
    ev = lambda t, y: big - np.abs(y).max()
    ev.terminal = True
    r1 = solve_ivp(lambda t, y: F(t, y.reshape(2, 2)).ravel(), (p.T, th + s_top), PT.ravel(),
                   rtol=1e-11, atol=1e-13, events=ev)
    if r1.status == 1:
        return dict(blowup=True, s_blow=float(r1.t_events[0][0] - th), samples=[])
    P1 = r1.y[:, -1]

    # phase 2: lam = log s, dP/dlam = s P'(tau + s)
    def G(lam, y):
        s = np.exp(lam)
        return (s * F(th + s, y.reshape(2, 2))).ravel()

    ev2 = lambda lam, y: big - np.abs(y).max()
    ev2.terminal = True
    lams = np.linspace(np.log(s_top), np.log(s_min), 300)
    r2 = solve_ivp(G, (lams[0], lams[-1]), P1, t_eval=lams, rtol=1e-11, atol=1e-13, events=ev2)
    samples = []
    for lam, y in zip(r2.t, r2.y.T):
        P = y.reshape(2, 2)
        samples.append((float(np.exp(lam)), P, P @ B - w))
    if r2.status == 1:
        # the event time, not the last t_eval grid point (fixed after review: the grid point
        # overstated s_b by up to one log-grid step, e.g. 5.87e-3 instead of 5.754e-3)
        return dict(blowup=True, s_blow=float(np.exp(r2.t_events[0][0])), samples=samples)
    return dict(blowup=False, samples=samples)


def with_(p, **kw):
    return replace(p, **kw)


def continuous_family(p, eps, delta1=None, s_tiny=1e-13):
    """Continuous quadratic calibration Hessians P(t) on [0, T] for the global-model condition (R):
        P' >= -(A^T P + P A + H_xx) + 2 eps I + (Delta / (2|sigma|)) beta beta^T,  beta = P b - w.
    After the switch: the maximal solution P-hat (equality) backward from P(T) = Phi_xx - 2 eps I.
    delta1 = None: keep P-hat down to tau (logarithmic tangency); P(tau) := limit, obtained by the
        rank-one layer formula P-hat(tau + s_tiny) - beta beta^T / eta (exactly tangential).
    delta1 > 0: on (tau, tau + delta1] replace P-hat by the linear-rate construction
        P' = G(P, t) + y y^T / (b.y),  y = v - G b,  v = beta-hat(tau + delta1) / delta1,
        so that P b - w = beta-hat(tau + delta1) (t - tau) / delta1 (Theorem 2 of extension-n2.md).
    Before the switch: equality in (R), backward from P(tau) (beta(tau) = 0).
    Returns a callable P(t) and diagnostics."""
    th = find_switch(p)[0]
    sol = solve_arcs(p, th)
    Delta = abs(p.ub - p.ua)
    w, Hxx, I2 = p.w, p.Hxx, np.eye(2)
    sig_a, sig_b = sol["a"]["sig"], sol["b"]["sig"]

    def G(t, P, sig):
        beta = P @ B - w
        s = abs(sig(t))
        sing = np.outer(beta, beta) * (Delta / (2 * s)) if s > 0 else 0.0 * I2
        return -(A.T @ P + P @ A + Hxx) + 2 * eps * I2 + sing

    kw = dict(rtol=1e-11, atol=1e-13, dense_output=True)
    PT = p.Phixx(*sol["xT"]) - 2 * eps * I2
    segs = []
    t_hat_end = th + (delta1 if delta1 is not None else 0.05)
    r1 = solve_ivp(lambda t, y: G(t, y.reshape(2, 2), sig_b).ravel(), (p.T, t_hat_end), PT.ravel(), **kw)
    assert r1.status == 0
    segs.append((t_hat_end, p.T, r1.sol))
    P1 = r1.y[:, -1].reshape(2, 2)
    diag = dict(th=th)
    if delta1 is None:
        # log-variable integration of P-hat down to tau + s_tiny
        def Glam(lam, y):
            s = np.exp(lam)
            return (s * G(th + s, y.reshape(2, 2), sig_b)).ravel()
        r2 = solve_ivp(Glam, (np.log(t_hat_end - th), np.log(s_tiny)), P1.ravel(), rtol=1e-11, atol=1e-13,
                       dense_output=True)
        assert r2.status == 0
        sol2 = r2.sol
        segs.append((th + s_tiny, t_hat_end, lambda t, f=sol2: f(np.log(np.maximum(np.asarray(t) - th, s_tiny)))))
        Pe = r2.y[:, -1].reshape(2, 2)
        be = Pe @ B - w
        diag["beta_tiny"] = be
        Ptau = Pe - np.outer(be, be) / (B @ be)
    else:
        b1 = P1 @ B - w
        diag["beta_layer_start"] = b1
        v = b1 / delta1

        def Glay(t, y):
            P = y.reshape(2, 2)
            Gm = G(t, P, sig_b)
            yv = v - Gm @ B
            by = B @ yv
            assert by > 0, ("b.y <= 0 in layer", t, by)
            return (Gm + np.outer(yv, yv) / by).ravel()
        r2 = solve_ivp(Glay, (t_hat_end, th + s_tiny), P1.ravel(), **kw)
        assert r2.status == 0, r2.message
        segs.append((th, t_hat_end, r2.sol))
        Ptau = r2.y[:, -1].reshape(2, 2)
        be = Ptau @ B - w
        Ptau = Ptau - np.outer(be, be) / (B @ be) if abs(B @ be) > 0 else Ptau  # remove O(s_tiny) residue
    diag["Ptau"] = Ptau
    diag["beta_tau"] = Ptau @ B - w
    big = 1e6
    ev = lambda t, y: big - np.abs(y).max()
    ev.terminal = True
    r3 = solve_ivp(lambda t, y: G(t, y.reshape(2, 2), sig_a).ravel(), (th - s_tiny, 0.0), Ptau.ravel(),
                   events=ev, **kw)
    diag["pre_blowup"] = (r3.status == 1)
    diag["pre_blowup_t"] = float(r3.t[-1]) if r3.status == 1 else None
    segs.append((0.0, th, r3.sol))

    def Pfun(t):
        t = float(t)
        if abs(t - th) < s_tiny:
            return Ptau
        for lo, hi, f in segs:
            if lo <= t <= hi:
                return np.asarray(f(t)).reshape(2, 2)
        raise ValueError(t)
    return Pfun, diag
