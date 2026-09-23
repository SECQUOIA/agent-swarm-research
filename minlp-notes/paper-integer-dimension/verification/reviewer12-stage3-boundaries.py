"""Exact finite checks supporting the stage-3 boundary proofs."""
from fractions import Fraction as F
from itertools import product
convex=concave=residues=rectangles=root_cells=0
for q in (2,3,4,7):
    for eta in (F(0),F(1,10),F(1),F(10),F(100)):
        M=2
        while M**(q-1)<=2**q*(1+eta): M+=1
        for gap in range(1,11):
            r=F(1,M**gap)
            u=F(1,M)+(1-F(1,M))*r
            v=F(1,M)+(1-F(1,M))*r**q
            assert v>(1+eta)*u**q
            convex+=1
for eta in (F(0),F(1,10),F(1,2),F(9,10),F(99,100)):
    b=2
    while F(2,b)>=1-eta: b+=1
    M=b*b
    for gap in range(1,11):
        r=F(1,M**(2*gap)); root_r=F(1,M**gap)
        u=F(1,M)+(1-F(1,M))*r
        v=F(1,M)+(1-F(1,M))*root_r
        assert v*v<(1-eta)**2*u
        concave+=1
for M in (2,3,7,13):
    for p in (1,2,3):
        for base in product(range(min(M,3)),repeat=p):
            zx=[b-M*(i+2) for i,b in enumerate(base)]
            zy=[b+M*(2*i+3) for i,b in enumerate(base)]
            z=[F(M-1,M)*x+F(1,M)*y for x,y in zip(zx,zy)]
            assert all(a.denominator==1 for a in z)
            residues+=1
for q in (2,3,5):
    rho=F(9,8); eta=rho**q-1
    for scale in range(1,10):
        lo=rho**(-scale); hi=lo*rho
        for ix in range(21):
            x=lo+(hi-lo)*F(ix,20)
            for w in (lo**q,hi**q):
                assert abs(w-x**q)<=eta*x**q
                rectangles+=1
for D in (2,3,7,16,31):
    for j in range(16):
        for it in range(21):
            theta=F(it,20); t=(j+theta)/16
            x=(1-theta)*F(j,16)**D+theta*F(j+1,16)**D
            assert t**D<=x<=(t+F(1,16))**D
            root_cells+=1
print(f'PASS: {convex} convex ratios, {concave} concave ratios, {residues} residue mixtures, {rectangles} rectangle errors, {root_cells} root-cell bounds')
