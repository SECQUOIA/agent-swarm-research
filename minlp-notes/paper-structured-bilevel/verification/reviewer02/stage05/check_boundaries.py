from fractions import Fraction as F
from itertools import product
from pathlib import Path

def verts(n,g):
    out={}
    for bits in product((0,1),repeat=n):
        z=[];prev=F(0)
        for b in bits:
            prev=b+(1-2*b)*g*prev;z.append(prev)
        out[bits]=z
    return out

def dot(a,b):return sum(x*y for x,y in zip(a,b))
checks=0
for n in range(1,7):
    g=F(1,4);V=verts(n,g);D=4**(n-1);gap=F(1,D*D);tau=gap/(2*n)
    c=[(1-g)*g**(2*(n-i-1)-1) for i in range(n-1)]+[F(0)]
    for bits,v in V.items():
        assert v[-1]-dot(c,v)-v[-1]**2==0
        lam=2*v[-1]-1
        grad=[tau*x-y for x,y in zip(v,c)];grad[-1]-=lam
        for j in range(n):
            bb=list(bits);bb[j]=1-bb[j];u=V[tuple(bb)]
            direction=[a-b for a,b in zip(u,v)]
            assert dot(grad,direction)>=gap/2
            checks+=1
# Padded original-cube vertices, not vertices of a relaxed padding model.
padded=0
for a in [(2,3),(1,1,1),(2,2,3)]:
    W=sum(a);r=0
    while F(1,4**(r+1))>F(1,8*W):r+=1
    n=len(a);N=n+(n-1)*r;free=[i*(r+1) for i in range(n)]
    V=verts(N,F(1,4));valid=[(b,z) for b,z in V.items() if all(z[j]<=F(1,2) for j in range(N) if j not in free)]
    assert len(valid)==2**n
    sums={sum(ai*bi for ai,bi in zip(a,b)) for b in product((0,1),repeat=n)}
    for b,z in valid:
        assert all(b[j]==0 for j in range(N) if j not in free)
        assert abs(sum(ai*z[j] for ai,j in zip(a,free))-sum(ai*b[j] for ai,j in zip(a,free)))<=F(1,8)
    for T in range(W+1):
        exists=any(abs(sum(ai*z[j] for ai,j in zip(a,free))-T)<=F(1,4) for b,z in valid)
        assert exists==(T in sums);padded+=1
# The normalized Lasso recursion has every full sign vector with last entry +1.
patterns=[(0,),(1,)]
for p in range(1,6):
    assert {q for q in patterns if 0 not in q}=={q+(1,) for q in product((-1,1),repeat=p-1)}
    patterns=[q+(0,) for q in patterns]+[q+(1,) for q in reversed(patterns)]+[tuple(-x for x in q)+(1,) for q in patterns[1:]]
msg=f'{checks} exact original-cube exposure edge checks; {padded} padded target equivalences; Lasso full-sign recursion checked through dimension 5.\n'
Path(__file__).with_suffix('.log').write_text(msg);print(msg)
