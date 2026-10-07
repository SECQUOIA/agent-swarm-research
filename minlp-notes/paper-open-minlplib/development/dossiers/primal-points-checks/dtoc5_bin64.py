# Sensitivity of the dtoc5 primal point to the reading of OSIL constants:
# rebuild u_t from the same rational y with binary64 coefficients and compare objectives.
import gzip
from fractions import Fraction as F
from decimal import Decimal
pt = {}
for line in gzip.open('data/dtoc5_point.txt.gz','rt'):
    if line.startswith('#') or not line.strip(): continue
    k, v = line.split(); pt[k] = F(Decimal(v))
T = 49999
u = [pt[f'x{t+2}'] for t in range(T)]
y = [pt[f'x{50001+t}'] for t in range(T+1)]
for c1, c2, lab in [(F(Decimal('2e-5')), F(Decimal('8e-5')), 'decimal'), (F(2e-5), F(8e-5), 'binary64')]:
    uu = [(y[t] - y[t+1] + c2*y[t]*y[t])/c1 for t in range(T)]
    f = c1*(sum(v*v for v in uu) + sum(v*v for v in y[:T]))
    if lab == 'decimal': f_dec = f; assert uu == u
    print(lab, float(f), 'diff to decimal-model point objective:', float(f - f_dec))
