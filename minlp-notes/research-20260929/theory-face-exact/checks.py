"""Numerical checks of the lemmas in face-exact-exponential.md (floating point, not proofs).

1. Center inequality (Lemma 1): every valid box C (LB(C) >= f* - eps) of the mc relaxation satisfies
   sum_{i<n} (1 - s_i - s_{i+1}) <= rho sum_i s_i^2 + eps/(b r^2),  s_i = 1 - w_i/(2r),  R = [-1,1]^n.
   Tested on boxes produced by random face-extension (so that many valid boxes are large).
2. Orthant boxes (Proposition 3): kappa = 0, c = 0; LB of x* + sigma*[0,W]^n for every sign vector,
   compared with 0 (unfrustrated) and with the bound -b^2 W^2/(4D) (one frustrated edge).
4. Lemma 3.1 (python3 checks.py lemma31): log(1-s) <= log(theta) - lambda (rho s^2 + 2s - 1) on a grid of
   s in [0,1) for rho in (0, rho_max], and failure just above rho_max.
3. Per-factor envelope gap (Lemma 4): for h(x) = x^2 and the factor x^2 + b x y on random boxes,
   the convex envelope at random points (PSD + RLT hull, exact for 2 variables by Anstreicher-Burer 2010)
   has gap >= psi(d_x, d_y) = max_{sigma in [0,1]} (b sigma d_x d_y - D sigma^2 d_x^2/2), D = 2.
Usage: python3 checks.py
"""
import itertools
import math
import numpy as np
import cvxpy as cp
from bb_path import Inst, relax

b, D = 0.8, 2.0
rho = D / (2 * b)


def valid(I, l, u, eps):
    return relax(I, "mc", l, u)[0] >= I.fstar - eps


def grow(I, rng, eps, steps=(0.5, 0.25, 0.1, 0.05, 0.02, 0.01)):
    n = I.n
    z = rng.uniform(-1, 1, n)
    l, u = z - 1e-4, z + 1e-4
    l, u = np.maximum(l, -1), np.minimum(u, 1)
    if not valid(I, l, u, eps):
        return None
    for st in steps:
        improved = True
        while improved:
            improved = False
            for (i, side) in rng.permutation([(i, s) for i in range(n) for s in (0, 1)]):
                i = int(i)
                l2, u2 = l.copy(), u.copy()
                if side == 0:
                    l2[i] = max(-1.0, l[i] - st)
                else:
                    u2[i] = min(1.0, u[i] + st)
                if (l2[i] != l[i] or u2[i] != u[i]) and valid(I, l2, u2, eps):
                    l, u = l2, u2
                    improved = True
    return l, u


def check_center(eps=1e-4):
    print("1. center inequality on grown valid boxes (kappa = 0.1 and 0.0, c = 0, r = 1)")
    rng = np.random.default_rng(7)
    for kappa in (0.1, 0.0):
        for n in (3, 5, 8):
            I = Inst(n, kappa, "zero")
            worst, best_lv, cnt = -math.inf, -math.inf, 0
            for _ in range(40 if n < 8 else 15):
                res = grow(I, rng, eps)
                if res is None:
                    continue
                l, u = res
                s = 1 - (u - l) / 2
                lhs = np.sum(1 - s[:-1] - s[1:])
                rhs = rho * np.sum(s * s) + eps / b
                worst = max(worst, lhs - rhs)
                best_lv = max(best_lv, np.sum(np.log(u - l)) - n * math.log(2))
                cnt += 1
            print(f"  kappa={kappa} n={n}: {cnt} grown valid boxes, max(lhs - rhs) = {worst:.4f} (must be <= 0); "
                  f"largest volume fraction^(1/n) = {math.exp(best_lv / n):.4f} "
                  f"(Theorem 1 allows <= {0.6 * math.exp(5 / 9 * (1 + eps / b) / n):.4f}; orthant box 0.5)")


def check_orthants():
    print("2. orthant boxes x* + sigma*[0,W]^n, kappa = 0, c = 0 (exact McCormick gap)")
    for n in (3, 4, 6):
        I = Inst(n, 0.0, "zero")
        for W in (1.0, 0.5):
            res = {}
            for sig in itertools.product((-1, 1), repeat=n):
                sig = np.array(sig)
                l = np.where(sig > 0, 0.0, -W)
                u = np.where(sig > 0, W, 0.0)
                lb = relax(I, "mc", l, u)[0]
                fr = int(np.sum(sig[:-1] * sig[1:] < 0))
                res.setdefault(fr, []).append(lb)
            txt = "; ".join(f"{fr} frustrated: max LB {max(v):.2e}, min LB {min(v):.4f} ({len(v)} boxes)"
                            for fr, v in sorted(res.items()))
            print(f"  n={n} W={W}: {txt}; one-edge bound -b^2W^2/(4D) = {-b*b*W*W/(4*D):.4f}")


def envelope_gap(bl, bu, p):
    """convex envelope of q(x,y) = x^2 + b x y on the box [bl,bu] at the point p (PSD + RLT)."""
    X = cp.Variable((2, 2), symmetric=True)
    x = p
    M = cp.bmat([[np.ones((1, 1)), x.reshape(1, 2)], [x.reshape(2, 1), X]])
    cons = [M >> 0]
    for i in range(2):
        for j in range(i, 2):
            cons += [X[i, j] - bl[i] * x[j] - bl[j] * x[i] >= -bl[i] * bl[j],
                     X[i, j] - bu[i] * x[j] - bu[j] * x[i] >= -bu[i] * bu[j],
                     X[i, j] - bl[i] * x[j] - bu[j] * x[i] <= -bl[i] * bu[j],
                     X[i, j] - bu[i] * x[j] - bl[j] * x[i] <= -bu[i] * bl[j]]
    pr = cp.Problem(cp.Minimize(X[0, 0] + b * X[0, 1]), cons)
    pr.solve(solver="CLARABEL", tol_gap_abs=1e-10, tol_gap_rel=1e-10, tol_feas=1e-10)
    q = p[0] ** 2 + b * p[0] * p[1]
    return q - pr.value


def psi(a, c):
    sig = np.clip(b * c / (D * a), 0, 1) if a > 0 else 1.0
    return max(0.0, b * sig * a * c - D * sig * sig * a * a / 2)


def check_envelope(N=400):
    print("3. per-factor envelope gap of x^2 + 0.8 x y versus psi(d_x, d_y)")
    rng = np.random.default_rng(3)
    worst, ratios, mc_ratio = math.inf, [], []
    for _ in range(N):
        bl = rng.uniform(-1, 0.5, 2)
        bu = bl + rng.uniform(0.05, 1.5, 2)
        p = bl + rng.uniform(0, 1, 2) * (bu - bl)
        g = envelope_gap(bl, bu, p)
        d = np.minimum(p - bl, bu - p)
        ps = psi(d[0], d[1])
        mc = b * min((p[0] - bl[0]) * (p[1] - bl[1]), (bu[0] - p[0]) * (bu[1] - p[1]))
        worst = min(worst, g - ps)
        if ps > 1e-6:
            ratios.append(g / ps)
        if mc > 1e-6:
            mc_ratio.append(g / mc)
    print(f"  {N} random (box, point) pairs: min(gap - psi) = {worst:.2e} (must be >= -solver tol); "
          f"gap/psi in [{min(ratios):.3f}, {max(ratios):.3f}], median {np.median(ratios):.3f}; "
          f"envelope gap / McCormick gap median {np.median(mc_ratio):.3f}")


def check_lemma31():
    print("4. Lemma 3.1 on a grid of 2*10^6 points of [0,1) for 400 values of rho")
    s = np.linspace(0, 1, 2_000_001)[:-1]
    worst = -math.inf
    for rho in np.linspace(1e-3, 1.9905, 400):
        S = math.sqrt(1 + rho)
        th, lam = S / (1 + S), (1 + S) / (2 * S * S)
        worst = max(worst, np.max(np.log1p(-s) - math.log(th) + lam * (rho * s * s + 2 * s - 1)))
    print(f"  max over rho in [0.001, 1.9905] of [lhs - rhs] = {worst:.2e} (must be <= 0 up to rounding)")
    for rho in (2.0, 2.2):
        S = math.sqrt(1 + rho)
        th, lam = S / (1 + S), (1 + S) / (2 * S * S)
        print(f"  rho = {rho}: max [lhs - rhs] = {np.max(np.log1p(-s) - math.log(th) + lam * (rho * s * s + 2 * s - 1)):.2e} "
              f"(positive: the closed form fails above rho_max)")


if __name__ == "__main__":
    import sys
    if sys.argv[1:] == ["lemma31"]:
        check_lemma31()
        sys.exit()
    check_orthants()
    check_envelope()
    check_center()
