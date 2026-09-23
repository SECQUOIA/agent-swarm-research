"""Independent exact finite checks, not proofs for unbounded parameters."""
from fractions import Fraction as Q
from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import re
import sympy as sp

ROOT = Path(__file__).resolve().parents[3]
SNAP = ROOT / 'process/snapshots/stage06-round01'
OUT = Path(__file__).resolve().parent
counts = {}

# All 4-by-4 candidate augmented signed moment matrices. Exact principal
# minors decide PSD; independently recover a finite sign distribution.
accepted = 0
for entries in product((-1, 0, 1), repeat=6):
    a = sp.eye(4)
    for (i, j), v in zip(combinations(range(4), 2), entries):
        a[i, j] = a[j, i] = v
    if any(a.extract(ix, ix).det() < 0
           for k in range(2, 5) for ix in combinations(range(4), k)):
        continue
    reps, cls, signs = [], [], []
    for i in range(4):
        matches = [(j, int(a[i, r])) for j, r in enumerate(reps) if a[i, r]]
        if matches:
            j, sign = matches[0]
        else:
            j, sign = len(reps), 1
            reps.append(i)
        cls.append(j)
        signs.append(sign)
    atoms = []
    for tail in product((-1, 1), repeat=len(reps)-1):
        xi = (1,) + tail
        atoms.append([signs[i]*xi[cls[i]] for i in range(4)])
    assert all(sum(Q(v[i]*v[j], len(atoms)) for v in atoms) == a[i,j]
               for i in range(4) for j in range(4))
    accepted += 1
counts['signed_matrix_candidates'] = 3**6
counts['signed_PSD_matrices_realized'] = accepted

# Exhaust all collections of distinct nonempty supports of size <=3 on
# four originals. Parity rank and the support-union bound are exact.
supports = [a for a in range(1,16) if a.bit_count() <= 3]
families = 0
for choose in range(1 << len(supports)):
    rows = [a for j,a in enumerate(supports) if choose >> j & 1]
    basis = {}
    union = 0
    for row in rows:
        union |= row
        v = row
        while v:
            p = v.bit_length()-1
            if p in basis:
                v ^= basis[p]
            else:
                basis[p] = v
                break
    q = len(basis)
    assert union.bit_count() <= 3*q
    # Every consistent right hand side is a fibre of this linear map.
    fibres = {}
    for t in range(16):
        rhs = tuple((t&a).bit_count() % 2 for a in rows)
        fibres[rhs] = fibres.get(rhs,0)+1
    assert len(fibres) == 2**q
    assert set(fibres.values()) == {2**(4-q)}
    families += 1
counts['parity_support_families'] = families

# The order-one cut is multiaffine on the full lifted box, so its
# nonnegativity at all vertices is an exact check for each chosen box.
xi,xj,xk,u,v,ai,aj,ak,h,b = sp.symbols('xi xj xk u v ai aj ak h b')
cut = 3*h/2-b*(u*(xk-ak)+ak*(xi*xj-ai*aj))/2
lhs = (1-b*v)/2-(1-b*ai*aj*ak)/2+3*h/2
assert sp.expand(lhs-cut+b*((v-u*xk)+ak*(u-xi*xj))/2) == 0
checked = 0
for M in (1,2,3,5):
    width = Q(2,M)
    for starts in product(range(M),repeat=3):
        corner = tuple(-1+width*s for s in starts)
        for bits in product((0,1),repeat=3):
            x = tuple(a+width*t for a,t in zip(corner,bits))
            for ue,sign in product((-1,1),repeat=2):
                residual = 3*width/2-Q(sign,2)*(ue*(x[2]-corner[2])+
                    corner[2]*(x[0]*x[1]-corner[0]*corner[1]))
                assert residual >= 0
                checked += 1
counts['order_one_full_box_vertices'] = checked

# Available-degree inequalities include the order-one D=2 boundary.
budgets = 0
for r,D in product(range(1,8),range(1,8)):
    if r*D < 2:
        continue
    assert 3 <= 2*r*D
    for generators in range(2*r+1):
        for square in range(r+1):
            if generators+2*square <= 2*r:
                assert D*(generators+square) <= 2*r*D
                budgets += 1
counts['degree_budgets'] = budgets
assert 384*3**24 < 2**64

# Independently replay the actual printed executable certificate text.
for file in ('appendix-finite-signings.tex','appendix-cubic-certificates.tex'):
    source = (SNAP/'sections'/file).read_text()
    blocks = re.findall(r'\\begin\{verbatim\}(.*?)\\end\{verbatim\}',source,re.S)
    exec(compile('\n'.join(blocks),file,'exec'),{})
counts['printed_finite_certificate_programs'] = 2
counts['snapshot_pdf_sha256'] = hashlib.sha256((SNAP/'main.pdf').read_bytes()).hexdigest()
counts['scope'] = 'Exact finite falsification checks only; no universal theorem or asymptotic source validation inferred.'
(OUT/'check_focus.json').write_text(json.dumps(counts,indent=2)+'\n')
print(json.dumps(counts,indent=2))
