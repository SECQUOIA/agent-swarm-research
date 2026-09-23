"""Exact independent checks for positive-polynomial inverse approximation.

Coefficients are computed by the Lagrange coefficient formula, independently
of the candidate's formal-substitution recurrence. Reference inverse values
are enclosed by exact rational bisection. No floating-point root values are
used as certificates.
"""
from fractions import Fraction as F
from math import comb,lcm


def mul(a,b,q):
    out=[F(0)]*(q+1)
    for i,ai in enumerate(a):
        for j,bj in enumerate(b):
            if i+j<=q:out[i+j]+=ai*bj
    return out


def evaluate(coeff,x):
    value=F(0)
    for c in reversed(coeff):value=value*x+c
    return value


def bracket(coeff,target,width):
    lo=F(0);hi=F(1)
    while hi-lo>width:
        mid=(lo+hi)/2
        if evaluate(coeff,mid)<target:lo=mid
        else:hi=mid
    return lo,hi


def inverse_lagrange(a,q):
    h=[F(0)]+[x/a[1] for x in a[2:]]
    h=h+[F(0)]*max(0,q+1-len(h))
    h=h[:q+1]
    out=[F(0)]*(q+1)
    for n in range(1,q+1):
        power=[F(1)]+[F(0)]*q
        total=F(0)
        for k in range(n):
            total+=(-1)**k*comb(n+k-1,k)*power[n-1]
            power=mul(power,h,q)
        out[n]=total/(n*a[1]**n)
    return out


raws=[
    [F(0),F(1)],
    [F(0),F(0),F(1)],
    [F(0),F(1,2**100),F(0),F(1)],
    [F(0),F(1),F(0),F(0),F(0),F(1,2**90)],
    [F(0),F(3,7),F(0),F(5,11),F(0),F(0),F(2,13)],
    [F(0)]*8+[F(1)],
]
centers=values=identities=0
for raw in raws:
    total=sum(raw);g=[x/total for x in raw];P=len(g)-1
    assert (1+F(1,4*P))**(P-1)-1<F(1,3)
    for m in (2,4,6):
        eta=F(1,2**m);K=P*m;q=m+3
        trunc=F(1,2**K)
        assert evaluate(g,eta)>=trunc
        for k in sorted(set((0,K//2,K-1))):
            A=F(1,2**(k+1));step=A/(32*P)
            for panel in sorted(set((0,16*P,32*P-1))):
                left=A+panel*step;right=left+step;tau=(left+right)/2
                lo,hi=bracket(g,tau,tau/(64*P*P));z0=(lo+hi)/2;t0=evaluate(g,z0)
                assert z0>0 and abs(t0-tau)<=tau/(64*P)
                Rt=t0/(8*P);rz=z0/(4*P)
                a=[sum(g[j]*comb(j,h)*z0**(j-h) for j in range(h,P+1)) for h in range(P+1)]
                assert t0<=z0*a[1]<=P*t0
                assert Rt<=a[1]*rz/2
                cs=inverse_lagrange(a,q)
                # Compose the independently computed inverse jet into g.
                power=[F(1)]+[F(0)]*q;composition=[F(0)]*(q+1)
                for h in range(1,min(P,q)+1):
                    power=mul(power,cs,q)
                    for j in range(q+1):composition[j]+=a[h]*power[j]
                assert composition[1]==1 and all(composition[j]==0 for j in range(2,q+1))
                D=lcm(*(x.denominator for x in a[1:]));A1=int(a[1]*D)
                for j in range(1,q+1):
                    assert (cs[j]*A1**(2*j-1)/D**j).denominator==1
                    assert abs(cs[j])*Rt**j<=2
                    identities+=1
                for target in (left,tau,right):
                    assert abs(target-t0)/Rt<=F(16,63)
                    approx=z0+evaluate(cs,target-t0)
                    rlo,rhi=bracket(g,target,eta/128)
                    assert max(abs(approx-rlo),abs(approx-rhi))<=eta/4
                    values+=1
                centers+=1
print('rational centers',centers,'exact denominator/Cauchy checks',identities,'certified inverse values',values)
