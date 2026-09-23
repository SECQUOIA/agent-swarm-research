"""Independent closed-form witnesses and full cell/mode LP comparison.
No author code is imported. LP variables retain every mode and grid cell.
"""
from fractions import Fraction as F
from itertools import product
from random import Random
from pathlib import Path
import numpy as np,json
from scipy.optimize import linprog
OUT=Path(__file__).resolve().parent

def formula(n,t):
 T=t[-1];N=len(t)-1;c=next(j for j in range(1,N+1) if t[j]>=T/3)
 H=min((T+t[c])/4,(T-t[c-1])/2);best=H
 C=t[c];xx=max(F(0),(C-T+2*H)/2)
 anchors=[(F(0),[F(0)]*n),(C,[xx,xx]+[min(C,T-2*H)/(n-2)]*(n-2)),(T,[H,H]+[(T-2*H)/(n-2)]*(n-2))]
 winner='H'
 for a in range(1,N+1):
  for b in range(a,N+1):
   A,B,P,Q=t[a],t[b],t[a-1],t[b-1]
   lo=max(T/3,F(n-1,n)*T-B,((n-1)*T-A-(n-1)*B)/n)
   hi=min(A,((n-2)*A+B)/n,F(n-1,n)*T-P,((n-1)*T-P-(n-1)*Q)/n,(T-P+(n-2)*A)/n)
   if (n-2)*(T-A)>(n-1)*B or lo>hi:continue
   E=hi
   lowM=max(T/n,T-A-E,(n-1)*(E+Q)-(n-2)*T,(n-1)*E-(n-2)*A)
   highM=min(T-P-E,(n-1)*(E+B)-(n-2)*T)
   assert lowM<=highM
   M=lowM;x=max(F(0),(n-1)*E-(n-2)*A,A-T+M);y=max(x,B-T+M)
   if E>best:
    best=E;winner='U'
    anchors=[(F(0),[F(0)]*n),(A,[x]+[(A-x)/(n-1)]*(n-1)),(B,[y]+[(B-y)/(n-1)]*(n-1)),(T,[M]+[(T-M)/(n-1)]*(n-1))]
 points=[]
 for time,v in anchors:
  if points and points[-1][0]==time:assert points[-1][1]==v
  else:points.append((time,v))
 for (a,va),(b,vb) in zip(points,points[1:]):
  assert sum(va)==a and sum(vb)==b and all(y>=x for x,y in zip(va,vb))
 cumulative=[]
 for time in t:
  if time==0:cumulative.append([F(0)]*n);continue
  a,va,b,vb=next((a,va,b,vb) for (a,va),(b,vb) in zip(points,points[1:]) if a<=time<=b)
  cumulative.append([x+(time-a)*(y-x)/(b-a) for x,y in zip(va,vb)])
 observed=T
 for p,q,cut in product(range(n),range(n),range(N+1)):
  err=F(0)
  for time,Avec in zip(t,cumulative):
   W=[F(0)]*n;W[p]+=min(time,t[cut]);W[q]+=max(F(0),time-t[cut])
   err=max(err,max(abs(x-y) for x,y in zip(Avec,W)))
  observed=min(observed,err)
 assert observed==best
 return best,winner

def full_lp(n,t,a,b,family):
 N=len(t)-1;T=t[-1];size=n*N+1
 def pref(i,j):
  r=[F(0)]*size
  for l in range(j):r[i*N+l]=1
  return r
 def linear(*terms):
  r=[F(0)]*size
  for v,coef in terms:r=[x+coef*y for x,y in zip(r,v)]
  return r
 e=[F(0)]*size;e[-1]=1
 rows=[];rhs=[]
 def add(r,value):rows.append(r);rhs.append(value)
 for i in range(n-1):add(linear((pref(i+1,N),1),(pref(i,N),-1)),0)
 for i,j in ((0,a),(1,b)):
  v=linear((pref(i,N),1),(e,1))
  add(v,T-t[j-1]);add([-x for x in v],t[j]-T)
 add(linear((pref(1,a),1),(e,1)),t[a])
 add(linear((pref(0,b),1),(e,1)),t[b])
 if family=='all':
  for i in range(2,n):add(linear((pref(i,a),1),(e,1)),t[a])
 else:add(linear((e,1),(pref(1,N),-1)),0)
 eq=[];d=[]
 for j in range(N):
  r=[F(0)]*size
  for i in range(n):r[i*N+j]=1
  eq.append(r);d.append(t[j+1]-t[j])
 obj=[0]*size;obj[-1]=-1
 sol=linprog(obj,A_ub=np.asarray(rows,float),b_ub=np.asarray(rhs,float),A_eq=np.asarray(eq,float),b_eq=np.asarray(d,float),bounds=[(0,None)]*(size-1)+[(float(T/3),None)],method='highs')
 assert sol.status in (0,2)
 return None if sol.status==2 else -sol.fun
rng=Random(19131);cases=[]
for n in range(3,8):
 for N in range(1,7):cases.append((n,[F(j) for j in range(N+1)]))
for _ in range(35):
 n=rng.randint(3,8);N=rng.randint(1,6);t=[F(0)]
 for j in range(N):t.append(t[-1]+F(rng.randint(1,13),rng.randint(1,9)))
 cases.append((n,t))
branches={'H':0,'U':0};lpcount=0
for n,t in cases:
 best,which=formula(n,t);branches[which]+=1
 values=[]
 for a in range(1,len(t)):
  for b in range(a,len(t)):
   for family in ('all','two'):
    value=full_lp(n,t,a,b,family);lpcount+=1
    if value is not None:values.append(value)
 assert values and abs(max(values)-float(best))<1e-7*(1+float(t[-1])),(n,t,best,max(values))
for N in range(1,31):
 best,_=formula(3,[F(j) for j in range(N+1)])
 q,r=divmod(N,3);expected=F(2,3) if N==1 else q+(F(0),F(1,2),F(3,4))[r]
 assert best==expected
specials=[(5,[F(j) for j in range(10)],F(17,5)),(9,list(map(F,['0','19/2','61/6','265/24','481/24','2669/120'])),F(2593,270))]
for n,t,expected in specials:assert formula(n,t)[0]==expected
result={'full_mode_cell_LPs':lpcount,'grids_compared':len(cases),'winning_families':branches,'n3_residues_exact_up_to_N':30,'extra_exact_examples':2}
(OUT/'grid-results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
