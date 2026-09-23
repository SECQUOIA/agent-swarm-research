"""Reviewer 03 independent exact finite checks; no universal claim by testing."""
from fractions import Fraction as Q
from itertools import combinations, product
from math import comb, prod
from functools import lru_cache
from pathlib import Path
import hashlib, json

counts = {}
def ff(x,a):
    return prod((x-j for j in range(a)), start=Q(1))

def psd(a):
    # Exact symmetric Schur elimination; a zero diagonal in a PSD residual
    # must have an all-zero row. No floating-point eigenvalue tolerance.
    a=[row[:] for row in a]
    while a:
        assert all(a[i][i]>=0 for i in range(len(a)))
        pivot=next((i for i in range(len(a)) if a[i][i]>0),None)
        if pivot is None:
            assert all(x==0 for row in a for x in row)
            return
        ids=[i for i in range(len(a)) if i!=pivot]
        p=a[pivot][pivot]
        a=[[a[i][j]-a[i][pivot]*a[pivot][j]/p for j in ids] for i in ids]

# Full quotient localizing matrices for every assignment size (symmetry
# identifies actual coordinate choices), including zero weights and v=s.
cases=[(1,2,Q(1)),(1,3,Q(1)),(1,3,Q(3,2)),(1,3,Q(2)),
       (2,6,Q(3)),(2,7,Q(3)),(2,7,Q(7,2)),(2,7,Q(4))]
matrices=zero=0
for r,s,t in cases:
    for a in range(2*r+1):
      for b in range(2*r+1-a):
        v=a+b; d=(2*r-v)//2
        basis=[set(c) for j in range(d+1) for c in combinations(range(s-v),j)]
        def local(c):
            return ff(t,a+c)*ff(s-t,b)/ff(s,v+c)
        pi=local(0)
        assert pi>=0
        if pi==0: zero+=1; assert d==0
        matrix=[[local(len(I|J)) for J in basis] for I in basis]
        psd(matrix); matrices+=1
        # Every allowed repeated slack product reduces to an assignment
        # with no more factors, and conflicts reduce to zero.
        for repeats in range(2*r-v+1):
            budget=(2*r-v-repeats)//2
            if budget>=0:
                ids=[i for i,I in enumerate(basis) if len(I)<=budget]
                psd([[matrix[i][j] for j in ids] for i in ids])
counts['exact_assignment_psd_matrices']=matrices
counts['zero_indicator_weights']=zero

# All-assigned and sign-boundary identities in larger orders.
negative=0
for r in range(1,8):
 s=4*r-2
 for t in (Q(2*r-1),Q(2*r-1,1)+Q(1,2)):
  if s-t<2*r-1: continue
  for a in range(2*r+1):
   for b in range(2*r+1-a): assert ff(t,a)*ff(s-t,b)/ff(s,a+b)>=0
 for j in range(2*r-1):
  t=Q(2*j+1,2)
  assert ff(t,j+2)/ff(4*r,j+2)<0
  negative+=1
counts['negative_noninteger_boundary_cases']=negative

# Endpoint count including k=0,z=0, impossible avoidance, overlaps A and D.
avoidance=0
for n in range(2,7):
 allmask=(1<<n)-1
 for k in range(n):
  for m in range(1,n-k+1):
   z=n-k-m
   ws=[]
   for H in combinations(range(n),k):
    hm=sum(1<<i for i in H)
    for Z in combinations([i for i in range(n) if i not in H],z):
     ws.append((hm,sum(1<<i for i in Z)))
   denominator=len(ws)
   base=max(Q(n-k,n),Q(n-z,n))
   for states in product(range(4),repeat=n):
    A=sum(1<<i for i,j in enumerate(states) if j&1)
    D=sum(1<<i for i,j in enumerate(states) if j&2)
    frac=Q(sum(not(h&D or zz&A) for h,zz in ws),denominator)
    assert frac*frac<=base**((A|D).bit_count())
    avoidance+=1
counts['exact_endpoint_patterns']=avoidance

@lru_cache(None)
def leaves(a,b): return 1 if a==0 or b==0 else leaves(a-1,b)+leaves(a,b-1)
vertex_cases=0
for n in range(2,8):
 for k in range(n):
  assert leaves(k+1,n-k)==comb(n+1,k+1)
  K=Q(2*k+1,2)
  for delta in (Q(0),Q(1,8),Q(3,8),Q(1,2),Q(3,4)):
   values=[]
   for total in (K-delta,K+delta):
    for fixed in product((Q(0),Q(1)),repeat=n-1):
     last=total-sum(fixed)
     if 0<=last<=1: values.append(last*(1-last))
   if any(K-delta<=s<=K+delta for s in range(n+1)): values.append(Q(0))
   assert min(values)==(Q(1,4)-delta*delta if delta<Q(1,2) else Q(0))
   vertex_cases+=1
counts['exact_slab_vertex_cases']=vertex_cases

# Boolean quotient arithmetic, separately implemented for a discontinuous,
# unbounded but finite-everywhere local auxiliary psi(0)=7, psi(x)=1/x (x>0).
def add(*ps):
 out={}
 for p in ps:
  for m,c in p.items(): out[m]=out.get(m,Q(0))+c
 return {m:c for m,c in out.items() if c}
def mul(p,q):
 out={}
 for i,a in p.items():
  for j,b in q.items(): out[i|j]=out.get(i|j,Q(0))+a*b
 return {m:c for m,c in out.items() if c}
def scale(p,c): return {m:v*c for m,v in p.items() if v*c}
one={0:Q(1)}
# r=2, two fractional blocks with k=m=z=4; one actual witness block.
# One middle coordinate fixed in first block, all endpoints present in second.
xs=[]; ys=[]; zs=[]; masks=[]; params=[]; es=[]; nxt=0; expected=Q(0)
for kind in ('partial','free','evaluation'):
 bx=[]; mask=0; fixedmiddle=4 if kind=='evaluation' else int(kind=='partial')
 for i in range(12):
  w=Q(1) if i<4 else Q(1,8) if i<8 else Q(0)
  fixed=kind=='evaluation' or (kind=='partial' and i==4)
  if fixed:
   x={0:w}; y={0:1/w if w else Q(7)}; z={0:w*(1-w)}
  else:
   x={1<<nxt:Q(1)}; mask|=1<<nxt; nxt+=1
   y=add(scale(one,7),scale(x,-6)); z={}
  bx.append(x); xs.append(x); ys.append(y); zs.append(z)
 es.append(add(*bx,scale(one,-Q(9,2))))
 masks.append(mask); params.append((12-fixedmiddle,Q(9,2)-Q(fixedmiddle,8)))
 expected+=fixedmiddle*Q(7,64)
def E(p):
 return sum(c*prod(ff(t,(m&mask).bit_count())/ff(s,(m&mask).bit_count())
                   for mask,(s,t) in zip(masks,params)) for m,c in p.items())
assert E(one)==1
variables=xs+ys+zs
# Coupled affine square involving every original block, and high-degree
# local identities times global variables within lifted order two.
P=add(one,*[scale(x,Q((j%7)-3)) for j,x in enumerate(variables)])
assert E(mul(P,P))>=0
checks=0
for x,y,z in zip(xs,ys,zs):
 h=mul(x,add(mul(x,y),scale(one,-1))) # x(xy-1)=0 on full graph; degree 3.
 penalty=add(z,scale(x,-1),mul(x,x))
 for v in variables:
  assert E(mul(h,v))==0
  assert E(mul(penalty,v))==0
  checks+=2
 for g in (x,add(one,scale(x,-1)),add(y,scale(one,-1)),mul(x,y)):
  assert E(mul(g,mul(P,P)))>=0 # deg g<=2, deg P=1
  checks+=1
for e in es:
 for v in variables: assert E(mul(e,v))==0; checks+=1
assert E(add(*zs))==expected
# A globally coupled written objective differs from sum z by graph identities.
h=mul(xs[0],add(mul(xs[0],ys[0]),scale(one,-1)))
written=add(*zs,mul(h,xs[-1]))
assert E(written)==expected
counts['exact_unbounded_graph_tensor_checks']=checks

# Frozen identity plus stated zero thresholds and relative constant.
q=lambda k,m,z,r,eps:min(k-2*r+2,z-2*r+2,m*(Q(1,2)-2*eps))
assert q(2,2,2,2,Q(0))==0
assert q(4,4,4,1,Q(1,4))==0
assert q(1,1,1,1,Q(0))==Q(1,2)
tau=Q(1,4)-Q(1,32)*(Q(5,2)+Q(1,4))-Q(1,32)
assert tau==Q(17,128) and 2*tau/6==Q(17,384)
root=Path(__file__).resolve().parents[3]
snapshot=root/'process/snapshots/stage04-round01'
manifest=json.loads((snapshot/'manifest.json').read_text())
for name,digest in manifest.items(): assert hashlib.sha256((snapshot/name).read_bytes()).hexdigest()==digest
counts['frozen_hashes_verified']=len(manifest)
counts['arithmetic']='exact rational arithmetic; no numerical eigenvalues'
Path(__file__).with_suffix('.json').write_text(json.dumps(counts,indent=2)+'\n')
print(json.dumps(counts,indent=2))
