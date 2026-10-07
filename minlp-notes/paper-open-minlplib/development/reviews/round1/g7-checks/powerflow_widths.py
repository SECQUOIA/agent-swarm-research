import sys, hashlib
sys.path.insert(0, '/tmp/g7/pfw/research-20260929/publication/primal/powerflow')
import certify
from fractions import Fraction as Q
for n in ('powerflow0030p', 'powerflow0039p', 'powerflow0039r'):
    r = certify.main(n)
    w = r['obj_hi'] - r['obj_lo']
    print(f'{n} exact width {w.numerator}/{w.denominator} ~ {float(w):.17g}; <= 2.83e-42: {w <= Q("2.83e-42")}; <= 2.8e-42: {w <= Q("2.8e-42")}')
