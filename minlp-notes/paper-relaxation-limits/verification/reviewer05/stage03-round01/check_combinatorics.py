from fractions import Fraction as Q
from itertools import product, combinations, permutations
from functools import lru_cache
from collections import Counter
from pathlib import Path
import json

out={}
# Exact complete small graph check; reject only after exploring all width-two eliminations.
@lru_cache(None)
def width2(adj):
    if not any(adj): return True
    for v,nb in enumerate(adj):
        if nb and nb.bit_count()<=2:
            a=list(adj); ns=[u for u in range(len(a)) if nb>>u&1]
            for u in ns:
                a[u]=(a[u]&~(1<<v)) | (nb & ~(1<<u))
            a[v]=0
            if width2(tuple(a)):return True
    return False
accepted=0
for mask in range(1<<12):
    adj=[0]*7
    for v in range(3):
        for f in range(4):
            if mask>>(4*v+f)&1:
                adj[v]|=1<<(3+f);adj[3+f]|=1<<v
    if not width2(tuple(adj)):continue
    accepted+=1
    bad=[]
    # Only odd-factor simple cycles possible with three variable vertices are C6.
    for fs in combinations(range(4),3):
        if any(all((adj[v]>>(3+fp[v])&1) and (adj[(v+1)%3]>>(3+fp[v])&1) for v in range(3)) for fp in permutations(fs)):
            bad.append(fs)
    assert any(all(len({cs[f] for f in fs})>1 for fs in bad) for cs in product(range(2),repeat=4))
out['three_variables_four_factors']={'graphs':4096,'width_at_most_two':accepted,'all_cycle_two_coloring':'PASS'}
# Resource profiles, telescoping and pointwise equality beyond simplified b>=L regime.
cases=0
for b in range(2,13):
 for L in range(2,31):
    w=[Q(b-1,b**(l+1)) for l in range(L)]+[Q(1,b**L)]
    M=lambda q:Q((L-q)*(b-1)+b,b**q)
    s=next(s for s in range(1,L) if M(s+1)<=1<=M(s))
    mix=(1-M(s+1))/(M(s)-M(s+1))
    val=Q(0);count=Q(0)
    for q,pq in [(s,mix),(s+1,1-mix)]:
      prof=[b**(l-q+1) if l>=q else 0 for l in range(L+1)]
      assert sum(w[l]*prof[l] for l in range(L+1))==M(q)
      for l,R in enumerate(prof):
        score=sum(min(b**j,R) for j in range(1,l+1))
        assert score==s*R+sum(b**j for j in range(1,l-s+1))
        val+=pq*w[l]*score;count+=pq*w[l]*R
    assert count==1 and val==s+Q(L-s,b**s)
    assert sum(M(q) for q in range(s+1,L+1))==Q(L-s,b**s)
    cases+=1
out['radix_resource_profiles']=cases
# All counts and prefix-hit properties at manageable radix dimensions.
cases=0
for b,L in [(2,2),(2,5),(3,3),(4,3),(5,3),(6,2)]:
 words=list(product(range(b),repeat=L));order=sorted(words,key=lambda w:w[::-1])
 for R in range(len(words)+1):
    for j in range(1,L+1):
      assert len({w[:j] for w in order[:R]})==min(b**j,R)
    cases+=1
out['digit_reversal_counts']=cases
# Explicit leaf-first / descending-factor elimination count.
counts=[]
for b,L in [(2,2),(3,3),(4,3),(4,4),(5,3)]:
    leaves=list(product(range(b),repeat=L));ad={}
    def edge(a,c):ad.setdefault(a,set()).add(c);ad.setdefault(c,set()).add(a)
    for leaf in leaves:
      for j in range(1,L+1):
        f=('f',leaf[:j]);edge(('z',leaf),f);edge(('a',j),f)
    order=[('z',w) for w in leaves]+[('f',w) for j in range(L,0,-1) for w in product(range(b),repeat=j)]+[('a',j) for j in range(1,L+1)]
    width=0
    for node in order:
      nb=ad.pop(node);width=max(width,len(nb))
      for v in nb:ad[v].remove(node);ad[v].update(nb-{v})
    assert width==L
    counts.append([b,L,len(order),width])
out['radix_elimination_widths']=counts
# Every subset on odd cycles; matching/complement marginals and coverage baseline.
cases=0
for l in [3,5,7,9,11,13]:
    laws=[]
    for missed in range(l):
       matching={(missed+1+2*k)%l for k in range((l-1)//2)}
       laws.extend([matching,set(range(l))-matching])
    assert all(sum(i in J for J in laws)==l for i in range(l))
    assert all(sum(v in J or (v-1)%l in J for J in laws)==2*l-1 for v in range(l))
    for bits in product(range(2),repeat=l):
       coverage=sum(bits[v] or bits[(v-1)%l] for v in range(l))
       assert coverage<=sum(bits)+(l-1)//2
       cases+=1
out['odd_cycle_subsets']=cases
payoffs=Counter()
for a,b,c,d,e,f in product(range(2),repeat=6):
    payoffs[((a==b) and (e==f),(a!=b) and (c==d),(c!=d) and (e!=f))]+=1
assert len(payoffs)==4 and set(payoffs.values())=={16} and all(sum(p)<=1 for p in payoffs)
out['parity_payoff_counts']={str(p):v for p,v in payoffs.items()}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
