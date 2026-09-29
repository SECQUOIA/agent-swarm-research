"""Item (3): the product cone U_jm^2 <= Z_jm B_mm (Section 5, Remark 4.5).

 (a) Level-2 moment matrix: for random finite distributions of (zeta, beta) with beta_m (1 - zeta_m) = 0,
     the 2x2 principal minor of the degree-4 moment matrix on the monomials {zeta_j zeta_m, beta_m} is
     [[Z_jm, U_jm], [U_jm, B_mm]] (after zeta^2 = zeta, zeta_m beta_m = beta_m), hence PSD.
 (b) Exact 2x2 hull of the full lift (zeta, beta, zeta zeta', zeta beta', beta beta') on a pair {a, b},
     written disjunctively over the four zeta patterns: maximizing U_ab = E[zeta_a beta_b] with Z_ab, B_bb,
     z_a, z_b fixed gives exactly sqrt(Z_ab B_bb). So the full-lift pair hull implies the cone, and the
     cone is its exact projection onto (U_ab, Z_ab, B_bb) for these data.
usage: python3 rc_moment.py > rc_moment.log
"""
import itertools
from rc_common import np
import cvxpy as cp


def part_a(rng, p=4, atoms=6, trials=200):
    worst_id, worst_eig = 0.0, np.inf
    for _ in range(trials):
        w = rng.dirichlet(np.ones(atoms))
        Zs = rng.integers(0, 2, (atoms, p)).astype(float)
        Bs = rng.standard_normal((atoms, p)) * Zs
        E = lambda f: sum(w[t] * f(Zs[t], Bs[t]) for t in range(atoms))
        for j, m in itertools.permutations(range(p), 2):
            # raw degree-4 moments of the monomials u = zeta_j zeta_m and v = beta_m
            Muu = E(lambda z, b: (z[j] * z[m]) ** 2)
            Muv = E(lambda z, b: z[j] * z[m] * b[m])
            Mvv = E(lambda z, b: b[m] ** 2)
            Z, U, B = E(lambda z, b: z[j] * z[m]), E(lambda z, b: z[j] * b[m]), Mvv
            worst_id = max(worst_id, abs(Muu - Z), abs(Muv - U))
            worst_eig = min(worst_eig, np.linalg.eigvalsh(np.array([[Muu, Muv], [Muv, Mvv]])).min(),
                            Z * B - U ** 2)
    print(f"(a) max |minor entry - (Z_jm, U_jm)| = {worst_id:.1e}; min over minors of "
          f"min(eig, Z B - U^2) = {worst_eig:.1e}")


def part_b(cases):
    for za, zb_, Zab, Bbb in cases:
        cons, lam, xs, Xs = [], {}, {}, {}
        for s in [(0, 0), (1, 0), (0, 1), (1, 1)]:
            W = cp.Variable((3, 3), PSD=True)
            for t, on in enumerate(s):
                if not on:
                    cons += [W[t + 1, :] == 0]
            lam[s], xs[s], Xs[s] = W[0, 0], W[1:, 0], W[1:, 1:]
        B = sum(Xs.values())
        cons += [sum(lam.values()) == 1, lam[(1, 0)] + lam[(1, 1)] == za, lam[(0, 1)] + lam[(1, 1)] == zb_,
                 lam[(1, 1)] == Zab, B[1, 1] == Bbb, cp.trace(B) <= 10]
        Uab = xs[(1, 1)][1]           # E[zeta_a beta_b]: only the pattern (1, 1) has zeta_a = 1 and beta_b free
        prob = cp.Problem(cp.Maximize(Uab), cons)
        prob.solve(solver="CLARABEL", tol_gap_abs=1e-10, tol_gap_rel=1e-10, tol_feas=1e-10)
        print(f"(b) z=({za},{zb_}) Z_ab={Zab} B_bb={Bbb}: max U_ab = {prob.value:.9f}, "
              f"sqrt(Z_ab B_bb) = {np.sqrt(Zab * Bbb):.9f}")


if __name__ == "__main__":
    part_a(np.random.default_rng(11))
    part_b([(0.5, 0.6, 0.3, 2.0), (0.9, 0.2, 0.1, 5.0), (0.4, 0.4, 0.0, 3.0)])
