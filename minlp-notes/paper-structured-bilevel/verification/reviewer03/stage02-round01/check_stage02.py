"""Independent exact finite checks of stage 2 boundaries and recovery."""
from pathlib import Path
from itertools import combinations, product
import json
import sympy as s

HERE = Path(__file__).resolve().parent
x,z = s.symbols('x z', real=True)

def gezero(a):
    return bool(s.simplify(a) >= 0)

def vertices(G, h):
    """Original-coordinate vertex enumeration, including singular/empty cases."""
    ans=[]
    for ids in combinations(range(G.rows),G.cols):
        V=G[list(ids),:]
        if s.simplify(V.det()) == 0:
            continue
        y=V.inv()*h[list(ids),:]
        if all(gezero(v) for v in h-G*y) and y not in ans:
            ans.append(y)
    return ans

# Moving rows encode x*y=0 and a unit interval. The origin loses rank.
G=s.Matrix([[x],[-x],[1],[-1]])
h=s.Matrix([0,0,1,0])
assert vertices(G.subs(x,0),h)==[s.Matrix([1]),s.Matrix([0])]
assert vertices(G.subs(x,1),h)==[s.Matrix([0])]
assert vertices(s.Matrix([[1],[-1]]),s.Matrix([-1,0]))==[]
# Lower-dimensional singleton in ambient dimension two, with duplicate rows.
G2=s.Matrix([[1,0],[-1,0],[0,1],[0,-1],[2,0]])
h2=s.Matrix([1,-1,2,-2,2])
assert vertices(G2,h2)==[s.Matrix([1,2])]

# KKT basis for min (z-1)^2 with moving equality x*z=0.
K=s.Matrix([[2,x],[x,0]])
assert s.factor(K.det()) == -x*x
assert s.simplify((K.inv()*s.Matrix([2,0]))[0])==0
assert (s.Matrix([[2]]).inv()*s.Matrix([2]))[0]==1

# Exact stationary/global separation and upper-row tie semantics.
f=z*z*(1-z)**2
stationary=s.solve(s.diff(f,z),z)
assert stationary==[0,s.Rational(1,2),1]
assert [f.subs(z,a) for a in stationary]==[0,s.Rational(1,16),0]
ties=[0,1]
assert any(a<=s.Rational(1,2) for a in ties)
assert not all(a<=s.Rational(1,2) for a in ties)

# Common-field support tuples for three scalar blocks, aggregate dimension two.
# All data belong to Q(sqrt(2)); no independent field composition is used.
alpha=s.sqrt(2)
columns=[s.Matrix([1,alpha]),s.Matrix([alpha,-1]),s.Matrix([1,1])]
corners=list(product([s.Integer(0),s.Integer(1)],repeat=3))
def image(y):
    return sum((columns[i]*y[i] for i in range(3)),s.zeros(2,1))

# Finite direction proposals; scores and ties are compared exactly.
tuples=[]
for direction in product(range(-4,5),repeat=2):
    if direction==(0,0):
        continue
    lam=s.Matrix(direction)
    # First maximizer for each scalar block. Zero score chooses vertex zero.
    y=tuple(s.Integer(1) if gezero(lam.dot(a)) and lam.dot(a)!=0 else s.Integer(0)
            for a in columns)
    if y not in tuples:
        tuples.append(y)
images=[image(y) for y in tuples]

def recover(t):
    for size in range(1,4):
        for ids in combinations(range(len(images)),size):
            mat=s.Matrix.hstack(*[images[j].col_join(s.ones(1,1)) for j in ids])
            if mat.rank()!=size:
                continue
            for rows in combinations(range(3),size):
                square=mat[list(rows),:]
                if square.det()==0:
                    continue
                target=t.col_join(s.ones(1,1))
                weights=s.simplify(square.inv()*target[list(rows),:])
                if s.simplify(mat*weights-target)==s.zeros(3,1) and all(map(gezero,weights)):
                    y=[s.simplify(sum(weights[a]*tuples[j][b] for a,j in enumerate(ids)))
                       for b in range(3)]
                    assert all(gezero(a) and gezero(1-a) for a in y)
                    assert s.simplify(image(y)-t)==s.zeros(2,1)
                    for a in list(weights)+y:
                        s.polys.numberfields.to_number_field(a,alpha)
                    return ids,weights,y
                break
    raise AssertionError('No retained support combination for target')

# Distinct oracle: the full Cartesian image is used only for this tiny check.
# If each original corner lies in the retained hull, the complete polytopes agree.
for corner in corners:
    recover(image(corner))
target=image((alpha/2,s.Rational(1,3),s.Rational(2,5)))
ids,weights,recovered=recover(target)
summary={
    'moving_rank_and_empty_fibers':'passed',
    'lower_dimensional_duplicate_rows':'passed',
    'stationary_global_and_universal_upper_semantics':'passed',
    'support_tuples':len(tuples),
    'cartesian_corners_checked':len(corners),
    'recovery_weights':[str(a) for a in weights],
    'recovered_blocks':[str(a) for a in recovered],
    'common_field':'Q(sqrt(2))',
    'limits':'Finite exact diagnostics; no general sign enumeration or quantifier elimination implementation.'
}
(HERE/'checks.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
