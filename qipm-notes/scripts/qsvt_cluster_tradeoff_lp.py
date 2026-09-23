import numpy as np
from scipy.optimize import linprog

def min_M(Lam, rho, d, tol_rel=0.25):
    # p(y) = sum_k c_k T_k(2y/Lam - 1); constraints |p(y)-1/y| <= tol_rel/y on [1,rho];
    # minimize M = max |p| on [0,Lam]
    def cheb_row(y):
        t = 2*y/Lam - 1
        row = np.zeros(d+1); row[0]=1.0
        if d>=1: row[1]=t
        for k in range(2,d+1): row[k] = 2*t*row[k-1] - row[k-2]
        return row
    ycl = np.geomspace(1, rho, 60)
    # dense grid on [0,Lam] incl. gap; use Chebyshev-distributed points for stability
    th = np.linspace(0, np.pi, 900)
    ygl = (1-np.cos(th))/2*Lam
    A_ub, b_ub = [], []
    nvar = d+2  # coeffs + M
    for y in ycl:
        r = cheb_row(y)
        A_ub.append(np.r_[ r, 0]); b_ub.append(1/y + tol_rel/y)
        A_ub.append(np.r_[-r, 0]); b_ub.append(-(1/y - tol_rel/y))
    for y in ygl:
        r = cheb_row(y)
        A_ub.append(np.r_[ r, -1]); b_ub.append(0.0)
        A_ub.append(np.r_[-r, -1]); b_ub.append(0.0)
    cobj = np.zeros(nvar); cobj[-1]=1.0
    res = linprog(cobj, A_ub=np.array(A_ub), b_ub=np.array(b_ub),
                  bounds=[(None,None)]*(d+1)+[(0,None)], method='highs')
    return res.fun if res.status==0 else np.inf

for Lam in [1e4, 1e6]:
    rho = 4.0
    print(f"Lambda={Lam:.0e} (sqrt={np.sqrt(Lam):.0f}), rho={rho}")
    for d in [10, 25, 50, 100, 200, 400]:
        M = min_M(Lam, rho, d)
        print(f"  d={d:>4}  min M = {M:.3e}   (Bernstein floor sqrt(L)/(2 rho d) = {np.sqrt(Lam)/(2*rho*d):.3f})")
