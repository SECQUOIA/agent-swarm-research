"""Exact checks for scalarized positive shapes and dyadic-layer powers."""
from fractions import Fraction as Q
import random

rng = random.Random(7092026)
shape_checks = 0
for degree in range(2, 25):
    for _ in range(12):
        coeffs = [Q(rng.randrange(6),7) for k in range(2,degree+1)]
        if not any(coeffs):
            coeffs[0] = Q(1)
        total = sum(coeffs)
        coeffs = [c/total for c in coeffs]
        phi = lambda x: sum(c*x**k for k,c in enumerate(coeffs,2))
        x,y = Q(rng.randrange(17),16),Q(rng.randrange(17),16)
        u,v,mid = phi(x),phi(y),phi((x+y)/2)
        # Equivalent exact check of sqrt(phi(mid)) <= (sqrt(u)+sqrt(v))/2.
        needed = mid-(u+v)/4
        if needed > 0:
            assert u*v >= 4*needed*needed
        shape_checks += 1

curvature_checks = 0
recurrence_checks = 0
for degree in [2,3,4,7,8,15,16,31,32,64]:
    J = (degree-1).bit_length()
    layers = [(1-Q(1,2**j),Q(1,2**(j+1))) for j in range(J)]
    layers.append((1-Q(1,2**J),Q(1,2**J)))
    assert layers[0][0] == 0 and sum(length for _,length in layers) == 1
    for j,(left,length) in enumerate(layers):
        right = left+length
        for k in range(2,degree+1):
            assert k*(k-1)*length*length*right**(k-2) <= 2
            curvature_checks += 1
        L = rng.randrange(5)
        h = Q(1,2**L)
        index = rng.randrange(2**L)
        prefix = index*h
        bits = [(index >> (L-ell-1)) & 1 for ell in range(L)]
        eta = Q(rng.randrange(9),8)*h
        selectors = [int(q==j) for q in range(J+1)]
        a = left+length*prefix
        rho = length*eta
        x = a+rho
        assert left <= x <= right
        def multiply_a(v):
            prefix_v = sum(Q(1,2**(ell+1))*bit*v for ell,bit in enumerate(bits))
            return sum(sel*(origin*v+scale*prefix_v) for sel,(origin,scale) in zip(selectors,layers))
        v,t = Q(1),rho
        for k in range(1,degree+1):
            previous_t = t
            v,t = multiply_a(v),multiply_a(t)
            assert v == a**k and t == a**k*rho
            if k >= 2:
                remainder = x**k-v-k*previous_t
                assert 0 <= remainder <= h*h
                recurrence_checks += 1

allocation_checks = 0
for _ in range(30):
    rows,cols = 3,4
    C = [[Q(rng.randrange(6),3) for i in range(cols)] for j in range(rows)]
    lam = [Q(rng.randrange(1,6),4) for j in range(rows)]
    A = [sum(lam[j]*C[j][i] for j in range(rows)) for i in range(cols)]
    optimum = [min(Q(1),1/a) if a else Q(1) for a in A]
    mu = [1/p-a for p,a in zip(optimum,A)]
    assert all(v>=0 for v in mu)
    assert all(v*(p-1)==0 for v,p in zip(mu,optimum))
    budget = sum(a*p for a,p in zip(A,optimum))
    # Supporting scalarization and original weighted-l1 allocation coincide.
    Cp = [sum(row[i]*optimum[i] for i in range(cols)) for row in C]
    assert sum(lam[j]*Cp[j] for j in range(rows)) == budget
    allocation_checks += 1
print(f'PASS: {shape_checks} convex-square-root identities, {curvature_checks} layer curvature bounds, {recurrence_checks} exact prefix/Taylor bounds, {allocation_checks} scalarization KKT cases')
