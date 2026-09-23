"""Independent exact checks of the frozen Stage 2 mathematical certificates.

Finite parameter checks supplement, and do not replace, the universal proofs.
Run with the minlp-notes Python environment (SymPy required).
"""
from pathlib import Path
from fractions import Fraction as Q
from itertools import product, combinations_with_replacement
from math import comb, prod
import contextlib
import io
import json
import re
import sympy as S

OUT = Path(__file__).resolve().parent
PAPER = OUT.parents[2]
SNAP = PAPER / 'process/snapshots/stage02-round02'
report = {}

# Replay what an outside reader obtains by concatenating the printed blocks.
appendix = (SNAP / 'sections/appendix-cubic-certificates.tex').read_text()
blocks = re.findall(r'\\begin\{verbatim\}\n(.*?)\\end\{verbatim\}', appendix, re.S)
assert len(blocks) == 2
printed = ''.join(blocks)
assert printed == (SNAP / 'verification/check_stage02_finite.py').read_text()
output = io.StringIO()
with contextlib.redirect_stdout(output):
    exec(compile(printed, '<printed cubic certificate>', 'exec'), {})
report['printed_certificate'] = {'blocks': 2, 'output': output.getvalue(),
    'three_group_states': 7**3 + 9**3 + 65**3,
    'two_group_states': 5**2 + 9**2 + 13**2 + 17**2}

# Independently evaluate O and B from the probability laws themselves.
def product_O(means):
    total = Q(0)
    for orientation in product((0, 1), repeat=len(means)):
        lower = max([Q(0)] + [1-x for x,o in zip(means,orientation) if o])
        upper = min([Q(1)] + [x for x,o in zip(means,orientation) if not o])
        total += max(Q(0), upper-lower)
    return total / 2**len(means)

def product_B(means):
    boundaries = sorted({Q(0), Q(1)} |
        {x if x <= Q(1,2) else 2*(1-x) for x in means})
    total = Q(0)
    for left,right in zip(boundaries,boundaries[1:]):
        t = (left+right)/2
        probabilities = [(int(t < x) if x <= Q(1,2)
            else Q(1,2) if t < 2*(1-x) else Q(1)) for x in means]
        total += (right-left)*prod(probabilities)
    return total

grid = [Q(i,16) for i in range(17)]
for x in grid:
    assert product_O((x,)) == product_B((x,)) == x
cases = 0
for degree in (2,3):
    for means in combinations_with_replacement(grid,degree):
        u = min(means)
        t = u-max(Q(0),sum(means)-degree+1)
        D = (u-product_O(means), u-prod(means), u-product_B(means))
        assert sum(w*d for w,d in zip((18,6,7),D)) >= 12*t
        cases += 1
report['direct_rational_cubic_couplings'] = {'tuples': cases, 'grid_denominator':16}

# Recover all printed Bernstein identities and derive both eliminated quartics.
tex = (SNAP/'sections/03-cubic-equal-means.tex').read_text()
a,b,c,t,m = S.symbols('a b c t m')
F = 6*c**3+27*b*c**2+18*b**2+30*a*c+20*a*b+9*a**2
ell = 37*a+S.Rational(79,2)*b+38*c-S.Rational(103,3)
h = F-ell
p = S.expand(h.subs({a:1,b:S.Rational(13,24)-3*c*c/4}))
stationary = S.solve([S.diff(h,a),S.diff(h,b)],(a,b))
r = S.expand(h.subs(stationary))
rows = re.findall(r'\$(p|r)\$&\$\[([0-9/]+),([0-9/]+)\]\$&(\d+)&\$\(([^)]+)\)',tex)
assert len(rows)==5
all_coeffs = []
for name,l,u,den,nums in rows:
    coeff = [S.Rational(int(v),int(den)) for v in nums.split(',')]
    all_coeffs.extend(coeff)
    bern = sum(coeff[j]*comb(4,j)*t**j*(1-t)**(4-j) for j in range(5))
    expected = {'p':p,'r':r}[name].subs(c,S.Rational(l)+(S.Rational(u)-S.Rational(l))*t)
    assert S.expand(bern-expected)==0
delta = min(all_coeffs)
assert delta == S.Rational(901,120000)
assert S.Rational(161,4)/(S.Rational(223,12)-delta)==S.Rational(1610000,743033)

twoF = a*c*c+S.Rational(5,4)*a*a
twoell = S.Rational(11,6)*a+S.Rational(20,27)*c-S.Rational(95,108)
twosq = S.Rational(5,4)*(a-(11-6*c*c)/15)**2+(1-c)*(3*c-2)**2*(3*c+7)/135
assert S.expand(twoF-twoell-twosq)==0
variantF = a*c*c+S.Rational(24,25)*a*a
variantell = S.Rational(41,25)*a+S.Rational(4,5)*c-S.Rational(68,75)
variantsq = S.Rational(24,25)*(a-(41-25*c*c)/48)**2+(1-c)*(5*c-3)**2*(5*c+11)/480
assert S.expand(variantF-variantell-variantsq)==0
for poly,atoms,mean,val in [(twoF,[(Q(1,4),Q(1,3),Q(1)),(Q(3,4),Q(5,9),Q(2,3))],
                             (Q(1,2),Q(3,4)),S.Rational(16,27)),
                            (variantF,[(Q(1,2),Q(1,3),Q(1)),(Q(1,2),Q(2,3),Q(3,5))],
                             (Q(1,2),Q(4,5)),S.Rational(83,150))]:
    assert sum(w*x for w,x,y in atoms)==mean[0]
    assert sum(w*y for w,x,y in atoms)==mean[1]
    assert sum(w*poly.subs({a:x,c:y}) for w,x,y in atoms)==val
num = S.Rational(161,4)-S.Rational(135,4)/m+6/m**2
den = S.Rational(223,12)+S.Rational(135,4)/m+9/m**2
assert (num/den).subs(m,36)==S.Rational(16985,8436)
report['symbolic'] = {'bernstein_rows':len(rows),'minimum_coefficient':str(delta),
    'limiting_lower':'1610000/743033','two_scalar_identities':'exact'}

# Verify the resource construction and all affine breakpoints for 2 <= L <= 60.
for L in range(2,61):
    B = lambda q: Q(L-q+2,2**q)
    candidates = [s for s in range(1,L) if B(s+1)<=1<=B(s)]
    gaps = set()
    for s in candidates:
        mix = (1-B(s+1))/(B(s)-B(s+1))
        assert 0 <= mix <= 1
        mass=Q(0); objective=Q(0); anchors=[Q(0)]*L
        for q,weight in [(s,mix),(s+1,1-mix)]:
            for l in range(L+1):
                prob = weight * (Q(1,2**(l+1)) if l<L else Q(1,2**L))
                R = 0 if l<q else 2**(l-q+1)
                mass += prob*R
                objective += prob*sum(min(2**j,R) for j in range(1,l+1))
                for j in range(1,l+1): anchors[j-1] += prob
        assert mass==1
        assert anchors==[Q(1,2**j) for j in range(1,L+1)]
        gap = s+Q(L-s,2**s)
        assert objective==gap
        gaps.add(gap)
        for l in range(L+1):
            cap = 0 if l<=s else 2**(l-s+1)-2
            for R in [0]+[2**j for j in range(L+1)]:
                assert sum(min(2**j,R) for j in range(1,l+1)) <= s*R+cap
    assert len(gaps)==1
for L in range(2,10):
    m=2**L
    order=[int(format(i,f'0{L}b')[::-1],2) for i in range(m)]
    prefixes=[set() for _ in range(L)]
    for R,label in enumerate(order,1):
        for j in range(1,L+1):
            prefixes[j-1].add(label>>(L-j))
            assert len(prefixes[j-1])==min(2**j,R)
report['dyadic']={'resource_and_breakpoints':'L=2,...,60','all_prefix_counts':'L=2,...,9'}

# Finite coefficient-removal margins need no logarithm approximation beyond log 2 < 1.
m=1000
assert Q(25*m+2)-Q(m**3,23200)<0
assert Q(3131,2275)-Q(1,2)==Q(3987,4550)>0
assert Q(2160)/(1072+Q(12,5))==Q(2700,1343)
report['coefficient_removal']={'log_failure_upper':str(Q(25*m+2)-Q(m**3,23200)),
    'normalized_positive_margin':'3987/4550'}
(OUT/'results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
