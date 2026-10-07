import sys; import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np, rb, warnings
warnings.filterwarnings('ignore')
def run(D,eta,k1,k2,third='diag'):
    sbar=np.array([0,0,1.0])
    p1=np.array([D,-k1*D,-2*D*np.sqrt(k1)*(1-eta)])
    p2=np.array([D,-k2*D,-2*D*np.sqrt(k2)*(1-eta)])
    p3=np.array([D,D,D*D]) if third=='diag' else np.array([0,0,-1.0])
    P=np.stack([p1,p2,p3],1); c=np.ones(3)
    z,lam=rb.zK(sbar,P,c); Pt=rb.scaled_rays(P,c,z); Di=rb.D_inv(sbar,Pt)
    cA,hA,X=rb.zA_ratio(sbar,Pt,iters=36); rp,_=rb.rho_par(sbar,Pt)
    print('D %g eta %g k1 %g k2 %g third %s: zK %.4g supp %s Dinv %.4g zA %.4g Dinv*zA %.4g Dinv*rho_par %.4g'%(D,eta,k1,k2,third,z,np.flatnonzero(lam>1e-12).tolist(),Di,cA,Di*cA,Di*rp),flush=True)
for eta in [1e-3,1e-4]:
    run(300,eta,1,2)
for k2 in [1.5,3,5,10]:
    run(300,0.01,1,k2)
run(300,0.01,1,2,'down')
