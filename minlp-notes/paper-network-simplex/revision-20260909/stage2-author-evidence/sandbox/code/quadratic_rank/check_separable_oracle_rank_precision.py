"""Exact product-code and coupled-band checks for the separable extension."""
from fractions import Fraction as F
from math import comb


lattice_checks=0
for n in range(1,9):
    for r in range(1,7):
        for scale,base in [(2,15),(36,219)]:
            radius=scale*n*r*r
            exact=sum(2**k*comb(n,k)*comb(radius,k) for k in range(n+1))
            assert exact<(base*r*r)**n
            lattice_checks+=1


def q(x):
    return (x*x,x*x*x)


def image(z):
    return (z[0],z[1],z[0]+z[1])


band_checks=0
r=2
for n in [1,2,4,8]:
    delta=F(1,16*n*r*3)
    for case in range(24):
        total_gap=[F(0),F(0)]
        for i in range(n):
            a=F((7*case+11*i)%127,128)
            b=a+F(1,128)
            theta=F((case+3*i)%9,8)
            x=(1-theta)*a+theta*b
            qa,qb,qx=q(a),q(b),q(x)
            for j in range(r):
                total_gap[j]+=(1-theta)*qa[j]+theta*qb[j]-qx[j]
        for sign0 in [-1,1]:
            for sign1 in [-1,1]:
                center=[total_gap[0]+sign0*n*delta,total_gap[1]+sign1*n*delta]
                assert max(map(abs,center))<=F(17,64*r)
                for u0 in [-1,1]:
                    for u1 in [-1,1]:
                        error=[center[0]+F(u0,2*r),center[1]+F(u1,2*r)]
                        assert max(map(abs,error))<=F(49,64*r)
                        assert max(map(abs,image(error)))<=1
                        band_checks+=1
print(f'PASS: {lattice_checks} exact lattice-ball bounds; '
      f'{band_checks} coupled separable rounding/band checks')
