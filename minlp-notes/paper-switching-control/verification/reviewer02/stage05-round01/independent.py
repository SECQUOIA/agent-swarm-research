import sys
sys.dont_write_bytecode=True
from pathlib import Path
from fractions import Fraction as Q
from itertools import product,combinations_with_replacement,permutations
from random import Random
from collections import Counter
from scipy.optimize import linprog
HERE=Path(__file__).resolve().parent
REF=HERE/'relocated'/'verification'
sys.path[:0]=[str(REF/'reference'),str(REF/'stage05')]
from rounding import optimal_few_switches,optimal_one_switch,complete_with_one_block
from continuous_exact import optimal_continuous
from coarsening import certified_coarsen
stats=Counter();rng=Random(552031)
def sw(w):return sum(a!=b for a,b in zip(w,w[1:]))
def err(rows,dt,w):
 z=[Q(0)]*len(rows[0]);best=Q(0)
 for a,d,p in zip(rows,dt,w):
  z=[z[i]+a[i]-d*(i==p) for i in range(len(z))];best=max(best,*map(abs,z))
 return best

def dwell_ok(w,dt,dwell):
 start=0
 for j in range(1,len(w)+1):
  if j==len(w) or w[j]!=w[start]:
   if sum(dt[start:j])<dwell[w[start]]:return False
   start=j
 return True
for n,N in ((2,1),(3,2),(3,4),(4,3),(2,5)):
 for trial in range(5):
  dt=tuple(Q(rng.randrange(1,6),rng.randrange(1,7)) for _ in range(N))
  rows=[]
  for d in dt:
   weights=[rng.randrange(4) for i in range(n)]
   if not sum(weights):weights[0]=1
   rows.append(tuple(d*w/sum(weights) for w in weights))
  words=list(product(range(n),repeat=N));errors={w:err(rows,dt,w) for w in words}
  for s in range(N+2):
   for dwell in ((Q(0),)*n,tuple(Q(rng.randrange(7),3) for i in range(n)),(sum(dt)+1,)*n):
    valid=[w for w in words if sw(w)<=s and dwell_ok(w,dt,dwell)]
    got=optimal_few_switches(rows,dt,s,minimum_dwell=dwell)
    expected=min((errors[w] for w in valid),default=None)
    assert (None if got is None else got.error)==expected
    if got is not None:assert got.schedule() in valid and errors[got.schedule()]==expected
    stats['grid_budget_dwell_instances']+=1
  for initial in (None,*range(n)):
   allowed={j for j in range(1,N) if rng.randrange(2)}
   valid=[w for w in words if (initial is None or w[0]==initial) and sw(w)<=1 and all(w[j]==w[j-1] or j in allowed for j in range(1,N))]
   got=optimal_one_switch(rows,dt,initial_mode=initial,switch_indices=allowed)
   assert got.error==min(errors[w] for w in valid)==errors[got.schedule()]
   stats['one_switch_restricted_instances']+=1
  for size in range(N):
   pref=tuple(rng.randrange(n) for _ in range(size))
   for required in (False,True):
    eligible=[i for i in range(n) if not(required and pref and i==pref[-1])]
    got,p=complete_with_one_block(rows,dt,pref,require_switch=required)
    assert got==min(errors[pref+(i,)*(N-size)] for i in eligible)==errors[pref+(p,)*(N-size)]
    stats['fixed_prefix_completions']+=1
# Independent exact dual certification with nonnegative block-length variables.
def exact_lp(c,A,b):
 r=linprog([float(x) for x in c],A_ub=[[float(x) for x in row] for row in A],b_ub=[float(x) for x in b],bounds=[(0,None)]*len(c),method='highs')
 assert r.success
 for den in (10**5,10**7,10**9):
  x=[Q(float(v)).limit_denominator(den) for v in r.x]
  y=[Q(float(v)).limit_denominator(den) for v in r.ineqlin.marginals]
  reduced=[c[j]-sum(v*row[j] for v,row in zip(y,A)) for j in range(len(c))]
  if min(x)>=0 and max(y)<=0 and min(reduced)>=0 and all(sum(v*t for v,t in zip(row,x))<=rhs for row,rhs in zip(A,b)) and sum(v*t for v,t in zip(c,x))==sum(v*t for v,t in zip(y,b)):
   stats['continuous_exact_primal_dual_certificates']+=1
   return sum(v*t for v,t in zip(c,x))
 raise AssertionError('failed exact certificate')
def independent_cont(rows,dt,s,one):
 n=len(rows[0]);k=s+1;g=[Q(0)];cum=[[Q(0)]*n]
 for a,d in zip(rows,dt):g.append(g[-1]+d);cum.append([x+y for x,y in zip(cum[-1],a)])
 T=g[-1];best=T
 for cells in combinations_with_replacement(range(len(dt)),k-1):
  for word in product(range(n),repeat=k):
   A=[];b=[]
   def add(row,rhs):A.append(list(map(Q,row)));b.append(Q(rhs))
   add([1]*k+[0],T);add([-1]*k+[0],-T);add([0]*k+[1],T)
   for j in range(1,k):
    cell=cells[j-1];add([int(h<j) for h in range(k)]+[0],g[cell+1]);add([-int(h<j) for h in range(k)]+[0],-g[cell])
   for j in range(1,k+1):
    cell=cells[j-1] if j<k else len(dt)-1
    for i in range(n):
     rate=rows[cell][i]/dt[cell];offset=cum[cell][i]-rate*g[cell]
     coeff=[(rate-int(word[h]==i)) if h<j else Q(0) for h in range(k)]
     add([-v for v in coeff]+[-1],offset)
     if not one:add(coeff+[-1],-offset)
   best=min(best,exact_lp([Q(0)]*k+[Q(1)],A,b))
 return best
cases=[(((Q(1,4),Q(1,12)),(Q(1,6),Q(1,2))),(Q(1,3),Q(2,3)),1),
       (((Q(1,5),Q(2,5)),(Q(2,5),0)),(Q(3,5),Q(2,5)),2),
       (((Q(1,2),Q(1,3),Q(1,6)),),(1,),2)]
for rows,dt,s in cases:
 for one in (False,True):
  expected=independent_cont(rows,dt,s,one)
  got=optimal_continuous(rows,dt,s,one_sided=one)
  assert got.error==expected,(rows,dt,s,one,got,expected)
  stats['continuous_instances']+=1
  if not one:
   for M in (1,2,3,5):
    cert=certified_coarsen(rows,dt,s,cells=M)
    assert (cert.lower<expected if cert.lower_strict else cert.lower<=expected) and expected<=cert.upper
    stats['coarsening_against_continuous_exact']+=1
# Enumerate support witnesses for every 3-mode word on 6 unequal microintervals,
# grouped into 3 equal coarse cells, but with unequal splits inside each cell.
dt=[Q(1,7),Q(6,7),Q(2,7),Q(5,7),Q(3,7),Q(4,7)]
for old in product(range(3),repeat=6):
 support=[sorted(set(old[2*j:2*j+2])) for j in range(3)];found=False
 for new in product(*support):
  counts=[0]*3;mass=[Q(0)]*3;valid=True
  for j,p in enumerate(new):
   counts[p]+=1
   for h in (2*j,2*j+1):mass[old[h]]+=dt[h]
   valid &= all(x.numerator//x.denominator<=c<=-((-x.numerator)//x.denominator) for x,c in zip(mass,counts))
  if valid:
   assert sw(new)<=sw(old)
   rows=[tuple(d*int(p==i) for i in range(3)) for d,p in zip(dt,old)]
   assert err(rows,dt,tuple(p for p in new for _ in range(2)))<1
   found=True
 assert found
 stats['unequal_microinterval_support_controls']+=1
# Candidate-set exchange lemma on arbitrary rational bottleneck assignment data.
for n,d in ((4,1),(5,2),(6,3)):
 for trial in range(40):
  masses=[rng.randrange(5) for _ in range(n)];cost=[[rng.randrange(9) for _ in range(n)] for _ in range(d)]
  union=set(sorted(range(n),key=lambda i:(-masses[i],i))[:d])
  for row in cost:union.update(sorted(range(n),key=lambda i:(row[i],i))[:d])
  def obj(p):return max([cost[r][i] for r,i in enumerate(p)]+[masses[i] for i in range(n) if i not in p])
  assert min(map(obj,permutations(range(n),d)))==min(map(obj,permutations(union,d)))
  stats['candidate_exchange_instances']+=1
print(dict(stats))
