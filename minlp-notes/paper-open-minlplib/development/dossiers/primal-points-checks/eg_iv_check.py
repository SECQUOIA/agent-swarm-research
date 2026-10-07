# Rigorous re-check of the eg_* primal points with outward-rounded interval
# arithmetic in Python's decimal module (libmpdec); independent of mpmath.
# exp: decimal's exp is documented as correctly rounded (ROUND_HALF_EVEN), so
# next_minus/next_plus of the rounded value bound the true value.
import sys, xml.etree.ElementTree as ET
from decimal import Decimal, Context, ROUND_FLOOR, ROUND_CEILING, ROUND_HALF_EVEN
from fractions import Fraction as F
P = 60
DN = Context(prec=P, rounding=ROUND_FLOOR, Emin=-999999, Emax=999999)
UP = Context(prec=P, rounding=ROUND_CEILING, Emin=-999999, Emax=999999)
NE = Context(prec=P, rounding=ROUND_HALF_EVEN, Emin=-999999, Emax=999999)
NS = '{os.optimizationservices.org}'
def t(e): return e.tag.replace(NS, '')
def iadd(a, b): return (DN.add(a[0], b[0]), UP.add(a[1], b[1]))
def imul(a, b):
    lo = min(DN.multiply(x, y) for x in a for y in b)
    hi = max(UP.multiply(x, y) for x in a for y in b)
    return (lo, hi)
def ineg(a): return (a[1].copy_negate(), a[0].copy_negate())  # exact; unary minus would round to 28 digits
def isq(a):
    lo, hi = a
    if lo >= 0: return (DN.multiply(lo, lo), UP.multiply(hi, hi))
    if hi <= 0: return (DN.multiply(hi, hi), UP.multiply(lo, lo))
    return (Decimal(0), max(UP.multiply(lo, lo), UP.multiply(hi, hi)))
def iexp(a):
    lo = NE.next_minus(NE.exp(a[0])); hi = NE.next_plus(NE.exp(a[1]))
    return (max(lo, Decimal(0)), hi)
def ev(e, x):
    k = t(e)
    if k == 'number': v = Decimal(e.get('value')); return (v, v)
    if k == 'variable':
        c = Decimal(e.get('coef', '1')); return imul((c, c), x[int(e.get('idx'))])
    ch = list(e)
    if k == 'negate': return ineg(ev(ch[0], x))
    if k == 'square': return isq(ev(ch[0], x))
    if k == 'exp': return iexp(ev(ch[0], x))
    if k == 'sum':
        r = (Decimal(0), Decimal(0))
        for c in ch: r = iadd(r, ev(c, x))
        return r
    if k == 'product':
        r = (Decimal(1), Decimal(1))
        for c in ch: r = imul(r, ev(c, x))
        return r
    raise ValueError('unsupported node ' + k)
def expand(el_parent):
    vals = []
    for el in el_parent:
        mult = int(el.get('mult', '1')); incr = el.get('incr')
        v = el.text.strip()
        if incr is None: vals += [v] * mult
        else:
            v0 = int(v); inc = int(incr); vals += [str(v0 + i * inc) for i in range(mult)]
    return vals
def bnd(s, default):
    if s is None: return default
    if s in ('INF', 'inf', 'Infinity'): return None if default is None else 'inf'
    return s
def main(name):
    root = ET.parse(f'eg/{name}.osil').getroot()
    data = root.find(NS + 'instanceData')
    vars_ = list(data.find(NS + 'variables'))
    names = [v.get('name') for v in vars_]
    sol = dict(l.split() for l in open(f'eg/{name}.retry.sol') if l.strip())
    x = []
    worst_bound = None
    for v in vars_:
        val = Decimal(sol[v.get('name')]); x.append((val, val))
        lb = v.get('lb', '0'); ub = v.get('ub', 'INF')
        fv = F(val)
        if lb != '-INF': assert fv >= F(Decimal(lb)), (v.get('name'), 'lb')
        if ub != 'INF': assert fv <= F(Decimal(ub)), (v.get('name'), 'ub')
        if v.get('type', 'C') in ('I', 'B'): assert fv.denominator == 1, (v.get('name'), 'int')
        assert v.get('type', 'C') in ('C', 'I', 'B')
    cons = list(data.find(NS + 'constraints'))
    m = len(cons)
    lin = [dict() for _ in range(m)]
    lcc = data.find(NS + 'linearConstraintCoefficients')
    if lcc is not None:
        start = [int(s) for s in expand(lcc.find(NS + 'start'))]
        col = [int(s) for s in expand(lcc.find(NS + 'colIdx'))]
        val = expand(lcc.find(NS + 'value'))
        for i in range(m):
            for k in range(start[i], start[i + 1]): lin[i][col[k]] = Decimal(val[k])
    nl = {}
    for e in data.find(NS + 'nonlinearExpressions'):
        nl[int(e.get('idx'))] = list(e)[0]
    obj = data.find(NS + 'objectives').find(NS + 'obj')
    assert obj.get('maxOrMin') == 'min' and obj.get('constant') is None
    oc = list(obj); assert len(oc) == 1 and int(oc[0].get('idx')) == names.index('objvar') and oc[0].text.strip() == '1'
    assert -1 not in nl and data.find(NS + 'quadraticCoefficients') is None
    minmargin = None; Fhi = None
    for i, c in enumerate(cons):
        r = (Decimal(0), Decimal(0))
        for j, a in lin[i].items(): r = iadd(r, imul((a, a), x[j]))
        if i in nl: r = iadd(r, ev(nl[i], x))
        lb = c.get('lb'); ub = c.get('ub')
        if lb is not None and lb != '-INF':
            mg = DN.subtract(r[0], Decimal(lb)); assert mg > 0, (c.get('name'), 'lb', mg)
            minmargin = mg if minmargin is None or mg < minmargin[0] else minmargin
            if minmargin is mg: minmargin = (mg, c.get('name'))
        if ub is not None and ub != 'INF':
            mg = DN.subtract(Decimal(ub), r[1]); assert mg > 0, (c.get('name'), 'ub', mg)
        if names.index('objvar') in lin[i]:
            # objvar + g_i(x) >= lb_i  -> objvar >= lb_i - g_i
            g = ev(nl[i], x); need = UP.subtract(Decimal(lb), g[0])
            Fhi = need if Fhi is None else max(Fhi, need)
    ov = x[names.index('objvar')][0]
    margins = []
    for i, c in enumerate(cons):
        r = (Decimal(0), Decimal(0))
        for j, a in lin[i].items(): r = iadd(r, imul((a, a), x[j]))
        if i in nl: r = iadd(r, ev(nl[i], x))
        lb = c.get('lb'); ub = c.get('ub')
        s = []
        if lb is not None: s.append(float(DN.subtract(r[0], Decimal(lb))))
        if ub is not None: s.append(float(DN.subtract(Decimal(ub), r[1])))
        margins.append((min(s), c.get('name'), float(r[1] - r[0])))
    margins.sort()
    print(f'{name}: all {m} rows hold rigorously; bounds/integrality exact OK; objective (objvar) = {ov}; '
          f'least feasible objvar F(x) <= {UP.plus(Fhi):.25} ; objvar - F_hi >= {float(DN.subtract(ov, Fhi)):.3e}')
    print('   smallest row margins:', [(f'{a:.3e}', b, f'w={w:.1e}') for a, b, w in margins[:4]])
for n in sys.argv[1:]: main(n)
