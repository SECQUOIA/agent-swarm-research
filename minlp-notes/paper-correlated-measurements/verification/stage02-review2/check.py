"""Independent review checks: actual regressions, unequal blocks, and reductions."""
from itertools import combinations
from fractions import Fraction as F
import json
from pathlib import Path
import numpy as np
from scipy.linalg import block_diag

rng = np.random.default_rng(230213)
def root(a, inverse=False):
    v,u=np.linalg.eigh(a)
    return (u*(v**(-.5 if inverse else .5)))@u.T

def local(R, dims, S, L):
    starts=np.cumsum([0]+dims)
    ix={t:np.arange(starts[t],starts[t+1]) for t in range(len(dims))}
    selected=np.concatenate([ix[t] for t in S])
    rss=R[np.ix_(selected,selected)]
    offsets=np.cumsum([0]+[dims[t] for t in S])
    loc={t:np.arange(offsets[a],offsets[a+1]) for a,t in enumerate(S)}
    A=np.eye(len(selected)); ds=[]; reg={}
    for t in S:
        H=[j for j in S if t-L<=j<t]
        hi=np.concatenate([ix[j] for j in H]) if H else np.array([],dtype=int)
        b=np.linalg.solve(R[np.ix_(hi,hi)],R[np.ix_(ix[t],hi)].T).T if H else np.zeros((dims[t],0))
        D=R[np.ix_(ix[t],ix[t])]-b@R[np.ix_(hi,ix[t])]
        if H: A[np.ix_(loc[t],np.concatenate([loc[j] for j in H]))]=-b
        ds.append(D); reg[t]=(H,b,D)
    Di=block_diag(*[root(d,True) for d in ds])
    C=Di@A@rss@A.T@Di
    Q=A.T@Di@Di@A
    return C,Q,rss,reg,ix

m,C,rho=F(1),F(1,8),F(2,5)
theta=(4*C*rho+m*rho*(1-rho))/(4*C*rho+m*(1-rho))
B=2*C/m*rho/(theta-rho)
K=C*(1+B*rho/(theta-rho))
assert 2*C*(rho/(theta-rho)-rho/(1-rho))==m/2
for L in range(8):
    near=sum(rho**(h+2*d) for h in range(1,L+1) for d in range(L+1-h,L+1))
    formula=rho**(L+2)*(1-rho**L)*(1-rho**(L+1))/((1-rho)*(1-rho**2))
    assert near==formula
    tail=rho**(L+1)/(1-rho)
    assert tail*sum(rho**(2*d) for d in range(1,L+1))+near==tail*rho*(1-rho**L)/(1-rho)

dims=[1,3,2,1,2,3,1]
n=len(dims); cuts=np.cumsum([0]+dims); R=np.zeros((cuts[-1],cuts[-1]))
for t in range(n):
    for s in range(t):
        raw=rng.normal(size=(dims[t],dims[s]))
        raw*=float(C*rho**(t-s))/np.linalg.norm(raw,2)
        R[cuts[t]:cuts[t+1],cuts[s]:cuts[s+1]]=raw
        R[cuts[s]:cuts[s+1],cuts[t]:cuts[t+1]]=raw.T
b0=float(2*C*rho/(1-rho))
for t in range(n):
    O,_=np.linalg.qr(rng.normal(size=(dims[t],dims[t])))
    diag=(O*(1+b0+np.geomspace(.1,10**(t/2),dims[t])))@O.T
    R[cuts[t]:cuts[t+1],cuts[t]:cuts[t+1]]=diag
assert np.linalg.eigvalsh(R)[0]>=float(m)
cases=0; worst_ratio=0.; max_transfer_discrepancy=0.; max_metric_discrepancy=0.; max_dummy_discrepancy=0.
V=[]
for d in dims:
    O,_=np.linalg.qr(rng.normal(size=(d,d)))
    V.append((O*np.geomspace(.01,100,d))@O.T)
sqrtV=block_diag(*[root(v) for v in V]); Rmetric=sqrtV@R@sqrtV
for size in range(1,n+1):
  for SS in combinations(range(n),size):
    S=list(SS)
    for L in range(n):
      c,q,rss,reg,ix=local(R,dims,S,L)
      err=np.linalg.norm(c-np.eye(len(c)),2)
      delta=float(2*K/m*theta**(L+1)/(1-theta)*(1+B*theta*(1-theta**L)/(1-theta)))
      assert err<=delta+1e-10
      worst_ratio=max(worst_ratio,err/delta)
      eig2=np.linalg.eigvalsh(root(rss)@q@root(rss))
      max_transfer_discrepancy=max(max_transfer_discrepancy,float(np.max(abs(eig2-np.linalg.eigvalsh(c)))))
      for t,(H,b,D) in reg.items():
        assert np.linalg.eigvalsh(D)[0]>=float(m)-1e-10
        at=0
        for j in H:
          assert np.linalg.norm(b[:,at:at+dims[j]],2)<=float(B*theta**(t-j))+1e-10
          at+=dims[j]
      cm,*_=local(Rmetric,dims,S,L)
      max_metric_discrepancy=max(max_metric_discrepancy,abs(err-np.linalg.norm(cm-np.eye(len(cm)),2)))
      padded=np.zeros_like(R)
      selected=np.concatenate([ix[t] for t in S])
      padded[np.ix_(selected,selected)]=R[np.ix_(selected,selected)]
      for t in set(range(n))-set(S): padded[np.ix_(ix[t],ix[t])]=float(m)*np.eye(dims[t])
      cp,*_=local(padded,dims,list(range(n)),L)
      max_dummy_discrepancy=max(max_dummy_discrepancy,abs(err-np.linalg.norm(cp-np.eye(len(cp)),2)))
      cases+=1
D=block_diag(*[R[cuts[t]:cuts[t+1],cuts[t]:cuts[t+1]] for t in range(n)])
normed=root(D,True)@R@root(D,True)
ev=np.linalg.eigvalsh(normed)
assert ev[0]>=1/(1+b0)-1e-10 and ev[-1]<=1+b0+1e-10
assert max_transfer_discrepancy<1e-9
assert max_metric_discrepancy<1e-7
assert max_dummy_discrepancy<1e-9
out=dict(cases=cases,packet_dimensions=dims,worst_actual_bound_ratio=worst_ratio,
         transfer_eigenvalue_error=max_transfer_discrepancy,
         metric_norm_error=max_metric_discrepancy,dummy_norm_error=max_dummy_discrepancy,
         normalized_spectrum=ev[[0,-1]].tolist())
Path(__file__).with_name('results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
