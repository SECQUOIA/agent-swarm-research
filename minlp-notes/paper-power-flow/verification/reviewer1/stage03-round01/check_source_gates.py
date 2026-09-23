"""Distinct exact diagnostics for the salvageable conjunction-only source gates.

These finite Fraction checks supplement an algebraic audit; they do not prove
universality, the non-basic-closed obstruction, or interval bounds globally.
"""
from fractions import Fraction as F
from itertools import product

def multiplication_to_squares(x,y):
    a,b=x+1,y+1
    ax,by=a+F(1,2),b+F(1,2)
    hx,hy=ax/2,by/2
    total=hx+hy
    shifted=total-F(1,2)
    sq=shifted*shifted
    upper=sq+F(1,2)
    aq,bq=a*a,b*b
    aqp,bqp=aq+F(1,2),bq+F(1,2)
    aqh,bqh=aqp/2,bqp/2
    qs=aqh+bqh
    qh=qs/2
    diff=upper-qh
    doubled=2*diff
    out=doubled-F(1,2)
    values=[a,b,ax,by,hx,hy,total,shifted,sq,upper,aq,bq,aqp,bqp,aqh,bqh,qs,qh,diff,doubled,out]
    assert out==a*b
    assert all(F(1,2)<=z<=2 for z in values)

def square_to_inversions(x):
    a=x+1
    b=a+F(1,2)
    ib=1/b
    ia=1/a
    c=ia+F(1,2)
    d=c-F(2,3)
    e=d+F(1,2)
    f=e-ib
    g=2*f
    h=g-F(2,3)
    i=1/h
    j=i-F(1,2)
    k=j+F(3,4)
    half=b/2
    out=k-half
    values=[a,b,ib,ia,c,d,e,f,g,h,i,j,k,half,out]
    assert out==a*a
    assert all(F(1,2)<=z<=2 for z in values)

samples=[F(i,100000) for i in range(-20,21)]
for x,y in product(samples,repeat=2): multiplication_to_squares(x,y)
for x in samples: square_to_inversions(x)
print(f'PASS: {len(samples)**2} multiplication-to-squares profiles and {len(samples)} square-to-inversions profiles.')
# A concrete failure of the source Lemma A's prescribed extension:
# (x>=0 OR y>=0), at x=-1/2,y=1/2, allows u arbitrary >=0 in
# (x-u)*(y-v)=0, u,v>=0, after taking v=y. Hence no projection bijection.
x,y=F(-1,2),F(1,2)
for u in (F(0),F(1),F(2)):
    v=y
    assert u>=0 and v>=0 and (x-u)*(y-v)==0
print('PASS: three different inactive-slack extensions of one source point refute Lemma A projection uniqueness.')
