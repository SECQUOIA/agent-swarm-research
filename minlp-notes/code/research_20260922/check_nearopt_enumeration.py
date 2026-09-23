"""Exact finite checks for near-optimal counting and approximate enumeration.

The probability checks enumerate the noise outcomes. The enumeration oracle
deliberately returns the worst value permitted by its additive guarantee.
These checks challenge finite cases; they do not prove the general theorem.
"""

from fractions import Fraction as F
from itertools import product
import heapq, random
rng=random.Random(9283)
countcases=outcomes=0
for n in range(1,4):
    cube=list(product((0,1),repeat=n))
    families=[tuple(z for j,z in enumerate(cube) if mask>>j&1) for mask in range(1,1<<len(cube))]
    for Z in families:
      for mode in range(2):
        g={z:F(0) if mode==0 else F(sum((i+1)*(2*z[i]-1) for i in range(n)),4) for z in Z}
        for N in (2,3):
          grid=[F(-1)+F(2*j,N-1) for j in range(N)]
          sums={d:0 for d in (F(0),F(1,4),F(1,2))}
          for xi in product(grid,repeat=n):
            vals={z:g[z]+sum(a*b for a,b in zip(z,xi)) for z in Z}
            v=min(vals.values())
            for d in sums: sums[d]+=sum(val<=v+d for val in vals.values())
            outcomes+=1
          for d,tot in sums.items():
            assert F(tot,N**n)<=(1+d+F(1,N))**n,(n,Z,g,N,d,tot)
            countcases+=1

runs=extractions=oracles=0
for n in range(1,7):
  cube=list(product((0,1),repeat=n))
  tables=[]
  if n<=2:
    for values in product(range(3),repeat=len(cube)):
      tables.append(dict(zip(cube,map(F,values))))
  else:
    for _ in range(150):
      Z=[z for z in cube if rng.randrange(3)] or [cube[0]]
      tables.append({z:F(rng.randrange(-6,7),3) for z in Z})
  for costs in tables:
    for eps in (F(0),F(1,3),F(1)):
      for delta in (F(0),F(1,3),F(1)):
        for update in (False,True):
          Q=[]; serial=0; calls=0; out=[]
          def call(fix):
            global serial,calls
            calls+=1
            members=[z for z in costs if all(z[i]==v for i,v in fix.items())]
            if not members: return
            mv=min(costs[z] for z in members)
            z=max((z for z in members if costs[z]<=mv+eps),key=lambda z:(costs[z],z))
            serial+=1
            heapq.heappush(Q,(costs[z]-eps,serial,fix,z))
          call({})
          U=costs[Q[0][3]]
          v=min(costs.values())
          while Q and Q[0][0]<=U+delta:
            lb,_,fix,z=heapq.heappop(Q)
            assert z not in out
            assert costs[z]<=v+delta+2*eps
            out.append(z)
            if update: U=min(U,costs[z])
            free=[i for i in range(n) if i not in fix]
            prefix=dict(fix)
            for i in free:
              child=dict(prefix);child[i]=1-z[i]
              call(child);prefix[i]=z[i]
            covered=[]
            for _,_,f,_ in Q:
              covered.extend(w for w in costs if all(w[i]==a for i,a in f.items()))
            assert len(covered)==len(set(covered))
            assert set(covered)==set(costs)-set(out)
          assert set(z for z in costs if costs[z]<=v+delta)<=set(out)
          assert calls<=1+n*len(out)
          runs+=1;extractions+=len(out);oracles+=calls
print('Near-optimal first moment:',countcases,'cases,',outcomes,'exact noise outcomes passed.')
print('Adversarial approximate enumeration:',runs,'runs,',extractions,'extractions,',oracles,'oracle calls passed.')
