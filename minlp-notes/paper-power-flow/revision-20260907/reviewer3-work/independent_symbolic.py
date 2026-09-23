"""Independent reviewer algebra and exact linear-system checks; no manuscript edits."""
from pathlib import Path
import random
import sympy as S
from importlib.util import spec_from_file_location, module_from_spec
R=S.Rational
x,y,z,a,b=S.symbols('x y z a b')
# Eliminate shifted product in the order of the published equations.
m=(1+x)*(1+y)
f=m+R(1,2)
g=f-(y+R(3,4))
h=g+R(3,4)
assert S.expand((z+R(3,4))+(x+R(3,4))-h)==z-x*y
# Reconstruct the square chain independently and verify rational identity globally.
b=a+R(1,2)
bp=1/b
ap=1/a
c=ap+R(1,2)
d=c-R(2,3)
e=d+R(1,2)
f=e-bp
g=2*f
h=g-R(2,3)
i=1/h
j=i-R(1,2)
k=j+R(3,4)
l=b/2
o=k-l
assert S.cancel(h-1/(a*(a+R(1,2))))==0
assert S.simplify(o-a*a)==0
# A symbolic three-square product identity.
r=(x+y)/2
u=r*r+R(1,2)
d=(x*x+y*y+1)/4
assert S.expand(2*(u-d)-R(1,2)-x*y)==0
print('Symbolic elimination: shifted product, reciprocal square, three-square product valid.')
# Exact Gaussian rank solves independently test graph propagation on larger graphs.
p=Path(__file__).resolve().parents[1]/'stage2-snapshot/checks/check_ac_exact.py'
spec=spec_from_file_location('checked_ac',p)
ac=module_from_spec(spec)
spec.loader.exec_module(ac)
rng=random.Random(3072026)
solvable=0
for trial in range(150):
    n=rng.randrange(1,10)
    es=[]
    potential=[rng.randrange(-2,3) for _ in range(n)]
    for j in range(n):
        for i in range(j):
            if rng.random()<R(1,3):
                shift=(potential[j]-potential[i]) if trial%2==0 else rng.randrange(-1,2)
                es.append((i,j,shift))
    A=S.zeros(len(es),n)
    rhs=S.zeros(len(es),1)
    for row,(i,j,k) in enumerate(es):
        A[row,i]=-1;A[row,j]=1;rhs[row,0]=k
    exists=(A.rank()==A.row_join(rhs).rank())
    actual=ac.vertex_shifts(n,es)
    assert exists==(actual is not None)
    reversed_some=[(j,i,-k) if rng.randrange(2) else (i,j,k) for i,j,k in es]
    assert actual==ac.vertex_shifts(n,reversed_some)
    if exists:
        solvable+=1
        assert all(v.denominator==1 for v in actual)
print(f'150 independent exact incidence-matrix rank cases: {solvable} consistent; arbitrary edge reversal invariant.')
# Original denominator-inactive Boolean counterexample is infinite, not a bijection.
for u in [R(0),R(1,7),R(1),R(10)]:
    assert (-R(1,2)-u)*(R(1,2)-R(1,2))==0
print('Inactive Boolean branch counterexample verified with four distinct auxiliary values.')
