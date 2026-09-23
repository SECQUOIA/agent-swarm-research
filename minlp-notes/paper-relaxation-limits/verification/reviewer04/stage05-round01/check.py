"""Independent exact checks for reviewer04. Finite checks supplement the proofs."""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import hashlib
import json
import sympy as s

out = {}
cases = 0
# Constant class 0 is deterministic; two other classes are independent signs.
for allocation in product(range(3), repeat=5):
    for orientation in product((-1, 1), repeat=5):
        rows = []
        for a, b in product((-1, 1), repeat=2):
            vals = (1, a, b)
            rows.append((1,) + tuple(t * vals[c] for t, c in zip(orientation, allocation)))
        classes, signs = (0,) + allocation, (1,) + orientation
        for i in range(6):
            for j in range(6):
                expected = signs[i] * signs[j] if classes[i] == classes[j] else 0
                assert sum(row[i]*row[j] for row in rows) == 4*expected
        cases += 1
out['signed_augmented_matrices'] = cases

# A concrete signed-class law can leave the graph despite matching ALL
# first/second moments of a graph-supported law, and both graph equations.
nongraph = []
for b in (-1, 1):
    graph = [(1, x, y, z, x*y, b) for x, y, z in product((-1, 1), repeat=3) if x*y*z == b]
    box = [(1, x, y, z, b*z, b) for x, y, z in product((-1, 1), repeat=3)]
    moment = lambda rows, i, j: Q(sum(row[i]*row[j] for row in rows), len(rows))
    assert all(moment(graph, i, j) == moment(box, i, j) for i in range(6) for j in range(6))
    assert sum(row[4]-row[1]*row[2] for row in box) == 0
    assert sum(row[5]-row[4]*row[3] for row in box) == 0
    failures = sum(row[4] != row[1]*row[2] for row in box)
    residual_square = Q(sum((row[4]-row[1]*row[2])**2 for row in box), len(box))
    assert failures == 4 and residual_square == 2
    nongraph.append({'sign': b, 'atoms': 8, 'off_graph_atoms': failures,
                     'graph_equation_squared_expectation': str(residual_square)})
out['nongraph_realization'] = nongraph

x, y, z, u, v, ai, aj, ak, h, b = s.symbols('x y z u v ai aj ak h b')
q = 3*h/2-b*(u*(z-ak)+ak*(x*y-ai*aj))/2
lhs = (1-b*v)/2-(1-b*ai*aj*ak)/2+3*h/2
rhs = q-b*((v-u*z)+ak*(u-x*y))/2
assert s.expand(lhs-rhs) == 0
assert s.Poly(q, x, y, z, u, v).total_degree() == 2
assert s.expand(v-x*y*z-((v-u*z)+z*(u-x*y))) == 0
out['quadratic_and_cubic_graph_identities'] = 'exact symbolic pass'

beta = s.symbols('beta')
bernstein = 0
for bits in product((0, 1), repeat=3):
    corner = (1-b*(ai+h*bits[0])*(aj+h*bits[1])*(ak+h*bits[2]))/2
    basis = s.prod((coord-a if bit else a+h-coord)
                   for coord, a, bit in zip((x,y,z),(ai,aj,ak),bits))
    bernstein += (corner-beta)*basis
assert s.expand(bernstein-h**3*((1-b*x*y*z)/2-beta)) == 0
out['bernstein_identity'] = 'exact symbolic pass'

# Validity of the quadratic upper-certificate cut on selected full boxes,
# including singleton original intervals and auxiliaries that leave the graph.
grid = (Q(-1), Q(-1,2), Q(0), Q(1,2), Q(1))
intervals = [(a,c) for a in grid for c in grid if a <= c]
checks = 0
for ivs in product(intervals, repeat=3):
    corner = tuple(iv[0] for iv in ivs)
    width = max(c-a for a,c in ivs)
    for xyz in product(*ivs):
        for sign, aux in product((-1,1), repeat=2):
            aa,ab,ac = corner
            xx,yy,zz = xyz
            cut = 3*width/2-sign*(aux*(zz-ac)+ac*(xx*yy-aa*ab))/2
            assert cut >= 0
            checks += 1
out['exact_full_box_quadratic_vertex_checks'] = checks
assert 384*3**24 < 2**64
assert Q(7,16*64) == Q(7,1024)
assert Q(7,16*64*3*17) == Q(7,52224)
out['constants'] = 'exact integer/rational pass'
out['limits'] = 'Finite checks do not prove the universal transfer or random-width theorem.'
out['script_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
Path(__file__).with_suffix('.json').write_text(json.dumps(out, indent=2)+'\n')
print(json.dumps(out, indent=2))
