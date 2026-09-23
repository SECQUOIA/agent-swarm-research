import numpy as np, sys
sys.path.insert(0, '/home/sgusev/repo/qipm')
from pathlib import Path
from standard_form import load_standard_form
from scipy.optimize import linprog
import scipy.linalg as sla
rng = np.random.default_rng(4)

def theta_fit(name, ndir=30):
    c, b, A, off = load_standard_form(Path(f'/home/sgusev/repo/qipm/cache_dir/netlib/{name}/{name}.std'))
    A = A.toarray(); m, n = A.shape
    r = np.linalg.matrix_rank(A)
    if r < m:
        Q, R, P = sla.qr(A.T, pivoting=True); keep = sorted(P[:r]); A = A[keep]; b = b[keep]; m = r
    res2 = linprog(c, A_eq=A, b_eq=b, bounds=[(0,None)]*n, method='highs')
    OPT = res2.fun; xstar = res2.x
    scale = max(1.0, abs(OPT))
    gs, Ds = [], []
    dirs = [rng.standard_normal(n) for _ in range(ndir)]
    for g in scale*np.array([1e-1,1e-2,1e-3,1e-4,1e-5,1e-6]):
        best = 0.0
        for u in dirs:
            r1 = linprog(-u, A_eq=A, b_eq=b, A_ub=c.reshape(1,-1), b_ub=[OPT+g],
                         bounds=[(0,None)]*n, method='highs')
            r2 = linprog(u, A_eq=A, b_eq=b, A_ub=c.reshape(1,-1), b_ub=[OPT+g],
                         bounds=[(0,None)]*n, method='highs')
            if r1.status==0 and r2.status==0:
                best = max(best, np.linalg.norm(r1.x - r2.x))
        gs.append(g); Ds.append(best)
    gs = np.array(gs); Ds = np.array(Ds)
    print(f"{name}: gaps/diams:")
    for g,D in zip(gs,Ds): print(f"   g={g:.1e} D={D:.4e} D/g^0.5={D/np.sqrt(g):.2e} D/g={D/g:.2e}")
    # local slopes
    sl = np.diff(np.log10(Ds))/np.diff(np.log10(gs))
    print(f"   local theta slopes: {np.round(sl,3)}  -> predicted alpha=2-2theta: {np.round(2-2*sl,3)}")

for name in ["scagr7", "kb2", "afiro", "sc50b"]:
    theta_fit(name)
