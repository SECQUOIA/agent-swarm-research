"""Independent exact planar-geometry checks of the Stage 3 formulas."""
from itertools import combinations, product
from fractions import Fraction as F
from pathlib import Path
import json

def vertices(intervals):
    (ls, us), (lt, ut), (lh, uh) = intervals
    rows = [(1,0,us),(-1,0,-ls),(0,1,ut),(0,-1,-lt),(1,1,uh),(-1,-1,-lh)]
    out = set()
    for (a,b,c), (d,e,f) in combinations(rows, 2):
        det = a*e-b*d
        if det:
            p = (F(c*e-b*f, det), F(a*f-c*d, det))
            if all(a*p[0]+b*p[1] <= c for a,b,c in rows):
                out.add(p)
    return hull(out)

def hull(points):
    points = sorted(set(points))
    if len(points) <= 1:
        return tuple(points)
    def cross(o,a,b):
        return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    def half(seq):
        result = []
        for p in seq:
            while len(result)>1 and cross(result[-2],result[-1],p)<=0:
                result.pop()
            result.append(p)
        return result
    return tuple(sorted(half(points)[:-1]+half(points[::-1])[:-1]))

def forms(p):
    return p[0], p[1], p[0]+p[1]

def inside(p, intervals):
    return all(lo <= value <= hi for value,(lo,hi) in zip(forms(p), intervals))

def bounds_formula(I):
    (ls,us),(lt,ut),(lh,uh)=I
    return ((max(ls,lh-ut),min(us,uh-lt)),
            (max(lt,lh-us),min(ut,uh-ls)),
            (max(lh,ls+lt),min(uh,us+ut)))

def choose(I):
    (ls,us),(lt,ut),(lh,uh)=I
    s=max(ls,lh-ut)
    return s,max(lt,lh-s)

intervals=list(combinations((-1,0,1),2))+[(i,i) for i in (-1,0,1)]
domains={}
checked=0
for I in product(intervals,repeat=3):
    vs=vertices(I)
    (ls,us),(lt,ut),(lh,uh)=I
    assert bool(vs)==(ls+lt<=uh and lh<=us+ut)
    checked+=1
    if vs:
        exact=tuple((min(forms(p)[i] for p in vs),max(forms(p)[i] for p in vs)) for i in range(3))
        assert bounds_formula(I)==exact
        assert inside(choose(I),I)
        domains[vs]=exact

pairs=recoveries=0
for (v1,I1),(v2,I2) in product(domains.items(),repeat=2):
    sums=[(a[0]+b[0],a[1]+b[1]) for a,b in product(v1,v2)]
    true=hull(sums)
    summed=tuple((a+c,b+d) for (a,b),(c,d) in zip(I1,I2))
    assert vertices(summed)==true
    pairs+=1
    center=tuple(sum(p[i] for p in true)/len(true) for i in range(2))
    for r in (*true,center):
        intersect=tuple((max(lo,value-hi2),min(hi,value-lo2))
                        for value,(lo,hi),(lo2,hi2) in zip(forms(r),I1,I2))
        first=choose(intersect)
        second=(r[0]-first[0],r[1]-first[1])
        assert inside(first,I1) and inside(second,I2)
        recoveries+=1

out={"status":"PASS","interval_patterns":checked,"distinct_domains":len(domains),
     "exact_minkowski_pairs":pairs,"exact_recoveries":recoveries,
     "includes_points_and_segments":True}
Path(__file__).with_name("check-output.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps(out))
