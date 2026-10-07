"""pindyck: dual bound from strong concavity (no new computation; uses the review's saved exact enclosures).

If grad^2 J <= -mu I on the convex set G (proved: mu = 1/1000) and p, p* in G, then
J(p) <= J(p*) + g.(p - p*) - (mu/2)|p - p*|^2 <= J(p*) + |g|^2 / (2 mu),   g = grad J(p*).
"""
from fractions import Fraction as Fr
import mpmath
mpmath.mp.dps = 60
L = [l.split() for l in open('primal_enclosure.txt')]
d = {r[0]: (Fr(r[1]), Fr(r[2])) for r in L}
Jlo, Jhi = d['J']
g2 = sum(max(abs(d['g%d' % t][0]), abs(d['g%d' % t][1]))**2 for t in range(1, 17))
mu = Fr(1, 1000)
add = g2 / (2 * mu)
UB = Jhi + add
q = lambda x: mpmath.mpf(x.numerator) / x.denominator
print('J(p*) in [%s, %s]' % (mpmath.nstr(q(Jlo), 45), mpmath.nstr(q(Jhi), 45)))
print('|grad J(p*)|_2^2 <= %s ; |g|^2/(2 mu) <= %s' % (mpmath.nstr(q(g2), 6), mpmath.nstr(q(add), 6)))
print('upper bound on J over F: %s' % mpmath.nstr(q(UB), 45))
print('min-form dual bound: objective >= %s' % mpmath.nstr(q(-UB), 45))
print('gap to the exactly feasible point p*: <= %s' % mpmath.nstr(q(UB - Jlo), 6))
# a safe display: truncate -UB downward at 30 decimals
k = 30
v = -UB
f = (v * 10**k).__floor__()
disp = Fr(f, 10**k)
print('safe display (rounded down, %d decimals): %s' % (k, mpmath.nstr(q(disp), 40)))
assert disp <= -UB
# compare with the current summary display and the old linear-term bound
old = Fr('-1170.4862854360886163932')
print('summary display -1170.4862854360886163932 is weaker by %s' % mpmath.nstr(q(disp - old), 6))
# primal display safety
print('summary primal -1170.486285436088562 >= -J_lo:', Fr('-1170.486285436088562') >= -Jlo)
