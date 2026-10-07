"""Tree (three-bag chain A - B - C) checks of Theorem 3.1 and its sharpness.

Bags after eliminating private variables: a(s1), b(s1, s2), c(s2).
Split: A: a - phi1, B: b + phi1 - phi2, C: c + phi2.
rho(Phi) = max m_A + m_B + m_C  s.t. bag functions >= m_t on grids.

T1  K sweep: a = -|s1|, b = |s1| - |s2| + K (s1 - s2)^2, c = |s2|, Phi = P_n.
    Both bands are single functions; 2 max_e dist = 2 E_n, 2 sum_e dist = 4 E_n.
T2  per-edge band distances do not control the tree gap (Proposition 3.3):
    s in [0,1]^2, a = G(1 - s1), c = G(1 - s2), b = B s1 s2 + M (s1 + s2 - 2 s1 s2).
T3  random finite instances: gap vs the bag-wise quantity Q and the joint bound.
"""
import numpy as np
from scipy.optimize import linprog
from consistency_lib import cheb_basis

out = None  # opened under __main__ only, so importing this module leaves its log alone


def log(m):
    print(m)
    if out is not None:
        out.write(m + "\n")
        out.flush()


def tree_rho(a, b, c, B1, B2, full1=False, full2=False):
    """a (k1), b (k1 x k2), c (k2) on grids; B1 (k1 x d1), B2 (k2 x d2) bases.
    full=True replaces the class on that edge by all functions on the grid."""
    k1, k2 = b.shape
    if full1:
        B1 = np.eye(k1)
    if full2:
        B2 = np.eye(k2)
    d1, d2 = B1.shape[1], B2.shape[1]
    nv = d1 + d2 + 3  # [c1, c2, mA, mB, mC]
    iA, iB, iC = d1 + d2, d1 + d2 + 1, d1 + d2 + 2
    rows, rhs = [], []
    # a - B1 c1 >= mA  ->  B1 c1 + mA <= a
    R = np.zeros((k1, nv)); R[:, :d1] = B1; R[:, iA] = 1; rows.append(R); rhs.append(a)
    # c + B2 c2 >= mC  -> -B2 c2 + mC <= c
    R = np.zeros((k2, nv)); R[:, d1:d1 + d2] = -B2; R[:, iC] = 1; rows.append(R); rhs.append(c)
    # b + B1 c1 - B2 c2 >= mB -> -B1 c1 + B2 c2 + mB <= b
    R = np.zeros((k1 * k2, nv))
    R[:, :d1] = -np.repeat(B1, k2, axis=0)
    R[:, d1:d1 + d2] = np.tile(B2, (k1, 1))
    R[:, iB] = 1
    rows.append(R); rhs.append(b.reshape(-1))
    cost = np.zeros(nv); cost[[iA, iB, iC]] = -1
    res = linprog(cost, A_ub=np.vstack(rows), b_ub=np.concatenate(rhs),
                  bounds=[(None, None)] * nv, method="highs")
    assert res.status == 0, res.message
    return -res.fun


def fstar(a, b, c):
    return np.min(a[:, None] + b + c[None, :])


def T1():
    log("[T1] gap for Phi = P_n on both edges; K couples s1 and s2")
    s = np.unique(np.concatenate([np.linspace(-1, 1, 161), [0.0]]))
    a, c = -np.abs(s), np.abs(s)
    S1, S2 = np.meshgrid(s, s, indexing="ij")
    for n in [4, 8]:
        B = cheb_basis(s, n)
        # single-edge gap = 2 E_n(|s|) on this grid
        g1 = fstar(a, np.abs(S1) - np.abs(S2), c) - tree_rho(a, np.abs(S1) - np.abs(S2), c, B, B, full2=True)
        for K in [0.0, 0.3, 1.0, 3.0, 10.0, 100.0]:
            b = np.abs(S1) - np.abs(S2) + K * (S1 - S2) ** 2
            fs = fstar(a, b, c)
            g = fs - tree_rho(a, b, c, B, B)
            ge1 = fs - tree_rho(a, b, c, B, B, full2=True)
            ge2 = fs - tree_rho(a, b, c, B, B, full1=True)
            log(f"  n={n} K={K:6.1f}: f*={fs:.3f} gap={g:.5f}  edge-only gaps {ge1:.5f}, {ge2:.5f}  "
                f"(2E_n={g1:.5f}, 4E_n={2 * g1:.5f}); gap/2E_n = {g / g1:.3f}")


def T2():
    log("\n[T2] s in [0,1]^2; per-edge band distances vs the joint gap")
    s = np.linspace(0, 1, 101)
    S1, S2 = np.meshgrid(s, s, indexing="ij")
    G, Bv, M = 10.0, 1.0, 0.8
    a, c = G * (1 - s), G * (1 - s)
    b = Bv * S1 * S2 + M * (S1 + S2 - 2 * S1 * S2)
    fs = fstar(a, b, c)
    for name, deg in [("constants", 0), ("affine", 1), ("P2", 2), ("P4", 4)]:
        Bm = cheb_basis(s, deg, 0.0, 1.0)
        g = fs - tree_rho(a, b, c, Bm, Bm)
        g1 = fs - tree_rho(a, b, c, Bm, Bm, full2=True)
        g2 = fs - tree_rho(a, b, c, Bm, Bm, full1=True)
        log(f"  {name:9s}: f* = {fs:.4f}, gap = {g:.4f}, 2dist(Band_1) = {g1:.4f}, 2dist(Band_2) = {g2:.4f}, "
            f"sum = {g1 + g2:.4f}  -> {'VIOLATES' if g > g1 + g2 + 1e-9 else 'ok'} gap <= sum")


def Q_and_joint(a, b, c, B1, B2):
    """Q = inf_{psi in E, phi in Phi} sum_t max(F_t^psi - F_t^phi), and
    J = inf_{psi in E} sum_e min_phi osc(psi_e - phi_e) (= 2 sum_e dist)."""
    k1, k2 = b.shape
    d1, d2 = B1.shape[1], B2.shape[1]
    fs = fstar(a, b, c)
    # variables: psi1(k1) psi2(k2) mA mB mC phi1(d1) phi2(d2) then extra
    base = k1 + k2 + 3 + d1 + d2
    ip1, ip2 = 0, k1
    iA, iB, iC = k1 + k2, k1 + k2 + 1, k1 + k2 + 2
    if1, if2 = k1 + k2 + 3, k1 + k2 + 3 + d1

    def E_rows(nv):
        rows, rhs = [], []
        R = np.zeros((k1, nv)); R[:, ip1:ip1 + k1] = np.eye(k1); R[:, iA] = 1
        rows.append(R); rhs.append(a)                       # a - psi1 >= mA
        R = np.zeros((k2, nv)); R[:, ip2:ip2 + k2] = -np.eye(k2); R[:, iC] = 1
        rows.append(R); rhs.append(c)                       # c + psi2 >= mC
        R = np.zeros((k1 * k2, nv))
        R[:, ip1:ip1 + k1] = -np.repeat(np.eye(k1), k2, axis=0)
        R[:, ip2:ip2 + k2] = np.tile(np.eye(k2), (k1, 1))
        R[:, iB] = 1
        rows.append(R); rhs.append(b.reshape(-1))           # b + psi1 - psi2 >= mB
        Aeq = np.zeros((1, nv)); Aeq[0, [iA, iB, iC]] = 1
        return rows, rhs, Aeq, np.array([fs])

    # Q: extra cA cB cC
    nv = base + 3
    jA, jB, jC = base, base + 1, base + 2
    rows, rhs, Aeq, beq = E_rows(nv)
    # r1 = psi1 - B1 phi1 (k1), r2 = psi2 - B2 phi2
    R1 = np.zeros((k1, nv)); R1[:, ip1:ip1 + k1] = np.eye(k1); R1[:, if1:if1 + d1] = -B1
    R2 = np.zeros((k2, nv)); R2[:, ip2:ip2 + k2] = np.eye(k2); R2[:, if2:if2 + d2] = -B2
    R = -R1.copy(); R[:, jA] = -1; rows.append(R); rhs.append(np.zeros(k1))     # -r1 <= cA
    R = R2.copy(); R[:, jC] = -1; rows.append(R); rhs.append(np.zeros(k2))      # r2 <= cC
    R = np.repeat(R1, k2, axis=0) - np.tile(R2, (k1, 1)); R[:, jB] = -1
    rows.append(R); rhs.append(np.zeros(k1 * k2))                               # r1 - r2 <= cB
    cost = np.zeros(nv); cost[[jA, jB, jC]] = 1
    rq = linprog(cost, A_ub=np.vstack(rows), b_ub=np.concatenate(rhs), A_eq=Aeq, b_eq=beq,
                 bounds=[(None, None)] * nv, method="highs")
    # joint bound: extra u1 l1 u2 l2
    nv = base + 4
    u1, l1, u2, l2 = base, base + 1, base + 2, base + 3
    rows, rhs, Aeq, beq = E_rows(nv)
    R1 = np.zeros((k1, nv)); R1[:, ip1:ip1 + k1] = np.eye(k1); R1[:, if1:if1 + d1] = -B1
    R2 = np.zeros((k2, nv)); R2[:, ip2:ip2 + k2] = np.eye(k2); R2[:, if2:if2 + d2] = -B2
    R = R1.copy(); R[:, u1] = -1; rows.append(R); rhs.append(np.zeros(k1))
    R = -R1.copy(); R[:, l1] = 1; rows.append(R); rhs.append(np.zeros(k1))
    R = R2.copy(); R[:, u2] = -1; rows.append(R); rhs.append(np.zeros(k2))
    R = -R2.copy(); R[:, l2] = 1; rows.append(R); rhs.append(np.zeros(k2))
    cost = np.zeros(nv); cost[[u1, u2]] = 1; cost[[l1, l2]] = -1
    rj = linprog(cost, A_ub=np.vstack(rows), b_ub=np.concatenate(rhs), A_eq=Aeq, b_eq=beq,
                 bounds=[(None, None)] * nv, method="highs")
    return rq.fun, rj.fun


def T3():
    log("\n[T3] random finite chains (k values per separator): gap, Q, joint bound, band lower bound")
    rng = np.random.default_rng(0)
    k = 5
    s = np.linspace(-1, 1, k)
    worst_Q = 0.0
    counts = {"Q>gap": 0, "total": 0, "sum<gap": 0, "gap=max": 0, "gap=max, both>0": 0}
    examples = []
    for trial in range(300):
        a = rng.normal(size=k)
        c = rng.normal(size=k)
        b = rng.normal(size=(k, k))
        for deg in [0, 1, 2]:
            Bm = cheb_basis(s, deg)
            fs = fstar(a, b, c)
            g = fs - tree_rho(a, b, c, Bm, Bm)
            g1 = fs - tree_rho(a, b, c, Bm, Bm, full2=True)
            g2 = fs - tree_rho(a, b, c, Bm, Bm, full1=True)
            Q, J = Q_and_joint(a, b, c, Bm, Bm)
            counts["total"] += 1
            if g > g1 + g2 + 1e-7:
                counts["sum<gap"] += 1
            # lower end of Theorem 3.1 attained; "both>0": both per-edge distances positive, so sum > max
            if abs(g - max(g1, g2)) <= 1e-7:
                counts["gap=max"] += 1
                if min(g1, g2) > 1e-4:
                    counts["gap=max, both>0"] += 1
                    if len(examples) < 3:
                        examples.append((trial, deg, g, g1, g2))
            if Q > g + 1e-7:
                counts["Q>gap"] += 1
                worst_Q = max(worst_Q, Q - g)
            assert max(g1, g2) <= g + 1e-7, (g1, g2, g)
            assert g <= Q + 1e-7 and Q <= J + 1e-7, (g, Q, J)
            if trial < 4:
                log(f"  trial {trial} deg {deg}: gap={g:.4f}  max_e 2dist(Band_e)={max(g1, g2):.4f}  "
                    f"sum_e={g1 + g2:.4f}  Q={Q:.4f}  joint bound={J:.4f}")
    log(f"  {counts['total']} cases: lower bound max_e <= gap <= Q <= joint bound held in all; "
        f"Q > gap in {counts['Q>gap']} cases (largest excess {worst_Q:.4f}); "
        f"per-edge sum sum_e 2dist(Band_e) < gap in {counts['sum<gap']} cases")
    log(f"  lower end attained (gap = max_e 2dist(Band_e) to 1e-7) in {counts['gap=max']} cases; "
        f"in {counts['gap=max, both>0']} of them both per-edge values exceed 1e-4 (so the sum exceeds the max)")
    for e in examples:
        log("    trial %d deg %d: gap=%.6f  2dist(Band_1)=%.6f  2dist(Band_2)=%.6f" % e)


if __name__ == "__main__":
    out = open("logs/check_tree.log", "w")
    T1()
    T2()
    T3()
