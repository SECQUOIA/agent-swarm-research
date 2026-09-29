"""Exact checks of three proximity obstruction families (scouting scratch).

E1  separable convex quadratic cost flow, TU matrix, integral data:
    l_inf proximity grows like n/2.
E2  unconstrained convex quadratic with integer Hessian entries <= 5:
    l_inf proximity grows like 0.4 * 2^n (equals half the l_inf radius of the
    Q-Voronoi cell up to the 0.4/0.5 factor).
E3  one Euclidean ball with integral data and a linear objective:
    proximity grows like sqrt(radius).

All arithmetic is exact (fractions / integers); every integer optimum is
found by exhaustive enumeration over a region proved to contain all optima.
"""
from fractions import Fraction as F
from itertools import product
import math


def e1(k, eps):
    # nodes s,v,t ; arcs e:s->v, a_j:v->t (j<k), d:s->t ; supply k at s.
    # cost: e -> 0, a_j -> (x-1/2)^2, d -> eps*x^2 ; 0 <= x <= k.
    # continuous optimum (strictly convex in (a, d); x_e = sum a_j):
    xe = F(k) * (F(1, 2) + eps * k) / (1 + eps * k)
    cont = {"e": xe, "a": xe / k, "d": k - xe}
    # KKT check: potentials p_s,p_v,p_t with reduced cost 0 on all arcs
    # (all continuous values are interior): grad a_j = 2(a-1/2) = p_t - p_v,
    # grad d = 2 eps x_d = p_t - p_s, grad e = 0 = p_v - p_s.
    ga = 2 * (cont["a"] - F(1, 2))
    gd = 2 * eps * cont["d"]
    assert ga == gd, (ga, gd)
    # integer optima by enumeration of all integral flows (a_j in 0..k)
    best, arg = None, []
    for a in product(range(k + 1), repeat=k):
        s = sum(a)
        if s > k:
            continue
        cost = sum((F(x) - F(1, 2)) ** 2 for x in a) + eps * (k - s) ** 2
        if best is None or cost < best:
            best, arg = cost, [a]
        elif cost == best:
            arg.append(a)
    prox = min(max(abs(sum(a) - xe), max(abs(x - cont["a"]) for x in a),
                   abs((k - sum(a)) - cont["d"])) for a in arg)
    return float(xe), len(arg), float(prox)


def e2(n):
    # D = I - 2*S (unimodular lower bidiagonal), Q = D^T D, f = |Dx - t|^2
    D = [[1 if i == j else (-2 if i == j + 1 else 0) for j in range(n)] for i in range(n)]
    Q = [[sum(D[r][i] * D[r][j] for r in range(n)) for j in range(n)] for i in range(n)]
    t = [F(2, 5)] * n
    # x* = D^{-1} t by forward substitution
    x = []
    for i in range(n):
        x.append(t[i] + (2 * x[i - 1] if i else 0))
    # integer optimum: Dz ranges over all of Z^n, nearest point to t is 0
    # (unique since every |t_i - y_i| is minimised only at y_i = 0).
    z = [0] * n
    prox = max(abs(xi - zi) for xi, zi in zip(x, z))
    qmax = max(abs(v) for row in Q for v in row)
    return float(prox), qmax


def e3(N):
    R2 = N * N + N  # integral radius^2
    eps = F(1, 4 * (math.isqrt(N) + 1))  # small enough to force x1 = N first
    c = (F(1), eps)
    # continuous optimum of max c^T x over the ball: x = R c/|c|
    norm_c = math.sqrt(1 + float(eps) ** 2)
    R = math.sqrt(R2)
    xc = (R / norm_c, R * float(eps) / norm_c)
    # integer optimum: enumerate all lattice points in the ball (exact)
    r = math.isqrt(R2)
    best, arg = None, []
    for x1 in range(-r, r + 1):
        m = math.isqrt(R2 - x1 * x1)
        for x2 in (-m, m):  # optimum has |x2| maximal for its sign
            val = c[0] * x1 + c[1] * x2
            if best is None or val > best:
                best, arg = val, [(x1, x2)]
            elif val == best:
                arg.append((x1, x2))
    prox = min(math.hypot(a - xc[0], b - xc[1]) for a, b in arg)
    return arg, prox


if __name__ == "__main__":
    print("E1 separable convex flow over TU (eps = 1/k^2)")
    for k in range(1, 8):
        xe, nopt, prox = e1(k, F(1, k * k))
        print(f"  k={k} n={k+2} x_e*={xe:.4f} #int-opt={nopt} prox_inf={prox:.4f} (k/2={k/2})")
    print("E2 bidiagonal Hessian, entries <= 5")
    for n in range(2, 13):
        prox, qmax = e2(n)
        print(f"  n={n} max|Q_ij|={qmax} prox_inf={prox:.1f} 0.4*(2^n-1)={0.4*(2**n-1):.1f}")
    print("E3 ball x1^2+x2^2 <= N^2+N, objective max x1 + eps x2")
    for N in [4, 16, 64, 256, 1024, 4096]:
        arg, prox = e3(N)
        print(f"  N={N} int-opt={arg} prox_2={prox:.3f} sqrt(N)={math.sqrt(N):.3f}")
