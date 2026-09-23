from itertools import combinations
from fractions import Fraction as F
import json
import sympy as s

edges = [(1,2),(2,3),(3,4),(1,3),(1,4),(2,4)]
A = s.zeros(4,6)
for k,(u,v) in enumerate(edges):
    A[u-1,k] = -1
    A[v-1,k] = 1
C = (-A[:3,:3].inv()*A[:3,3:]).col_join(s.eye(3))
assert A*C == s.zeros(4,3)
patterns = pivots = checked_rows = 0
for mask in range(64):
    obs = [k for k in range(6) if (mask>>k)&1]
    unobs = [k for k in range(6) if k not in obs]
    O = C[obs,:] if obs else s.zeros(0,3)
    rank = O.rank()
    assert 3-rank == len(unobs)-A[:,unobs].rank()
    patterns += 1
    for chosen in combinations(obs,rank):
        D = C[list(chosen),:] if chosen else s.zeros(0,3)
        if D.rank() != rank: continue
        for cols in combinations(range(3),rank):
            B = D[:,list(cols)] if cols else s.zeros(0,0)
            if B.det() == 0: continue
            assert abs(B.det()) == 1
            free = [k for k in range(3) if k not in cols]
            for row in range(6):
                W = C[row,list(cols)]*B.inv()
                R = C[row,free]-W*D[:,free]
                assert set(W) <= {s.Integer(-1),s.Integer(0),s.Integer(1)}
                assert set(R) <= {s.Integer(-1),s.Integer(0),s.Integer(1)}
                checked_rows += 1
            pivots += 1
x = {(1,2):F(1,2),(3,4):F(1,2),(2,3):F(1,4),(1,3):F(1,4),(1,4):F(1,4),(2,4):F(1,4)}
y = F(1,2)
z = F(1,5)
for e in [(1,3),(1,4),(2,4)]:
    assert 0 <= z <= y and z <= x[e] and z >= x[e]-(1-y)
assert 3*z-y == F(1,10)
print(json.dumps({'observation_patterns':patterns,'independent_row_and_pivot_choices':pivots,'unit_W_R_row_checks':checked_rows,'example_exact_violation':str(3*z-y),'status':'PASS'},indent=2))
