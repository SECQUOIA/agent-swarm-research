"""Independent compiled-knot audit checks.

Root enclosures and rounding bounds use exact fractions. The huge integer
and rational exponent checks use 300-digit Decimal reference values and
supplement, rather than certify, the symbolic uniform proof.
"""
from fractions import Fraction as F
from decimal import Decimal, localcontext

def ceil_log2(x):
    x=F(x); z=x.numerator.bit_length()-x.denominator.bit_length()
    p=F(2**z) if z>=0 else F(1,2**(-z))
    return z if p>=x else z+1

def fixed_power(s,D,P):
    unit=1<<P
    b=s*unit
    assert b.denominator==1
    b=b.numerator; out=unit; exponent=D
    while exponent:
        if exponent&1: out=(out*b)//unit
        exponent//=2
        if exponent: b=(b*b)//unit
    return F(out,unit)

def integer_knot(k,L,D,delta):
    if k==0: return F(0)
    if k==2**L: return F(1)
    u=F(k,2**L)**2
    tau=delta*F(1,2**(2*L)*16)
    R=ceil_log2(2/delta); P=max(R+1,ceil_log2(D/tau))
    lo=F(0); hi=F(1)
    for _ in range(R):
        s=(lo+hi)/2
        A=fixed_power(s,D,P)
        if A+tau<u: lo=s
        elif A>u: hi=s
        else: return s
    return (lo+hi)/2

def H(w,N):
    z=(w-1)/(w+1)
    return 2*sum((z**(2*j+1)/F(2*j+1) for j in range(N)),F(0))

def rational_knot(k,L,alpha,delta):
    if k==0: return F(0)
    if k==2**L: return F(1)
    t=F(k,2**L); e=1
    while 2**e*t<1: e+=1
    v=2**e*t
    assert 1<=v<2 and e<=L
    factor=1 if alpha>=2 else 2
    N=1
    while F(3*factor*(L+1),9**N)>delta/8: N+=1
    A=F(2,alpha)*(H(v,N)-e*H(F(2),N))
    assert -factor*L<=A<=0
    M=1
    while M<2*factor*L: M*=2
    q=A/M
    J=1
    while F(1,2**(J+1))>delta/(16*M): J+=2
    P=F(1); term=F(1)
    for j in range(1,J+1):
        term=term*q/j; P+=term
    assert F(1,2)<=P<=1
    y=P**M
    B=ceil_log2(4/delta)
    return F((y*2**B).__floor__(),2**B)

def dec(x):
    return Decimal(x.numerator)/Decimal(x.denominator)

exact=0; rounded=0; huge=0; rational=0
for D in [2,3,7,19,64]:
    for L in [1,3,5]:
        for k in sorted(set([0,1,2**(L-1),2**L-1,2**L])):
            delta=F(1,1024*D)
            root=integer_knot(k,L,D,delta)
            assert 0<=root<=1
            u=F(k,2**L)**2
            assert max(F(0),root-delta)**D<=u<=min(F(1),root+delta)**D
            exact+=1
    for P in [8,16,25]:
        for s in [F(0),F(1,8),F(3,8),F(7,8),F(1)]:
            a=fixed_power(s,D,P)
            assert 0<=s**D-a<=(D-1)*F(1,2**P)
            rounded+=1
with localcontext() as ctx:
    ctx.prec=300
    for D in [2**80+3,2**200+51]:
        for L,k in [(3,1),(3,7),(20,1),(20,2**19+1)]:
            delta=F(1,64*D)
            root=integer_knot(k,L,D,delta)
            truth=(dec(F(k,2**L)).ln()*Decimal(2)/Decimal(D)).exp()
            assert abs(dec(root)-truth)<dec(delta)
            huge+=1
    for alpha in [F(2),F(5,2),F(17,3),F(10**25+1,7),F(2**100+3,2**20+1),F(3,2),F(4,3),1+F(1,2**90)]:
        for L,k in [(1,1),(3,1),(3,7),(7,1),(7,65)]:
            delta=min(F(1),alpha-1)*F(1,128)/alpha
            root=rational_knot(k,L,alpha,delta)
            truth=(dec(F(k,2**L)).ln()*dec(2/alpha)).exp()
            assert 0<=root<=1 and abs(dec(root)-truth)<dec(delta)
            rational+=1
print(f'PASS: {exact} exact integer root enclosures; {rounded} exact rounded-power bounds; {huge} 300-digit huge-exponent checks; {rational} 300-digit rational-exponent checks.')
