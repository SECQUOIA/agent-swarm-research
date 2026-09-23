"""Independent exhaustive word masks, without the manuscript's nine-state DP."""
from itertools import product,permutations
from collections import Counter
from fractions import Fraction as Q

def run(N):
    words=list(product(range(3),repeat=N)); allmask=(1<<len(words))-1
    budgets={s:0 for s in range(N)}
    coord={}
    for wi,w in enumerate(words):
        changes=sum(a!=b for a,b in zip(w,w[1:]));budgets[changes]|=1<<wi
        counts=[0,0,0]
        for j,a in enumerate(w,1):
            counts[a]+=1
            for i,val in enumerate(counts):coord[j,i,val]=coord.get((j,i,val),0)|(1<<wi)
    cumulative=0
    for s in range(N):cumulative|=budgets[s];budgets[s]=cumulative
    floors_by_layer={}
    for j in range(1,N+1):
        options={}
        for f in product(range(j),repeat=3):
            if j-sum(f) not in (1,2):continue
            mask=allmask
            for i,v in enumerate(f):mask&=coord.get((j,i,v),0)|coord.get((j,i,v+1),0)
            options[f]=mask
        floors_by_layer[j]=options
    distribution=Counter();bad=[];total=0
    def extend(history,compatible):
        nonlocal total
        j=len(history)
        if j==N:
            assert compatible
            # Every bound takes both endpoint values in some full word: this
            # independently checks realizability by averaging all these words.
            for layer,f in enumerate(history,1):
                for i,v in enumerate(f):
                    assert compatible&coord.get((layer,i,v),0)
                    assert compatible&coord.get((layer,i,v+1),0)
            cost=next(s for s in range(N) if compatible&budgets[s])
            distribution[cost]+=1;total+=1
            if N==7 and cost==4:bad.append(history)
            return
        for f,mask in floors_by_layer[j+1].items():
            if all(0<=b-a<=1 for a,b in zip(history[-1],f)):
                extend(history+(f,),compatible&mask)
    extend(((0,0,0),),floors_by_layer[1][(0,0,0)])
    print(N,'cells:',total,'realizable histories; switch distribution',dict(sorted(distribution.items())))
    expected={5:{0:3,1:138,2:255},6:{0:3,1:255,2:1377,3:237},7:{0:3,1:414,2:4542,3:3891,4:6}}[N]
    assert distribution==expected
    if N==7:
        canonical=((0,0,0),(1,0,0),(1,1,0),(1,1,1),(2,1,1),(2,1,1),(2,1,2))
        orbit={tuple(tuple(f[p[i]] for i in range(3)) for f in canonical) for p in permutations(range(3))}
        assert set(bad)==orbit
        print('PASS exact six-history orbit; no cardinality-only inference')
for N in [5,6,7]:run(N)
print('PASS full-word coverage and coordinatewise strict realizability for every enumerated history')
