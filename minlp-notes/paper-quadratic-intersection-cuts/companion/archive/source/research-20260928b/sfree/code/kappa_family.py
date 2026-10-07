"""Tangent-edge analysis for the sliced orbit family (bilinear).

If the corner minimizer t0 lies in the relative interior of the edge [v_i, v_j] of
T* = conv(sbar, v_1..v_N), v_j = sbar + (z/w_j) p_j, then any invertible F with
C_F containing T* satisfies  F^T = theta * J adj(M(d) + kappa M(t0))  (d = v_i - v_j),
with the sign of theta fixed by t0.  Each vertex v gives the kappa-set
{kappa : sym(F_kappa^T M(v)) >= 0}; the orbit contains T* iff these sets intersect.
"""
import numpy as np
from core import Mmat

J2 = np.array([[0.0, 1.0], [-1.0, 0.0]])


def adj(A):
    return np.array([[A[1, 1], -A[0, 1]], [-A[1, 0], A[0, 0]]])


def kappa_pencil(side, t0, d):
    Md = Mmat(side, d, h=0.0); M0 = Mmat(side, t0)
    G0 = J2 @ adj(Md); G1 = J2 @ adj(M0)
    X = G0 @ M0; X = (X + X.T) / 2          # = c b0 b0^T, independent of kappa
    sgn = 1.0 if np.trace(X) > 0 else -1.0
    return sgn * G0, sgn * G1


def kappa_interval(G0, G1, side, v, strict=False, grid=None):
    """Return the set {kappa : sym((G0 + kappa G1) M(v)) >= 0} as a list of intervals
    (exact: diagonal entries affine in kappa, determinant quadratic in kappa)."""
    M = Mmat(side, v)
    A = G0 @ M; A = (A + A.T) / 2
    B = G1 @ M; B = (B + B.T) / 2
    # conditions: A11 + k B11 >= 0, A22 + k B22 >= 0, det(A + k B) >= 0
    # det(A + kB) = detA + k (A11 B22 + A22 B11 - 2 A12 B12) + k^2 detB
    c0 = np.linalg.det(A); c1 = A[0, 0] * B[1, 1] + A[1, 1] * B[0, 0] - 2 * A[0, 1] * B[0, 1]; c2 = np.linalg.det(B)
    return (A, B, (c2, c1, c0))


def feasible_kappas(G0, G1, side, verts, kgrid):
    ok = np.ones(len(kgrid), bool)
    for v in verts:
        M = Mmat(side, v)
        for idx, k in enumerate(kgrid):
            X = (G0 + k * G1) @ M; X = (X + X.T) / 2
            if np.linalg.eigvalsh(X)[0] < -1e-12:
                ok[idx] = False
    return ok
