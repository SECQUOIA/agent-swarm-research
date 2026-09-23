"""Independent exact finite checks. No manuscript or author-checker imports."""
from fractions import Fraction as Q
from itertools import product
from math import comb, factorial
from pathlib import Path
import hashlib
import json

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
SNAP = ROOT / 'process/snapshots/stage04-round01'
counts = {}

# Arbitrary product sets matter only through membership of 0,p,1 for this
# finite witness family. A zero mask is allowed: the actual set can be
# nonempty while missing all three witness values.
domains = 0
for n in range(2, 5):
    words = list(product(range(3), repeat=n))
    for k in range(n):
        for m in range(1, n-k+1):
            z = n-k-m
            witnesses = [w for w in words if w.count(2)==k and w.count(1)==m]
            total = factorial(n)//factorial(k)//factorial(m)//factorial(z)
            assert len(witnesses)==total
            base = Q(max(n-k,n-z), n)
            for masks in product(range(8), repeat=n):
                a = sum(not (mask & 1) for mask in masks)
                d = sum(not (mask & 4) for mask in masks)
                restricted = sum((mask & 5)!=5 for mask in masks)
                contained = sum(all(mask & (1 << v) for mask,v in zip(masks,w)) for w in witnesses)
                fraction = Q(contained,total)
                assert fraction <= Q(n-z,n)**a
                assert fraction <= Q(n-k,n)**d
                # Squaring avoids irrational half-exponents, with no loss
                # since both sides of the desired bound are nonnegative.
                assert fraction*fraction <= base**restricted
                domains += 1
counts['product_domain_membership_cases'] = domains

def chord_lp(box, demand):
    """Exact linear resource-allocation optimum by sorted marginal cost."""
    if sum(a for a,b in box)>demand or sum(b for a,b in box)<demand:
        return None
    remaining = demand-sum(a for a,b in box)
    value = sum(a*(1-a) for a,b in box)
    for slope,width in sorted((1-a-b,b-a) for a,b in box):
        used = min(width, remaining)
        value += slope*used
        remaining -= used
    assert remaining==0
    return value

midpoint_leaves = positive_leaves = tree_cases = 0
for n in range(2,11):
    for k in range(n):
        demand = k+Q(1,2)
        def midpoint(prefix,c,d):
            global midpoint_leaves
            if c==k+1 or d==n-k:
                value=chord_lp(prefix+[(Q(0),Q(1))]*(n-len(prefix)), demand)
                assert value is None or value>=Q(1,4)
                midpoint_leaves += 1
                return 1,1
            assert len(prefix)<n
            nl,ll=midpoint(prefix+[(Q(0),Q(1,2))],c,d+1)
            nr,lr=midpoint(prefix+[(Q(1,2),Q(1))],c+1,d)
            return 1+nl+nr,ll+lr
        nodes,leaves=midpoint([],0,0)
        assert leaves==comb(n+1,k+1) and nodes==2*leaves-1
        tree_cases += 1
        if n>8:
            continue
        alpha=Q(1,3)
        target=alpha*(1-alpha)
        def positive(prefix):
            global positive_leaves
            if len(prefix)==n:
                value=chord_lp(prefix,demand)
                assert value is None or value>target
                positive_leaves += 1
                return 1,1
            middle=prefix+[(alpha,1-alpha)]+[(Q(0),Q(1))]*(n-len(prefix)-1)
            value=chord_lp(middle,demand)
            assert value is None or value>=target
            positive_leaves += 1
            nl,ll=positive(prefix+[(Q(0),alpha)])
            nr,lr=positive(prefix+[(1-alpha,Q(1))])
            # Current root and intermediate upper child and middle leaf.
            return 3+nl+nr,1+ll+lr
        nodes,leaves=positive([])
        assert nodes==2**(n+2)-3 and leaves==2**(n+1)-1
        tree_cases += 1
counts.update(tree_cases=tree_cases, midpoint_leaves_checked=midpoint_leaves,
              positive_tolerance_leaves_checked=positive_leaves)

# All vertex objective-value types of each tested tolerance slab: cube
# vertices inside the slab and slab-boundary intersections with cube edges.
# By objective symmetry the potentially fractional coordinate can be last.
tolerance_cases = tolerance_vertices = 0
for n in range(2,8):
    for k in range(n):
        for delta in [Q(0),Q(1,16),Q(1,4),Q(7,16),Q(1,2),Q(3,4)]:
            lower,upper=k+Q(1,2)-delta,k+Q(1,2)+delta
            values=[]
            for bits in product([Q(0),Q(1)],repeat=n):
                if lower<=sum(bits)<=upper:
                    values.append(Q(0))
            for bits in product([Q(0),Q(1)],repeat=n-1):
                for boundary in [lower,upper]:
                    v=boundary-sum(bits)
                    if 0<=v<=1:
                        values.append(v*(1-v))
            assert values
            expected=Q(1,4)-delta*delta if delta<Q(1,2) else Q(0)
            assert min(values)==expected
            tolerance_vertices += len(values)
            tolerance_cases += 1
counts.update(tolerance_cases=tolerance_cases,tolerance_vertex_values=tolerance_vertices)

# Exact integer boundaries of q_r; sufficiently many endpoint witnesses
# remain even if exclusions are concentrated in only one class.
order_cases=0
for k,m,z,r in product(range(1,13),range(1,6),range(1,13),range(1,8)):
    for epsilon in [Q(0),Q(1,8),Q(7,32)]:
        q=min(k-2*r+2,z-2*r+2,m*(Q(1,2)-2*epsilon))
        for hrem in range(k+1):
            if hrem>=q:
                continue
            assert k-hrem>=2*r-1 and z-hrem>=2*r-1
            assert k+m+z-hrem>=2*r
            assert hrem*Q(1,2*m)*(1-Q(1,2*m))<Q(1,4)-epsilon
            order_cases += 1
counts['order_threshold_cases']=order_cases
tau=Q(1,4)-Q(1,32)*(Q(5,2)+Q(1,4))-Q(1,32)
assert tau==Q(17,128) and 2*tau/6==Q(17,384)

manifest=json.loads((SNAP/'manifest.json').read_text())
checked=0
for name in ['macros.tex','sections/01-foundations.tex',
             'sections/09-cardinality-spatial.tex','sections/10-cardinality-preordering.tex',
             'sections/11-coordinate-domains-lifts.tex','sections/12-relative-blocks-cuts.tex']:
    assert hashlib.sha256((SNAP/name).read_bytes()).hexdigest()==manifest[name]
    checked += 1
counts['frozen_source_hashes_verified']=checked
report={'status':'PASS','arithmetic':'exact rational/integer', 'counts':counts,
        'limits':'Finite cases check counting, upper certificates, tolerance boundaries and order thresholds; they do not prove the universal moment, graph-lift or tensor theorems.'}
(OUT/'independent-results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
