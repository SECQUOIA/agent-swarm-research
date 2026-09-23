"""Independent exact checks of the stage-2 Max-Cut amplification."""
from fractions import Fraction as Q
from itertools import combinations, product

cases = pairs = scalar = 0
for n in range(1, 5):
    possible = list(combinations(range(n), 2))
    for mask in range(1 << len(possible)):
        edges = [e for i, e in enumerate(possible) if mask >> i & 1]
        vertices = list(product((0, 1), repeat=n))
        def f(x):
            return sum((x[i]-x[j])**2 for i,j in edges)
        v = max(vertices, key=f)
        M = f(v)
        assert f(tuple(1-x for x in v)) == M
        assert f((Q(1, 2),)*n) == 0
        for k in range(1, len(edges)+2):
            cases += 1
            tolerance = Q(2*k-1, 2)
            assert (M <= tolerance) == (M < k)
            if M < k:
                for x in vertices:
                    for w in (0, tolerance):
                        assert abs(w-f(x)) <= tolerance
                continue
            points = []
            for bits in product((0, 1), repeat=4):
                blocks = [tuple(1-x for x in v) if b else v for b in bits[:3]]
                points.append((blocks, bits[3]))
            for (a,za),(b,zb) in combinations(points,2):
                errors=[abs(Q(M,1)/tolerance-f(tuple(Q(x+y,2) for x,y in zip(aa,bb)))/tolerance) for aa,bb in zip(a,b)]
                errors.append(abs(4*(za*za+zb*zb)-8*Q(za+zb,2)**2))
                assert max(errors)>1
                pairs += 1
for beta in (0,1):
    for i in range(101):
        r=Q(i,100); z=(beta+r)/2; v=beta*r
        for s in (max(0,2*r-1),r,r*r):
            w=2*(beta+2*v+s)
            assert abs(w-8*z*z)<=Q(1,2)
            if s==r*r: assert w==8*z*z
            scalar += 1
print(f'PASS: {cases} graph/threshold cases, {pairs} augmented packing pairs, {scalar} scalar-lift checks')
