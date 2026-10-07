"""Exact check of the hand proof that x267 (tank-3 level at link 0 of waterno2_06) <= 5.6977."""
from fractions import Fraction as F
from decimal import Decimal, getcontext
getcontext().prec = 60
a = F('63.61644904'); b = F('2.03724124'); c = F('34.92732674')   # station-D pump curve (rows e44/e50)
H0 = F(4) + 103 - F('41/10') - 90                                  # x464 = L3 + 103 + 5 QD^2 - (L2 + 90), L3 = 4, L2 = 4.1
def qmax(k):
    A = a + k; C = c - H0; disc = b * b + 4 * A * C
    r = F(str((Decimal(disc.numerator) / Decimal(disc.denominator)).sqrt())) + F(1, 10**40)
    assert r * r >= disc
    return (b + r) / (2 * A)
QD = max(2 * qmax(20), min(qmax(5), F('0.58')), b / a)
E3 = 4 + F(9, 4) * (QD - F('0.296666667'))
print('H0 =', H0, '; QD <=', float(QD), '; x267 <=', float(E3))
print('root cell upper 5.936197237759838 >= bound:', F(5.936197237759838) >= E3)
