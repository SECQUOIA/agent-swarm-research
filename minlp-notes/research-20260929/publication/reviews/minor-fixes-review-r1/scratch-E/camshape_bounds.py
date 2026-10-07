"""Group E independent check: bound differences MINLPLib camshape vs QPLIB copies,
QPLIB-point violations of MINLPLib bounds, and p1 row violation in camshape800.
Exact rationals; statement-level parser (split on ';'), eval-based rows."""
import re, sys
from fractions import Fraction as F
from pathlib import Path

D = Path(__file__).resolve().parents[3] / 'literature/control/sources/qplib/camshape_copies'
SOL = Path(__file__).resolve().parents[4] / 'open-instances/minlplib_sol'
TOK = re.compile(r'(objvar|x\d+)|(\d+\.?\d*(?:[eE][+-]?\d+)?)')


def stmts(path):
    txt = '\n'.join(l for l in open(path).read().splitlines() if not l.lstrip().startswith('*'))
    return [' '.join(s.split()) for s in txt.split(';')]


def model(path, shift):
    def nm(v):
        return v if v == 'objvar' else 'x%d' % (int(v[1:]) - shift)
    bounds, rows = {}, []
    for s in stmts(path):
        m = re.fullmatch(r'(\w+)\.(lo|up|fx) = (\S+)', s)
        if m:
            b = bounds.setdefault(nm(m.group(1)), [None, None])
            v = F(m.group(3))
            if m.group(2) in ('lo', 'fx'): b[0] = v
            if m.group(2) in ('up', 'fx'): b[1] = v
            continue
        m = re.fullmatch(r'(e\d+)\.\. (.*) =([ELG])= (\S+)', s)
        if m:
            expr = TOK.sub(lambda t: "V['%s']" % nm(t.group(1)) if t.group(1) else "F('%s')" % t.group(2), m.group(2))
            expr = expr.replace('sqr(', 'SQ(')
            rows.append((m.group(1), compile(expr, m.group(1), 'eval'), m.group(3), F(m.group(4)), 'objvar' in m.group(2)))
    return bounds, rows


def point(path, shift):
    pt = {}
    for l in open(path):
        p = l.split()
        if len(p) >= 2 and re.fullmatch(r'x\d+|objvar', p[0]):
            pt[p[0] if p[0] == 'objvar' else 'x%d' % (int(p[0][1:]) - shift)] = F(p[1])
    return pt


def viol(mod, pt):
    bounds, rows = mod
    V = {k: pt.get(k, F(0)) for k in set(bounds) | set(pt)}

    class Z(dict):
        def __missing__(self, k): return F(0)
    V = Z(V)
    worst_row, worst_b = (F(0), None), (F(0), None)
    for name, code, sense, rhs, isobj in rows:
        if isobj: continue
        val = eval(code, {'F': F, 'SQ': lambda a: a * a, 'V': V})
        v = {'E': abs(val - rhs), 'L': max(val - rhs, F(0)), 'G': max(rhs - val, F(0))}[sense]
        if v > worst_row[0]: worst_row = (v, name)
    for k, (lo, up) in bounds.items():
        if k == 'objvar': continue
        if lo is not None and lo - V[k] > worst_b[0]: worst_b = (lo - V[k], k + '.lo')
        if up is not None and V[k] - up > worst_b[0]: worst_b = (V[k] - up, k + '.up')
    return worst_row, worst_b


overall = (0, None)
for n, q in [(100, 2738), (200, 2480), (400, 2703), (800, 3177)]:
    M = model(D / f'camshape{n}.gms', 0)
    Q = model(D / f'QPLIB_{q}.gms', 1)
    assert set(M[0]) == set(Q[0]), 'bounded variable sets differ'
    nb = sum(b is not None for v in M[0].values() for b in v)
    worst = (0.0, None)
    for v in M[0]:
        for i in (0, 1):
            a, b = M[0][v][i], Q[0][v][i]
            assert (a is None) == (b is None), (v, i)
            if a is None: continue
            d = abs(float(a - b)) / max(abs(float(a)), 1.0)
            if d > worst[0]: worst = (d, (v, 'lo' if i == 0 else 'up', str(a), str(b)))
    print(f'camshape{n}/QPLIB_{q}: {nb} finite bounds parsed; max rel bound diff {worst[0]:.4e} at {worst[1]}')
    if worst[0] > overall[0]: overall = (worst[0], (n, q) + worst[1])
    qp = point(D / f'QPLIB_{q}.sol', 1)
    r, b = viol(M, qp)
    print(f'   QPLIB point in MINLPLib model: max row viol {float(r[0]):.4e} ({r[1]}); max bound viol {float(b[0]):.5e} ({b[1]})')
    if n == 800:
        p1 = point(SOL / 'camshape800.p1.sol', 0)
        r, b = viol(M, p1)
        print(f'   MINLPLib p1 in MINLPLib camshape800: max row viol {float(r[0]):.4e} ({r[1]}); bound viol {float(b[0]):.3e} ({b[1]})')
        r, b = viol(Q, p1)
        print(f'   MINLPLib p1 in QPLIB_3177: max row viol {float(r[0]):.4e} ({r[1]}); bound viol {float(b[0]):.3e} ({b[1]})')
print('overall max rel bound diff', f'{overall[0]:.4e}', overall[1])
