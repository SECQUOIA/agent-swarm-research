"""R1-math: check Bernstein coefficient formula (eq. bernstein) and the chord lemma constant."""
import sympy as sp, random, itertools
from sympy import binomial as C, Rational as Q
random.seed(2)
t1, t2 = sp.symbols('t1 t2')
d = (3, 2)
a = {(i, j): Q(random.randint(-5, 5), random.randint(1, 4)) for i in range(d[0]+1) for j in range(d[1]+1)}
p = sum(a[k]*t1**k[0]*t2**k[1] for k in a)
def B(dd, i, t): return C(dd, i)*t**i*(1-t)**(dd-i)
c = {}
for al in a:
    c[al] = sum(a[be]*C(al[0], be[0])/C(d[0], be[0])*C(al[1], be[1])/C(d[1], be[1])
                for be in a if be[0] <= al[0] and be[1] <= al[1])
recon = sum(c[al]*B(d[0], al[0], t1)*B(d[1], al[1], t2) for al in c)
print("Bernstein formula residual:", sp.expand(recon - p))
# chord lemma: p(t) >= chord - M/2 (t-a)(b-t) ; tightness for p = M t^2/2
tt, M, al_, be_ = sp.symbols('t M alpha beta')
pp = M*tt**2/2
chord = pp.subs(tt, al_) + (pp.subs(tt, be_) - pp.subs(tt, al_))*(tt-al_)/(be_-al_)
print("chord - M/2(t-a)(b-t) - p:", sp.simplify(chord - M/2*(tt-al_)*(be_-tt) - pp))
print("max of (t-a)(b-t):", sp.simplify(((tt-al_)*(be_-tt)).subs(tt, (al_+be_)/2)))
