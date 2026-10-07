import csv, math
from fractions import Fraction as F
def floor_sig(x, k=3):
    # largest decimal with k significant digits that is <= x (x > 0)
    e = math.floor(math.log10(float(x))) - (k - 1)
    q = F(10) ** e if e >= 0 else F(1, 10 ** (-e))
    n = (x / q).numerator // (x / q).denominator
    v = n * q
    assert v <= x
    s = ('%.' + str(max(0, -e)) + 'f') % float(v) if abs(e) < 12 else '%.*e' % (k - 1, float(v))
    assert F(s) <= x
    return s
for row in csv.DictReader(open('margin_figure.csv')):
    d = F(row['listed_dual']); f = F(row['proven_f_upper']); m = d - f
    t = row['listed_dual'].lstrip('-'); k = len(t.split('.')[1]) if '.' in t else 0
    print(f"{row['instance']:28s} {row['solver']:8s} {row['class']:18s} margin>={floor_sig(m):>14s} rel>={floor_sig(m/abs(d)):>10s} units>={floor_sig(m*10**k):>10s}")
