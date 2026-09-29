"""Reviewer's independent spot checks (own code).

[J]   Lemma 3.1: integral of min(xi*eta, (1-xi)(1-eta))^(-s) over the unit square (direct 2D quadrature
      of the min form, split along xi+eta=1) against 2 Gamma(1-s)^2/Gamma(3-2s); divergence at s = 1
      shown by truncation at distance delta from the corners.
[ENV] Lemmas 2.3/2.4 for JOINT envelopes of random trilinear functions on random boxes in R^3:
      vex computed by the vertex LP (8 vertices); check vex(x) <= phi(x) - |d_ij phi| d_i d_j and
      the chord bound along e_i - sign(d_ij phi) e_j.
[TILT] Proposition 3.13 upper construction: max over a fine grid of Gamma - m - eps on all 2K boxes.
[FO]  Theorem 6.1(b): the first-order scheme McCormick - 0.2 min(x-l, u-x) on the two boxes x<=a, x>=a.
[OBL] Theorem 5.3 for widest-side bisection (beta = 1/2): average over the non-dyadic grid a_k = (k + 1/sqrt2)/64.
"""
import math
import itertools
import random
import numpy as np
import mpmath as mp
from scipy.optimize import linprog
from kink_rules import run, relax, rule_bisect


def part_J():
    for s in (0.25, 0.5, 0.75, 0.9):
        f = lambda xi, eta: min(xi * eta, (1 - xi) * (1 - eta)) ** (-s)
        # region xi+eta<=1 uses xi*eta; the other half is symmetric
        half = mp.quad(lambda xi: mp.quad(lambda eta: (xi * eta) ** (-s), [0, 1 - xi]), [0, 1])
        closed = 2 * mp.gamma(1 - s) ** 2 / mp.gamma(3 - 2 * s)
        print(f"[J] s={s}: 2*quad = {float(2 * half):.6f}, closed form = {float(closed):.6f}, "
              f"bound 2.3/(1-s)^2 = {2.3 / (1 - s) ** 2:.3f}")
    for d in (1e-2, 1e-4, 1e-6):
        v = 2 * mp.quad(lambda xi: mp.quad(lambda eta: 1 / (xi * eta), [d, 1 - xi]), [d, 1 - d])
        print(f"[J] s=1 truncated at delta={d:g}: {float(v):.3f}  (log^2(1/delta) = {math.log(1 / d) ** 2:.1f})")


def vex_joint(phi, box, x):
    V = list(itertools.product(*[(l, u) for (l, u) in box]))
    vals = [phi(np.array(v)) for v in V]
    Aeq = np.vstack([np.array(V).T, np.ones(len(V))])
    beq = np.concatenate([x, [1.0]])
    r = linprog(vals, A_eq=Aeq, b_eq=beq, bounds=[(0, None)] * len(V), method="highs")
    return r.fun


def part_ENV(trials=300):
    rng = np.random.default_rng(7)
    worst23, worst24 = float("inf"), float("inf")
    for _ in range(trials):
        coef = rng.normal(size=8)            # multilinear in 3 variables: sum over subsets
        subsets = [S for k in range(4) for S in itertools.combinations(range(3), k)]
        phi = lambda z, coef=coef: sum(c * np.prod([z[i] for i in S]) for c, S in zip(coef, subsets))

        def dij(z, i, j, coef=coef):
            return sum(c * np.prod([z[k] for k in S if k not in (i, j)])
                       for c, S in zip(coef, subsets) if i in S and j in S)
        box = [tuple(sorted(rng.uniform(-1, 1, 2))) for _ in range(3)]
        x = np.array([rng.uniform(l, u) for (l, u) in box])
        v = vex_joint(phi, box, x)
        gap = phi(x) - v
        d = [min(x[k] - box[k][0], box[k][1] - x[k]) for k in range(3)]
        for (i, j) in ((0, 1), (0, 2), (1, 2)):
            D = dij(x, i, j)
            b23 = abs(D) * d[i] * d[j]
            if b23 > 1e-9:
                worst23 = min(worst23, gap / b23)
            s = 1.0 if D >= 0 else -1.0
            # chord along e_i - s e_j: t in [t-, t+]
            tp = min(box[i][1] - x[i], x[j] - box[j][0] if s > 0 else box[j][1] - x[j])
            tm = min(x[i] - box[i][0], box[j][1] - x[j] if s > 0 else x[j] - box[j][0])
            b24 = abs(D) * tp * tm
            if b24 > 1e-9:
                worst24 = min(worst24, gap / b24)
    print(f"[ENV] {trials} random trilinear functions: min gap/(|d_ij phi| d_i d_j) = {worst23:.4f}, "
          f"min gap/chord bound = {worst24:.4f} (both should be >= 1)")


def part_TILT():
    for theta in (0.3, 0.03):
        for eps in (1e-3, 1e-5):
            h = 4 * math.sqrt(eps / theta)
            K = math.ceil(1 / h)
            worst = -float("inf")
            for k in range(K):
                y0, y1 = k / K, (k + 1) / K
                ym = 0.5 * (y0 + y1)
                xm = 0.5 - theta * (ym - 0.5)
                for (lx, ux) in ((0.0, xm), (xm, 1.0)):
                    xs = np.linspace(lx, ux, 201)
                    ys = np.linspace(y0, y1, 201)
                    X, Y = np.meshgrid(xs, ys, indexing="ij")
                    gap = np.minimum((X - lx) * (Y - y0), (ux - X) * (y1 - Y))      # c = +1
                    U = (X - 0.5) + theta * (Y - 0.5)
                    m = 2 * np.abs(U) + U * (Y - 0.5)
                    worst = max(worst, float((gap - m - eps).max()))
            print(f"[TILT] theta={theta}, eps={eps:g}: 2K = {2 * K} boxes, lower bound (1/2)sqrt(theta/eps) = "
                  f"{0.5 * math.sqrt(theta / eps):.1f}, max grid (gap - m - eps) = {worst:.2e}")


def part_FO():
    a, b = 1 / 3, math.sqrt(2) - 1
    worst = -float("inf")
    for (lx, ux) in ((0.0, a), (a, 1.0)):
        xs = np.linspace(lx, ux, 401)
        ys = np.linspace(0, 1, 401)
        X, Y = np.meshgrid(xs, ys, indexing="ij")
        Xa, Yb = X - a, Y - b
        Xl, Xu, Yl, Yu = lx - a, ux - a, -b, 1 - b
        mcc = np.minimum((Xa - Xl) * (Yu - Yb), (Xu - Xa) * (Yb - Yl))   # c = -1 gap
        gap = mcc + 0.2 * np.minimum(X - lx, ux - X)
        m = 2 * np.abs(Xa) - Xa * Yb
        worst = max(worst, float((gap - m).max()))
    print(f"[FO] first-order scheme, two boxes: max grid (gap - m) = {worst:.2e} (<= 0 means exact certificate)")


def part_OBL(na=64):
    for eps in (1e-3, 1e-4, 1e-5):
        Ea = np.mean([run(rule_bisect, eps, a=(k + 1 / math.sqrt(2)) / na) for k in range(na)])
        # mirrored family f'_{a0,b}: swap coordinates -> same as f_{b,a0} with the roles of x,y exchanged;
        # widest-side bisection with ties -> first coordinate is not symmetric, so emulate directly
        Eb = np.mean([run_mirror(eps, (k + 1 / math.sqrt(2)) / na) for k in range(na)])
        bound = 0.5 * math.sqrt(1 / (8 * eps))
        print(f"[OBL] eps={eps:g}: E_a N = {Ea:.1f}, E_b N' = {Eb:.1f}, sum = {Ea + Eb:.1f} >= "
              f"beta sqrt(|c|/(8eps)) = {bound:.1f}: {Ea + Eb >= bound}")


def run_mirror(eps, b, a0=1 / 3):
    stack = [(0.0, 1.0, 0.0, 1.0)]
    n = 0
    while stack:
        lx, ux, ly, uy = stack.pop()
        n += 1
        lb = relax((ly, uy, lx, ux), a=b, b=a0)[0]          # f'(x,y) = f_{b,a0}(y,x)
        if lb >= -eps:
            continue
        if ux - lx >= uy - ly:
            p = 0.5 * (lx + ux); stack += [(lx, p, ly, uy), (p, ux, ly, uy)]
        else:
            p = 0.5 * (ly + uy); stack += [(lx, ux, ly, p), (lx, ux, p, uy)]
    return n


if __name__ == "__main__":
    part_J()
    part_ENV()
    part_TILT()
    part_FO()
    part_OBL()
