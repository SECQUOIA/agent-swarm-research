import sys; import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np, rb, warnings
warnings.filterwarnings('ignore')
def inst(D, eta, k2, mode):
    sbar=np.array([0,0,1.0])
    p1=np.array([D,-D,-2*D*(1-eta)])
    if mode=='tan2':
        p2=np.array([D,-k2*D,-2*D*np.sqrt(k2)*(1-eta)])
    else:
        p2=np.array([D,-k2*D,0.0])
    p3=np.array([D,D,D*D])      # q along: 1 + D^2 s - D^2 s^2 -> hits at s ~ 1
    return sbar,np.stack([p1,p2,p3],1)
for mode in ['tan1','tan2']:
  for eta in [0.01]:
    for D in [3,10,30,100,300]:
        sbar,P=inst(D,eta,2.0,mode)
        c=np.ones(3)
        z,lam=rb.zK(sbar,P,c)
        Pt=rb.scaled_rays(P,c,z)
        Di=rb.D_inv(sbar,Pt)
        cA,hA,X=rb.zA_ratio(sbar,Pt,iters=36)
        rp,_=rb.rho_par(sbar,Pt)
        print(mode,'eta',eta,'D',D,'zK %.4g supp %s Dinv %.4g zA %.4g/%.4g Dinv*zA %.4g rho_par %.4g Dinv*rho_par %.4g bound %.4g'%(z,np.flatnonzero(lam>1e-12).tolist(),Di,cA,hA,Di*cA,rp,Di*rp,rb.theoremA_bound(Di)),flush=True)
