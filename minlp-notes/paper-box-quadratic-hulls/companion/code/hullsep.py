"""Exact separation from the 3-cube quadratic moment hull (QPB3) by a small SDP.

For a triple moment matrix M (4x4, [1 x'; x X]) solve
    delta(M) = min <C, M>  s.t.  Abar_p' C Abar_p - N_p in PSD,  N_p >= 0 (zero diag),
                                 <C, MC> = 1,
for the five tetrahedra p of a triangulation of the cube.  By Anstreicher-Burer
Theorem 7 and COP_4 = PSD_4 + N_4, the feasible C are exactly the normalized
cube-nonnegative quadratics, so delta(M) < 0 iff M is outside QPB3.  The optimal
C gives a valid cut <C, M> >= 0 after a small certified shift of its constant
term (see certify_cut).
"""

import numpy as np
import scipy.sparse as sp
import clarabel
from relax import ABAR5, MC

SQ2 = np.sqrt(2.0)
UPPER = [(i, j) for j in range(4) for i in range(j + 1)]       # Clarabel svec order
CIDX = {}
for t, (i, j) in enumerate([(i, j) for i in range(4) for j in range(i, 4)]):
    CIDX[(i, j)] = CIDX[(j, i)] = t
NPAIRS = [(i, j) for i in range(4) for j in range(i + 1, 4)]


def _template(tets=ABAR5):
    nC = 10
    nN = 6 * len(tets)
    nv = nC + nN
    rows, cols, vals, b = [], [], [], []
    r = 0
    # equality <C, MC> = 1
    for (i, j), t in [((i, j), CIDX[(i, j)]) for i in range(4) for j in range(i, 4)]:
        co = MC[i, j] * (1 if i == j else 2)
        rows.append(r); cols.append(t); vals.append(co)
    b.append(1.0)
    r += 1
    # N >= 0  ->  s = N  -> A = -I
    for p in range(len(tets)):
        for q in range(6):
            rows.append(r); cols.append(nC + 6 * p + q); vals.append(-1.0); b.append(0.0); r += 1
    # PSD blocks: s = svec(Abar' C Abar - N)
    for p, Ab in enumerate(tets):
        for (i, j) in UPPER:
            sc = 1.0 if i == j else SQ2
            # (Ab' C Ab)_ij = sum_rc Ab[r,i] C_rc Ab[c,j]
            coef = {}
            for rr in range(4):
                for cc in range(4):
                    co = Ab[rr, i] * Ab[cc, j]
                    if co:
                        t = CIDX[(rr, cc)]
                        coef[t] = coef.get(t, 0.0) + co
            for t, co in coef.items():
                rows.append(r); cols.append(t); vals.append(-co * sc)
            if i != j:
                q = NPAIRS.index((i, j))
                rows.append(r); cols.append(nC + 6 * p + q); vals.append(1.0 * sc)
            b.append(0.0)
            r += 1
    A = sp.csc_matrix((vals, (rows, cols)), shape=(r, nv))
    cones = [clarabel.ZeroConeT(1), clarabel.NonnegativeConeT(nN)] + [clarabel.PSDTriangleConeT(4)] * len(tets)
    return A, np.array(b), cones, nv


_A, _b, _cones, _nv = _template()


def _settings():
    st = clarabel.DefaultSettings()
    st.verbose = False
    st.max_threads = 1
    st.tol_gap_abs = 1e-9
    st.tol_gap_rel = 1e-9
    st.tol_feas = 1e-9
    st.presolve_enable = False
    st.chordal_decomposition_enable = False
    return st


def depth(M):
    """Return (delta, C 4x4)."""
    q = np.zeros(_nv)
    for i in range(4):
        for j in range(i, 4):
            q[CIDX[(i, j)]] = M[i, j] * (1 if i == j else 2)
    P = sp.csc_matrix((_nv, _nv))
    s = clarabel.DefaultSolver(P, q, _A, _b, _cones, _settings())
    sol = s.solve()
    c = np.array(sol.x)[:10]
    C = np.zeros((4, 4))
    for i in range(4):
        for j in range(i, 4):
            C[i, j] = C[j, i] = c[CIDX[(i, j)]]
    return float(sol.obj_val), C, str(sol.status)


def certify_cut(C, tets=ABAR5):
    """Return delta >= 0 such that q_C + delta >= 0 on the cube, using the
    decomposition Abar' C Abar = PSD + NN + R on each tetrahedron and
    lambda' R lambda >= -max|R| for barycentric lambda.  Floating point."""
    worst = 0.0
    for Ab in tets:
        G = Ab.T @ C @ Ab
        # split: N = positive part of off-diagonal of (G - PSD part); simple certified split:
        # take the DNN-free decomposition from eigen-clipping G - N with N from off-diagonal
        # clipping; we only need a valid lower bound of min lambda'G lambda on the simplex.
        from relax import stqp_min
        val, _ = stqp_min(G[None])
        worst = min(worst, float(val[0]))
    # stqp_min is exact up to rounding for 4x4; add a margin
    return max(0.0, -worst) + 1e-12 * (1 + np.abs(C).max())
