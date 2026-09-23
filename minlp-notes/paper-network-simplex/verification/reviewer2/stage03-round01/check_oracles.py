"""Independent integer enumeration of structured-domain hull tests and recovery."""
import itertools
import json
import random
from pathlib import Path
rng=random.Random(39127)

def add_points(domains, dim):
    out={(0,)*dim}
    for domain in domains: out={tuple(x+y for x,y in zip(a,b)) for a in out for b in domain}
    return out

def theta_points(lo,hi):
    return {(s,t) for s in range(lo[0],hi[0]+1) for t in range(lo[1],hi[1]+1) if lo[2]<=s+t<=hi[2]}

def supports(lo,hi):
    a=(max(lo[0],lo[2]-hi[1]), max(lo[1],lo[2]-hi[0]), max(lo[2],lo[0]+lo[1]))
    b=(min(hi[0],hi[2]-lo[1]), min(hi[1],hi[2]-lo[0]), min(hi[2],hi[0]+hi[1]))
    return a,b

th_cases=0; th_targets=0
for case in range(130):
    d=rng.randrange(1,5)
    intervals=[]; domains=[]
    for j in range(d):
        lo=tuple(rng.randrange(-3,3) for _ in range(3))
        hi=tuple(x+rng.randrange(4) for x in lo)
        pts=theta_points(lo,hi)
        feasible=all(lo[i]<=hi[i] for i in range(3)) and lo[0]+lo[1]<=hi[2] and lo[2]<=hi[0]+hi[1]
        assert feasible==bool(pts)
        if not pts: break
        a,b=supports(lo,hi)
        for i in range(3):
            values=[p[i] if i<2 else sum(p) for p in pts]
            assert a[i]==min(values) and b[i]==max(values)
        intervals.append((lo,hi)); domains.append(pts)
    if len(domains)!=d: continue
    total=add_points(domains,2)
    sup=[supports(*interval) for interval in intervals]
    a=tuple(sum(ab[0][i] for ab in sup) for i in range(3))
    b=tuple(sum(ab[1][i] for ab in sup) for i in range(3))
    for ss in range(a[0]-1,b[0]+2):
        for tt in range(a[1]-1,b[1]+2):
            forms=(ss,tt,ss+tt)
            assert (all(a[i]<=forms[i]<=b[i] for i in range(3))) == ((ss,tt) in total)
            th_targets+=1
    for target in total:
        r=target
        for j,(lo,hi) in enumerate(intervals):
            forms=(r[0],r[1],sum(r))
            aa=tuple(sum(ab[0][i] for ab in sup[j+1:]) for i in range(3))
            bb=tuple(sum(ab[1][i] for ab in sup[j+1:]) for i in range(3))
            ll=tuple(max(lo[i],forms[i]-bb[i]) for i in range(3))
            uu=tuple(min(hi[i],forms[i]-aa[i]) for i in range(3))
            ss=max(ll[0],ll[2]-uu[1]); tt=max(ll[1],ll[2]-ss)
            assert (ss,tt) in domains[j]
            r=(r[0]-ss,r[1]-tt)
        assert r==(0,0)
    th_cases+=1

par_cases=0; par_targets=0; infeasible_local=0
for case in range(110):
    k=rng.randrange(2,6); d=rng.randrange(1,4)
    cols=[]; domains=[]
    for j in range(d):
        lo=tuple(rng.randrange(-2,2) for _ in range(k))
        hi=tuple(x+rng.randrange(3) for x in lo)
        pts={p for p in itertools.product(*(range(lo[i],hi[i]+1) for i in range(k))) if sum(p)==0}
        local=sum(lo)<=0<=sum(hi)
        assert local==bool(pts)
        if not local:
            infeasible_local+=1; break
        cols.append((lo,hi)); domains.append(pts)
    if len(domains)!=d: continue
    total=add_points(domains,k)
    candidates=set(total)
    for _ in range(120):
        prefix=tuple(rng.randrange(-5,6) for i in range(k-1))
        candidates.add(prefix+(-sum(prefix),))
    subsets=[[i for i in range(k) if mask & (1<<i)] for mask in range(1<<k)]
    for target in candidates:
        conditions=True
        for S in subsets:
            complement=[i for i in range(k) if i not in S]
            rhs=sum(min(sum(hi[i] for i in S),-sum(lo[i] for i in complement)) for lo,hi in cols)
            if sum(target[i] for i in S)>rhs:
                conditions=False; break
        assert conditions==(target in total)
        if conditions:
            rr=[target[i]-sum(lo[i] for lo,hi in cols) for i in range(k)]
            cc=[-sum(lo) for lo,hi in cols]
            assert min(rr)>=0 and min(cc)>=0 and sum(rr)==sum(cc)
            for S in subsets:
                Csum=[sum(hi[i]-lo[i] for i in S) for lo,hi in cols]
                shifted_rhs=sum(min(Csum[j],cc[j]) for j in range(d))
                original_rhs=sum(min(sum(hi[i] for i in S),-sum(lo[i] for i in range(k) if i not in S)) for lo,hi in cols)
                assert original_rhs==shifted_rhs+sum(lo[i] for lo,hi in cols for i in S)
        par_targets+=1
    par_cases+=1
record={'status':'PASS','theta_nonempty_families':th_cases,'theta_integer_targets':th_targets,'parallel_nonempty_families':par_cases,'parallel_integer_targets':par_targets,'parallel_local_infeasibility_checks':infeasible_local,'note':'Exact integer enumeration supplements the general proofs; it is not a claim of exhaustive rational testing.'}
Path(__file__).with_name('result.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record))
