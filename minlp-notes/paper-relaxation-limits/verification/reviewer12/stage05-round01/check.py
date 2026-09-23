"""Independent exact finite checks; not a proof of asymptotic XOR width."""
from collections import Counter
from fractions import Fraction as Q
from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import sympy as s

out = {}

def basis(rows):
    pivots = {}
    originals = []
    for row in rows:
        reduced = row
        while reduced:
            pivot = reduced.bit_length() - 1
            if pivot in pivots:
                reduced ^= pivots[pivot]
            else:
                pivots[pivot] = reduced
                originals.append(row)
                break
    return originals

supports = [i for i in range(1, 32) if i.bit_count() <= 3]
families = 0
for k in range(5):
    for family in combinations(supports, k):
        # Repetition changes neither rank nor fibers, but must be retained.
        rows = family + family[:2]
        selected = basis(rows)
        union = lambda rr: sum(1 << j for j in range(5) if any(x & (1 << j) for x in rr))
        assert union(rows) == union(selected)
        assert union(rows).bit_count() <= 3 * len(selected)
        fibers = Counter(tuple((t & row).bit_count() % 2 for row in rows) for t in range(32))
        assert len(fibers) == 2 ** len(selected)
        assert set(fibers.values()) == {2 ** (5 - len(selected))}
        families += 1
out['rank_families_with_duplicate_rows'] = families

# Formal identities in the polynomial ring, not just on graph points.
x, y, z, u, v, a, b, c, h, sign, beta = s.symbols('x y z u v a b c h sign beta')
cut = 3*h/2 - sign*(u*(z-c) + c*(x*y-a*b))/2
clause = (1-sign*v)/2
corner = (1-sign*a*b*c)/2
assert s.expand(clause-corner+3*h/2-cut+sign*((v-u*z)+c*(u-x*y))/2) == 0
assert s.expand(v-x*y*z-(v-u*z)-z*(u-x*y)) == 0
bernstein = 0
for bits in product((0, 1), repeat=3):
    value = (1-sign*s.prod(aa+h*bb for aa, bb in zip((a,b,c), bits)))/2
    basis_poly = s.prod(xx-aa if bb else aa+h-xx for xx,aa,bb in zip((x,y,z),(a,b,c),bits))
    bernstein += (value-beta)*basis_poly
assert s.expand(h**3*((1-sign*x*y*z)/2-beta)-bernstein) == 0
out['formal_identities'] = ['quadratic_cut', 'cubic_graph_transfer', 'eight_corner_Bernstein']

# The quadratic cut is multiaffine in its four active coordinates, so
# exact vertex checking checks each selected full box, not only its graph.
vertex_cases = 0
box_cases = 0
for width in (Q(1,4), Q(1,2), Q(1), Q(2)):
    starts = [Q(j,4) for j in range(-4,5) if Q(j,4)+width <= 1]
    for lower in product(starts, repeat=3):
        aa,bb,cc = lower
        for xx,yy,zz,uu,ss in product((aa,aa+width),(bb,bb+width),(cc,cc+width),(-1,1),(-1,1)):
            q = 3*width/2 - ss*(uu*(zz-cc)+cc*(xx*yy-aa*bb))/2
            assert q >= 0
            vertex_cases += 1
        box_cases += 1
out['quadratic_full_box_checks'] = {'boxes':box_cases, 'signed_vertices':vertex_cases}

# A rational two-atom full-box distribution: both graph equations hold
# only in expectation, and its objective is below every graph point.
atoms = [(Q(5,8), (Q(1,2),Q(1,2),Q(3,4),Q(1),Q(9,32))),
         (Q(3,8), (Q(1,2),Q(1,2),Q(1,2),Q(-1),Q(9,32)))]
expect = lambda f: sum(weight*f(*point) for weight,point in atoms)
assert expect(lambda x,y,z,u,v:u-x*y) == 0
assert expect(lambda x,y,z,u,v:v-u*z) == 0
assert all(point[3] != point[0]*point[1] for _,point in atoms)
value = expect(lambda x,y,z,u,v:(1-v)/2)
graph_min = (1-Q(1,2)*Q(1,2)*Q(3,4))/2
assert value == Q(23,64) < graph_min == Q(13,32)
assert value >= (1-Q(1,2)**3)/2 - 3*Q(1,4)/2
out['nongraph_two_atom_law'] = {'objective':str(value), 'true_graph_minimum':str(graph_min),
                              'graph_equation_moments':'both zero', 'off_graph_mass':'1'}

# Exhaust every low-width signed closure on four originals, and test
# a width-three inconsistent six-variable formula separately.
def closure(clauses, width):
    derived = {(0,1), *clauses}
    while True:
        added = {(a^b, sa*sb) for a,sa in derived for b,sb in derived if (a^b).bit_count() <= width}
        if added <= derived:
            return derived
        derived |= added

checked = 0
triples = [i for i in range(16) if i.bit_count() == 3]
for signs in product((0,-1,1), repeat=4):
    clauses = [(row,sign) for row,sign in zip(triples,signs) if sign]
    for width in (3,4):
        derived = closure(clauses,width)
        if (0,-1) in derived:
            continue
        moments = dict(derived)
        idx = [i for i in range(16) if i.bit_count() <= width//2]
        gram = s.Matrix([[moments.get(i^j,0) for j in idx] for i in idx])
        assert gram.is_positive_semidefinite
        assert all(gram[0,idx.index(row)] == sign for row,sign in clauses if row in idx)
        checked += 1
clauses6 = [(7,1),(25,1),(42,1),(52,-1)]
assert (0,-1) not in closure(clauses6,3)
assert (0,-1) in closure(clauses6,4)
assert s.Matrix([[dict(closure(clauses6,3)).get(i^j,0) for j in [0,1,2,4,8,16,32]]
                 for i in [0,1,2,4,8,16,32]]) == s.eye(7)
out['signed_closure_cases'] = checked
out['odd_width_inconsistent_example'] = 'width 3: identity Gram, nonzero cubic moments; width 4: contradiction'

# Both halfspace boundaries and all substitution sign sums, exactly.
negative_cases = 0
for n in range(1,11):
    counts = Counter(sum(w) for w in product((-1,1),repeat=n))
    assert sum(k*v for k,v in counts.items()) == 0
    assert sum(k*k*v for k,v in counts.items()) == n*2**n
    assert 2*sum(v for k,v in counts.items() if k >= 0) >= 2**n
    for r in range(1,n+3):
        for t in range(min(r-1,(n+1)//2)):
            for fixed_sum in range(-t,t+1,2):
                selected = 0 if fixed_sum < 0 else fixed_sum+1
                val = sum(Q(fixed_sum+sum(w),2**(n-t)) for w in product((-1,1),repeat=n-t)
                          if all(w[j] == -1 for j in range(selected)))
                assert 1+2*selected <= 2*r and val < 0
                if fixed_sum >= 0:
                    assert val == -Q(1,2**selected)
                negative_cases += 1
out['negative_halfspace_localizers'] = negative_cases
assert 384*3**24 < 2**64
assert Q(7,16*64) == Q(7,1024)
assert Q(7,16*64*3*17) == Q(7,52224)
assert 3/Q(1,16) == 48
out['arithmetic'] = 'integer/rational/symbolic; no numerical tolerances'
out['script_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
Path(__file__).with_name('results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
