"""Dossier check (own code): parse the MINLPLib OSIL of an eg_* instance generically
(variables, bounds, types, linear coefficients with mult/incr decompression, row bounds,
OSnL trees) and evaluate every row at the saved .sol point in mpmath interval arithmetic.
Also prints structural facts: term counts, shared centres, common gamma per row, e27 == e28."""
import sys, xml.etree.ElementTree as ET
from fractions import Fraction as F
import mpmath as mp
from mpmath import iv
iv.prec = 200
NS = '{os.optimizationservices.org}'
T = lambda e: e.tag.replace(NS, '')

def expand(els):
    out = []
    for el in els:
        mult = int(el.get('mult', '1')); incr = el.get('incr')
        v = el.text.strip()
        if incr is None:
            out += [v] * mult
        else:
            base = int(v); inc = int(incr)
            out += [str(base + j * inc) for j in range(mult)]
    return out

def load(name):
    r = ET.parse(f'{name}.osil').getroot().find(NS + 'instanceData')
    V = [(v.get('name'), v.get('type', 'C'), v.get('lb'), v.get('ub')) for v in r.find(NS + 'variables')]
    obj = r.find(NS + 'objectives')[0]
    C = [(c.get('name'), c.get('lb'), c.get('ub')) for c in r.find(NS + 'constraints')]
    L = r.find(NS + 'linearConstraintCoefficients')
    start = [int(s) for s in expand(L.find(NS + 'start'))]
    col = [int(s) for s in expand(L.find(NS + 'colIdx'))]
    val = expand(L.find(NS + 'value'))
    lin = {k: [(col[j], val[j]) for j in range(start[k], start[k + 1])] for k in range(len(C))}
    NL = {int(n.get('idx')): n[0] for n in r.find(NS + 'nonlinearExpressions')}
    return V, obj, C, lin, NL

def ev(e, x):
    t = T(e)
    if t == 'number': return iv.mpf(e.get('value'))
    if t == 'variable':
        c = e.get('coef'); v = x[int(e.get('idx'))]
        return v if c is None else iv.mpf(c) * v
    ch = [ev(c, x) for c in e]
    if t == 'negate': return -ch[0]
    if t == 'sum':
        s = ch[0]
        for c in ch[1:]: s = s + c
        return s
    if t == 'product':
        s = ch[0]
        for c in ch[1:]: s = s * c
        return s
    if t == 'exp': return iv.exp(ch[0])
    if t == 'square': return ch[0] ** 2
    raise ValueError(t)

def terms(nl):
    """decode one row into (sign, [(a, centres(7), gammas(7), coefs(7))], linear list)."""
    root = nl; sign = 1
    if T(root) == 'negate': sign = -1; root = root[0]
    assert T(root) == 'sum'
    out, linear = [], []
    for p in root:
        if T(p) == 'variable':
            linear.append((int(p.get('idx')), p.get('coef'))); continue
        assert T(p) == 'product', T(p)
        a = None; fac = {}
        for f in p:
            if T(f) == 'number': a = f.get('value'); continue
            assert T(f) == 'exp'
            pr = f[0]; assert T(pr) == 'product'
            sq, g = pr[0], pr[1]; assert T(sq) == 'square' and T(g) == 'number'
            sm = sq[0]; assert T(sm) == 'sum' and T(sm[0]) == 'number' and T(sm[1]) == 'variable'
            i = int(sm[1].get('idx')); fac[i] = (sm[0].get('value'), g.get('value'), sm[1].get('coef'))
        out.append((a, fac))
    return sign, out, linear

for name in sys.argv[1:]:
    V, obj, C, lin, NL = load(name)
    vn = [v[0] for v in V]
    print(f"== {name}: {len(V)} vars, {len(C)} rows; objective {obj.get('maxOrMin')} "
          f"{[(c.get('idx'), c.text) for c in obj]}; linear coeffs {sum(len(v) for v in lin.values())}")
    print("   vars:", [(n, t, lb, ub) for n, t, lb, ub in V])
    assert all(lin[k] == [(7, '1')] for k in range(24)) and all(lin[k] == [] for k in range(24, 28))
    # structure
    rows = [terms(NL[k]) for k in range(28)]
    nterms = [len(r[1]) for r in rows]
    cent = [sorted(tuple(F(fac[i][0]) for i in range(7)) for a, fac in r[1]) for r in rows]
    same_c = all(c == cent[0] for c in cent)
    gam_common = all(len({tuple(fac[i][1] for i in range(7)) for a, fac in r[1]}) == 1 for r in rows)
    coefs = {tuple(fac[i][2] for i in range(7)) for r in rows for a, fac in r[1]}
    e27 = sorted((F(a), tuple(F(fac[i][0]) for i in range(7))) for a, fac in rows[26][1])
    e28 = sorted((F(a), tuple(F(fac[i][0]) for i in range(7))) for a, fac in rows[27][1])
    g27 = {tuple(fac[i][1] for i in range(7)) for a, fac in rows[26][1]}; g28 = {tuple(fac[i][1] for i in range(7)) for a, fac in rows[27][1]}
    signs = [r[0] for r in rows]
    print(f"   terms/row {set(nterms)}; all rows negated: {set(signs)}; same 97 centres in all rows: {same_c}; "
          f"gamma common per row: {gam_common}; scale coefficients: {coefs}")
    print(f"   e27 and e28: same signed terms (sign {rows[26][0]},{rows[27][0]}): {e27 == e28 and g27 == g28 and rows[26][2] == rows[27][2]}")
    print(f"   linear terms inside nl: {[(k + 1, r[2]) for k, r in enumerate(rows) if r[2]]}")
    print(f"   row bounds e25..e28: {C[24:]}")
    sa = [sum(abs(F(a)) for a, fac in r[1]) for r in rows]
    print(f"   sum|a|: objective rows {float(min(sa[:24])):.1f}..{float(max(sa[:24])):.1f}; side {[round(float(v), 1) for v in sa[24:]]}")
    # primal point
    sol = dict(l.split() for l in open(f'{name}.retry.sol') if l.strip())
    xq = [F(sol[n]) for n in vn]
    ok = True
    for (n, t, lb, ub), q in zip(V, xq):
        if lb not in (None, '-INF') and q < F(lb): ok = False; print('   bound viol', n)
        if lb is None and q < 0: ok = False; print('   bound viol (default lb 0)', n)
        if ub not in (None, 'INF') and q > F(ub): ok = False; print('   bound viol', n)
        if t == 'I' and q.denominator != 1: ok = False; print('   integrality', n)
    x = [iv.mpf(sol[n]) for n in vn]
    slacks = []; Fenc = []
    for k, (cn, lb, ub) in enumerate(C):
        g = ev(NL[k], x)
        val = g + (x[7] if k < 24 else 0)
        if lb is not None:
            s = val - iv.mpf(lb); slacks.append((cn, s.a)); ok &= s.a > 0
        if ub is not None:
            s = iv.mpf(ub) - val; slacks.append((cn, s.a)); ok &= s.a > 0
        if k < 24: Fenc.append(iv.mpf(lb) - g)
    lo = max(f.a for f in Fenc); hi = max(f.b for f in Fenc)
    sm = min(slacks, key=lambda z: z[1])
    print(f"   point {[sol[n] for n in vn[:7]]}: bounds/integrality/rows proved: {ok}; smallest proved slack {mp.nstr(sm[1], 4)} ({sm[0]})")
    print(f"   objvar in sol = {sol['objvar']}; F(x*) = max_k (c_k + G_k) in [{mp.nstr(lo, 25)}, {mp.nstr(hi, 25)}]")
    act = sorted(((mp.nstr(hi - f.b, 3), k + 1) for k, f in enumerate(Fenc) if hi - f.b < 1e-6), key=lambda z: z[1])
    print(f"   objective rows within 1e-6 of the max: {act}")
