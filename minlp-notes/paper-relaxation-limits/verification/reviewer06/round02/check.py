"""Independent exact quadratic enumeration; no cut masks or floating point."""
from collections import Counter
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
FROZEN = HERE.parents[2] / 'process/snapshots/stage01-round02'

def extrema(n, negatives, vertices=None):
    vertices = list(range(n)) if vertices is None else list(vertices)
    if not vertices:
        return 0, 0
    values = [sum((-1 if (i,j) in negatives else 1) * s[i] * s[j]
                  for i,j in combinations(vertices, 2))
              for tail in product((-1,1), repeat=len(vertices)-1)
              for s in [dict(zip(vertices, (1,) + tail))]]
    return min(values), max(values)

def exhaustive(n):
    edges = list(combinations(range(n), 2))
    free = [e for e in edges if 0 not in e]
    vectors = [(1,) + t for t in product((-1,1), repeat=n-1)]
    values = [sum(s[i]*s[j] for i,j in edges) for s in vectors]
    histogram = Counter()
    previous = 0
    for k in range(1 << len(free)):
        gray = k ^ (k >> 1)
        if k:
            bit = (gray ^ previous).bit_length()-1
            i,j = free[bit]
            change = -2 if (gray >> bit) & 1 else 2
            values = [q + change*s[i]*s[j] for q,s in zip(values,vectors)]
        assert (max(values)-min(values)) % 2 == 0
        histogram[(max(values)-min(values))//2] += 1
        previous = gray
    return {'representatives':sum(histogram.values()),
            'minimum_range':min(histogram),
            'M':str(Fraction(len(edges),min(histogram))),
            'histogram':dict(sorted(histogram.items()))}

table = {n: exhaustive(n) for n in range(2,8)}
assert [table[n]['minimum_range'] for n in table] == [1,2,4,4,5,8]
negatives = {3:set(), 4:set(), 5:{(1,2),(1,4),(2,3)},
             6:{(1,4),(1,5),(2,3),(2,5),(3,4)},
             7:{(1,2),(1,3),(1,6),(2,3),(2,5),(3,4)}}
witnesses = {}
for n,negative in list(negatives.items()) + [(7,negatives[6])]:
    lo,hi = extrema(n,negative)
    ratios = []
    for size in range(2,n+1):
        for vertices in combinations(range(n),size):
            l,h = extrema(n,negative,vertices)
            ratios.append(Fraction(size*(size-1),h-l))
    key = str(n) if negative == negatives[n] else 'extended_K6'
    witnesses[key] = {'negative_edges':sorted(negative),'min_Q':lo,'max_Q':hi,
                     'center':str(Fraction(n*(n-1),hi-lo)),
                     'all_faces':str(max(ratios))}
assert [(witnesses[str(n)]['min_Q'],witnesses[str(n)]['max_Q'])
        for n in range(3,8)] == [(-1,3),(-2,6),(-4,4),(-5,5),(-7,9)]
assert witnesses['extended_K6']['center'] == '21/10'
assert witnesses['extended_K6']['all_faces'] == '3'
appendix = (FROZEN/'sections/appendix-finite-signings.tex').read_text()
printed = appendix.split('\\begin{verbatim}',1)[1].split('\\end{verbatim}',1)[0]
namespace = {}
exec(printed,namespace)
assert namespace['result'] == [table[n]['minimum_range'] for n in table]
result = {'arithmetic':'exact Python integers and Fraction',
          'enumeration':table,'witnesses':witnesses,'printed_result':namespace['result']}
(HERE/'checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
