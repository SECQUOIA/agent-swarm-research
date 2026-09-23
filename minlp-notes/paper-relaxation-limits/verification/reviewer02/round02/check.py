"""Independent exact quadratic enumeration; standard library only."""
from collections import Counter
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path
import json

OUT = Path(__file__).resolve().parent

def quadratic_values(n, edges, a):
    return [sum(w*s[i]*s[j] for (i,j),w in zip(edges,a))
            for tail in product((-1,1), repeat=max(0,n-1))
            for s in [(1,)+tail]]

def check_n(n):
    edges=list(combinations(range(n),2))
    free=[e for e in edges if e[0]>0]
    signs=[(1,)+s for s in product((-1,1),repeat=n-1)]
    chars=[[s[i]*s[j] for s in signs] for i,j in free]
    values=[sum(s[i]*s[j] for i,j in edges) for s in signs]
    hist=Counter()
    previous=0
    for k in range(1 << len(free)):
        gray=k^(k>>1)
        if k:
            changed=gray^previous
            edge=changed.bit_length()-1
            delta=-2 if gray&changed else 2
            values=[v+delta*c for v,c in zip(values,chars[edge])]
        qrange=max(values)-min(values)
        assert qrange%2==0
        hist[qrange//2]+=1
        previous=gray
    assert sum(hist.values()) == 1 << len(free)
    return {'n':n,'representatives':sum(hist.values()),'minimum_R':min(hist),
            'M':str(Fraction(len(edges),min(hist))),'histogram':dict(sorted(hist.items()))}

witnesses={3:[],4:[],5:[(1,2),(1,4),(2,3)],6:[(1,4),(1,5),(2,3),(2,5),(3,4)],
           7:[(1,2),(1,3),(1,6),(2,3),(2,5),(3,4)]}

def witness(n, negative):
    negative=set(negative)
    edges=list(combinations(range(n),2))
    a=[-1 if e in negative else 1 for e in edges]
    vals=quadratic_values(n,edges,a)
    best=Fraction(0)
    for count in range(2,n+1):
        for W in combinations(range(n),count):
            induced=list(combinations(range(count),2))
            b=[-1 if (W[i],W[j]) in negative else 1 for i,j in induced]
            q=quadratic_values(count,induced,b)
            best=max(best,Fraction(2*len(induced),max(q)-min(q)))
    return {'min_Q':min(vals),'max_Q':max(vals),'center':str(Fraction(2*len(edges),max(vals)-min(vals))), 'all_faces':str(best)}

# Independent definition of each rectangular sign norm, without polarization.
edges=list(combinations(range(4),2))
polarization_cases=0
for a in product((-1,0,1),repeat=len(edges)):
    vals=quadratic_values(4,edges,a)
    R=(max(vals)-min(vals))//2
    maxblock=0
    for mask in range(16):
        crossing=[(i,j,w) for (i,j),w in zip(edges,a) if bool(mask&(1<<i)) != bool(mask&(1<<j))]
        maxblock=max(maxblock,max(sum(w*s[i]*s[j] for i,j,w in crossing) for s in product((-1,1),repeat=4)))
    assert R==maxblock
    polarization_cases+=1
rows=[check_n(n) for n in range(2,8)]
assert [r['minimum_R'] for r in rows]==[1,2,4,4,5,8]
checks={str(n):witness(n,negative) for n,negative in witnesses.items()}
assert [(checks[str(n)]['min_Q'],checks[str(n)]['max_Q']) for n in range(3,8)]==[(-1,3),(-2,6),(-4,4),(-5,5),(-7,9)]
extended=witness(7,witnesses[6])
assert extended=={'min_Q':-9,'max_Q':11,'center':'21/10','all_faces':'3'}
# Replay the literal appendix program as a separate check of reproducibility.
root=OUT.parents[2]
source=(root/'process/snapshots/stage01-round02/sections/appendix-finite-signings.tex').read_text()
code=source.split('\\begin{verbatim}')[1].split('\\end{verbatim}')[0]
namespace={}
exec(compile(code,'printed-appendix','exec'),namespace)
assert namespace['result']==[r['minimum_R'] for r in rows]
result={'exact_arithmetic':True,'method':'Gray-code updates of direct quadratic values; integer sign norms; Fraction ratios',
        'enumeration':rows,'witnesses':checks,'extended_K6':extended,'polarization_cases':polarization_cases}
(OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
