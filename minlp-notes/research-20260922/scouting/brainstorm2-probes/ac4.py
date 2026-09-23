import sys, numpy as np
exec(open('/tmp/bs2/ac.py').read().split('rows=')[0])
name=sys.argv[1]
I=read(D+name+'.osil'); N=len(I['vt'])-1; R=I['rows'][0]
rng=np.random.default_rng(1)
X=[rng.integers(0,2,N) for _ in range(300)]
p=np.array([ev(R['nl'],list(b)+[0.0]) for b in X])
for label,fn in [('cyc',lambda s,k: float(np.dot(s,np.roll(s,-k)))**2)]:
    F=np.array([[fn(2*b-1,k) for k in range(1,N)]+[1.0] for b in X])
    w,*_=np.linalg.lstsq(F,p,rcond=None); print(label,np.max(np.abs(F@w-p))); print(np.round(w,3))
