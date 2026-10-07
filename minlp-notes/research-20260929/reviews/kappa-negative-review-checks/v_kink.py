"""Reviewer's exact spot check of kappa-negative.md Section 9.2 (kappa = 0 two-switch toy, kink family).
Own taus (float KKT at N = 16000 by v_close's scan), own exact KKT point, stage losses by direct 2-variable
box minimization of the residual (vtoy.stage_min_direct), and window minima of
J_W(z) - J_W(zbar), J_W = sum_{t in W} L_t + S_b(x_b) - S_a(x_a), over (d_a, om_a, ..., om_{b-1}) in the box,
by exact coefficient recovery and face enumeration.
usage: python3 v_kink.py f:t1 f:t2 N m1 m2
"""
import itertools
import json
import sys
from fractions import Fraction as Fr

import numpy as np

from vtoy import traj, kkt_check, stage_min_direct, coord_refine, Toy
from v_two import toy2, scan, pattern
from v_close import data as fdata, kkt_point


def taus_16000(t1f, t2f, guess):
    N = 16000
    a, k = fdata(0.0, 0.0, t1f, t2f, 1.0, N)
    u, sig, frac, viol, J = kkt_point(N, a, k, guess)
    h = 2.0 / N
    out = []
    t = 1
    while t < N and len(out) < 2:
        if u[t] != u[t - 1]:
            before = u[t - 1]
            after = u[t + 1] if -1 < u[t] < 1 else u[t]
            out.append(Fr(t * h + h * (u[t] - after) / (before - after)).limit_denominator(10 ** 9))
            t += 2
            continue
        t += 1
    return out


def kink_P(N, taus, c=Fr(3, 10)):
    t1, t2 = taus
    mid = (t1 + t2) / 2
    P = []
    for i in range(N + 1):
        t = Fr(i) * 2 / N
        if t <= t1:
            v = Fr(0)
        elif t <= mid:
            v = -c * (t - t1)
        elif t <= t2:
            v = -c * (t2 - t)
        else:
            v = -c * (t - t2)
        P.append(v)
    return P


def window_min(toy, E, P, a, b):
    h, x, u, p, at, k = E["h"], E["x"], E["u"], E["p"], E["a"], E["k"]
    R = toy.R
    n = 1 + (b - a)

    def JW(v):
        xa = x[a] + v[0]
        xx = xa
        tot = Fr(0)
        for i, t in enumerate(range(a, b)):
            ut = u[t] + v[1 + i]
            tot += h * ((xx - at[t]) ** 2 / 2 + k[t] * xx * ut)
            xx = xx + h * ut
        Sb = p[b] * xx + P[b] * (xx - x[b]) ** 2 / 2
        Sa = p[a] * xa + P[a] * (xa - x[a]) ** 2 / 2
        return tot + Sb - Sa
    z0 = [Fr(0)] * n
    f0 = JW(z0)
    e = lambda i, s=1: [Fr(s) if j == i else Fr(0) for j in range(n)]
    g = [(JW(e(i)) - JW(e(i, -1))) / 2 for i in range(n)]
    H = [[None] * n for _ in range(n)]
    for i in range(n):
        H[i][i] = JW(e(i)) + JW(e(i, -1)) - 2 * f0
    for i in range(n):
        for j in range(i + 1, n):
            vij = [Fr(0)] * n; vij[i] = Fr(1); vij[j] = Fr(1)
            H[i][j] = H[j][i] = JW(vij) - f0 - g[i] - g[j] - H[i][i] / 2 - H[j][j] / 2
    lo = [(-R - x[a]) if a > 0 else Fr(0)] + [Fr(-1) - u[t] for t in range(a, b)]
    hi = [(R - x[a]) if a > 0 else Fr(0)] + [Fr(1) - u[t] for t in range(a, b)]
    best = None
    for pat in itertools.product((0, 1, 2), repeat=n):
        z = [lo[i] if pat[i] == 0 else hi[i] for i in range(n)]
        free = [i for i in range(n) if pat[i] == 2]
        if free:
            fx = [i for i in range(n) if pat[i] != 2]
            A = [[H[i][j] for j in free] for i in free]
            rhs = [-(g[i] + sum((H[i][j] * z[j] for j in fx), Fr(0))) for i in free]
            M = [row[:] + [r] for row, r in zip(A, rhs)]
            m = len(free)
            ok = True
            for c in range(m):
                piv = next((r for r in range(c, m) if M[r][c] != 0), None)
                if piv is None:
                    ok = False
                    break
                M[c], M[piv] = M[piv], M[c]
                for r in range(m):
                    if r != c and M[r][c] != 0:
                        fct = M[r][c] / M[c][c]
                        M[r] = [M[r][q] - fct * M[c][q] for q in range(m + 1)]
            if not ok:
                continue
            sol = [M[i][m] / M[i][i] for i in range(m)]
            if not all(lo[i] <= s <= hi[i] for i, s in zip(free, sol)):
                continue
            for i, s in zip(free, sol):
                z[i] = s
        val = sum(g[i] * z[i] for i in range(n)) + sum(H[i][j] * z[i] * z[j] for i in range(n) for j in range(n)) / 2
        if best is None or val < best:
            best = val
    return best


def main():
    t1s, t2s, N, m1, m2 = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
    t1f, t2f = float(t1s[2:]), float(t2s[2:])
    toy = toy2(Fr(0), Fr(t1f), Fr(t2f))
    res = scan(toy, N, m1, m2, 4)
    J, a1, v1, a2, v2 = res[0]
    E = traj(toy, N, pattern(N, a1, v1, a2, v2))
    ok, frac = kkt_check(E)
    assert ok
    h = E["h"]
    taus = taus_16000(t1f, t2f, (m1 * 2.0 / N, m2 * 2.0 / N))
    P = kink_P(N, taus)
    losses = {t: stage_min_direct(toy, E, P, t, Fr(-1), Fr(1)) for t in range(N)}
    fail = [t for t, v in losses.items() if v > 0]
    wins = {t: [float(-window_min(toy, E, P, t - K, t + K + 1) / h ** 3) for K in (0, 1)] for t in fail}
    print(json.dumps(dict(t1=t1f, t2=t2f, N=N, taus=[float(v) for v in taus], frac=frac,
                          failing=[(t, float(losses[t] / h ** 3)) for t in fail], window_deficits_h3_K01=wins)), flush=True)


if __name__ == "__main__":
    main()
