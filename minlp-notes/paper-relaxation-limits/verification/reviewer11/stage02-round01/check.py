"""Exact review checks; no optimizer is required to verify the certificates."""
from fractions import Fraction as Q
from math import comb
from pathlib import Path
import json
import re
import sympy as sp

paper = Path(__file__).resolve().parents[3]
frozen = paper / 'process/snapshots/stage02-round01'

# Replay the actual printed finite proof, rather than a possibly stale companion.
tex = (frozen / 'sections/appendix-cubic-certificates.tex').read_text()
printed = re.search(r'\\begin\{verbatim\}(.*?)\\end\{verbatim\}', tex, re.S)[1]
exec(compile(printed, 'frozen-printed-certificate', 'exec'), {})

# Independently derived small-member duals. A numerical LP suggested the
# coefficients; every assertion below is an exact rational certificate.
small = []
for m, dual, wanted in [
    (4, (Q(-19), Q(9), Q(4)), Q(27, 16)),
    (8, (Q(-188), Q(47), Q(20)), Q(21, 11)),
    (12, (Q(-684), Q(231, 2), Q(48)), Q(99, 50)),
]:
    constant, da, dc = dual
    value = lambda a, c: a * comb(c, 2) + (5*m//4) * comb(a, 2)
    slacks = [value(a, c) - constant-da*a-dc*c
              for a in range(m+1) for c in range(m+1)]
    assert min(slacks) == 0
    a, c = m//2, 3*m//4
    vex = value(a, c)
    assert vex == constant+da*a+dc*c
    cav = Q(9*m*m*(m-1), 16)
    assert cav/(cav-vex) == wanted < 2
    small.append(dict(m=m, states=len(slacks), dual=list(map(str, dual)),
                      attaining_counts=[a, c], vex=vex, cav=str(cav),
                      ratio=str(wanted)))

# The m=36 source specialization is already implied by the stronger finite
# analytic formula in the manuscript; it is not a missing proof development.
m = 36
num = Q(161,4)-Q(135,4*m)+Q(6,m*m)
den = Q(223,12)+Q(135,4*m)+Q(9,m*m)
assert num/den == Q(16985,8436) > 2
assert num/(den-Q(901,120000)) > num/den

# Derive the quartics by solving stationary equations, then derive each
# Bernstein coefficient from the transformed power coefficients.
a,b,c,t = sp.symbols('a b c t')
h = 6*c**3+27*b*c*c+18*b*b+30*a*c+20*a*b+9*a*a-37*a-sp.Rational(79,2)*b-38*c+sp.Rational(103,3)
b_boundary = sp.solve(sp.diff(h,b).subs(a,1),b)[0]
quartics = {'p': sp.expand(h.subs({a:1,b:b_boundary}))}
stationary = sp.solve([sp.diff(h,a),sp.diff(h,b)],(a,b))
quartics['r'] = sp.expand(h.subs(stationary))
main_tex = (frozen/'sections/03-cubic-equal-means.tex').read_text()
rows = re.findall(r'\$(p|r)\$&\$\[([^,]+),([^\]]+)\]\$&(\d+)&\$\(([^)]+)\)',main_tex)
assert len(rows)==5
all_bern = []
for kind,lo,hi,den,nums in rows:
    lo,hi = sp.Rational(lo),sp.Rational(hi)
    power = sp.Poly(quartics[kind].subs(c,lo+(hi-lo)*t),t)
    derived = [sum(power.nth(j)*sp.Rational(comb(i,j),comb(4,j))
                   for j in range(i+1)) for i in range(5)]
    listed = [sp.Rational(v,den) for v in nums.split(',')]
    assert derived==listed
    all_bern.extend(derived)
assert min(all_bern)==sp.Rational(901,120000)
assert sp.Rational(161,4)/(sp.Rational(223,12)-min(all_bern))==sp.Rational(1610000,743033)

# Independently check every cutoff, including ties, and resource mixture for
# modest L. This is supplementary finite evidence for the all-L proof.
for L in range(2,65):
    budget = lambda q: Q(L-q+2,2**q)
    choices = [s for s in range(1,L) if budget(s+1)<=1<=budget(s)]
    assert choices
    answers = set()
    weights = [Q(1,2**(l+1)) if l<L else Q(1,2**L) for l in range(L+1)]
    for s in choices:
        mix = (1-budget(s+1))/(budget(s)-budget(s+1))
        assert 0<=mix<=1
        expected_r = Q(0)
        expected_h = Q(0)
        for q, probability in ((s,mix),(s+1,1-mix)):
            for l, wl in enumerate(weights):
                r = 0 if l<q else 2**(l-q+1)
                expected_r += probability*wl*r
                expected_h += probability*wl*sum(min(2**j,r) for j in range(1,l+1))
        assert expected_r == 1
        assert expected_h == s+Q(L-s,2**s)
        answers.add(expected_h)
    assert len(answers)==1

result = dict(printed_finite_certificates='passed',
              independent_bernstein_derivation='all 25 coefficients passed',
              additional_two_level_exact_certificates=small,
              analytic_m36_specialization='16985/8436; stronger frozen bound holds',
              dyadic_cutoffs='all L=2,...,64 and all adjacent choices passed')
Path(__file__).with_name('checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
