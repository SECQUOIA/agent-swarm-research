"""Numerical check of Proposition 11 (minimizer on the boundary of the box with
strict complementarity), see ../../proofs-12-11.md.

f(x) = x1 + x2^2 + x3^2 + a x2 x3 + b x1 x2 on B0 = [0, 0.5] x [-0.4, 0.6] x [-0.5, 0.45],
a = 1, b = 0.5.  x* = 0, f* = 0, active set A = {1} (x1 = l1 = 0, g1 = 1 > 0),
free set F = {2, 3} (g_F = 0).  Relaxation: composite McCormick of the sum, i.e.
x1 + x2^2 + x3^2 + a*McC(x2 x3) + b*McC(x1 x2) with McCormick underestimators on
the current box.  Iterated exact OBBT with cutoff U = f* + eps (convex programs,
cvxpy/Clarabel, solved in coordinates normalised to the current box).

Predictions of Proposition 11 / Lemma 11.2:
  * free widths contract linearly with ratio -> rho(a) = (sqrt(2a^2+4a) - a)/2
    (the reduced tangent map is Phi of Proposition 7);
  * active width: width_1(B_{k+1}) ~ (eps - m_k)/g_1 with
    m_k = min over the free box of B_k of [x2^2 + x3^2 + a*McC(x2 x3)] = -G w_k^2,
    so width_1(B_{k+1}) / (eps - m_k) -> 1 and width_1 = O(free width^2);
  * for eps > 0: free widths stall at Theta(sqrt(eps)), the active width at Theta(eps).
Run with ~/miniconda3/envs/minlp-notes/bin/python prop11_obbt.py
"""
import numpy as np
import cvxpy as cp

A_COEF, B_COEF = 1.0, 0.5
B0 = (np.array([0.0, -0.4, -0.5]), np.array([0.5, 0.6, 0.45]))


def solve(prob):
    """Clarabel with a few settings (the programs become degenerate as the box shrinks)."""
    for kw in ({"equilibrate_enable": False}, {}, {"static_regularization_constant": 1e-7},
               {"equilibrate_enable": False, "max_iter": 1000, "tol_feas": 1e-7}):
        try:
            prob.solve(solver=cp.CLARABEL, **kw)
        except cp.error.SolverError:
            continue
        if prob.status in ("optimal", "optimal_inaccurate"):
            return
    raise RuntimeError("solver failed")


def mcc_under(x, y, lx, ux, ly, uy):
    """Epigraph pieces of the McCormick underestimator of x*y on [lx,ux]x[ly,uy]."""
    return [ly * x + lx * y - lx * ly, uy * x + ux * y - ux * uy]


def obbt_round(lo, hi, U):
    wid = hi - lo
    S = max(wid[1], wid[2]) ** 2          # scale of phi near x* (free width squared)
    y = cp.Variable(3)
    t23, t12 = cp.Variable(), cp.Variable()
    x = lo + cp.multiply(wid, y)
    cons = [y >= 0, y <= 1]
    cons += [t23 >= p / S for p in mcc_under(x[1], x[2], lo[1], hi[1], lo[2], hi[2])]
    cons += [t12 >= p / S for p in mcc_under(x[0], x[1], lo[0], hi[0], lo[1], hi[1])]
    phi = (x[0] + cp.square(x[1]) + cp.square(x[2])) / S + A_COEF * t23 + B_COEF * t12
    cons.append(phi <= U / S)
    newlo, newhi = lo.copy(), hi.copy()
    for i in range(3):
        for sense in (+1, -1):
            prob = cp.Problem(cp.Minimize(sense * y[i]), cons)
            solve(prob)
            yi = y.value[i]
            if sense > 0:   # widen by 1e-8 of the width to stay valid under solver tolerances
                newlo[i] = max(lo[i], lo[i] + wid[i] * (yi - 1e-8))
            else:
                newhi[i] = min(hi[i], lo[i] + wid[i] * (yi + 1e-8))
    return newlo, newhi


def free_relaxed_min(lo, hi):
    """m = min over the free box of x2^2 + x3^2 + a*McC(x2 x3) (the -G w^2 term)."""
    x = cp.Variable(2)
    t = cp.Variable()
    S = max(hi[1] - lo[1], hi[2] - lo[2]) ** 2
    cons = [x >= lo[1:], x <= hi[1:]]
    cons += [t >= p / S for p in mcc_under(x[0], x[1], lo[1], hi[1], lo[2], hi[2])]
    prob = cp.Problem(cp.Minimize(cp.sum_squares(x) / S + A_COEF * t), cons)
    solve(prob)
    return prob.value * S


def run(eps, iters):
    lo, hi = B0[0].copy(), B0[1].copy()
    rows = []
    for k in range(iters):
        wF = max(hi[1] - lo[1], hi[2] - lo[2])
        m = free_relaxed_min(lo, hi)
        nlo, nhi = obbt_round(lo, hi, eps)
        nwF = max(nhi[1] - nlo[1], nhi[2] - nlo[2])
        rows.append((k, wF, hi[0] - lo[0], nwF / wF, (nhi[0] - nlo[0]) / (eps - m),
                     (nhi[0] - nlo[0]) / wF ** 2))
        lo, hi = nlo, nhi
    return rows, lo, hi


if __name__ == "__main__":
    rho = (np.sqrt(2 * A_COEF ** 2 + 4 * A_COEF) - A_COEF) / 2
    print(f"a = {A_COEF}, b = {B_COEF}; predicted free ratio rho(a) = {rho:.6f}")
    print("\neps = 0")
    print(f"{'k':>3} {'free width':>11} {'act width':>11} {'free ratio':>10} "
          f"{'act_{k+1}/(eps-m_k)':>19} {'act_{k+1}/wF_k^2':>16}")
    # Beyond about 28 rounds (active width ~1e-8 against free width ~1e-4) the
    # degenerate programs exceed Clarabel's accuracy and the iteration stalls
    # numerically, so we stop there.
    rows, lo, hi = run(0.0, 28)
    for r in rows:
        if r[0] % 3 == 0 or r[0] == 27:
            print(f"{r[0]:3d} {r[1]:11.3e} {r[2]:11.3e} {r[3]:10.6f} {r[4]:19.6f} {r[5]:16.6f}")
    # Stall prediction: a symmetric free box [-h, h]^2 is a fixed point of the scaled
    # map once Q_min(1) = 1 - a^2/4 <= eps/h^2 (Proposition 7's computation), so the
    # free width is 2 sqrt(eps/(1 - a^2/4)) and the active width is
    # (eps + a h^2)/g_1 = eps (1 + a/(1 - a^2/4)).
    c = 1 - A_COEF ** 2 / 4
    print(f"\neps > 0: widths after 60 rounds (stalled); predicted free/sqrt(eps) = "
          f"{2 / np.sqrt(c):.4f}, act/eps = {1 + A_COEF / c:.4f}")
    print(f"{'eps':>8} {'free width':>11} {'free/sqrt(eps)':>14} {'act width':>11} {'act/eps':>8}")
    for eps in [1e-3, 1e-4, 1e-5, 1e-6, 1e-7]:
        rows, lo, hi = run(eps, 60)
        wF = max(hi[1] - lo[1], hi[2] - lo[2])
        wA = hi[0] - lo[0]
        print(f"{eps:8.0e} {wF:11.3e} {wF / np.sqrt(eps):14.4f} {wA:11.3e} {wA / eps:8.4f}")
