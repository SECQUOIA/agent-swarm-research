from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[3])

import numpy as np, sys, math
sys.path.insert(0,(_PUBLIC_REPO + '/research-20261001/orbit-closure/code'))
from orbit_lib import Corner, M
def first_hit(sb,p):
    # q(sb + t p) = q0 + g1 t + g2 t^2
    q0=sb[2]-sb[0]*sb[1]; g1=p[2]-sb[0]*p[1]-sb[1]*p[0]; g2=-p[0]*p[1]
    ts=np.roots([g2,g1,q0]) if abs(g2)>0 else ([-q0/g1] if g1!=0 else [])
    ts=sorted(t.real for t in np.atleast_1d(ts) if abs(np.imag(t))<1e-12 and t.real>0)
    return ts[0] if ts else np.inf
for name,sb,P in [('thm14',np.array([-4.5,0,1.5]),np.column_stack([np.array(v)-np.array([-4.5,0,1.5]) for v in ([-1,-6,18],[-5,6,-18],[0,2.5,2.5])])),
                  ('wcorner',np.array([1.,-1,1]),np.array([[1,0,0],[0,-1,0],[0,0,1],[0,0,-1.]]).T),
                  ('prop16',np.array([-2.,3,2]),np.column_stack([np.array(v)-np.array([-2.,3,2]) for v in ([0,0,0],[6,-2,0.25],[1,-2.5,0.5])]))]:
    cn=Corner(sb,P)
    t=[first_hit(sb,P[:,j]) for j in range(P.shape[1])]
    xh=np.array([(sb[0]-sb[1])/2,(sb[2]+1)/2]); lamv=xh/np.linalg.norm(xh)
    s,c=lamv; R=np.array([[c,-s],[s,c]])
    X=R@M(sb)
    S=(X+X.T)/2
    print(name,'first hits t_j =',np.round(t,6))
    print('  SCIP: lambda=(sin,cos)=',np.round(lamv,6),' X=R M(sbar)=',np.round(X,6),' symmetric:',np.allclose(X,X.T),' eig',np.round(np.linalg.eigvalsh(S),6))
    aA=cn.cut_A(S/np.trace(S),0.0); aB=cn.cut_B_fast(S/np.trace(S),0.0)
    print('  SCIP set cut (uncompleted)',np.round(aA,6),' completed (Case 4)',np.round(aB,6))
    w=np.ones(P.shape[1])
    with np.errstate(divide='ignore'):
        print('  SCIP bound at w=1: uncompleted %.6f, completed %.6f'%(min(w/np.where(aA>0,aA,1e-300)), min(w/np.where(aB>0,aB,1e-300))))
