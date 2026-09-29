"""Monte Carlo check of the mechanism of Theorem 4.3 with real matrices.

For an instance (H, w) with x* = 1 (WLOG: signed columns), T = {g_i in [-2,-1]}:
 (1) the events used in the proof: n' = |T| vs pN, s_max(H^perp_T) vs
     sqrt(N)(sqrt(beta)+1), a = sqrt(rho/N)||w|| vs sqrt(rho beta);
 (2) the deterministic inequality used for every class,
         f(xbar) - W <= -2X + X^2/W + 4 (rho/N) s_max(H^perp_T)^2 sum p_i^2,
     with X in [2ak, 4ak], on random families F of k-subsets of T;
 (3) the empirical overlap threshold: the value of sum p_i^2 / k at which the
     barycenter crosses W, compared with lambda_1 = sqrt(beta)/(2 sb^2 sqrt(rho))
     used in the proof, and with the heuristic 2X/(4 rho beta k).
Families: m disjoint k-sets (sum p^2 = k/m), m random k-sets, and "stars"
(members share a core of size s).
"""
import numpy as np
from scipy.stats import norm

p_T = norm.cdf(-1) - norm.cdf(-2)
rng = np.random.default_rng(2026)


def run(N, beta, rho, seed, k=8):
    r = np.random.default_rng(seed)
    M = int(round(beta * N))
    H = r.standard_normal((M, N))            # signed columns h~_i (x* = 1)
    w = r.standard_normal(M)
    W = w @ w
    B = np.sqrt(rho / N) * H
    what = w / np.sqrt(W)
    g = what @ H
    T = np.flatnonzero((g >= -2) & (g <= -1))
    nT = len(T)
    Hp = H[:, T] - np.outer(what, g[T])
    smax = np.linalg.norm(Hp, 2)
    sb = np.sqrt(beta) + 1
    a = np.sqrt(rho / N * W)
    zeta = B.T @ w
    out = dict(N=N, beta=beta, rho=rho, nT_over_pN=nT / (p_T * N),
               smax_over_bound=smax / (np.sqrt(N) * sb),
               smax_over_true=smax / (np.sqrt(M - 1) + np.sqrt(nT)),
               a_over=a / np.sqrt(rho * beta))
    lam1 = np.sqrt(beta) / (2 * sb ** 2 * np.sqrt(rho))

    def bary(members):
        c = np.zeros(N)
        for S in members:
            c[S] += 2.0 / len(members)
        res = w + B @ c
        val = res @ res - W
        pvec = c[T] / 2
        sp2 = float(pvec @ pvec)
        X = -(zeta @ c)
        bound = -2 * X + X ** 2 / W + 4 * (rho / N) * smax ** 2 * sp2
        return val, sp2, X, bound

    viol = 0; rows = []
    # disjoint families
    perm = r.permutation(T)
    for m in range(1, nT // k + 1):
        members = [perm[j * k:(j + 1) * k] for j in range(m)]
        val, sp2, X, bound = bary(members)
        viol += val > bound + 1e-8 * W
        rows.append(("disjoint", m, sp2 / k, val, X / (a * k)))
    # random families
    for m in (2, 4, 8, 16, 32, 64, 128):
        for rep in range(3):
            members = [r.choice(T, k, replace=False) for _ in range(m)]
            val, sp2, X, bound = bary(members)
            viol += val > bound + 1e-8 * W
            rows.append(("random", m, sp2 / k, val, X / (a * k)))
    # stars with core s
    for s in range(1, k):
        core = r.choice(T, s, replace=False)
        rest = np.setdiff1d(T, core)
        members = [np.concatenate([core, r.choice(rest, k - s, replace=False)]) for _ in range(64)]
        val, sp2, X, bound = bary(members)
        viol += val > bound + 1e-8 * W
        rows.append(("star s=%d" % s, 64, sp2 / k, val, X / (a * k)))
    # empirical crossing: smallest sum p^2/k among families with val >= 0 and
    # largest among those with val < 0
    below = [r_[2] for r_ in rows if r_[3] < 0]
    above = [r_[2] for r_ in rows if r_[3] >= 0]
    disj = [r_ for r_ in rows if r_[0] == "disjoint"]
    m_cross = next((r_[1] for r_ in disj if r_[3] < 0), None)
    Xk = np.mean([r_[4] for r_ in disj]) * a     # X/k for disjoint families
    out.update(k=k, nT=nT, viol=int(viol), nfam=len(rows), lam1=lam1,
               max_sp2k_below=max(below) if below else None,
               min_sp2k_above=min(above) if above else None,
               heur_cross=2 * Xk / (4 * rho * beta),
               m_cross_disjoint=m_cross, heur_m=4 * rho * beta / (2 * Xk))
    return out


if __name__ == "__main__":
    print("columns: n'/(pN), s_max/(sqrt(N) sb), s_max/(sqrt(M-1)+sqrt(n')), a/sqrt(rho beta);"
          " violations of the class inequality; empirical sum p^2/k crossing interval vs lambda_1 and"
          " the heuristic 2X/(4 rho beta k); smallest m of disjoint k-sets whose barycenter beats W vs heuristic")
    for beta in (1.0, 2.0):
        for N in (1000, 3000):
            for rho in (10.0, 20.0, 40.0, 80.0, 160.0):
                o = run(N, beta, rho, seed=int(1000 * beta + N + rho))
                print("beta=%g N=%d rho=%g k=%d n'=%d | n'/pN=%.3f smax/bound=%.3f smax/true=%.3f a=%.3f | "
                      "viol %d/%d | crossing sum p^2/k in (%.4f, %.4f]  lambda_1=%.4f heur=%.4f | "
                      "m_cross=%s heur_m=%.1f"
                      % (beta, N, rho, o["k"], o["nT"], o["nT_over_pN"], o["smax_over_bound"],
                         o["smax_over_true"], o["a_over"], o["viol"], o["nfam"],
                         o["max_sp2k_below"] if o["max_sp2k_below"] is not None else float("nan"),
                         o["min_sp2k_above"] if o["min_sp2k_above"] is not None else float("nan"),
                         o["lam1"], o["heur_cross"], o["m_cross_disjoint"], o["heur_m"]), flush=True)
