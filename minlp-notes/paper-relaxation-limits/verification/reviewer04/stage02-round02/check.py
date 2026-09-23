"""Independent exact finite checks; universal claims require the written proofs."""
from fractions import Fraction as Q
from itertools import product, combinations_with_replacement
from math import comb, prod
from pathlib import Path
import contextlib
import io
import json
import re
import sympy as S

HERE = Path(__file__).resolve().parent
SNAP = HERE.parents[2] / 'process/snapshots/stage02-round02'
results = {}

# Replay precisely both printed blocks, checking them against the frozen file.
tex = (SNAP / 'sections/appendix-cubic-certificates.tex').read_text()
blocks = re.findall(r'\\begin\{verbatim\}\n(.*?)\\end\{verbatim\}', tex, re.S)
assert len(blocks) == 2
printed = ''.join(blocks)
assert printed == (SNAP / 'verification/check_stage02_finite.py').read_text()
with contextlib.redirect_stdout(io.StringIO()) as stream:
    exec(compile(printed, 'frozen printed checker', 'exec'), {})
results['printed_checker'] = stream.getvalue().splitlines()

# Independently integrate O and B, rather than reuse their claimed deficiency formulas.
def orientation_intersection(xs):
    total = Q(0)
    for bits in product((0, 1), repeat=len(xs)):
        intervals = [(Q(0), x) if bit == 0 else (1-x, Q(1))
                     for x, bit in zip(xs, bits)]
        total += max(Q(0), min(b for a, b in intervals)-max(a for a, b in intervals))
    return total / 2**len(xs)

def b_intersection(xs):
    breaks = sorted({Q(0), Q(1)} | {x if x <= Q(1,2) else 2*(1-x) for x in xs})
    total = Q(0)
    for lo, hi in zip(breaks, breaks[1:]):
        t = (lo+hi)/2
        probabilities = [(Q(t <= x) if x <= Q(1,2)
                          else Q(1,2) if t <= 2*(1-x) else Q(1)) for x in xs]
        total += (hi-lo)*prod(probabilities)
    return total

grid = [Q(i, 12) for i in range(13)] + [Q(499,1000), Q(501,1000), Q(999,1000)]
grid = sorted(set(grid))
for x in grid:
    assert orientation_intersection([x]) == b_intersection([x]) == x
tested = 0
for k in (2,3):
    for xs in combinations_with_replacement(grid, k):
        u = xs[0]
        gap = u-max(Q(0), sum(xs)-k+1)
        do, di, db = (u-orientation_intersection(xs), u-prod(xs), u-b_intersection(xs))
        assert min(do, di, db) >= 0
        assert 18*do+6*di+7*db >= 12*gap
        assert do >= (1-Q(1,2**(k-1)))/(k-1)*gap
        tested += 1
results['exact_cubic_and_bilinear_marginal_tuples'] = tested

# Exact dyadic resource-law checks, including ties and actual XOR marginals.
cutoffs = 0
xor_states = 0
for L in range(2,13):
    m = 2**L
    weights = [Q(1,2**(l+1)) if l < L else Q(1,m) for l in range(L+1)]
    assert sum(weights) == 1
    for j in range(1,L+1):
        assert sum(weights[j:]) == Q(1,2**j)
    B = lambda q: Q(L-q+2,2**q)
    for s in range(1,L):
        if not B(s+1) <= 1 <= B(s):
            continue
        cutoffs += 1
        theta = (1-B(s+1))/(B(s)-B(s+1))
        assert 0 <= theta <= 1
        er = gain = Q(0)
        for q, prob in ((s,theta),(s+1,1-theta)):
            for l, mass in enumerate(weights):
                r = 0 if l < q else 2**(l-q+1)
                assert r <= m
                er += prob*mass*r
                gain += prob*mass*sum(min(2**j,r) for j in range(1,l+1))
                if L <= 6:
                    failed = [int(f'{i:0{L}b}'[::-1],2) for i in range(r)]
                    for j in range(1,L+1):
                        assert len({i >> (L-j) for i in failed}) == min(2**j,r)
                    for leaf in range(m):
                        assert sum(leaf in {i^shift for i in failed} for shift in range(m)) == r
                    xor_states += 1
        assert er == 1
        target = s+Q(L-s,2**s)
        assert gain == target
        for l in range(L+1):
            intercept = 0 if l <= s else 2**(l-s+1)-2
            for r in range(m+1):
                assert sum(min(2**j,r) for j in range(1,l+1)) <= s*r+intercept
results['dyadic_cutoffs_L2_to_L12'] = cutoffs
results['dyadic_XOR_profile_states_L2_to_L6'] = xor_states

# Independently derive the eliminated quartics and reconstruct the printed Bernstein rows.
a,b,c,t = S.symbols('a b c t')
F = 6*c**3+27*b*c**2+18*b**2+30*a*c+20*a*b+9*a**2
ell = 37*a+S.Rational(79,2)*b+38*c-S.Rational(103,3)
h = F-ell
p = S.expand(h.subs({a:1,b:S.Rational(13,24)-3*c**2/4}))
stationary = S.solve([S.diff(h,a), S.diff(h,b)], (a,b))
r = S.expand(h.subs(stationary))
rows = [(p,0,S.Rational(1,5),60000,[63125,39125,20975,9395,4133]),
        (p,S.Rational(1,5),S.Rational(3,10),240000,[16532,6008,1802,3788,11597]),
        (r,S.Rational(3,10),S.Rational(1,2),7440000,[215357,1285415,1434125,1250375,1008125]),
        (r,S.Rational(1,2),S.Rational(3,4),190464,[25808,18056,7964,9230,15869]),
        (r,S.Rational(3,4),1,190464,[15869,22508,34520,45920,31040])]
for polynomial,lo,hi,D,values in rows:
    bernstein = sum(S.Rational(v,D)*comb(4,i)*t**i*(1-t)**(4-i) for i,v in enumerate(values))
    assert S.expand(polynomial.subs(c,lo+(hi-lo)*t)-bernstein) == 0
delta = min(Q(v,D) for polynomial,lo,hi,D,values in rows for v in values)
assert delta == Q(901,120000)
assert Q(161,4)/(Q(223,12)-delta) == Q(1610000,743033)
results['Bernstein_uniform_slack'] = str(delta)

for coefficient,la,lc,l0,center,tail,atoms,mean,val in [
    (S.Rational(5,4),S.Rational(11,6),S.Rational(20,27),-S.Rational(95,108),
     (11-6*c*c)/15,(1-c)*(3*c-2)**2*(3*c+7)/135,
     [(Q(1,4),Q(1,3),Q(1)),(Q(3,4),Q(5,9),Q(2,3))],(Q(1,2),Q(3,4)),Q(16,27)),
    (S.Rational(24,25),S.Rational(41,25),S.Rational(4,5),-S.Rational(68,75),
     (41-25*c*c)/48,(1-c)*(5*c-3)**2*(5*c+11)/480,
     [(Q(1,2),Q(1,3),Q(1)),(Q(1,2),Q(2,3),Q(3,5))],(Q(1,2),Q(4,5)),Q(83,150))]:
    expression = a*c*c+coefficient*a*a
    assert S.expand(expression-la*a-lc*c-l0-coefficient*(a-center)**2-tail) == 0
    assert sum(w for w,x,y in atoms) == 1
    assert tuple(sum(w*point[j] for w,*point in atoms) for j in (0,1)) == mean
    assert sum(w*expression.subs({a:x,c:y}) for w,x,y in atoms) == val
results['two_level_scalar_identities_and_atom_laws'] = 2

# Exact direct enumeration of the adjacent-count law's singleton and subset products.
equal_cases = 0
for n in range(2,9):
    for u in [Q(j,10) for j in range(1,10)]:
        nu = n*u
        floor = nu.numerator//nu.denominator
        theta = nu-floor
        law = {}
        for bits in product((0,1),repeat=n):
            k = sum(bits)
            law[bits] = ((1-theta)/comb(n,k) if k == floor else theta/comb(n,k) if k == floor+1 else 0)
        assert sum(law.values()) == 1
        assert all(sum(mass*bits[i] for bits,mass in law.items()) == u for i in range(n))
        for d in range(2,n+1):
            q = ((1-theta)*comb(floor,d)+theta*comb(floor+1,d))/comb(n,d)
            assert sum(mass*prod(bits[:d]) for bits,mass in law.items()) == q
            assert q <= u**d < u
            equal_cases += 1
results['equal_mean_subset_checks'] = equal_cases
assert Q(3131,2275)-Q(1,2) == Q(3987,4550) > 0
assert 25002-Q(1000**3,23200) < 0
results['finite_sampling_margin'] = '3987/4550'
results['status'] = 'PASS'
(HERE/'results.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
