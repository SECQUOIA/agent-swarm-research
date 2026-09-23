"""Independent exact quadratic-value enumeration; no cut-mask implementation."""
from collections import Counter
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path
import json
import runpy

HERE = Path(__file__).resolve().parent
PAPER = HERE.parents[2]
FROZEN = PAPER / 'process/snapshots/stage01-round02'


def enumerate_ranges(n):
    edges = list(combinations(range(n), 2))
    free = [edge for edge in edges if 0 not in edge]
    signs = [(1,) + s for s in product((-1, 1), repeat=n-1)]
    characters = [[s[i] * s[j] for s in signs] for i, j in free]
    values = [sum(s[i] * s[j] for i, j in edges) for s in signs]
    histogram = Counter()
    old_gray = 0
    for k in range(1 << len(free)):
        gray = k ^ (k >> 1)
        if k:
            changed = gray ^ old_gray
            edge_index = changed.bit_length() - 1
            delta = -2 if gray & changed else 2
            values = [v + delta * c for v, c in zip(values, characters[edge_index])]
        span = max(values) - min(values)
        assert span % 2 == 0
        histogram[span // 2] += 1
        old_gray = gray
    assert sum(histogram.values()) == 1 << len(free)
    return dict(sorted(histogram.items()))


def face_extrema(n, negative, face):
    edges = list(combinations(face, 2))
    values = []
    for assignment in product((-1, 1), repeat=len(face)):
        s = dict(zip(face, assignment))
        values.append(sum((-1 if (i, j) in negative else 1) * s[i] * s[j]
                          for i, j in edges))
    return min(values), max(values)


def witness(n, negative):
    lo, hi = face_extrema(n, negative, tuple(range(n)))
    best = Fraction(0)
    for size in range(2, n+1):
        for face in combinations(range(n), size):
            low, high = face_extrema(n, negative, face)
            best = max(best, Fraction(size * (size-1), high-low))
    return {'min_Q': lo, 'max_Q': hi,
            'center': str(Fraction(n*(n-1), hi-lo)), 'all_faces': str(best)}


def main():
    histograms = {n: enumerate_ranges(n) for n in range(2, 8)}
    assert [min(h) for h in histograms.values()] == [1, 2, 4, 4, 5, 8]
    negatives = {3: [], 4: [], 5: [(1,2),(1,4),(2,3)],
                 6: [(1,4),(1,5),(2,3),(2,5),(3,4)],
                 7: [(1,2),(1,3),(1,6),(2,3),(2,5),(3,4)]}
    witnesses = {n: witness(n, neg) for n, neg in negatives.items()}
    assert [(w['min_Q'], w['max_Q']) for w in witnesses.values()] == [(-1,3),(-2,6),(-4,4),(-5,5),(-7,9)]
    extended = witness(7, negatives[6])
    assert extended == {'min_Q': -9, 'max_Q': 11, 'center': '21/10', 'all_faces': '3'}
    appendix = (FROZEN / 'sections/appendix-finite-signings.tex').read_text()
    program = appendix.split('\\begin{verbatim}', 1)[1].split('\\end{verbatim}', 1)[0]
    (HERE / 'printed_program.py').write_text(program)
    printed = runpy.run_path(str(HERE / 'printed_program.py'))['result']
    report = {'method': 'Exact integer Gray-code enumeration of all normalized quadratic forms',
              'histograms': histograms, 'witnesses': witnesses, 'extended_K6': extended,
              'printed_program_result': printed}
    (HERE / 'results.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
