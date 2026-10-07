"""Reviewer check of Theorem B.2 and of the Phi comparison (Section B.4) of extension-adaptive.md.

1. Own shell partition Pi(0; h0, theta) of [0,1]^d (Lemma 3.1 of [D], centre at the corner):
   tiling check (volume, disjointness by sampling), width condition, count vs author's shells().
2. Own leaf minima: closed form per coordinate, cross-checked by L-BFGS-B on every leaf (small cases).
3. Root bound by brute force over all binary sequences s in {0,1}^{K+1} (K <= 12), and by a
   min-plus product for large K; compared with the author's certificate().
4. The d^{d/2} factor: N_dec >= K Gamma(d/2+1) pi^{-d/2} (alpha/eps)^{d/2} (volume argument, see
   review) against the admissible-family upper bound
   sup_eta Phi(eps, eta) <= K 2^{-(d+2)} (ceil(sqrt(alpha/(4 eps)))^d + 3).
"""
import itertools
import math
import os
import sys
import numpy as np
from scipy.optimize import minimize

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "theory-decomposition", "adaptive"))
sys.path.insert(0, os.path.join(HERE, "..", "..", "theory-decomposition"))
import check_staircase as AUTH  # noqa: E402


def my_shells(d, h, mu):
    """Lemma 3.1 with p = 0 in X = [0,1]^d."""
    theta = 2.0 ** (-mu)
    J = max(0, math.ceil(math.log2(1.0 / h)))
    Ls, Us = [np.zeros((1, d))], [np.full((1, d), min(h, 1.0))]
    m = int(round(4 / theta))
    for j in range(1, J + 1):
        R, g = 2.0 ** j * h, theta * 2.0 ** (j - 1) * h
        idx = np.array(list(itertools.product(range(m), repeat=d)))
        lo = -R + g * idx
        hi = lo + g
        inner = np.all((lo >= -R / 2 - 1e-15) & (hi <= R / 2 + 1e-15), axis=1)
        lo, hi = lo[~inner], hi[~inner]
        lo, hi = np.clip(lo, 0, 1), np.clip(hi, 0, 1)
        ok = np.all(hi - lo > 1e-15, axis=1)
        Ls.append(lo[ok])
        Us.append(hi[ok])
    return np.concatenate(Ls), np.concatenate(Us), theta


def leafmin_closed(L, U, coef, alpha):
    y = np.clip(alpha * (L + U) / (2 * (coef + alpha)), L, U)
    return (coef * y * y - alpha * (y - L) * (U - y)).sum(axis=1)


def leafmin_numeric(L, U, coef, alpha):
    out = []
    for l, u in zip(L, U):
        f = lambda y: coef * y @ y - alpha * np.sum((y - l) * (u - y))  # noqa: E731
        gr = lambda y: 2 * coef * y - alpha * (u + l - 2 * y)  # noqa: E731
        r = minimize(f, 0.5 * (l + u), jac=gr, bounds=list(zip(l, u)), method="L-BFGS-B",
                     options=dict(ftol=1e-15, gtol=1e-12))
        out.append(r.fun)
    return np.array(out)


def main():
    alpha = 1.0
    print("== 1-3: certificate of Theorem B.2(b), alpha = 1, P = alpha d/4 + 1")
    rng = np.random.default_rng(0)
    worst_num = 0.0
    for d in (1, 2, 3):
        for eps in (1e-2, 1e-3):
            for K in (2, 3, 5, 8, 12, 64, 1024):
                P = alpha * d / 4 + 1
                h0 = math.sqrt(2 * eps / (K * d * alpha ** 2))
                mu = max(0, math.ceil(math.log2(math.sqrt(alpha * d) / 2)))
                SL, SU, theta = my_shells(d, h0, mu)
                # tiling checks
                vol = float(np.prod(SU - SL, axis=1).sum())
                pts = rng.random((4000, d))
                inside = ((pts[:, None, :] > SL[None]) & (pts[:, None, :] < SU[None])).all(axis=2).sum(axis=1)
                dist = SL.max(axis=1)  # sup-distance of a box in the positive orthant to 0
                w = (SU - SL).max(axis=1)
                noncentral = dist > 0
                width_ok = bool(np.all(w[noncentral] <= theta * dist[noncentral] + 1e-15))
                J = max(0, math.ceil(math.log2(1 / h0)))
                bound = (J + 1) * (4 / theta) ** d
                AL, AU = AUTH.shells(np.zeros(d), h0, mu, d, lo=0.0, hi=1.0)
                # leaf minima
                m_flat_all = leafmin_closed(SL, SU, 1.0, alpha)
                central = ~noncentral
                m_flat = float(m_flat_all.min())
                claim_central = -d * alpha ** 2 * h0 ** 2 / (4 * (1 + alpha))
                g = math.ceil(math.sqrt(alpha * d / (2 * eps)))
                h1 = 1.0 / g
                m_fat = -alpha * d * h1 ** 2 / 4
                m_desc = float(leafmin_closed(np.zeros((1, d)), np.ones((1, d)), 2.0, alpha)[0]) + P
                if len(SL) <= 400 and K <= 3:
                    num = leafmin_numeric(SL, SU, 1.0, alpha)
                    worst_num = max(worst_num, float(np.abs(num - m_flat_all).max()))
                m = {(0, 0): m_flat, (1, 1): m_flat, (0, 1): m_fat, (1, 0): m_desc}
                if K <= 12:
                    lr = min(sum(m[(s[t], s[t + 1])] for t in range(K))
                             for s in itertools.product((0, 1), repeat=K + 1))
                    how = "brute"
                else:
                    M = np.array([[m[(0, 0)], m[(0, 1)]], [m[(1, 0)], m[(1, 1)]]])
                    v = np.zeros(2)
                    for _ in range(K):
                        v = np.min(v[:, None] + M, axis=0)
                    lr = float(v.min())
                    how = "minplus"
                size = K * (g ** d + 2 * len(SL) + 1) + 2 * (K - 1)
                a = AUTH.certificate(K, d, alpha, P, eps)
                print("d=%d eps=%.0e K=%4d theta=%.3g shells=%d (author %d, Lemma 3.1 bound %d) vol=%.12f "
                      "overlap_max=%d uncovered=%d width_ok=%s central_min=%.3e (claim %.3e, >= -eps/(2K)=%.3e) "
                      "noncentral_min=%.2e fat=%.3e (>= -eps/2: %s) desc=%.3f lr[%s]=%.4e (author %.4e) "
                      "lr>=-eps: %s size=%d (author %d)" % (
                          d, eps, K, theta, len(SL), len(AL), bound, vol, inside.max(), int((inside == 0).sum()),
                          width_ok, m_flat_all[central].min(), claim_central, -eps / (2 * K),
                          m_flat_all[noncentral].min() if noncentral.any() else float("nan"),
                          m_fat, m_fat >= -eps / 2, m_desc, how, lr, a["lr"], lr >= -eps, size, a["size"]),
                      flush=True)
    print("worst |closed form - L-BFGS-B| over checked leaves: %.2e" % worst_num)

    print("\n== 3b: shells with theta < 1 (alpha = 4, d = 2 and 4), leaf minima of non-central shells >= 0")
    for alpha2, d in ((4.0, 2), (4.0, 4), (16.0, 2)):
        eps = 1e-3
        K = 4
        h0 = math.sqrt(2 * eps / (K * d * alpha2 ** 2))
        mu = max(0, math.ceil(math.log2(math.sqrt(alpha2 * d) / 2)))
        SL, SU, theta = my_shells(d, h0, mu)
        mins = leafmin_closed(SL, SU, 1.0, alpha2)
        dist = SL.max(axis=1)
        print("alpha=%.0f d=%d theta=%.4g shells=%d min over non-central leaves=%.3e central=%.3e (>= -eps/(2K) = %.3e)"
              % (alpha2, d, theta, len(SL), mins[dist > 0].min(), mins[dist == 0].min(), -eps / (2 * K)))

    print("\n== 4: N_dec lower bound vs upper bound on sup_eta Phi, alpha = 1 (ratio = N_dec_lb / Phi_ub)")
    alpha = 1.0
    for eps in (1e-2, 1e-4):
        for d in (1, 2, 4, 8, 12, 16, 24, 32):
            r = math.sqrt(eps / alpha)
            nd_lb = math.exp(math.lgamma(d / 2 + 1) - (d / 2) * math.log(math.pi) - d * math.log(r))  # per bag
            phi_ub = 2.0 ** (-(d + 2)) * (math.ceil(1 / (2 * r)) ** d + 3)                          # per bag
            ratio = nd_lb / phi_ub
            print("eps=%.0e d=%2d  N_dec/K >= %.3e  sup Phi/K <= %.3e  ratio >= %.3e  ratio/2^(d+2)=%.2e  "
                  "ratio/4^(d+2)=%.2e  ratio/8^(d+2)=%.2e" % (
                      eps, d, nd_lb, phi_ub, ratio, ratio / 2 ** (d + 2), ratio / 4 ** (d + 2), ratio / 8 ** (d + 2)))


if __name__ == "__main__":
    main()
