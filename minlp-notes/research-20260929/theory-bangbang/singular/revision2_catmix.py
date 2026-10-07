"""Round-2 revision checks for singular-arcs.md (confirmation review
reviews/singular-arcs-confirm-r1.md, items R1, R2, R3, R5, R7).  COPS catmix,
trapezoidal rule, reduced projective model of catmix_trap.py.

Part K (R1, R3, R5): audit of the saved points logs/catmix{100,200}_smooth_u.npy
  - arc stages (first stage below 1 to last stage above 0), stages of the arc
    at a bound, their gradients and KKT signs, max |gradient| on the interior
    stages;
  - the reduced Hessian on the interior stages, computed analytically by a
    second-order adjoint (analytic second partials of the stage maps; float
    arithmetic, not rational; checked against central differences of the
    analytic gradient); number of negative
    eigenvalues, most negative, eigenvalues nearest zero, Newton step;
  - control range and deviation from the neighbour average, over the interior
    stages and over the whole arc;
  - sign changes of the alternating envelope (absolute stage numbers).
Part L (R1): one time-limited attempt to find a verified KKT point at N = 200
  from the saved point: semismooth Newton with Levenberg-Marquardt damping on
  the Fischer-Burmeister form of the KKT conditions of the arc stages (lower
  bound u >= 0; the arc controls stay far below 1), analytic Hessian (float).
Part M (R2): Remark 3.9.  (i) The two toy examples of the review, with the
  transfer map built from the linear first-order equations directly (not from
  the half-trace formula).  (ii) m+ = (1-a)^2 f(0), m- = (1+a)^2 f(pi) and
  tr(Phi)/2 for the catmix trapezoidal rule and exact flow, against the
  small-h form -(K + 4 phi)/(K - 4 phi), f(pi) = phi h^3, K = 2 sqrt(10).
Part Z (R7c): arithmetic for the MINLPLib catmix100 value.
Usage: python3 revision2_catmix.py [K] [L | L=maxit] [M] [Z]   (default: K M Z; L: 400 iterations)
"""
import sys
import time

import mpmath as mp
import numpy as np

import catmix_schemes as S
import catmix_trap as C
import catmix_windows as W
import revision_catmix as RC

mp.mp.dps = 50


def arc_of(u):
    return int(np.argmax(u < 1 - 1e-9)), int(np.max(np.where(u > 1e-9)[0]))


def exact_grad_hess(R, an, u):
    """log(J+1), its gradient and its analytic Hessian in u (second-order adjoint,
    float arithmetic; the name "exact" is kept because a review script imports it).
    Stage i = 1..N-1: theta_i = F(theta_{i-1}, u_i), cost L(theta_{i-1}, u_i);
    terminal T(theta_{N-1}, u_N); theta_0 = h u_0 / 2 (linear)."""
    N = R.N
    th, cost = R.simulate(u)
    Tv = an["T"](th[N - 1], u[N])
    q = np.zeros(N)
    q[N - 1] = Tv[1]
    g = np.zeros(N + 1)
    g[N] = Tv[2]
    for i in range(N - 1, 0, -1):
        Lv = an["L"](th[i - 1], u[i])
        Fv = an["F"](th[i - 1], u[i])
        g[i] = Lv[2] + q[i] * Fv[2]
        q[i - 1] = Lv[1] + q[i] * Fv[1]
    g[0] = q[0] * R.h / 2
    H = np.zeros((N + 1, N + 1))
    s = np.zeros(N + 1)
    s[0] = R.h / 2
    for i in range(1, N):
        Lv = an["L"](th[i - 1], u[i])
        Fv = an["F"](th[i - 1], u[i])
        ltt = Lv[3] + q[i] * Fv[3]
        ltu = Lv[4] + q[i] * Fv[4]
        luu = Lv[5] + q[i] * Fv[5]
        H += ltt * np.outer(s, s)
        H[i, :] += ltu * s
        H[:, i] += ltu * s
        H[i, i] += luu
        s = Fv[1] * s
        s[i] += Fv[2]
    H += Tv[3] * np.outer(s, s)
    H[N, :] += Tv[4] * s
    H[:, N] += Tv[4] * s
    H[N, N] += Tv[5]
    return cost, g, H


def fd_hess(R, u, idx, e):
    n = len(idx)
    Hf = np.zeros((n, n))
    for jj, j in enumerate(idx):
        up, um = u.copy(), u.copy()
        up[j] += e
        um[j] -= e
        Hf[:, jj] = (R.grad_logJ(up)[1][idx] - R.grad_logJ(um)[1][idx]) / (2 * e)
    return (Hf + Hf.T) / 2


def envelope_changes(u, i0, i1):
    """alternating component a_i = (-1)^i (u_i - (u_{i-1} + u_{i+1})/2) / 2 for
    i0 < i < i1; returns the stages i where sign(a_i) != sign(a_{i-1})."""
    idx = np.arange(i0 + 1, i1)
    a = ((-1.0) ** idx) * (u[idx] - 0.5 * (u[idx - 1] + u[idx + 1])) / 2
    return [int(idx[k]) for k in range(1, len(idx)) if a[k] * a[k - 1] < 0]


def audit(R, an, u, label, fd=True):
    N = R.N
    i0, i1 = arc_of(u)
    cost, g, H = exact_grad_hess(R, an, u)
    arc = np.arange(i0, i1 + 1)
    atb = [int(j) for j in arc if u[j] <= 1e-9 or u[j] >= 1 - 1e-9]
    inter = np.array([j for j in arc if j not in atb])
    bad = [j for j in range(N + 1) if (u[j] >= 1 - 1e-9 and g[j] > 1e-12) or (u[j] <= 1e-9 and g[j] < -1e-12)]
    print("%s N=%d: J=%.13f; arc stages %d..%d (m=%d); arc stages at a bound: %s, gradient there %s "
          "(lower bound needs g >= 0); stages with a wrong KKT sign (tol 1e-12): %s; max|g| on the %d interior stages = %.2e"
          % (label, N, np.exp(cost) - 1, i0, i1, len(arc), atb, ["%.2e" % g[j] for j in atb], bad, len(inter),
             np.max(np.abs(g[inter]))), flush=True)
    HI = H[np.ix_(inter, inter)]
    ev, V = np.linalg.eigh(HI)
    order = np.argsort(np.abs(ev))
    step = np.linalg.solve(HI, -g[inter])
    v0 = V[:, order[0]]
    print("   analytic Hessian (second-order adjoint, float) on the interior stages: #neg=%d, most negative %.4e (J units %.4e), eigenvalues nearest 0 %s, "
          "largest %.3e; Newton step max|du| = %.2e; |g.v|/|lambda| along the eigenvector nearest 0 = %.2e"
          % (int(np.sum(ev < 0)), ev[0], ev[0] * np.exp(cost), ["%.2e" % ev[k] for k in order[:4]], ev[-1],
             np.max(np.abs(step)), abs(g[inter] @ v0) / abs(ev[order[0]])), flush=True)
    if fd:
        for e in (1e-6, 1e-5):
            Hf = fd_hess(R, u, inter, e)
            evf = np.linalg.eigvalsh(Hf)
            print("   central differences, step %.0e: max|H_fd - H_analytic| = %.1e, #neg=%d, smallest |eig| %.2e"
                  % (e, np.max(np.abs(Hf - HI)), int(np.sum(evf < 0)), np.min(np.abs(evf))), flush=True)
    dev_idx = np.arange(i0 + 1, i1)
    dev = np.abs(u[dev_idx] - 0.5 * (u[dev_idx - 1] + u[dev_idx + 1]))
    dev_int = np.array([dev[k] for k, j in enumerate(dev_idx) if j in set(inter.tolist())])
    ch = envelope_changes(u, i0, i1)
    print("   u range: interior stages [%.4f, %.4f], whole arc [%.4f, %.4f]; max deviation from the neighbour average: "
          "interior stages %.3f, whole arc %.3f" % (u[inter].min(), u[inter].max(), u[arc].min(), u[arc].max(),
                                                    dev_int.max(), dev.max()), flush=True)
    print("   envelope sign changes at stages %s; spacings %s" % (ch, np.diff(ch).tolist()), flush=True)
    return dict(u=u, cost=cost, g=g, H=H, inter=inter, ev=ev, i0=i0, i1=i1)


def part_K():
    print("== Part K: audit of the saved KKT-point candidates")
    for N in (100, 200):
        t0 = time.time()
        R = C.Red(N)
        an = W.analytic2(N)
        u = np.load("logs/catmix%d_smooth_u.npy" % N)
        a = audit(R, an, u, "saved point")
        sd = RC.symbol_data(N)
        m = len(a["inter"])
        est = float(sd["fpi"] + sd["f2"] / 2 * (mp.pi / (m + 1)) ** 2)
        print("   symbol: f(pi) = %.4e; lowest eigenvalue of an m-stage Toeplitz section ~ f(pi) + f''(pi)/2 (pi/(m+1))^2 "
              "= %.4e (m = %d); saved point: most negative / f(pi) = %.3f, / section estimate = %.3f; m d0/pi = %.2f"
              % (float(sd["fpi"]), est, m, a["ev"][0] / float(sd["fpi"]), a["ev"][0] / est,
                 float(m * sd["d0"] / mp.pi)), flush=True)
        mr = {100: 59, 200: 118}[N]
        print("   finite-section estimate for the %d interior stages of the smooth reference (revision_catmix.py Part C): %.4e"
              % (mr, float(sd["fpi"] + sd["f2"] / 2 * (mp.pi / (mr + 1)) ** 2)), flush=True)
        print("   (%.0f s)" % (time.time() - t0), flush=True)


def fb(a, b):
    r = np.sqrt(a * a + b * b)
    return a + b - r, r


def part_L(tmax=900.0, maxit=400):
    print("== Part L: semismooth Newton / Levenberg-Marquardt on the FB form of the KKT conditions, N = 200")
    N = 200
    R = C.Red(N)
    an = W.analytic2(N)
    u = np.load("logs/catmix200_smooth_u.npy")
    i0, i1 = arc_of(u)
    A = np.arange(i0, i1 + 1)
    cost, g, H = exact_grad_hess(R, an, u)
    sc = 1.0 / np.max(np.abs(np.diag(H)[A]))

    def resid(v):
        c_, g_, H_ = exact_grad_hess(R, an, v)
        r, rho = fb(v[A], sc * g_[A])
        return r, rho, g_, H_

    r, rho, g, H = resid(u)
    mu = 1e-6 * np.max(np.abs(H[np.ix_(A, A)] * sc)) ** 2
    t0 = time.time()
    it = 0
    hist = []
    while time.time() - t0 < tmax and it < maxit:
        it += 1
        a_, b_ = u[A], sc * g[A]
        da = np.where(rho > 0, 1 - a_ / np.where(rho > 0, rho, 1), 1 - 1 / np.sqrt(2))
        db = np.where(rho > 0, 1 - b_ / np.where(rho > 0, rho, 1), 1 - 1 / np.sqrt(2))
        Jm = np.diag(da) + db[:, None] * (sc * H[np.ix_(A, A)])
        JtJ, Jtr = Jm.T @ Jm, Jm.T @ r
        improved = False
        for _ in range(30):
            d = np.linalg.solve(JtJ + mu * np.eye(len(A)), -Jtr)
            un = u.copy()
            un[A] += d
            rn, rhon, gn, Hn = resid(un)
            if np.linalg.norm(rn) < np.linalg.norm(r):
                u, r, rho, g, H = un, rn, rhon, gn, Hn
                mu = max(mu / 5, 1e-40)
                improved = True
                break
            mu *= 4
        free = [j for j in A if u[j] > 1e-12]
        hist.append((it, float(np.linalg.norm(r)), float(np.max(np.abs(g[free]))), mu))
        if it % 10 == 0 or not improved:
            print("   it %d: |r| = %.3e, max|g| on stages with u > 1e-12 = %.3e, mu = %.1e, min u on arc = %.2e"
                  % (it, np.linalg.norm(r), np.max(np.abs(g[free])), mu, u[A].min()), flush=True)
        if not improved or np.linalg.norm(r) < 1e-16:
            break
    print("   stopped after %d iterations, %.0f s; |r| = %.3e" % (it, time.time() - t0, np.linalg.norm(r)), flush=True)
    # snap tiny controls to the bound and audit
    u2 = u.copy()
    u2[(u2 < 1e-12)] = 0.0
    a = audit(R, an, u2, "Part L end point", fd=False)
    np.save("logs/catmix200_r2_attempt_u.npy" if maxit == 400 else "logs/catmix200_r2_attempt%d_u.npy" % maxit, u2)


def transfer(a, c, Q, Sx, Rr):
    """transfer map (dtheta_t, lam_t) -> (dtheta_{t+1}, lam_{t+1}) from
    R du + c lam' = -S dth,  S du + a lam' = lam - Q dth,  dth' = a dth + c du."""
    Phi = np.zeros((2, 2))
    for k, (x, lam) in enumerate(((1.0, 0.0), (0.0, 1.0))):
        du, lamn = np.linalg.solve(np.array([[Rr, c], [Sx, a]]), np.array([-Sx * x, lam - Q * x]))
        Phi[:, k] = (a * x + c * du, lamn)
    return Phi


def toy(a, c, Q, Sx, Rr):
    f = lambda om: (Rr + 2 * Sx * np.real(c / (np.exp(1j * om) - a)) + Q * abs(c / (np.exp(1j * om) - a)) ** 2)
    e = 1e-4
    f2 = (f(np.pi + e) - 2 * f(np.pi) + f(np.pi - e)) / e ** 2
    grid = np.linspace(0, np.pi, 2001)
    Phi = transfer(a, c, Q, Sx, Rr)
    mp_ = (1 - a) ** 2 * f(0.0)
    mm_ = (1 + a) ** 2 * f(np.pi)
    print("toy (a,c,Q,S,R)=(%g,%g,%g,%g,%g): f(0)=%.4f f(pi)=%.4f f''(pi)=%.4f min f on [0,pi]=%.4f; m+=%.4f m-=%.4f; "
          "det Phi=%.12f, tr Phi/2=%.6f, -(m+ + m-)/(m+ - m-)=%.6f, eigenvalues %s"
          % (a, c, Q, Sx, Rr, f(0.0), f(np.pi), f2, min(f(w) for w in grid), mp_, mm_, np.linalg.det(Phi),
             np.trace(Phi) / 2, -(mp_ + mm_) / (mp_ - mm_), np.round(np.linalg.eigvals(Phi), 6).tolist()), flush=True)


def part_M():
    print("== Part M: Remark 3.9 checks")
    toy(0.5, 1, 1, 0, 1)
    toy(-0.5, 1, -2, -0.25, 1)
    K = 2 * mp.sqrt(10)
    for name, N in (("trapezoid", 100), ("trapezoid", 200), ("trapezoid", 400), ("exact flow", 100), ("exact flow", 200)):
        h = mp.mpf(1) / N
        FL = S.scheme(name, h)
        t, u, q, d = S.fixed_point(FL)
        a, c = d["Ft"], d["Fu"]
        Q = d["Ltt"] + q * d["Ftt"]
        Sx = d["Ltu"] + q * d["Ftu"]
        Rr = d["Luu"] + q * d["Fuu"]
        f0, fpi = S.symbol(d, q, mp.mpf(0)), S.symbol(d, q, mp.pi)
        mp_, mm_ = (1 - a) ** 2 * f0, (1 + a) ** 2 * fpi
        Phi = transfer(float(a), float(c), float(Q), float(Sx), float(Rr))
        phi = fpi / h ** 3
        lim = -(K + 4 * phi) / (K - 4 * phi)
        ev = np.linalg.eigvals(Phi)
        print("%s N=%d: f(0)/h=%.6f (K/10=%.6f), (1-a)/h=%.5f, m+/h^3=%.5f (K=%.5f), f(pi)/h^3=%.6f, m-/h^3=%.5f "
              "(4 f(pi)/h^3=%.5f); tr Phi/2 from the equations=%.10f, -(m+ + m-)/(m+ - m-)=%.10f, "
              "small-h form -(K+4phi)/(K-4phi)=%.10f; |eigenvalues| %s"
              % (name, N, float(f0 / h), float(K / 10), float((1 - a) / h), float(mp_ / h ** 3), float(K),
                 float(phi), float(mm_ / h ** 3), float(4 * phi), np.trace(Phi) / 2, float(-(mp_ + mm_) / (mp_ - mm_)),
                 float(lim), np.round(np.abs(ev), 5).tolist()), flush=True)
        if name == "trapezoid" and N == 100:
            om0 = mp.acos(lim)
            print("   small-h form gives d0 = pi - acos(.) = %.5f, pi/d0 = %.4f" % (float(mp.pi - om0), float(mp.pi / (mp.pi - om0))))


def part_Z():
    listed, ours, cops_local = -0.04806939108, -0.0480694320309772, -0.04806939757
    print("== Part Z: MINLPLib catmix100 primal bound %.11f (treewidth-census/instancedata.csv); chattering point %.16f; "
          "gap %.3e; [C]'s local solve %.11f is %.3e below the listed value"
          % (listed, ours, listed - ours, cops_local, listed - cops_local))


if __name__ == "__main__":
    parts = sys.argv[1:] or ["K", "M", "Z"]
    if "Z" in parts:
        part_Z()
    if "M" in parts:
        part_M()
    if "K" in parts:
        part_K()
    for p_ in parts:
        if p_ == "L" or p_.startswith("L="):
            part_L(maxit=int(p_[2:]) if p_.startswith("L=") else 400)
