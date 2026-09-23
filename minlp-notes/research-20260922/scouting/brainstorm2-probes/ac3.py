import sys, numpy as np
sys.path.insert(0,'/tmp/bs2'); 
exec(open('/tmp/bs2/ac.py').read().split('rows=')[0])
name=sys.argv[1]
I=read(D+name+'.osil'); N=len(I['vt'])-1; R=I['rows'][0]
rng=np.random.default_rng(1)
X=[rng.integers(0,2,N) for _ in range(300)]
p=np.array([ev(R['nl'],list(b)+[0.0]) for b in X])
F=[]
for b in X:
    s=2*b-1
    F.append([float(np.dot(s[:N-k],s[k:]))**2 for k in range(1,N)]+[1.0])
F=np.array(F); w,res,*_=np.linalg.lstsq(F,p,rcond=None)
print(name,'maxres',np.max(np.abs(F@w-p)))
print(np.round(w,4))
