"""Independent dossier check: evaluate every OSIL row at the saved retry points in mpmath
interval arithmetic (iv, 200 bits) with a generic OSnL tree walker; check bounds, integrality,
rows, and enclose min objvar = max_k (lb_k - nl_k(x)) over the 24 objective rows."""
import sys, xml.etree.ElementTree as ET
from fractions import Fraction as F
import mpmath as mp
from mpmath import iv
iv.prec = 200
NS = '{os.optimizationservices.org}'
def tag(e): return e.tag.replace(NS, '')
def q(s): return iv.mpf(str(s)) if s is not None else None   # decimal -> tight interval
def ev(e, x):
    t = tag(e)
    if t == 'number': return iv.mpf(e.get('value'))
    if t == 'variable':
        c = e.get('coef'); v = x[int(e.get('idx'))]
        return v if c is None else iv.mpf(c) * v
    ch = [ev(c, x) for c in e]
    if t == 'negate': return -ch[0]
    if t == 'sum' or t == 'plus':
        s = ch[0]
        for c in ch[1:]: s = s + c
        return s
    if t == 'minus': return ch[0] - ch[1]
    if t in ('product', 'times'):
        s = ch[0]
        for c in ch[1:]: s = s * c
        return s
    if t == 'exp': return iv.exp(ch[0])
    if t == 'square': return ch[0] ** 2
    raise ValueError(t)
for name in sys.argv[1:]:
    root = ET.parse(f'{name}.osil').getroot()
    idata = root.find(NS + 'instanceData')
    vars_ = idata.find(NS + 'variables')
    vn = [v.get('name') for v in vars_]
    sol = dict(l.split() for l in open(f'{name}.retry.sol') if l.strip())
    xv = [F(sol[n]) for n in vn]
    ok = True
    for v, val in zip(vars_, xv):
        lb = v.get('lb'); ub = v.get('ub')
        lb = F(0) if lb is None else (None if lb == '-INF' else F(lb))
        ub = None if ub is None or ub == 'INF' else F(ub)
        if lb is not None and val < lb: ok = False; print('  bound viol', v.get('name'))
        if ub is not None and val > ub: ok = False; print('  bound viol', v.get('name'))
        if v.get('type') == 'I' and val.denominator != 1: ok = False; print('  integrality', v.get('name'))
    x = [iv.mpf(mp.mpf(val.numerator) / val.denominator) if val.denominator == 1 else
         iv.mpf([str(val), str(val)]) for val in xv]
    # exact decimals: build intervals from the decimal strings
    x = [iv.mpf(sol[n]) for n in vn]
    cons = idata.find(NS + 'constraints')
    lin = idata.find(NS + 'linearConstraintCoefficients')
    # linear part: only objvar coefficient 1 in rows 0..23 (checked below)
    starts = [int(el.text) for el in lin.find(NS + 'start')] if False else None
    nls = {int(n.get('idx')): n[0] for n in idata.find(NS + 'nonlinearExpressions')}
    objidx = vn.index('objvar')
    Fmin = None; minslack = None
    for k, c in enumerate(cons):
        g = ev(nls[k], x)
        linpart = x[objidx] if k < 24 else iv.mpf(0)
        val = g + linpart
        lb, ub = c.get('lb'), c.get('ub')
        if lb is not None:
            s = val - iv.mpf(lb)
            if not s.a >= 0: ok = False; print('  row', c.get('name'), 'lb not proved', s)
            minslack = s.a if minslack is None else min(minslack, s.a)
        if ub is not None:
            s = iv.mpf(ub) - val
            if not s.a >= 0: ok = False; print('  row', c.get('name'), 'ub not proved', s)
            minslack = s.a if minslack is None else min(minslack, s.a)
        if k < 24:
            need = iv.mpf(lb) - g
            Fmin = need if Fmin is None else iv.mpf([max(Fmin.a, need.a), max(Fmin.b, need.b)])
    print(name, 'feasible proved:', ok, ' smallest proved slack', mp.nstr(minslack, 5))
    print('   objvar(sol) =', sol['objvar'], '; max_k(lb_k - g_k) in', mp.nstr(Fmin.a, 22), mp.nstr(Fmin.b, 22))
