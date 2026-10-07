"""Reviewer's float re-check of kappa-negative.md Section 9.3 (close switches, k jumps at tk) and 9.4-style
recursion.  Own KKT search (two-switch pattern scan with exact-in-float 2-D QP per pattern) and own
maximal recursion (extension-n2.md Lemma 10, scalar, Delta = 2, eps = 0, P_N = phi2 = 1).
Data convention as in the author's code: jump times compared as Fraction(float(t_i)).
usage: python3 v_close.py  (runs the configurations listed in CONFIGS)
"""
import itertools
import json
import math
from fractions import Fraction as Fr

import numpy as np

from vtoy import Toy

# (k1, k2, t1, t2, tk, guess switch times) ; kappa = -k
CONFIGS = [
    (-1.0, 0.0, 0.5, 1.5, 0.5, (0.3, 0.71)),
    (-1.0, 0.0, 0.55, 1.45, 0.546875, (0.43, 0.735)),
    (-1.0, 0.0, 0.45, 1.55, 0.453125, (0.19, 0.705)),
    (-0.5, 0.0, 0.6, 1.4, 0.59375, (0.5, 0.725)),
    (-0.5, 0.0, 0.5, 1.5, 0.484375, (0.29, 0.705)),
    (-0.5, -0.3, 0.6, 1.4, 0.59375, (0.52, 0.68)),
    (0.0, -1.0, 0.5, 1.5, 0.5, (0.365, 0.565)),
    (-0.3, -0.5, 0.65, 1.35, 0.640625, (0.63, 0.645)),
]


def data(k1, k2, t1, t2, tk, N):
    toy = Toy(a_pts=((0, 4), (Fr(float(t1)), -4), (Fr(float(t2)), 4)), k_pts=((0, k1), (Fr(float(tk)), k2)),
              phi1=-3, phi2=1, R=4)
    a, k = toy.data(N)
    return np.array([float(v) for v in a]), np.array([float(v) for v in k])


def sim(N, a, k, u):
    h = 2.0 / N
    x = np.concatenate([[0.0], np.cumsum(h * u)])
    J = h * np.sum((x[:N] - a) ** 2 / 2 + k * x[:N] * u) - 3 * x[N] + x[N] ** 2 / 2
    p = np.empty(N + 1)
    p[N] = -3 + x[N]
    inc = h * (x[:N] - a + k * u)
    p[:N] = p[N] + np.cumsum(inc[::-1])[::-1]
    sig = k * x[:N] + p[1:]
    return J, x, sig


def Hent(N, k, i, j):
    h = 2.0 / N
    m = max(i, j)
    return h * h * (h * (N - 1 - m) + 1.0 + (k[m] if i != j else 0.0))


def qp2(g, H):
    best = None
    for pat in itertools.product((0, 1, 2), repeat=2):
        z = [-1.0 if p == 0 else 1.0 for p in pat]
        free = [i for i in range(2) if pat[i] == 2]
        if len(free) == 1:
            i = free[0]; j = 1 - i
            if H[i][i] <= 0:
                continue
            z[i] = -(g[i] + H[i][j] * z[j]) / H[i][i]
            if abs(z[i]) > 1:
                continue
        elif len(free) == 2:
            det = H[0][0] * H[1][1] - H[0][1] ** 2
            if det == 0:
                continue
            z = [(-g[0] * H[1][1] + H[0][1] * g[1]) / det, (H[0][1] * g[0] - H[0][0] * g[1]) / det]
            if max(abs(z[0]), abs(z[1])) > 1:
                continue
        val = g[0] * z[0] + g[1] * z[1] + (H[0][0] * z[0] ** 2 + 2 * H[0][1] * z[0] * z[1] + H[1][1] * z[1] ** 2) / 2
        if best is None or val < best[0]:
            best = (val, z)
    return best


def kkt_point(N, a, k, guess):
    h = 2.0 / N
    g1, g2 = int(round(guess[0] / h)), int(round(guess[1] / h))
    W = max(8, int(0.004 * N))
    best = None
    for m1 in range(g1 - W, g1 + W + 1):
        for m2 in range(max(m1 + 2, g2 - W), g2 + W + 1):
            u = np.ones(N)
            u[m1:m2] = -1.0
            u[m1] = 0.0; u[m2] = 0.0
            J0, x, sig = sim(N, a, k, u)
            g = [h * sig[m1], h * sig[m2]]
            H = [[Hent(N, k, m1, m1), Hent(N, k, m1, m2)], [Hent(N, k, m2, m1), Hent(N, k, m2, m2)]]
            val, z = qp2(g, H)
            if best is None or J0 + val < best[0]:
                uu = u.copy(); uu[m1], uu[m2] = z
                best = (J0 + val, uu)
    u = best[1]
    J, x, sig = sim(N, a, k, u)
    tol = 1e-11
    frac = [t for t in range(N) if -1 + 1e-12 < u[t] < 1 - 1e-12]
    viol = max([0.0] + [max(0.0, sig[t]) for t in range(N) if u[t] >= 1 - 1e-12] +
               [max(0.0, -sig[t]) for t in range(N) if u[t] <= -1 + 1e-12] + [abs(sig[t]) for t in frac])
    return u, sig, frac, viol, J


def rmax(N, k, sig, frac):
    h = 2.0 / N
    P = np.empty(N + 1)
    P[N] = 1.0
    fr = set(frac)
    for t in range(N - 1, -1, -1):
        beta = P[t + 1] + k[t]
        s = 0.0 if t in fr else abs(sig[t])
        m = s / h + P[t + 1]
        if m <= 0:
            return t
        P[t] = h + P[t + 1] - beta * beta / m
    return None


def main():
    for (k1, k2, t1, t2, tk, guess) in CONFIGS:
        row = []
        for N in (1000, 2000, 4000, 8000):
            a, k = data(k1, k2, t1, t2, tk, N)
            u, sig, frac, viol, J = kkt_point(N, a, k, guess)
            sw = [t for t in range(1, N) if u[t] != u[t - 1]]
            s1 = sw[0]
            br = rmax(N, k, sig, frac)
            row.append(dict(N=N, kkt_viol=viol, frac=frac, s1=s1, brk=br, brk_minus_s1=None if br is None else br - s1))
        h = 2.0 / 8000
        print(json.dumps(dict(kappa1=-k1, kappa2=-k2, t1=t1, t2=t2, tk=tk, runs=row)), flush=True)


if __name__ == "__main__":
    main()
