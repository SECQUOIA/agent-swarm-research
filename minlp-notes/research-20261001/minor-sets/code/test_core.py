"""Sanity checks of minor_core.py (targeted, numerical).

1. SCIP's literal step-length formula (sepa_interminor.c) equals the step length of C_U,
   U the polar rotation of Mbar (note, Prop. 1), on random points and rays.
2. U^T Mbar is symmetric positive definite and U^T lies in span{I, J} (so SCIP's set is the
   unique member of bcm and pr families, note Prop. 3(4)).
3. z_K from support enumeration vs a global solve with SCIP (PySCIPOpt) on random corners.
4. Family nesting: scip <= bcm <= orbit and scip <= pr <= orbit <= z_K on random corners.
Usage: python3 test_core.py SEED
"""
import sys
import numpy as np
import pyscipopt as ps
from minor_core import (mat, det4, step, polar_rotation, scip_interminor_step, zK, family_bounds, I2, J2)

seed = int(sys.argv[1]) if len(sys.argv) > 1 else 0
rng = np.random.default_rng(seed)


def rand_point():
    while True:
        s = rng.normal(size=4)
        if det4(s) > 0.05:
            return s


# 1, 2
worst = 0.0
nfin = 0
for _ in range(2000):
    s = rand_point()
    U = polar_rotation(mat(s))
    PS = U.T @ mat(s)
    assert abs(PS[0, 1] - PS[1, 0]) < 1e-10 and np.linalg.eigvalsh(0.5 * (PS + PS.T))[0] > 0
    cf = np.linalg.lstsq(np.stack([I2.ravel(), J2.ravel()], 1), U.T.ravel(), rcond=None)
    assert np.allclose(cf[0][0] * I2 + cf[0][1] * J2, U.T)
    p = rng.normal(size=4)
    a1 = step(U.T, s, p)
    a2 = scip_interminor_step(s, p)
    if np.isfinite(a1) or np.isfinite(a2):
        nfin += 1
        worst = max(worst, abs(a1 - a2) / max(1.0, abs(a1)))
print('1-2: polar/point-rule identities hold on 2000 points; max rel. diff of step lengths '
      'C_U vs SCIP formula = %.2e over %d finite rays' % (worst, nfin))


# 3
def scip_zk(sbar, P, w):
    m = ps.Model()
    m.hideOutput()
    m.setParam('limits/time', 60)
    N = P.shape[1]
    lam = [m.addVar(lb=0, ub=1e4) for _ in range(N)]
    s = [sbar[i] + ps.quicksum(P[i, j] * lam[j] for j in range(N)) for i in range(4)]
    m.addCons(s[0] * s[3] - s[1] * s[2] <= 0)
    m.setObjective(ps.quicksum(w[j] * lam[j] for j in range(N)))
    m.optimize()
    if m.getStatus() == 'infeasible':
        return np.inf
    return m.getObjVal()


mx = 0.0
cnt = 0
for trial in range(40):
    s = rand_point()
    N = int(rng.integers(3, 7))
    P = rng.normal(size=(4, N))
    w = rng.uniform(0.2, 2.0, N)
    a = zK(s, P, w)
    b = scip_zk(s, P, w)
    if not np.isfinite(a) and not np.isfinite(b):
        continue
    cnt += 1
    rel = abs(a - b) / max(1.0, abs(b))
    mx = max(mx, rel)
    if rel > 1e-4:
        print('MISMATCH', trial, a, b)
print('3: z_K vs SCIP global solve on %d corners with finite z_K: max rel. diff %.2e' % (cnt, mx))

# 4
viol = 0
for trial in range(15):
    s = rand_point()
    P = rng.normal(size=(4, 4))
    w = rng.uniform(0.2, 2.0, 4)
    zk = zK(s, P, w)
    if not np.isfinite(zk):
        continue
    fb = family_bounds(s, P, w, zk, iters=30)
    r = {k: v['ratio'] for k, v in fb.items()}
    tol = 2e-6
    ok = (r['scip'] <= r['bcm'] + tol and r['bcm'] <= r['orbit'] + tol and r['scip'] <= r['pr'] + tol
          and r['pr'] <= r['orbit'] + tol and r['orbit'] <= 1 + 1e-9)
    viol += (not ok)
    print('4: trial %d ratios %s %s' % (trial, {k: round(v, 5) for k, v in r.items()}, 'ok' if ok else 'NESTING VIOLATED'))
print('4: nesting violations:', viol)
