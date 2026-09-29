"""Recheck of Proposition 4.7: f = |X1 - X2| + (X1 - X2) y on [0,1]^3, X_k = x_k - a_k,
termwise McCormick on x1*y and -x2*y.  Claims: 0.102/eps <= N_cov <= N_opt <= 1 + 18/eps
(a1 = 1/3, a2 = sqrt2 - 1), via Theorem 3.6 below and a quadtree in (x1, x2) above.

Own code.  Each quadtree leaf is certified *exactly*: the node bound
    LB(C) = min_{x in C} max_k l_k(x)    (8 affine pieces: |D| x vex(x1 y) x vex(-x2 y))
is bounded below by an exact rational dual certificate (convex weights lambda from HiGHS,
rationalised, then min over the box of sum lambda_k l_k computed exactly).  If the certificate
misses -eps, the exact LB is recomputed by rational vertex enumeration.

[1] lower-bound constant tau H^2(S)/9 for a1 = 1/3, a2 = sqrt2 - 1;
[2] quadtree leaves vs 1 + 18/eps, refinements per level vs 6/h, exact validity of every leaf,
    for rational (a1, a2) and several eps.
[3] optimal set: f = 0 exactly on {D = 0} and on {D < 0, y = 1} (random rational points).
"""
from fractions import Fraction as Fr
import itertools
import math
import random
import sys

import numpy as np
from scipy.optimize import linprog


def pieces(box, a1, a2):
    """Affine pieces l(x1, x2, y) = g . (x1, x2, y) + g0 of the node relaxation, as Fractions."""
    l1, u1, l2, u2, ly, uy = box
    dlt = a1 - a2
    absD = [((Fr(1), Fr(-1), Fr(0)), -dlt), ((Fr(-1), Fr(1), Fr(0)), dlt)]
    # vex(x1 y) = max(ly x1 + l1 y - l1 ly, uy x1 + u1 y - u1 uy)
    v1 = [((ly, Fr(0), l1), -l1 * ly), ((uy, Fr(0), u1), -u1 * uy)]
    # vex(-x2 y) = max(-(uy x2 + l2 y - l2 uy), -(ly x2 + u2 y - u2 ly))
    v2 = [((Fr(0), -uy, -l2), l2 * uy), ((Fr(0), -ly, -u2), u2 * ly)]
    lin = ((Fr(0), Fr(0), a2 - a1), Fr(0))       # (a2 - a1) y
    out = []
    for p, q, r in itertools.product(absD, v1, v2):
        g = tuple(p[0][i] + q[0][i] + r[0][i] + lin[0][i] for i in range(3))
        out.append((g, p[1] + q[1] + r[1] + lin[1]))
    return out


def box_min_affine(g, g0, box):
    l1, u1, l2, u2, ly, uy = box
    lo = (l1, l2, ly); hi = (u1, u2, uy)
    return g0 + sum(g[i] * (lo[i] if g[i] >= 0 else hi[i]) for i in range(3))


def solve_lin(A, b):
    n = len(A)
    M = [list(A[i]) + [b[i]] for i in range(n)]
    for col in range(n):
        piv = next((r for r in range(col, n) if M[r][col] != 0), None)
        if piv is None:
            return None
        M[col], M[piv] = M[piv], M[col]
        for r in range(n):
            if r != col and M[r][col] != 0:
                f = M[r][col] / M[col][col]
                M[r] = [M[r][k] - f * M[col][k] for k in range(n + 1)]
    return [M[i][n] / M[i][i] for i in range(n)]


def exact_lb(box, P):
    """min s s.t. s >= l_k(x), x in box: rational vertex enumeration in (x1, x2, y, s)."""
    l1, u1, l2, u2, ly, uy = box
    G, h = [], []   # G z >= h, z = (x1, x2, y, s)
    for (g, g0) in P:
        G.append([-g[0], -g[1], -g[2], Fr(1)]); h.append(g0)
    for i, (lo, hi) in enumerate(((l1, u1), (l2, u2), (ly, uy))):
        e = [Fr(0)] * 4; e[i] = Fr(1); G.append(e); h.append(lo)
        e = [Fr(0)] * 4; e[i] = Fr(-1); G.append(e); h.append(-hi)
    best = None
    for S in itertools.combinations(range(len(G)), 4):
        z = solve_lin([G[i] for i in S], [h[i] for i in S])
        if z is None:
            continue
        if all(sum(G[i][k] * z[k] for k in range(4)) >= h[i] for i in range(len(G))):
            best = z[3] if best is None else min(best, z[3])
    return best


def certified_lb(box, a1, a2, eps):
    """Return (certified lower bound on LB(C), method)."""
    P = pieces(box, a1, a2)
    A = np.array([[float(g[0]), float(g[1]), float(g[2]), -1.0] for g, _ in P])
    b = np.array([-float(g0) for _, g0 in P])
    l1, u1, l2, u2, ly, uy = box
    res = linprog([0, 0, 0, 1], A_ub=A, b_ub=b,
                  bounds=[(float(l1), float(u1)), (float(l2), float(u2)), (float(ly), float(uy)), (None, None)],
                  method="highs")
    if res.status == 0:
        lam = [max(Fr(-m).limit_denominator(10 ** 9), Fr(0)) for m in res.ineqlin.marginals]
        s = sum(lam)
        if s > 0:
            lam = [x / s for x in lam]
            g = tuple(sum(lam[k] * P[k][0][i] for k in range(8)) for i in range(3))
            g0 = sum(lam[k] * P[k][1] for k in range(8))
            cert = box_min_affine(g, g0, box)
            if cert >= -eps:
                return cert, "dual"
    return exact_lb(box, P), "enum"


def quadtree(a1, a2, eps):
    """Leaves of the review's quadtree (full y-range); refinement counts per side h."""
    dlt = a1 - a2
    leaves, refined = [], {}
    stack = [(Fr(0), Fr(0), Fr(1))]
    while stack:
        x1, x2, h = stack.pop()
        lo = (x1 - x2 - h) - dlt
        hi = (x1 - x2 + h) - dlt
        mind = Fr(0) if lo <= 0 <= hi else min(abs(lo), abs(hi))
        if h <= 2 * eps or mind >= 2 * h:
            leaves.append((x1, x1 + h, x2, x2 + h, Fr(0), Fr(1)))
        else:
            refined[h] = refined.get(h, 0) + 1
            h2 = h / 2
            for dx, dy in ((0, 0), (h2, 0), (0, h2), (h2, h2)):
                stack.append((x1 + dx, x2 + dy, h2))
    return leaves, refined


def part1():
    print("[1] lower bound tau H^2(S)/9 with tau = 1/sqrt2 (a1 = 1/3, a2 = sqrt2 - 1)")
    a1, a2 = 1 / 3, math.sqrt(2) - 1
    d = abs(a1 - a2)
    length = math.sqrt(2) * (1 - d)          # segment x1 - x2 = a1 - a2 in the unit square
    print(f"    H^2(S) = {length:.5f};  tau H^2 / 9 = {length / math.sqrt(2) / 9:.5f}  (note: 0.102)")
    # tau(V, E) for the plane spanned by (1,1,0)/sqrt2 and e_y: W_x1 = W_x2 = W_t1/sqrt2, W_y = W_t2,
    # so max_E W_i W_j / area = W_t1 W_t2 / (sqrt2 area) >= 1/sqrt2, with equality for rectangles.
    print("    tau: W_t1 W_t2 >= area for every convex body, equality for axis rectangles -> 1/sqrt2")


def part2():
    print("[2] quadtree: leaf counts, per-level refinements, exact validity of every leaf")
    configs = [(Fr(1, 3), Fr(41421356, 10 ** 8)), (Fr(1, 2), Fr(1, 2)), (Fr(1, 7), Fr(5, 6))]
    for a1, a2 in configs:
        for eps in (Fr(1, 10), Fr(1, 30), Fr(1, 100), Fr(1, 300)):
            leaves, refined = quadtree(a1, a2, eps)
            worst = None; nenum = 0
            for C in leaves:
                cert, how = certified_lb(C, a1, a2, eps)
                nenum += how == "enum"
                worst = cert if worst is None else min(worst, cert)
            lvl_ok = all(n <= 6 / h for h, n in refined.items())
            print(f"    a=({float(a1):.4f},{float(a2):.4f}) eps={eps}: leaves={len(leaves)} "
                  f"(1+18/eps={float(1 + 18 / eps):.0f}, leaves*eps={float(len(leaves) * eps):.2f}); "
                  f"refinements<=6/h per level: {lvl_ok}; min certified LB / eps = {float(worst / eps):.4f} "
                  f"(valid iff >= -1); exact enumerations: {nenum}")
            sys.stdout.flush()


def part3():
    print("[3] optimal set (d)")
    rng = random.Random(5)
    bad = 0
    for _ in range(3000):
        a1, a2 = Fr(rng.randint(1, 99), 100), Fr(rng.randint(1, 99), 100)
        x1, x2, y = Fr(rng.randint(0, 100), 100), Fr(rng.randint(0, 100), 100), Fr(rng.randint(0, 100), 100)
        if rng.random() < 0.3:
            x2 = x1 - a1 + a2
        if rng.random() < 0.3:
            y = Fr(1)
        D = x1 - a1 - x2 + a2
        f = abs(D) + D * y
        predicted_zero = (D == 0) or (D < 0 and y == 1)
        bad += (f < 0) or ((f == 0) != predicted_zero)
    print(f"    3000 rational points: f >= 0 and (f = 0 iff D = 0 or (D < 0, y = 1)); mismatches {bad}")


if __name__ == "__main__":
    part1(); part3(); part2()
