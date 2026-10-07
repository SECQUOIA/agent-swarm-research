from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[3])

import numpy as np, sys, warnings
warnings.filterwarnings('ignore')
sys.path.insert(0,(_PUBLIC_REPO + '/research-20261001/orbit-closure/code'))
from orbit_lib import Corner, corner_bound
from closure import price
sb=np.array([-4.5,0,1.5]); P=np.column_stack([np.array(v)-sb for v in ([-1,-6,18],[-5,6,-18],[0,2.5,2.5])])
cn=Corner(sb,P)
for w in [(1e-6,1,1),(1,1e-6,1),(1e-3,1,1),(1,1e-3,1),(1,1,1e-6)]:
    zK,lamK=corner_bound(sb,P,np.array(w)); print('zK',w,zK,np.round(lamK,4))
for j in range(3):
    for fam in ('A','B','BP'):
        e=np.zeros(3); e[j]=1
        v,th,a=price(cn,e,fam=fam,nsample=20000,nstart=20,rng=np.random.default_rng(5))
        print('inf a_%d over %s ~ %.6g'%(j+1,fam,v), np.round(a,4) if a is not None else None)
