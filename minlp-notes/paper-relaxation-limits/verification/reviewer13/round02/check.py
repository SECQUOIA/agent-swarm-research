"""Independent exact quadratic-value enumeration; no cut-mask implementation."""
from itertools import combinations, product
from fractions import Fraction
from pathlib import Path
import contextlib
import io
import json
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
snapshot = ROOT / 'process/snapshots/stage01-round02'
rows = []
for n in range(2, 8):
    edges = list(combinations(range(n), 2))
    free = [e for e in edges if e[0] != 0]
    signs = np.array([(1,) + s for s in product((-1, 1), repeat=n-1)], dtype=np.int64)
    features = np.array([signs[:, i] * signs[:, j] for i, j in edges], dtype=np.int64)
    coeff = np.ones((2 ** len(free), len(edges)), dtype=np.int64)
    coeff[:, [edges.index(e) for e in free]] = np.array(list(product((-1, 1), repeat=len(free))), dtype=np.int64)
    values = coeff @ features
    # Each dot product is a sum of at most 21 numbers in {-1,1}; int64 is exact.
    osc = values.max(axis=1) - values.min(axis=1)
    assert (osc % 2 == 0).all()
    ranges = osc // 2
    unique, counts = np.unique(ranges, return_counts=True)
    rows.append({'n': n, 'representatives': len(coeff), 'minimum_R': int(ranges.min()),
                 'M_n': str(Fraction(len(edges), int(ranges.min()))),
                 'histogram': dict(zip(map(str, unique), map(int, counts)))})
assert [r['minimum_R'] for r in rows] == [1, 2, 4, 4, 5, 8]

witnesses = {3: [], 4: [], 5: [(1,2),(1,4),(2,3)],
             6: [(1,4),(1,5),(2,3),(2,5),(3,4)],
             7: [(1,2),(1,3),(1,6),(2,3),(2,5),(3,4)]}
def witness_check(n, negative):
    edges = list(combinations(range(n), 2))
    def extrema(W):
        values = [sum((-1 if (i,j) in negative else 1)*s[i]*s[j]
                      for i,j in edges if i in W and j in W)
                  for z in product((-1,1), repeat=len(W))
                  for s in [dict(zip(W,z))]]
        return min(values), max(values)
    lo, hi = extrema(tuple(range(n)))
    best = Fraction(0)
    for k in range(2, n+1):
        for W in combinations(range(n), k):
            l, h = extrema(W)
            best = max(best, Fraction(k*(k-1), h-l))
    return {'min_Q':lo, 'max_Q':hi, 'center':str(Fraction(n*(n-1), hi-lo)), 'all_faces':str(best)}
checks = {str(n): witness_check(n, negative) for n,negative in witnesses.items()}
assert [(c['min_Q'], c['max_Q']) for c in checks.values()] == [(-1,3),(-2,6),(-4,4),(-5,5),(-7,9)]
extended = witness_check(7, witnesses[6])
assert extended == {'min_Q':-9,'max_Q':11,'center':'21/10','all_faces':'3'}

source = (snapshot / 'sections/appendix-finite-signings.tex').read_text()
printed = source.split('\\begin{verbatim}')[1].split('\\end{verbatim}')[0]
stream = io.StringIO()
with contextlib.redirect_stdout(stream):
    exec(compile(printed, '<printed appendix>', 'exec'), {})
report = {'arithmetic':'exact int64 quadratic sums bounded in absolute value by 21; exact Fraction ratios',
          'enumeration':rows, 'witnesses':checks, 'extended_K6':extended,
          'printed_program_stdout':stream.getvalue()}
Path(__file__).with_name('results.json').write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps(report, indent=2))
