# pattern-theory critique check (2026-10-04). Run from a scratch dir holding copies of the inputs
# (pages.json, fetched.json, candidates.json, census_merged.json from research-20260929; OSIL from ~/.cache/minlplib).
# Extended-valued spot checks for Theorem 5 (affine class) and Prop 4 Remark 2.
import numpy as np
from scipy.optimize import linprog
rng=np.random.default_rng(7)
INF=np.inf
def lp(c,A,b):
    r=linprog(c,A_ub=A,b_ub=b,bounds=[(None,None)]*len(c),method='highs'); assert r.status==0,r.message; return r.fun
worst=0; cnt=0
for trial in range(400):
    m,k=rng.integers(4,9),rng.integers(4,9)
    s=np.sort(rng.uniform(-1,1,m)); t=np.sort(rng.uniform(-1,1,k))
    a=rng.normal(size=m); c=rng.normal(size=k)
    B=rng.normal(size=(m,k))+rng.uniform(-2,2)*np.outer(s,t)
    # constraints: random infeasible entries in head bag (a), middle pairs and tail
    a[rng.random(m)<0.3]=INF; B[rng.random((m,k))<0.4]=INF; c[rng.random(k)<0.3]=INF
    # separator 1 between bag a (value a(s)) and bags B,c : Gamma=a, V(s)=min_j B+c
    V=np.array([np.min(B[i]+c) for i in range(m)]); G=a.copy()
    fstar=np.min(G+V)
    if not np.isfinite(fstar): continue
    L=np.where(np.isfinite(G),fstar-G,-INF); U=V
    # inf Delta over affine phi=lam*s+c0: sup_{L>-inf}(L-phi)+sup_{U<inf}(phi-U)
    A=[];b=[]
    for i in range(m):
        if np.isfinite(L[i]): A.append([-s[i],-1,-1,0]); b.append(-L[i])   # p>=L-phi
        if np.isfinite(U[i]): A.append([s[i],1,0,-1]); b.append(U[i])      # q>=phi-U
    d1=lp([0,0,1,1],A,b)
    # 2 dist: min delta s.t. exists phi affine and psi in band with |phi-psi|<=delta on grid
    # psi free where both edges infinite; constraint only where finite edges: L-delta<=phi, phi<=U+delta
    A=[];b=[]
    for i in range(m):
        if np.isfinite(L[i]): A.append([-s[i],-1,-1]); b.append(-L[i])
        if np.isfinite(U[i]): A.append([s[i],1,-1]); b.append(U[i])
    d2=lp([0,0,1],A,b)
    worst=max(worst,abs(d1-2*d2)); cnt+=1
print('Theorem 5 extended-valued affine class: cases',cnt,'max |infDelta-2dist| =',worst)
# Remark 2 with unreachable cells: 4 layers path, cells per separator, exact b's with +inf entries
import itertools
bad=0;tot=0
for trial in range(300):
    N=4; nc=[1]+[int(rng.integers(2,5)) for _ in range(N-1)]+[1]
    b=[None]+[np.where(rng.random((nc[t-1],nc[t]))<0.35,INF,rng.normal(size=(nc[t-1],nc[t]))) for t in range(1,N+1)]
    # SP
    d=[np.array([0.0])]
    for t in range(1,N+1):
        d.append(np.array([np.min(d[t-1]+b[t][:,j]) for j in range(nc[t])]))
    SP=d[N][0]
    if not np.isfinite(SP): continue
    tot+=1
    # LP: maximize sum_t z_t s.t. z_t <= b_t(D,D') + c_{t,D'} - c_{t-1,D} for finite b; c_0=c_N=0
    idx={}; n=0
    for t in range(1,N):
        for j in range(nc[t]): idx[(t,j)]=n; n+=1
    zi=[n+t for t in range(N)]; nv=n+N
    A=[];bb=[]
    for t in range(1,N+1):
        for i in range(nc[t-1]):
            for j in range(nc[t]):
                if not np.isfinite(b[t][i,j]): continue
                row=[0.0]*nv; row[zi[t-1]]=1
                if t<N: row[idx[(t,j)]]-=1
                if t>1: row[idx[(t-1,i)]]+=1
                A.append(row); bb.append(b[t][i,j])
    c=[0.0]*n+[-1.0]*N
    r=linprog(c,A_ub=A,b_ub=bb,bounds=[(None,None)]*nv,method='highs')
    if r.status!=0 or abs(-r.fun-SP)>1e-9: bad+=1
print('Remark 2 (finite cell constants attain SP), cases',tot,'failures',bad)
