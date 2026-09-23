"""Reviewer 10 exact falsification checks; finite evidence, not universal proofs.

Run from any directory with Python 3.10+. Writes only the adjacent result.json.
The final two replays use frozen author code and are labelled as replays.
"""
from fractions import Fraction as F
from itertools import product
from math import comb
from pathlib import Path
import contextlib
import io
import json
import random
import re
import runpy

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SNAP = ROOT / 'process/snapshots/stage06-round01'
rng = random.Random(610)

def generator_check(r, c):
    n = len(r)
    m = n // 2
    S = sum(r)
    assert S == sum(c) and S > 0
    W = [[x*y/S for y in c] for x in r]
    B = sum(W[i][m+i] for i in range(m))
    D = 1-sum(W[i][i] for i in range(n))
    g = m-S+(2*m+1)*B+(4*m+1)*D
    assert g >= B+D >= 0
    a = [int(x >= F(1,2)) for x in r]
    b = a[:]
    for i in range(m):
        if b[i] == b[m+i]:
            b[i], b[m+i] = 1, 0
    dist = sum(abs(W[i][j]-F(b[i]*b[j],m))
               for i in range(n) for j in range(n))
    assert dist <= 4*S*B+58*S*D+5*abs(S-m)
    assert dist <= (136*m+10)*g
    assert dist <= 28*m*B+156*m*D+5*(m-S)
    return B, D, g

counts = {}
for m in (1, 2):
    groups = {}
    for v in product((F(0),F(1,2),F(1)), repeat=2*m):
        if sum(v):
            groups.setdefault(sum(v), []).append(v)
    count = 0
    for group in groups.values():
        for r,c in product(group, repeat=2):
            generator_check(r,c)
            count += 1
    counts[str(m)] = count

random_count = 0
for m in range(1,9):
    for _ in range(120):
        r = [F(rng.randrange(21),20) for _ in range(2*m)]
        c = r[:]
        rng.shuffle(c)
        # Transfer rational mass between two coordinates without changing total.
        for _ in range(2*m):
            i,j = rng.sample(range(2*m),2)
            delta = min(c[i],1-c[j])*F(rng.randrange(11),10)
            c[i] -= delta
            c[j] += delta
        if sum(r):
            generator_check(r,c)
            random_count += 1

atom_count = 0
for m in range(1,9):
    for x in product((0,1), repeat=m):
        b = list(x)+[1-a for a in x]
        B,D,g = generator_check(list(map(F,b)),list(map(F,b)))
        assert B == D == g == 0
        X = [[x[i]*x[j] for j in range(m)] for i in range(m)]
        inverse = [[F(X[i][j],m) for j in range(m)] +
                   [F(x[i]-X[i][j],m) for j in range(m)] for i in range(m)]
        inverse += [[F(x[j]-X[i][j],m) for j in range(m)] +
                    [F(1-x[i]-x[j]+X[i][j],m) for j in range(m)] for i in range(m)]
        assert inverse == [[F(b[i]*b[j],m) for j in range(2*m)] for i in range(2*m)]
        atom_count += 1

pseudo = []
for k in range(3,32,2):
    # The symmetric Lagrange density representing evaluation at weight k/2.
    weights = []
    for j in range(k+1):
        lagrange = F(1)
        for i in range(k+1):
            if i != j:
                lagrange *= F(F(k,2)-i,j-i)
        weights.append(lagrange)
    densities = [w/F(comb(k,j),2**k) for j,w in enumerate(weights)]
    f = [(F(j)-F(k,2))**2/F(k*k)-F(1,4*k*k) for j in range(k+1)]
    assert sum(weights) == 1
    assert max(abs(d) for d in densities)**2 <= k**3
    assert sum(w*v for w,v in zip(weights,f)) == -F(1,4*k*k)
    theta = F(1,8*k*k)
    assert all(0 <= v+theta <= 1 for v in f)
    assert sum(w*(v+theta) for w,v in zip(weights,f)) == -F(1,8*k*k)
    mean = sum(F(comb(k,j),2**k)*(f[j]+theta) for j in range(k+1))
    assert mean >= F(1,6*k)
    pseudo.append(k)

iterations = {}
for n in range(1,4):
    b=F(1,2**(2**n)); c=1-b
    z=w=F(0)
    affine=0
    while z < F(1,2):
        assert 0 <= w <= c*z <= c
        w=max(w,c*z)
        z,w=max(z,b+w),max(w,z-b)
        affine += 1
        assert w <= c*z and z <= affine*b
    assert affine >= 2**(2**n-1)
    iterations[str(n)] = affine

capture = io.StringIO()
with contextlib.redirect_stdout(capture):
    printed = (SNAP/'sections/appendix-finite-signings.tex').read_text()
    code = re.search(r'\\begin\{verbatim\}(.*?)\\end\{verbatim\}',printed,re.S).group(1)
    exec(compile(code,'frozen printed finite-signing program','exec'),{})
    runpy.run_path(str(SNAP/'verification/check_stage02_finite.py'))

result = {'arithmetic':'Exact Python integers and fractions throughout',
          'exhaustive_half_grid_generator_counts':counts,
          'seeded_rational_generator_count':random_count,
          'paired_atoms_checked':atom_count,
          'odd_pseudo_density_sizes':pseudo,
          'alternating_primitive_first_half_iteration':iterations,
          'frozen_author_code_replay_stdout':capture.getvalue(),
          'limits':'Finite rounding tests do not prove stability. Pseudo-density tests verify normalization, norm and shifted moments, not positivity on every low-degree square. One alternating FBBT schedule does not prove the every-schedule theorem. Signing and cubic portions replay frozen author code.'}
(HERE/'result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
