"""Independent exact arithmetic checks supporting reviewer12's stage4 review.
Finite samples corroborate the report's analytic proofs; they are not proofs.
"""
from fractions import Fraction as Q
from itertools import product
from math import comb

counts = {}
# Full middle integer section: all triples of box vertices, sampled outer weights.
A, c = Q(7,4), Q(1,48)
L, d = A*(1-c)**32, A*c**32
assert A-1 < L < 1 and d < Q(1,4) and (A+d)/2 < 1
boxes = [list(product((0,c),(L,A),(0,d))),
         list(product((c,1-c),(0,L),(0,L))),
         list(product((1-c,1),(0,d),(L,A)))]
n = 0
for vertices in product(*boxes):
    for k in range(9):
        t = Q(k,16)
        point = [t*vertices[0][j]+(1-2*t)*vertices[1][j]+t*vertices[2][j] for j in range(3)]
        x, y1, y2 = point
        assert c <= x <= 1-c
        assert abs(y1-A*(1-x)**32) < 1
        assert abs(y2-A*x**32) < 1
        n += 1
counts['middle_section_vertex_mixtures'] = n
for a,b in [(Q(0),Q(1,2)),(Q(1,2),Q(1)),(Q(0),Q(1))]:
    gaps=[]
    for t in [Q(1,3),Q(2,3)]:
        x=(1-t)*a+t*b
        gaps += [(1-t)*A*(1-a)**32+t*A*(1-b)**32-A*(1-x)**32,
                 (1-t)*A*a**32+t*A*b**32-A*x**32]
    assert max(gaps)>1
counts['thirds_incompatible_pairs']=3
# Simplex band's two norm estimates, including zero and extreme vectors.
n=0
for dim in range(1,6):
    vectors=[tuple(Q(k,6) for k in v) for v in product(range(4),repeat=dim) if sum(v)<=3]
    for g,v in product(vectors,repeat=2):
        error=[a-b for a,b in zip(g,v)]
        assert sum(abs(e) for e in error)<=1
        assert sum(e*e for e in error)<=Q(1,2)
        n+=1
counts['simplex_errors']=n
# Exact second-difference identity on monomials: integral of triangular kernel.
n=0
for degree in range(2,41):
    a,h=Q(1,2),Q(1,8)
    rhs=Q(0)
    for k in range(degree-1):
        if k%2==0:
            rhs += degree*(degree-1)*comb(degree-2,k)*a**(degree-2-k)*2*h**(k+2)/((k+1)*(k+2))
    assert (a-h)**degree-2*a**degree+(a+h)**degree==rhs
    n+=1
counts['second_difference_identities']=n
for M in range(2,101):
    h=Q(1,2*M)
    curvature=Q(15,8)/(h*h)
    assert curvature==Q(15,2)*M*M
    assert 8*(1+curvature)==8+60*M*M
counts['tilted_radius_lower_bounds']=99
# Compiled oracle error and integer-count margins.
assert Q(13,64)+Q(1,16)==Q(17,64)
assert Q(17,64)+Q(1,2)==Q(49,64)<1
for factor,power in [(486*8,12),(486*16,13),(486*28,14),(486*144,17),
                     (5832*15,17),(5832*27,18),(5832*219,21)]:
    assert factor < 2**power
counts['compiled_count_constants']=7
print(counts)
