"""Independent check of Proposition 4 of covering-upper-half.md.

Path: root 2 b s1^2, middle kappa (s1 - s2)^2 - b s2^2, leaf 2 b s2^2 on
[-1, 1]^2, kappa >= 2b.  Edge 1 carries s1, edge 2 carries s2.

Checks (grid of m points, exact minima on the grid):
  - closed forms U_1 = kappa b/(kappa+b) s^2, L_1 = -2b s^2, U_2 = 2b s^2,
    L_2 = -(b (kappa - 2b)/(2b + kappa)) s^2, and 0 in both bands;
  - rho over affine splits, maximized directly over the two slopes
    (constants telescope) with Nelder-Mead from many starts: max = -b;
  - the reduced function U'_1(s1) = min_{s2} [kappa (s1 - s2)^2 - b s2^2]
    after phi_2 = 0: where it is concave, its width above L_1 near 0, and
    the one-cell affine bracket of the reduced band [L_1, U'_1].
"""
import numpy as np
from scipy.optimize import minimize, minimize_scalar


def main():
    m = 1601
    s = np.linspace(-1, 1, m)
    S1, S2 = np.meshgrid(s, s, indexing="ij")
    for b, k in [(1.0, 10.0), (1.0, 2.0), (0.1, 10.0), (0.5, 3.0)]:
        root = 2 * b * s ** 2
        midT = k * (S1 - S2) ** 2 - b * S2 ** 2
        leaf = 2 * b * s ** 2
        F = root[:, None] + midT + leaf[None, :]
        fstar = F.min()
        U1 = (midT + leaf[None, :]).min(axis=1)
        L1 = fstar - root
        U2 = leaf
        V2 = (root[:, None] + midT).min(axis=0)
        L2 = fstar - V2
        e1 = np.max(np.abs(U1 - k * b / (k + b) * s ** 2))
        e2 = np.max(np.abs(L2 + b * (k - 2 * b) / (2 * b + k) * s ** 2))
        inband = min(U1.min(), -L1.max(), U2.min(), -L2.max())

        def rho(lams):
            l1, l2 = lams
            return (np.min(root + l1 * s)
                    + np.min(midT + l2 * S2 - l1 * S1)
                    + np.min(leaf - l2 * s))
        best = -np.inf
        rng = np.random.default_rng(1)
        for st in range(30):
            x0 = rng.uniform(-3, 3, size=2) if st else np.zeros(2)
            res = minimize(lambda x: -rho(x), x0, method="Nelder-Mead",
                           options=dict(xatol=1e-10, fatol=1e-12, maxiter=4000))
            best = max(best, -res.fun)
        # reduced function after phi_2 = 0
        Ured = midT.min(axis=1)
        d2 = np.diff(Ured, 2) / (s[1] - s[0]) ** 2
        conc = s[1:-1][d2 < -1e-9]
        width = (Ured - L1)[np.abs(s) <= 0.2]
        # one-cell affine bracket of the reduced band
        def br(lam):
            return np.max(lam * s - Ured) + np.max(L1 - lam * s)
        rb = minimize_scalar(br, bounds=(-20, 20), method="bounded",
                             options=dict(xatol=1e-12)).fun
        print(f"b={b}, kappa={k}: f*={fstar:.1e}; closed-form errors U_1 "
              f"{e1:.1e}, L_2 {e2:.1e}; min(U_1, -L_1, U_2, -L_2) = "
              f"{inband:.1e} (0 in both bands)")
        print(f"   max over affine splits of rho = {best:.6f} (-b = {-b}); "
              f"gap(Aff) = {fstar - best:.6f}")
        print(f"   reduced U'_1 (phi_2 = 0): concave on [{conc.min():.3f}, "
              f"{conc.max():.3f}] (1 - b/kappa = {1 - b / k:.3f}), convex "
              f"beyond; max width U'_1 - L_1 on |s| <= 0.2: {width.max():.2e}"
              f"; one-cell affine bracket of [L_1, U'_1]: {rb:.4f}")


if __name__ == "__main__":
    main()
