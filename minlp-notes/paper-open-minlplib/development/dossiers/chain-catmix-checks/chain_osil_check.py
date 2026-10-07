"""Independent (xml.etree) reading of chainN.osil; compare objective, length row and linear rows with the
polyline piece form at random z (mpmath, 50 digits)."""
from pathlib import Path as _PublicPath
_PUBLIC_HOME = str(_PublicPath.home())

import sys, random
import xml.etree.ElementTree as ET
import mpmath as mp
mp.mp.dps = 50
NS = '{os.optimizationservices.org}'
def expand(el_parent, cast):
    out = []
    for el in el_parent.findall(NS + 'el'):
        m = int(el.get('mult', '1')); inc = el.get('incr'); v = el.text
        for t in range(m):
            out.append(cast(v) + (t * cast(inc) if inc else 0))
    return out
def ev(node, X):
    tag = node.tag[len(NS):]
    ch = list(node)
    if tag == 'variable':
        return mp.mpf(node.get('coef', '1')) * X[int(node.get('idx'))]
    if tag == 'number':
        return mp.mpf(node.get('value'))
    if tag == 'sum':
        return mp.fsum(ev(c, X) for c in ch)
    if tag == 'product':
        r = mp.mpf(1)
        for c in ch: r *= ev(c, X)
        return r
    if tag == 'times':
        return ev(ch[0], X) * ev(ch[1], X)
    if tag == 'plus':
        return ev(ch[0], X) + ev(ch[1], X)
    if tag == 'minus':
        return ev(ch[0], X) - ev(ch[1], X)
    if tag == 'negate':
        return -ev(ch[0], X)
    if tag == 'sqrt':
        return mp.sqrt(ev(ch[0], X))
    if tag == 'square':
        return ev(ch[0], X) ** 2
    raise ValueError(tag)
for N in [int(v) for v in sys.argv[1:]]:
    root = ET.parse((_PUBLIC_HOME + '/.cache/minlplib/minlplib/osil/chain%d.osil') % N).getroot()
    inst = root.find(NS + 'instanceData')
    vars_ = inst.find(NS + 'variables').findall(NS + 'var')
    assert len(vars_) == 2 * N + 2
    bnds = [(v.get('lb', '0'), v.get('ub', 'INF'), v.get('type', 'C')) for v in vars_]
    fin = [(j, b) for j, b in enumerate(bnds) if b[:2] != ('-INF', 'INF')]
    obj = inst.find(NS + 'objectives').find(NS + 'obj')
    cons = inst.find(NS + 'constraints').findall(NS + 'con')
    lcc = inst.find(NS + 'linearConstraintCoefficients')
    start = expand(lcc.find(NS + 'start'), int)
    col = expand(lcc.find(NS + 'colIdx'), int)
    val = expand(lcc.find(NS + 'value'), mp.mpf)
    nls = {int(nl.get('idx')): nl[0] for nl in inst.find(NS + 'nonlinearExpressions').findall(NS + 'nl')}
    print(N, 'finite bounds:', fin, ' types:', set(b[2] for b in bnds), ' obj attrs:', obj.attrib, ' nl rows:', sorted(nls))
    eta = mp.mpf(1) / (2 * N); h = 2 * eta
    rnd = random.Random(N)
    worst = 0
    for trial in range(3):
        z = [None] + [mp.mpf(rnd.uniform(-1.0, 3.5)) for _ in range(N)]   # z_1..z_N
        z0 = 2 - z[1]; zN1 = 6 - z[N]
        zz = [z0] + z[1:] + [zN1]   # z_0..z_{N+1}
        x = [(zz[i] + zz[i + 1]) / 2 for i in range(N + 1)]
        u = [(zz[i + 1] - zz[i]) / h for i in range(N + 1)]
        X = x + u
        assert abs(X[0] - 1) < mp.mpf(10)**-45 and abs(X[N] - 3) < mp.mpf(10)**-45
        rows = []
        for r in range(len(cons)):
            lin = mp.fsum(val[k] * X[col[k]] for k in range(start[r], start[r + 1]))
            rows.append(lin + (ev(nls[r], X) if r in nls else 0))
        f = ev(nls[-1], X)
        lam0 = mp.sqrt(eta**2 + (z[1] - 1)**2); lamN = mp.sqrt(eta**2 + (3 - z[N])**2)
        lam = {k: mp.sqrt(h**2 + (z[k + 1] - z[k])**2) for k in range(1, N)}
        fpiece = lam0 + 3 * lamN + mp.fsum(lam[k] * (z[k] + z[k + 1]) / 2 for k in range(1, N))
        lpiece = lam0 + lamN + mp.fsum(lam.values())
        lin_res = max(abs(rows[r] - mp.mpf(cons[r].get('lb'))) for r in range(len(cons)) if r not in nls)
        nlr = [r for r in range(len(cons)) if r in nls]
        worst = max(worst, abs(f - fpiece), abs(rows[nlr[0]] - lpiece), lin_res)
        rhs = [cons[r].get('lb') for r in nlr]
    print('   nonlinear row rhs', rhs, ' max |OSIL - piece form| over 3 random z:', mp.nstr(worst, 3))
