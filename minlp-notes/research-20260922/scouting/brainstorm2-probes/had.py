import sys, numpy as np
exec(open('/tmp/bs2/ac.py').read().split('rows=')[0])
for n in (6,7):
    I=read(D+f'hadamard_{n}.osil'); R=I['rows'][0]
    rng=np.random.default_rng(0)
    for _ in range(5):
        b=rng.integers(0,2,n*n); x=list(b.astype(float))+[0.0]
        print(n, ev(R['nl'],x), round(np.linalg.det(b.reshape(n,n)),6), round(np.linalg.det(b.reshape(n,n).T),6), R['lin'], R['lb'],R['ub'])
rng=np.random.default_rng(5)
for n in (6,7):
    I=read(D+f'hadamard_{n}.osil'); R=I['rows'][0]; bad=0
    for _ in range(200):
        b=(rng.random(n*n)<0.6).astype(int); x=list(b.astype(float))+[0.0]
        if abs(ev(R['nl'],x)-np.linalg.det(b.reshape(n,n)))>1e-6: bad+=1
    print(n,'mismatches',bad)
