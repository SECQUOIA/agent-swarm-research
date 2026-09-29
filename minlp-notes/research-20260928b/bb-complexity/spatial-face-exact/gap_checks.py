"""Checks of the gap lemmas (Section 2) and of the per-box integral J(s) (Section 3.1).

1. McCormick gap formula and bounds (Lemma 2.1), with the envelope computed by the vertex LP.
2. Mixed-partial lower bound for the convex envelope of a random multilinear function (Lemma 2.2):
   gap(x) >= max_{i<j} |d_ij phi(x)| d_i(x) d_j(x); envelope by the vertex LP (exact).
3. Chord lower bound (Lemma 2.3): gap(x) >= |d_ij phi(x)| * t_minus * t_plus along e_i - s e_j.
4. Termwise envelope gap >= joint envelope gap.
5. J(s) = int_{[0,1]^2} min(xi*eta, (1-xi)(1-eta))^{-s} = 2 Gamma(1-s)^2 / Gamma(3-2s) (Lemma 3.2).
"""
import itertools
import math
import numpy as np
from scipy.optimize import linprog
from scipy import integrate

rng = np.random.default_rng(20260928)


def vex_vertex_lp(phi, l, u, x):
    """Convex envelope of phi over box [l,u] at x: min sum lam_v phi(v), sum lam_v v = x (exact for
    multilinear phi, whose envelope is vertex polyhedral)."""
    n = len(l)
    V = np.array([[u[i] if b[i] else l[i] for i in range(n)] for b in itertools.product([0, 1], repeat=n)])
    vals = np.array([phi(v) for v in V])
    A_eq = np.vstack([V.T, np.ones(len(V))])
    b_eq = np.concatenate([x, [1.0]])
    r = linprog(vals, A_eq=A_eq, b_eq=b_eq, bounds=[(0, None)] * len(V), method="highs")
    assert r.status == 0
    return r.fun


def check_mccormick(trials=2000):
    worst = 0.0
    lower_ratio, upper_ok, amgm_ok = math.inf, True, True
    for _ in range(trials):
        l = rng.uniform(-2, 1, 2); u = l + rng.uniform(0.05, 3, 2)
        x = l + rng.uniform(0, 1, 2) * (u - l)
        c = rng.choice([-1, 1]) * rng.uniform(0.1, 3)
        phi = lambda v: c * v[0] * v[1]
        gap_lp = phi(x) - vex_vertex_lp(phi, l, u, x)
        dm, dp = x - l, u - x
        if c > 0:
            gap_f = c * min(dm[0] * dm[1], dp[0] * dp[1])
        else:
            gap_f = -c * min(dm[0] * dp[1], dp[0] * dm[1])
        worst = max(worst, abs(gap_lp - gap_f))
        d = np.minimum(dm, dp); w = u - l
        if d[0] * d[1] > 1e-9:
            lower_ratio = min(lower_ratio, gap_f / (abs(c) * d[0] * d[1]))
        upper_ok &= gap_f <= abs(c) * min(d[0] * w[1], d[1] * w[0]) + 1e-12
        amgm_ok &= gap_f <= abs(c) / 2 * (dm[0] * dp[0] + dm[1] * dp[1]) + 1e-12
    print(f"[1] McCormick: max |gap_LP - formula| = {worst:.2e}; min gap/(|c| d_x d_y) = {lower_ratio:.4f} (>=1); "
          f"gap <= |c| min(d_x w_y, d_y w_x): {upper_ok}; gap <= |c|/2 (a_x+a_y): {amgm_ok}")


def random_multilinear(n, deg_max=3):
    subsets = [S for k in range(0, deg_max + 1) for S in itertools.combinations(range(n), k)]
    coef = {S: rng.normal() for S in subsets}
    def phi(x):
        return sum(cf * np.prod([x[i] for i in S]) for S, cf in coef.items())
    def dij(x, i, j):
        return sum(cf * np.prod([x[k] for k in S if k not in (i, j)]) for S, cf in coef.items() if i in S and j in S)
    return coef, phi, dij


def check_multilinear(trials=400, n=4):
    min_ratio, min_chord_ratio = math.inf, math.inf
    viol2, viol3, viol4 = 0, 0, 0
    for _ in range(trials):
        coef, phi, dij = random_multilinear(n)
        l = rng.uniform(-1.5, 0.5, n); u = l + rng.uniform(0.1, 2, n)
        x = l + rng.uniform(0, 1, n) * (u - l)
        gap = phi(x) - vex_vertex_lp(phi, l, u, x)
        dm, dp = x - l, u - x
        d = np.minimum(dm, dp)
        lb = max(abs(dij(x, i, j)) * d[i] * d[j] for i, j in itertools.combinations(range(n), 2))
        if gap < lb - 1e-9:
            viol2 += 1
        if lb > 1e-9:
            min_ratio = min(min_ratio, gap / lb)
        # chord along e_i - s e_j
        for i, j in itertools.combinations(range(n), 2):
            D = dij(x, i, j)
            if abs(D) < 1e-12:
                continue
            s = 1.0 if D > 0 else -1.0
            # moving t along e_i - s e_j: x_i + t in [l_i,u_i], x_j - s t in [l_j,u_j]
            tp = min(dp[i], dm[j] if s > 0 else dp[j])
            tm = min(dm[i], dp[j] if s > 0 else dm[j])
            chord = abs(D) * tp * tm
            if gap < chord - 1e-9:
                viol3 += 1
            if chord > 1e-9:
                min_chord_ratio = min(min_chord_ratio, gap / chord)
        # termwise >= joint
        term_gap = 0.0
        for S, cf in coef.items():
            if len(S) >= 2:
                ps = lambda v, S=S, cf=cf: cf * np.prod([v[k] for k in S])
                term_gap += ps(x) - vex_vertex_lp(ps, l, u, x)
        if term_gap < gap - 1e-9:
            viol4 += 1
    print(f"[2] multilinear n={n}, deg<=3, {trials} trials: violations of mixed-partial bound = {viol2}; "
          f"min gap/bound = {min_ratio:.4f}")
    print(f"[3] chord bound violations = {viol3}; min gap/chord bound = {min_chord_ratio:.4f}")
    print(f"[4] termwise gap < joint gap occurrences = {viol4}")


def check_J():
    for s in (0.25, 0.5, 0.75, 0.9):
        f = lambda eta, xi: min(xi * eta, (1 - xi) * (1 - eta)) ** (-s)
        # integrate over the two triangles separately (singularities at corners)
        num = 2 * integrate.dblquad(lambda eta, xi: (xi * eta) ** (-s), 0, 1, 0, lambda xi: 1 - xi,
                                    epsabs=1e-10, epsrel=1e-8)[0]
        closed = 2 * math.gamma(1 - s) ** 2 / math.gamma(3 - 2 * s)
        # Monte Carlo on the min-form as an independent check of the triangle reduction
        z = rng.uniform(0, 1, (400000, 2))
        mc = np.mean(np.minimum(z[:, 0] * z[:, 1], (1 - z[:, 0]) * (1 - z[:, 1])) ** (-s)) if s < 0.5 else float('nan')
        print(f"[5] J({s}) quadrature = {num:.6f}, closed form = {closed:.6f}, MC(min form, s<1/2) = {mc:.4f}, "
              f"(1-s)^2 J/2 = {(1 - s) ** 2 * closed / 2:.4f}")


if __name__ == "__main__":
    check_mccormick()
    check_multilinear()
    check_J()
