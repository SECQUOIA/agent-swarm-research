"""Exact checks of stage 3 formulas, branch contracts, and constructions.

Finite checks supplement, and do not replace, the measurable-input proofs.
No numerical dependencies. All imports refer to the bundled reference copy.
"""
from fractions import Fraction as Q
from math import comb
from itertools import permutations
from random import Random
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'reference'))
from general_reach_research import old_upper, uniform_lower, seeded_upper, transfer
from check_seeded_review import multiply, divide
from two_switch_equal_mass_certificate import integral, reach
from arbitrary_block_certificate import errors


def coefficient_checks():
 count=branches=series=0
 for n in range(2,81):
  for k in range(1,n):
   old=old_upper(n,k); low=uniform_lower(n,k)
   assert low<=old and old>=Q(1,n)
   assert old-Q(1,k+1)==Q((n-k-1)*(2*n-k*(k+1)),n*k*(k+1)*(2*n-k-1))
   assert Q(1,k)-old==Q((k+1)*(n-k),n*k*(2*n-k-1))
   if k==1: assert old==low==Q(n-1,n)
   if k>1: assert old==transfer(n,old_upper(n-1,k-1))
   if k>=2: assert (old<=Q(1,k+1))==(k+1<=n<=k*(k+1)//2)
   if k>=4:
    c=seeded_upper(n,k,clipped=False); m=n-k+4
    assert c<old and c>=low
    assert (c<Q(1,n))==(m<=6)
    integer_test=(n+k+1)*(m-1)*(2*(m-1)**4-m**4)<=(n-k-1)*n*(n-1)*m**3
    assert integer_test==(c<=Q(1,k+1))
   for ell in range(1,min(4,k)+1):
    m=n-k+ell
    c=uniform_lower(m,ell)
    for size in range(m+1,n+1): c=transfer(size,c)
    assert c==seeded_upper(n,k,ell,clipped=False)
    count+=1
 for n in range(3,51):
  for factor in [Q(1,1000),Q(1,10),Q(999,1000),Q(1),Q(1001,1000),Q(3),Q(100)]:
   c=factor/(n-1); e=transfer(n,c)
   options=[]
   if factor<=1: options += [('minimum',a) for a in [Q(0),Q(1,2*n),Q(1,n)]]
   if factor>=1: options += [('maximum',a) for a in [Q(1,n),1-e,(1-e+Q(1,n))/2,Q(1)]]
   for choice,a in options:
    if choice=='maximum' and a<Q(1,n):continue
    if a>=1-e: assert 1-a<=e
    else:
     length=1-a-e; budget=e-a/(n-1)
     assert length>0 and budget>0 and c*length<=budget
    assert (n*e-1)/(n*e+1)==Q(n-2,n)*((n-1)*c-1)/((n-1)*c+1)
    branches+=1
 # Formal power series: all coefficients are exact, not fitted samples.
 for k in range(1,81):
  old=divide([Q(2),Q(-2*(k+1)),Q(k*(k+1))],[Q(2*k),Q(-k*(k+1))],3)
  low=divide([Q(1)],[Q(comb(k+j,j+1)) for j in range(3)],3)
  assert old==[Q(1,k),Q(-k-1,2*k),Q(k*k-1,4*k)]
  assert low==[Q(1,k),Q(-k-1,2*k),Q(k*k-1,12*k)]
  for ell in range(1,min(4,k)+1):
   d=k-ell
   ratio=divide([Q(1),Q(-d-1)],[Q(1),Q(-d)],4)
   power=[Q(1)]
   for _ in range(ell):power=multiply(power,ratio,4)
   power=[2*v for v in power]; power[0]-=1
   pre=divide(multiply([Q(1),Q(-d)],[Q(1),Q(-d-1)],4),[Q(1),Q(-1)],4)
   eta=multiply(pre,power,4)
   assert eta==[Q(1),Q(-2*k),Q(k*(k-1)),Q(k*(k-1))-Q(ell**3-ell,3)]
   num=list(eta);num[0]+=1
   value=divide(num,[-v for v in eta[1:]],3)
   expected=Q(3*k**3-3*k-2*ell**3+2*ell,12*k*k)
   assert value==[Q(1,k),Q(-k-1,2*k),expected]
   assert value[2]-low[2]==Q((k-ell)*(k*k+k*ell+ell*ell-1),6*k*k)
   series+=1
 print({'seed_coefficient_cases':count,'branch_contract_cases':branches,'formal_seed_series':series})


def predecessor_checks():
 def u(n):return Q(n**4-7*n**3+21*n*n-29*n+15,n*(2*n-3)*(2*n*n-6*n+5))
 def p(n):return n**4-17*n**3+77*n*n-130*n+75
 for n in range(5,101):
  assert u(n)==transfer(n,uniform_lower(n-1,3))
  assert u(n)-Q(1,5)==Q(p(n),5*n*(2*n-3)*(2*n*n-6*n+5))
  assert (u(n)<=Q(1,5))==(n<=11)
  num=6*n**4-20*n**3+21*n*n-7*n+1
  den=(2*n-3)*(2*n-1)*(2*n*n-6*n+5)*(2*n*n-2*n+1)
  assert u(n)-uniform_lower(n,4)==Q(num,den)>0
  h=n-5
  assert num==6*h**4+100*h**3+621*h*h+1703*h+1741
 for h in range(100):assert p(12+h)==h**4+31*h**3+329*h*h+1286*h+963
 assert [p(n) for n in range(5,12)]==[-150,-309,-492,-645,-690,-525,-24]
 assert divide([Q(1),Q(-7),Q(21),Q(-29),Q(15)],multiply([Q(2),Q(-3)],[Q(2),Q(-6),Q(5)],5),3)==[Q(1,4),Q(-5,8),Q(11,16)]
 assert seeded_upper(16,5,clipped=False)==Q(588449,3544816)<Q(1,6)<old_upper(16,5)==Q(35,208)
 assert seeded_upper(17,5,clipped=False)>Q(1,6)
 assert Q(245,1014)==(1-Q(1,6))/(1+Q(8,7)+Q(8,7)**2)<uniform_lower(8,3)==Q(343,1352)
 for n in range(2,101):
  for k in range(1,n):
   assert (Q(k*(n-k+1),n-k)>=n)==((n-k)**2<=k)
   assert (Q(k*(n-k+1),n-k)>=k+1)==(n<=2*k)
   for j in range(1,k+1):
    t=Q(j*(n-j+1),n-j)
    prev=Q((j-1)*(n-j+2),n-j+1)
    assert t>prev and (n-j)*t==(n-j+1)*prev+n-2*j+2
 print({'predecessor_rational_identities':'passed','plateaus_and_light_boundaries':'passed'})


def construct_seeded(a,k,T=Q(1),branches=None):
 n=len(a); e=seeded_upper(n,k,clipped=False)*T
 if k==4:
  for word in permutations(range(n),4):
   b=Q(0);blocks=[]
   for i in word:
    end=reach(a[i],b+e,T)
    blocks.append((i,b,end));b=end
    if b==T:return blocks
  raise AssertionError('Four-block seed failed')
 child=seeded_upper(n-1,k-1,clipped=False)
 masses=[integral(row,T) for row in a]
 kind='minimum' if child<Q(1,n-1) else 'maximum'
 q=(min if kind=='minimum' else max)(range(n),key=masses.__getitem__)
 if branches is not None: branches.add(kind)
 mass=masses[q]
 if mass>=T-e:
  if branches is not None:branches.add('constant')
  return [(q,Q(0),T)]
 length=T-mass-e
 assert child*length<=e-mass/(n-1) and e-mass/(n-1)>0
 indices=[i for i in range(n) if i!=q]
 completed=[[v+a[q][j]/(n-1) for j,v in enumerate(a[i])] for i in indices]
 blocks=construct_seeded(completed,k-1,length,branches)
 return [(indices[i],b,end) for i,b,end in blocks]+[(q,length,T)]


def greedy_light(a,k,e):
 n=len(a); b=Q(0);blocks=[];used=set()
 for j in range(1,k+1):
  end=min(Q(1),Q(j*(n-j+1),n-j)*e)
  i=max((i for i in range(n) if i not in used),key=lambda i:integral(a[i],end))
  used.add(i);blocks.append((i,b,end));b=end
  if end==1:break
 return blocks


def construction_checks():
 rng=Random(310907); seed_cases=light_cases=0;branches=set()
 for n in range(6,11):
  for k in range(5,n):
   for trial in range(5):
    cols=[]
    for j in range(5):
     weights=[rng.randrange(8) for _ in range(n)];weights[0]+=1
     if trial==0:weights=[1]*n
     if trial==1:weights=[1]+[0]*(n-1)
     cols.append([Q(v,sum(weights)) for v in weights])
    a=[list(row) for row in zip(*cols)]
    blocks=construct_seeded(a,k,branches=branches)
    negative,positive=errors(a,blocks)
    assert len(blocks)<=k and negative<=seeded_upper(n,k,clipped=False)
    seed_cases+=1
 for n in range(2,20):
  # Cyclic columns give exact equal terminal masses with nonconstant rates.
  weights=[rng.randrange(8) for _ in range(n)];weights[0]+=1
  a=[[Q(weights[(i+j)%n],sum(weights)) for j in range(n)] for i in range(n)]
  for k in range(1,n):
   e=Q(1,n);blocks=greedy_light(a,k,e);T=blocks[-1][2]
   negative,positive=errors(a,blocks,T)
   assert max(negative,positive)<=e
   if k>=(n-k)**2:assert T==1 and max(negative,positive)==e
   light_cases+=1
 assert branches=={'minimum','maximum','constant'}
 print({'seeded_measurable_construction_samples':seed_cases,'greedy_light_samples':light_cases,'branches':sorted(branches)})

if __name__=='__main__':
 if not __debug__:raise RuntimeError('Run without -O')
 coefficient_checks();predecessor_checks();construction_checks()
