"""Group C independent check: old waterno2_09..24 vectors vs OSIL bounds, and relative primal change.
Uses only the source decimal strings, the cached OSIL and the stored exact objective rationals."""
import json
import xml.etree.ElementTree as ET
from fractions import Fraction as F
from pathlib import Path

PUB = Path(__file__).resolve().parents[3]
SRC = PUB.parent / 'open-instances-wave2' / 'waterno2' / 'logs'
OSIL = Path.home() / '.cache/minlplib/minlplib/osil'
NS = '{os.optimizationservices.org}'


def sym_value(sym):
    # midpoint of the isolating interval, accurate to ~1e-45
    return (F(sym['lo']) + F(sym['hi'])) / 2


for n in ['09', '12', '18', '24']:
    name = f'waterno2_{n}'
    src = json.loads((SRC / f'primal_{n}_w2.json').read_text())
    ex = json.loads((PUB / 'primal/water-ann-kan/points' / f'{name}.exact.json').read_text())
    root = ET.parse(OSIL / f'{name}.osil').getroot()
    vs = list(root.find('.//' + NS + 'variables'))
    assert len(vs) == len(src['x']) == len(ex['x'])
    # alignment check: source coordinate j vs exact point at OSIL name j
    syms = {s['name'] if False else k: s for k, s in ex['symbols'].items()}
    maxdiff = F(0)
    for v, s in zip(vs, src['x']):
        e = ex['x'][v.get('name')]
        if isinstance(e, dict):
            w = sym_value(ex['symbols'][str(e['w'])])
            ev = F(e['c0']) + F(e['c1']) * w
        else:
            ev = F(e)
        maxdiff = max(maxdiff, abs(ev - F(s)))
    # bounds (OSIL defaults lb=0, ub=+inf)
    worst, where = F(0), None
    nviol = 0
    for v, s in zip(vs, src['x']):
        x = F(s)
        lb = v.get('lb', '0')
        ub = v.get('ub', 'INF')
        for side, b in (('lb', lb), ('ub', ub)):
            if 'INF' in b.upper():
                continue
            viol = F(b) - x if side == 'lb' else x - F(b)
            if viol > 0:
                nviol += 1
            if viol > worst:
                worst, where = viol, f"{v.get('name')} {side}={b} x={s}"
    # objective: linear in OSIL objective coefficients
    obj = root.find('.//' + NS + 'objectives')[0]
    const = F(obj.get('constant', '0'))
    old_eval = const + sum(F(c.text) * F(src['x'][int(c.get('idx'))]) for c in obj)
    old_float = F(repr(src['obj']))
    new = F(ex['objective'])
    print(f"{name}: align maxdiff {float(maxdiff):.3e}; bound violations {nviol}, max {float(worst):.10g} at {where}")
    print(f"   old obj (eval of decimals) {float(old_eval)!r}, stored float {src['obj']!r}, exact {float(new)!r}")
    print(f"   increase {float(new-old_eval):.4e}; rel (vs eval) {float((new-old_eval)/old_eval):.5e}; "
          f"rel (vs stored float) {float((new-old_float)/old_float):.5e}; rel (vs exact) {float((new-old_eval)/new):.5e}")
