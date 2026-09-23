"""Exact checks for the rank-based inner-band construction.

Uses V=[[1,0],[0,1],[1,1]], K=the ambient unit cube, and B=I.
The uniform oracle/spanner algorithms remain analytically proved elsewhere.
"""
from fractions import Fraction as F


def q(x):
    return (x*x,x*x*x)


def image(z):
    return (z[0],z[1],z[0]+z[1])


def mix(a,b,t):
    return tuple((1-t)*u+t*v for u,v in zip(a,b))


r=2
# P_0 is the coordinate square of radius1/2. Its image lies in K because
# each output coordinate, including the sum, has absolute value<=1.
box_checks=0
for i in range(-8,9):
    for j in range(-8,9):
        z=(F(i,16),F(j,16))
        assert max(map(abs,image(z)))<=1
        box_checks+=1

chord_checks=band_checks=0
# B^-1=I; L_B=1+sum|B^-1|=3 and delta=1/(16rL_B).
delta=F(1,96)
for k in range(64):
    a,b=F(k,64),F(k+1,64)
    qa,qb=q(a),q(b)
    for h in range(9):
        theta=F(h,8)
        x=(1-theta)*a+theta*b
        exact_chord=mix(qa,qb,theta)
        gap=tuple(t-v for t,v in zip(exact_chord,q(x)))
        assert all(v>=0 for v in gap)
        assert max(map(abs,image(gap)))==sum(gap)
        chord_checks+=1
        for signs in [(-1,-1),(-1,1),(1,-1),(1,1)]:
            # A permissible signed endpoint error; interpolation with the same
            # error at both ends reaches the rounding box boundary exactly.
            err=tuple(s*delta for s in signs)
            center_error=tuple(g+e for g,e in zip(gap,err))
            assert max(map(abs,center_error))<=F(17,64*r)
            for band_signs in [(-1,-1),(-1,1),(1,-1),(1,1)]:
                band=tuple(F(s,2*r) for s in band_signs)
                total=tuple(g+u for g,u in zip(center_error,band))
                assert max(map(abs,total))<=F(49,64*r)
                assert max(map(abs,image(total)))<=1
                band_checks+=1
print(f'PASS: {box_checks} inner-parallelotope checks; '
      f'{chord_checks} exact vector-chord comparisons; {band_checks} inner-band errors')
