from fractions import Fraction as F
from itertools import combinations
import random
import sympy as s
from check_ac_exact import vertex_shifts

# Symbolic elimination, starting with the physical nodal powers.
x,y,I,W,C=s.symbols('x y I W C', nonzero=True)
pin_tie=(1-I)+(1-(C-x))-(2-C)
pin_output=(1-W)+2*(1-(C-x))+(1-(C-y))-(5-3*C)
power_I=I*((I-W)+(I-1))+1
assert s.expand(pin_tie)==x-I
assert s.expand(pin_output)==2*x+y-W-1
assert s.simplify(power_I.subs({I:x,W:2*x-1+1/x}))==0
assert s.simplify(pin_output.subs(W,2*x-1+1/x))==y-1/x
for constant in (s.Rational(5,2),s.Rational(9,2)):
    assert s.expand(((1-x)+(1-y)+(1-(constant-s.Symbol('z'))))-(3-constant)) == s.Symbol('z')-x-y
print('Symbolic physical gadget elimination: passed.')

# Exact straight-line incidence drawing of the crossover has no improper intersections.
pts={'X':(-2,0),'Y':(0,-2),'Xp':(2,0),'Yp':(0,2),
     'Z':(0,0),'A':(-1,-1),'B':(-1,1),'C':(1,-1)}
edges=[(a,b) for a,bs in [('A',['X','Y','Z']),('B',['X','Yp','Z']),('C',['Xp','Y','Z'])] for b in bs]
def cross(a,b,c):
    return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
for (a,b),(c,d) in combinations(edges,2):
    if {a,b}&{c,d}: continue
    p,q,r,t=map(pts.get,(a,b,c,d))
    assert not (cross(p,q,r)*cross(p,q,t)<0 and cross(r,t,p)*cross(r,t,q)<0)
print('Exact crossover drawing: no proper edge crossings.')

# Independent rational Gaussian elimination, not graph propagation or cycle enumeration.
def consistent(matrix):
    a=[[F(v) for v in row] for row in matrix]
    row=0
    for col in range(len(a[0])-1):
        pivot=next((j for j in range(row,len(a)) if a[j][col]),None)
        if pivot is None: continue
        a[row],a[pivot]=a[pivot],a[row]
        p=a[row][col]
        a[row]=[v/p for v in a[row]]
        for j in range(row+1,len(a)):
            p=a[j][col]
            a[j]=[v-p*w for v,w in zip(a[j],a[row])]
        row+=1
    return all(any(r[:-1]) or not r[-1] for r in a)
rng=random.Random(517267)
count=0
for n in range(1,13):
    for case in range(35):
        es=[(i,j,rng.randrange(-1,2)) for i,j in combinations(range(n),2) if rng.random()<.25]
        matrix=[]
        for i,j,k in es:
            r=[0]*(n+1);r[i]=-1;r[j]=1;r[-1]=k;matrix.append(r)
        if not matrix: matrix=[[0]*(n+1)]
        shifts=vertex_shifts(n,es)
        assert consistent(matrix)==(shifts is not None)
        if shifts is not None:
            assert all(a.denominator==1 for a in shifts)
        count+=1
print(f'Independent Gaussian consistency oracle: {count} graph instances, n=1..12, passed.')
