from fractions import Fraction as Q
from itertools import product
from independent_algorithms import direct,knots,changes,optimal_few_switches,certified_coarsen,optimal_continuous
# Independently known continuous binary instance values bracketed using perturbed data.
cases=0
for a,b in ((Q(1,7),Q(1,6)),(Q(3,5),Q(2,3)),(Q(0),Q(1,10)),(Q(1),Q(9,10))):
 original=((a,1-a),); supplied=((b,1-b),);dt=(Q(1),)
 exact=a*(1-a)/(1+max(a,1-a))
 for M in (1,2,3,5):
  cert=certified_coarsen(supplied,dt,1,cells=M,cumulative_tolerance=abs(a-b))
  assert (cert.lower<exact if cert.lower_strict else cert.lower<=exact)
  actual=direct(original,dt,cert.schedule,tuple(Q(j,M) for j in range(M+1)))
  assert exact<=actual<=cert.upper
  assert actual-exact<cert.mesh_width+2*abs(a-b)
  cases+=1
print("PASS positive input-perturbation certificates against 16 analytic original optima")
# Boundary-degenerate time-cell enumeration, budget greater than input-cell count.
for side in (False,True):
 got=optimal_continuous(((Q(1,2),Q(1,2)),),(Q(1),),2,one_sided=side)
 assert got.error==Q(1,10)==direct(((Q(1,2),Q(1,2)),),(Q(1),),got.modes,got.times,side)
print("PASS N=1, s=2 continuous exact enumeration; binary uniform optimum 1/10 for both criteria")
for n,m in ((2,1),(3,1),(4,1),(2,2)):
 N=n*m+1;rows=((Q(1,n),)*n,)+tuple(tuple(Q(i==n-1) for i in range(n)) for _ in range(N-1));dt=(Q(1),)*N
 answer=optimal_few_switches(rows,dt,n*m-1)
 assert answer.error==1-Q(1,n)
 word=tuple(i for _ in range(m) for i in range(n))
 times=tuple(Q(j,n*m) for j in range(n*m))+(Q(N),)
 error=direct(rows,dt,word,times)
 assert error==Q(n-1,n*n*m)
 assert answer.error-error==(1-Q(1,n))*(1-Q(1,n*m))
print("PASS four exact sharp-gap schedules and exact grid optima, including the 9/16 half-mesh counterexample")
for M in (1,3,5,9):
 h=Q(1,M);rows=[]
 for j in range(M):
  a=max(Q(0),min((j+1)*h,Q(1,2))-j*h)
  rows.append((a,h-a))
 got=optimal_few_switches(rows,(h,)*M,1,minimum_dwell=(Q(1,2),)*2)
 assert got.error==Q(1,2) and changes(got.schedule())==0
print("PASS odd-grid dwell obstruction at M=1,3,5,9")
