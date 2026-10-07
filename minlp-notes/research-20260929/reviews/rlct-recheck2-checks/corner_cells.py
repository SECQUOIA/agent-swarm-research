"""Second recheck: the step N_v <= J_v of Theorem 3.3 on face4d.

m = x(1-x) + y^4 + z^4 + w^4 on [0,0.9] x [-0.4,0.5]^3, exact alphaBB with
alpha = alpha' = 1.05, UBD = f* = 0, prune iff LB >= -eps.  For every vertex v
and level j = 1..30, the corner cell with vertex v is tested.  The lower bound
is a sum of one-dimensional convex minima (golden-section search, 200 steps).
Reports N_v (non-pruned corner levels) and J_v = #{j >= 1 : m(v) <= Lambda_1 s_j^2},
with Lambda_0 = alpha' n/4, M = 3 (largest |Hessian eigenvalue| on X0: max(2, 12*0.5^2)),
Lambda_1 = ((n+2)^2/4)(Lambda_0 + M).
Usage: python3 corner_cells.py > logs/corner_cells.log
"""
import itertools
import math

ALPHA = 1.05
LO = [0.0, -0.4, -0.4, -0.4]
HI = [0.9, 0.5, 0.5, 0.5]
PHI = [lambda t: t * (1 - t), lambda t: t ** 4, lambda t: t ** 4, lambda t: t ** 4]
n = 4
LAM0 = ALPHA * n / 4
M = 3.0
LAM1 = ((n + 2) ** 2 / 4) * (LAM0 + M)
S0 = 0.9


def min1d(phi, a, b):
    g = lambda t: phi(t) - ALPHA * (t - a) * (b - t)
    lo, hi = a, b
    r = (math.sqrt(5) - 1) / 2
    for _ in range(200):
        c, d = hi - r * (hi - lo), lo + r * (hi - lo)
        if g(c) <= g(d):
            hi = d
        else:
            lo = c
    return min(g(a), g(b), g((lo + hi) / 2))


def main():
    for eps in (1e-3, 1e-8, 1e-14):
        print(f"eps = {eps:.0e}")
        worst = 0
        for corner in itertools.product((0, 1), repeat=n):
            v = [HI[i] if corner[i] else LO[i] for i in range(n)]
            mv = sum(PHI[i](v[i]) for i in range(n))
            Nv = 0
            for j in range(1, 31):
                s = [(HI[i] - LO[i]) * 2.0 ** -j for i in range(n)]
                cell = [(v[i] - s[i], v[i]) if corner[i] else (v[i], v[i] + s[i]) for i in range(n)]
                lb = sum(min1d(PHI[i], *cell[i]) for i in range(n))
                if lb < -eps:
                    Nv += 1
            Jv = sum(1 for j in range(1, 200) if mv <= LAM1 * (S0 * 2.0 ** -j) ** 2) if mv > 0 else None
            ok = "" if Jv is None else ("ok" if Nv <= Jv else "VIOLATION")
            if Jv is not None:
                worst = max(worst, Nv - Jv)
            print(f"  v = {v}: m(v) = {mv:.4f}, N_v = {Nv}, J_v = {Jv} {ok}")
        print(f"  max over non-optimal vertices of N_v - J_v: {worst}")


if __name__ == "__main__":
    main()
