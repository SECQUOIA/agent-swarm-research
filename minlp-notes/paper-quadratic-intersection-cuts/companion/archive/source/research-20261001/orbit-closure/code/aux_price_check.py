from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[7])

import numpy as np, sys, warnings
warnings.filterwarnings('ignore')
sys.path.insert(0,(_PUBLIC_REPO + '/research-20261001/orbit-closure/code'))
from orbit_lib import Corner
from closure import price
sb=np.array([-4.5,0,1.5]); P=np.column_stack([np.array(v)-sb for v in ([-1,-6,18],[-5,6,-18],[0,2.5,2.5])])
cn=Corner(sb,P)
for lam,fam in [((67/250,41/100,151/500),'B'),((27/99,41/99,30/99),'B'),((51/350,0,17/150),'BP')]:
    v,th,a=price(cn,np.array(lam),fam=fam,nsample=20000,nstart=30,rng=np.random.default_rng(3))
    print(fam, lam, 'sum',sum(lam),'min pricing',v)
