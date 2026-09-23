import sys
sys.dont_write_bytecode=True
from pathlib import Path
from fractions import Fraction as Q
from itertools import combinations,combinations_with_replacement,product
import json
from scipy.optimize import linprog
import sympy as S
HERE=Path(__file__).resolve().parent; REF=HERE/'relocated/verification/reference'
# Independently assemble all appendix rows from the manuscript, without using
# the original relaxation builder or chronological program.
U=frozenset(range(6));events=[(h,tuple(c)) for h in (2,3) for m in range(6,h,-1) for c in combinations(range(6),m)]
assert len(events)==64;lookup={e:j for j,e in enumerate(events)}
def t(h,u):return 6+7*lookup[h,tuple(sorted(u))]
def a(h,u,i):return t(h,u)+1+i
rows=[];eq=[]
def add(terms,b,where=rows):
 d={}
 for i,v in terms:d[i]=d.get(i,0)+v
 where.append((tuple(sorted((i,v) for i,v in d.items() if v)),b))
for i in range(6):add([(i,-1)],-1)
for i in range(1,6):add([(0,1),(i,-1)],0)
add([(i,-1) for i in range(1,6)],-6)
for h,u in events:
 add([(t(h,u),-1)]+[(a(h,u,i),1) for i in range(6)],0,eq)
 for i in u:add([(i,1),(a(h,u,i),-1)],1)
 if h==2:
  for i in u:
   for j in u:
    if i!=j:add([(j,1),(a(h,u,i),1),(t(h,u),-1)],-1)
 else:
  for i in u:add([(t(2,set(u)-{i}),1),(a(h,u,i),1),(t(h,u),-1)],-1)
for h,u in events:
 for hh,v in events:
  if h<=hh and set(u)<=set(v) and (h,u)!=(hh,v):
   for i in range(6):add([(a(h,u,i),1),(a(hh,v,i),-1)],0)
for h,u in events:
 if len(u)<6 and set(range(h))<=set(u):
  for i in range(6):add([(a(h,U,i),1),(a(h,u,i),-1)],0)
assert len(rows)==3660 and len(eq)==64
objective=[0]*454
for i in range(4):
 objective[t(3,U-{i})]+=1
 for j in U-{i}:objective[t(3,U-{i,j})]+=1
old=list(map(Q,json.loads((REF/'general_reach_relaxation_witness.json').read_text())['variables']))
def dot(row,x):return sum(v*x[i] for i,v in row)
assert min(old)>=0 and all(dot(row,old)<=b for row,b in rows) and all(dot(row,old)==b for row,b in eq)
assert sum(v*x for v,x in zip(objective,old))==Q(40328,387)
order=sorted(range(64),key=lambda j:(old[6+7*j],j))
violations=[old[7+7*i+h]-old[7+7*j+h] for ii,i in enumerate(order) for j in order[ii+1:] for h in range(6) if old[7+7*i+h]>old[7+7*j+h]]
assert len(violations)==239 and max(violations)==Q(224,645)
cert=json.loads((HERE/'relocated/verification/stage03/chronological_chamber_certificate.json').read_text())
assert order==cert['order']
for i,j in zip(order,order[1:]):
 for h in range(6):add([(7+7*i+h,1),(7+7*j+h,-1)],0)
rows.sort();eq.sort();assert len(rows)==4038
y=list(map(Q,cert['inequality_dual']));z=list(map(Q,cert['equality_dual']));primal=list(map(Q,cert['primal']))
assert len(y)==len(rows) and len(z)==len(eq) and max(y)<=0
residual=list(map(Q,objective))
for mul,(row,b) in list(zip(y,rows))+list(zip(z,eq)):
 for i,v in row:residual[i]-=mul*v
bound=sum(v*b for v,(_,b) in zip(y,rows))+sum(v*b for v,(_,b) in zip(z,eq))
assert min(residual)>=0 and bound==Q(13104,125)
assert min(primal)>=0 and all(dot(row,primal)<=b for row,b in rows) and all(dot(row,primal)==b for row,b in eq)
assert sum(v*x for v,x in zip(objective,primal))==bound
print('PASS independent appendix: 454 variables, 3660 original/4038 strengthened rows, 64 equalities, exact witness, chronological failures, dual bound and attaining primal',flush=True)
# Exact symbolic algebra, not numerical substitution, for mode removal and the
# closed/seeded coefficients and all seed asymptotics.
n,c,x=S.symbols('n c x');k=S.symbols('k',positive=True,integer=True)
f=((n-1)**2*c+1)/(n*(n-1)*(1+c))
assert S.factor(f-1/n-(n-2)*((n-1)*c-1)/(n*(n-1)*(c+1)))==0
assert S.factor(S.diff(f,c)-(n-2)/((n-1)*(1+c)**2))==0
C=(n*(n-1)+(n-k)*(n-k-1))/(n*k*(2*n-k-1))
assert S.factor(C-1/(k+1)-2*(n-k-1)*(n-k*(k+1)/2)/(n*k*(k+1)*(2*n-k-1)))==0
assert S.factor(1/k-C-(k+1)*(n-k)/(n*k*(2*n-k-1)))==0
checks=0
for kk in range(1,11):
 L=1/(n*((n/(n-1))**kk-1))
 assert S.series(L.subs(n,1/x),x,0,3).removeO().expand()==S.Rational(1,kk)-S.Rational(kk+1,2*kk)*x+S.Rational(kk*kk-1,12*kk)*x*x
 for ell in range(1,min(4,kk)+1):
  m=n-kk+ell;theta=m*(m-1)/(n*(n-1))*(2*((m-1)/m)**ell-1)
  seeded=(1+theta)/(n*(1-theta))
  expected=S.Rational(1,kk)-S.Rational(kk+1,2*kk)*x+S.Rational(3*kk**3-3*kk-2*ell**3+2*ell,12*kk**2)*x*x
  assert S.series(seeded.subs(n,1/x),x,0,3).removeO().expand()==expected
  if kk==ell:assert S.factor(seeded-L)==0
  checks+=1
for nn in range(5,50):
 for kk in range(4,nn):
  m=nn-kk+4;th=Q(m*(m-1),nn*(nn-1))*(2*Q(m-1,m)**4-1);s=(1+th)/(nn*(1-th))
  criterion=(nn+kk+1)*(m-1)*(2*(m-1)**4-m**4)<=(nn-kk-1)*nn*(nn-1)*m**3
  assert (s<=Q(1,kk+1))==criterion
print('PASS symbolic recurrence, plateau identities, dimension gap,',checks,'exact seed series; 1035 integer plateau comparisons',flush=True)
# Fresh all-word continuous LP audit of the n=3 obstruction. Use block lengths
# (rather than author switch-time coordinates), and certify every LP exactly.
knots=[(0,0,0,0),(146,98,48,0),(194,110,48,36),(256,110,78,68),(408,224,116,68),(516,224,178,114),(580,240,178,162),(971,417,309,245)]
g=[Q(v[0],146) for v in knots];cum=[list(Q(x,146) for x in v[1:]) for v in knots];T=Q(57,8)
cum.append([x+(T-g[-1])/3 for x in cum[-1]]);g.append(T)
rates=[[(y-x)/(b-a) for x,y in zip(u,v)] for a,b,u,v in zip(g,g[1:],cum,cum[1:])]
certificates=[]
def certify(A,b):
 r=linprog([0,0,0,1],A_ub=[[float(v) for v in row] for row in A],b_ub=[float(v) for v in b],bounds=[(0,None)]*4,method='highs')
 assert r.success
 for den in (10**5,10**7,10**9,10**12):
  xx=[Q(float(v)).limit_denominator(den) for v in r.x];yy=[Q(float(v)).limit_denominator(den) for v in r.ineqlin.marginals]
  red=[Q(j==3)-sum(y*row[j] for y,row in zip(yy,A)) for j in range(4)]
  if min(xx)>=0 and max(yy)<=0 and min(red)>=0 and all(sum(v*x for v,x in zip(row,xx))<=rhs for row,rhs in zip(A,b)) and xx[-1]==sum(y*rhs for y,rhs in zip(yy,b)):
   return xx,yy
 # Reconstruct an exact primal/dual basis when componentwise approximation
 # does not recover the floating solution's common rational vertex.
 allA=A+[[-Q(i==j) for j in range(4)] for i in range(4)]
 allb=b+[Q(0)]*4
 active=[i for i,v in enumerate(r.ineqlin.residual) if abs(v)<1e-7]+[len(A)+i for i,v in enumerate(r.x) if abs(v)<1e-7]
 for basis in combinations(active,4):
  mat=S.Matrix([allA[i] for i in basis])
  if mat.det()==0:continue
  xx=list(map(Q,mat.inv()*S.Matrix([allb[i] for i in basis])))
  yybase=list(map(Q,mat.T.inv()*S.Matrix([0,0,0,1])))
  if max(yybase)>0 or min(xx)<0:continue
  if not all(sum(v*x for v,x in zip(row,xx))<=rhs for row,rhs in zip(A,b)):continue
  yy=[Q(0)]*len(A)
  for i,v in zip(basis,yybase):
   if i<len(A):yy[i]=v
  assert xx[-1]==sum(y*rhs for y,rhs in zip(yy,b))
  assert min(Q(j==3)-sum(y*row[j] for y,row in zip(yy,A)) for j in range(4))>=0
  return xx,yy
 raise AssertionError(('exact basis reconstruction failed',word,cells))
for word in product(range(3),repeat=3):
 for cells in combinations_with_replacement(range(8),2):
  A=[];b=[]
  def add(row,rhs):A.append(list(map(Q,row)));b.append(Q(rhs))
  add([1,1,1,0],T);add([-1,-1,-1,0],-T);add([0,0,0,1],T)
  for j,cell in enumerate(cells,1):
   add([int(h<j) for h in range(3)]+[0],g[cell+1]);add([-int(h<j) for h in range(3)]+[0],-g[cell])
  for j,cell in enumerate(cells+(7,),1):
   for i in range(3):
    rate=rates[cell][i];offset=cum[cell][i]-rate*g[cell]
    coeff=[int(word[h]==i)-rate if h<j else 0 for h in range(3)]
    add(coeff+[-1],offset)
  xx,yy=certify(A,b)
  certificates.append({'word':word,'cells':cells,'primal':list(map(str,xx)),'dual':list(map(str,yy))})
assert len(certificates)==972
value=min(Q(r['primal'][-1]) for r in certificates);assert value==Q(18673,18396)
best=[r for r in certificates if Q(r['primal'][-1])==value]
repeat_min=min(Q(r['primal'][-1]) for r in certificates if len(set(r['word']))<3)
assert repeat_min>value
(HERE/'n3-all-word-certificates.json').write_text(json.dumps({'optimum':str(value),'best':best,'repeated_word_minimum':str(repeat_min),'programs':certificates},indent=2)+'\n')
print('PASS n3 all 972 LPs certified exactly: optimum',value,'repeated-word minimum',repeat_min,'matching cases',len(best),flush=True)
# Four-block symbolic topology tested beyond interpolation points, including
# the first symbolic dimension and larger finite dimensions.
sys.path.insert(0,str(REF));import verify_general_four_block as four
for pair,z0 in four.CASES:
 V,A,b,B,d,obj=four.symbolic_program(pair,z0)
 for nn in (11,17,23,31):
  VV,AA,bb,BB,dd,cc=four.quotient(nn,pair,z0)
  assert VV==V and AA==A and bb==b and dd==d
  def evaluate(p):return sum(v*nn**j for j,v in enumerate(p))
  assert [tuple((i,evaluate(p)) for i,p in row.items() if evaluate(p)) for row in B]==BB
  assert list(map(evaluate,obj))==cc
print('PASS 40 extra all-dimension quotient topology/objective checks',flush=True)
