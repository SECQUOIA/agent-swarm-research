"""Independent discrete-side checks for extension-n2.md (Euler transcription of the double-integrator family).

Own implementation, written from the problem statement, not from discrete.py:
- the Euler states are affine in u: x2_t = x20 + h sum_{j<t} u_j, x1_t = x10 + t h x20 + h^2 sum_{j<t} (t-1-j) u_j;
  J(u) is an exact quadratic; Hessian entries are computed from closed-form sums (H_entry);
- KKT points are found by ENUMERATION: bang-bang +1 / free set F / -1, with F a run of 0, 1 or 2 consecutive
  stages; u_F solves sigma_F = 0 exactly (sigma affine in u); every KKT sign is then checked;
- the maximal recursion of Lemma 10 is implemented from my own derivation of the stage quadratic;
- stage losses over the exact reachable box: quadratic minimisation over a 3-d box by solving, for each of the
  8 u/x-face combinations, ... (plain face enumeration, own code).
"""
import itertools
import json
import sys
import time

import numpy as np

EX = {
    "A": dict(rho=2.0, k1=-0.3, k2=-0.3, q=0.3, c=1.0, x20=0.5, e=0.0),
    "A0": dict(rho=1.0, k1=-0.3, k2=-0.3, q=0.3, c=0.2, x20=0.5, e=0.0),
    "B": dict(rho=1.0, k1=0.6, k2=-1.2, q=1.0, c=0.5, x20=0.5, e=0.3),
    "B2": dict(rho=0.5, k1=0.5, k2=-0.6, q=0.3, c=0.2, x20=0.0, e=0.0),
    "C": dict(rho=0.5, k1=0.5, k2=-0.2, q=0.3, c=0.2, x20=0.0, e=0.0),
}
T, a, x10 = 2.0, 1.0, 0.0


class Prob:
    def __init__(self, name, N):
        self.__dict__.update(EX[name])
        self.name, self.N, self.h = name, N, T / N

    def states(self, u):
        N, h = self.N, self.h
        x2 = np.empty(N + 1); x1 = np.empty(N + 1)
        x2[0], x1[0] = self.x20, x10
        x2[1:] = self.x20 + h * np.cumsum(u)
        x1[1:] = x10 + h * np.cumsum(x2[:-1])
        return x1, x2

    def cost(self, u):
        x1, x2 = self.states(u)
        h = self.h
        run = h * np.sum(self.e * x2[:-1] + self.q / 2 * x1[:-1] ** 2 - self.c / 2 * x2[:-1] ** 2
                         + (self.k1 * x1[:-1] + self.k2 * x2[:-1]) * u)
        return run - a * x1[-1] + self.rho / 2 * x2[-1] ** 2

    def sigma(self, u):
        """sigma_t = (1/h) dJ/du_t via the backward adjoint lam_t = dJ/dx_t."""
        x1, x2 = self.states(u)
        N, h = self.N, self.h
        l1, l2 = -a, self.rho * x2[N]
        sig = np.empty(N)
        for t in range(N - 1, -1, -1):
            sig[t] = self.k1 * x1[t] + self.k2 * x2[t] + l2
            # lam_t = h grad(l0 + l1 u)(x_t) + Fx^T lam_{t+1},  Fx = [[1, h], [0, 1]]
            l1, l2 = (h * (self.q * x1[t] + self.k1 * u[t]) + l1,
                      h * (self.e - self.c * x2[t] + self.k2 * u[t]) + h * l1 + l2)
        self._lam0 = (l1, l2)
        return sig

    def H_entry(self, i, j):
        """d^2 J / du_i du_j from the closed-form sensitivities G1[s,i] = h^2 (s-1-i), G2[s,i] = h (s > i)."""
        N, h = self.N, self.h
        s = np.arange(max(i, j) + 1, N)          # running-cost stages that see both u_i and u_j
        G1i, G1j = h * h * (s - 1 - i), h * h * (s - 1 - j)
        val = h * np.sum(self.q * G1i * G1j - self.c * h * h)
        # l1(x_t) u_t cross terms: d/du_i [k.x_j] u_j with i < j, and symmetric
        def cross(p, r):  # derivative of h * (k1 x1_r + k2 x2_r) * u_r w.r.t. u_p (p < r)
            return h * (self.k1 * h * h * (r - 1 - p) + self.k2 * h) if p < r else 0.0
        val += cross(i, j) + cross(j, i)
        val += self.rho * h * h                  # terminal rho/2 x2_N^2
        # terminal -a x1_N is linear: no Hessian contribution
        return val

    def hessian(self):
        N, h = self.N, self.h
        t = np.arange(N)
        s = np.arange(N)
        # G1[s, i] = h^2 (s-1-i) for s > i;  G2[s, i] = h for s > i  (rows s = 0..N-1 are running stages)
        S, I = np.meshgrid(s, t, indexing="ij")
        G1 = np.where(S > I, h * h * (S - 1 - I), 0.0)
        G2 = np.where(S > I, h, 0.0)
        H = h * (self.q * G1.T @ G1 - self.c * G2.T @ G2)
        M = h * (self.k1 * G1 + self.k2 * G2)    # row r: d(k.x_r)/du ; the running term is u_r (k.x_r)
        H += M + M.T
        H += self.rho * h * h * np.ones((N, N))
        return H


def kkt_enumerate(pb, m_guess, radius=6):
    """All KKT points of the form (+1 ... +1, u_F, -1 ... -1), F = run of 0, 1, 2 stages, near m_guess."""
    N, h = pb.N, pb.h
    found = []
    for m in range(max(0, m_guess - radius), min(N, m_guess + radius) + 1):
        for k in (0, 1, 2):
            F = list(range(m, min(N, m + k)))
            u = np.where(np.arange(N) < m, 1.0, -1.0)
            if F:
                s0 = pb.sigma(u)[F]
                HF = np.array([[pb.H_entry(i, j) for j in F] for i in F])
                uF = u[F] - h * np.linalg.solve(HF, s0)   # sigma_F(u) = sigma_F(u0) + H_FF du_F / h
                if np.any(uF < -1 - 1e-12) or np.any(uF > 1 + 1e-12):
                    continue
                u[F] = np.clip(uF, -1, 1)
            sig = pb.sigma(u)
            other = np.setdiff1d(np.arange(N), F)
            viol = np.max(np.where(u[other] > 0, np.maximum(0, sig[other]), np.maximum(0, -sig[other])))
            fres = np.max(np.abs(sig[F])) if F else 0.0
            if viol <= 1e-12 and fres <= 1e-11:
                inter = [int(t) for t in F if abs(abs(u[t]) - 1) > 1e-12]
                found.append(dict(m=m, F=F, interior=inter, u=u.copy(), sig=sig, J=pb.cost(u), viol=float(viol),
                                  fres=float(fres)))
    # de-duplicate identical controls
    uniq = []
    for f in found:
        if not any(np.max(np.abs(f["u"] - g["u"])) < 1e-12 for g in uniq):
            uniq.append(f)
    return uniq


def m_guess_of(pb):
    """Sign change of sigma along pure bang-bang controls (bisection on the switch index)."""
    N = pb.N
    lo, hi = 0, N
    while hi - lo > 1:
        mid = (lo + hi) // 2
        u = np.where(np.arange(N) < mid, 1.0, -1.0)
        sg = pb.sigma(u)[mid]
        if sg < 0:   # still wants +1 at stage mid -> switch later
            lo = mid
        else:
            hi = mid
    return hi


def costates(pb, u):
    """p_t = dJ/dx_t (discrete costates), t = 0..N (p_0 is the full-state gradient at t = 0)."""
    x1, x2 = pb.states(u)
    N, h = pb.N, pb.h
    p = np.empty((N + 1, 2))
    p[N] = (-a, pb.rho * x2[N])
    for t in range(N - 1, -1, -1):
        p[t, 0] = h * (pb.q * x1[t] + pb.k1 * u[t]) + p[t + 1, 0]
        p[t, 1] = h * (pb.e - pb.c * x2[t] + pb.k2 * u[t]) + h * p[t + 1, 0] + p[t + 1, 1]
    return p


def maximal_recursion(pb, kk, eps, PN=None):
    """P_t = h Hxx + Fx^T P_{t+1} Fx - 2 h eps I - beta beta^T / m,  m = 2|sig|/(h Delta) + kap (vertex) or kap
    (interior control); returns P and the break stage (m <= 0)."""
    N, h = pb.N, pb.h
    Fx = np.array([[1.0, h], [0.0, 1.0]])
    b = np.array([0.0, 1.0]); w = -np.array([pb.k1, pb.k2])
    Hxx = np.diag([pb.q, -pb.c])
    P = np.full((N + 1, 2, 2), np.nan)
    P[N] = np.diag([0.0, pb.rho]) - 2 * eps * np.eye(2) if PN is None else PN
    inter = set(kk["interior"])
    for t in range(N - 1, -1, -1):
        X = P[t + 1]
        beta = Fx.T @ X @ b - w
        kap = b @ X @ b
        m = kap + (0.0 if t in inter else 2 * abs(kk["sig"][t]) / (h * 2.0))
        if m <= 0:
            return P, t
        P[t] = h * Hxx + Fx.T @ X @ Fx - 2 * h * eps * np.eye(2) - np.outer(beta, beta) / m
    return P, None


def lyap_family(pb, eps):
    N, h = pb.N, pb.h
    Fx = np.array([[1.0, h], [0.0, 1.0]])
    P = np.empty((N + 1, 2, 2))
    P[N] = np.diag([0.0, pb.rho]) - 2 * eps * np.eye(2)
    for t in range(N - 1, -1, -1):
        P[t] = h * np.diag([pb.q, -pb.c]) + Fx.T @ P[t + 1] @ Fx - 2 * h * eps * np.eye(2)
    return P


def boxmin(g, Hm, lo, hi):
    """min of g.z + 1/2 z^T Hm z over lo <= z <= hi (float), by enumerating all faces."""
    n = len(g)
    best = np.inf
    for pat in itertools.product(range(3), repeat=n):
        fixed = [i for i in range(n) if pat[i] < 2]
        free = [i for i in range(n) if pat[i] == 2]
        z = np.zeros(n)
        for i in fixed:
            z[i] = lo[i] if pat[i] == 0 else hi[i]
        if free:
            A = Hm[np.ix_(free, free)]
            rhs = -(g[free] + Hm[np.ix_(free, fixed)] @ z[fixed])
            try:
                zf = np.linalg.solve(A, rhs)
            except np.linalg.LinAlgError:
                continue
            if np.any(zf < lo[free] - 1e-14) or np.any(zf > hi[free] + 1e-14):
                continue
            z[free] = zf
        best = min(best, g @ z + 0.5 * z @ Hm @ z)
    return best


def stage_losses(pb, kk, P):
    """loss_t = rho_t(zbar) - min over (reach box x U) of rho_t, from the explicit residual in z = (x1, x2, u):
    rho_t(z) = h l(x, u) + S_{t+1}(x + h(x2, u)) - S_t(x),  S_t(x) = p_t.x + 1/2 (x - c_t)^T P_t (x - c_t)."""
    N, h = pb.N, pb.h
    u, x1, x2, p = kk["u"], kk["x1"], kk["x2"], kk["p"]
    M = np.array([[1.0, h, 0.0], [0.0, 1.0, h]])   # x_{t+1} = M z
    E = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])
    HL = h * np.array([[pb.q, 0, pb.k1], [0, -pb.c, pb.k2], [pb.k1, pb.k2, 0]])
    loss = np.empty(N)
    for t in range(N):
        zb = np.array([x1[t], x2[t], u[t]])
        c1 = np.array([x1[t + 1], x2[t + 1]]); c0 = zb[:2]
        Hm = HL + M.T @ P[t + 1] @ M - E.T @ P[t] @ E
        # gradient at zbar: h grad l + M^T (p_{t+1} + P_{t+1}(M zb - c1)) - E^T (p_t + P_t (x - c0))
        g = h * np.array([pb.q * zb[0] + pb.k1 * zb[2], pb.e - pb.c * zb[1] + pb.k2 * zb[2],
                          pb.k1 * zb[0] + pb.k2 * zb[1]]) + M.T @ (p[t + 1] + P[t + 1] @ (M @ zb - c1)) - E.T @ p[t]
        if t == 0:
            lo = np.array([0.0, 0.0, -1 - u[0]]); hi = np.array([0.0, 0.0, 1 - u[0]])
        else:
            w2, w1 = t * h, h * h * t * (t - 1) / 2
            lo = np.array([x10 + t * h * pb.x20 - w1 - zb[0], pb.x20 - w2 - zb[1], -1 - zb[2]])
            hi = np.array([x10 + t * h * pb.x20 + w1 - zb[0], pb.x20 + w2 - zb[1], 1 - zb[2]])
        loss[t] = -boxmin(g, Hm, lo, hi)
    return loss


def solve(name, N):
    pb = Prob(name, N)
    mg = m_guess_of(pb)
    sols = kkt_enumerate(pb, mg)
    return pb, sols


def kk_of(pb, s):
    x1, x2 = pb.states(s["u"])
    return dict(u=s["u"], sig=s["sig"], x1=x1, x2=x2, p=costates(pb, s["u"]), interior=s["interior"])


if __name__ == "__main__":
    task = sys.argv[1]
    out = []
    if task == "kkt":   # KKT structure (number of KKT points found, interior stages) for A0, A, B
        for name, Ns in (("A0", [50, 200, 500, 1000, 2000, 5000]), ("A", [50, 200, 500, 1000, 2000, 5000]),
                         ("B", [500, 1000, 2000])):
            for N in Ns:
                pb, sols = solve(name, N)
                rec = dict(example=name, N=N, n_kkt=len(sols),
                           kkt=[dict(m=s["m"], interior=s["interior"], J=s["J"], uF=[float(s["u"][t]) for t in s["interior"]])
                                for s in sols])
                print(json.dumps(rec), flush=True); out.append(rec)
    elif task == "hess":  # reduced Hessian spectrum
        for name, N in (("A", 200), ("A0", 200), ("A", 500)):
            pb = Prob(name, N)
            H = pb.hessian()
            # spot-check the dense Hessian against H_entry and against differencing of sigma
            rng = np.random.default_rng(1)
            u0 = rng.uniform(-1, 1, N)
            err = 0.0
            for j in rng.choice(N, 5, replace=False):
                du = np.zeros(N); du[j] = 1.0
                col = pb.h * (pb.sigma(u0 + du) - pb.sigma(u0))
                err = max(err, np.max(np.abs(col - H[:, j])), abs(pb.H_entry(3, j) - H[3, j]))
            ev = np.linalg.eigvalsh(H)
            rec = dict(example=name, N=N, n_neg=int((ev < 0).sum()), min_eig=float(ev[0]), max_eig=float(ev[-1]),
                       check_err=float(err))
            print(json.dumps(rec), flush=True); out.append(rec)
    elif task == "rmaxB":  # break stage of the maximal recursion, example B (and B2, C)
        for name in ("B", "B2", "C"):
            for N in (500, 1000, 2000, 4000, 8000, 16000):
                pb, sols = solve(name, N)
                s = sols[0]
                kk = kk_of(pb, s)
                for eps in (0.0, 0.02):
                    P, brk = maximal_recursion(pb, kk, eps)
                    rec = dict(example=name, N=N, n_kkt=len(sols), interior=s["interior"], m=s["m"], eps=eps, brk=brk,
                               brk_minus_m=None if brk is None else brk - s["m"],
                               time_after=None if brk is None else (brk - s["m"]) * pb.h,
                               maxabsP=float(np.nanmax(np.abs(P))))
                    print(json.dumps(rec), flush=True); out.append(rec)
    elif task == "windows":  # float stage losses of the maximal recursion and the Lyapunov family, example A / A0
        for name in ("A", "A0"):
            for N in [int(v) for v in sys.argv[2:]]:
                t0 = time.time()
                pb, sols = solve(name, N)
                s = sols[0]
                kk = kk_of(pb, s)
                P, brk = maximal_recursion(pb, kk, 0.02)
                lr = stage_losses(pb, kk, P) if brk is None else None
                ll = stage_losses(pb, kk, lyap_family(pb, 0.02))
                bad = np.where(ll > 1e-12)[0]
                rec = dict(example=name, N=N, n_kkt=len(sols), m=s["m"], interior=s["interior"], rmax_brk=brk,
                           rmax_nfail=None if lr is None else int((lr > 1e-12).sum()),
                           rmax_maxloss=None if lr is None else float(lr.max()),
                           lyap_nfail=int(len(bad)), lyap_range=[int(bad.min() - s["m"]), int(bad.max() - s["m"])] if len(bad) else None,
                           lyap_duration=float(len(bad) * pb.h), secs=time.time() - t0)
                print(json.dumps(rec), flush=True); out.append(rec)
    with open("logs/v_discrete_%s.json" % task, "w") as f:
        json.dump(out, f, indent=1)
