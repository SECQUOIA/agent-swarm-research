"""Exact spot check of the revised Section 9.2 rows (kappa = 0, k = 0, kink family), confirmation referee r1.

Switch times tau_j: phase positions of the own float KKT point at N = 16000 (theta = t_n + h (u_n - after) /
(before - after) at a switching stage n).  Family P(t) = 0 before tau_1, -0.3 dist(t, {tau_1, tau_2}) between,
-0.3 (t - tau_2) after; P_i = P(i h).  Window residual (own derivation): for W = [a, b),
  sum_t [h sigma_t om_t + h d_t^2/2 + h k_t d_t om_t] + P_b d_b^2/2 - P_a d_a^2/2,  d_{t+1} = d_t + h om_t,
minimized exactly over d_a in the state box (|x| <= 4) and om_t in U - u_t by face enumeration.
"""
import itertools
import json
import sys
from fractions import Fraction as Fr

sys.path.insert(0, ".")
from c_two import Toy, kkt_search  # noqa: E402
from c_exact import piece, traj, Hij  # noqa: E402

T = Fr(2)


def solve(A, b):
    n = len(b)
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for c in range(n):
        piv = next((r for r in range(c, n) if M[r][c] != 0), None)
        if piv is None:
            return None
        M[c], M[piv] = M[piv], M[c]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c] / M[c][c]
                M[r] = [M[r][j] - f * M[c][j] for j in range(n + 1)]
    return [M[i][n] / M[i][i] for i in range(n)]


def box_min(g, H, lo, hi):
    n = len(g)
    best = None
    for pat in itertools.product((0, 1, 2), repeat=n):
        z = [lo[i] if pat[i] == 0 else hi[i] for i in range(n)]
        free = [i for i in range(n) if pat[i] == 2]
        if free:
            fx = [i for i in range(n) if pat[i] != 2]
            A = [[H[i][j] for j in free] for i in free]
            b = [-(g[i] + sum((H[i][j] * z[j] for j in fx), Fr(0))) for i in free]
            sol = solve(A, b)
            if sol is None or not all(lo[i] <= v <= hi[i] for i, v in zip(free, sol)):
                continue
            for i, v in zip(free, sol):
                z[i] = v
        val = sum(g[i] * z[i] for i in range(n)) + sum(H[i][j] * z[i] * z[j] for i in range(n) for j in range(n)) / 2
        if best is None or val < best:
            best = val
    return best


def window_min(N, x, u, sig, k, P, a, b):
    h = T / N
    m = b - a
    n = 1 + m
    # d_t = d_a + h sum_{a<=s<t} om_s  as a linear form in z = (d_a, om_a..om_{b-1})
    def e(t):
        v = [Fr(0)] * n
        v[0] = Fr(1)
        for s in range(a, t):
            v[1 + s - a] = h
        return v
    g = [Fr(0)] * n
    H = [[Fr(0)] * n for _ in range(n)]

    def add(v1, v2, c):
        for i in range(n):
            for j in range(n):
                H[i][j] += c * v1[i] * v2[j]
    for t in range(a, b):
        et = e(t)
        ft = [Fr(0)] * n
        ft[1 + t - a] = Fr(1)
        g[1 + t - a] += h * sig[t]
        add(et, et, h)
        add(et, ft, h * k[t])
        add(ft, et, h * k[t])
    add(e(b), e(b), P[b])
    add(e(a), e(a), -P[a])
    lo = [(-4 - x[a]) if a > 0 else Fr(0)] + [-1 - u[t] for t in range(a, b)]
    hi = [(4 - x[a]) if a > 0 else Fr(0)] + [1 - u[t] for t in range(a, b)]
    return box_min(g, H, lo, hi)


def exact_point(ft, r, t1, t2):
    N = ft.N
    a = [Fr(v) for v in piece((("0", 4), (t1, -4), (t2, 4)), N)]
    k = [Fr(0)] * N
    u = [Fr(1) if v >= 1 - 1e-12 else Fr(-1) if v <= -1 + 1e-12 else None for v in r["u"]]
    F = [t for t in range(N) if u[t] is None]
    for t in F:
        u[t] = Fr(0)
    if F:
        _, _, sig0 = traj(N, a, k, Fr(-3), Fr(1), u)
        h = T / N
        sol = solve([[Hij(N, k, Fr(1), i, j) for j in F] for i in F], [-h * sig0[i] for i in F])
        for t, v in zip(F, sol):
            u[t] = v
    x, J, sig = traj(N, a, k, Fr(-3), Fr(1), u)
    ok = all((sig[t] == 0) if t in F else (sig[t] <= 0 if u[t] == 1 else sig[t] >= 0) for t in range(N))
    return a, k, u, x, sig, F, ok


def main():
    recs = []
    for (t1, t2) in (("0.65", "1.35"), ("0.7", "1.3")):
        # taus from N = 16000
        ft = Toy(t1, t2, 0.0, 0.0, "1", 16000)
        g = {"0.65": (0.282, 0.357), "0.7": (0.334, 0.361)}[t1]
        r = kkt_search(ft, int(g[0] * 16000), int(g[1] * 16000), 320, 12)
        u = r["u"]
        hf = 2 / 16000
        taus = []
        t = 1
        while t < 16000 and len(taus) < 2:
            if u[t] != u[t - 1]:
                before = u[t - 1]
                after = u[t + 1] if (-1 < u[t] < 1) else u[t]
                taus.append(Fr(t * hf + hf * (u[t] - after) / (before - after)).limit_denominator(10 ** 9))
                t += 2
                continue
            t += 1
        for N in (1000, 2000, 4000):
            ftN = Toy(t1, t2, 0.0, 0.0, "1", N)
            rN = kkt_search(ftN, int(g[0] * N), int(g[1] * N), max(6, N // 50), 12)
            a, k, uN, x, sig, F, ok = exact_point(ftN, rN, t1, t2)
            h = T / N
            mid = (taus[0] + taus[1]) / 2
            P = []
            for i in range(N + 1):
                tt = Fr(i) * T / N
                P.append(Fr(0) if tt <= taus[0] else -Fr(3, 10) * (tt - taus[0]) if tt <= mid
                         else -Fr(3, 10) * (taus[1] - tt) if tt <= taus[1] else -Fr(3, 10) * (tt - taus[1]))
            fails = {}
            for s in range(N):
                L = -window_min(N, x, uN, sig, k, P, s, s + 1)
                if L > 0:
                    fails[s] = L
            wins = {s: [float(-window_min(N, x, uN, sig, k, P, s - K, s + K + 1) / h ** 3) for K in (0, 1)] for s in fails}
            rec = dict(t1=t1, t2=t2, N=N, taus=[float(v) for v in taus], kkt_exact=ok, frac=F,
                       failing_over_h3={s: float(L / h ** 3) for s, L in fails.items()}, windows_K01_over_h3=wins)
            print(json.dumps(rec), flush=True)
            recs.append(rec)
    with open("logs/kink.json", "w") as f:
        json.dump(recs, f, indent=1)


if __name__ == "__main__":
    main()
