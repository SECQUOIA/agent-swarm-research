"""Exact checks for the critique of dossiers/small.md (run on copies; reads only primal_enclosure.txt from cwd).

Copy R/reviews/pindyck-review-checks/logs/primal_enclosure.txt to the working directory first.
"""
from fractions import Fraction as F
from math import factorial, sqrt

print('--- display subtraction vs gap cells')
d27, p27 = F('-0.16084761546364905'), F('-0.16084761546360086')
d25, p25 = F('-70.75207783344770759'), F('-70.752077833447705')
de, pe = F('-15.294675643368093'), F('-15.29467564336808959')
print('ex6_2_7 displays differ by', float(p27 - d27), '(cell <= 4.9e-14)')
print('ex6_2_5 displays differ by', float(p25 - d25), '(cell <= 2.1e-15)')
print('etamac  displays differ by', float(pe - de), '(cell <= 2.6e-15)')
obj25 = F('-70.75207783344770558036712203349626517975370343012333996')   # upper end, gibbs_check.log
cert25 = F('-70.7520778334477075803539469')
p25n = F('-70.75207783344770558')
print('proposed ex6_2_5 primal display', p25n, 'safe:', p25n >= obj25, ' display diff:', float(p25n - d25))
etam_obj = F('-15.2946756433680895919829233612845357438291772')            # verifier point upper end, etamac.json
etam_safe = F('-15.2946756433680921685')                                    # closing-confirm-r2 certified lower end
den = F('-15.29467564336809217')
print('proposed etamac dual display', den, 'valid:', den <= etam_safe, ' primal', pe, 'safe:', pe >= etam_obj, ' display diff:', float(pe - den))
print('etamac exact gap (verifier point, -...0921685):', float(etam_obj - etam_safe))

print('--- unsafe secondary dual strings (above the certified value)')
c27 = F('-0.160847615463649043442185')
lhi = F('-15.2946756433680921684870123983196445558882659')   # l(x_hat) upper end; the bound is <= this
for s, ref in (('-0.16084761546364904', c27), ('-70.75207783344770758', cert25),
               ('-15.294675643368092', lhi), ('-15.294675643368092168', lhi)):
    print(s, 'exceeds certified value by', float(F(s) - ref))

print('--- pindyck strong-concavity gap from either party\'s enclosures')
d = {}
for line in open('primal_enclosure.txt'):
    r = line.split(); d[r[0]] = (F(r[1]), F(r[2]))
g2 = sum(max(abs(d['g%d' % t][0]), abs(d['g%d' % t][1])) ** 2 for t in range(1, 17))
print('review enclosure: |g|^2/(2mu) <=', float(g2 / F(2, 1000)))
ga = 16 * F('8.01e-17') ** 2                                    # author: max_t |dJ/dp_t| <= 8.01e-17
print('author enclosure: 16*(8.01e-17)^2/(2mu) <=', float(ga / F(2, 1000)), '+ J width 4.9e-30')

print('--- hvycrash')
x = F(26, 10)
S = lambda n: sum(F((-1) ** k) * x ** (2 * k) / factorial(2 * k) for k in range(n + 1))
print('cos 2.6 in [%.9f, %.9f]' % (float(S(7)), float(S(6))))
D08 = F('0.486237') * F(8, 100) ** 2 + F('0.0162079')
print('|r| bound for sub-(-h) increments: 1/sqrt(0.0162079) =', 1 / sqrt(0.0162079), '; with c >= 0.08:', 1 / sqrt(float(D08)))

print('--- ex6_2_7 n1 ln n1 pieces (stored digits) and lam.b vs primal')
print(float(F('0.240734108219679') + F('11.24') + F('2.248') - F('12.7287341082197') - 1))
print('ex6_2_5 primal - lam.b =', float(F('-70.75207783344770558036712') - F('-70.7520778334477055803539469')))
