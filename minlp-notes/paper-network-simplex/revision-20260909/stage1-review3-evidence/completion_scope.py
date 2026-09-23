from fractions import Fraction as F
import json

# One vertex, one self-loop, b=0, capacity=1, m=2, O={(e,1)}.
# The observed label has no unobserved arc, hence its residual cycle rank is 0.
y = [F(1,3), F(1,3)]
lam = [1-sum(y), *y]  # global states 0,1,2
x, z1 = F(1,2), F(1,6)
completions = [[F(1,6), F(1,6), F(1,6)], [F(1,12), F(1,6), F(1,4)]]
for f in completions:
    assert sum(f) == x
    assert f[1] == z1
    assert all(0 <= fk <= lk for fk,lk in zip(f,lam))
    # Self-loop incidence is the zero column: every state balance holds.
assert completions[0][2] != completions[1][2]
print(json.dumps({'status':'PASS', 'residual_coordinate_count':0,
 'same_original_coordinates': {'x':str(x),'y':list(map(str,y)),'z_e1':str(z1)},
 'two_feasible_state_completions': [list(map(str,f)) for f in completions],
 'interpretation':'Locally observed label 1 is determined; unobserved label 2 is not.'}, indent=2))
