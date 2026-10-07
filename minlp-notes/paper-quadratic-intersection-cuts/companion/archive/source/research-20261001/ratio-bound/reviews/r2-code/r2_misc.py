"""Review r2: small exact checks.
(a) The note writes the range of Theorem B2(2) as 'eps <= 1.83e-5' in four places, but the certified eps_1 is
    1.8288e-5 < 1.83e-5.  Check whether the same X also covers eps <= 183/10^7: find a rational height h' with
    sym(X M(rho, rho, h')) PSD and (rho/(h'-1))^2 >= 183/10^7.
(b) Arithmetic behind the orbit-closure note's use of this note: W-corner depth D = sqrt(2)/eps and Theorem A's bound
    z_A >= 2/((1+sqrt2) D) = (2 - sqrt2) eps (z_K = 2, valid for D >= 1, i.e. eps <= sqrt2); and 3 * 160 = 480.
(c) Percent gaps quoted in Sections 3.1, 3.2, 6.1 and 9."""
from fractions import Fraction as Fr
import sympy as sp

X = [[Fr('1'), Fr('-1.678587')], [Fr('0.007315'), Fr('0.698332')]]
rho = Fr(1367, 10)


def symXM(s):
    x, y, w = s
    M = [[w, x], [y, Fr(1)]]
    A = [[sum(X[i][k] * M[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
    return A[0][0], (A[0][1] + A[1][0]) / 2, A[1][1]


hp = Fr(31800)
a, b, d = symXM((rho, rho, hp))
psd = a >= 0 and d >= 0 and a * d - b * b >= 0
eps = (rho / (hp - 1)) ** 2
print('(a) h\' = 31800: PSD %s; (rho/(h\'-1))^2 = %.6e >= 1.83e-5: %s' % (psd, float(eps), eps >= Fr(183, 10 ** 7)))

e = sp.symbols('epsilon', positive=True)
sbar = sp.Matrix([1, -1, 1]); qbar = sbar[2] - sbar[0] * sbar[1]
zK = 2
Xt = zK / e; Yt = zK / e              # p~_1 = (2/eps) e_x, p~_2 = -(2/eps) e_y, w-rays have no x, y part
D = sp.sqrt(Xt * Yt / qbar)
bound = sp.simplify(zK / ((1 + sp.sqrt(2)) * D))
print('(b) W-corner: q(sbar) =', qbar, ', D =', sp.simplify(D), ', z_K * f(D) =', bound,
      '; equals (2 - sqrt2) eps:', sp.simplify(bound - (2 - sp.sqrt(2)) * e) == 0, '; 3*160 =', 3 * 160)

for lab, hi, lo in [('B2: 137/136.7', Fr(137), Fr(1367, 10)), ('B3 eta=1e-3,k=4', Fr(197, 100), Fr(2461, 1250)),
                    ('B3 eta=1e-2,k=4', Fr(5, 2), Fr(6117, 2500)), ('B3 k=9/4', Fr(63, 40), Fr(15621, 10000)),
                    ('B3 k=49/25', Fr(154, 100), Fr(18851, 12500))]:
    print('(c) %-18s gap %.4f%%' % (lab, 100 * float(hi / lo - 1)))
print('(c) 1.54 / (1/(1+sqrt2)) = %.4f; 137*sqrt2 = %.4f; 1367/10*sqrt2 = %.4f' %
      (1.54 * (1 + 2 ** 0.5), 137 * 2 ** 0.5, 136.7 * 2 ** 0.5))
