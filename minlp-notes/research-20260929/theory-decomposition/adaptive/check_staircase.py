"""Part B of extension-adaptive.md: the staircase family refuting the lower half of Conjecture 3.7
with a fixed-degree poly(|T|).

Path of K bags V_t = {s_t, y_t, s_{t+1}}, s_t binary (one-dimensional separators s_2..s_K),
y_t in [0,1]^d, factor a_t = (1 - s_{t+1} + s_t)|y_t|^2 + P (s_t - s_{t+1})_+^2, f* = 0.
Relaxation on boxes that fix the binaries: a_t - alpha q_{B_y}(y).

Certificate (Theorem B.2): cells {0},{1}; per bag and binary pair
  (0,1): uniform grid of [0,1]^d with side h1 = 1/ceil(sqrt(alpha d/(2 eps)));
  (0,0),(1,1): shell partition around the corner y = 0 (Lemma 3.1), h0 = sqrt(2 eps/(K d alpha^2)),
               theta = largest power of 1/2 with theta <= 2/sqrt(alpha d);
  (1,0): one leaf.
The root bound is computed exactly: bag minima in closed form (separable convex quadratics),
then a two-state DP over binary s. The closed forms are checked in every row: the minimizer
satisfies the KKT conditions of the convex problem (so it is the true minimizer), and the relaxed
function evaluated directly at it equals the closed form (kkt_err below). A brute-force grid check
(small cases) is kept as a sanity check; it is one-sided (closed form <= grid minimum).
Reports: l_r >= -eps?, certificate size, Psi lower bound K (alpha K/eps)^{d/2}, their ratio.
"""
import math
import os
import sys
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from dp_certificate import shells  # noqa: E402


def slice_min(L, U, coef, alpha):
    """min over y in box [L,U] (rows) of coef*|y|^2 - alpha*sum (y-L)(U-y); per row. coef >= 0."""
    # per coordinate: (coef+alpha) y^2 - alpha (L+U) y + alpha L U, convex
    ystar = np.clip(alpha * (L + U) / (2 * (coef + alpha)), L, U)
    v = coef * ystar ** 2 - alpha * (ystar - L) * (U - ystar)
    return v.sum(axis=1)


def exactness_error(L, U, coef, alpha):
    """Two-sided check of slice_min on the boxes [L,U] (rows). The relaxed function
    coef*|y|^2 - alpha*sum (y-L)(U-y) is a separable strictly convex quadratic, so y* is the true
    minimizer iff it satisfies the KKT conditions for the box. Returns the largest KKT violation
    and the largest |direct value at y* - closed form|."""
    ystar = np.clip(alpha * (L + U) / (2 * (coef + alpha)), L, U)
    g = 2 * (coef + alpha) * ystar - alpha * (L + U)          # partial derivatives at y*
    scale = 1.0 + np.abs(alpha * (L + U))
    at_lo, at_hi = ystar <= L, ystar >= U
    viol = np.where(at_lo & ~at_hi, np.maximum(-g, 0), np.where(at_hi & ~at_lo, np.maximum(g, 0),
                                                              np.where(at_lo & at_hi, 0.0, np.abs(g))))
    direct = (coef * (ystar ** 2).sum(1) - alpha * ((ystar - L) * (U - ystar)).sum(1))
    return float((viol / scale).max()), float(np.abs(direct - slice_min(L, U, coef, alpha)).max())


def certificate(K, d, alpha, P, eps, grid_check=False):
    h0 = math.sqrt(2 * eps / (K * d * alpha ** 2))
    mu = max(0, math.ceil(math.log2(math.sqrt(alpha * d) / 2)))
    SL, SU = shells(np.zeros(d), h0, mu, d, lo=0.0, hi=1.0)
    m_flat = float(slice_min(SL, SU, 1.0, alpha).min())          # slices (0,0), (1,1)
    m_desc = float(slice_min(np.zeros((1, d)), np.ones((1, d)), 2.0, alpha).min()) + P  # slice (1,0)
    g = math.ceil(math.sqrt(alpha * d / (2 * eps)))
    h1 = 1.0 / g
    m_fat = -alpha * d * h1 ** 2 / 4                               # slice (0,1): every grid leaf
    m = {(0, 0): m_flat, (1, 1): m_flat, (0, 1): m_fat, (1, 0): m_desc}
    # two-state DP over s_1..s_{K+1}
    V = {0: 0.0, 1: 0.0}
    for _ in range(K):
        V = {s2: min(V[s1] + m[(s1, s2)] for s1 in (0, 1)) for s2 in (0, 1)}
    lr = min(V.values())
    leaves_per_bag = g ** d + 2 * len(SL) + 1
    size = K * leaves_per_bag + 2 * (K - 1)
    psi_lb = K * (alpha * K / eps) ** (d / 2)
    out = dict(K=K, d=d, eps=eps, lr=lr, ok=lr >= -eps, h0=h0, theta=2.0 ** -mu, fat=g ** d,
               shell=len(SL), size=size, psi_lb=psi_lb, ratio=psi_lb / size,
               m_flat=m_flat, m_fat=m_fat, m_desc=m_desc)
    # two-sided exactness of the closed forms: shell leaves (coef 1), the (1,0) leaf (coef 2),
    # and one fat grid leaf [0,h1]^d (coef 0), whose minimum must be m_fat
    e1 = exactness_error(SL, SU, 1.0, alpha)
    e2 = exactness_error(np.zeros((1, d)), np.ones((1, d)), 2.0, alpha)
    e3 = exactness_error(np.zeros((1, d)), np.full((1, d), h1), 0.0, alpha)
    fat_err = abs(float(slice_min(np.zeros((1, d)), np.full((1, d), h1), 0.0, alpha)[0]) - m_fat)
    out["kkt_err"] = max(e1[0], e2[0], e3[0])
    out["val_err"] = max(e1[1], e2[1], e3[1], fat_err)
    if grid_check and d <= 2:
        # brute force: min of relaxed function on each shell leaf over a 41^d grid
        worst = 0.0
        t = np.linspace(0, 1, 41)
        for Lr, Ur in zip(SL, SU):
            pts = np.stack(np.meshgrid(*[Lr[i] + t * (Ur[i] - Lr[i]) for i in range(d)],
                                       indexing="ij"), -1).reshape(-1, d)
            vals = (pts ** 2).sum(1) - alpha * ((pts - Lr) * (Ur - pts)).sum(1)
            worst = max(worst, float(slice_min(Lr[None], Ur[None], 1.0, alpha)[0] - vals.min()))
        out["grid_excess"] = worst  # closed form minus grid minimum; <= 0 is necessary, not sufficient
    return out


def main():
    alpha = 1.0
    print("alpha = %.1f, P = alpha d/4 + 1" % alpha)
    for d in (1, 2, 4):
        P = alpha * d / 4 + 1.0
        for eps in (1e-3, 1e-6):
            for K in (4, 16, 64, 256, 1024):
                r = certificate(K, d, alpha, P, eps, grid_check=(K == 4 and eps == 1e-3))
                print("d=%d eps=%.0e K=%5d l_r=% .3e ok=%s theta=%.3g fat=%d shell=%d size=%.3e "
                      "Psi_lb=%.3e ratio=%.3e ratio/K^(d/2)=%.3e kkt_err=%.1e val_err=%.1e%s" % (
                          d, eps, K, r["lr"], r["ok"], r["theta"], r["fat"], r["shell"], r["size"],
                          r["psi_lb"], r["ratio"], r["ratio"] / K ** (d / 2), r["kkt_err"], r["val_err"],
                          (" grid_excess=%.1e" % r["grid_excess"]) if "grid_excess" in r else ""),
                      flush=True)


if __name__ == "__main__":
    main()
