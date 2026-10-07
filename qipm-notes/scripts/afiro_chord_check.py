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
rng = np.random.default_rng(1)

c, b, A, off = load_standard_form(Path((str(_QIPM_ROOT) + '/cache_dir/netlib/afiro/afiro.std')))
A = A.toarray(); m, n = A.shape
print(f"afiro standard form: m={m} n={n}")
# row rank
r = np.linalg.matrix_rank(A)
if r < m:
    # keep independent rows
    q, rr, piv = np.linalg.qr(A.T, mode='reduced'), None, None
    U, S, VT = np.linalg.svd(A)
    keep = []
    import scipy.linalg as sla
    Q, R, P = sla.qr(A.T, pivoting=True)
    keep = sorted(P[:r])
    A = A[keep]; b = b[keep]; m = r
    print(f"reduced to independent rows: m={m}")
# strictly feasible start: max t s.t. Ax=b, x_i >= t, t <= 1  -> vars (x,t)
res = linprog(np.r_[np.zeros(n), -1.0], A_eq=np.c_[A, np.zeros(m)], b_eq=b,
              A_ub=np.c_[-np.eye(n), np.ones(n)], b_ub=np.zeros(n),
              bounds=[(None,None)]*n + [(None, 1.0)], method='highs')
x0, t0 = res.x[:n], res.x[n]
print(f"phase-I: min slack t = {t0:.3e}")
assert t0 > 0
# optimal value
res2 = linprog(c, A_eq=A, b_eq=b, bounds=[(0,None)]*n, method='highs')
OPT = res2.fun
print(f"OPT = {OPT:.6f}")
_,_,Vt = np.linalg.svd(A); Z = Vt[m:].T
Pc = Z@(Z.T@c); npc = np.linalg.norm(Pc)
print(f"||Pi_V c|| = {npc:.4f}, nu = n = {n}")

def central(mu, x):
    for _ in range(500):
        g = Z.T@(c - mu/x); H = Z.T@np.diag(mu/x**2)@Z
        d = np.linalg.solve(H,-g)
        lam = np.sqrt(max(d@H@d,0)); step = 1.0 if lam<0.25 else 1/(1+lam)
        while np.any(x+step*(Z@d)<=0): step*=0.5
        x = x+step*(Z@d)
        if lam<1e-10: break
    return x

def ell_est(x, gap, ndir=40):
    # max ||y-x|| over {y: Ay=b, y>=0, c^Ty <= c^Tx}, lower-estimated by direction LPs
    best = 0.0
    cths = c@x
    for _ in range(ndir):
        u = rng.standard_normal(n)
        r = linprog(-u, A_eq=A, b_eq=b, A_ub=c.reshape(1,-1), b_ub=[cths],
                    bounds=[(0,None)]*n, method='highs')
        if r.status == 0:
            best = max(best, np.linalg.norm(r.x - x))
    return best

nu = n
ub = (nu + 2*np.sqrt(nu))**2
x = x0.copy()
print(f"{'mu':>8} {'gap':>10} {'kappa':>10} {'lmin*l^2':>9} {'lmax*g2/c2':>11} {'CGits':>6}")
for mu in [1e0, 1e-1, 1e-2, 1e-3, 1e-4, 1e-5]:
    x = central(mu, x)
    H = Z.T@np.diag(1/x**2)@Z
    w = np.linalg.eigvalsh(H)
    gap = c@x - OPT
    l = ell_est(x, gap)
    # CG iterations
    bb = rng.standard_normal(n-m); bb/=np.linalg.norm(bb)
    xk = np.zeros(n-m); rr = bb.copy(); p = rr.copy(); rs = rr@rr; it=0
    while np.sqrt(rs) > 1e-8 and it < 3000:
        Hp = H@p; al = rs/(p@Hp); xk+=al*p; rr-=al*Hp
        rsn = rr@rr; p = rr + (rsn/rs)*p; rs = rsn; it+=1
    print(f"{mu:>8.0e} {gap:>10.3e} {w[-1]/w[0]:>10.3e} {w[0]*l*l:>9.2f} {w[-1]*gap*gap/npc**2:>11.3f} {it:>6}")
print(f"(theory: lmin*l^2 in [1, {ub:.0f}]; lmax*g^2/||Pc||^2 >= 1)")
