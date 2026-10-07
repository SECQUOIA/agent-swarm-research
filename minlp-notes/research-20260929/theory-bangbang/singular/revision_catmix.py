"""Revision checks for singular-arcs.md, Section 5 (COPS catmix, trapezoidal
rule, reduced projective model of catmix_trap.py).  Written after review
round 1 (findings F1, F2, F3).

Part A (symbol, mpmath 50 digits; catmix_schemes.py): for the trapezoidal
  rule at h = 1/100, 1/200, 1/400:
  - f(0), f(pi), f''(pi) of the accessory symbol;
  - check that N(om) := f(om) |e^{i om} - F_theta|^2 is affine in cos(om)
    (n = 1), so f >= 0 on the circle iff f(0) >= 0 and f(pi) >= 0;
  - the exact zero om0 of f near pi, d0 = pi - om0, and the Taylor value
    sqrt(2|f(pi)|/f''(pi)); conjugate-point spacing pi/d0 (stages);
  - predicted number of negative eigenvalues m d0/pi for an arc of m stages.
Part B (stationary 2-cycle, mpmath): per-stage gain of the best 2-periodic
  orbit with controls (v, 0) over the fixed point, against the quadratic
  prediction (1/2) u_s^2 |f(pi)|.
Part C (F1: like-for-like baseline).  The KKT point of catmix_trap.py
  ("smooth" in the first version) oscillates.  Here the baseline is the best
  control that is smooth on the arc: piecewise linear in the stage index with
  knots every s stages (s >= 4 excludes the alternating mode), bang stages as
  in the saved saddle (N = 100, 200) or the stored COPS point (N = 400),
  optionally with free first and last arc stages.  Minimized with L-BFGS-B
  and polished by Newton in the knot space.  Reports J, the gain over the
  chattering point, and (N = 100, 200) the Hessian on the free block at this
  smooth base point: most negative eigenvalue and number of negative
  eigenvalues, against the saved oscillating saddle.
Part D (sympy): eta_L = 1 exactly at the exit junction.
Part E (mpmath): checks of Proposition 3.7 (n = 1 storage criterion) and of
  the transfer matrix of the linearized first-order recursion (Remark 3.9).
Usage: python3 revision_catmix.py [A] [B] [C] [D] [E]   (default: A B C)
"""
import json
import sys
import time

import mpmath as mp
import numpy as np
from scipy.optimize import minimize

import catmix_schemes as S
import catmix_trap as C

mp.mp.dps = 50
T1, T2 = 0.136299034595, 0.725230107592
U_S = 0.227142082708498
J_CHATTER = {100: -0.0480694320309772, 200: -0.0480591455801168, 400: -0.0480565477567615}
J_SADDLE = {100: -0.04806939479831862, 200: -0.04805913591486621}


def symbol_data(N):
    h = mp.mpf(1) / N
    FL = S.scheme("trapezoid", h)
    t, u, q, d = S.fixed_point(FL)
    f = lambda om: S.symbol(d, q, om)
    a = d["Ft"]
    Nn = lambda om: f(om) * abs(mp.expj(om) - a) ** 2
    f0, fpi = f(mp.mpf(0)), f(mp.pi)
    f2 = mp.diff(f, mp.pi, 2)
    # affine-in-cos check at three interior frequencies
    n0, npi = Nn(mp.mpf(0)), Nn(mp.pi)
    aff = max(abs(Nn(om) - (n0 + npi) / 2 - (n0 - npi) / 2 * mp.cos(om)) / abs(n0)
              for om in (mp.pi / 7, mp.pi / 2, 5 * mp.pi / 6))
    c0 = -(n0 + npi) / (n0 - npi)          # N(c0) = 0, c = cos(om)
    om0 = mp.acos(c0) if abs(c0) <= 1 else None
    d0 = mp.pi - om0 if om0 is not None else None
    d0t = mp.sqrt(2 * abs(fpi) / f2)
    return dict(h=h, theta=t, u=u, q=q, d=d, FL=FL, f0=f0, fpi=fpi, f2=f2, aff=aff,
                om0=om0, d0=d0, d0_taylor=d0t, f_at_om0=(f(om0) if om0 is not None else None))


def part_A():
    print("== Part A: trapezoidal accessory symbol (catmix, reduced 1-D)")
    for N in (100, 200, 400):
        s = symbol_data(N)
        h = s["h"]
        print("N=%d f(0)/h^2=%.4e f(pi)/h^3=%.6f f''(pi)/h^3=%.5f  affine-in-cos rel.err=%.1e  "
              "d0 exact=%.5f (f(om0)=%.1e)  d0 Taylor=%.5f  pi/d0=%.3f stages"
              % (N, float(s["f0"] / h ** 2), float(s["fpi"] / h ** 3), float(s["f2"] / h ** 3),
                 float(s["aff"]), float(s["d0"]), float(s["f_at_om0"]), float(s["d0_taylor"]),
                 float(mp.pi / s["d0"])), flush=True)
        for m in {100: (59,), 200: (113, 118), 400: (235, 236)}[N]:
            print("   arc of m=%d stages: predicted negative eigenvalues m d0/pi = %.2f" % (m, float(m * s["d0"] / mp.pi)))


def part_B():
    print("== Part B: stationary 2-cycle (v, 0) versus the fixed point, per stage (log(J+1) units)")
    for N in (100, 200, 400):
        s = symbol_data(N)
        FL, th, u = s["FL"], s["theta"], s["u"]
        Lfix = FL(th, u)[1]

        def cyc(v):
            # theta_a -> (v) -> theta_b -> (0) -> theta_a
            g = lambda ta: FL(FL(ta, v)[0], mp.mpf(0))[0] - ta
            ta = mp.findroot(g, th)
            tb, La = FL(ta, v)
            _, Lb = FL(tb, mp.mpf(0))
            return (La + Lb) / 2, ta, tb

        vbest = mp.findroot(lambda v: mp.diff(lambda vv: cyc(vv)[0], v), 2 * u)
        avg, ta, tb = cyc(vbest)
        gain = Lfix - avg
        pred = u ** 2 * abs(s["fpi"]) / 2
        # symmetric amplitude eps around u: controls (u+eps, u-eps), eps = u
        print("N=%d fixed point u=%.10f; best 2-cycle v=%.6f (2u=%.6f); per-stage gain=%.5e  "
              "quadratic prediction (1/2)u^2|f(pi)|=%.5e  ratio=%.4f"
              % (N, float(u), float(vbest), float(2 * u), float(gain), float(pred), float(gain / pred)), flush=True)
        n_arc = (T2 - T1) * N
        print("   total over (t2-t1)/h=%.2f stages, times (J+1): 2-cycle %.4e, quadratic %.4e"
              % (n_arc, float(gain) * n_arc * (1 + J_CHATTER[N]), float(pred) * n_arc * (1 + J_CHATTER[N])))
        if N == 100:
            def cyc2(v1, v2):
                g = lambda ta: FL(FL(ta, v1)[0], v2)[0] - ta
                ta = mp.findroot(g, th)
                tb, La = FL(ta, v1)
                return (La + FL(tb, v2)[1]) / 2
            for r in (mp.mpf("0.01"), mp.mpf("0.1"), mp.mpf("0.5"), mp.mpf(1)):
                eps = r * u
                gg = Lfix - cyc2(u + eps, u - eps)
                print("   symmetric 2-cycle (u+eps, u-eps), eps/u=%.2f: gain/((1/2)eps^2|f(pi)|) - 1 = %.3e"
                      % (float(r), float(gg / (eps ** 2 * abs(s["fpi"]) / 2) - 1)))


def arc_set(N):
    """first stage below 1 and last stage above 0 (u = 1 before, u = 0 after):
    of the saved saddle for N = 100, 200 (at N = 200 its first such stage sits
    at the bound 0), of the stored COPS point for N = 400."""
    u = np.load("logs/catmix%d_smooth_u.npy" % N) if N in (100, 200) else np.load(C.COPS % N)
    return int(np.argmax(u < 1 - 1e-9)), int(np.max(np.where(u > 1e-9)[0]))


def interior(u):
    return np.where((u > 1e-9) & (u < 1 - 1e-9))[0]


def smooth_baseline(R, i0, i1, s, junction_free):
    N = R.N
    idx = np.arange(i0, i1 + 1)
    inner = idx[1:-1] if junction_free else idx
    a, b = inner[0], inner[-1]
    knots = list(range(a, b + 1, s))
    if knots[-1] != b:
        knots.append(b)
    knots = np.array(knots, dtype=float)
    B = np.zeros((len(idx), len(knots) + (2 if junction_free else 0)))
    for r, i in enumerate(idx):
        if junction_free and i == i0:
            B[r, len(knots)] = 1.0
        elif junction_free and i == i1:
            B[r, len(knots) + 1] = 1.0
        else:
            j = np.searchsorted(knots, i, side="right") - 1
            j = min(j, len(knots) - 2)
            w = (i - knots[j]) / (knots[j + 1] - knots[j])
            B[r, j] += 1 - w
            B[r, j + 1] += w
    base = np.zeros(N + 1)
    base[:i0] = 1.0

    def u_of(z):
        u = base.copy()
        u[i0:i1 + 1] = B @ z
        return u

    def fg(z):
        cost, g = R.grad_logJ(u_of(z))
        return cost, B.T @ g[i0:i1 + 1]

    z0 = np.full(B.shape[1], U_S)
    r = minimize(fg, z0, jac=True, method="L-BFGS-B", bounds=[(0, 1)] * len(z0),
                 options=dict(maxiter=5000, ftol=1e-16, gtol=1e-15))
    z = r.x
    # Newton polish in knot space (interior)
    for _ in range(8):
        c0, g0 = fg(z)
        Hk = np.zeros((len(z), len(z)))
        e = 1e-6
        for j in range(len(z)):
            zp, zm = z.copy(), z.copy()
            zp[j] += e
            zm[j] -= e
            Hk[:, j] = (fg(zp)[1] - fg(zm)[1]) / (2 * e)
        dz = np.linalg.solve((Hk + Hk.T) / 2, -g0)
        zn = np.clip(z + dz, 0, 1)
        if fg(zn)[0] <= c0:
            z = zn
        if np.max(np.abs(dz)) < 1e-14:
            break
    cost, gk = fg(z)
    u = u_of(z)
    return u, cost, float(np.max(np.abs(gk))), len(z)


def free_hessian(R, u, free):
    def gf(v):
        return R.grad_logJ(v)[1][free]
    n = len(free)
    H = np.zeros((n, n))
    e = 1e-6
    for jj, j in enumerate(free):
        up, um = u.copy(), u.copy()
        up[j] += e
        um[j] -= e
        H[:, jj] = (gf(up) - gf(um)) / (2 * e)
    return (H + H.T) / 2


def part_C(Ns=(100, 200, 400)):
    print("== Part C: smooth-on-the-arc baseline (knots every s stages)")
    for N in Ns:
        t0 = time.time()
        R = C.Red(N)
        i0, i1 = arc_set(N)
        sd = symbol_data(N)
        pred = float(sd["u"] ** 2 * abs(sd["fpi"]) / 2) * (T2 - T1) * N * (1 + J_CHATTER[N])
        best = None
        for s in (4, 6, 10):
            for jf in (False, True):
                u, cost, gk, nk = smooth_baseline(R, i0, i1, s, jf)
                J = float(np.exp(cost) - 1)
                free = np.arange(i0, i1 + 1)
                gfull = np.max(np.abs(R.grad_logJ(u)[1][free]))
                rec = dict(N=N, s=s, junction_free=jf, n_knots=nk, J_smooth=J, max_grad_knots=gk,
                           max_grad_free_stages=float(gfull),
                           gain_over_chatter=J - J_CHATTER[N], predicted_gain=pred,
                           J_minus_saddle=(J - J_SADDLE[N]) if N in J_SADDLE else None,
                           u_arc_range=[float(u[i0:i1 + 1].min()), float(u[i0:i1 + 1].max())])
                print(json.dumps(rec), flush=True)
                if best is None or J < best[0]:
                    best = (J, u, s, jf)
        if N in (100, 200):
            J, u, s, jf = best
            free = interior(u)
            H = free_hessian(R, u, free)
            ev, V = np.linalg.eigh(H)
            alt = float(np.mean(np.sign(V[1:, 0]) != np.sign(V[:-1, 0])))
            fpiJ = float(sd["fpi"]) * (1 + J)
            print("N=%d Hessian (log(J+1)) on the %d interior stages of the best smooth base point (s=%d, junction_free=%s): "
                  "min eig=%.4e (J units %.4e), #neg=%d (predicted m d0/pi=%.2f), eigvec sign alternation=%.2f; "
                  "symbol f(pi)=%.4e (J units %.4e)"
                  % (N, len(free), s, jf, ev[0], ev[0] * (1 + J), int(np.sum(ev < 0)),
                     float(len(free) * sd["d0"] / mp.pi), alt, float(sd["fpi"]), fpiJ), flush=True)
            us = np.load("logs/catmix%d_smooth_u.npy" % N)
            fs = interior(us)
            evs = np.linalg.eigvalsh(free_hessian(R, us, fs))
            print("N=%d Hessian on the %d interior stages of the saved oscillating KKT point: min eig=%.4e (J units %.4e), "
                  "#neg=%d (predicted m d0/pi=%.2f)"
                  % (N, len(fs), evs[0], evs[0] * (1 + J_SADDLE[N]), int(np.sum(evs < 0)),
                     float(len(fs) * sd["d0"] / mp.pi)), flush=True)
        print("N=%d done in %.0f s" % (N, time.time() - t0), flush=True)


def part_D():
    """eta_L at the exit junction, exact: on the last arc (u = 0) the reduced
    cost-to-go is V(tau, theta) = log(1 - theta (1 - e^{-tau})); at the
    junction sigma = theta + b psi = 0."""
    import sympy as sp
    th, tau = sp.symbols("theta tau", positive=True)
    V = sp.log(1 - th * (1 - sp.exp(-tau)))
    # V solves the HJB equation of the last arc: -V_tau + (-theta) + V_theta (theta^2 - theta) = 0
    hjb = sp.simplify(-sp.diff(V, tau) - th + sp.diff(V, th) * (th ** 2 - th))
    psi, Q = sp.diff(V, th), sp.diff(V, th, 2)
    b = 1 - 10 * th - th ** 2
    w = -(1 + sp.diff(b, th) * psi)            # w = -(l1' + b' psi), l1 = theta
    eta = sp.simplify(b * (Q * b - w))
    print("== Part D: HJB residual of V on the last arc = %s; Q + psi^2 = %s" % (hjb, sp.simplify(Q + psi ** 2)))
    # impose sigma = theta + b psi = 0 by eliminating tau
    s = sp.symbols("s")                          # s = 1 - e^{-tau}
    eta_s = sp.simplify(eta.subs(sp.exp(-tau), 1 - s))
    sig_s = sp.simplify((th + b * psi).subs(sp.exp(-tau), 1 - s))
    ssol = sp.solve(sp.Eq(sig_s, 0), s)
    print("   sigma = 0 gives s = 1 - e^{-tau} = %s; eta_L there = %s"
          % (ssol, [sp.simplify(eta_s.subs(s, v)) for v in ssol]))


def part_E():
    """Checks of Proposition 3.7 (n = 1) and of the linearized first-order
    recursion on a stationary run of fractional stages.
    a = F_theta, c = F_u, [[Q, S], [S, R]] = Hessian of Lagr = L + q F.
    (i) m+ = (Q c^2 + 2 S c (1-a) + R (1-a)^2) = (1-a)^2 f(0),
        m- = (Q c^2 - 2 S c (1+a) + R (1+a)^2) = (1+a)^2 f(pi),
        m0 = cross term, band of admissible P: |m0 - 2 c^2 P| <= sqrt(m+ m-);
        brute-force scan of lambda_min of the stage matrix over P.
    (ii) transfer matrix of the stationarity + state recursion: det = 1 and
        trace/2 = cos(om0) with f(om0) = 0."""
    print("== Part E: Proposition 3.7 check and linearized first-order recursion")
    for name, N in (("trapezoid", 100), ("trapezoid", 400), ("exact flow", 100)):
        h = mp.mpf(1) / N
        FL = S.scheme(name, h)
        t, u, q, d = S.fixed_point(FL)
        f = lambda om: S.symbol(d, q, om)
        a, c = d["Ft"], d["Fu"]
        Q = d["Ltt"] + q * d["Ftt"]
        Sx = d["Ltu"] + q * d["Ftu"]
        R = d["Luu"] + q * d["Fuu"]
        mp_ = Q * c ** 2 + 2 * Sx * c * (1 - a) + R * (1 - a) ** 2
        mm_ = Q * c ** 2 - 2 * Sx * c * (1 + a) + R * (1 + a) ** 2
        m0 = Q * c ** 2 + Sx * c * ((1 - a) + (-1 - a)) + R * (1 - a) * (-1 - a)
        e1 = mp_ / ((1 - a) ** 2 * f(mp.mpf(0))) - 1
        e2 = mm_ / ((1 + a) ** 2 * f(mp.pi)) - 1

        def lam_min(P):
            M = mp.matrix([[Q + P * (a ** 2 - 1), Sx + P * a * c], [Sx + P * a * c, R + P * c ** 2]])
            return min(mp.eig(M)[0], key=lambda z: mp.re(z))

        Pc = m0 / (2 * c ** 2)
        band = mp.sqrt(mp_ * mm_) / (2 * c ** 2) if mp_ * mm_ >= 0 else None
        grid = [Pc + k * mp.mpf(10) ** -6 * max(1, abs(Pc)) for k in range(-50, 51)]
        best = max(mp.re(lam_min(P)) for P in grid)
        alpha, gam, kap = a - c * Sx / R, c ** 2 / R, Q - Sx ** 2 / R
        Phi = mp.matrix([[alpha + gam * kap / alpha, -gam / alpha], [-kap / alpha, 1 / alpha]])
        tr2 = (Phi[0, 0] + Phi[1, 1]) / 2
        n0 = f(mp.mpf(0)) * (1 - a) ** 2
        npi = f(mp.pi) * (1 + a) ** 2
        c0 = -(n0 + npi) / (n0 - npi)
        print("%s N=%d: f(pi)=%.4e; m+/((1-a)^2 f(0))-1=%.1e  m-/((1+a)^2 f(pi))-1=%.1e; "
              "P-band half-width=%s; max over a P-grid around m0/(2c^2) of lambda_min=%.3e; "
              "transfer matrix det-1=%.1e, trace/2=%.12f, cos(om0) from f=%.12f"
              % (name, N, float(f(mp.pi)), float(e1), float(e2),
                 ("%.3e" % float(band)) if band is not None else "empty (f(pi) < 0)", float(best),
                 float(mp.det(Phi) - 1), float(tr2), float(c0)), flush=True)


if __name__ == "__main__":
    parts = sys.argv[1:] or ["A", "B", "C"]
    if "D" in parts:
        part_D()
    if "E" in parts:
        part_E()
    if "A" in parts:
        part_A()
    if "B" in parts:
        part_B()
    if "C" in parts:
        part_C()
