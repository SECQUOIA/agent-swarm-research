from itertools import product,permutations
from collections import Counter
# This checker never uses count-node edges or switch-cost DP. It intersects
# sets of full words satisfying the individual coordinate prefix inequalities.
for N in (5,6,7):
 words=list(product(range(3),repeat=N));prefixes=[];budgetmasks=[0]*N
 for idx,w in enumerate(words):
  c=[0,0,0];prefix=[]
  for p in w:c[p]+=1;prefix.append(tuple(c))
  prefixes.append(prefix)
  sw=sum(a!=b for a,b in zip(w,w[1:]));budgetmasks[sw]|=1<<idx
 masks={};exact={}
 for j in range(N):
  for i in range(3):
   for f in range(j+2):
    exact[j,i,f]=sum(1<<idx for idx,p in enumerate(prefixes) if p[j][i]==f)
   for f in range(j+1):masks[j,i,f]=exact[j,i,f]|exact[j,i,f+1]
 distribution=Counter();bad=[]
 def walk(history,valid):
  j=len(history);floor=history[-1]
  if j==N:
   assert valid
   for h,f in enumerate(history):
    for i in range(3):assert valid&exact[h,i,f[i]] and valid&exact[h,i,f[i]+1]
   minimum=next(s for s,m in enumerate(budgetmasks) if valid&m);distribution[minimum]+=1
   if minimum>=4:bad.append(history)
   return
  for d in product((0,1),repeat=3):
   new=tuple(x+y for x,y in zip(floor,d));sigma=j+1-sum(new)
   if sigma not in (1,2):continue
   newmask=valid
   for i in range(3):newmask&=masks[j,i,new[i]]
   walk(history+(new,),newmask)
 walk(((0,0,0),),(1<<len(words))-1)
 want={5:{0:3,1:138,2:255},6:{0:3,1:255,2:1377,3:237},7:{0:3,1:414,2:4542,3:3891,4:6}}[N]
 assert distribution==want
 if N==7:
  canonical=((0,0,0),(1,0,0),(1,1,0),(1,1,1),(2,1,1),(2,1,1),(2,1,2))
  orbit={tuple(tuple(f[i] for i in p) for f in canonical) for p in permutations(range(3))};assert set(bad)==orbit
  repairs=((1,2,0,0,0,2,2),(0,0,2,1,1,2,2),(0,0,1,1,2,2,0))
  for i,w in enumerate(repairs):
   prefix=prefixes[words.index(w)]
   failures=[(j,h) for j,(f,c) in enumerate(zip(canonical,prefix)) for h in range(3) if not f[h]<=c[h]<=f[h]+1]
   assert failures==[(i+1,i)] and sum(a!=b for a,b in zip(w,w[1:]))<=3
 print(N,dict(distribution),'full-word membership and coordinate-extremum realizability verified',flush=True)
