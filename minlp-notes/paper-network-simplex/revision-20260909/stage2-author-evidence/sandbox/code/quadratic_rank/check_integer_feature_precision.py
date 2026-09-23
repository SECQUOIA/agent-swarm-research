"""Exact normalized integer-feature and minor-volume checks."""
import random
import sympy as sp

rng = random.Random(9052026)
count = 0
for r in range(1, 7):
    for extra in range(5):
        n = r+extra
        while True:
            T = sp.Matrix(r, n, lambda i,j: rng.randrange(-3, 4))
            if T.rank() == r:
                break
        _, columns = T.rref()
        minor = abs(T[:, list(columns)].det())
        widths = sp.Matrix([sum(abs(T[i,j]) for j in range(n)) for i in range(r)])
        offsets = sp.Matrix([sum(min(0,T[i,j]) for j in range(n)) for i in range(r)])
        product = sp.prod(widths)
        assert 1 <= minor <= product
        assert sp.Rational(minor,product) >= 1/product
        a = sp.Matrix([sp.Rational(rng.randrange(1,7), 5) for i in range(r)])
        H = T.T*sp.diag(*a)*T
        assert H.rank() == r
        x = sp.Matrix([sp.Rational(rng.randrange(17),16) for j in range(n)])
        u = sp.diag(*[1/w for w in widths])*(T*x-offsets)
        assert all(0 <= z <= 1 for z in u)
        assert (x.T*H*x)[0]/2 == sum(a[i]*(widths[i]*u[i]+offsets[i])**2/2 for i in range(r))
        # Rational row rescaling changes coefficients, but preserves the map.
        scales = [sp.Rational(i+2,i+3) for i in range(r)]
        S = sp.diag(*scales)*T
        scaled_a = [a[i]/scales[i]**2 for i in range(r)]
        assert S.T*sp.diag(*scaled_a)*S == H
        count += 1
print(f'PASS: {count} exact integer-feature minor, range, rank, quotient and scaling cases')
