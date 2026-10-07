"""How often does the cone of the projected rays P equal R^3 on the McCormick LP corners
of the sfree note (Section 9.2)?  When cone(P) = R^k, Conforti et al. (MOR 2015, Thm 6.3)
give exact attainment of the corner bound by the polytope conv{sbar + (z_K/w_j) p_j}
(see note.md, Proposition A).  Replays the generator of
research-20260928b/sfree/code/exp_mccormick.py with the same seeds and filters
(including the SCIP single-constraint bound z1 > 1e-6), without the orbit computations.
Usage: python3 cone_span_mccormick.py SEED NTRIALS [p npairs nlin]
"""
import sys, os, json
import numpy as np
from scipy.optimize import linprog
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../research-20260928b/sfree/code'))
import exp_mccormick as em
from core import qval, bilinear_quadratic


def cone_is_whole_space(P, tol=1e-9):
    """cone(P) = R^k  iff  {y : P^T y <= 0} = {0}."""
    k = P.shape[0]
    for i in range(k):
        for s in (1.0, -1.0):
            cvec = np.zeros(k); cvec[i] = -s           # maximize s*y_i
            r = linprog(cvec, A_ub=P.T, b_ub=np.zeros(P.shape[1]), bounds=[(-1, 1)] * k, method='highs')
            if r.status != 0 or -r.fun > tol:
                return False
    return True


if __name__ == '__main__':
    seed = int(sys.argv[1]); T = int(sys.argv[2])
    SIZE = tuple(int(a) for a in sys.argv[3:6]) if len(sys.argv) > 5 else (4, 4, 3)
    em.rng = np.random.default_rng(seed)
    n_all = n_span = 0
    rows = []
    for trial in range(T):
        I = em.make_instance(*SIZE)
        out = em.solve_lp(I)
        if out is None:
            continue
        h, A, bb = out
        bc = em.basis_cone(I, h, A, bb)
        if bc is None:
            continue
        x, R, w, Ab, rhs, zlp = bc
        p = I['p']
        viol = [(abs(x[p + e] - x[i] * x[j]), e) for e, (i, j) in enumerate(I['pairs'])]
        vmax, e = max(viol)
        if vmax < 1e-4:
            continue
        i, j = I['pairs'][e]; idx = [i, j, p + e]
        P = R[idx, :]
        z1 = em.single_constraint_bound(I, e) - zlp
        if z1 < 1e-6:
            continue
        span = cone_is_whole_space(P)
        nz = int(np.sum(w < 1e-9))
        n_all += 1; n_span += span
        rows.append(dict(trial=trial, N=P.shape[1], cone_is_R3=bool(span), nzero_w=nz))
        print(json.dumps(rows[-1]), flush=True)
    print('SUMMARY', json.dumps(dict(seed=seed, size=SIZE, n=n_all, cone_is_R3=n_span)))
