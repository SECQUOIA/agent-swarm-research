from fractions import Fraction as Q
from itertools import product

alpha=Q(2)
widths=(Q(1),Q(3,16))
branches=[((Q(-3,4),Q(-1,8)),Q(0)),((Q(-5,4),Q(-1,4)),Q(1,5))]

def f(v):
 return alpha*sum(x*x for x in v)/2+min(sum(a*x for a,x in zip(slope,v))+c for slope,c in branches)

def optimum(noise):
 vals=[]
 for slope,c in branches:
  x=[min(w,max(Q(0),-(a+d)/alpha)) for a,d,w in zip(slope,noise,widths)]
  vals.append(alpha*sum(z*z for z in x)/2+sum((a+d)*z for a,d,z in zip(slope,noise,x))+c)
 return min(vals)

sigma=Q(1,4); M=9
noises=[-sigma+2*sigma*j/(M-1) for j in range(M)]
total_near=0; interval_checks=0
previous=(1,1)
near_counts={}
level_data=[]
for level in range(6):
 h=max(widths)/2**level
 counts=[]
 for w in widths:
  m=1
  while w/m>h:m*=2
  counts.append(m)
 assert all(m in (old,2*old) for m,old in zip(counts,previous))
 previous=counts
 steps=[w/m for w,m in zip(widths,counts)]
 assert all(m==1 or h/2<t<=h for m,t in zip(counts,steps))
 B=alpha*sum(t*t for t in steps)/8
 delta=2*B
 level_data.append((tuple(counts),tuple(steps),B))
 points=list(product(*[[j*t for j in range(m+1)] for m,t in zip(counts,steps)]))
 expected=Q(0)
 for noise in product(noises,repeat=2):
  star=optimum(noise)
  near_counts[level,noise]=0
  for v in points:
   if f(v)+sum(c*x for c,x in zip(noise,v))>star+delta:continue
   expected+=Q(1,M*M); total_near+=1
   near_counts[level,noise]+=1
   for i,(m,t) in enumerate(zip(counts,steps)):
    if v[i] in (0,widths[i]):continue
    left=list(v);right=list(v);left[i]-=t;right[i]+=t
    low=(f(v)-f(tuple(right))-delta)/t
    high=(f(tuple(left))-f(v)+delta)/t
    assert low<=noise[i]<=high
    assert high-low<=alpha*t+2*delta/t
    assert high-low<=alpha*t*(1+2*len(widths))
    interval_checks+=1
 bound=Q(1)
 for m,t in zip(counts,steps):
  prob=min(Q(1),(alpha*t+2*delta/t)/(2*sigma)+Q(1,M))
  bound*=2+(m-1)*prob
 assert expected<=bound
 print('PASS level',level,'partitions',counts,'expected near-optimal points',expected,'bound',bound)

# A fixed atomic noise distribution cannot give a mesh-uniform bound.
# f=0, c=0 has mass 1/M. All grid points are globally optimal on this event.
for m in (8,64,512):
 lower=Q(m+1,M)
 assert lower>Q(m,M)
print('PASS:',total_near,'near-optimal events;',interval_checks,'necessary interval checks; atomic-noise lower bound grows as (m+1)/M')

processed=0; survivors=0
for noise in product(noises,repeat=2):
 cells=[(0,0)]; incumbent=None; old_counts=(1,1)
 for level,(counts,steps,B) in enumerate(level_data):
  if level:
   cells=[tuple(v) for parent in kept for v in product(*[[2*i,2*i+1] if m==2*old else [i] for i,m,old in zip(parent,counts,old_counts)])]
  evaluated=[]
  for cell in cells:
   vals=[]
   for bits in product((0,1),repeat=2):
    v=tuple((i+b)*t for i,b,t in zip(cell,bits,steps))
    vals.append(f(v)+sum(c*x for c,x in zip(noise,v)))
   upper=min(vals); lb=upper-B
   incumbent=upper if incumbent is None else min(incumbent,upper)
   evaluated.append((cell,lb));processed+=1
  kept=[cell for cell,lb in evaluated if lb<incumbent]
  lower=min([incumbent]+[lb for _,lb in evaluated if lb<incumbent])
  assert lower<=optimum(noise)<=incumbent
  assert incumbent-lower<=B
  assert incumbent-optimum(noise)<=B
  assert len(kept)<=4*near_counts[level,noise]
  survivors+=len(kept);old_counts=counts
  if not kept:break
print('PASS:',processed,'processed cells;',survivors,'surviving cells; all intervals and near-optimal-corner counts valid')
