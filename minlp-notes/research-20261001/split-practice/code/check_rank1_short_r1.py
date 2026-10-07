"""Exact affine LLL check of short maximizers at fractional rank-1 roots.

The first-column neighbour is on the 1e-6 grid. This check uses the same
integer embedding as review r1, with the stream's Fraction LLL.
"""
import json
import math
from fractions import Fraction as F
from pathlib import Path

import numpy as np

from lattice import lll_rows_exact, q_exact

ROOT = Path(__file__).resolve().parents[1]
records = [json.loads(line) for k in range(3)
           for line in (ROOT / f'logs/sep_run2_s{k}.jsonl').read_text().splitlines()]
count = 0
with open(ROOT / 'logs/rank1_short_r1.jsonl', 'w') as out:
    for d in records:
        if d['rank']['1e-05'] != 1 or not d['file'].endswith('root.npz'):
            continue
        file = d['file']
        n = int(file.split('_n')[1].split('_')[0])
        Y = np.load(ROOT / f'data/points_BT{n}' / file)['Y']
        Y = (Y + Y.T) / 2
        x = [F(round(float(a) * 10**6), 10**6) for a in Y[0, 1:] / Y[0, 0]]
        D = math.lcm(*(a.denominator for a in x))
        if D == 1:
            print(file, 'integral grid neighbour; skipped')
            continue
        p = [D] + [int(a * D) for a in x]
        N, m, penalty = len(p), -(D // 2), 10**12
        rows = [[int(i == j) for j in range(N)] + [penalty * p[i], 0]
                for i in range(N)]
        rows += [[0] * N + [-penalty * m, 1]]
        reduced = lll_rows_exact(rows)
        candidates = [[a * row[-1] for a in row[:N]] for row in reduced
                      if row[N] == 0 and abs(row[-1]) == 1]
        assert candidates
        v = min(candidates, key=lambda a: (max(map(abs, a)), sum(e * e for e in a)))
        assert sum(a * b for a, b in zip(p, v)) == m
        q = F(m * (m + D), D * D)
        qY = q_exact([[F(float(a)) for a in row] for row in Y], v)
        rec = dict(file=file, D=D, v=v, q_exact=str(q), q_at_Y_exact=str(qY),
                   q_at_Y=float(qY), vmax=max(map(abs, v)),
                   support=sum(a != 0 for a in v[1:]),
                   normalized=float(-qY / sum(a * a for a in v[1:])),
                   best_normalized=d['ratio']['ratio'])
        assert q == -F(1, 4) and rec['vmax'] <= 4
        assert -0.25 - 1e-6 <= qY < 0 and abs(float(qY) + 0.25) < 1e-6
        out.write(json.dumps(rec) + '\n'); out.flush()
        print(json.dumps(rec), flush=True)
        count += 1
assert count == 9
print('All 9 fractional rank-1 roots: exact -1/4, coefficients <=4, stored violation within 1e-6 of 1/4')
