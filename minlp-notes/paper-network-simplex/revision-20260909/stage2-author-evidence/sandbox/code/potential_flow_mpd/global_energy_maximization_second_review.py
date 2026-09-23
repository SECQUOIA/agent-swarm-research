"""Exact cone, zero-case, and passive duality controls for the second audit.

This checks the formulation identities, not an SOCP optimization algorithm.
"""
from fractions import Fraction as F
from itertools import combinations, product
from random import Random


def run():
    values = [F(0), F(1, 8), F(1, 2), F(1), F(2), F(5)]
    betas = [F(1, 2**80), F(1, 8), F(1), F(3), F(2**80)]
    projection_checks = necessity_checks = 0
    for beta, z, t in product(betas, values, values):
        projected = z**3 <= beta*t*t
        if projected:
            u = z*z/t if t else F(0)
            assert z*z <= t*u and u*u <= beta*z
        elif z > 0 and t == 0:
            assert not projected
        projection_checks += 1
        for u in values:
            if z*z <= t*u and u*u <= beta*z:
                assert projected
            necessity_checks += 1
    for lower in betas:
        r = min(F(1), lower)/2
        z, u, t = F(1), r, 2/r
        assert z > 0 and u > 0 and t > 0
        assert t*u-z*z == 1
        assert lower*z-u*u > 0

    rng = Random(574293)
    states = edge_checks = 0
    for n in range(2, 9):
        edges = list(combinations(range(n), 2))
        for _ in range(12):
            pi = [F(0)]+[F(rng.randrange(-5, 6), rng.randrange(1, 5)) for _ in range(n-1)]
            b = [F(0)]*n
            data = []
            for i, j in edges:
                d = pi[i]-pi[j]
                magnitude = F(rng.randrange(1, 6), rng.randrange(1, 5))
                x = magnitude if d > 0 else -magnitude if d < 0 else F(0)
                beta = abs(d)/magnitude**2 if d else F(2)
                z, u, t = beta*x*x, beta*abs(x), beta*abs(x)**3
                assert beta > 0 and d == beta*x*abs(x)
                assert z == abs(d) and z*z == t*u and u*u == beta*z
                b[i] += x
                b[j] -= x
                data.append((beta, x, z, u, t))
                edge_checks += 1
            assert sum(b) == 0
            dissipated = sum(t for beta, x, z, u, t in data)
            potential_work = sum(p*nom for p, nom in zip(pi, b))
            assert potential_work == dissipated
            dual = potential_work-F(2, 3)*dissipated
            assert dual == dissipated/3
            bound = sum(map(abs, b))
            upper = max(beta for beta, x, z, u, t in data)
            for beta, x, z, u, t in data:
                assert abs(x) <= bound
                assert z <= upper*bound**2
                assert u <= upper*bound
                assert t <= upper*bound**3
            assert max(map(abs, pi)) <= len(edges)*upper*bound**2
            states += 1
    print(f"PASS: {projection_checks} projected cone cases, {necessity_checks} "
          f"necessity controls, {states} exact complete-graph states, "
          f"{edge_checks} edge conjugate/cone witnesses, five interior constructions")


if __name__ == "__main__":
    run()
