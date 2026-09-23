"""Exact checks for the forest incidence quotient and volume tiling proof.

Run with the repository's scientific Python environment. These finite checks
support, but do not replace, the proofs in the accompanying research note.
"""
from fractions import Fraction
import random
import sympy as sp

rng = random.Random(5092026)
cases = 0
minor_checks = 0
point_checks = 0
for n in range(2, 11):
    for sample in range(4):
        edges = [(i, rng.randrange(i)) for i in range(1, n)]
        if sample == 1:
            edges = [(i, i-1) for i in range(1, n)]
        if sample == 2:
            edges = [(i, 0) for i in range(1, n)]
        # Some cases have several components and isolated vertices.
        if sample == 3:
            edges = [e for e in edges if rng.randrange(3)]
        r = len(edges)
        if not r:
            continue
        B = sp.zeros(r, n)
        for k, (v, w) in enumerate(edges):
            B[k, v], B[k, w] = 1, -1
        assert B.rank() == r
        adjacency = [[] for _ in range(n)]
        for v, w in edges:
            adjacency[v].append(w)
            adjacency[w].append(v)
        remaining = set(range(n))
        components = []
        while remaining:
            stack = [min(remaining)]
            comp = set()
            while stack:
                v = stack.pop()
                if v in comp:
                    continue
                comp.add(v)
                stack.extend(adjacency[v])
            remaining -= comp
            components.append(sorted(comp))
        volume = Fraction(1, 2**r)
        for comp in components:
            volume *= len(comp)
            rows = [k for k, e in enumerate(edges) if e[0] in comp]
            for omitted in comp:
                M = B.extract(rows, [v for v in comp if v != omitted])
                assert abs(M.det()) == 1
                minor_checks += 1
        assert Fraction(1, 2**r) <= volume <= 1
        # Exact affine/quadratic quotient and componentwise canonical points.
        a = sp.Matrix([sp.Rational(rng.randrange(1, 9), 7) for _ in edges])
        H = B.T * sp.diag(*a) * B
        assert H.rank() == r
        for _ in range(8):
            x = sp.Matrix([sp.Rational(rng.randrange(21), 20) for _ in range(n)])
            canonical = x.copy()
            for comp in components:
                vmin = min(x[v] for v in comp)
                for v in comp:
                    canonical[v] -= vmin
            assert B * canonical == B * x
            assert all(0 <= v <= 1 for v in canonical)
            assert all(min(canonical[v] for v in comp) == 0 for comp in components)
            u = (B*x+sp.ones(r, 1))/2
            assert all(0 <= v <= 1 for v in u)
            original = (x.T*H*x)[0]/2
            diagonal = sum(a[k]*(2*u[k]-1)**2/2 for k in range(r))
            assert original == diagonal
            y = sp.Matrix([sp.Rational(rng.randrange(21), 20) for _ in range(n)])
            v = (B*y+sp.ones(r, 1))/2
            q = lambda z: sum(a[k]*(2*z[k]-1)**2/2 for k in range(r))
            assert (q(u)+q(v))/2-q((u+v)/2) == sum(4*a[k]*(u[k]-v[k])**2/8 for k in range(r))
            point_checks += 1
        cases += 1
print(f'PASS: {cases} exact forest cases, {minor_checks} incidence minors, {point_checks} quotient/Jensen/canonical-representative checks')
