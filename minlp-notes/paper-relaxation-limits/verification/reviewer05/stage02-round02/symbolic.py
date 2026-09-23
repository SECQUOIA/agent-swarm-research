"""Independent symbolic reconstruction of the scalar count certificates."""
from pathlib import Path
import json
import re
import sympy as s

here = Path(__file__).resolve().parent
tex = (here.parents[2] / "process/snapshots/stage02-round02/sections/03-cubic-equal-means.tex").read_text()
a,b,c,t,m = s.symbols("a b c t m")
Q = s.Rational
F = 6*c**3+27*b*c**2+18*b**2+30*a*c+20*a*b+9*a**2
h = F-37*a-Q(79,2)*b-38*c+Q(103,3)
assert s.det(s.hessian(h,(a,b))) == 248
p = s.expand(h.subs({a:1,b:Q(13,24)-3*c**2/4}))
stationary = s.solve([s.diff(h,a),s.diff(h,b)],(a,b))
r = s.expand(h.subs(stationary))
rows = re.findall(r"\$(p|r)\$&\$\[([^,]+),([^\]]+)\]\$&(\d+)&\$\(([^)]+)\)\$",tex)
assert len(rows) == 5
all_coefficients = []
for name,lo,hi,denom,nums in rows:
    lo,hi = Q(lo),Q(hi)
    power = s.Poly((p if name == "p" else r).subs(c,lo+(hi-lo)*t),t)
    computed = [s.simplify(sum(power.nth(j)*Q(s.binomial(i,j),s.binomial(4,j))
                             for j in range(i+1))) for i in range(5)]
    displayed = [Q(int(v),int(denom)) for v in nums.split(",")]
    assert computed == displayed
    all_coefficients.extend(computed)
delta = min(all_coefficients)
assert delta == Q(901,120000)
assert (Q(161,4)/(Q(223,12)-delta)) == Q(1610000,743033)

for coefficient,aa,cc,constant,center,remainder in [
    (Q(5,4),Q(11,6),Q(20,27),Q(95,108),(11-6*c**2)/15,
     (1-c)*(3*c-2)**2*(3*c+7)/135),
    (Q(24,25),Q(41,25),Q(4,5),Q(68,75),(41-25*c**2)/48,
     (1-c)*(5*c-3)**2*(5*c+11)/480)]:
    assert s.expand(a*c**2+coefficient*a**2-aa*a-cc*c+constant
                    -coefficient*(a-center)**2-remainder) == 0

choose2 = lambda v: v*(v-1)/2
choose3 = lambda v: v*(v-1)*(v-2)/6
fm = (2*choose3(m*c)+3*m*b*choose2(m*c)+2*m*choose2(m*b)
      +5*m/3*(m*a)*(m*c)+10*m/9*(m*a)*(m*b)+m*choose2(m*a))
assert s.expand(18*fm/m**3-F+(18*c**2+27*b*c+18*b+9*a)/m-12*c/m**2) == 0
coefs = [2,3,2*m,5*m/3,10*m/9,m]
sizes = [choose3(m),m*choose2(m),choose2(m),m**2,m**2,choose2(m)]
upper = [Q(3,4),Q(1,2),Q(1,2),Q(1,4),Q(1,4),Q(1,4)]
cav = s.expand(18/m**3*sum(k*n*u for k,n,u in zip(coefs,sizes,upper)))
gap = s.expand(cav-18/m**3*Q(1,4)*2*choose3(m))
denom = cav-Q(139,6)-delta+72/m
assert s.expand(gap-(Q(161,4)-Q(135,4)/m+6/m**2)) == 0
assert (gap/(denom+delta)).subs(m,36) == Q(16985,8436)
assert (gap/denom).subs(m,36) == Q(42462500,21081891)
out = {"bernstein_rows":len(rows),"minimum_coefficient":str(delta),
       "limiting_bound":str(Q(161,4)/(Q(223,12)-delta)),
       "m36_slack_bound":str((gap/denom).subs(m,36)),
       "two_level_identities":2,"analytic_count_and_envelopes":"exact"}
(here/"symbolic-results.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps(out,indent=2))
