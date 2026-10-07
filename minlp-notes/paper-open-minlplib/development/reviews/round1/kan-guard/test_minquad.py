"""Independent exact oracle and deterministic regressions; execute only in /tmp."""
import ast
import copy
import itertools
import json
import math
from pathlib import Path
import random
import struct
import sys
from fractions import Fraction as F
import numpy as np

HERE = Path(__file__).resolve().parent

def load(path, guarded):
    tree = ast.parse(path.read_text())
    names = {'minquad', '_minquad_exact'} if guarded else {'minquad'}
    nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in names]
    if guarded:
        nodes = [n for n in tree.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'MINQUAD_STATS' for t in n.targets)] + nodes
    ns = dict(np=np, INF=np.inf, sys=sys, Fr=F,
              dn=lambda x: np.nextafter(x, -np.inf), up=lambda x: np.nextafter(x, np.inf))
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(path), 'exec'), ns)
    return ns

new = load(HERE / 'kan_bnb_rigexp.py', True)
old = load(HERE / 'original_kan_bnb_rigexp.py', False)

def oracle(row):
    # Independent geometric oracle: the minimum over slopes chooses gh on the
    # negative half and gl on the positive half. Optimize those two quadratics.
    gl, gh, m, sl, sh = map(F, row)
    candidates = []
    for g, a, b in ((gh, sl, min(sh, F(0))), (gl, max(sl, F(0)), sh)):
        if a > b:
            continue
        value = lambda s: g*s + (m/2)*s*s
        candidates.extend((value(a), value(b)))
        if m > 0:
            vertex = -g/m
            if a <= vertex <= b:
                candidates.append(value(vertex))
    return min(candidates)

def assert_safe(value, exact, row):
    assert not math.isnan(value) and value != math.inf, (row, value)
    assert value == -math.inf or F(value) <= exact, (row, value, exact)

t = math.ulp(0.0)
probe = (0.0, 0.0, -t, -3.0, 3.0)
old_value = float(old['minquad'](*[np.array([x]) for x in probe])[0])
new_value = float(new['minquad'](*[np.array([x]) for x in probe])[0])
assert F(old_value) == -3*F(t) and oracle(probe) == -F(t)*9/2
assert new_value == -5*t
print('Referee probe: old = -3t (unsafe); guarded = -5t <= exact -9t/2')

rng = random.Random(20261004)
fmax = sys.float_info.max
normal = sys.float_info.min

def bits_float():
    while True:
        v = struct.unpack('>d', rng.getrandbits(64).to_bytes(8, 'big'))[0]
        if math.isfinite(v):
            return v

def mkrow(gs, m, ss):
    return (*sorted(gs), m, -abs(ss[0]), abs(ss[1]))

cases = []
for _ in range(20000):
    cases.append(('ordinary', mkrow((rng.uniform(-100,100), rng.uniform(-100,100)), rng.uniform(-100,100), (rng.uniform(0,10), rng.uniform(0,10)))))
for _ in range(20000):
    cases.append(('random_binary64', mkrow((bits_float(), bits_float()), bits_float(), (bits_float(),bits_float()))))
for _ in range(5000):
    cases.append(('subnormal', mkrow((rng.randint(-100,100)*t, rng.randint(-100,100)*t), rng.randint(-100,100)*t, (rng.uniform(0,20),rng.uniform(0,20)))))
# Every relevant boundary: smallest subnormals, normal transition, largest values,
# signed zero, zero displacement/gradient/curvature, and power-of-two ranges.
ms = [0., -0., t, -t, 2*t, -2*t, 3*t, -3*t, normal, -normal,
      math.nextafter(normal, math.inf), -math.nextafter(normal, math.inf), 1., -1., fmax, -fmax]
gs = [0., -0., t, -t, normal, -normal, 1., -1., fmax, -fmax]
widths = [0., t, 2*t, normal, 1., 3., math.ldexp(1., 512), fmax]
for m, g, a, b in itertools.product(ms, gs, widths, widths):
    cases.append(('boundary_grid', (g,g,m,-a,b)))
for _ in range(5000):
    m = math.ldexp(rng.uniform(1,2), rng.randint(-500,500))
    g = math.ldexp(rng.uniform(-2,2), rng.randint(-500,500))
    v = -g/m
    if not math.isfinite(v):
        continue
    for edge in (math.nextafter(v,-math.inf), v, math.nextafter(v,math.inf)):
        if v >= 0:
            row = (g,g,m,-abs(v),edge)
        else:
            row = (g,g,m,edge,abs(v))
        if row[3] <= 0 <= row[4]:
            cases.append(('vertex_boundary', row))
for _ in range(1000):
    s = rng.choice([0., -0., t, -t, normal, -normal, 1., -1., fmax, -fmax])
    cases.append(('zero_width', (*sorted((bits_float(),bits_float())), bits_float(), s, s)))
for _ in range(1000):
    a,b = sorted((abs(bits_float()),abs(bits_float())))
    if rng.getrandbits(1): a,b = -b,-a
    cases.append(('unsigned_interval', (*sorted((bits_float(),bits_float())), bits_float(), a,b)))

counts = {}
finite_returns = 0
for start in range(0,len(cases),1024):
    batch = cases[start:start+1024]
    data = np.array([row for _,row in batch]).T
    output = new['minquad'](*data)
    for (kind,row), val in zip(batch,output):
        assert_safe(float(val),oracle(row),row)
        counts[kind] = counts.get(kind,0)+1
        finite_returns += math.isfinite(float(val))
print('PASS exact rational comparisons:', json.dumps(counts,sort_keys=True))
print('Finite results:', finite_returns, '/', len(cases))

# Scalar and broadcasting interfaces, with all sign choices of zero.
for gl, gh, m, sl, sh in itertools.product((0.,-0.), repeat=5):
    val = float(new['minquad'](gl,gh,m,sl,sh))
    assert_safe(val,F(0),(gl,gh,m,sl,sh))
arr = new['minquad'](np.zeros((2,1)), np.ones((1,3)), 1., -1., 1.)
assert arr.shape == (2,3) and np.all(arr <= -.5)
assert new['minquad'](*(np.array([]) for _ in range(5))).size == 0
invalid = []
for pos in range(5):
    for val in (math.inf,-math.inf,math.nan):
        row = [0.,0.,1.,-1.,1.]
        row[pos] = val
        invalid.append(row)
invalid += [[1.,-1.,1.,-1.,1.], [0.,0.,1.,1.,-1.]]
for row in invalid:
    assert float(new['minquad'](*row)) == -math.inf
# Exercise rational-to-float overflow in both directions and exact cancellation.
# Positive overflow is possible on unsigned intervals; signed intervals contain
# zero, so their exact minimum cannot be positive.
conversion_probes = [
    ((0.,0.,fmax,fmax,fmax), fmax),
    ((0.,0.,-fmax,fmax,fmax), -math.inf),
    ((fmax,fmax,0.,1.,1.), fmax),
    ((fmax,fmax,-fmax,2.,2.), 0.),
]
for row,expected in conversion_probes:
    val=float(new['minquad'](*row))
    assert_safe(val,oracle(row),row)
    assert val==expected, (row,val,expected)
print('PASS four conversion probes: positive/negative overflow, maximum finite, exact cancellation')
stats = copy.deepcopy(new['MINQUAD_STATS'])
assert stats['guard_calls'] == stats['fallback_calls']
assert stats['guard_entries'] == stats['fallback_entries']
assert stats['invalid_entries'] == len(invalid)
assert all(v>0 for k,v in stats['reasons'].items() if k != 'nonpositive_denominator')
# Under finite input, denom cannot become <= 0: 2*mpos >= 2*t and
# its predecessor is >= t. NaN/negative inputs select mpos=1; +inf
# is caught by the finiteness guard. This defensive predicate stays false.
assert stats['reasons']['nonpositive_denominator'] == 0
print('PASS scalar, broadcast, empty, signed-zero and invalid-input contracts')
print('Counters:',json.dumps(stats,sort_keys=True))
summary = dict(seed=20261004, comparison_counts=counts, comparisons=len(cases),
               finite_returns=finite_returns, signed_zero_scalar_cases=32,
               invalid_cases=len(invalid), conversion_probes=len(conversion_probes), stats=stats,
               referee_probe=dict(old_over_t=-3, new_over_t=-5, exact_over_t='-9/2'))
(HERE / 'test-results.json').write_text(json.dumps(summary,indent=2)+'\n')
