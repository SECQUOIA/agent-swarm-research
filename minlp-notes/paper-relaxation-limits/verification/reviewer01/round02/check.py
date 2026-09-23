"""Independent direct-character finite check; Python standard library only."""
from collections import Counter
from fractions import Fraction
from itertools import combinations, product
import contextlib
import hashlib
import io
import json
from pathlib import Path

PAPER = Path(__file__).resolve().parents[3]
FROZEN = PAPER / 'process/snapshots/stage01-round02'


def extrema(vertices, negative):
    edges = list(combinations(vertices, 2))
    values = []
    for tail in product((-1, 1), repeat=max(0, len(vertices)-1)):
        s = dict(zip(vertices, (1,) + tail))
        values.append(sum((-1 if (i,j) in negative else 1)*s[i]*s[j]
                          for i,j in edges))
    return min(values), max(values)


def check_size(n):
    edges = list(combinations(range(n), 2))
    free = [(i,j) for i,j in edges if i > 0]
    # Direct quadratic sign characters, with a positive root star.
    characters = []
    for tail in product((-1, 1), repeat=n-1):
        s = (1,) + tail
        characters.append((sum(tail), tuple(s[i]*s[j] for i,j in free)))
    histogram = Counter()
    for coefficients in product((-1, 1), repeat=len(free)):
        values = [star + sum(a*c for a,c in zip(coefficients, chars))
                  for star, chars in characters]
        width = max(values)-min(values)
        assert width % 2 == 0
        histogram[width//2] += 1
    return {'n': n, 'count': sum(histogram.values()),
            'min_range': min(histogram), 'histogram': dict(sorted(histogram.items()))}


def main():
    manifest = json.loads((FROZEN/'manifest.json').read_text())
    assert all(hashlib.sha256((FROZEN/p).read_bytes()).hexdigest() == h
               for p,h in manifest.items())
    rows = [check_size(n) for n in range(2,8)]
    assert [r['min_range'] for r in rows] == [1,2,4,4,5,8]
    witness_edges = {3: [],4: [],5: [(1,2),(1,4),(2,3)],
        6: [(1,4),(1,5),(2,3),(2,5),(3,4)],
        7: [(1,2),(1,3),(1,6),(2,3),(2,5),(3,4)]}
    witnesses = {}
    for n, neg in witness_edges.items():
        low, high = extrema(tuple(range(n)), set(neg))
        witnesses[n] = {'min_Q':low, 'max_Q':high,
                        'center_ratio':str(Fraction(n*(n-1), high-low))}
    assert [(w['min_Q'],w['max_Q']) for w in witnesses.values()] == [(-1,3),(-2,6),(-4,4),(-5,5),(-7,9)]
    neg = set(witness_edges[6])
    extended_extrema = extrema(tuple(range(7)), neg)
    best = Fraction(0)
    for k in range(2,8):
        for face in combinations(range(7),k):
            low,high = extrema(face,neg)
            best = max(best,Fraction(k*(k-1),high-low))
    assert extended_extrema == (-9,11) and best == 3
    appendix = (FROZEN/'sections/appendix-finite-signings.tex').read_text()
    code = appendix.split('\\begin{verbatim}',1)[1].split('\\end{verbatim}',1)[0]
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        exec(compile(code,'frozen-appendix','exec'),{})
    report = {'arithmetic':'exact Python integers and Fraction',
              'manifest_verified':True,'enumeration':rows,'witnesses':witnesses,
              'extended_K6':{'extrema':extended_extrema,'max_face_ratio':str(best)},
              'verbatim_program_output':output.getvalue().strip()}
    Path(__file__).with_name('results.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__ == '__main__':
    main()
