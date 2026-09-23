"""Independent exact finite checks; no solver or floating point is used."""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import json


def signing_ranges(n):
    edges = list(combinations(range(n), 2))
    free = list(combinations(range(1, n), 2))
    signs = [(1,) + s for s in product((-1, 1), repeat=n-1)]
    # Update Q directly in Gray order, independently of the printed cut masks.
    q = [sum(s[i]*s[j] for i, j in edges) for s in signs]
    characters = [[s[i]*s[j] for s in signs] for i, j in free]
    histogram = Counter()
    previous = 0
    for k in range(1 << len(free)):
        gray = k ^ (k >> 1)
        if k:
            changed = gray ^ previous
            j = changed.bit_length()-1
            delta = -2 if gray & changed else 2
            q = [value + delta*c for value, c in zip(q, characters[j])]
        osc = max(q)-min(q)
        assert osc % 2 == 0
        histogram[osc//2] += 1
        previous = gray
    return dict(sorted(histogram.items()))


def laws():
    checked = 0
    for n in range(1, 5):
        for p in product([F(i, 4) for i in range(5)], repeat=n):
            # One shared threshold attains every upper monomial envelope.
            cuts = sorted({F(0), F(1), *p})
            atoms = [((b-a), tuple(int((a+b)/2 < x) for x in p))
                     for a, b in zip(cuts, cuts[1:])]
            assert sum(w for w, _ in atoms) == 1
            for i in range(n):
                assert sum(w*x[i] for w, x in atoms) == p[i]
            for r in range(1, n+1):
                for e in combinations(range(n), r):
                    assert sum(w for w, x in atoms if all(x[i] for i in e)) == min(p[i] for i in e)
            # The circle construction handles one prescribed full support.
            start = F(0)
            intervals = []
            endpoints = {F(0), F(1)}
            for x in p:
                length = 1-x
                intervals.append((start % 1, length))
                endpoints.update((start % 1, (start+length) % 1))
                start += length
            cuts = sorted(endpoints)
            atoms = [(b-a, tuple(int(((a+b)/2-u) % 1 >= length)
                                 for u, length in intervals))
                     for a, b in zip(cuts, cuts[1:])]
            assert sum(w for w, _ in atoms) == 1
            for i in range(n):
                assert sum(w*x[i] for w, x in atoms) == p[i]
            assert sum(w for w, x in atoms if all(x)) == max(F(0), sum(p)-n+1)
            checked += 1
    return checked


def extrema(n, negative, vertices=None):
    vertices = tuple(range(n)) if vertices is None else tuple(vertices)
    edges = list(combinations(vertices, 2))
    vals = []
    for s in product((-1, 1), repeat=len(vertices)):
        assignment = dict(zip(vertices, s))
        vals.append(sum((-1 if (i,j) in negative else 1)*assignment[i]*assignment[j]
                        for i,j in edges))
    return min(vals), max(vals)


histograms = {n: signing_ranges(n) for n in range(2, 8)}
assert [min(h) for h in histograms.values()] == [1, 2, 4, 4, 5, 8]
witnesses = {3: [], 4: [], 5: [(1,2),(1,4),(2,3)],
             6: [(1,4),(1,5),(2,3),(2,5),(3,4)],
             7: [(1,2),(1,3),(1,6),(2,3),(2,5),(3,4)]}
extreme_table = {n: extrema(n, neg) for n, neg in witnesses.items()}
assert list(extreme_table.values()) == [(-1,3),(-2,6),(-4,4),(-5,5),(-7,9)]
extended = extrema(7, witnesses[6])
assert extended == (-9,11)
face_best = F(0)
for r in range(2, 8):
    for subset in combinations(range(7), r):
        lo, hi = extrema(7, witnesses[6], subset)
        face_best = max(face_best, F(r*(r-1), hi-lo))
assert face_best == 3
result = {'arithmetic': 'exact integers and fractions',
          'laws_checked': laws(), 'histograms': histograms,
          'witness_extrema': extreme_table, 'extended_extrema': extended,
          'extended_best_face_ratio': str(face_best)}
Path(__file__).with_name('results.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2))
