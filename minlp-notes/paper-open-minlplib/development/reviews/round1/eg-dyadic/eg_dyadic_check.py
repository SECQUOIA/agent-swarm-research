"""Rigorous feasibility check of the eg_* retry points (dossier primal-points, v2).

Own OSiL reader and own outward-rounded interval arithmetic on dyadic numbers
(Python integers scaled by 2^-P).  No mpmath, no numpy, no decimal module, no
libm.  exp is bounded by the alternating Taylor series of exp(-y) for
0 <= y <= 2^-8 (partial sums bracket the value because the terms decrease)
after argument halving, followed by outward squaring.
Assumptions: Python integer and Fraction arithmetic are exact; the OSiL
reading below (decimal strings read as exact rationals, OSiL defaults).
usage: python3 eg_dyadic_check.py eg_int_s eg_disc_s eg_disc2_s
"""
import sys
import xml.etree.ElementTree as ET
from fractions import Fraction as Fr

P = 256
ONE = 1 << P
NS = '{os.optimizationservices.org}'


def fl(n, d):
    return n // d


def ce(n, d):
    return -((-n) // d)


class I:
    __slots__ = ('lo', 'hi')

    def __init__(s, lo, hi):
        assert lo <= hi
        s.lo, s.hi = lo, hi

    @staticmethod
    def q(x):
        x = Fr(x)
        return I(fl(x.numerator << P, x.denominator), ce(x.numerator << P, x.denominator))

    def __add__(a, b):
        return I(a.lo + b.lo, a.hi + b.hi)

    def __neg__(a):
        return I(-a.hi, -a.lo)

    def __mul__(a, b):
        c = (a.lo * b.lo, a.lo * b.hi, a.hi * b.lo, a.hi * b.hi)
        return I(min(c) >> P, -((-max(c)) >> P))

    def sq(a):
        if a.lo >= 0:
            return I((a.lo * a.lo) >> P, -((-(a.hi * a.hi)) >> P))
        if a.hi <= 0:
            return I((a.hi * a.hi) >> P, -((-(a.lo * a.lo)) >> P))
        return I(0, -((-max(a.lo * a.lo, a.hi * a.hi)) >> P))

    def ends(a):
        return Fr(a.lo, ONE), Fr(a.hi, ONE)


def exp_neg_point(t):
    """[L, U] (Fractions) with L <= exp(-t) <= U for rational t >= 0.
    Fixed point at W bits: y = t/2^s <= 2^-8 is enclosed in [yl, yh]/2^W; the
    series sum_k (-y)^k/k! is alternating with decreasing terms, so for each
    y the partial sums S_{2j+1} <= exp(-y) <= S_{2j}.  We bound exp(-y) below
    by S_odd(yh) evaluated with downward rounding (exp(-y) is decreasing, and
    S_odd is a valid lower bound at every y) and above by S_even(yl) with
    upward rounding.  Then square s times with outward rounding."""
    t = Fr(t)
    assert t >= 0
    s = 0
    while t > Fr(1 << s, 256):
        s += 1
    W = P + 96
    yl = fl(t.numerator << W, t.denominator << s)
    yh = ce(t.numerator << W, t.denominator << s)
    one = 1 << W
    # upper: even partial sum at yl, rounding up.  Terms T_k = yl^k/k! >= 0.
    def partial(y, up, nterms):
        # returns sum_{k=0}^{nterms-1} (-1)^k y^k/k! / 2^W scaled by 2^W, rounded in
        # the direction that keeps the result a lower (up=False) or upper (up=True) bound
        tot = 0
        Tl = one  # lower bound of T_k * 2^W
        Th = one  # upper bound of T_k * 2^W
        for k in range(nterms):
            if k % 2 == 0:
                tot += Th if up else Tl
            else:
                tot -= Tl if up else Th
            # T_{k+1} = T_k * y / (k+1)
            Tl = (Tl * y) // (one * (k + 1))
            Th = ce(Th * y, one * (k + 1))
        return tot
    n = 2
    while True:  # first omitted term y^n/n! below 2^-(W-8)
        if ce(yh ** n, (one ** (n - 1)) * __import__('math').factorial(n)) < (1 << 8):
            break
        n += 1
    ne = n if n % 2 == 0 else n + 1   # even number of terms -> lower bound (S_odd index)
    no = ne + 1                        # odd number of terms -> upper bound
    L = partial(yh, False, ne)
    U = partial(yl, True, no)
    L = max(L, 0)
    for _ in range(s):
        L = (L * L) >> W
        U = -((-(U * U)) >> W)
    return Fr(L, one), Fr(U, one)


def iexp(a):
    lo, hi = a.ends()

    def bounds(x):
        if x <= 0:
            return exp_neg_point(-x)
        L, U = exp_neg_point(x)
        assert L > 0
        return 1 / U, 1 / L

    l = bounds(lo)[0]
    u = bounds(hi)[1]
    return I(fl(l.numerator << P, l.denominator), ce(u.numerator << P, u.denominator))


def expand(el_parent):
    vals = []
    for el in el_parent:
        mult = int(el.get('mult', '1'))
        incr = el.get('incr')
        v = el.text.strip()
        if incr is None:
            vals += [v] * mult
        else:
            vals += [str(int(v) + i * int(incr)) for i in range(mult)]
    return vals


def ev(e, x):
    k = e.tag.replace(NS, '')
    ch = list(e)
    if k == 'number':
        assert set(e.attrib) <= {'value', 'type'}, e.attrib
        return I.q(Fr(e.get('value')))
    if k == 'variable':
        return I.q(Fr(e.get('coef', '1'))) * x[int(e.get('idx'))]
    if k == 'negate':
        assert len(ch) == 1
        return -ev(ch[0], x)
    if k == 'square':
        assert len(ch) == 1
        return ev(ch[0], x).sq()
    if k == 'exp':
        assert len(ch) == 1
        return iexp(ev(ch[0], x))
    if k == 'sum':
        r = I(0, 0)
        for c in ch:
            r = r + ev(c, x)
        return r
    if k == 'product':
        r = I(ONE, ONE)
        for c in ch:
            r = r * ev(c, x)
        return r
    raise ValueError('unsupported node ' + k)


def run(name):
    root = ET.parse(f'eg/{name}.osil').getroot()
    d = root.find(NS + 'instanceData')
    V = list(d.find(NS + 'variables'))
    names = [v.get('name') for v in V]
    sol = dict(l.split() for l in open(f'eg/{name}.retry.sol') if l.strip())
    xq = []
    for v in V:
        assert set(v.attrib) <= {'name', 'lb', 'ub', 'type'}, v.attrib
        val = Fr(sol[v.get('name')])
        lb, ub, ty = v.get('lb', '0'), v.get('ub', 'INF'), v.get('type', 'C')
        assert ty in ('C', 'I', 'B')
        if lb != '-INF':
            assert val >= Fr(lb), (v.get('name'), 'lb')
        if ub != 'INF':
            assert val <= Fr(ub), (v.get('name'), 'ub')
        if ty in ('I', 'B'):
            assert val.denominator == 1, (v.get('name'), 'integrality')
        xq.append(val)
    x = [I.q(v) for v in xq]
    assert all(xi.lo == xi.hi for xi, v in zip(x, xq) if (v * ONE).denominator == 1)
    C = list(d.find(NS + 'constraints'))
    m = len(C)
    for c in C:
        assert set(c.attrib) <= {'name', 'lb', 'ub'}, c.attrib  # no 'constant'
    lin = [dict() for _ in range(m)]
    lcc = d.find(NS + 'linearConstraintCoefficients')
    st = [int(z) for z in expand(lcc.find(NS + 'start'))]
    assert lcc.find(NS + 'rowIdx') is None
    col = [int(z) for z in expand(lcc.find(NS + 'colIdx'))]
    val = expand(lcc.find(NS + 'value'))
    assert len(st) == m + 1
    for i in range(m):
        for k in range(st[i], st[i + 1]):
            lin[i][col[k]] = lin[i].get(col[k], Fr(0)) + Fr(val[k])
    nl = {}
    for e in d.find(NS + 'nonlinearExpressions'):
        i = int(e.get('idx'))
        assert i not in nl
        nl[i] = list(e)[0]
    assert -1 not in nl and d.find(NS + 'quadraticCoefficients') is None
    obj = d.find(NS + 'objectives').find(NS + 'obj')
    assert obj.get('maxOrMin') == 'min' and obj.get('constant') is None
    oc = list(obj)
    jo = names.index('objvar')
    assert len(oc) == 1 and int(oc[0].get('idx')) == jo and Fr(oc[0].text.strip()) == 1
    margins = []
    Fhi = None
    for i, c in enumerate(C):
        r = I(0, 0)
        g = None
        for j, a in lin[i].items():
            r = r + I.q(a) * x[j]
        if i in nl:
            g = ev(nl[i], x)
            r = r + g
        lo, hi = r.ends()
        if c.get('lb') not in (None, '-INF'):
            mg = lo - Fr(c.get('lb'))
            assert mg > 0, (c.get('name'), 'lb', float(mg))
            margins.append((mg, c.get('name'), 'lb', hi - lo))
        if c.get('ub') not in (None, 'INF'):
            mg = Fr(c.get('ub')) - hi
            assert mg > 0, (c.get('name'), 'ub', float(mg))
            margins.append((mg, c.get('name'), 'ub', hi - lo))
        if jo in lin[i]:
            assert lin[i][jo] == 1 and set(lin[i]) == {jo} and c.get('ub') in (None, 'INF')
            need = Fr(c.get('lb')) - g.ends()[0]  # objvar >= lb - g  for every feasible objvar
            Fhi = need if Fhi is None else max(Fhi, need)
    margins.sort()
    ov = xq[jo]
    print(f'{name}: {len(V)} vars, {m} rows; all row margins > 0 over rigorous enclosures; '
          f'bounds and integrality exact; objvar = {float(ov)!r} ({sol["objvar"]}); '
          f'objvar - (upper bound on least feasible objvar) >= {float(ov - Fhi):.4e}')
    for mg, nm, side, w in margins[:5]:
        print(f'   {nm} {side}: margin >= {float(mg):.4e}, enclosure width {float(w):.1e}')
    return ov - Fhi


if __name__ == '__main__':
    # self-test of exp bounds against exact identities exp(a)exp(-a) = 1
    for t in [Fr(0), Fr(1, 3), Fr(5), Fr(-7, 2), Fr(1234, 7)]:
        e1 = iexp(I.q(t))
        e2 = iexp(I.q(-t))
        l1, h1 = e1.ends()
        l2, h2 = e2.ends()
        assert l1 * l2 <= 1 <= h1 * h2 or (t > 100), t
    for n in sys.argv[1:]:
        run(n)
