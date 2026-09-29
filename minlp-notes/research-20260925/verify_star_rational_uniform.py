"""Exact targeted checks for rational uniformly conditioned star examples.

This checks finite instances, not all N or the literature/novelty assessment.
"""
from fractions import Fraction as F
from itertools import product


def mul(a,b):
    return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])


def dot(a,b):
    return a[0]*b[0]+a[1]*b[1]


def add(a,b):
    return (a[0]+b[0],a[1]+b[1])


def sub(a,b):
    return (a[0]-b[0],a[1]-b[1])


def neg(a):
    return (-a[0],-a[1])


def rotate(a):
    return mul((F(5,13),F(-12,13)),a)


def polygon(qs):
    ps=[mul(q,q) for q in qs]
    first=mul(qs[0],qs[-1])
    es=[first]+[mul((F(0),F(1)),mul(q,r)) for q,r in zip(qs,qs[1:])]+[neg(first)]
    perimeter=2*(dot(add(ps[0],ps[-1]),first)+sum(dot(sub(r,p),e) for p,r,e in zip(ps,ps[1:],es[1:-1])))
    gs=[sub(e,f) for e,f in zip(es,es[1:])]
    return ps,gs,perimeter


def instance(n):
    ts=[F(2*i-(n-1),64*(n-1)) for i in range(n)]
    qs=[( (1-t*t)/(1+t*t),2*t/(1+t*t)) for t in ts]
    ps,gs,per=polygon(qs)
    deleted=[polygon(qs[:i]+qs[i+1:])[2] for i in range(n)]
    eta=(4/per+min(4/p for p in deleted))/2
    assert per>4 and all(F(4)<=p<per for p in deleted)
    assert 4/per<eta<1 and all(eta*p<4 for p in deleted)
    ps=[rotate(p) for p in ps];gs=[rotate(g) for g in gs]
    assert sum(g[0] for g in gs)==F(10,13)
    assert sum(g[1] for g in gs)==F(-24,13)
    assert sum(dot(g,p) for g,p in zip(gs,ps))==per/2
    ws=[-g[1] for g in gs];assert all(w>0 for w in ws)
    bs=[]
    for w in ws:
        b=F(1)
        while b*b>=4*w: b/=2
        while b*b<w: b*=2
        assert w<=b*b<4*w
        bs.append(b)
    ds=[b*b/w for b,w in zip(bs,ws)]
    assert all(1<=d<4 for d in ds)
    a=F(25,13);assert a-sum(b*b/d for b,d in zip(bs,ds))==F(1,13)
    z=[(1+eta*p[1])/2 for p in ps]; s=[eta*p[0]/2 for p in ps];r=[(1-eta*p[1])/2 for p in ps]
    assert all(0<zi<1 for zi in z)
    ys=[-w*si/b-zi*g[0]/b for w,si,b,zi,g in zip(ws,s,bs,z,gs)]
    cost=a+sum(d*(y+b*si/d)**2/zi-w*ri for d,y,b,si,zi,w,ri in zip(ds,ys,bs,s,z,ws,r))
    lv=a+sum(-2*g[0]*si-w*ri for g,si,w,ri in zip(gs,s,ws,r))
    c=sum(g[1]*zi for g,zi in zip(gs,z))-(2+sum(g[1] for g in gs))/2
    gap=eta*per/2-2
    assert c-lv==gap>0
    affine_residual=cost+sum(2*d*g[0]*y/b+(w+g[0]*g[0]/w)*zi for d,g,y,b,w,zi in zip(ds,gs,ys,bs,ws,z))+F(1,13)
    assert affine_residual==-gap
    signs=0
    for eps in product((-1,1),repeat=n):
        v=(sum(e*g[0] for e,g in zip(eps,gs)),sum(e*g[1] for e,g in zip(eps,gs)))
        assert dot(v,v)<=4
        signs+=1
    values=[a,eta,*bs,*ds,*ys,*z]
    bits=max(max(abs(v.numerator).bit_length(),v.denominator.bit_length()) for v in values)
    return signs,bits,float(cost),float(gap)


if __name__=='__main__':
    counts=0
    for n in range(2,10):
        signs,bits,cost,gap=instance(n);counts+=signs
        print(f'N={n}: signs={signs}, max_bits={bits}, candidate={cost:.9g}, certified_gap={gap:.9g}')
    print(f'PASS: 8 rational instances; {counts} exact sign-pattern PSD checks.')
