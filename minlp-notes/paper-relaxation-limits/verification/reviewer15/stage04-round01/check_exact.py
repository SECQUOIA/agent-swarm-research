"""Independent finite exact checks; no manuscript/author checker imports."""
from fractions import Fraction as Q
from itertools import combinations
from math import comb, prod
from pathlib import Path
import json


def fall(t, a):
    return prod((t - i for i in range(a)), start=Q(1))


def moment(s, t, a):
    return fall(t, a) / fall(s, a)


def masks(n, degree):
    return [sum(1 << i for i in c) for d in range(degree + 1)
            for c in combinations(range(n), d)]


def exact_psd(matrix):
    """Exact symmetric Schur elimination, checking every zero pivot row."""
    a = [row[:] for row in matrix]
    positive = 0
    for k in range(len(a)):
        pivot = a[k][k]
        assert pivot >= 0, (k, pivot)
        if not pivot:
            assert all(a[k][j] == 0 for j in range(k, len(a)))
            continue
        positive += 1
        for i in range(k + 1, len(a)):
            for j in range(i, len(a)):
                a[i][j] -= a[i][k] * a[k][j] / pivot
                a[j][i] = a[i][j]
    return positive


report = {"arithmetic": "exact fractions", "checks": {}}
gram = indicators = balances = 0
for r in range(1, 6):
    # Integer endpoints (including zero coefficients) and nearby nonintegers.
    s = 4 * r
    for t in (Q(2 * r - 1), Q(4 * r - 1, 2), Q(2 * r + 1)):
        assert t >= 2 * r - 1 and s - t >= 2 * r - 1
        for d in range(1, r + 1):
            for overlap in range(d + 1):
                actual = sum(comb(overlap, j) * fall(t, 2*d-j)
                             * fall(s-t, j) / fall(s, 2*d)
                             for j in range(overlap + 1))
                assert actual == moment(s, t, 2*d-overlap)
                gram += 1
        for a in range(2*r + 1):
            for b in range(2*r + 1 - a):
                for c in range(2*r + 1 - a - b):
                    direct = sum((-1)**j * comb(b, j)
                                 * moment(s, t, a+c+j)
                                 for j in range(b+1))
                    formula = fall(t, a+c)*fall(s-t, b)/fall(s, a+b+c)
                    assert direct == formula
                    if c == 0:
                        assert direct >= 0
                    indicators += 1
        for a in range(2*r):
            assert a*moment(s, t, a)+(s-a)*moment(s, t, a+1) == t*moment(s, t, a)
            balances += 1
report["checks"].update(gram_entries=gram, indicator_identities=indicators,
                        balance_recurrences=balances)

tensor_records = []
for sizes, totals, r in [([3, 3, 3], [Q(3, 2)]*3, 1),
                          ([7, 7], [Q(7, 2)]*2, 2)]:
    n = sum(sizes)
    def evaluate(mask):
        value = Q(1)
        offset = 0
        for s, t in zip(sizes, totals):
            value *= moment(s, t, ((mask >> offset) & ((1 << s)-1)).bit_count())
            offset += s
        return value
    basis = masks(n, r)
    matrix = [[evaluate(a | b) for b in basis] for a in basis]
    rank = exact_psd(matrix)
    entry = {"sizes": sizes, "order": r, "matrix_dimension": len(basis),
             "positive_pivots": rank}
    if r == 2:
        # A lower slack in one block and upper slack in another; all global
        # affine squares, including linear combinations spanning both blocks.
        basis = masks(n, 1)
        u, v = 1, 1 << sizes[0]
        local = [[evaluate(a | b | u)-evaluate(a | b | u | v)
                  for b in basis] for a in basis]
        entry["cross_localizer_dimension"] = len(basis)
        entry["cross_localizer_positive_pivots"] = exact_psd(local)
    tensor_records.append(entry)
report["checks"]["tensor_matrices"] = tensor_records

# Objective-agreement restriction is substantive: a degree-one penalty
# objective plus any available global Boolean identity has identical value.
# The computation above already checks all squares after arbitrary affine
# substitutions, since any such square has a coefficient vector in its basis.
tau = Q(1, 4)-Q(1, 32)*(Q(5, 2)+Q(1, 4))-Q(1, 32)
assert tau == Q(17, 128) and Q(2)*tau/Q(6) == Q(17, 384)
report["checks"]["relative_exponent_per_coordinate"] = str(Q(2)*tau/Q(6))
report["limit"] = "Finite exact matrix and identity checks supplement the general proof; they do not establish universal positivity or graph-lift validity."
Path(__file__).with_suffix('.json').write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps(report, indent=2))
