"""Exact checks of the eg dual displays against the binary64 certified values, and of the gaps."""
from fractions import Fraction as F
from decimal import Decimal, getcontext
getcontext().prec = 60
rows = [('eg_int_s', '6.4531031529331155', '6.4531031593842274088'),
        ('eg_disc_s', '5.760539610694994', '5.7605396164535106058'),
        ('eg_disc2_s', '5.642100574331458', '5.6421005799711067563')]
for n, L, P in rows:
    b = F(float(L)); d = F(L)
    print(f"{n}: display {L}; binary64 value {Decimal(b.numerator)/Decimal(b.denominator)}; display - binary = {float(d-b):.3e}")
    for Ld in ([L, '5.760539610694993'] if n == 'eg_disc_s' else [L]):
        g = F(P) - F(Ld)
        print(f"   with dual display {Ld}: abs gap {float(g):.7e}, rel gap (/dual) {float(g/F(Ld)):.7e}")
