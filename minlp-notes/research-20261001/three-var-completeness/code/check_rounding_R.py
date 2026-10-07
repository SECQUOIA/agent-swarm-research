"""Probe: is R (D3 + 24 family LMIs) invariant under rounding a diagonal
moment down (note.md, Section 2.1)?

For random objectives c with nonnegative square coefficients we minimize
<c, y> over R intersected with {Y_ii >= m_i + gap} for one coordinate i (this
forces an "intrinsic" excess of the diagonal moment), apply the rounding map
l -> l o rho_i (which keeps the D3 system feasible, Lemma 2.3) and test the
24 family conditions at the rounded point by the separation SDP
    min { <A_g, W> : W psd, W >= 0, tr W = 1 },  A_g = B_g - b_g b_g^T,
which is negative exactly when a family inequality of copy g is violated
(family note, Section 3).  Numerical only.

usage: python check_rounding_R.py SEED N GAP
"""
import sys
import warnings

import cvxpy as cp
import numpy as np

warnings.filterwarnings("ignore")
from check_rounding_numeric import rho_vector  # noqa: E402
from cube3 import FAMILY_REPS, MINDEX, QKEYS, family_b_B, moments_under  # noqa: E402
from sdp3 import SOLVER_OPTS, relaxation_constraints  # noqa: E402

W = cp.Variable((4, 4), symmetric=True)
Apar = cp.Parameter((4, 4), symmetric=True)
sep = cp.Problem(cp.Minimize(cp.trace(Apar @ W)), [W >> 0, W >= 0, cp.trace(W) == 1])


def family_violation(yv):
    worst = np.inf
    for g in FAMILY_REPS:
        m = moments_under(g, lambda k: yv[MINDEX[k]])
        b, B = family_b_B(m)
        b = np.array(b, float)
        A = np.array(B, float) - np.outer(b, b)
        Apar.value = (A + A.T) / 2
        sep.solve(solver='CLARABEL')
        worst = min(worst, sep.value)
    return worst


if __name__ == '__main__':
    seed, n, gap = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3])
    rng = np.random.default_rng(seed)
    y, cons = relaxation_constraints(True, True)
    c = cp.Parameter(10)
    i_par = None
    probs = []
    for i in range(3):
        e2 = tuple(2 if j == i else 0 for j in range(3))
        e1 = tuple(1 if j == i else 0 for j in range(3))
        obj = sum(c[t] * y[MINDEX[k]] for t, k in enumerate(QKEYS))
        probs.append(cp.Problem(cp.Minimize(obj), cons + [y[MINDEX[e2]] >= y[MINDEX[e1]] + gap]))
    worst_before, worst_after, count, viol = np.inf, np.inf, 0, 0
    for it in range(n):
        cv = rng.normal(size=10)
        cv[4:7] = np.abs(cv[4:7])
        i = it % 3
        c.value = cv
        try:
            probs[i].solve(**SOLVER_OPTS)
        except BaseException as e:
            if isinstance(e, KeyboardInterrupt):
                raise
            continue
        if y.value is None or probs[i].status not in ('optimal', 'optimal_inaccurate'):
            continue
        yv = np.array(y.value)
        vb = family_violation(yv)
        va = family_violation(rho_vector(yv, i))
        worst_before = min(worst_before, vb)
        worst_after = min(worst_after, va)
        count += 1
        viol += va < -1e-6
    print('points', count, 'min family value before %.2e' % worst_before,
          'after rounding %.2e' % worst_after, 'violations after rounding (< -1e-6):', viol, flush=True)
