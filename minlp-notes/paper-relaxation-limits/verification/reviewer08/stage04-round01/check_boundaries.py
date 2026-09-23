"""Independent exact finite falsification checks; no manuscript imports."""
from fractions import Fraction as Q
from math import comb
from pathlib import Path
import json

counts = {"endpoint_domains": 0, "restriction_parameters": 0,
          "midpoint_trees": 0, "relative_parameters": 0}

# Enumerate endpoint exclusion masks, including overlap, empty endpoint
# classes, and impossible avoidance events. Square the claimed probability
# bound so every comparison is rational and no floating root is taken.
for n in range(2, 7):
    masks = range(1 << n)
    for k in range(n):
        for z in range(n - k):
            m = n - k - z
            witnesses = [(h, zz) for h in masks if h.bit_count() == k
                         for zz in masks if zz.bit_count() == z and not h & zz]
            base = max(Q(n-k, n), Q(n-z, n))
            for a in masks:
                for d in masks:
                    accepted = sum(not (zz & a or h & d) for h, zz in witnesses)
                    fraction = Q(accepted, len(witnesses))
                    assert fraction**2 <= base**((a | d).bit_count())
                    counts["endpoint_domains"] += 1

# All removal-type triples within a finite parameter range, at zero,
# interior, and near-zero positive objective targets. These check the
# strict below-target argument and the integer +2 in q_r.
for n in range(3, 19):
    for k in range(1, n-1):
        for z in range(1, n-k):
            m = n-k-z
            for r in range(1, 11):
                for eps in (Q(0), Q(1,8), Q(255,1024)):
                    qr = min(k-2*r+2, z-2*r+2, m*(Q(1,2)-2*eps))
                    if qr <= 0:
                        continue
                    for rh in range(k+1):
                        for rm in range(m+1):
                            for rz in range(z+1):
                                removed = rh+rm+rz
                                if removed >= qr:
                                    continue
                                s = n-removed
                                p = Q(1,2*m)
                                t = k-rh+p*(m-rm)
                                assert s >= 2*r and t >= 2*r-1 and s-t >= 2*r-1
                                assert rm*p*(1-p) < Q(1,4)-eps
                                counts["restriction_parameters"] += 1

def leaves(a, b, memo={}):
    if not a or not b:
        return 1
    if (a,b) not in memo:
        memo[a,b] = leaves(a-1,b)+leaves(a,b-1)
    return memo[a,b]

for n in range(2, 101):
    for k in range(n):
        assert leaves(k+1,n-k) == comb(n+1,k+1)
        counts["midpoint_trees"] += 1

for r in range(1, 13):
    for t in range(2*r-1, 2*r+10):
        q0 = t-2*r+2
        eta = Q(1,32)
        theta = (Q(1,4)-eta)/(2*(Q(t)+Q(3,4)))
        tau = Q(1,4)-theta*(Q(t)+Q(3,4))-eta
        assert tau > 0 and 1 <= q0 <= t
        assert q0*tau/(3*t) > 0
        counts["relative_parameters"] += 1
assert Q(1,4)-Q(1,32)*Q(11,4)-Q(1,32) == Q(17,128)
assert Q(2,6)*Q(17,128) == Q(17,384)

result = {"status": "PASS", "arithmetic": "exact integers and rational fractions",
          "counts": counts,
          "limits": "Finite boundary and count checks; not a proof of universal positivity or graph transfer."}
Path(__file__).with_suffix('.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2))
