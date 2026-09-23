import numpy as np
from scipy.optimize import linprog

def min_deg(Lam, symmetric):
    # separate p(1/Lam)<=0.1, p(2/Lam)>=0.9 with |p|<=1 on [0,1] (one-sided) or [-1,1] (symmetric)
    def rows(ys, d):
        out=[]
        for y in ys:
            r = np.zeros(d+1); r[0]=1
            if d>=1: r[1]=y
            for k in range(2,d+1): r[k]=2*y*r[k-1]-r[k-2]  # Chebyshev in y directly on [-1,1]
            out.append(r)
        return np.array(out)
    def feas(d):
        th = np.linspace(0,np.pi,1400); grid = np.cos(th)
        if not symmetric: grid = (grid+1)/2*0 + (1-np.cos(th))/2  # [0,1]
        # for [0,1] case need Chebyshev args in [-1,1]: rescale
        if symmetric:
            G = rows(grid, d); pts = rows([1/Lam, 2/Lam], d)
        else:
            G = rows(2*grid-1, d); pts = rows([2/Lam*1-1+2*(1/Lam)*0 for _ in []] , d) if False else rows([2*(1/Lam)-1, 2*(2/Lam)-1], d)
        A_ub = np.vstack([G,-G, pts[0:1], -pts[1:2]])
        b_ub = np.r_[np.ones(2*len(grid)), 0.1, -0.9]
        res = linprog(np.zeros(d+1), A_ub=A_ub, b_ub=b_ub, bounds=[(None,None)]*(d+1), method='highs')
        return res.status==0
    lo, hi = 1, 6000
    while lo<hi:
        mid=(lo+hi)//2
        if feas(mid): hi=mid
        else: lo=mid+1
    return lo

for Lam in [50, 100, 200, 400]:
    d_sym = min_deg(Lam, True)
    d_one = min_deg(Lam, False)
    print(f"Lambda={Lam:>4}: [-1,1]-bounded min degree={d_sym:>5} (d/Lam={d_sym/Lam:.2f})   [0,1]-bounded={d_one:>4} (d/sqrt={d_one/np.sqrt(Lam):.2f})")
