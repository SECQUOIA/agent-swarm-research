from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[3])

import numpy as np, sys, warnings
warnings.filterwarnings('ignore')
sys.path.insert(0,(_PUBLIC_REPO + '/research-20261001/orbit-closure/code'))
from orbit_lib import Corner
from closure import price
sb=np.array([-4.5,0,1.5]); P=np.column_stack([np.array(v)-sb for v in ([-1,-6,18],[-5,6,-18],[0,2.5,2.5])])
cn=Corner(sb,P)
lam=np.array([0.2211,0.8805,0.2464])
for fam in ('B','A'):
    v,th,a=price(cn,lam,fam=fam,nsample=20000,nstart=30,rng=np.random.default_rng(3))
    print(fam,'min pricing',v)
