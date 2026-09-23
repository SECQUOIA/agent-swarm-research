from itertools import combinations, product
from fractions import Fraction as F
from pathlib import Path
import json
import sympy as s

# Independent exact DP implementation. It caches selected histories, not paths.
def solve(n,L,g,k,mandatory,forbidden,score):
    g=min(g,n+1)
    dp={((),0,0):(s.Rational(0),())}
    for t in range(n):
        nxt={}
        for (hist,c,q),(value,path) in dp.items():
            for b in (0,1):
                if b and (c or t in forbidden or q==k): continue
                if not b and t in mandatory: continue
                nh=tuple(j for j in hist+(t,)*b if j>=t+1-L)
                key=(nh,g-1 if b else max(c-1,0),q+b)
                cand=(value+(score(t,hist) if b else 0),path+(t,)*b)
                if key not in nxt or cand[0]>nxt[key][0]: nxt[key]=cand
        dp=nxt
    out=[v for key,v in dp.items() if key[2]==k]
    return max(out,default=None,key=lambda v:v[0])

n=6
# All constraints, all gaps including an enormous binary-encoded gap, L=0 and g>L.
feas_cases=0
for L in (0,1,2):
 for g in (1,2,3,7,10**30):
  for tags in product((0,1,2),repeat=n):
   mandatory={i for i,x in enumerate(tags) if x==1}
   forbidden={i for i,x in enumerate(tags) if x==2}
   for k in range(n+1):
    expected=[S for S in combinations(range(n),k) if mandatory<=set(S) and not forbidden.intersection(S) and all(b-a>=g for a,b in zip(S,S[1:]))]
    score=lambda t,h:s.Integer(100*(t+1)+sum((t-j)**2 for j in h))
    result=solve(n,L,g,k,mandatory,forbidden,score)
    if expected:
     exact=max(sum(score(t,tuple(j for j in S if t-L<=j<t)) for t in S) for S in expected)
     assert result is not None and result[0]==exact
    else: assert result is None
    feas_cases+=1

# Dense exact covariance and Fisher construction, independent of production code.
n=6;rho=s.Rational(1,10);L=2;eps=s.Rational(1,200)
W=s.Matrix([[2,1,0],[1,2,0],[0,0,1]])
J0=s.diag(1,0,0)
fixtures={}
for name,d in [('scalar',1),('block',2),('partial',1)]:
 latent=2 if name!='scalar' else 1
 rotation=s.Matrix([[0,-1],[1,0]]) if latent==2 else s.eye(1)
 A=rho*rotation
 H=[(s.eye(2) if name=='block' else s.Matrix([[1,0]]) if i%2==0 else s.Matrix([[0,1]])) if latent==2 else s.eye(1) for i in range(n)]
 R=s.zeros(n*d)
 for i in range(n):
  for j in range(i+1):
   val=H[i]*(A**(i-j))*H[j].T
   if i==j: val+=s.eye(d)
   R[i*d:(i+1)*d,j*d:(j+1)*d]=val
   R[j*d:(j+1)*d,i*d:(i+1)*d]=val.T
 Fm=s.Matrix(n*d,3,lambda i,j:s.Rational(((i+1)*(j+2))%7-3,1+j))
 scores={};true={};local={}
 for mask in range(1<<n):
  S=tuple(i for i in range(n) if mask>>i&1)
  idx=[i*d+a for i in S for a in range(d)]
  Fs=Fm.extract(idx,range(3));Rs=R.extract(idx,idx)
  true[S]=s.trace(W*(J0+Fs.T*Rs.inv()*Fs)) if S else s.trace(W*J0)
  total=s.trace(W*J0)
  for t in S:
   hist=tuple(j for j in S if t-L<=j<t)
   key=(t,hist)
   if key not in scores:
    ii=list(range(t*d,(t+1)*d));hh=[j*d+a for j in hist for a in range(d)]
    b=R.extract(ii,hh)*R.extract(hh,hh).inv() if hh else s.zeros(d,0)
    D=R.extract(ii,ii)-b*R.extract(hh,ii)
    G=Fm.extract(ii,range(3))-b*Fm.extract(hh,range(3))
    scores[key]=s.trace(W*G.T*D.inv()*G)
   total+=scores[key]
  local[S]=total
 cases=0;worst=s.Integer(1)
 for g in (1,2,3,7,10**30):
  for k in range(n+1):
   for mandatory,forbidden in [(set(),set()),({1},{4}),({1,2},set()),({0},{0})]:
    choices=[S for S in true if len(S)==k and mandatory<=set(S) and not forbidden.intersection(S) and all(b-a>=g for a,b in zip(S,S[1:]))]
    result=solve(n,L,g,k,mandatory,forbidden,lambda t,h:scores[t,h])
    if not choices: assert result is None;continue
    assert result[0]+s.trace(W*J0)==max(local[S] for S in choices)
    optimum=max(true[S] for S in choices)
    ratio=true[result[1]]/optimum
    assert ratio>=1-eps
    worst=min(worst,ratio);cases+=1
 fixtures[name]={'cases':cases,'minimum_true_ratio':str(worst),'subsets':len(true)}

# Independent hard graph: triangular prism, all subsets, exact inverse.
A=s.zeros(6)
for i,j in [(0,1),(1,2),(2,0),(3,4),(4,5),(5,3),(0,3),(1,4),(2,5)]: A[i,j]=A[j,i]=1
R=s.eye(6)+A/12
for mask in range(1,64):
 S=[i for i in range(6) if mask>>i&1];k=len(S)
 val=(s.ones(1,k)*R.extract(S,S).inv()*s.ones(k,1))[0]
 independent=all(A[i,j]==0 for i,j in combinations(S,2))
 assert val==k if independent else val<=k-s.Rational(1,9)

out={'status':'pass','exhaustive_constraint_dp_cases':feas_cases,'exact_covariance_fixtures':fixtures,'triangular_prism_nonempty_subsets':63}
Path(__file__).with_name('results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
