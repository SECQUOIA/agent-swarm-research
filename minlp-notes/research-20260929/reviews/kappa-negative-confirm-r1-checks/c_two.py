"""Independent re-check (confirmation referee, round 1) of the two-switch close-switch toy of
kappa-negative.md, Section 9.3 (float), written from the note's definitions only.

Toy: x' = u, |u| <= 1, x0 = 0, T = 2, a = 4 on [0,t1), -4 on [t1,t2), 4 on [t2,2]; k = k1 on [0,tk), k2 after;
Euler: J = h sum_{t<N} [(x_t - a_t)^2/2 + k_t x_t u_t] - 3 x_N + x_N^2/2;  a_t = a(t h), jump times read as
exact decimals.  dJ/du_t = h sigma_t, sigma_t = k_t x_t + p_{t+1}, p_N = -3 + x_N, p_t = p_{t+1} + h (x_t - a_t + k_t u_t).

KKT search (own): enumerate monotone patterns (+1 | v1 at s1 | -1 ... | v2 at s2 | +1), minimize the exact 2-D
quadratic in (v1, v2) over [-1,1]^2 by faces, coordinate descent over (s1, s2) and then a full 2-D scan of
+-R stages around the result; keep the best; check the full KKT conditions.
Maximal recursion ([E, Lemma 10], eps = 0, Delta = 2): P_N = 1, beta = P_{t+1} + k_t,
m = |sigma_t|/h (0 at fractional stages) + P_{t+1}; break if m <= 0; P_t = h + P_{t+1} - beta^2/m.
"""
import itertools
import json
import sys
import time
from fractions import Fraction as Fr

import numpy as np

T = 2


def piece(pts, N):
    """pts = ((t_i as decimal string, value), ...); value at stage t = last i with t h >= t_i (exact)."""
    out = np.empty(N + 1)
    for t in range(N + 1):
        v = pts[0][1]
        for ti, vi in pts:
            if Fr(ti) * N <= Fr(t) * T:
                v = vi
        out[t] = v
    return out


class Toy:
    def __init__(self, t1, t2, k1, k2, tk, N):
        self.N = N
        self.h = T / N
        self.a = piece((("0", 4.0), (t1, -4.0), (t2, 4.0)), N)[:N]
        self.k = piece((("0", k1), (tk, k2)), N)[:N]
        self.k1, self.k2, self.tk = k1, k2, tk

    def sim(self, u):
        h, N = self.h, self.N
        x = np.concatenate([[0.0], np.cumsum(h * u)])
        J = h * np.sum((x[:N] - self.a) ** 2 / 2 + self.k * x[:N] * u) - 3 * x[N] + x[N] ** 2 / 2
        pN = -3 + x[N]
        inc = h * (x[:N] - self.a + self.k * u)
        p = np.empty(N + 1)
        p[N] = pN
        p[:N] = pN + np.cumsum(inc[::-1])[::-1]
        sig = self.k * x[:N] + p[1:]
        return x, J, sig

    def H(self, i, j):
        h, N = self.h, self.N
        m = max(i, j)
        return h * h * (h * (N - 1 - m) + 1.0 + (self.k[m] if i != j else 0.0))

    def pattern(self, s1, s2, v1=0.0, v2=0.0):
        u = np.ones(self.N)
        u[s1 + 1:s2] = -1.0
        u[s1] = v1
        u[s2] = v2
        return u

    def best_v(self, s1, s2):
        u = self.pattern(s1, s2)
        _, J0, sig = self.sim(u)
        g = np.array([self.h * sig[s1], self.h * sig[s2]])
        Hm = np.array([[self.H(s1, s1), self.H(s1, s2)], [self.H(s1, s2), self.H(s2, s2)]])
        best = None
        for pat in itertools.product((0, 1, 2), repeat=2):
            z = np.array([-1.0 if p == 0 else 1.0 for p in pat])
            free = [i for i in range(2) if pat[i] == 2]
            if free:
                fx = [i for i in range(2) if pat[i] != 2]
                A = Hm[np.ix_(free, free)]
                b = -(g[free] + Hm[np.ix_(free, fx)] @ z[fx]) if fx else -g[free]
                if abs(np.linalg.det(A)) < 1e-300:
                    continue
                sol = np.linalg.solve(A, b)
                if np.any(sol < -1) or np.any(sol > 1):
                    continue
                z[free] = sol
            val = g @ z + z @ Hm @ z / 2
            if best is None or val < best[0]:
                best = (val, z.copy())
        return J0 + best[0], best[1]


def kkt_search(toy, s1, s2, W, R):
    N = toy.N
    memo = {}

    def ev(a, b):
        if not (1 <= a < b - 1 and b < N - 1):
            return np.inf, None
        if (a, b) not in memo:
            memo[(a, b)] = toy.best_v(a, b)
        return memo[(a, b)]
    cur = (s1, s2)
    for _ in range(10):
        changed = False
        for j in (0, 1):
            cands = [(m, cur[1]) if j == 0 else (cur[0], m) for m in range(cur[j] - W, cur[j] + W + 1)]
            best = min(cands, key=lambda c: ev(*c)[0])
            if ev(*best)[0] < ev(*cur)[0] - 1e-15:
                cur, changed = best, True
        if not changed:
            break
    # full 2-D scan around
    cands = [(a, b) for a in range(cur[0] - R, cur[0] + R + 1) for b in range(cur[1] - R, cur[1] + R + 1)]
    best = min(cands, key=lambda c: ev(*c)[0])
    Jb, v = ev(*best)
    # second-best distinct KKT candidates (for information)
    u = toy.pattern(best[0], best[1], v[0], v[1])
    x, J, sig = toy.sim(u)
    tol = 1e-9 * toy.h
    frac = [t for t in range(N) if -1 + 1e-12 < u[t] < 1 - 1e-12]
    viol = 0.0
    for t in range(N):
        if t in frac:
            viol = max(viol, abs(sig[t]))
        elif u[t] >= 1 - 1e-12:
            viol = max(viol, max(0.0, sig[t]))
        else:
            viol = max(viol, max(0.0, -sig[t]))
    return dict(s1s2=best, v=v.tolist(), J=J, u=u, x=x, sig=sig, frac=frac, kkt_viol=viol, nev=len(memo))


def rmax(toy, u, sig, frac, fixed=()):
    N, h, k = toy.N, toy.h, toy.k
    P = [None] * (N + 1)
    P[N] = 1.0
    fr = set(frac)
    for t in range(N - 1, -1, -1):
        if t in fixed:
            P[t] = h + P[t + 1]
            continue
        beta = P[t + 1] + k[t]
        s = 0.0 if t in fr else abs(sig[t])
        m = s / h + P[t + 1]
        if m <= 0:
            return P, t
        P[t] = h + P[t + 1] - beta * beta / m
    return P, None


def coarse_switches(toy0):
    """Brute force over all monotone patterns at the coarse grid of toy0 (its own N)."""
    N = toy0.N
    best = None
    for s1 in range(1, N - 3):
        for s2 in range(s1 + 2, N - 1):
            J, v = toy0.best_v(s1, s2)
            if best is None or J < best[0]:
                best = (J, s1, s2)
    return best[1] / N * T, best[2] / N * T


def run(cfg, Ns, W=None, R=12, Nc=200, out=None):
    t1, t2, k1, k2, tk = cfg
    tau = coarse_switches(Toy(t1, t2, k1, k2, tk, Nc))
    recs = []
    for N in Ns:
        t0 = time.time()
        toy = Toy(t1, t2, k1, k2, tk, N)
        s1g, s2g = int(round(tau[0] / T * N)), int(round(tau[1] / T * N))
        r = kkt_search(toy, s1g, s2g, W if W else max(6, N // 50), R)
        u, sig, frac = r["u"], r["sig"], r["frac"]
        P, br = rmax(toy, u, sig, frac)
        h = toy.h
        s1 = next(t for t in range(1, N) if u[t] != u[t - 1])
        s2 = next(t for t in range(s1 + 1, N) if u[t] > -1 and u[t - 1] == -1)
        mk = next(t for t in range(N) if toy.k[t] == k2)
        eta1 = None if (br is not None and br >= s1 + 1) else P[s1 + 1] - (-k1)
        e2 = None if (br is not None and br >= mk) else P[mk] - (-k2) - (s2 - mk) * h
        rec = dict(cfg=cfg, N=N, coarse_tau=tau, s1=s1, s2=s2, frac=frac, v=r["v"], J=r["J"], kkt_viol_over_h=r["kkt_viol"] / h,
                   e2=e2, eta_hat_1=eta1, break_minus_s1=None if br is None else br - s1, sec=round(time.time() - t0, 1))
        print(json.dumps(rec), flush=True)
        recs.append(rec)
    return recs


if __name__ == "__main__":
    which = sys.argv[1]
    Ns = [int(v) for v in sys.argv[2].split(",")]
    CFG = {"m275": ("0.6", "1.4", -0.5, 0.0, "0.59375"), "m085": ("0.5", "1.5", -0.5, 0.0, "0.484375"),
           "m040": ("0.6", "1.4", -0.5, -0.3, "0.59375"), "p160": ("0.5", "1.5", -0.5, -0.3, "0.484375"),
           "m590": ("0.5", "1.5", -1.0, 0.0, "0.5"), "m690": ("0.55", "1.45", -1.0, 0.0, "0.546875"),
           "m490": ("0.45", "1.55", -1.0, 0.0, "0.4375")}
    run(CFG[which], Ns)
