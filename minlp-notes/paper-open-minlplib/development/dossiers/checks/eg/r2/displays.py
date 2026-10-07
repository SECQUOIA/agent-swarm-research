"""Exact checks: binary64 values of the certified bounds, display safety, gaps (Fractions)."""
from fractions import Fraction as F
from decimal import Decimal, getcontext
getcontext().prec = 40
def dec(q): return Decimal(q.numerator) / Decimal(q.denominator)
# (instance, certified float repr from the search log, summary dual display, primal objvar (sol), IEEE-only U' from the log, summary primal display)
rows = [('eg_int_s', '6.4531031529331155', '6.4531031529331155', '6.4531031593842274088', '6.4531031593862185', '6.4531031593842275'),
        ('eg_disc_s', '5.760539610694994', '5.760539610694994', '5.7605396164535106058', '5.760539616455533', '5.7605396164535107'),
        ('eg_disc2_s', '5.642100574331458', '5.642100574331458', '5.6421005799711067563', '5.642100579973559', '5.6421005799711068')]
for n, cert, Ldisp, P, Up, Pdisp in rows:
    b = F(float(cert)); d = F(Ldisp)
    print(f"{n}: certified binary64 {dec(b)}; display {Ldisp} - binary64 = {float(d - b):+.3e}")
    for lab, L in (('display', d), ('binary64', b)):
        for plab, PP in (('sol objvar', F(P)), ('summary primal display', F(Pdisp)), ("IEEE-only U'", F(Up))):
            g = PP - L
            print(f"   dual {lab:8s} vs {plab:22s}: abs gap {float(g):.10e}; rel gap {float(g / L):.10e}")
    print(f"   summary primal display {Pdisp} >= sol objvar: {F(Pdisp) >= F(P)}; retry.md truncation 16 digits below objvar by {float(F(P) - F(P[:18])):.2e}")
