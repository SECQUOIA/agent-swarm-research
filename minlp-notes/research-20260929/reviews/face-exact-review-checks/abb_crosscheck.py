"""Referee: toy B&B with per-factor alphaBB (kappa = 0, c = 0), bisection, bound from bb_path.relax(...,'abb')
versus an independent Clarabel solve of the same box-constrained QP.
Usage: python3 abb_crosscheck.py eps n1 n2 ...
"""
import sys
import math
import numpy as np
import scipy.sparse as sp
import clarabel
sys.path.insert(0, "../../theory-face-exact")
import bb_path

b = 0.8
a = (math.sqrt(4 + 4 * b * b) - 2) / 4


def lb_abb(n, l, u):
    at = np.full(n, 2 * a); at[0] = at[-1] = a
    P = np.diag(2 + 2 * at) + np.diag(np.full(n - 1, b), 1) + np.diag(np.full(n - 1, b), -1)
    q = -at * (l + u)
    const = float(np.sum(at * l * u))
    A = sp.vstack([sp.eye(n), -sp.eye(n)]).tocsc()
    st = clarabel.DefaultSettings(); st.verbose = False; st.tol_gap_abs = st.tol_gap_rel = st.tol_feas = 1e-11
    sol = clarabel.DefaultSolver(sp.csc_matrix(np.triu(P)), q, A, np.concatenate([u, -l]), [clarabel.NonnegativeConeT(2 * n)], st).solve()
    return sol.obj_val + const


eps = float(sys.argv[1])
for n in [int(x) for x in sys.argv[2:]]:
    I = bb_path.Inst(n, 0.0, "zero")
    for use in ("highs", "clarabel"):
        stack = [(I.lo.copy(), I.hi.copy())]; leaves = nodes = flips = 0; md = 0.0
        while stack:
            l, u = stack.pop(); nodes += 1
            x1 = bb_path.relax(I, "abb", l, u)[0]; x2 = lb_abb(n, l, u)
            md = max(md, abs(x1 - x2)); flips += (x1 >= -eps) != (x2 >= -eps)
            if (x1 if use == "highs" else x2) >= -eps:
                leaves += 1; continue
            i = int(np.argmax(u - l)); p = 0.5 * (l[i] + u[i])
            u1 = u.copy(); u1[i] = p; l2 = l.copy(); l2[i] = p
            stack += [(l2, u), (l, u1)]
        print(f"abb bisect kappa=0 zero eps={eps:.0e} n={n} bound={use}: leaves={leaves} flips={flips} max|diff|={md:.2e}", flush=True)
