"""Independent exact checks for the Stage 1 claim review; no manuscript imports."""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path

# Two parallel unit-capacity s-t arcs, unit demand, two explicit labels.
# Only product (arc 1, label 1) is retained; its unobserved complement is a tree.
states = []
for eps in (F(0), F(1, 12)):
    f1 = (F(1, 6), F(1, 6))
    f2 = (F(1, 6) + eps, F(1, 6) - eps)
    f0 = (F(1, 6) - eps, F(1, 6) + eps)
    for f in (f0, f1, f2):
        assert sum(f) == F(1, 3)
        assert all(0 <= a <= F(1, 3) for a in f)
    assert tuple(sum(f[i] for f in (f0, f1, f2)) for i in range(2)) == (F(1, 2),) * 2
    assert f1[0] == F(1, 6)
    states.append([[str(a) for a in f] for f in (f0, f1, f2)])
assert states[0][2] != states[1][2]

# Rank-three local witness, on exact rational points in its stated neighborhood.
C = ((1,0,0),(0,1,0),(0,0,1),(1,1,0),(-1,0,1),(0,-1,-1))
checked = 0
for p, q in product((F(-1,192),F(0),F(1,192)), repeat=2):
    if 2*p+q < 0:
        continue
    theta = ((p,q,p),(q/2,-q/2,F(0)),(F(1,6)-p-q/2,F(1,24)-q/2,F(1,8)-p))
    assert tuple(sum(t[i] for t in theta) for i in range(3)) == (F(1,6),F(1,24),F(1,8))
    for t in theta:
        for i, row in enumerate(C):
            a = sum(c*v for c,v in zip(row,t))
            lo, hi = (F(-1,12),F(1,4)) if i == 3 else (F(-1,6),F(1,6))
            assert lo <= a <= hi
    checked += 1

result = {"completion_counterexample": {"rho": 0, "distinct_refinements": states},
          "rank_three_exact_feasible_samples": checked}
Path(__file__).with_suffix('.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
