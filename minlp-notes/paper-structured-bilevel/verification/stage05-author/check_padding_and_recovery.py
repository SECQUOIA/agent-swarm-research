"""Exact new-scope checks: padded cube response and gradient rational recovery.
Finite checks of two risky supporting arguments, not a global bilevel solver.
"""
from fractions import Fraction as F
from itertools import product
from math import factorial, ceil, lcm
import sympy as s


def vertices(n):
    for bits in product((0,1), repeat=n):
        prev=F(0); point=[]
        for bit in bits:
            prev=bit+(1-2*bit)*prev/4
            point.append(prev)
        yield bits,point


def padded():
    tested=0; slabs=0
    for weights in ([1,2],[1,2,3],[2,3,4]):
        n=len(weights); W=sum(weights); r=0
        while F(1,4)**(r+1)>F(1,8*W): r+=1
        N=n+(n-1)*r; free=[i*(r+1) for i in range(n)]
        points=list(vertices(N)); D=4**(N-1); delta=F(1,D*D); tau=delta/(2*N)
        c=[F(3,4)*F(1,4)**(2*(N-i-1)-1) for i in range(N-1)]+[F(0)]
        eligible=[]
        for bits,v in points:
            value=v[-1]-sum(ci*vi for ci,vi in zip(c,v))-v[-1]**2
            assert value==0
            ok=all(v[j]<=F(1,2) for j in range(N) if j not in free)
            assert ok==all(bits[j]==0 for j in range(N) if j not in free)
            if not ok: continue
            eligible.append(v)
            assert abs(sum(w*v[j] for w,j in zip(weights,free))-sum(w*bits[j] for w,j in zip(weights,free)))<=F(1,8)
            for h in (-delta/4,F(0),delta/4):
                price=2*v[-1]-1+h
                if not -1<=price<=1: continue
                grad=[tau*vi-ci-(price if j==N-1 else 0) for j,(vi,ci) in enumerate(zip(v,c))]
                for _,u in points:
                    dot=sum(g*(uj-vj) for g,uj,vj in zip(grad,u,v))
                    assert dot>=0
                    if u!=v: assert dot>=delta/4
                    tested+=1
        sums={sum(w*b for w,b in zip(weights,bits)) for bits in product((0,1),repeat=n)}
        for target in range(W+1):
            fits=any(abs(sum(w*v[j] for w,j in zip(weights,free))-target)<=F(1,4) for v in eligible)
            assert fits==(target in sums); slabs+=1
    print(f'PASS: {tested} full-cube exact directional certificates for padded vertices; {slabs} slab equivalences')


def clip(v): return min(F(1),max(F(0),v))
def convergents(v):
    p0,p1,q0,q1=0,1,1,0
    num,den=v.numerator,v.denominator
    while den:
        a,rem=divmod(num,den); p0,p1=p1,a*p1+p0; q0,q1=q1,a*q1+q0
        yield F(p1,q1)
        num,den=den,rem


def exact_active(Q,t):
    n=len(t)
    for status in product((0,1,2),repeat=n):
        free=[i for i,k in enumerate(status) if k==2]
        z=s.Matrix([int(k==1) for k in status]); mat=s.Matrix(Q); rhs=s.Matrix(t)
        if free:
            sol=mat.extract(free,free).inv()*(-rhs-mat*z).extract(free,[0])
            for i,v in zip(free,sol): z[i]=v
        grad=mat*z+rhs
        if all(0<=v<=1 for v in z) and all((grad[i]>=0 if status[i]==0 else grad[i]<=0 if status[i]==1 else grad[i]==0) for i in range(n)):
            return [F(v) for v in z]
    raise AssertionError('missing active optimum')


def recovery():
    cases=[([[F(1,2**30)]],[F(-1,3)]),([[F(7,5)]],[F(-2,7)]),
           ([[F(2),F(1)],[F(1),F(2)]],[F(-2,3),F(-4,5)]),
           ([[F(2),F(-1)],[F(-1),F(2)]],[F(5),F(-1,3)]),
           ([[F(3),F(1),F(0)],[F(1),F(3),F(-1)],[F(0),F(-1),F(2)]],[F(-1,5),F(-2,7),F(-3,4)])]
    its=0
    for Q,t in cases:
        n=len(t); inv=s.Matrix(Q).inv(); L=max(sum(abs(v) for v in row) for row in Q)
        K=L*max(sum(abs(F(inv[i,j])) for j in range(n)) for i in range(n))
        scale=lcm(*(v.denominator for row in Q for v in row),*(v.denominator for v in t))
        H=max(1,*(abs(int(v*scale)) for row in Q for v in row),*(abs(int(v*scale)) for v in t))
        B=factorial(n)*H**n
        logB=(B-1).bit_length(); logN=(n-1).bit_length()
        count=ceil(K*(2*logB+logN+4)); z=[F(0)]*n
        for _ in range(count):
            z=[clip(z[i]-(sum(Q[i][j]*z[j] for j in range(n))+t[i])/L) for i in range(n)]
        truth=exact_active(Q,t); error=F(1,4*B*B)
        assert all(abs(v-w)<error for v,w in zip(z,truth))
        recovered=[]
        for v in z:
            choices=set(convergents(v))|{F(0),F(1)}
            good=[q for q in choices if q.denominator<=B and abs(v-q)<=error]
            assert len(good)==1
            recovered.append(good[0])
        assert recovered==truth; its+=count
    print(f'PASS: {len(cases)} independent active-face comparisons for projected-gradient/continued-fraction recovery; {its} exact iterations')

if __name__=='__main__': padded(); recovery()
