import numpy as np, sys
sys.path.insert(0, '/home/sgusev/repo/qipm')
from pathlib import Path
from standard_form import load_standard_form
from scipy.optimize import linprog
import scipy.linalg as sla
rng = np.random.default_rng(3)
c, b, A, off = load_standard_form(Path('/home/sgusev/repo/qipm/cache_dir/netlib/adlittle/adlittle.std'))
A = A.toarray(); m, n = A.shape
r = np.linalg.matrix_rank(A)
if r < m:
    Q, R, P = sla.qr(A.T, pivoting=True); keep = sorted(P[:r]); A = A[keep]; b = b[keep]; m = r
res = linprog(np.r_[np.zeros(n), -1.0], A_eq=np.c_[A, np.zeros(m)], b_eq=b,
              A_ub=np.c_[-np.eye(n), np.ones(n)], b_ub=np.zeros(n),
              bounds=[(None,None)]*n + [(None, 1.0)], method='highs')
x = res.x[:n]
res2 = linprog(c, A_eq=A, b_eq=b, bounds=[(0,None)]*n, method='highs'); OPT = res2.fun
_,_,Vt = np.linalg.svd(A); Z = Vt[m:].T
scale = max(1.0, abs(c@x-OPT))
for mu in scale*np.array([1e-3, 1e-4, 1e-5]):
    for _ in range(800):
        g = Z.T@(c - mu/x); H = Z.T@np.diag(mu/x**2)@Z
        d = np.linalg.solve(H,-g)
        lam = np.sqrt(max(d@H@d,0)); step = 1.0 if lam<0.25 else 1/(1+lam)
        while np.any(x+step*(Z@d)<=0): step*=0.5
        x = x+step*(Z@d)
        if lam<1e-10: break
    H = Z.T@np.diag(1/x**2)@Z
    w = np.linalg.eigvalsh(H)
    lw = np.log10(w)
    # split clusters by decade gaps
    gaps = np.where(np.diff(lw) > 1.0)[0]
    bounds_idx = [0] + list(gaps+1) + [len(w)]
    desc = []
    for i in range(len(bounds_idx)-1):
        seg = w[bounds_idx[i]:bounds_idx[i+1]]
        desc.append(f"[{seg[0]:.1e},{seg[-1]:.1e}]x{len(seg)} (ratio {seg[-1]/seg[0]:.1e})")
    # CG
    bb = rng.standard_normal(n-m); bb/=np.linalg.norm(bb)
    rr = bb.copy(); p = rr.copy(); rs = rr@rr; it=0
    while np.sqrt(rs) > 1e-8 and it < 4000:
        Hp = H@p; al = rs/(p@Hp); rr-=al*Hp
        rsn = rr@rr; p = rr + (rsn/rs)*p; rs = rsn; it+=1
    print(f"mu={mu:.1e} kappa={w[-1]/w[0]:.2e} CG={it}")
    for d_ in desc: print("   ", d_)
