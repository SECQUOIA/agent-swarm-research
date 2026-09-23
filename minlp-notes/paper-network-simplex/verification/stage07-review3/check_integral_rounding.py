"""Independent exact cycle rounding of rational network flows; no LP or author code."""
from fractions import Fraction as F
from itertools import product
from collections import defaultdict,deque
from pathlib import Path
import random,json
rng=random.Random(730921)
counts=defaultdict(int)
def balance(arcs,x,n):
 b=[F(0)]*n
 for (a,c),v in zip(arcs,x):b[a]-=v;b[c]+=v
 return tuple(b)
def cycle(arcs,x,n):
 fractional=[e for e,v in enumerate(x) if v.denominator!=1]
 tree=[[] for _ in range(n)]
 for e in fractional:
  a,b=arcs[e]
  if a==b:return {e:1}
  parent={b:None};queue=deque([b])
  while queue and a not in parent:
   v=queue.popleft()
   for other,k,sign in tree[v]:
    if other not in parent:parent[other]=(v,k,sign);queue.append(other)
  if a in parent:
   # Added arc a->b followed by the tree route b->a.
   out={e:1};cur=a
   while cur!=b:
    prev,k,sign=parent[cur];out[k]=sign;cur=prev
   assert balance(arcs,[F(out.get(k,0)) for k in range(len(arcs))],n)==(0,)*n
   return out
  tree[a].append((b,e,1));tree[b].append((a,e,-1))
 raise AssertionError('Nonempty fractional support had no cycle')
def rounded(arcs,u,b,x):
 memo={}
 def visit(t):
  if t in memo:return memo[t]
  assert balance(arcs,t,len(b))==b and all(0<=v<=cap for v,cap in zip(t,u))
  if all(v.denominator==1 for v in t):return {t:F(1)}
  direction=cycle(arcs,t,len(b));counts['fractional_cycle_splits']+=1
  plus=[];minus=[]
  for e,s in direction.items():
   down=t[e]-t[e].numerator//t[e].denominator;up=1-down
   plus.append(up if s==1 else down);minus.append(down if s==1 else up)
  ep,em=min(plus),min(minus);assert ep>0 and em>0
  hi=tuple(v+ep*direction.get(e,0) for e,v in enumerate(t));lo=tuple(v-em*direction.get(e,0) for e,v in enumerate(t))
  assert sum(v.denominator!=1 for v in hi)<sum(v.denominator!=1 for v in t)
  assert sum(v.denominator!=1 for v in lo)<sum(v.denominator!=1 for v in t)
  answer=defaultdict(F)
  for v,w in visit(hi).items():answer[v]+=em/(ep+em)*w
  for v,w in visit(lo).items():answer[v]+=ep/(ep+em)*w
  assert sum(answer.values())==1
  assert all(sum(w*v[e] for v,w in answer.items())==t[e] for e in range(len(arcs)))
  memo[t]=dict(answer);return memo[t]
 return visit(x)
for k in range(48):
 n=2+k%3;arcs=[(rng.randrange(n),rng.randrange(n)) for _ in range(5+k%3)]
 u=[rng.randrange(3) for _ in arcs];reference=[rng.randrange(c+1) for c in u];b=balance(arcs,reference,n)
 feasible=[tuple(F(v) for v in x) for x in product(*(range(c+1) for c in u)) if balance(arcs,x,n)==b]
 assert feasible
 for m in (0,2,4):
  raw=[rng.randrange(4) for _ in range(m+1)];raw[-1]+=1;weights=[F(a,sum(raw)) for a in raw]
  states=[];refined=[]
  for j in range(m+1):
   choices=[rng.choice(feasible) for _ in range(3)]
   x=tuple(sum(F(t+1,6)*v[e] for t,v in enumerate(choices)) for e in range(len(arcs)))
   result=rounded(arcs,u,b,x);states.append(x)
   refined.extend((weights[j]*w,j,v) for v,w in result.items() if weights[j]*w)
   counts['state_flows_rounded']+=1
  obs=[(e,j) for e in range(len(arcs)) for j in range(m) if rng.randrange(2)]
  assert sum(w for w,_,_ in refined)==1
  for e in range(len(arcs)):assert sum(weights[j]*states[j][e] for j in range(m+1))==sum(w*v[e] for w,_,v in refined)
  for e,j in obs:assert weights[j]*states[j][e]==sum(w*v[e] for w,s,v in refined if s==j)
  for j in range(m):assert weights[j]==sum(w for w,s,_ in refined if s==j)
  counts['integral_graph_refinements']+=1
 counts['graphs']+=1
# Explicit parallel, antiparallel, and loop fractional cycles.
for arcs,u,b,x in [([(0,1),(0,1)],[1,1],(-1,1),(F(1,2),F(1,2))), ([(0,1),(1,0)],[2,2],(0,0),(F(3,2),F(3,2))), ([(0,0)],[2],(0,),(F(2,3),))]:
 result=rounded(arcs,u,tuple(map(F,b)),x);assert len(result)>1;counts['explicit_fractional_cycle_cases']+=1
out=dict(counts);out['status']='PASS';Path('paper-network-simplex/verification/stage07-review3/integral-rounding.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
