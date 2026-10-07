"""Exact check of Remark rem:falseguess (appendix-proximal.tex) and of the
budgets J_K of Theorem thm:diagdiscovery for that instance.

F = x^2 + y^2 - 3xy + 63/128 (x+y) on [0,1]^2.
Proximal stage as in Appendix B: fresh box X cap [c +- rho h], graded grid
from c with step h + theta t, corrections L w^2/8, proximal weight
eta = L theta^2/4, brute-force minimization (n = 2).
Run: python3 -B r3_falseguess.py
"""
from fractions import Fraction as Fr
from math import isqrt

L = Fr(2)


def F(x, y):
    return x * x + y * y - 3 * x * y + Fr(63, 128) * (x + y)


def graded(c, lo, hi, h, th):
    nodes = {c}
    t = Fr(0)
    while t < hi - c:
        t = min(t + h + th * t, hi - c)
        nodes.add(c + t)
    t = Fr(0)
    while t < c - lo:
        t = min(t + h + th * t, c - lo)
        nodes.add(c - t)
    return sorted(nodes)


def corr(nodes):
    d = {}
    for k, v in enumerate(nodes):
        w = Fr(0)
        if k > 0:
            w = max(w, v - nodes[k - 1])
        if k + 1 < len(nodes):
            w = max(w, nodes[k + 1] - v)
        d[v] = L * w * w / 8
    return d


def ceil_sqrt(m):
    r = isqrt(m)
    return r if r * r == m else r + 1


def run(K, stages):
    mu = 2
    while Fr(K, 4 ** mu) > Fr(1, 8):
        mu += 1
    th = Fr(1, 2 ** mu)
    eta = L * th * th / 4
    rho = 2 * ceil_sqrt(2 * K)  # n = 2
    c = (Fr(0), Fr(0))
    out = []
    for j in range(stages + 1):
        h = Fr(1, 2 ** j)
        grids = []
        for ci in c:
            lo, hi = max(Fr(0), ci - rho * h), min(Fr(1), ci + rho * h)
            grids.append(graded(ci, lo, hi, h, th))
        d0, d1 = corr(grids[0]), corr(grids[1])
        best, arg, ties = None, None, 0
        for a in grids[0]:
            for b in grids[1]:
                P = F(a, b) - d0[a] - d1[b] + eta * ((a - c[0]) ** 2 + (b - c[1]) ** 2)
                if best is None or P < best:
                    best, arg, ties = P, (a, b), 1
                elif P == best:
                    ties += 1
        out.append((j, arg, ties, len(grids[0]), len(grids[1])))
        c = arg
    return mu, out


if __name__ == "__main__":
    # budgets J_K: tau = 1/(4 n R), R = Delta * prod P_ii, Delta = 128
    Delta = 128
    R = Delta * (Delta * 2) * (Delta * 2)
    tau = Fr(1, 4 * 2 * R)
    for K in [1, 2, 4]:
        J = 0
        while 4 ** J * tau * tau < 4 * K * 2 * 1:
            J += 1
        print(f"K={K}: J_K={J}")
    ok_all = True
    for K in [1, 2, 4]:
        mu, out = run(K, 33)
        origin = all(arg == (0, 0) for _, arg, _, _, _ in out)
        unique = all(t == 1 for _, _, t, _, _ in out)
        maxg = max(max(g0, g1) for *_, g0, g1 in out)
        print(f"K={K} (mu={mu}): origin at all stages 0..33: {origin}; unique argmin: {unique};"
              f" max grid size {maxg}")
        ok_all &= origin
    print("PASS rem:falseguess" if ok_all else "FAIL rem:falseguess")
    # matrices
    H = [[2, -3], [-3, 2]]
    lam0 = 2 * Fr(63, 128)
    print("H+Lambda at origin diag:", 2 + lam0, "eigs:", 2 + lam0 - 3, 2 + lam0 + 3)
    g1 = 2 - 3 + Fr(63, 128)
    lam1 = 2 * abs(g1)
    print("at (1,1): grad", g1, "diag", 2 + lam1, "min eig", 2 + lam1 - 3)
