"""Python models of SCIP's choice of maximal quadratic-free set.

NOTE  : research-20260928b/sfree/code/scout_sfree.py ms_set, the model used in the earlier
        note ("SCIP's set"), with its bisection step_length.
FIXED : the same construction with the Case-4 scaling as in SCIP's code: x-hat keeps x(s)
        unscaled and only the extra coordinate is divided by 2 (1 + kappa^2)^(1/4).
        (ZIB report 20-29, p. 13, multiplies the whole vector (x(s), (w + kappa + r)/(2 r^(1/2)))
        by r^(-1/2), r = (1 + kappa^2)^(1/2): a positive rescaling of SCIP's (xhat, yhat), hence
        the same set.  ms_set instead divides x(s), y(s) by r^(1/2) but the extra coordinate only
        by 2 r^(1/2), a transcription slip; it agrees with SCIP iff kappa = 0.)
Both take S = {s : s^T Q s + b^T s + c <= 0} in the space SCIP uses and the LP point sbar.
"""
import os, sys
import numpy as np
SFREE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../research-20260928b/sfree/code')
sys.path.insert(0, SFREE)
from scout_sfree import ms_set, step_length   # noqa: E402  (the earlier note's model)


def ms_set_fixed(Q, b, c, sbar, eigtol=1e-9):
    """Chmiela-Munoz-Serrano set with SCIP's lambda rule and SCIP's Case-4 scaling.
    Returns (G, case) with C = {G <= 0}."""
    k = len(sbar)
    th, V = np.linalg.eigh(Q)
    bb = V.T @ b
    Ip = [i for i in range(k) if th[i] > eigtol]
    Im = [i for i in range(k) if th[i] < -eigtol]
    I0 = [i for i in range(k) if abs(th[i]) <= eigtol]
    kappa = c - 0.25 * sum(bb[i] ** 2 / th[i] for i in Ip + Im)
    bI0 = np.array([bb[i] for i in I0])

    def xyz(s):
        psi = V.T @ s
        x = np.array([np.sqrt(th[i]) * (psi[i] + bb[i] / (2 * th[i])) for i in Ip])
        y = np.array([np.sqrt(-th[i]) * (psi[i] + bb[i] / (2 * th[i])) for i in Im])
        z = np.array([psi[i] for i in I0])
        return x, y, z

    case4 = len(I0) > 0 and np.linalg.norm(bI0) > 1e-12
    if not case4:
        G, cs = ms_set(Q, b, c, sbar)        # Cases 1-3 are unchanged
        return G, cs
    r = np.sqrt(1 + kappa ** 2)
    f = r ** 0.5

    def hat(s):
        x, y, z = xyz(s)
        wv = bI0 @ z
        xh = np.append(x, (wv + (kappa + r)) / (2 * f))
        yh = np.append(y, (wv + (kappa - r)) / (2 * f))
        return xh, yh

    xhb, _ = hat(sbar)
    L = xhb / np.linalg.norm(xhb)
    lt = L[-1]

    def phi(y):
        ny = np.linalg.norm(y)
        if -lt * ny + y[-1] <= 0:
            return ny
        return np.sqrt(max(0.0, (1 - lt ** 2) * (ny ** 2 - y[-1] ** 2))) + lt * y[-1]

    def G(s):
        xh, yh = hat(s)
        return phi(yh) - L @ xh
    return G, 'case4'


def steps(G, sbar, P):
    return np.array([step_length(G, sbar, P[:, j]) for j in range(P.shape[1])])


def kappa_case(Q, b, c, eigtol=1e-9):
    k = Q.shape[0]
    th, V = np.linalg.eigh(Q)
    bb = V.T @ b
    nz = np.abs(th) > eigtol
    kappa = c - 0.25 * np.sum(bb[nz] ** 2 / th[nz])
    bI0 = bb[~nz]
    case4 = bI0.size > 0 and np.linalg.norm(bI0) > 1e-12
    npos = int(np.sum(th > eigtol)); nneg = int(np.sum(th < -eigtol))
    if case4:
        cs = 4
    elif abs(kappa) < 1e-12:
        cs = 1
    elif kappa > 0:
        cs = 2
    else:
        cs = 3
    return kappa, cs, npos, nneg
