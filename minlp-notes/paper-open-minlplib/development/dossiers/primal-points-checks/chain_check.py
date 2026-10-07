# Independent exact check of the chain points in Q(sqrt(D)) from the generator data
# and the OSIL expression trees (own parser and field arithmetic).
import sys, json, xml.etree.ElementTree as ET
from fractions import Fraction as F
from decimal import Decimal
from math import isqrt
NS = '{os.optimizationservices.org}'
def Q(s): return F(Decimal(s))
class E:  # p + q*sqrt(D), D a positive rational non-square
    D = None
    __slots__ = ('p', 'q')
    def __init__(s, p, q=F(0)): s.p = F(p); s.q = F(q)
    def __add__(s, o): o = o if isinstance(o, E) else E(o); return E(s.p+o.p, s.q+o.q)
    __radd__ = __add__
    def __neg__(s): return E(-s.p, -s.q)
    def __sub__(s, o): return s + (-(o if isinstance(o, E) else E(o)))
    def __mul__(s, o): o = o if isinstance(o, E) else E(o); return E(s.p*o.p + s.q*o.q*E.D, s.p*o.q + s.q*o.p)
    __rmul__ = __mul__
    def inv(s): n = s.p*s.p - s.q*s.q*E.D; return E(s.p/n, -s.q/n)
    def sign(s):
        a, b = s.p, s.q
        if b == 0: return (a > 0) - (a < 0)
        if a == 0: return (b > 0) - (b < 0)
        if (a > 0) == (b > 0): return 1 if a > 0 else -1
        c = a*a - b*b*E.D  # sign of a + b sqrt D equals sign(a) if a^2 > b^2 D
        return (1 if a > 0 else -1) if c > 0 else (1 if b > 0 else -1)
    def iszero(s): return s.p == 0 and s.q == 0
def expand(p):
    out = []
    for el in p:
        mult = int(el.get('mult', '1')); incr = el.get('incr'); v = el.text.strip()
        out += [v]*mult if incr is None else [str(int(v)+i*int(incr)) for i in range(mult)]
    return out
def run(N):
    g = json.load(open(f'data/chain{N}_generator.json'))
    a, b = g['a'], g['b']; t = g['t']
    w = [1 if i in (0, N) else 2 for i in range(N+1)]
    S1 = sum(w[i]*Q(t[i]) for i in range(N+1) if i not in (a, b))
    S2 = sum(w[i]/Q(t[i]) for i in range(N+1) if i not in (a, b))
    alpha = (12*N - S1)/2; beta = (4*N - S2)/2
    disc = alpha*alpha - 4*alpha/beta
    assert disc > 0 and not (isqrt(disc.numerator)**2 == disc.numerator and isqrt(disc.denominator)**2 == disc.denominator)
    E.D = disc
    tt = [E(Q(t[i])) if i not in (a, b) else None for i in range(N+1)]
    tt[a] = E(alpha/2, F(-1, 2)); tt[b] = E(alpha/2, F(1, 2))  # smaller root at a
    assert tt[a].sign() > 0 and (tt[b] - tt[a]).sign() > 0
    u = [(ti - ti.inv())*F(1, 2) for ti in tt]
    s = [(ti + ti.inv())*F(1, 2) for ti in tt]
    root = ET.parse(f'data/chain{N}.osil').getroot(); d = root.find(NS+'instanceData')
    V = list(d.find(NS+'variables')); assert len(V) == 2*N+2
    # x from x_0 = 1 via x_{i+1} = x_i + eta (u_i + u_{i+1}); eta read from the OSIL below
    lcc = d.find(NS+'linearConstraintCoefficients')
    start = [int(z) for z in expand(lcc.find(NS+'start'))]; col = [int(z) for z in expand(lcc.find(NS+'colIdx'))]; val = expand(lcc.find(NS+'value'))
    eta = F(1, 2*N)
    x = [E(1)]
    for i in range(N): x.append(x[i] + eta*(u[i] + u[i+1]))
    X = x + u   # OSIL order: x_0..x_N then u_0..u_N (checked by the rows below)
    for v, xv in zip(V, X):
        lb = v.get('lb', '0'); ub = v.get('ub', 'INF'); assert v.get('type', 'C') == 'C'
        if lb != '-INF': assert (xv - Q(lb)).sign() >= 0, v.get('name')
        if ub != 'INF': assert (E(Q(ub)) - xv).sign() >= 0, v.get('name')
    cands = s
    def ev(e):
        k = e.tag.replace(NS, ''); ch = list(e)
        if k == 'number': return E(Q(e.get('value')))
        if k == 'variable': return Q(e.get('coef', '1')) * X[int(e.get('idx'))]
        if k == 'sum':
            r = E(0)
            for c in ch: r = r + ev(c)
            return r
        if k == 'product':
            r = E(1)
            for c in ch: r = r * ev(c)
            return r
        if k == 'square': z = ev(ch[0]); return z*z
        if k == 'sqrt':
            arg = ev(ch[0])
            for c in cands:  # accept only an exact nonnegative square root
                if (c*c - arg).iszero() and c.sign() >= 0: return c
            raise ValueError('sqrt argument has no listed exact root')
        raise ValueError(k)
    C = list(d.find(NS+'constraints')); m = len(C)
    rows = [E(0) for _ in range(m)]
    for i in range(m):
        for k in range(start[i], start[i+1]): rows[i] = rows[i] + Q(val[k])*X[col[k]]
    obj = None
    for e in d.find(NS+'nonlinearExpressions'):
        i = int(e.get('idx')); r = ev(list(e)[0])
        if i == -1: obj = r
        else: rows[i] = rows[i] + r
    o = d.find(NS+'objectives').find(NS+'obj'); assert o.get('maxOrMin', 'min') == 'min' and o.get('constant') is None and len(list(o)) == 0
    for i, c in enumerate(C):
        lb, ub = c.get('lb'), c.get('ub'); assert lb is not None and lb == ub
        assert (rows[i] - Q(lb)).iszero(), c.get('name')
    # enclose objective: p + q sqrt(D)
    Dn, Dd = disc.numerator, disc.denominator
    K = 10**80
    r_lo = F(isqrt(Dn*Dd*K*K), Dd*K); r_hi = r_lo + F(1, Dd*K)   # sqrt(D) in [r_lo, r_hi]
    vals = [obj.p + obj.q*r_lo, obj.p + obj.q*r_hi]
    lo, hi = min(vals), max(vals)
    box = json.load(open(f'data/chain{N}_box.json'))
    oe = box['objective_enclosure_decimal']; oe = eval(oe) if isinstance(oe, str) else oe
    print(f'chain{N}: {m} rows exact, bounds exact; f in [{float(lo)!r}, {float(hi)!r}] (width {float(hi-lo):.1e}); inside stored 40-dp enclosure: {Q(oe[0]) <= lo and hi <= Q(oe[1])}')
for N in map(int, sys.argv[1:]): run(N)
