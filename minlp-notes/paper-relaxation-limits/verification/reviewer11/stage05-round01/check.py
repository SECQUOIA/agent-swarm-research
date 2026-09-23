"""Independent exact Stage 5 checks; finite degree cases are not universal proofs."""
from fractions import Fraction
from itertools import product
from pathlib import Path
import hashlib
import json
import sympy as s

x, y, z, u, v, a, b, c, h, sign, beta = s.symbols('x y z u v a b c h sign beta')
q = 3*h/2-sign*(u*(z-c)+c*(x*y-a*b))/2
lhs = (1-sign*v)/2-(1-sign*a*b*c)/2+3*h/2
assert s.expand(lhs-q+sign*((v-u*z)+c*(u-x*y))/2) == 0
assert s.Poly(q,x,y,z,u,v).total_degree() == 2
assert s.expand(v-x*y*z-((v-u*z)+z*(u-x*y))) == 0
bernstein = 0
for bits in product((0,1), repeat=3):
    corner = (a+h*bits[0])*(b+h*bits[1])*(c+h*bits[2])
    weight = s.prod(t-lo if bit else lo+h-t for t,lo,bit in zip((x,y,z),(a,b,c),bits))
    bernstein += ((1-sign*corner)/2-beta)*weight
assert s.expand(h**3*((1-sign*x*y*z)/2-beta)-bernstein) == 0

degree_cases = 0
for r,D in product(range(1,13),range(1,9)):
    if r*D < 2:
        continue
    assert 3 <= 2*r*D and 6 <= 4*r*D
    for generator_degree in range(2*r+1):
        for square_degree in range((2*r-generator_degree)//2+1):
            assert 2*D*(generator_degree+square_degree) <= 4*r*D
            assert D*(generator_degree+2*square_degree) <= 2*r*D
            degree_cases += 1

# Test the full-box cut on unequal-width boxes, including degenerate ones.
# Its multiaffinity in x,y,z,u means vertices suffice for each selected box.
intervals = [(Fraction(-1),Fraction(-1)), (Fraction(-1),Fraction(-2,3)),
             (Fraction(-1,3),Fraction(1,4)), (Fraction(1,2),Fraction(1))]
vertex_cases = 0
for box in product(intervals,repeat=3):
    lo = tuple(t[0] for t in box)
    width = max(t[1]-t[0] for t in box)
    for xx,yy,zz,uu,sgn in product(*box,(-1,1),(-1,1)):
        val = 3*width/2-sgn*(uu*(zz-lo[2])+lo[2]*(xx*yy-lo[0]*lo[1]))/2
        assert val >= 0
        vertex_cases += 1

assert 384*3**24 < 2**64
assert Fraction(7,16*64) == Fraction(7,1024)
assert Fraction(7,16*64*3) == Fraction(7,3072)
assert Fraction(7,3072*17) == Fraction(7,52224)
sources = {
 'schoenebeck': '/tmp/minlp-relaxation-limits-sources/schoenebeck-full.pdf',
 'disjunctive': '/home/sgusev/repo/minlp-notes/literature/papers/ahmadi2026-disjunctive-sum-of-squares/original.pdf',
 'stabbing': '/tmp/stage05-author-sources/stabbing.pdf',
 'branchcut': '/tmp/stage05-author-sources/branch-cut.pdf',
}
record = {'exact': True, 'symbolic_identities': 3, 'degree_cases': degree_cases,
          'full_box_vertex_cases': vertex_cases,
          'limits': 'Finite degree cases do not prove universal budgets; source hashes are identity checks, not proof checks.',
          'source_sha256': {key: hashlib.sha256(Path(path).read_bytes()).hexdigest() for key,path in sources.items()}}
Path(__file__).with_name('result.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
