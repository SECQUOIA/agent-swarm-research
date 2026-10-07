"""Referee check R2: tree bounds (Theorem 3.1), Proposition 3.3, Corollary 3.4.

Path a(s1) - b(s1,s2) - c(s2), root b.  Edge 1: child a; edge 2: child c.
Split: a - phi1, b + phi1 + phi2, c - phi2 (both a and c are children of b).
Band of edge e computed from explicit value functions (not by giving the other
edge the full class):  U_1 = a, V_1(s1) = min_s2 [b + c], L_1 = f* - V_1, etc.
Independent of the author's check_tree.py.
"""
import numpy as np
from scipy.optimize import linprog

OPT = {"primal_feasibility_tolerance": 1e-10, "dual_feasibility_tolerance": 1e-10}
rng = np.random.default_rng(777)


def tree_rho(a, b, c, B1, B2):
    k1, k2 = b.shape
    d1, d2 = B1.shape[1], B2.shape[1]
    nv = d1 + d2 + 3
    ia, ib, ic = d1 + d2, d1 + d2 + 1, d1 + d2 + 2
    rows, rhs = [], []
    R = np.zeros((k1, nv)); R[:, :d1] = B1; R[:, ia] = 1; rows.append(R); rhs.append(a)      # a - phi1 >= ma
    R = np.zeros((k2, nv)); R[:, d1:d1 + d2] = B2; R[:, ic] = 1; rows.append(R); rhs.append(c)  # c - phi2 >= mc
    R = np.zeros((k1 * k2, nv))
    R[:, :d1] = -np.repeat(B1, k2, axis=0); R[:, d1:d1 + d2] = -np.tile(B2, (k1, 1)); R[:, ib] = 1
    rows.append(R); rhs.append(b.reshape(-1))                                                # b + phi1 + phi2 >= mb
    cost = np.zeros(nv); cost[[ia, ib, ic]] = -1
    r = linprog(cost, A_ub=np.vstack(rows), b_ub=np.concatenate(rhs), bounds=[(None, None)] * nv,
                method="highs", options=OPT)
    assert r.status == 0, r.message
    return -r.fun, r.x[:d1], r.x[d1:d1 + d2]


def bracket_min(B, U, L):
    """min over phi in span(B) of sup(phi - U) + sup(L - phi); returns value and phi."""
    k, d = B.shape
    A1 = np.hstack([B, -np.ones((k, 1)), np.zeros((k, 1))])
    A2 = np.hstack([-B, np.zeros((k, 1)), -np.ones((k, 1))])
    cost = np.zeros(d + 2); cost[d:] = 1
    r = linprog(cost, A_ub=np.vstack([A1, A2]), b_ub=np.concatenate([U, -L]),
                bounds=[(None, None)] * (d + 2), method="highs", options=OPT)
    assert r.status == 0, r.message
    return r.fun, B @ r.x[:d]


def two_dist(B, f):
    """2 dist(f, span B) with constants in span B = min osc(f - phi)."""
    return bracket_min(B, f, f)[0]


def bands(a, b, c):
    fs = np.min(a[:, None] + b + c[None, :])
    U1 = a; V1 = np.min(b + c[None, :], axis=1); L1 = fs - V1
    U2 = c; V2 = np.min(a[:, None] + b, axis=0); L2 = fs - V2
    return fs, (U1, L1), (U2, L2)


def analyse(a, b, c, B1, B2):
    fs, (U1, L1), (U2, L2) = bands(a, b, c)
    rho, _, _ = tree_rho(a, b, c, B1, B2)
    gap = fs - rho
    d1, phi1 = bracket_min(B1, U1, L1)
    d2, _ = bracket_min(B2, U2, L2)
    dp = two_dist(B1, U1) + two_dist(B2, U2)
    # sequential bound (Cor 3.4): eliminate edge 1 with phi1 optimal for its own bracket,
    # then edge 2 in the reduced problem with parent bag b + phi1(s1).
    b_red = b + phi1[:, None]
    fs_red = np.min(b_red + c[None, :])
    U2r = c; V2r = np.min(b_red, axis=0); L2r = fs_red - V2r
    d2r, _ = bracket_min(B2, U2r, L2r)
    seq = d1 + d2r
    return dict(fs=fs, gap=gap, e1=d1, e2=d2, dp=dp, seq=seq)


def prop33():
    print("[Prop 3.3] a = 10(1-s1), c = 10(1-s2), b = s1 s2 + M(s1 + s2 - 2 s1 s2) on [0,1]^2")
    s = np.linspace(0, 1, 101)
    S1, S2 = np.meshgrid(s, s, indexing="ij")
    for M in [1.0, 0.8, 0.6]:
        a = 10 * (1 - s); c = 10 * (1 - s)
        b = S1 * S2 + M * (S1 + S2 - 2 * S1 * S2)
        B0 = np.ones((len(s), 1))
        r = analyse(a, b, c, B0, B0)
        fs, (U1, L1), _ = bands(a, b, c)
        const_in_band = np.all(L1 <= 1e-12) and np.all(U1 >= -1e-12)
        print(f"  M={M}: f*={r['fs']:.4f} gap(R)={r['gap']:.4f}  2dist(R,Band_1)={r['e1']:.4f} "
              f"2dist(R,Band_2)={r['e2']:.4f} (formula 1-M = {1 - M:.4f}); 0 in Band_1: {const_in_band}; "
              f"sequential bound = {r['seq']:.4f}; 2 sum dist(U_e,R) = {r['dp']:.4f}")
    # M = 1 is b = s1 + s2 - s1 s2
    a = 10 * (1 - s); b = S1 + S2 - S1 * S2
    print(f"  by hand: V_1(s1) = min_s2[s1 + s2 - s1 s2 + 10(1-s2)] on grid: max|V_1 - 1| = "
          f"{np.max(np.abs(np.min(b + (10 * (1 - s))[None, :], axis=1) - 1)):.1e}")


def random_trees():
    print("\n[Thm 3.1] random 3-bag chains, separators with k points, classes P_0..P_2 in Chebyshev basis")
    cnt = dict(total=0, lower_fail=0, upper_dp_fail=0, upper_seq_fail=0, sum_below=0)
    worst_ratio = 0
    for trial in range(300):
        k1, k2 = rng.integers(4, 8), rng.integers(4, 8)
        a = rng.normal(size=k1); c = rng.normal(size=k2); b = rng.normal(size=(k1, k2)) * rng.uniform(0.3, 2)
        t1 = np.linspace(-1, 1, k1); t2 = np.linspace(-1, 1, k2)
        for deg in [0, 1, 2]:
            B1 = np.polynomial.chebyshev.chebvander(t1, deg)
            B2 = np.polynomial.chebyshev.chebvander(t2, deg)
            r = analyse(a, b, c, B1, B2)
            cnt["total"] += 1
            tol = 1e-8
            if max(r["e1"], r["e2"]) > r["gap"] + tol:
                cnt["lower_fail"] += 1
            if r["gap"] > r["dp"] + tol:
                cnt["upper_dp_fail"] += 1
            if r["gap"] > r["seq"] + tol:
                cnt["upper_seq_fail"] += 1
            if r["e1"] + r["e2"] < r["gap"] - tol:
                cnt["sum_below"] += 1
                worst_ratio = max(worst_ratio, r["gap"] / max(r["e1"] + r["e2"], 1e-12))
    print(f"  {cnt['total']} cases: lower bound 2 max_e dist(Phi_e,Band_e) <= gap violated {cnt['lower_fail']} times; "
          f"gap <= 2 sum_e dist(U_e,Phi_e) violated {cnt['upper_dp_fail']} times; "
          f"gap <= sequential bound violated {cnt['upper_seq_fail']} times")
    print(f"  per-edge sum 2 sum_e dist(Phi_e,Band_e) < gap in {cnt['sum_below']} cases "
          f"(largest gap / per-edge sum = {worst_ratio:.2f}, capped at 1e12 when the sum is 0)")


def T1():
    print("\n[T1] a=-|s1|, b=|s1|-|s2|+K(s1-s2)^2, c=|s2| with a and c children of b; P_n on both edges")
    s = np.unique(np.concatenate([np.linspace(-1, 1, 201), [0.0]]))
    S1, S2 = np.meshgrid(s, s, indexing="ij")
    for n in [4]:
        B = np.polynomial.chebyshev.chebvander(s, n)
        twoE = two_dist(B, np.abs(s))
        for K in [0.0, 1.0, 10.0, 100.0, 1000.0]:
            a = -np.abs(s); c = np.abs(s)
            b = np.abs(S1) - np.abs(S2) + K * (S1 - S2) ** 2
            r = analyse(a, b, c, B, B)
            print(f"  n={n} K={K:7.1f}: gap/2E_n = {r['gap'] / twoE:.4f}; per-edge 2dist = {r['e1'] / twoE:.3f}, "
                  f"{r['e2'] / twoE:.3f} (units of 2E_n)")


if __name__ == "__main__":
    prop33()
    random_trees()
    T1()
