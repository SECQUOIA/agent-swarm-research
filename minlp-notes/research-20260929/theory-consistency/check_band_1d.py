"""One-separator checks of the band identity and of rates for several classes.

Examples (separator s in [-1, 1]; f* = 0 in all of them):
  E1  U = L = -|s|                      kinked, zero-width band (affine recourse)
  E1c U = L = -|s - c|, c = 1/sqrt(7)   same, kink not on any dyadic node
  E2  U = L = -(s_+)^2                  C^{1,1} kink, zero width (quadratic example)
  E3  U = L = (s+2) - (s+2) log(s+2)     analytic, singularity at s = -2
  E4  U = 0.7 s - s^2 - 0.5|s + 0.5|,  L = T - 1.5 (s - 0.3)^2
      (T = tangent of U at s* = 0.3, slope -0.4): kink away from the pinch,
      separator margin w = 0.5 (s - 0.3)^2 for s >= -0.5 and w >= 0.3 below
  E5  U = -(s_+)^2, L = U - c s^2, c = 0.5 and 1.2 (curvature jump at the pinch)
  E6  U = -|s|, L = U - 0.5 s^2           kinked pinch with quadratic width
"""
import numpy as np
import time
from consistency_lib import (poly_gap, cellwise_gap, joint_cellwise_gap,
                             grid, hat_basis, band_gap, eval_gap)

BETA = 0.28016949902386913  # Bernstein's constant: n E_n(|x|) -> BETA
c0 = 1 / np.sqrt(7)

EX = {
    "E1": (lambda s: -np.abs(s), lambda s: -np.abs(s), (0.0,)),
    "E1c": (lambda s: -np.abs(s - c0), lambda s: -np.abs(s - c0), (c0,)),
    "E2": (lambda s: -np.maximum(s, 0) ** 2, lambda s: -np.maximum(s, 0) ** 2, (0.0,)),
    "E3": (lambda s: (s + 2) - (s + 2) * np.log(s + 2),
           lambda s: (s + 2) - (s + 2) * np.log(s + 2), ()),
}


def U4(s):
    return 0.7 * s - s ** 2 - 0.5 * np.abs(s + 0.5)


def T4(s):
    return -0.28 - 0.4 * (s - 0.3)


def L4(s):
    return T4(s) - 1.5 * (s - 0.3) ** 2


EX["E4"] = (U4, L4, (-0.5, 0.3))
EX["E5a"] = (lambda s: -np.maximum(s, 0) ** 2,
             lambda s: -np.maximum(s, 0) ** 2 - 0.5 * s ** 2, (0.0,))
EX["E5b"] = (lambda s: -np.maximum(s, 0) ** 2,
             lambda s: -np.maximum(s, 0) ** 2 - 1.2 * s ** 2, (0.0,))
EX["E6"] = (lambda s: -np.abs(s), lambda s: -np.abs(s) - 0.5 * s ** 2, (0.0,))


def log(msg, fh):
    print(msg)
    fh.write(msg + "\n")
    fh.flush()


def main():
    fh = open("logs/check_band_1d.log", "w")
    t0 = time.time()
    # sanity: band well defined (L <= U) on a fine grid
    s = grid(-1, 1, 200001, (0.0, c0, -0.5, 0.3))
    for k, (U, L, _) in EX.items():
        w = U(s) - L(s)
        log(f"[band] {k}: min(U-L) = {w.min():.3e}, argmin s = {s[np.argmin(w)]:.4f}", fh)

    # 1. polynomial classes
    log("\n[poly] gap(P_n): LP value on grid (lower est.) / LP solution on fine grid (upper est.)", fh)
    degs = [1, 2, 4, 8, 16, 32, 64]
    for k in ["E1", "E2", "E3", "E4", "E5a", "E5b", "E6"]:
        U, L, ex = EX[k]
        for n in degs:
            g, gu = poly_gap(U, L, n, extra=ex)
            extra = ""
            if k == "E1" and n > 1:
                extra = f"  n*gap = {n * g:.4f} (2*beta = {2 * BETA:.4f})"
            if k in ("E2", "E5a", "E6") and n > 1:
                extra = f"  n*gap = {n * g:.4f}, n^2*gap = {n * n * g:.4f}"
            if k == "E3" and n > 1:
                extra = f"  gap^(1/n) = {g ** (1.0 / n) if g > 0 else 0:.4f} (1/rho = {1 / (2 + np.sqrt(3)):.4f})"
            log(f"  {k} n={n:3d}: gap = {g:.6e} / {gu:.6e}{extra}", fh)

    # E2: repository lower bound E_n(h) >= 1/(27 pi (n+2)^2), so gap >= 2/(27 pi (n+2)^2)
    log("\n[E2] compare with repository bound gap = 2E_n(h) >= 2/(27 pi (n+2)^2)", fh)
    for n in [4, 8, 16, 32]:
        U, L, ex = EX["E2"]
        g, _ = poly_gap(U, L, n, extra=ex)
        log(f"  n={n}: gap = {g:.4e} >= {2 / (27 * np.pi * (n + 2) ** 2):.4e}", fh)

    # 2. cellwise classes on uniform meshes (E1c: kink not on a node; E4)
    log("\n[mesh] uniform J cells on [-1,1]: PC (deg 0), PA (deg 1, discontinuous), P1 (continuous hats)", fh)
    for k in ["E1c", "E4"]:
        U, L, ex = EX[k]
        for J in [2, 4, 8, 16, 32, 64, 128]:
            edges = np.linspace(-1, 1, J + 1)
            cells = list(zip(edges[:-1], edges[1:]))
            pc, pcu, _ = cellwise_gap(U, L, cells, [0] * J, extra=ex, m=401, mfine=4001)
            pa, pau, _ = cellwise_gap(U, L, cells, [1] * J, extra=ex, m=401, mfine=4001)
            sg = grid(-1, 1, 20001, ex)
            gh, _, _, _ = band_gap(hat_basis(sg, edges), U(sg), L(sg))
            # closed form for PC: max over cells of (max_D L - min_D U)
            pcf = max(np.max(L(grid(a, b, 4001, ex))) - np.min(U(grid(a, b, 4001, ex)))
                      for a, b in cells)
            h = 2.0 / J
            log(f"  {k} J={J:4d} h={h:.4f}: PC = {pc:.4e} (closed form {pcf:.4e}, /h = {pc / h:.3f}); "
                f"PA = {pa:.4e} (/h = {pa / h:.3f}, /h^2 = {pa / h ** 2:.3f}); P1cont = {gh:.4e}", fh)

    # 3. check gap(cellwise) = max_D g_D against one joint LP
    log("\n[joint] cellwise class: max of per-cell gaps vs one joint LP", fh)
    for k in ["E1c", "E4", "E2"]:
        U, L, ex = EX[k]
        for J, p in [(4, 1), (8, 2), (5, 3)]:
            edges = np.linspace(-1, 1, J + 1)
            cells = list(zip(edges[:-1], edges[1:]))
            gmax, _, _ = cellwise_gap(U, L, cells, [p] * J, extra=ex, m=401, mfine=801)
            gj = joint_cellwise_gap(U, L, cells, [p] * J, m=401, extra=ex)
            log(f"  {k} J={J} p={p}: max_D g_D = {gmax:.6e}, joint LP = {gj:.6e}, diff = {abs(gmax - gj):.1e}", fh)

    # 4. E4: uniform PA bound g_D <= (M_L + M_U) r^2/2 - w_min(D), M_L = 3, M_U = 0
    log("\n[E4] PA bound: gap <= max_D (3/2) r_D^2 - w_min(D)  (r = half width)", fh)
    U, L, ex = EX["E4"]
    for J in [4, 8, 16, 32, 64]:
        edges = np.linspace(-1, 1, J + 1)
        cells = list(zip(edges[:-1], edges[1:]))
        pa, _, gs = cellwise_gap(U, L, cells, [1] * J, extra=ex, m=401, mfine=801)
        bnd = []
        for (a, b) in cells:
            ss = grid(a, b, 2001, ex)
            bnd.append(1.5 * ((b - a) / 2) ** 2 - np.min(U(ss) - L(ss)))
        viol = max(g - bb for g, bb in zip(gs, bnd))
        log(f"  J={J}: PA gap = {pa:.4e}, bound = {max(bnd):.4e}, max_D(g_D - bound_D) = {viol:.2e} (should be <= 0)", fh)

    # 5. E4 adaptive meshes at tolerance eps: bisect cells until the per-cell gap <= eps
    log("\n[E4] adaptive bisection: number of cells to reach gap <= eps", fh)
    for deg, name in [(0, "PC"), (1, "PA")]:
        for eps in [1e-2, 1e-3, 1e-4, 1e-5, 1e-6]:
            cells = [(-1.0, 1.0)]
            done = []
            while cells:
                a, b = cells.pop()
                g, _ = cellwise_gap(U, L, [(a, b)], [deg], extra=ex, m=201, mfine=201)[:2]
                if g <= eps:
                    done.append((a, b))
                else:
                    mid = 0.5 * (a + b)
                    cells += [(a, mid), (mid, b)]
            smallest = min(b - a for a, b in done)
            log(f"  {name} eps={eps:.0e}: cells = {len(done):6d}, smallest width = {smallest:.2e}, "
                f"cells*sqrt(eps) = {len(done) * np.sqrt(eps):.3f}", fh)
    log(f"\nelapsed {time.time() - t0:.1f} s", fh)


if __name__ == "__main__":
    main()
