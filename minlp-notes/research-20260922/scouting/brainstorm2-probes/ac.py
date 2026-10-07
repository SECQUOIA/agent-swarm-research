from pathlib import Path as _CleanupPath
_NOTES_ROOT = _CleanupPath(__file__).resolve().parent.joinpath('../../..').resolve()

import sys, numpy as np, csv
sys.path.insert(0,(str(_NOTES_ROOT) + '/research-20260922/scouting/minlplib-open-data'))
from osil import read
D=(str(_CleanupPath.home()) + '/.cache/minlplib/minlplib/osil/')
def ev(t,x):
    op=t[0]
    if op=='num': return t[1]
    if op=='var': return x[t[1]]
    a=[ev(c,x) for c in t[1:]]
    if op=='sum': return sum(a)
    if op=='times':
        p=1.0
        for v in a: p*=v
        return p
    if op=='negate': return -a[0]
    raise NotImplementedError(op)
rows={x['name']:x for x in csv.DictReader(open((str(_NOTES_ROOT) + '/research-20260922/scouting/minlplib-open-data/open.csv')))}
rng=np.random.default_rng(0)
for name in sorted(n for n in rows if n.startswith('autocorr')):
    I=read(D+name+'.osil'); N=len(I['vt'])-1
    R=I['rows'][0]
    parts=name.split('bern')[1].replace('fix','').split('-'); n_,M=int(parts[0]),int(parts[1])
    def P(b):  # objvar >= P(b) since row: P - objvar <= 0
        x=list(b)+[0.0]; return ev(R['nl'],x)+sum(c*x[j] for j,c in R['lin'].items() if j<N)
    def E(b,M):
        s=2*np.array(b)-1; return sum(float(np.dot(s[:N-k],s[k:]))**2 for k in range(1,M))
    X=[rng.integers(0,2,N) for _ in range(12)]
    p=np.array([P(b) for b in X])
    best=None
    for MM in range(2,N+2):
        e=np.array([E(b,MM) for b in X])
        A=np.vstack([p,np.ones_like(p)]).T; sol,res,*_=np.linalg.lstsq(A,e,rcond=None)
        if np.max(np.abs(A@sol-e))<1e-6: best=(MM,sol); break
    print(name,N,M,best, rows[name]['primalbound'],rows[name]['dualbound'],'lin',len(R['lin']),'fixvars',sum(1 for j in range(N) if I['lb'][j]==I['ub'][j]))
