"""Referee check R1: one-separator band identity and cellwise max formula.

Independent of the author's consistency_lib.py.  Two separate LPs:
  (i)  the split relaxation written on the bag data (no value functions):
       rho = max mA + mB  s.t.  GA[i,j] - phi_i >= mA,  GB[i,l] + phi_i >= mB,
       phi = B c in the class;
  (ii) the sup-norm distance from the class to the band [L, U]:
       t* = min t  s.t.  (Bc)_i - U_i <= t,  L_i - (Bc)_i <= t,  t >= 0.
The identity says f* - rho = 2 t* when the class contains the constants.
"""
import numpy as np
from scipy.optimize import linprog

rng = np.random.default_rng(12345)
OPT = {"primal_feasibility_tolerance": 1e-10, "dual_feasibility_tolerance": 1e-10}


def split_rho(GA, GB, B):
    k, d = B.shape
    ny, nz = GA.shape[1], GB.shape[1]
    nv = d + 2
    rows, rhs = [], []
    # (Bc)_i + mA <= GA[i,j]
    for j in range(ny):
        R = np.zeros((k, nv)); R[:, :d] = B; R[:, d] = 1
        rows.append(R); rhs.append(GA[:, j])
    # -(Bc)_i + mB <= GB[i,l]
    for l in range(nz):
        R = np.zeros((k, nv)); R[:, :d] = -B; R[:, d + 1] = 1
        rows.append(R); rhs.append(GB[:, l])
    cost = np.zeros(nv); cost[d] = -1; cost[d + 1] = -1
    r = linprog(cost, A_ub=np.vstack(rows), b_ub=np.concatenate(rhs),
                bounds=[(None, None)] * nv, method="highs", options=OPT)
    assert r.status == 0, r.message
    return -r.fun


def dist_band(B, U, L):
    k, d = B.shape
    nv = d + 1
    R1 = np.hstack([B, -np.ones((k, 1))])
    R2 = np.hstack([-B, -np.ones((k, 1))])
    cost = np.zeros(nv); cost[d] = 1
    r = linprog(cost, A_ub=np.vstack([R1, R2]), b_ub=np.concatenate([U, -L]),
                bounds=[(None, None)] * d + [(0, None)], method="highs", options=OPT)
    assert r.status == 0, r.message
    return r.fun


def partA():
    print("[A] random discrete one-separator instances")
    worst = 0.0
    worst_nc = 0.0
    nc_mismatch = 0
    ntest = 0
    for trial in range(400):
        k = rng.integers(3, 9)
        ny, nz = rng.integers(2, 7), rng.integers(2, 7)
        GA = rng.normal(size=(k, ny)) * rng.uniform(0.2, 3)
        GB = rng.normal(size=(k, nz)) * rng.uniform(0.2, 3)
        U = GA.min(axis=1); V = GB.min(axis=1)
        fs = np.min(U + V)
        L = fs - V
        for d in range(1, k):
            ntest += 1
            B = np.hstack([np.ones((k, 1)), rng.normal(size=(k, d - 1))])
            gap = fs - split_rho(GA, GB, B)
            t = dist_band(B, U, L)
            worst = max(worst, abs(gap - 2 * t))
            # class WITHOUT constants: identity must be applied to Phi + R
            Bn = rng.normal(size=(k, d))
            gapn = fs - split_rho(GA, GB, Bn)
            tn = dist_band(Bn, U, L)
            tnR = dist_band(np.hstack([np.ones((k, 1)), Bn]), U, L)
            worst_nc = max(worst_nc, abs(gapn - 2 * tnR))
            if abs(gapn - 2 * tn) > 1e-6:
                nc_mismatch += 1
    print(f"  {ntest} (instance, class) pairs with constants: max |gap - 2 dist(Phi,Band)| = {worst:.2e}")
    print(f"  classes without constants: max |gap - 2 dist(Phi+R,Band)| = {worst_nc:.2e}; "
          f"gap != 2 dist(Phi,Band) in {nc_mismatch} of {ntest} cases")


def partB():
    print("\n[B] continuous example with explicit bags on grids (positive-width band, kink in U)")
    s = np.linspace(-1, 1, 201)
    y = np.linspace(-1.5, 1.5, 241)
    z = np.linspace(-1, 1, 201)
    S, Y = np.meshgrid(s, y, indexing="ij")
    GA = Y ** 4 / 4 - S * Y + 0.3 * S ** 2 + 0.2 * np.abs(S - 0.5)
    S2, Z = np.meshgrid(s, z, indexing="ij")
    GB = 0.5 * Z ** 2 + Z * (S2 - 0.2) + S2 ** 2 + 0.1 * np.cos(3 * S2 * Z)
    U = GA.min(axis=1); V = GB.min(axis=1)
    fs = np.min(U + V); L = fs - V
    w = U - L
    print(f"  f* = {fs:.6f}, pinch at s = {s[np.argmin(w)]:.3f}, max width = {w.max():.3f}")
    t = (s + 0) / 1.0
    for n in [0, 1, 2, 3, 4, 6, 8]:
        B = np.polynomial.chebyshev.chebvander(t, n)
        gap = fs - split_rho(GA, GB, B)
        d = dist_band(B, U, L)
        # zero-width comparison: 2 dist(U, P_n) and 2 dist(L, P_n) (Cor 2.2(3))
        dU = dist_band(B, U, U); dL = dist_band(B, L, L)
        lo = 2 * max(dU, dL) - w.max(); hi = 2 * min(dU, dL)
        print(f"  P_{n}: gap = {gap:.8f}, 2 dist(Band) = {2 * d:.8f}, diff = {gap - 2 * d:.1e}; "
              f"Cor 2.2(3): {lo:.4f} <= gap <= {hi:.4f} -> {'ok' if lo - 1e-9 <= gap <= hi + 1e-9 else 'FAIL'}")
    # cellwise class: piecewise constants / affine on J cells; compare joint LP to max of cells
    for J in [2, 4, 8]:
        edges = np.linspace(-1, 1, J + 1)
        cell = np.minimum(np.searchsorted(edges, s, side="right") - 1, J - 1)
        for p in [0, 1]:
            cols = []
            for D in range(J):
                m = cell == D
                for q in range(p + 1):
                    col = np.zeros_like(s); col[m] = s[m] ** q; cols.append(col)
            B = np.column_stack(cols)
            gap = fs - split_rho(GA, GB, B)
            gD = []
            for D in range(J):
                m = cell == D
                Bm = np.column_stack([s[m] ** q for q in range(p + 1)])
                # per-cell bracket g_D = min a+b s.t. Bc - U <= a, L - Bc <= b (may be negative)
                k, dd = Bm.shape
                A1 = np.hstack([Bm, -np.ones((k, 1)), np.zeros((k, 1))])
                A2 = np.hstack([-Bm, np.zeros((k, 1)), -np.ones((k, 1))])
                cost = np.zeros(dd + 2); cost[dd:] = 1
                r = linprog(cost, A_ub=np.vstack([A1, A2]), b_ub=np.concatenate([U[m], -L[m]]),
                            bounds=[(None, None)] * (dd + 2), method="highs", options=OPT)
                gD.append(r.fun)
            closed = max(L[cell == D].max() - U[cell == D].min() for D in range(J)) if p == 0 else None
            extra = f", closed form max_D(sup L - inf U) = {closed:.8f}" if p == 0 else ""
            print(f"  J={J} p={p}: joint gap = {gap:.8f}, max_D g_D = {max(gD):.8f}{extra}")


if __name__ == "__main__":
    partA()
    partB()
