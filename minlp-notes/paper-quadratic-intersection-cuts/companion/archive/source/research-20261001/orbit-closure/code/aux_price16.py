from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[7])

import numpy as np, sys, warnings
warnings.filterwarnings('ignore')
sys.path.insert(0,(_PUBLIC_REPO + '/research-20261001/orbit-closure/code'))
from orbit_lib import Corner
from closure import price
sb=np.array([-2.,3,2]); P=np.column_stack([np.array(v)-sb for v in ([0,0,0],[6,-2,0.25],[1,-2.5,0.5])])
cn=Corner(sb,P)
lo=np.array([0.955573, 0.010253, 0.029536])
for lam in [(24/25,1/100,29/1000), tuple(lo*1.004), tuple(lo*1.0035)]:
    for fam in ('B','A'):
        v,th,a=price(cn,np.array(lam),fam=fam,nsample=20000,nstart=30,rng=np.random.default_rng(3))
        print(fam, np.round(lam,6), 'sum %.6f'%sum(lam),'min pricing %.6f'%v)
