"""Direct reviewer check of the printed five-product K4 witness."""
from fractions import Fraction as F
from pathlib import Path
import json

C = [[1,0,0], [0,1,0], [0,0,1], [1,1,0], [-1,0,1], [0,-1,-1]]
v = list(map(F, ['1/2','1/2','1/2','1/4','1/2','1/2']))
b = list(map(F, ['-5/4','-3/4','1/2','3/2']))
arcs = [(1,2),(1,3),(2,3),(0,1),(0,2),(0,3)]
assert [sum(v[e] if t == i else -v[e] if s == i else F(0)
            for e, (s,t) in enumerate(arcs)) for i in range(4)] == b
aggregate = list(map(F, ['1/6','1/24','1/8']))
checked = 0
for pi in range(-15,16):
    for qi in range(-15,16):
        p, q = F(pi,1536), F(qi,1536)
        if 2*p+q < 0:
            continue
        states = [[p,q,p], [q/2,-q/2,0],
                  [F(1,6)-p-q/2,F(1,24)-q/2,F(1,8)-p]]
        assert all(sum(t[i] for t in states) == aggregate[i] for i in range(3))
        for t in states:
            deviations = [sum(F(a)*z for a,z in zip(row,t)) for row in C]
            assert all(-v[e]/3 <= a <= (1-v[e])/3
                       for e,a in enumerate(deviations))
        checked += 1
result = {'k4_local_exact_grid_feasible_witnesses': checked,
          'k4_balances_verified': True,
          'source': 'Independent reviewer-written calculation of printed witness, no implementation import.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
