"""Independent exact checks for reviewer07; finite checks do not prove asymptotics."""
from fractions import Fraction as Q
from itertools import product, combinations_with_replacement
from pathlib import Path
import hashlib
import json
import sympy as s

x, y, z, u, v, a, b, c, h, sign = s.symbols('x y z u v a b c h sign')
cut = 3*h/2-sign*(u*(z-c)+c*(x*y-a*b))/2
lhs = (1-sign*v)/2-(1-sign*a*b*c)/2+3*h/2
assert s.expand(lhs-cut+sign*((v-u*z)+c*(u-x*y))/2) == 0
assert s.Poly(cut,x,y,z,u,v).total_degree() == 2
assert s.expand(v-x*y*z-(v-u*z)-z*(u-x*y)) == 0
bernstein = 0
for bits in product((0,1), repeat=3):
    weight = s.prod((coord-low) if bit else (low+h-coord)
                    for coord,low,bit in zip((x,y,z),(a,b,c),bits))
    corner = s.prod(low+h*bit for low,bit in zip((a,b,c),bits))
    bernstein += (1-sign*corner)*weight
assert s.expand(bernstein-(1-sign*x*y*z)*h**3) == 0

endpoints = [Q(-1),Q(-1,2),Q(0),Q(1,2),Q(1)]
intervals = list(combinations_with_replacement(endpoints,2))
checks = 0
boxes = 0
for box in product(intervals, repeat=3):
    aa,bb,cc = [iv[0] for iv in box]
    hh = max(iv[1]-iv[0] for iv in box)
    boxes += 1
    for xx,yy,zz,uu,ss in product(*box,(-1,1),(-1,1)):
        qq=3*hh/2-ss*(uu*(zz-cc)+cc*(xx*yy-aa*bb))/2
        assert qq >= 0
        checks += 1

# Exact laws satisfying the two graph equations only in expectation.
# Every original graph point in these nodes has clause cost 1/2.
laws=[]
for t in [Q(1,32),Q(1,8),Q(1,2),Q(1)]:
    atoms=[(Q(0),Q(0),-t,Q(-1),t),(Q(0),Q(0),t,Q(1),t)]
    mean=lambda f: sum(map(f,atoms))/2
    assert mean(lambda p:p[3]-p[0]*p[1]) == 0
    assert mean(lambda p:p[4]-p[3]*p[2]) == 0
    assert all(p[3] != p[0]*p[1] for p in atoms)
    cost=mean(lambda p:(1-p[4])/2)
    assert cost == (1-t)/2 < Q(1,2)
    assert cost >= Q(1,2)-3*t
    laws.append({'t':str(t),'cost':str(cost),'graph_min':'1/2',
                 'all_atoms_outside_graph':True})

assert 384*3**24 < 2**64
assert Q(7,16*64) == Q(7,1024)
assert Q(7,16*64*3) == Q(7,3072)
assert Q(7,3072*17) == Q(7,52224)
assert s.ceiling(3/Q(1,16)) == 48

out={'arithmetic':'exact rational and symbolic',
     'symbolic_identities':['quadratic cut','cubic graph transfer','eight-corner Bernstein'],
     'boxes':boxes,'cut_vertex_checks':checks,'nongraph_laws':laws,
     'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
     'status':'PASS',
     'limits':'Finite cases supplement the universal derivations; no random-XOR or asymptotic verification.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
