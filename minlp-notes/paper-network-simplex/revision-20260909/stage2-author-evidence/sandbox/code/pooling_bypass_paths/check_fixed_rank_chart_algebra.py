"""Independent symbolic checks of vector charts and coordinate recovery.

These test exact cancellations and a worst-case forbidden-direction family;
they do not substitute for original-network feasibility checks.
"""
from random import Random

import sympy as sp


def main():
    rng = Random(120511)
    identities = 0
    for t in range(1, 6):
        q = sp.symbols(f'q0:{t}')
        w = sp.Symbol('w')
        beta = [3**h for h in range(t)]
        for kind in ('general', 'repeated', 'equal_projection'):
            c1 = [sp.Integer(rng.randrange(-4, 5)) for _ in range(t)]
            c2 = [sp.Integer(rng.randrange(-4, 5)) for _ in range(t)]
            if kind == 'repeated':
                c2 = c1[:]
            elif kind == 'equal_projection':
                c2 = c1[:]
                if t > 1:
                    c2[0] += 3
                    c2[1] -= 1
            B = [sp.Integer(rng.randrange(-4, 5)) for _ in range(t)]
            b = sp.Rational(3, 2)
            g1 = sum(beta[h]*(c1[h]-q[h]) for h in range(t))
            g2 = sum(beta[h]*(c2[h]-q[h]) for h in range(t))
            R = b*sum(beta[h]*(B[h]-q[h]) for h in range(t))
            for h in range(t):
                a = sp.expand((c1[h]-q[h])*g2-(c2[h]-q[h])*g1)
                f = sp.expand(g1*(b*(B[h]-q[h])*g2-(c2[h]-q[h])*R))
                assert sp.Poly(a, *q).total_degree() <= 1
                assert sp.Poly(f, *q).total_degree() <= 2
                original_cleared = ((c1[h]-q[h])*g2*w
                                    +(c2[h]-q[h])*g1*(R-w)
                                    -b*(B[h]-q[h])*g1*g2)
                assert sp.expand(a*w-f-original_cleared) == 0
                identities += 1
    cover_checks = 0
    k = sp.Symbol('k')
    for t in range(2, 6):
        for n in range(1, 9):
            # At q=0, input i forbids exactly its assigned t-1 integer directions.
            vectors = []
            for i in range(n):
                roots = range(i*(t-1)+1, (i+1)*(t-1)+1)
                poly = sp.Poly(sp.prod(k-r for r in roots), k)
                vectors.append([int(poly.nth(h)) for h in range(t)])
            final = n*(t-1)+1
            good = []
            for value in range(1, final+1):
                beta = [value**h for h in range(t)]
                if all(sum(bh*ch for bh, ch in zip(beta, C)) != 0 for C in vectors):
                    good.append(value)
            assert good == [final]
            cover_checks += 1
    print(f'PASS: {identities} exact vector-equation identities and degree cancellations.')
    print(f'PASS: {cover_checks} moment-curve cover tests with every earlier direction forbidden.')


if __name__ == '__main__':
    main()
