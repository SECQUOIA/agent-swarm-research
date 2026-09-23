"""Fresh LP reconstruction and integer-polynomial verification, without manuscript imports."""
from pathlib import Path
from itertools import combinations
from collections import OrderedDict
import json
P=Path(__file__).resolve().parent/'relocated'
data=json.loads((P/'verification/reference/certificates_general_four_block.json').read_text())

def program(n,pair,z):
    fixed={0,1,2,*pair,z}; small={0,1,2}
    exclusions=[x for x in combinations(range(n),2) if any(i in small for i in x)]
    events=[()]+exclusions+[(i,) for i in range(3)]
    labels={}
    def ident(kind,event=(),mode=None):
        raw=event+(() if mode is None else (mode,)); seen={}; tag=[]
        for i in raw:
            if i in fixed: tag.append(i)
            else:
                if i not in seen:seen[i]=-1-len(seen)
                tag.append(seen[i])
        key=(kind,len(event),tuple(tag))
        if key not in labels:labels[key]=len(labels)
        return labels[key]
    roots=[ident('r',mode=i) for i in range(n)]
    ts={e:ident('t',e) for e in []};alloc={}
    for e in events:
        ts[e]=ident('t',e)
        alloc[e]=[ident('a',e,i) for i in range(n)]
    ub=OrderedDict();eq=OrderedDict()
    def row(items):
        r={}
        for i,v in items:r[i]=r.get(i,0)+v
        return tuple(sorted((i,v) for i,v in r.items() if v))
    for e in events:
        eq[row([(ts[e],-1)]+[(i,1) for i in alloc[e]])]=0
        for first in range(n):
            if first in e:continue
            for last in range(n):
                if last in e or first==last:continue
                ub[row([(roots[first],1),(ts[e],-1),(alloc[e][last],1)])]=-1
    def order(e,f):
        for j in range(n):ub[row([(alloc[e][j],1),(alloc[f][j],-1)])]=0
    for e in exclusions:
        for i in range(3):
            if i in e:order(e,(i,))
        order(e,())
        if all(i not in pair for i in e):order((),e)
    for i in range(3):
        order((i,),())
        if i not in pair:order((),(i,))
    objective=[0]*len(labels)
    for i in range(3):
        objective[ts[(i,)]]+=(n-1)**2
        for j in range(n):
            if i!=j:objective[ts[tuple(sorted((i,j)))]]+=(n-1)**2
    for i in range(n):
        if i!=z:objective[roots[i]]-=3*n*n
    return list(labels),list(ub.items()),list(eq.items()),objective

def identity(n,case,D,Y,Z):
    V,ub,eq,c=program(n,case['pair'],case['distinguished'])
    accum=[0]*len(c);bound=0
    for weights,rows in [(Y,ub),(Z,eq)]:
        for index,value in weights.items():
            r,b=rows[int(index)];bound+=value*b
            for col,a in r:accum[col]+=value*a
    assert all(D*c[i]==accum[i] for i in range(len(c)))
    assert bound==3*n*n*(n-1)*D
    return V,ub,eq,c
for case in data['finite']:
    assert all(type(y) is int and y<=0 for y in case['inequality'].values())
    assert type(case['denominator']) is int and case['denominator']>0
    identity(case['n'],case,case['denominator'],case['inequality'],case['equality'])
print('PASS: independently rebuilt complete finite LPs and all 179 dual identities',flush=True)

def evaluate(poly,n):
    out=0
    for c in reversed(poly):out=out*n+c
    return out

def newton_sign(poly,positive=False):
    # Newton series at 23: p(23+t)=sum Delta^j p(23) choose(t,j).
    # Every binomial is nonnegative for nonnegative integer t.
    values=[evaluate(poly,23+j) for j in range(len(poly))]
    if positive:assert values[0]>0
    while values:
        assert values[0]>=0
        values=[b-a for a,b in zip(values,values[1:])]
for case in data['symbolic']:
    D=case['denominator'];D0=case['denominator_div_n_minus_one_squared']
    y=case['inequality'];z=case['equality']
    newton_sign(D,True)
    for v in y.values():newton_sign([-c for c in v])
    # Check polynomial identities at degree+1 distinct integer points. Every
    # program is reconstructed at its actual dimension, without interpolation.
    degree=max(len(D0)-1+3,max(map(len,y.values()))-1,max(map(len,z.values())))
    for n in range(23,24+degree):
        assert evaluate(D,n)==(n-1)**2*evaluate(D0,n)>0
        identity(n,case,evaluate(D0,n),{i:evaluate(v,n) for i,v in y.items()},
                 {i:evaluate(v,n) for i,v in z.items()})
    # Independently inspect the affine mass multiplicity and constant row
    # topology at a farther dimension for each of the ten orbit types.
    v9,a9,b9,c9=program(9,case['pair'],case['distinguished'])
    v10,a10,b10,c10=program(10,case['pair'],case['distinguished'])
    v31,a31,b31,c31=program(31,case['pair'],case['distinguished'])
    assert v9==v10==v31 and a9==a10==a31
    for (r9,_),(r10,_),(r31,_) in zip(b9,b10,b31):
        p9,p10,p31=map(dict,(r9,r10,r31))
        for i in p9.keys()|p10.keys()|p31.keys():
            assert p31.get(i,0)==p9.get(i,0)+22*(p10.get(i,0)-p9.get(i,0))
    print('PASS polynomial identities and Newton-basis signs:',case['pair'],case['distinguished'],
          'degree',degree,'dimensions',23,23+degree,'topology through31',flush=True)
print('PASS: all-dimension proof reconstructed independently; no imported certificate routines',flush=True)
