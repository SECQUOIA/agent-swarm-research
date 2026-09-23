"""Independent finite checks. Universal arguments are in the review report."""
from collections import Counter
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import hashlib
import json
import sympy as s

supports = [v for v in range(1, 32) if v.bit_count() <= 3]
families = 0
fibers = 0
for rows in product(supports, repeat=3):
    span = {0}
    basis = []
    for row in rows:
        if row not in span:
            basis.append(row)
            span |= {v ^ row for v in tuple(span)}
    union = rows[0] | rows[1] | rows[2]
    basis_union = 0
    for row in basis:
        basis_union |= row
    assert union == basis_union
    assert union.bit_count() <= 3 * len(basis)
    counts = Counter(tuple((t & row).bit_count() % 2 for row in rows) for t in range(32))
    assert len(counts) == 2 ** len(basis)
    assert set(counts.values()) == {2 ** (5-len(basis))}
    for signs in product(range(2), repeat=3):
        signed = {tuple(x ^ y for x, y in zip(rhs, signs)): value for rhs, value in counts.items()}
        assert len(signed) == len(counts)
        fibers += len(signed)
    # Repeating a row arbitrarily adds no equation or original support.
    assert all(row in span for row in rows * 101)
    families += 1

x, y, z, u, v, a, b, c, h, sign, beta = s.symbols('x y z u v a b c h sign beta')
cost = (1-sign*x*y*z)/2
cut = 3*h/2-sign*(u*(z-c)+c*(x*y-a*b))/2
identity = (1-sign*v)/2-(1-sign*a*b*c)/2+3*h/2
assert s.expand(identity-cut+sign*((v-u*z)+c*(u-x*y))/2) == 0
assert s.expand(v-x*y*z-(v-u*z)-z*(u-x*y)) == 0
bernstein = 0
for corner in product(range(2), repeat=3):
    coeff = cost.subs({x:a+h*corner[0], y:b+h*corner[1], z:c+h*corner[2]})-beta
    term = coeff
    for var, low, bit in zip((x,y,z),(a,b,c),corner):
        term *= var-low if bit else low+h-var
    bernstein += term
assert s.expand(bernstein-h**3*(cost-beta)) == 0

vertex_cases = 0
for width in (Q(1,4), Q(1,2), Q(1), Q(2)):
    lows = [Q(-1), -width/2, 1-width]
    for lower in product(lows, repeat=3):
        for corner in product(range(2), repeat=3):
            point = [low+width*bit for low,bit in zip(lower,corner)]
            for aux,sgn in product((-1,1), repeat=2):
                aa,bb,cc = lower
                xx,yy,zz = point
                q = 3*width/2-Q(sgn,2)*(aux*(zz-cc)+cc*(xx*yy-aa*bb))
                assert q >= 0
                vertex_cases += 1

assert 384*3**24 < 2**64
assert Q(7,16*64) == Q(7,1024)
assert Q(7,16*64*3*17) == Q(7,52224)
assert 3/Q(1,16) == 48
out = {'kind':'exact finite enumeration and symbolic identities',
       'ordered_three_row_families_n5_D3':families,
       'consistent_signed_fibers':fibers,
       'quadratic_cut_vertex_cases':vertex_cases,
       'symbolic_identities':3,
       'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
       'result':'PASS',
       'limit':'Does not establish asymptotic XOR existence or universal rank/certificate theorems.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
