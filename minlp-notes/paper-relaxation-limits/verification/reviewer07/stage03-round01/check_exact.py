"""Independent finite checks; exhaustive rational arithmetic, no LP solver."""
from fractions import Fraction as F
from itertools import product, combinations
from math import prod
import json

counts = {}
# Check the displayed edge-cover/matching value identity on all costs in {0,1,3}
# on K4, including ties and zero-cost redundant cover edges.
edges = list(combinations(range(4), 2))
subsets = [tuple(i for i in range(6) if bits[i]) for bits in product((0, 1), repeat=6)]
covers = [s for s in subsets if set(v for i in s for v in edges[i]) == set(range(4))]
matchings = [s for s in subsets if len(set(v for i in s for v in edges[i])) == 2 * len(s)]
for costs in product((0, 1, 3), repeat=6):
    mu = [min(costs[i] for i,e in enumerate(edges) if v in e) for v in range(4)]
    a = min(sum(costs[i] for i in s) for s in covers)
    b = sum(mu) - max(sum(mu[edges[i][0]]+mu[edges[i][1]]-costs[i] for i in s) for s in matchings)
    assert a == b
counts['edge_cover_cost_vectors'] = 3**6

# Reconstruct the PARTITION vertex identity and threshold gap independently.
vertices = list(product((0,1), repeat=4))
yes = no = checks = 0
for raw in product(range(1,5), repeat=4):
    aa = [2*a for a in raw]
    total = sum(aa)
    ep = F(1, 16*total**3)
    base = 1+ep*total/2+ep**2*(F(total**2,8)-F(sum(a*a for a in aa),4))
    pi = [ep*a+ep**2*F(total*a-a*a,2) for a in aa]
    d0 = 1-ep**2*F(total**2,8)
    values = []
    partition = []
    for z in vertices:
        ss = sum(a*b for a,b in zip(aa,z))
        val = prod(1+ep*a*b for a,b in zip(aa,z))
        rem = val-1-ep*ss-ep**2*F(ss*ss-sum(a*a*b for a,b in zip(aa,z)),2)
        assert 0 <= rem <= ep**2/8
        tilted = val-sum(a*b for a,b in zip(pi,z))
        assert tilted == d0+ep**2*F((ss-total//2)**2,2)+rem
        values.append(tilted)
        if ss == total//2:
            complement = prod(1+ep*a*(1-b) for a,b in zip(aa,z))
            partition.append((val+complement)/2)
        else:
            assert val-(d0+ep**2/2+sum(a*b for a,b in zip(pi,z))) >= 0
        checks += 1
    if partition:
        yes += 1
        assert min(partition) <= base+ep**2/8
        assert min(values)+ep**2/32 < d0+ep**2/4
    else:
        no += 1
        assert min(values)-ep**2/32 > d0+ep**2/4
counts.update(partition_yes=yes, partition_no=no, partition_vertex_checks=checks)

# Fixed-ratio-type vertex oracle compared against full enumeration,
# with signed rational dual weights and unequal group sizes.
ratios = [F(3,2)]*3+[F(7,5)]*2
binary = list(product((0,1), repeat=5))
for weights in product((F(-3,2),F(0),F(5,3)), repeat=5):
    brute = min(prod(r**b for r,b in zip(ratios,z))-sum(w*b for w,b in zip(weights,z)) for z in binary)
    ww = [sorted(weights[:3], reverse=True), sorted(weights[3:], reverse=True)]
    by_counts = min(F(3,2)**a*F(7,5)**b-sum(ww[0][:a])-sum(ww[1][:b]) for a in range(4) for b in range(3))
    assert brute == by_counts
counts['ratio_type_weight_vectors'] = 3**5
print(json.dumps(counts, indent=2))
