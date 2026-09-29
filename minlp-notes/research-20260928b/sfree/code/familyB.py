"""Family (B): maximal completions C_F^G cap H of sliced orbit sets (bilinear).

Inequality indexed by v in RP^1:  v^T F^T M(t) v >= 0.  Its tangency point with the
null cone is n_v = F^{-T} (Jv)(Jv)^T; it is kept iff the homogenizing coordinate of
n_v is >= 0 (MPS 2026, G = {beta : a^T Gamma(beta) + d^T beta <= 0})."""
import numpy as np
from core import Mmat
J2 = np.array([[0.0, 1.0], [-1.0, 0.0]])
ANG = np.linspace(0, np.pi, 4001)[:-1]
VV = np.stack([np.cos(ANG), np.sin(ANG)], 1)


def hcoord(side, M):
    return M[1, 1] if side == '+' else M[1, 0]


def kept_mask(F, side):
    Fit = np.linalg.inv(F).T
    U = VV @ J2.T                      # rows u = J v
    Fu = U @ Fit.T                     # rows F^{-T} u
    # homogenizing coordinate of n_v = (F^{-T} u) u^T : entry (2,2) for '+', (2,1) for '-'
    h = Fu[:, 1] * (U[:, 1] if side == '+' else U[:, 0])
    return h >= -1e-14


def in_B(F, side, t, mask=None, tol=1e-10):
    if mask is None:
        mask = kept_mask(F, side)
    A = F.T @ Mmat(side, t)
    vals = np.einsum('ij,jk,ik->i', VV, A, VV)
    return np.all(vals[mask] >= -tol * (1 + np.abs(A).max()))


def stepB(F, side, sbar, p, mask=None, amax=1e6):
    if mask is None:
        mask = kept_mask(F, side)
    A = F.T @ Mmat(side, sbar); B = F.T @ Mmat(side, p, h=0.0)
    a = np.einsum('ij,jk,ik->i', VV, A, VV)[mask]
    bb = np.einsum('ij,jk,ik->i', VV, B, VV)[mask]
    if np.any(a <= 0):
        return 0.0
    neg = bb < 0
    if not neg.any():
        return np.inf
    return float(np.min(a[neg] / -bb[neg]))


def boundB(F, side, sbar, P, w):
    mask = kept_mask(F, side)
    al = [stepB(F, side, sbar, P[:, j], mask) for j in range(P.shape[1])]
    vals = [w[j] * al[j] for j in range(len(w)) if np.isfinite(al[j])]
    return min(vals) if vals else np.inf
