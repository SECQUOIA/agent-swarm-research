"""Independent reconstruction of the printed four-block LP and its certificates.

No project imports. Build rows from actual excluded sets, project raw variables
onto orbit identifiers, and check exact dual sums. Polynomial identities are
checked at degree+1 integer arguments; sign certificates by shifted coefficients.
"""
from pathlib import Path
from itertools import combinations
from collections import defaultdict
from math import comb
import json

P=Path(__file__).resolve().parent
data=json.loads((P/'relocated/verification/reference/certificates_general_four_block.json').read_text())

def program(n,pair,z):
    modes=range(n); S={0,1,2}; K=S|set(pair)|{z}
    qsets=[frozenset(q) for q in combinations(modes,2) if S.intersection(q)]
    events=[frozenset()]+qsets+[frozenset([i]) for i in range(3)]
    ids={}
    def var(kind,event=frozenset(),i=None):
        # Event indices precede allocation indices when identifying which
        # interchangeable label is equal to which excluded label.
        seen=[]
        def label(j):
            if j in K:return ('named',j)
            if j not in seen:seen.append(j)
            return ('anonymous',seen.index(j))
        eid=tuple(label(j) for j in sorted(event))
        key=(kind,eid,None if i is None else label(i))
        if key not in ids:ids[key]=len(ids)
        return ids[key]
    roots=[var('root',i=i) for i in modes]
    time={};alloc={}
    for event in events:
        time[event]=var('time',event)
        alloc[event]=[var('allocation',event,i) for i in modes]
    ineq=[];rhs=[];eq=[];ir={};er={}
    def add(terms,b,equality=False):
        row=defaultdict(int)
        for index,c in terms:row[index]+=c
        key=tuple(sorted((index,c) for index,c in row.items() if c))
        seen=er if equality else ir
        if key in seen:
            assert seen[key]==b
        else:
            seen[key]=b
            if equality:eq.append(key)
            else:ineq.append(key);rhs.append(b)
    for event in events:
        add([(time[event],-1)]+[(index,1) for index in alloc[event]],0,True)
        for j in modes:
            if j in event:continue
            for k in modes:
                if k not in event and k!=j:
                    add([(roots[j],1),(time[event],-1),(alloc[event][k],1)],-1)
    def order(a,b):
        for i in modes:add([(alloc[a][i],1),(alloc[b][i],-1)],0)
    for event in qsets:
        for i in sorted(S.intersection(event)):order(event,frozenset([i]))
        order(event,frozenset())
        if not event.intersection(pair):order(frozenset(),event)
    for i in range(3):
        order(frozenset([i]),frozenset())
        if i not in pair:order(frozenset(),frozenset([i]))
    c=[0]*len(ids)
    for event in qsets:c[time[event]]+=len(S.intersection(event))*(n-1)**2
    for i in range(3):c[time[frozenset([i])]]+=(n-1)**2
    for i in modes:
        if i!=z:c[roots[i]]-=3*n*n
    return ineq,rhs,eq,c

def check(n,cert,den,y,z):
    A,b,B,c=program(n,cert['pair'],cert['distinguished'])
    residual=[den*x for x in c]
    for rows,multipliers in [(A,y),(B,z)]:
        for j,v in multipliers.items():
            for i,a in rows[int(j)]:residual[i]-=v*a
    assert all(x==0 for x in residual),(n,cert['pair'],cert['distinguished'])
    assert sum(v*b[int(j)] for j,v in y.items())==den*3*n*n*(n-1)

def value(coeff,n):return sum(c*n**j for j,c in enumerate(coeff))
def translated(coeff,a):
    return [sum(coeff[j]*comb(j,h)*a**(j-h) for j in range(h,len(coeff))) for h in range(len(coeff))]

for cert in data['finite']:
    assert cert['denominator']>0 and all(v<=0 for v in cert['inequality'].values())
    check(cert['n'],cert,cert['denominator'],cert['inequality'],cert['equality'])
print('PASS: 179 finite certificates with independently reconstructed rows',flush=True)
evaluations=0
for cert in data['symbolic']:
    D=cert['denominator'];D0=cert['denominator_div_n_minus_one_squared']
    deg=max(len(D0)-1+3,max(len(v)-1 for v in cert['inequality'].values()),
            max(len(v)-1+1 for v in cert['equality'].values()))
    assert min(translated(D,23))>=0 and translated(D,23)[0]>0
    for v in cert['inequality'].values():assert min(translated([-c for c in v],23))>=0
    for n in range(9,9+max(deg+1,len(D))):
        assert value(D,n)==(n-1)**2*value(D0,n)
        check(n,cert,value(D0,n),{j:value(v,n) for j,v in cert['inequality'].items()},
              {j:value(v,n) for j,v in cert['equality'].items()})
        evaluations+=1
    # An additional point in the claimed domain checks the stabilized
    # quotient construction beyond the degree-determining dimensions.
    n=31
    check(n,cert,value(D0,n),{j:value(v,n) for j,v in cert['inequality'].items()},
          {j:value(v,n) for j,v in cert['equality'].items()})
    evaluations+=1
print('PASS: all 10 polynomial certificates,',evaluations,'exact matrix evaluations; degree bound and all shifted signs checked')
