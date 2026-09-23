from fractions import Fraction as F
from itertools import combinations, product
from functools import reduce
from math import gcd
import random,json
rng=random.Random(4505)
C=((1,0,0),(0,1,0),(0,0,1),(1,1,0),(-1,0,1),(0,-1,-1))
def neg(a):return tuple(-x for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def primitive(a):
 g=reduce(gcd,a)
 if not g:return None
 a=tuple(x//g for x in a)
 return a if next(x for x in a if x)>0 else neg(a)
def inverse(B):
 a,b,c=B
 det=dot(a,cross(b,c))
 if not det:return None
 cols=[cross(b,c),cross(c,a),cross(a,b)]
 return tuple(tuple(F(cols[j][i],det) for j in range(3)) for i in range(3))
def mv(A,b):return tuple(dot(a,b) for a in A)
def bases(rows):
 out=[]
 for ids in combinations(range(len(rows)),3):
  inv=inverse([rows[i] for i in ids])
  if inv is not None:out.append((ids,inv))
 return out
M=sorted(set(C)|{neg(c) for c in C})
D=sorted({p for a,b in combinations(M,2) if (p:=primitive(cross(a,b)))})
Rp={p for a,b in combinations(D,2) if (p:=primitive(cross(a,b)))}
R=sorted(Rp|{neg(p) for p in Rp})
N=sorted(set(M)|{neg(h) for h in R})
MB=bases(M); NB=bases(N)
assert len(D)==7 and len(R)==18
for d in D:assert all(abs(x)<=1 for x in d) and all(abs(dot(a,d))<=1 for a in M)
for h in R:
 assert max(map(abs,h))<=2
 for ids,inv in MB:
  q=tuple(sum(inv[j][i]*h[j] for j in range(3)) for i in range(3))
  if min(q)>=0:assert all(x.denominator==1 and x<=2 for x in q)
def verts(gamma):
 out=set()
 for ids,inv in MB:
  p=mv(inv,[gamma[i] for i in ids])
  if all(dot(a,p)<=b for a,b in zip(M,gamma)):out.add(p)
 assert out
 return sorted(out)
recovered_states=0
for case in range(36):
 d=1+case%6
 fam=[];agg=[F(0)]*3
 for j in range(d):
  center=tuple(F(rng.randint(-4,4),24) for i in range(3))
  radii=[F(rng.randint(1,4),24) for a in M]
  if (case+j)%4==0:
   radii=[F(0) if a in [(-1,0,0),(1,0,0)] else rad for a,rad in zip(M,radii)]
  if (case+j)%9==0:radii=[F(0)]*len(M)
  gamma=[dot(a,center)+rad for a,rad in zip(M,radii)]
  v=verts(gamma)
  support={h:max(dot(h,p) for p in v) for h in R}
  p,q=rng.choice(v),rng.choice(v)
  agg=[agg[i]+(p[i]+q[i])/2 for i in range(3)]
  fam.append((gamma,support))
 remaining=tuple(agg)
 for j,(gamma,support) in enumerate(fam):
  suffix={h:sum(s[h] for g,s in fam[j+1:]) for h in R}
  rhs=[]
  for n in N:
   opts=[]
   if n in M:opts.append(gamma[M.index(n)])
   if neg(n) in R:opts.append(suffix[neg(n)]+dot(n,remaining))
   rhs.append(min(opts))
  for ids,inv in NB:
   p=mv(inv,[rhs[i] for i in ids])
   if all(dot(n,p)<=b for n,b in zip(N,rhs)):break
  else:raise AssertionError('no recovery vertex')
  assert all(dot(a,p)<=b for a,b in zip(M,gamma))
  remaining=tuple(remaining[i]-p[i] for i in range(3))
  assert all(dot(h,remaining)<=suffix[h] for h in R)
  recovered_states+=1
 assert remaining==(0,0,0)
# Check new five-product section directly in original arc-flow coordinates.
edges=[(1,2),(1,3),(2,3),(0,1),(0,2),(0,3)]
v=(F(1,2),F(1,2),F(1,2),F(1,4),F(1,2),F(1,2))
b=(F(-5,4),F(-3,4),F(1,2),F(3,2))
bar=(F(1,6),F(1,24),F(1,8))
x=tuple(v[i]+dot(C[i],bar) for i in range(6))
def incidence(f):return tuple(sum(f[e] for e,(u,w) in enumerate(edges) if w==i)-sum(f[e] for e,(u,w) in enumerate(edges) if u==i) for i in range(4))
assert incidence(v)==b
feasible=infeasible=0
for a,c in product(range(-9,10),repeat=2):
 p,q=F(a,960),F(c,960);w=2*p+q
 if w<0:
  # Residual h support <=1/3, second-state h value zero, aggregate h=1/3.
  assert dot((1,1,1),bar)-w>F(1,3)
  infeasible+=1
  continue
 theta=[(F(1,6)-p-q/2,F(1,24)-q/2,F(1,8)-p),(p,q,p),(q/2,-q/2,F(0))]
 flows=[tuple(v[i]/3+dot(C[i],t) for i in range(6)) for t in theta]
 assert all(0<=z<=F(1,3) for f in flows for z in f)
 assert all(incidence(f)==tuple(z/3 for z in b) for f in flows)
 assert tuple(sum(f[i] for f in flows) for i in range(6))==x
 assert flows[1][0]==F(1,6)+p and flows[1][1]==F(1,6)+q
 assert flows[1][4]==F(1,6) and flows[2][2]==F(1,6) and flows[2][3]==F(1,12)
 feasible+=1
print(json.dumps({'K4_directions':len(D),'K4_support_rays':len(R),'normal_bases':len(MB),'recovery_normal_bases':len(NB),'recovery_families':36,'recovered_states':recovered_states,'five_product_grid_exact_witnesses':feasible,'five_product_grid_exact_support_obstructions':infeasible,'status':'PASS'},indent=2))
