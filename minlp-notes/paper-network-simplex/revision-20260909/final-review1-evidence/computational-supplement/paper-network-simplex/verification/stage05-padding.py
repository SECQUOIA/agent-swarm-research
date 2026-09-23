"""Exact positive-layer padding and unit normalization checks.

Starts from explicit tables, not from an implementation of De Loera--Onn's
universality reduction. That imported theorem is checked against its source;
this script checks the additional table-to-network algebra in the paper.
"""
from fractions import Fraction as F
from pathlib import Path
import json
import random

rng = random.Random(51505)
zero_layer_inputs = 0
for trial in range(60):
    r, c = 1+trial % 3, 1+trial % 4
    table = [[[F(rng.randrange(5)) if k != trial % 4 else F(0)
               for k in range(3)] for j in range(c)] for i in range(r)]
    zero_layer_inputs += int(any(sum(table[i][j][k] for i in range(r) for j in range(c)) == 0
                                 for k in range(3)))
    for row in table: row.append([F(0)]*3)
    table.append([[F(0)]*3 for j in range(c)] + [[F(1)]*3])
    r += 1; c += 1
    U = [[sum(table[i][j]) for j in range(c)] for i in range(r)]
    V = [[sum(table[i][j][k] for j in range(c)) for k in range(3)] for i in range(r)]
    W = [[sum(table[i][j][k] for i in range(r)) for k in range(3)] for j in range(c)]
    D = [sum(row[k] for row in V) for k in range(3)]
    assert all(v > 0 for v in D)
    B = sum(D)
    lam = [value/B for value in D]
    x = [sum(row)/B for row in V] + [value/B for row in U for value in row] + [sum(row)/B for row in W]
    f = [[V[i][k]/B for i in range(r)]
         + [table[i][j][k]/B for i in range(r) for j in range(c)]
         + [W[j][k]/B for j in range(c)] for k in range(3)]
    assert all(0 <= value <= lam[k] for k in range(3) for value in f[k])
    assert [sum(f[k][e] for k in range(3)) for e in range(len(x))] == x
    for k in range(3):
        assert sum(f[k][:r]) == sum(f[k][-c:]) == lam[k]
        for i in range(r):
            assert f[k][i] == sum(f[k][r+i*c+j] for j in range(c))
        for j in range(c):
            assert f[k][-c+j] == sum(f[k][r+i*c+j] for i in range(r))
    # Every arbitrary choice of designated first-layer cells is recovered
    # in the sparse product coordinates, without adding other products.
    designated = [(i, j) for i in range(r-1) for j in range(c-1) if rng.randrange(2)]
    assert [f[0][r+i*c+j]*B for i, j in designated] == [table[i][j][0] for i, j in designated]
    # Third-layer boundary values are forced by aggregate subtraction.
    assert all(x[e]-f[0][e]-f[1][e] == f[2][e] for e in list(range(r))+list(range(r+r*c, len(x))))

out = dict(exact_table_padding_and_normalization_cases=60,
           inputs_with_zero_layer=zero_layer_inputs, status='PASS',
           limitation='Does not implement or computationally reprove transportation universality.')
Path(__file__).with_suffix('.json').write_text(json.dumps(out, indent=2)+'\n')
print(json.dumps(out, indent=2))
