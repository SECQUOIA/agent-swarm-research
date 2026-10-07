from pathlib import Path as _CleanupPath
import os as _cleanup_os
# Point QIPM_SOURCE_ROOT to the external QIPM checkout containing standard_form.py.
if 'QIPM_SOURCE_ROOT' not in _cleanup_os.environ:
    raise RuntimeError('Set QIPM_SOURCE_ROOT to the QIPM source checkout before running this probe.')
_QIPM_ROOT = _CleanupPath(_cleanup_os.environ['QIPM_SOURCE_ROOT']).expanduser().resolve()

import numpy as np, sys
sys.path.insert(0, (str(_QIPM_ROOT)))
from pathlib import Path
from standard_form import load_standard_form
from scipy.optimize import linprog

def analyze(A, b, c, x0, mus, Z, label):
    x = x0.copy()
    print(label)
    print(f"{'mu':>8} {'kappa':>9} | centering: rhs_big sol_big | affine: rhs_big sol_big resid_drop")
    for mu in mus:
        for _ in range(800):
            g = Z.T@(c - mu/x); H = Z.T@np.diag(mu/x**2)@Z
            d = np.linalg.solve(H,-g)
            lam = np.sqrt(max(d@H@d,0)); step = 1.0 if lam<0.25 else 1/(1+lam)
            while np.any(x+step*(Z@d)<=0): step*=0.5
            x = x+step*(Z@d)
            if lam<1e-11: break
        Hs = Z.T@np.diag(1/x**2)@Z
        w, U = np.linalg.eigh(Hs)
        big = w > np.sqrt(w[0]*w[-1])
        def masses(rhs, Hmu):
            rb = U.T@rhs; sol = U.T@np.linalg.solve(Hmu, rhs)
            mr = np.sum(rb[big]**2)/np.sum(rb**2)
            ms = np.sum(sol[big]**2)/np.sum(sol**2)
            # residual if bottom-cluster solution component dropped:
            sold = sol.copy(); sold[~big]=0.0
            resid = np.linalg.norm(Hmu@(U@sold) - rhs)/np.linalg.norm(rhs)
            return mr, ms, resid
        mu2 = mu/2
        Hmu = Z.T@np.diag(mu2/x**2)@Z
        mrc, msc, rc = masses(-Z.T@(c - mu2/x), Hmu)
        Hmu_a = Z.T@np.diag(mu/x**2)@Z
        mra, msa, ra = masses(-Z.T@c, Hmu_a)   # affine-scaling: target mu=0 direction with current Hessian
        print(f"{mu:>8.0e} {w[-1]/w[0]:>9.1e} | {mrc:>10.4f} {msc:>8.4f} | {mra:>10.4f} {msa:>8.4f} {ra:>10.2e}")
    return x

n = 40
c = np.zeros(n); c[-1]=1.0; c[-2]=0.5
A = np.ones((1,n)); b=np.array([1.0])
_,_,Vt = np.linalg.svd(A); Z = Vt[1:].T
analyze(A, b, c, np.ones(n)/n, [1e-2,1e-4,1e-6], Z, "degenerate family:")

cc, bb, AA, off = load_standard_form(Path((str(_QIPM_ROOT) + '/cache_dir/netlib/afiro/afiro.std')))
AA = AA.toarray(); m, nn = AA.shape
r0 = linprog(np.r_[np.zeros(nn), -1.0], A_eq=np.c_[AA, np.zeros(m)], b_eq=bb,
              A_ub=np.c_[-np.eye(nn), np.ones(nn)], b_ub=np.zeros(nn),
              bounds=[(None,None)]*nn + [(None, 1.0)], method='highs')
_,_,Vt = np.linalg.svd(AA); Zf = Vt[m:].T
analyze(AA, bb, cc, r0.x[:nn], [1e-1,1e-3,1e-5], Zf, "\nafiro:")
