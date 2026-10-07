"""R1 check of Proposition prop:sharp and Corollary cor:uniformgrid (growth-sharp.tex).

F = sum_k [Lam/2 (u_k^2+v_k^2) + sig u_k v_k] on [-1,1]^n, n=2m.
Filtered uniform grids (theta=0), centered at 0, mesh h_j = 2^{1-j}.
Q separates over pairs, so min-marginals are computed exactly per pair.
"""
import math
from fractions import Fraction as Fr


def uniform_grid(lo, hi, c, h):
    nodes = {c, lo, hi}
    t = c
    while t + h < hi:
        t += h; nodes.add(t)
    t = c
    while t - h > lo:
        t -= h; nodes.add(t)
    return sorted(nodes)


def wmap(g):
    w = {}
    for k, v in enumerate(g):
        cand = [Fr(0)]
        if k > 0:
            cand.append(v - g[k - 1])
        if k + 1 < len(g):
            cand.append(g[k + 1] - v)
        w[v] = max(cand)
    return w


def run(m, Lam, sig, stages=9):
    n = 2 * m
    kappa = 2 * Lam / (Lam - sig)
    r = math.floor(math.sqrt((n - 2) * kappa / 16))
    box = [(Fr(-1), Fr(1))] * n
    out = []
    for j in range(stages):
        h = Fr(2, 2**j)
        G = [uniform_grid(box[i][0], box[i][1], Fr(0), h) for i in range(n)]
        W = [wmap(g) for g in G]
        # pair tables
        q = []
        for k in range(m):
            gu, gv, wu, wv = G[2 * k], G[2 * k + 1], W[2 * k], W[2 * k + 1]
            q.append({(a, b): Lam / 2 * (a * a + b * b) + sig * a * b - Lam / 8 * (wu[a] ** 2 + wv[b] ** 2)
                      for a in gu for b in gv})
        mins = [min(t.values()) for t in q]
        tot = sum(mins)
        beta = tot
        # corrected minimizer 0?
        argmins = [min((key for key in t if t[key] == mn)) for t, mn in zip(q, mins)]
        zero_unique = all(len([key for key in t if t[key] == mn]) == 1 and key0 == (0, 0)
                          for t, mn, key0 in zip(q, mins, argmins))
        U = Fr(0)  # incumbent F(0)=0 found at stage 0
        newbox = []
        sharp_ok = True
        for i in range(n):
            k, pos = divmod(i, 2)
            t = q[k]
            rest = tot - mins[k]
            mm = {}
            for a in G[i]:
                mm[a] = (min(t[(a, b)] for b in G[i + 1]) if pos == 0 else min(t[(b, a)] for b in G[i - 1])) + rest
            rho = min(-box[i][0], box[i][1])
            bound = min(rho, h * Fr(math.isqrt(int((n - 2) * kappa * 10**8 // 16)), 10**4))
            for a in G[i]:
                if abs(a) <= bound and mm[a] > U:
                    sharp_ok = False
            g = G[i]
            kept = [(a, b) for a, b in zip(g[:-1], g[1:]) if min(mm[a], mm[b]) <= U]
            newbox.append((min(x[0] for x in kept), max(x[1] for x in kept)))
        box = newbox
        nxt = len(uniform_grid(box[0][0], box[0][1], Fr(0), h / 2))
        out.append((j, zero_unique, sharp_ok, float(box[0][1]), (r + 1) * h <= 1, nxt, 4 * r + 5))
    return kappa, r, out


for m, Lam, sig in [(2, Fr(2), Fr(19, 10)), (3, Fr(2), Fr(39, 20)), (5, Fr(4), Fr(15, 4)), (8, Fr(2), Fr(19, 10))]:
    kappa, r, out = run(m, Lam, sig)
    print(f"m={m} n={2*m} kappa={float(kappa):.1f} r={r}")
    for j, zu, so, rad, cond, nxt, need in out:
        flag = "" if (not cond or j == 0 or nxt >= need) else "  <-- FAIL count"
        print(f"  j={j} zero_unique_min={zu} sharp_ok={so} retained_halfwidth={rad:.5f} (r+1)h<=1:{cond} next_nodes={nxt} 4r+5={need}{flag}")
