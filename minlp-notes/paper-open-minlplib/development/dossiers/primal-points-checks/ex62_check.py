"""Exact feasibility and rigorous objective enclosure of the verifier's ex6_2_7 / ex6_2_5
primal points (dossier primal-points v2).  Own OSiL reader; values are rational
intervals [lo, hi] (Fractions) rounded outward to 2^-P after each ln; ln via
ln v = 2 atanh((m-1)/(m+1)) + e*ln2 with m = v/2^e in [1,2), ln2 = 2 atanh(1/3),
atanh series with remainder z^(2N+3)/((2N+3)(1-z^2)).  No mpmath, no floats.
usage: python3 ex62_check.py ex6_2_7 point.json
"""
import json
import sys
import xml.etree.ElementTree as ET
from fractions import Fraction as Fr

P = 400
NS = '{os.optimizationservices.org}'


def rnd(lo, hi):
    S = 1 << P
    return (Fr((lo.numerator * S) // lo.denominator, S), Fr(-((-hi.numerator * S) // hi.denominator), S))


def atanh_enc(z):
    assert 0 <= z < Fr(1, 2)
    if z == 0:
        return Fr(0), Fr(0)
    s, k, term = Fr(0), 0, z
    while True:
        s += term / (2 * k + 1)
        k += 1
        term = term * z * z
        rem = term / ((2 * k + 1) * (1 - z * z))  # bounds the tail sum_{j>=k} z^(2j+1)/(2j+1)
        if rem < Fr(1, 1 << (P + 20)):
            return s, s + rem


LN2 = tuple(2 * v for v in atanh_enc(Fr(1, 3)))


def ln_point(v):
    assert v > 0
    e = 0
    while v / (Fr(2) ** e) >= 2:
        e += 1
    while v / (Fr(2) ** e) < 1:
        e -= 1
    m = v / (Fr(2) ** e)
    a, b = atanh_enc((m - 1) / (m + 1))
    lo = 2 * a + (e * LN2[0] if e >= 0 else e * LN2[1])
    hi = 2 * b + (e * LN2[1] if e >= 0 else e * LN2[0])
    return rnd(lo, hi)


def mul(a, b):
    c = [a[0] * b[0], a[0] * b[1], a[1] * b[0], a[1] * b[1]]
    return (min(c), max(c))


def ev(e, x):
    k = e.tag.replace(NS, '')
    ch = list(e)
    if k == 'number':
        v = Fr(e.get('value'))
        return (v, v)
    if k == 'variable':
        c = Fr(e.get('coef', '1'))
        return mul((c, c), x[int(e.get('idx'))])
    if k == 'sum':
        r = (Fr(0), Fr(0))
        for c in ch:
            v = ev(c, x)
            r = (r[0] + v[0], r[1] + v[1])
        return r
    if k == 'product':
        r = (Fr(1), Fr(1))
        for c in ch:
            r = mul(r, ev(c, x))
        return rnd(*r) if r[0] != r[1] else r
    if k == 'ln':
        v = ev(ch[0], x)
        return (ln_point(v[0])[0], ln_point(v[1])[1])
    if k == 'divide':
        a, b = ev(ch[0], x), ev(ch[1], x)
        assert b[0] > 0 or b[1] < 0
        r = mul(a, (1 / b[1], 1 / b[0]))
        return rnd(*r) if r[0] != r[1] else r
    if k == 'negate':
        v = ev(ch[0], x)
        return (-v[1], -v[0])
    raise ValueError(k)


def expand(p):
    out = []
    for el in p:
        mult = int(el.get('mult', '1'))
        incr = el.get('incr')
        v = el.text.strip()
        out += [v] * mult if incr is None else [str(int(v) + i * int(incr)) for i in range(mult)]
    return out


def run(name, pt):
    d = ET.parse(f'{name}.osil').getroot().find(NS + 'instanceData')
    V = list(d.find(NS + 'variables'))
    x = [Fr(s) for s in pt]
    assert len(x) == len(V)
    for v, xv in zip(V, x):
        assert set(v.attrib) <= {'name', 'lb', 'ub'}
        assert Fr(v.get('lb', '0')) <= xv <= Fr(v.get('ub')), v.get('name')
    C = list(d.find(NS + 'constraints'))
    lcc = d.find(NS + 'linearConstraintCoefficients')
    st = [int(z) for z in expand(lcc.find(NS + 'start'))]
    col = [int(z) for z in expand(lcc.find(NS + 'colIdx'))]
    val = expand(lcc.find(NS + 'value'))
    nl = {int(e.get('idx')): list(e)[0] for e in d.find(NS + 'nonlinearExpressions')}
    assert set(nl) == {-1}
    for i, c in enumerate(C):
        assert set(c.attrib) <= {'name', 'lb', 'ub'}
        r = sum(Fr(val[k]) * x[col[k]] for k in range(st[i], st[i + 1]))
        assert c.get('lb') == c.get('ub') and r == Fr(c.get('lb')), c.get('name')
    o = d.find(NS + 'objectives').find(NS + 'obj')
    assert o.get('maxOrMin') == 'min' and o.get('constant') is None and len(list(o)) == 0
    xi = [(v, v) for v in x]
    lo, hi = ev(nl[-1], xi)
    print(f'{name}: {len(V)} vars, {len(C)} rows hold exactly, bounds exact; objective in '
          f'[{float(lo)!r}, {float(hi)!r}], width {float(hi - lo):.1e}')
    return lo, hi


if __name__ == '__main__':
    name, path = sys.argv[1], sys.argv[2]
    pt = json.load(open(path))['own_primal_point']
    lo, hi = run(name, pt)
    for disp in sys.argv[3:]:
        print(f'  display {disp} >= upper end: {Fr(disp) >= hi}; display - upper end = {float(Fr(disp) - hi):.3e}')
    # print 25 digits of the enclosure
    S = 10 ** 25
    print('  lo (25 dp, floor):', (lo.numerator * S) // lo.denominator, ' hi (25 dp, ceil):', -((-hi.numerator * S) // hi.denominator))
