"""Numerical SDPs (cvxpy + Clarabel) for the three-variable completeness study.

These are discovery tools.  Every reported counterexample is re-certified in
exact rational arithmetic by separate scripts.
"""

import cvxpy as cp
import numpy as np

from cube3 import (FAMILY_REPS, MINDEX, MKEYS, QINDEX, QKEYS, SIMPLICES,
                   STATUSES, family_b_B, hom_matrix, localizing_polys,
                   moments_under, uniform_moments)

SOLVER_OPTS = dict(solver="CLARABEL", tol_gap_abs=1e-9, tol_gap_rel=1e-9,
                   tol_feas=1e-9, max_iter=500)


def relaxation_constraints(use_family=True, use_d3=True, reps=None):
    """Variables and constraints of R.

    Returns (y, constraints) where y is a cvxpy vector over MKEYS."""
    y = cp.Variable(len(MKEYS))
    cons = [y[MINDEX[(0, 0, 0)]] == 1]

    def ymap(k):
        return y[MINDEX[k]]

    if use_d3:
        for status in STATUSES:
            polys = localizing_polys(status)
            n = len(polys)
            M = cp.bmat([[sum(v * ymap(k) for k, v in polys[a][b].items())
                          for b in range(n)] for a in range(n)])
            cons.append(M >> 0)
    else:
        # Only the quadratic moment matrix must be PSD in that case.
        polys = localizing_polys((-1, -1, -1))
        M = cp.bmat([[sum(v * ymap(k) for k, v in polys[a][b].items())
                      for b in range(4)] for a in range(4)])
        cons.append(M >> 0)
    if use_family:
        for g in (FAMILY_REPS if reps is None else reps):
            m = moments_under(g, ymap)
            b, B = family_b_B(m)
            N = cp.Variable((4, 4), symmetric=True)
            cons += [N >= 0, cp.diag(N) == 0]
            Mat = cp.bmat([[cp.reshape(1.0 + 0 * y[0], (1, 1), order="F"),
                            cp.reshape(cp.hstack(b), (1, 4), order="F")],
                           [cp.reshape(cp.hstack(b), (4, 1), order="F"),
                            cp.bmat(B) - N]])
            cons.append(Mat >> 0)
    return y, cons


class Relaxation:
    """min <p, y> over R, with p a parameter."""

    def __init__(self, use_family=True, use_d3=True, reps=None):
        self.y, cons = relaxation_constraints(use_family, use_d3, reps)
        self.c = cp.Parameter(len(QKEYS))
        obj = sum(self.c[i] * self.y[MINDEX[k]] for i, k in enumerate(QKEYS))
        self.prob = cp.Problem(cp.Minimize(obj), cons)

    def solve(self, pvec):
        self.c.value = np.asarray(pvec, float)
        val = self.prob.solve(**SOLVER_OPTS)
        return val, self.prob.status, np.array(self.y.value)


class Separation:
    """min <p, w> over p in P3plus with <p, u> = 1 (u = uniform moments)."""

    def __init__(self, diag_nonneg=True):
        self.pv = cp.Variable(len(QKEYS))
        self.w = cp.Parameter(len(QKEYS))
        u = uniform_moments()
        cons = [sum(self.pv[i] * u[k] for i, k in enumerate(QKEYS)) == 1]
        if diag_nonneg:
            cons += [self.pv[QINDEX[(2, 0, 0)]] >= 0,
                     self.pv[QINDEX[(0, 2, 0)]] >= 0,
                     self.pv[QINDEX[(0, 0, 2)]] >= 0]
        P = self.hom_expr()
        for V in SIMPLICES:
            M = V.T @ P @ V
            N = cp.Variable((4, 4), symmetric=True)
            cons += [N >= 0, M - N >> 0]
        self.prob = cp.Problem(cp.Minimize(self.w @ self.pv), cons)

    def hom_expr(self):
        pv = self.pv
        e = {k: pv[i] for i, k in enumerate(QKEYS)}
        rows = [
            [e[(0, 0, 0)], e[(1, 0, 0)] / 2, e[(0, 1, 0)] / 2, e[(0, 0, 1)] / 2],
            [e[(1, 0, 0)] / 2, e[(2, 0, 0)], e[(1, 1, 0)] / 2, e[(1, 0, 1)] / 2],
            [e[(0, 1, 0)] / 2, e[(1, 1, 0)] / 2, e[(0, 2, 0)], e[(0, 1, 1)] / 2],
            [e[(0, 0, 1)] / 2, e[(1, 0, 1)] / 2, e[(0, 1, 1)] / 2, e[(0, 0, 2)]],
        ]
        return cp.bmat(rows)

    def solve(self, wvec):
        self.w.value = np.asarray(wvec, float)
        val = self.prob.solve(**SOLVER_OPTS)
        return val, self.prob.status, np.array(self.pv.value)


def cube_min(pvec):
    """Exact numerical minimum of a quadratic over the cube by face
    enumeration (falls back to a fine check on singular faces)."""
    from cube3 import face_minimizers, quad_from_vector
    p = quad_from_vector(pvec)
    vals = [v for (_, _, v) in face_minimizers(p, tol=-1e-12)]
    return min(vals)
