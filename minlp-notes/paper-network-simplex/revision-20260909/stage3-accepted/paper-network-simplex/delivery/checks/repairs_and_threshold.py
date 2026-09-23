"""Exact expansion of every exceptional three-label endpoint pattern."""
from collections import Counter
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import sympy as sp


def add(target, source, scale=1):
    for k, v in source.items():
        target[k] += scale*v


def endpoint(i, pattern, upper):
    rhs = {'x'+str(i): 1}
    for j, kind in enumerate(pattern):
        if kind in 'AT':
            rhs[f'u{i}{j}'] = -1
        if kind == 'B':
            rhs[f'v{i}{j}'] = 1
    if upper:
        rhs = {k: -v for k, v in rhs.items()}
        rhs['constant'], rhs['h'] = 1, -1
    return rhs


negative_count = positive_count = 0
for sign in (-1, 1):
    options = []
    for i in range(3):
        valid = []
        for pat in product('ABTU', repeat=3):
            if sign == -1 and {j for j, p in enumerate(pat) if p in 'AT'} == {i}:
                valid.append(pat)
            if sign == 1 and {j for j, p in enumerate(pat) if p == 'B'} == set(range(3))-{i}:
                valid.append(pat)
        options.append(valid)
    for patterns in product(*options):
        poly = Counter()
        for i, pat in enumerate(patterns):
            add(poly, endpoint(i, pat, sign == -1))
        add(poly, {'h': 1, 'y0': -1, 'y1': -1, 'y2': -1}, 1 if sign == -1 else 2)
        assert poly['h'] == 2*sign
        # Try each of the three possible gadget balances, not just the first.
        for i in range(3):
            repaired = poly.copy()
            add(repaired, {'x'+str(i): 1, 'b'+str(i): 1, 'h': 1, 'constant': -1}, -sign)
            assert all(abs(v) <= 1 for k, v in repaired.items()
                       if k[0] in 'xbu vh'.replace(' ', ''))
        if sign == -1:
            negative_count += 1
        else:
            positive_count += 1
assert (negative_count, positive_count) == (512, 27)

# Both printed examples pass the separate McCormick inequalities exactly.
def mc(x, y, z):
    return 0 <= z <= min(x, y) and z >= x+y-1
assert all(mc(F(2,5), F(1,3), 0) for _ in range(3))
assert 2*F(1,2)-3*F(2,5) == -F(1,5)
assert all(mc(F(9,20), F(1,4), F(1,20)) for _ in range(6))
assert 3*F(3,20)+2*(F(1,4)-F(1,2)) == -F(1,20)

# Four-label counterexample: exact local witnesses for the seven-observation
# construction, including nonzero perturbations along its boundary line.
K = sp.Matrix([[1,1,1,0], [1,0,0,1], [0,1,0,1], [0,0,1,1]])
assert K.det() != 0
alpha = sp.Matrix([2,1,1,1])
assert K.T*alpha == sp.ones(4,1)*3
a, c = sp.Rational(1,8), sp.Rational(1,32)
kinv = K.inv()
eps = a/(16*3*(1+max(sum(abs(v) for v in kinv.row(i)) for i in range(4))))
accepted = rejected = 0
for p, q in product(range(-3,4), repeat=2):
    dr, ds = p*eps/4, q*eps/4
    if 2*dr+ds < 0:
        rejected += 1
        continue
    delta, tau = sp.Matrix([dr, ds, 0, 0]), sp.Matrix([0, 2*dr+ds, 0, 0])
    w = sp.ones(4,1)*a+kinv*(-delta+tau)
    assert sum(w) == sp.Rational(1,2)
    f = []
    for i in range(4):
        row = [w[j] if K[i,j] else c for j in range(4)]
        if i == 0:
            row[3] += dr
        if i == 1:
            row[1] += ds
            row[0] -= tau[1]
        assert all(0 <= v <= w[j] <= 2*a for j, v in enumerate(row))
        target = sum(K.row(i))*a+(4-sum(K.row(i)))*c
        assert sum(row) == target
        f.append(row)
    # b entries are w-f and bypass entries are 1/4-w, verifying state bounds.
    assert all(0 <= 2*a-v <= 2*a for v in w)
    assert sum(2*a-v for v in w) == sp.Rational(1,2)
    accepted += 1
out = {'negative_two_patterns': negative_count, 'positive_two_patterns': positive_count,
       'exact_repair_choices': 3*(negative_count+positive_count),
       'four_label_local_witnesses': accepted, 'four_label_necessary_rejections': rejected,
       'printed_example_violations': ['-1/5', '-1/20']}
Path(__file__).with_suffix('.json').write_text(json.dumps(out, indent=2)+'\n')
print(json.dumps(out, indent=2))
