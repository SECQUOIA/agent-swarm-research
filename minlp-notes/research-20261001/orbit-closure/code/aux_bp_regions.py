from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[3])

import numpy as np, sys, math
sys.path.insert(0,(_PUBLIC_REPO + '/research-20261001/orbit-closure/code'))
from orbit_lib import Corner
cn=Corner(np.array([1.,-1,1]), np.array([[1,0,0],[0,-1,0],[0,0,1],[0,0,-1.]]).T)
def analytic(a,b,c):
    det=a*c-b*b; one=a+2*b+c; onep=a-2*b+c
    # ray 1
    if a+b<=0: a1=0.0; adm1=None
    else:
        s=(a*(b+c)+math.sqrt(a*det*one))/(a*(a+b))
        if s>=0: a1=(math.sqrt(a*one/det)-1)/4; adm1=True
        else: a1=max(0,-(b+c)/(2*c)); adm1=False
    if c-b<=0: a2=0.0; adm2=None
    else:
        t=(c*(a-b)+math.sqrt(c*det*onep))/(c*(c-b))
        kept=(a+b)+(b+c)*t>=0
        if kept: a2=(math.sqrt(c*onep/det)-1)/4; adm2=True
        else: a2=max(0,-(b+c)/one); adm2=False
    return a1,a2,adm1,adm2
rng=np.random.default_rng(1)
worst={}
maxerr=0
for k in range(200000):
    r=math.sqrt(rng.random()); th=rng.random()*2*math.pi
    u=(r*math.cos(th),r*math.sin(th))
    a,b,c=0.5+u[0]/2,u[1]/2,0.5-u[0]/2
    a1,a2,ad1,ad2=analytic(a,b,c)
    if k<3000:
        cut=cn.cut_B_fast(np.array([[a,b],[b,c]]),0.0)
        maxerr=max(maxerr,abs(cut[0]-a1)/(1+a1),abs(cut[1]-a2)/(1+a2))
    key=(ad1,ad2)
    s=a1+a2
    if key not in worst or s<worst[key][0]: worst[key]=(s,(a,b,c))
print('max rel err analytic vs cut_B_fast (3000 samples):',maxerr)
for k,v in worst.items(): print(k, 'min a1+a2 = %.5f at S='%v[0], np.round(v[1],4))
