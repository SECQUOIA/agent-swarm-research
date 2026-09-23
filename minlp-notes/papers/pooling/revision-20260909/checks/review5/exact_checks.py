from fractions import Fraction as F
from itertools import product

# Independent scalar gate checks, including variable endpoints and repeated names.
vals = sorted({F(a,b) for b in range(1,10) for a in range(1,19) if F(1,2)<=F(a,b)<=2})
for a in vals:
    for B in [7,11,31]:
        e=1/a
        assert (a/B)*e == 2*F(1,2*B)
        assert 0 <= 2-e <= 2
        assert (2-(2-e)) == e
        assert B-a >= 0
        assert B-2*e >= 3 if B==7 else B-2*e >= 0
    comp=F(5,2)-a
    assert F(1,2)<=comp<=2
    assert 1/(1/a)==a

inversions=0
additions=0
for x,y in product(vals,repeat=2):
    if x*y == 1:
        inversions+=1
        # Many-pool inversion: clean outlet is complement of y.
        clean=F(5,2)-y
        assert (x/7)*(F(5,2)-clean)==F(5,2)*F(2,35)
        # One-pool inversion: all three distinct pins.
        t1,t2=y,1/y
        assert x*t1==t1*t2==y*t2==1
    z=x+y
    if z<=2:
        additions+=1
        assert (F(5,2)-x-y)/(7*(F(5,2)-z)) == F(1,7)
        tau=2/z
        assert 1<=tau<=2
        assert z*tau==(x+y)*tau==2
        # Repeated-summand normalization preserves values uniquely.
        if x==y:
            u=1/x
            xp=1/u
            assert xp==x and xp*u==1

# Two source qualities, an active two-pool circulation, and two products.
# f: i0->a=1, i1->b=1, a->b=2, b->a=1, b->j=1/2, b->k=3/2.
f={('i0','a'):F(1),('i1','b'):F(1),('a','b'):F(2),('b','a'):F(1),('b','j'):F(1,2),('b','k'):F(3,2)}
q={'i0':F(0),'i1':F(1),'a':F(1,4),'b':F(1,2)}
h={'j':{'a':F(1,4),'b':F(1,4),'j':F(1),'k':F(0)},'k':{'a':F(3,4),'b':F(3,4),'j':F(0),'k':F(1)}}
for dest in ['j','k']:
    component={(u,v):amount*h[dest][v] for (u,v),amount in f.items()}
    for pool in ['a','b']:
        inf=sum(t for (u,v),t in component.items() if v==pool)
        outf=sum(t for (u,v),t in component.items() if u==pool)
        mass=sum(q[u]*t for (u,v),t in component.items() if v==pool)
        assert inf==outf and inf*q[pool]==mass
    assert all(0<=component[e]<=f[e] for e in f)
assert all(sum(f[e]*h[j][e[1]] for j in h)==f[e] for e in f)

# The facial converse on C=[0,1], R=[1/3,2/3].
assert F(1,3)*0+F(2,3)*1==F(2,3)
assert not (F(1,3)<=0<=F(2,3)) and not (F(1,3)<=1<=F(2,3))
# Positive unit mixture exists, whereas only zero integral throughput is feasible.
print(f'PASS: {len(vals)} rational gate inputs, {inversions} inversion pairs, {additions} addition pairs; cyclic destination/mass identities; facial nonintegrality example.')
