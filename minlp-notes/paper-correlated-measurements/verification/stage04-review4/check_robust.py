"""Independent finite-scenario checks; no manuscript or historical imports."""
from fractions import Fraction as F
import json
import random
from pathlib import Path
import sympy as sp

rng = random.Random(91404)
a = F(3, 4)
C = [(F(3,4), F(1,10)), (F(1,10), F(1)),
     (F(3,8), F(3,8)), (F(9,32), F(3,8))]
full = C + [(F(1,2), F(1,2)), (F(1), F(1,10))]
ds = [max(x[s] for x in C) for s in range(2)]
Ds = [max(x[s] for x in full) for s in range(2)]
score = lambda x, d: min(x[s]/d[s] for s in range(len(d)))
assert ds == [F(3,4), F(1)] and Ds == [F(1), F(1)]
assert score(C[2], ds) == score(C[3], ds) == max(score(x, ds) for x in C)
assert score(C[3], Ds)/max(score(x, Ds) for x in full) == a*a
for x in full:
    assert any(all(a*x[s] <= y[s] <= F(5,4)*x[s] for s in range(2)) for y in C)

# Full matrix, multiple-scenario covers: retain a-scaled target matrices.
# Rational determinant ratios avoid all logarithm and root comparisons.
cases = 0
for p in (1, 2, 3):
    for q in (1, 2, 3):
        for repeat in range(12):
            aa = sp.Rational(rng.randint(5, 9), 10)
            targets = []
            for _ in range(7):
                models = []
                for s in range(q):
                    B = sp.Matrix(p, p, [rng.randint(-3, 3) for _ in range(p*p)])
                    models.append(B*B.T + sp.eye(p))
                targets.append(models)
            cover = [[aa*M for M in row] for row in targets]
            family = targets + cover
            dets = [[M.det() for M in row] for row in family]
            cdets = dets[7:]
            true_d = [max(row[s] for row in dets) for s in range(q)]
            cover_d = [max(row[s] for row in cdets) for s in range(q)]
            for s in range(q):
                assert aa**p*true_d[s] <= cover_d[s] <= true_d[s]
            true_scores = [min(row[s]/true_d[s] for s in range(q)) for row in dets]
            set_scores = [min(row[s]/cover_d[s] for s in range(q)) for row in cdets]
            best_set = max(set_scores)
            for j, v in enumerate(set_scores):
                assert true_scores[j+7] <= v <= true_scores[j+7]/aa**p
                if v == best_set:
                    assert true_scores[j+7] >= aa**(2*p)*max(true_scores)
            # Invariance under unrelated rational invertible congruences.
            factors = []
            for s in range(q):
                T = sp.eye(p)
                T[0, 0] = s+2
                if p > 1:
                    T[0, 1] = 1
                factors.append(T.det()**2)
                for j, row in enumerate(family):
                    assert (T*row[s]*T.T).det() == factors[s]*dets[j][s]
            scaled_d = [true_d[s]*factors[s] for s in range(q)]
            for j, row in enumerate(dets):
                assert min(row[s]*factors[s]/scaled_d[s] for s in range(q)) == true_scores[j]
            cases += 1

# Exact common-price coefficients from the manuscript witness.
W = F(2,5)
lam = (F(1,2), F(1,2))
increments = [(F(3), F(0)), (F(0), F(3))]
common = max(sum(lam[s]*W*x[s] for s in range(2)) for x in increments)
separate = sum(lam[s]*max(W*x[s] for x in increments) for s in range(2))
assert common == F(3,5) and separate == F(6,5)
assert -1 + W + common == 0

result = {'exact_matrix_cover_and_congruence_cases': cases,
          'sharp_tie_ratio': str(a*a), 'common_support': str(common),
          'separate_support': str(separate), 'status': 'passed',
          'scope': 'Exact algebraic diagnostics, not a proof or runtime benchmark.'}
Path(__file__).with_name('results.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result))
