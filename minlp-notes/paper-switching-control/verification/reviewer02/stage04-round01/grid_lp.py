from fractions import Fraction as F
from itertools import product
from random import Random
from scipy.optimize import linprog
from collections import Counter
rng=Random(47721);stats=Counter()

def certify(c,A,b):
 r=linprog(list(map(float,c)),A_ub=[[float(v) for v in row] for row in A],b_ub=list(map(float,b)),bounds=[(0,None)]*len(c),method='highs')
 if not r.success:return None
 # Rationalize a proposed primal-dual pair; accept only exact identities.
 for maxden in (10**5,10**7,10**9):
  xx=[F(float(v)).limit_denominator(maxden) for v in r.x]
  yy=[F(float(v)).limit_denominator(maxden) for v in r.ineqlin.marginals]
  residual=[F(v)-sum(y*row[j] for y,row in zip(yy,A)) for j,v in enumerate(c)]
  if min(xx)>=0 and max(yy)<=0 and min(residual)>=0 and all(sum(v*x for v,x in zip(row,xx))<=z for row,z in zip(A,b)):
   primal=sum(v*x for v,x in zip(c,xx));dual=sum(y*z for y,z in zip(yy,b))
   if primal==dual:return primal
 raise AssertionError('Exact primal-dual reconstruction failed')

def lp(n,g,a,b,family):
 N=len(g)-1;dim=n*N+1;e=dim-1
 rows=[];rhs=[]
 def ix(i,j):return (j-1)*n+i
 def add(terms,z):
  row=[F(0)]*dim
  for idx,c in terms:row[idx]+=c
  rows.append(row);rhs.append(F(z))
 for j in range(1,N+1):
  add([(ix(i,j),1) for i in range(n)],g[j]);add([(ix(i,j),-1) for i in range(n)],-g[j])
  if j>1:
   for i in range(n):add([(ix(i,j-1),1),(ix(i,j),-1)],0)
 add([(ix(1,N),1),(ix(0,N),-1)],0)
 for i in range(2,n):add([(ix(i,N),1),(ix(1,N),-1)],0)
 add([(e,-1)],-g[-1]/3)
 for i,j in ((0,a),(1,b)):
  add([(e,1),(ix(i,N),1)],g[-1]-g[j-1]);add([(e,-1),(ix(i,N),-1)],g[j]-g[-1])
 add([(e,1),(ix(0,b),1)],g[b])
 for i in range(1,n) if family==0 else [1]:add([(e,1),(ix(i,a),1)],g[a])
 if family==1:add([(e,1),(ix(1,N),-1)],0)
 c=[0]*dim;c[e]=-1
 value=certify(c,rows,rhs)
 if value is not None:stats['exact_feasible_primal_dual']+=1;return -value
 # Certify infeasibility by minimizing one common nonnegative violation.
 phase=certify([0]*dim+[1],[row+[-1] for row in rows],rhs)
 assert phase is not None and phase>0
 stats['exact_infeasibility_certificates']+=1
 return None

def closed(n,g):
 T=g[-1];N=len(g)-1;c=next(j for j in range(1,N+1) if g[j]>=T/3)
 H=min((T+g[c])/4,(T-g[c-1])/2)
 winner=('H',c,H);best=H
 for a in range(1,N+1):
  for b in range(a,N+1):
   A,B,P,Q=g[a],g[b],g[a-1],g[b-1]
   L=max(T/3,F(n-1,n)*T-B,((n-1)*T-A-(n-1)*B)/n)
   U=min(A,((n-2)*A+B)/n,F(n-1,n)*T-P,((n-1)*T-P-(n-1)*Q)/n,(T-P+(n-2)*A)/n)
   if (n-2)*(T-A)<=(n-1)*B and L<=U:
    M=max(T/n,T-A-U,(n-1)*(U+Q)-(n-2)*T,(n-1)*U-(n-2)*A)
    upper=min(T-P-U,(n-1)*(U+B)-(n-2)*T)
    assert M<=upper
    x=max(F(0),(n-1)*U-(n-2)*A,A-T+M);y=max(x,B-T+M)
    assert 0<=x<=y<=M and 0<=A-x<=B-y<=T-M
    if U>best:best=U;winner=('L',a,b,U,M,x,y)
 return best,winner

def reconstruct(n,g,w):
 T=g[-1]
 if w[0]=='H':
  _,c,E=w;C=g[c];x=max(F(0),(C-T+2*E)/2)
  points=[(F(0),[F(0)]*n),(C,[x,x]+[min(C,T-2*E)/(n-2)]*(n-2)),(T,[E,E]+[(T-2*E)/(n-2)]*(n-2))]
 else:
  _,a,b,E,M,x,y=w;A,B=g[a],g[b]
  points=[(F(0),[F(0)]*n),(A,[x]+[(A-x)/(n-1)]*(n-1)),(B,[y]+[(B-y)/(n-1)]*(n-1)),(T,[M]+[(T-M)/(n-1)]*(n-1))]
 clean=[]
 for p in points:
  if clean and p[0]==clean[-1][0]:assert p[1]==clean[-1][1]
  else:clean.append(p)
 for (a,u),(b,v) in zip(clean,clean[1:]):assert sum(v)-sum(u)==b-a and all(x<=y for x,y in zip(u,v))
 cum=[]
 for t in g[1:]:
  a,u,b,v=next((a,u,b,v) for (a,u),(b,v) in zip(clean,clean[1:]) if a<=t<=b)
  cum.append([x+(t-a)*(y-x)/(b-a) for x,y in zip(u,v)])
 return cum

def direct(n,g,cum):
 best=g[-1]
 for p,q,j in product(range(n),range(n),range(len(g))):
  W=[F(0)]*n;peak=F(0)
  for h,A in enumerate(cum):
   W[p if h<j else q]+=g[h+1]-g[h]
   peak=max(peak,max(abs(x-y) for x,y in zip(A,W)))
  best=min(best,peak)
 return best

for n in (3,4,6):
 for N in range(1,6):
  for typ in (0,1):
   g=[F(0)]
   for j in range(N):g.append(g[-1]+(F(1) if typ==0 else F(rng.randrange(1,10),rng.randrange(1,9))))
   formula,w=closed(n,g);vals=[]
   for a in range(1,N+1):
    for b in range(a,N+1):
     for family in (0,1):
      v=lp(n,g,a,b,family)
      if v is not None:vals.append(v)
   assert formula==max(vals),(n,g,formula,max(vals))
   assert direct(n,g,reconstruct(n,g,w))==formula
   stats['grids_with_certified_all_family_optima']+=1
for N in range(1,41):
 g=list(map(F,range(N+1)));v,w=closed(3,g);k,r=divmod(N,3)
 expected=F(2,3) if N==1 else F(k)+(F(0),F(1,2),F(3,4))[r]
 assert v==expected
 if N<=15:assert direct(3,g,reconstruct(3,g,w))==v
stats['exact_residue_grid_values']=40
print(dict(stats))
print('All independently assembled full-grid LP families and closed-form reconstructions passed.')
