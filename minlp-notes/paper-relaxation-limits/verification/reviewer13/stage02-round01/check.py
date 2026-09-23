from pathlib import Path
from fractions import Fraction as Q
from math import comb
import re
import sympy as S
root=Path('process/snapshots/stage02-round01')
# Execute the actual printed exact certificates, after independent inspection.
code=(root/'sections/appendix-cubic-certificates.tex').read_text().split(r'\begin{verbatim}')[1].split(r'\end{verbatim}')[0]
exec(compile(code,'frozen-printed-certificate','exec'))
# Independently derive the scalar eliminations, then compare actual table rows.
a,b,c,t=S.symbols('a b c t')
h=6*c**3+27*b*c**2+18*b**2+30*a*c+20*a*b+9*a*a-37*a-S.Rational(79,2)*b-38*c+S.Rational(103,3)
p=S.expand(h.subs({a:1,b:S.Rational(13,24)-3*c*c/4}))
stationary=S.solve([S.diff(h,a),S.diff(h,b)],[a,b])
r=S.expand(h.subs(stationary))
src=(root/'sections/03-cubic-equal-means.tex').read_text()
rows=re.findall(r'\$(p|r)\$&\$\[([^,]+),([^\]]+)\]\$&(\d+)&\$\(([^)]+)\)\$',src)
assert len(rows)==5
coeffs=[]
for name,lo,hi,den,nums in rows:
 lo,hi=S.Rational(lo),S.Rational(hi)
 nums=list(map(int,nums.split(','))); den=int(den)
 bern=sum(S.Rational(v,den)*comb(4,i)*t**i*(1-t)**(4-i) for i,v in enumerate(nums))
 assert S.expand((p if name=='p' else r).subs(c,lo+(hi-lo)*t)-bern)==0
 coeffs.extend(S.Rational(v,den) for v in nums)
assert min(coeffs)==S.Rational(901,120000)
assert S.Rational(161,4)/(S.Rational(223,12)-min(coeffs))==S.Rational(1610000,743033)
for beta,l,center,tail in [
 (S.Rational(5,4),11*a/6+20*c/27-S.Rational(95,108),(11-6*c*c)/15,(1-c)*(3*c-2)**2*(3*c+7)/135),
 (S.Rational(24,25),41*a/25+4*c/5-S.Rational(68,75),(41-25*c*c)/48,(1-c)*(5*c-3)**2*(5*c+11)/480)]:
 assert S.expand(a*c*c+beta*a*a-l-beta*(a-center)**2-tail)==0
print('Exact scalar eliminations, five frozen Bernstein rows, slack and two-level identities passed.')
# Exact resource profiles and affine certificates; finite evidence of general proof.
for L in range(2,11):
 m=2**L
 weights=[Q(1,2**(l+1)) if l<L else Q(1,2**L) for l in range(L+1)]
 B=lambda q:Q(L-q+2,2**q)
 for s in range(1,L):
  if not B(s+1)<=1<=B(s): continue
  theta=(1-B(s+1))/(B(s)-B(s+1))
  mean=Q(0); val=Q(0)
  for q,mix in [(s,theta),(s+1,1-theta)]:
   for l,weight in enumerate(weights):
    R=0 if l<q else 2**(l-q+1)
    mean+=mix*weight*R
    val+=mix*weight*sum(min(2**j,R) for j in range(1,l+1))
  assert mean==1 and val==s+Q(L-s,2**s)
  for l in range(L+1):
   cap=0 if l<=s else 2**(l-s+1)-2
   for R in range(m+1):
    assert sum(min(2**j,R) for j in range(1,l+1))<=s*R+cap
print('Dyadic exact finite resource and affine certificates passed for L=2,...,10, including cutoff ties.')
