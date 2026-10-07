"""Does the scout's reimplementation of the Case-4 set (research-20260928b/sfree/code/scout_sfree.py: ms_set)
match SCIP's Case-4 set when kappa != 0?

SCIP (nlhdlr_quadratic.c, computeRestrictionToRay) uses xhat = (x, (w + kappa + r)/(2 sqrt r)),
yhat = (y, (w + kappa - r)/(2 sqrt r)), r = sqrt(1 + kappa^2), so ||xhat||^2 - ||yhat||^2 = q.  The scout's ms_set
also divides x and y by sqrt(r) (as the text of Chmiela et al. reads), which is not a scaling of q when kappa != 0.
This script samples interior points of both sets for q = w - x y + c (Case 4, kappa = c) and reports points of
int C with q < 0 (S-freeness violations).
Usage: python3 check_scout_case4.py
"""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'research-20260928b', 'sfree', 'code'))
from scout_sfree import ms_set   # noqa: E402


def scip_case4(Q, b, c, sbar):
    th, V = np.linalg.eigh(Q)
    bb = V.T @ b
    Ip = [i for i in range(3) if th[i] > 1e-9]; Im = [i for i in range(3) if th[i] < -1e-9]
    I0 = [i for i in range(3) if abs(th[i]) <= 1e-9]
    kappa = c - 0.25 * sum(bb[i] ** 2 / th[i] for i in Ip + Im)
    r = np.sqrt(1 + kappa ** 2); sr = np.sqrt(r)

    def hat(s):
        psi = V.T @ s
        x = np.array([np.sqrt(th[i]) * (psi[i] + bb[i] / (2 * th[i])) for i in Ip])
        y = np.array([np.sqrt(-th[i]) * (psi[i] + bb[i] / (2 * th[i])) for i in Im])
        w = sum(bb[i] * psi[i] for i in I0)
        return np.append(x, (w + kappa + r) / (2 * sr)), np.append(y, (w + kappa - r) / (2 * sr))
    xb, _ = hat(sbar)
    L = xb / np.linalg.norm(xb); lt = L[-1]

    def G(s):
        xh, yh = hat(s)
        ny = np.linalg.norm(yh)
        phi = ny if -lt * ny + yh[-1] <= 0 else np.sqrt(max(0, (1 - lt ** 2) * (ny ** 2 - yh[-1] ** 2))) + lt * yh[-1]
        return phi - L @ xh
    return G


rng = np.random.default_rng(5)
Q = np.zeros((3, 3)); Q[0, 1] = Q[1, 0] = -0.5
b = np.array([0.0, 0.0, 1.0])
q = lambda s, c: float(s @ Q @ s + b @ s + c)
viol = {'scout': 0, 'scip': 0}; ntest = 0; nints = {'scout': 0, 'scip': 0}
for trial in range(200):
    c = rng.choice([-3.0, -1.0, -0.3, 0.3, 1.0, 3.0])
    sbar = rng.normal(size=3) * 2
    if q(sbar, c) <= 0.05:
        continue
    ntest += 1
    for name, G in (('scout', ms_set(Q, b, c, sbar)[0]), ('scip', scip_case4(Q, b, c, sbar))):
        if not G(sbar) < 0:
            continue
        for _ in range(400):
            s = sbar + rng.normal(size=3) * rng.uniform(0.01, 5)
            if G(s) < 0:
                nints[name] += 1
                if q(s, c) < -1e-9:
                    viol[name] += 1
print('corners', ntest, 'interior samples', nints, 'samples with q < 0 (S-freeness violations)', viol)
