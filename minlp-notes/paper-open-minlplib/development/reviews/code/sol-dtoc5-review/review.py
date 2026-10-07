"""Independent dtoc5 review: parse OSIL; exact primal and full rational dual.

No repository imports or numerical solvers. Fraction handles the small rationals;
system GMP handles balanced sums whose final denominator has millions of digits.
Run from this directory. Every input is copied here before it is parsed.
"""
from fractions import Fraction as F
from pathlib import Path
import ctypes as C
import ctypes.util
import gzip
import hashlib
import json
import os
import time
import xml.etree.ElementTree as ET

WORK = Path(__file__).resolve().parent
os.sched_setaffinity(0, {min(os.sched_getaffinity(0))})
started = time.monotonic()

hashes = {name: hashlib.sha256((WORK / name).read_bytes()).hexdigest()
          for name in ('dtoc5.osil', 'dtoc5_point.txt.gz', 'objective_reference.txt')}

def local(element):
    return element.tag.rsplit('}', 1)[-1]

def expand(element, convert):
    result = []
    for entry in element:
        assert local(entry) == 'el'
        first = convert(entry.text)
        count = int(entry.get('mult', '1'))
        increment = convert(entry.get('incr', '0'))
        result.extend(first + k * increment for k in range(count))
    return result

root = ET.parse(WORK / 'dtoc5.osil').getroot()
data = next(e for e in root if local(e) == 'instanceData')
sections = {local(e): e for e in data}
assert set(sections) == {'variables', 'objectives', 'constraints',
                         'linearConstraintCoefficients', 'quadraticCoefficients'}
variables = list(sections['variables'])
rows = list(sections['constraints'])
n, T = len(variables), len(rows)
assert n == int(sections['variables'].get('numberOfVariables')) == 99999
assert T == int(sections['constraints'].get('numberOfConstraints')) == 49999
assert [v.get('name') for v in variables] == [f'x{i}' for i in range(2, n + 2)]
assert all(v.get('type', 'C') == 'C' for v in variables)
fixed = {}
for j, v in enumerate(variables):
    lo, hi = v.get('lb', '0'), v.get('ub', 'INF')
    if lo not in ('-INF', 'INF') and hi not in ('-INF', 'INF') and F(lo) == F(hi):
        fixed[j] = F(lo)
    else:
        assert (lo, hi) == ('-INF', 'INF'), (j, lo, hi)
assert fixed == {T: F(1)}
for t, row in enumerate(rows):
    assert local(row) == 'con'
    assert row.get('name') == f'e{t + 2}'
    assert F(row.get('lb', '-INF')) == F(row.get('ub', 'INF')) == 0
    assert F(row.get('constant', '0')) == 0
objects = list(sections['objectives'])
assert len(objects) == 1
obj = objects[0]
assert obj.get('maxOrMin') == 'min' and F(obj.get('weight', '1')) == 1
assert F(obj.get('constant', '0')) == 0 and len(obj) == 0
assert int(obj.get('numberOfObjCoef')) == 0

linear = {local(e): e for e in sections['linearConstraintCoefficients']}
assert set(linear) == {'start', 'colIdx', 'value'}  # row-major sparse matrix
start = expand(linear['start'], int)
columns = expand(linear['colIdx'], int)
values = expand(linear['value'], F)
assert len(columns) == len(values) == 3 * T == int(sections['linearConstraintCoefficients'].get('numberOfValues'))
assert start == list(range(0, 3 * T + 1, 3))
matrix = []
for t in range(T):
    entries = dict(zip(columns[start[t]:start[t + 1]], values[start[t]:start[t + 1]]))
    assert len(entries) == 3
    matrix.append(entries)

objective_q = {}
row_q = [{} for _ in rows]
terms = list(sections['quadraticCoefficients'])
assert len(terms) == int(sections['quadraticCoefficients'].get('numberOfQuadraticTerms')) == 3 * T
for term in terms:
    assert local(term) == 'qTerm'
    row, i, j = (int(term.get(k)) for k in ('idx', 'idxOne', 'idxTwo'))
    assert i == j and 0 <= i < n
    target = objective_q if row == -1 else row_q[row]
    assert i not in target
    target[i] = F(term.get('coef'))
h = objective_q[0]
assert h == F('2e-5') == F(1, 50000)
assert objective_q == {j: h for j in range(n - 1)}
for t in range(T):
    assert matrix[t] == {t: -h, T + t: F(1), T + t + 1: F(-1)}
    assert row_q[t] == {T + t: 4 * h}
print('OSIL: all variables, bounds, objective terms and rows match the theorem', flush=True)

point = {}
with gzip.open(WORK / 'dtoc5_point.txt.gz', 'rt') as stream:
    for line in stream:
        if not line.strip() or line.startswith('#'):
            continue
        name, decimal = line.split()
        assert name not in point
        point[name] = F(decimal)
assert set(point) == {v.get('name') for v in variables}
x = [point[v.get('name')] for v in variables]
assert all(x[j] == value for j, value in fixed.items())
for t in range(T):
    residual = sum(a * x[j] for j, a in matrix[t].items())
    residual += sum(a * x[j] ** 2 for j, a in row_q[t].items())
    assert residual == 0, (t, residual)
primal = sum(a * x[j] ** 2 for j, a in objective_q.items())
assert primal == F((WORK / 'objective_reference.txt').read_text().strip())
(WORK / 'primal_exact.txt').write_text(str(primal) + '\n')
print('Point: every decimal is rational; all 49999 residuals are exactly zero', flush=True)

# c_t = minus OSIL row. Assemble L = f - sum(lambda_t * OSIL_row_t)
# directly from the parsed model, rather than entering the dossier's formula.
lam = [-2 * x[t] for t in range(T)]
unmodified_last = lam[-1]
lam[-1] = F(0)
assert all(l <= 0 for l in lam)
a = [objective_q.get(j, F(0)) for j in range(n)]
b = [F(0) for _ in variables]
for t in range(T):
    for j, value in matrix[t].items():
        b[j] -= lam[t] * value
    for j, value in row_q[t].items():
        a[j] -= lam[t] * value
constant = sum(a[j] * value ** 2 + b[j] * value for j, value in fixed.items())
assert constant == h * (1 - 4 * lam[0]) - lam[0]
assert a[-1] == b[-1] == 0
assert all(a[j] > 0 for j in range(n - 1))
print('Lagrangian: diagonal Hessian positive on every unfixed nonterminal coordinate; terminal coefficients zero', flush=True)

# GMP mpq interface. GMP is single-threaded. Use a balanced sum to keep exact
# rational addition practical; no stage division is rounded in this computation.
class Z(C.Structure):
    _fields_ = [('alloc', C.c_int), ('size', C.c_int), ('limbs', C.POINTER(C.c_ulong))]
class Q(C.Structure):
    _fields_ = [('num', Z), ('den', Z)]
gmp = C.CDLL(C.util.find_library('gmp'))
def bind(name, args, result=None):
    fn = getattr(gmp, '__gmp' + name)
    fn.argtypes, fn.restype = args, result
    return fn
qi = bind('q_init', [C.POINTER(Q)])
qc = bind('q_clear', [C.POINTER(Q)])
qs = bind('q_set_str', [C.POINTER(Q), C.c_char_p, C.c_int], C.c_int)
qcan = bind('q_canonicalize', [C.POINTER(Q)])
qa = bind('q_add', [C.POINTER(Q)] * 3)
qsub = bind('q_sub', [C.POINTER(Q)] * 3)
qmul = bind('q_mul', [C.POINTER(Q)] * 3)
qcmp = bind('q_cmp', [C.POINTER(Q)] * 2, C.c_int)
qstr = bind('q_get_str', [C.c_void_p, C.c_int, C.POINTER(Q)], C.c_void_p)
zi = bind('z_init', [C.POINTER(Z)])
zc = bind('z_clear', [C.POINTER(Z)])
zsize = bind('z_sizeinbase', [C.POINTER(Z), C.c_int], C.c_size_t)
zfloor = bind('z_fdiv_q', [C.POINTER(Z)] * 3)
zstr = bind('z_get_str', [C.c_void_p, C.c_int, C.POINTER(Z)], C.c_void_p)

class Rational:
    def __init__(self, value=F(0)):
        self.q = Q()
        qi(C.byref(self.q))
        self.live = True
        assert qs(C.byref(self.q), str(value).encode(), 10) == 0
        qcan(C.byref(self.q))
    def clear(self):
        if self.live:
            qc(C.byref(self.q))
            self.live = False
    def __del__(self):
        self.clear()
    def add(self, other):
        qa(C.byref(self.q), C.byref(self.q), C.byref(other.q))
    def subtract(self, other):
        qsub(C.byref(self.q), C.byref(self.q), C.byref(other.q))
    def compare(self, other):
        return qcmp(C.byref(self.q), C.byref(other.q))
    def text(self):
        length = zsize(C.byref(self.q.num), 10) + zsize(C.byref(self.q.den), 10) + 5
        buffer = C.create_string_buffer(length)
        qstr(buffer, 10, C.byref(self.q))
        return buffer.value.decode()
    def floor_scaled(self, places):
        scale, product = Rational(F(10 ** places)), Rational()
        qmul(C.byref(product.q), C.byref(self.q), C.byref(scale.q))
        z = Z()
        zi(C.byref(z))
        zfloor(C.byref(z), C.byref(product.q.num), C.byref(product.q.den))
        buffer = C.create_string_buffer(zsize(C.byref(z), 10) + 3)
        zstr(buffer, 10, C.byref(z))
        value = int(buffer.value)
        zc(C.byref(z))
        return value

def balanced_sum(items):
    level = [Rational(v) for v in items]
    while len(level) > 1:
        following = []
        for i in range(0, len(level), 2):
            left = level[i]
            if i + 1 < len(level):
                left.add(level[i + 1])
                level[i + 1].clear()
            following.append(left)
        level = following
    return level[0] if level else Rational()

def decimal(integer, places):
    sign = '-' if integer < 0 else ''
    digits = str(abs(integer)).zfill(places + 1)
    return sign + digits[:-places] + '.' + digits[-places:]

division_terms = []
residual_terms = []
polynomial = constant
for j in range(n - 1):
    if j in fixed:
        continue
    minimum_loss = b[j] ** 2 / (4 * a[j])
    square_loss = (2 * a[j] * x[j] + b[j]) ** 2 / (4 * a[j])
    if j < T:  # all control minima have a common small rational denominator
        polynomial -= minimum_loss
    else:
        division_terms.append(minimum_loss)
    residual_terms.append(square_loss)
assert polynomial == constant - h * sum(l * l for l in lam) / 4
assert len(division_terms) == T - 1
print('Summing the full rational dual (balanced GMP additions)', flush=True)
dual = Rational(polynomial)
dual.subtract(balanced_sum(division_terms))
gap = Rational(primal)
gap.subtract(dual)
assert gap.compare(Rational()) > 0
print('Checking exact equality with the independently assembled sum of squares', flush=True)
squares = balanced_sum(residual_terms)
assert squares.compare(gap) == 0
assert dual.compare(Rational(F('5.38967211918114046742396649913627186883131268'))) > 0
assert gap.compare(Rational(F('7.21e-43'))) < 0
assert gap.compare(Rational(F('7.2e-43'))) > 0

# Independently reproduce the dossier's directed dyadic evaluation for comparison.
grid = 1 << 256
ceil_sum = sum(-((-v.numerator * grid) // v.denominator) for v in division_terms)
dossier_lower = polynomial - F(ceil_sum, grid)
assert dual.compare(Rational(dossier_lower)) >= 0
excess = Rational()
excess.add(dual)
excess.subtract(Rational(dossier_lower))
assert excess.compare(Rational(F(T - 1, grid))) < 0
(WORK / 'dossier_lower_exact.txt').write_text(str(dossier_lower) + '\n')

displays = {}
for label, value in [('dual', dual), ('primal', Rational(primal)), ('gap', gap),
                     ('dossier_lower', Rational(dossier_lower)), ('dual_minus_dossier', excess)]:
    places = 100
    lower = value.floor_scaled(places)
    upper = lower + (value.compare(Rational(F(lower, 10 ** places))) != 0)
    displays[label] = {'down_100': decimal(lower, places), 'up_100': decimal(upper, places)}
    print(label, displays[label], flush=True)
    if label in ('dual', 'gap'):
        (WORK / (label + '_exact.txt')).write_text(value.text() + '\n')
safe = {}
for label, value, direction in [('dual', dual, 'down'), ('primal', Rational(primal), 'up')]:
    floor = value.floor_scaled(44)
    safe[label + '_' + direction + '_44'] = decimal(floor + (direction == 'up'), 44)
safe['exact_certificate_gap_up'] = '7.21e-43'
safe['displayed_interval_width'] = str(F(safe['primal_up_44']) - F(safe['dual_down_44']))
report = {
    'hashes': hashes, 'affinity': sorted(os.sched_getaffinity(0)),
    'variables': n, 'rows': T, 'linear_entries': len(values), 'quadratic_terms': len(terms),
    'h': str(h), 'state_square_coefficient': str(4 * h),
    'fixed_variable': {variables[j].get('name'): str(v) for j, v in fixed.items()},
    'unmodified_last_multiplier': str(unmodified_last), 'last_control': str(x[T - 1]),
    'smallest_nonterminal_control': str(min(x[:T - 1])),
    'min_lambda': str(min(lam)), 'max_lambda': str(max(lam)),
    'exact_rows_verified': T, 'primal_matches_saved_rational': True,
    'exact_dual_equals_primal_minus_exact_squares': True,
    'dual_numerator_bits': int(zsize(C.byref(dual.q.num), 2)),
    'dual_denominator_bits': int(zsize(C.byref(dual.q.den), 2)),
    'decimal_enclosures': displays, 'safe_displays': safe,
    'elapsed_seconds': time.monotonic() - started,
}
(WORK / 'result.json').write_text(json.dumps(report, indent=2) + '\n')
print('SAFE', safe, flush=True)
print('PASS; seconds', report['elapsed_seconds'], flush=True)
