import numpy as np, sys
sys.path.insert(0, '/home/sgusev/repo/qipm')
from pathlib import Path
from standard_form import load_standard_form
from scipy.optimize import linprog

def run_ipm(A, b, c, x0, Z, OPT, window_only, mu0=1.0, mu_end=1e-8, shrink=0.85, label=""):
    x = x0.copy(); mu = mu0; ncorr = 0
    while mu > mu_end:
        mu *= shrink
        for _ in range(4):
            g = Z.T@(c - mu/x)
            H = Z.T@np.diag(mu/x**2)@Z
            w, U = np.linalg.eigh(H)
            w = np.maximum(w, w[-1]*1e-16)
            if window_only:
                lw = np.log10(w)
                gaps = np.diff(lw)
                imax = int(np.argmax(gaps))
                if gaps[imax] > 2.0:   # genuine cluster gap (>2 decades): drop bottom cluster
                    big = np.zeros_like(w, bool); big[imax+1:] = True
                    d = U[:,big]@((U[:,big].T@(-g))/w[big])
                else:                   # no cluster structure yet: full solve
                    d = U@((U.T@(-g))/w)
            else:
                d = U@((U.T@(-g))/w)
            lam = np.sqrt(max(d@(H@d),0))
            dz = Z@d
            # fraction-to-boundary
            neg = dz < 0
            tmax = np.min(-0.995*x[neg]/dz[neg]) if np.any(neg) else 1.0
            step = min(1.0 if lam < 0.25 else 1/(1+lam), tmax, 1.0)
            x = x + step*dz
            ncorr += 1
            if lam < 1e-3: break
    gap = c@x - OPT
    print(f"{label:>16} window_only={window_only!s:>5}: gap={gap:.3e} rel_gap={gap/max(1,abs(OPT)):.2e} corrections={ncorr}")
    return gap

n = 40
c = np.zeros(n); c[-1]=1.0; c[-2]=0.5
A = np.ones((1,n)); b = np.array([1.0])
_,_,Vt = np.linalg.svd(A); Z = Vt[1:].T
for wo in [False, True]:
    run_ipm(A, b, c, np.ones(n)/n, Z, 0.0, wo, label="degenerate toy")

cc, bb, AA, off = load_standard_form(Path('/home/sgusev/repo/qipm/cache_dir/netlib/afiro/afiro.std'))
AA = AA.toarray(); m, nn = AA.shape
r0 = linprog(np.r_[np.zeros(nn), -1.0], A_eq=np.c_[AA, np.zeros(m)], b_eq=bb,
              A_ub=np.c_[-np.eye(nn), np.ones(nn)], b_ub=np.zeros(nn),
              bounds=[(None,None)]*nn + [(None, 1.0)], method='highs')
r2 = linprog(cc, A_eq=AA, b_eq=bb, bounds=[(0,None)]*nn, method='highs')
_,_,Vt = np.linalg.svd(AA); Zf = Vt[m:].T
sc = max(1.0, abs(cc@r0.x[:nn] - r2.fun))
for wo in [False, True]:
    run_ipm(AA, bb, cc, r0.x[:nn], Zf, r2.fun, wo, mu0=sc, mu_end=sc*1e-10, label="afiro")
