"""Item (3): which ingredient of zb defeats the Section 4 construction?

Build the Lemma 4.1(ii) point (z, beta, B) for a two-point mixture on F = S u {l}, helpers Z1 = [p] \\ F,
and complete it in the full lift in two ways:
  (P1) Remark 4.5's completion: Z, U from the random variables of Remark 4.5 (U_{jm} != 0 on helpers).
  (P2) Z, U from the random-support mixture on F, and Z_{jm} = U_{jm} = U_{mj} = 0 on helper pairs.
For each pair T, (P2) lies in the exact 2x2 hull of the full lift (zeta, beta, zeta zeta', zeta beta',
beta beta') iff B_T - E[xi xi']_T is PSD: the mixture restricted to T is a genuine distribution and the
remainder is a PSD recession term of the (1,1) pattern with weight 0. Report:
  - min over pairs of lambda_min(B_T - E[xi xi']_T)          (>= 0: all full-lift pair hulls hold for P2)
  - lambda_min of [[1, beta'], [beta, B]]                    (Shor PSD in (beta, B))
  - lambda_min of the full moment matrix Y for P1 and P2     (Shor PSD in (1, zeta, beta))
  - max product-cone violation U_jm^2 - Z_jm B_mm for P1 and P2.
Expected: P2 satisfies every full-lift pair hull and the (1, beta) Shor PSD but not the full Shor PSD; P1
satisfies the full Shor PSD but not the product cones. So zb escapes the construction only through the
combination of the lifted products and the PSD constraint on the full moment matrix.
usage: python3 rc_fulllift.py > rc_fulllift.log
"""
import itertools
from rc_common import np


def psd_sqrt(A):
    w, V = np.linalg.eigh(A)
    return (V * np.sqrt(np.clip(w, 0, None))) @ V.T


def main(seed=5, n=6, p=40, t=0.3, sigma=0.5):
    rng = np.random.default_rng(seed)
    X = rng.standard_normal((n, p))
    F = [0, 1, 2, 3]                      # S = {0,1,2}, violator l = 3; mixture S (1-t), S - 2 + 3 (t)
    Z1 = [m for m in range(p) if m not in F]
    supports = [((0, 1, 2), 1 - t), ((0, 1, 3), t)]
    bvals = np.array([0.8, -1.1, 0.6, 0.9])  # conditional coefficients b_j (xi_j = b_j on T)
    zeta = np.array([[1.0 if j in T else 0.0 for j in F] for T, _ in supports])
    w = np.array([wt for _, wt in supports])
    xi = zeta * bvals
    z = w @ zeta
    beta = w @ xi
    Exx = (xi.T * w) @ xi                  # E[xi xi'] on F
    D = Exx - np.outer(beta, beta)
    ZF = (zeta.T * w) @ zeta               # E[zeta zeta']
    UF = (zeta.T * w) @ xi                 # E[zeta_j xi_m]
    # Lemma 4.1(ii)
    XF, XZ = X[:, F], X[:, Z1]
    Wm = XZ @ XZ.T
    Wi = np.linalg.inv(Wm)
    GF = np.sqrt(1 + sigma) * psd_sqrt(D)
    C = -XZ.T @ Wi @ XF @ GF
    PN = np.eye(len(Z1)) - XZ.T @ Wi @ XZ
    q = np.einsum("im,ij,jm->m", XZ, Wi, XZ)
    Lam = np.diag((C ** 2).sum(1) / (sigma * (1 - q) ** 2))
    K = PN @ Lam @ PN
    G = np.zeros((p, len(F))); G[F] = GF; G[Z1] = C
    Bfull = np.zeros((p, p))
    bfull = np.zeros(p); bfull[F] = beta
    zfull = np.zeros(p); zfull[F] = z
    Bfull += np.outer(bfull, bfull) + G @ G.T
    Bfull[np.ix_(Z1, Z1)] += K
    Efull = np.zeros((p, p)); Efull[np.ix_(F, F)] = Exx
    print(f"<X'X, B - beta beta'> = {np.sum((X.T @ X) * (Bfull - np.outer(bfull, bfull))):.1e}")
    # full-lift pair hulls for P2
    worst_pair = min(np.linalg.eigvalsh((Bfull - Efull)[np.ix_(T, T)]).min()
                     for T in itertools.combinations(range(p), 2))
    Mb = np.block([[np.ones((1, 1)), bfull[None, :]], [bfull[:, None], Bfull]])
    print(f"min over all {p * (p - 1) // 2} pairs of lambda_min(B_T - E[xi xi']_T) = {worst_pair:.2e}")
    print(f"lambda_min [[1, beta'], [beta, B]] = {np.linalg.eigvalsh(Mb).min():.2e}")

    def full_Y(Z, U):
        return np.block([[np.ones((1, 1)), zfull[None, :], bfull[None, :]],
                         [zfull[:, None], Z, U], [bfull[:, None], U.T, Bfull]])

    def cone_viol(Z, U):
        return max(U[j, m] ** 2 - Z[j, m] * Bfull[m, m] for j in range(p) for m in range(p) if j != m)

    # P2: mixture moments on F, zero on helpers
    Z2 = np.zeros((p, p)); Z2[np.ix_(F, F)] = ZF
    U2 = np.zeros((p, p)); U2[np.ix_(F, F)] = UF
    # P1 (Remark 4.5): beta-variable on F is xi + sqrt(sigma) chi, on Z1 it is C e + h with
    # e = (1+sigma)^{-1/2} D^{+1/2}[(xi - beta) + sqrt(sigma) chi]; so E[zeta_j beta_m] = E[zeta_j (C e)_m]
    Dp = np.linalg.pinv(psd_sqrt(D))
    Ez_e = ((zeta.T * w) @ (xi - beta)) @ Dp.T / np.sqrt(1 + sigma)   # E[zeta_j e'] (chi independent)
    U1 = U2.copy(); U1[np.ix_(F, Z1)] = Ez_e @ C.T
    for name, (Z, U) in {"P1 (Remark 4.5)": (Z2, U1), "P2 (U = 0 on helpers)": (Z2, U2)}.items():
        print(f"{name}: lambda_min(Y) = {np.linalg.eigvalsh(full_Y(Z, U)).min():.2e}, "
              f"max product-cone violation = {cone_viol(Z, U):.2e}")


if __name__ == "__main__":
    main()
