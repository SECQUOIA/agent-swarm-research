from fractions import Fraction as Q
from itertools import product
from pathlib import Path
from random import Random
import sys
base=Path(__file__).resolve().parent/'relocated/verification'
sys.path.insert(0,str(base/'reference'));sys.path.insert(0,str(base/'stage05'))
from rounding import optimal_few_switches
from coarsening import certified_coarsen
from continuous_exact import optimal_continuous
rng=Random(70907)

def cumulative(rows,dt,t):
 out=[Q(0)]*len(rows[0]);b=Q(0)
 for row,d in zip(rows,dt):
  length=max(Q(0),min(d,t-b))
  for i,z in enumerate(row):out[i]+=z*length/d
  b+=d
 return out

def error(rows,dt,word,outdt=None):
 if outdt is None:outdt=dt
 input_times=[Q(0)];output_times=[Q(0)]
 for d in dt:input_times.append(input_times[-1]+d)
 for d in outdt:output_times.append(output_times[-1]+d)
 peak=Q(0)
 for t in sorted(set(input_times+output_times)):
  a=cumulative(rows,dt,t);w=[Q(0)]*len(rows[0])
  for i,lo,hi in zip(word,output_times,output_times[1:]):w[i]+=max(Q(0),min(t,hi)-lo)
  peak=max(peak,max(abs(x-y) for x,y in zip(a,w)))
 return peak

def feasible(word,dt,s,dwell):
 if sum(a!=b for a,b in zip(word,word[1:]))>s:return False
 mode=word[0];run=Q(0)
 for i,d in zip(word,dt):
  if i!=mode:
   if run<dwell[mode]:return False
   run=Q(0);mode=i
  run+=d
 return run>=dwell[mode]

count=0
for n in (2,3):
 for trial in range(20):
  N=rng.randrange(1,5);dt=tuple(Q(rng.randrange(1,7),rng.randrange(1,7)) for _ in range(N));T=sum(dt)
  rows=[]
  for d in dt:
   weights=[rng.randrange(5) for _ in range(n)];weights[0]+=1
   rows.append(tuple(d*Q(x,sum(weights)) for x in weights))
  for s in (0,1,2,N+2):
   dwell=tuple(rng.choice((Q(0),T/4,T/2,T,2*T)) for _ in range(n))
   candidates=[error(rows,dt,w) for w in product(range(n),repeat=N) if feasible(w,dt,s,dwell)]
   best=min(candidates) if candidates else None
   got=optimal_few_switches(rows,dt,s,minimum_dwell=dwell)
   assert (got is None)==(best is None)
   if got:
    assert got.error==best==error(rows,dt,got.schedule())
    assert feasible(got.schedule(),dt,s,dwell)
   count+=1
print('PASS subset/dwell exact exhaustive comparisons:',count)

def one_continuous(rows,dt):
 n=len(rows[0]);T=sum(dt);mass=cumulative(rows,dt,T);best=T
 for p,q in product(range(n),repeat=2):
  if p==q:continue
  before=Q(0);ap=Q(0);tau=None
  for row,d in zip(rows,dt):
   rate=row[p]/d
   # solve 2*t-A_p(t)-T+m_q=0 on this segment
   candidate=(ap-rate*before+T-mass[q])/(2-rate)
   if before<=candidate<=before+d:tau=candidate;break
   before+=d;ap+=row[p]
  assert tau is not None
  val=error(rows,dt,(p,q),(tau,T-tau))
  best=min(best,val)
 return best

continuous=coarse=0
for n in (2,3):
 for trial in range(7):
  N=2;dt=tuple(Q(rng.randrange(1,5),rng.randrange(1,5)) for _ in range(N));rows=[]
  for d in dt:
   w=[rng.randrange(5) for _ in range(n)];w[0]+=1
   rows.append(tuple(d*Q(x,sum(w)) for x in w))
  exact=one_continuous(rows,dt)
  result=optimal_continuous(rows,dt,1)
  assert result.error==exact
  assert result.error==error(rows,dt,result.modes,tuple(b-a for a,b in zip(result.times,result.times[1:])))
  continuous+=1
  for M in (1,2,3,4):
   answer=certified_coarsen(rows,dt,1,cells=M)
   direct=error(rows,dt,answer.schedule,(sum(dt)/M,)*M)
   brute=min(error(rows,dt,w,(sum(dt)/M,)*M) for w in product(range(n),repeat=M) if sum(a!=b for a,b in zip(w,w[1:]))<=1)
   assert direct==answer.exact_error==brute
   assert answer.lower<exact if answer.lower_strict else answer.lower<=exact
   assert exact<=answer.upper
   assert answer.exact_error-exact<=sum(dt)/(2*M)
   coarse+=1
print('PASS exact continuous vertex vs independent crossing solution:',continuous)
print('PASS coarse errors/exhaustive optima and exact continuous interval including half-mesh:',coarse)
# An additional repeated-mode analytic case. For a binary uniform input and
# word 0,1,0, error E implies u<=2E, v<=2u+2E, and v-u>=1/2-E.
# Hence E>=1/10; u=1/5,v=3/5 attains it. Other words have <=1 switch
# unless they are the relabeled alternating word, and cannot improve it.
for one_sided in (False,True):
 result=optimal_continuous(((Q(1,2),Q(1,2)),),(Q(1),),2,one_sided=one_sided)
 assert result.error==Q(1,10)
print('PASS repeated-mode one-cell continuous optimum 1/10 for both objectives')
