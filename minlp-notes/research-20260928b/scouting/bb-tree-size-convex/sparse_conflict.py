"""Midpoint-conflict clique for the perspective relaxation of cardinality-
constrained ridge regression.  Supports S,T conflict iff
    g((1_S+1_T)/2) < OPT - eps,
where g(z) = min_beta ||y-X beta||^2 + lam sum beta_i^2/z_i (perspective).
Any convex-piece B&B tree using the perspective relaxation needs at least
(clique size) leaves."""
import os, sys, json, itertools, time
os.environ["OMP_NUM_THREADS"]="1"; os.environ["OPENBLAS_NUM_THREADS"]="1"
import numpy as np
from multiprocessing import Pool
from sparse_bb import instance, exact_value, bnb, forward_greedy

def all_supports(X,y,lam,k):
    p=X.shape[1]
    G=X.T@X; b=X.T@y; yy=y@y
    sups=np.array(list(itertools.combinations(range(p),k)))
    Gs=G[sups[:,:,None],sups[:,None,:]]+lam*np.eye(k)
    bs=b[sups]
    sol=np.linalg.solve(Gs,bs[...,None])[...,0]
    vals=yy-(bs*sol).sum(1)
    return sups,vals

def g_mid(X,y,lam,S,T):
    U=sorted(set(S)|set(T)); w=np.array([1.0 if (i in S and i in T) else 0.5 for i in U])
    XU=X[:,U]; b=XU.T@y
    M=XU.T@XU+lam*np.diag(1.0/w)
    return y@y-b@np.linalg.solve(M,b)

def conflict_clique(X,y,lam,k,sups,vals,ncand=1500,eps_rel=1e-6):
    OPT=vals.min(); thr=OPT*(1-eps_rel)
    order=np.argsort(vals)[:ncand]
    C=[tuple(sups[i]) for i in order]; f=vals[order]
    m=len(C)
    adj=np.zeros((m,m),bool)
    G=X.T@X; bfull=X.T@y; yy=y@y
    # batch by union size
    pairs=[(i,j) for i in range(m) for j in range(i+1,m)]
    groups={}
    for (i,j) in pairs:
        U=tuple(sorted(set(C[i])|set(C[j])))
        groups.setdefault(len(U),[]).append((i,j,U))
    for d,lst in groups.items():
        Us=np.array([u for (_,_,u) in lst])
        W=np.array([[1.0 if (x in C[i] and x in C[j]) else 0.5 for x in u] for (i,j,u) in lst])
        Ms=G[Us[:,:,None],Us[:,None,:]]+lam*np.einsum('ij,jk->ijk',1.0/W,np.eye(d))
        bs=bfull[Us]
        sol=np.linalg.solve(Ms,bs[...,None])[...,0]
        gv=yy-(bs*sol).sum(1)
        for (i,j,_),v in zip(lst,gv):
            if v<thr: adj[i,j]=adj[j,i]=True
    best=[]
    for start in range(min(60,m)):
        cl=[start]; cand=adj[start].copy()
        for j in range(m):
            if cand[j]:
                cl.append(j); cand&=adj[j]
        if len(cl)>len(best): best=cl
    deg=adj.sum(1)
    return len(best), float(np.mean(deg[:50])) if m>=50 else float(np.mean(deg)), f[best]-OPT

def job(a):
    n,p,k,sigma,seed=a
    X,y,lam,Ss=instance(n,p,k,seed=seed,sigma=sigma)
    t=time.time()
    sups,vals=all_supports(X,y,lam,k)
    OPT=vals.min()
    om,deg,_=conflict_clique(X,y,lam,k,sups,vals)
    r=bnb(X,y,lam,k,S_init=[Ss,forward_greedy(X,y,lam,k)])
    return dict(n=n,p=p,k=k,sigma=sigma,seed=seed,clique=om,deg50=deg,nodes=r['nodes'],
                leaves=(r['nodes']+1)//2, opt=float(OPT), bnb_opt=r['opt'],
                recov=tuple(sorted(sups[np.argmin(vals)].tolist()))==tuple(Ss),
                near={str(e):int((vals<=OPT*(1+e)).sum()) for e in [0.01,0.05,0.1]},
                time=time.time()-t)

if __name__=="__main__":
    p=int(sys.argv[1]);k=int(sys.argv[2]);sigma=float(sys.argv[3]);nseeds=int(sys.argv[4])
    ns=[int(v) for v in sys.argv[5].split(",")]; out=sys.argv[6]
    jobs=[(n,p,k,sigma,s) for n in ns for s in range(nseeds)]
    with Pool(int(sys.argv[7]) if len(sys.argv)>7 else 8) as pool, open(out,"w") as f:
        for r in pool.imap_unordered(job,jobs):
            f.write(json.dumps(r)+"\n"); f.flush()
