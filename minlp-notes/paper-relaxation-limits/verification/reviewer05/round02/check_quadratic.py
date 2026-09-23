"""Independent exact quadratic enumeration; no cut-weight masks are used."""
from collections import Counter
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
SNAPSHOT = HERE.parents[2] / 'process/snapshots/stage01-round02'

def enumeration(n, normalize=True):
    edges = list(combinations(range(n), 2))
    variable = [k for k, (i, j) in enumerate(edges) if not normalize or i != 0]
    spins = list(product((-1, 1), repeat=n))  # Include both global reversals.
    characters = [[s[i] * s[j] for s in spins] for i, j in edges]
    values = [sum(c) for c in zip(*characters)]
    hist = Counter()
    previous = 0
    for index in range(1 << len(variable)):
        gray = index ^ (index >> 1)
        if index:
            changed = gray ^ previous
            k = variable[changed.bit_length() - 1]
            delta = -2 if gray & changed else 2
            values = [q + delta*c for q, c in zip(values, characters[k])]
        width = max(values) - min(values)
        assert width % 2 == 0
        hist[width // 2] += 1
        previous = gray
    return hist

def witness(n, negative):
    negative = {tuple(e) for e in negative}
    extrema = {}
    ratios = []
    for count in range(2, n + 1):
        for vertices in combinations(range(n), count):
            edges = list(combinations(vertices, 2))
            vals = []
            for signs in product((-1, 1), repeat=count):
                s = dict(zip(vertices, signs))
                vals.append(sum((-1 if e in negative else 1)*s[e[0]]*s[e[1]] for e in edges))
            ratio = Fraction(2*len(edges), max(vals)-min(vals))
            ratios.append(ratio)
            if count == n:
                extrema = {'min_Q': min(vals), 'max_Q': max(vals), 'center': str(ratio)}
    return dict(extrema, all_faces=str(max(ratios)))

def main():
    output = {'arithmetic': 'unbounded Python integers and Fraction', 'normalized': {}, 'full_signings_crosscheck': {}}
    expected = {2: 1, 3: 2, 4: 4, 5: 4, 6: 5, 7: 8}
    for n in range(2, 8):
        hist = enumeration(n)
        assert min(hist) == expected[n]
        assert sum(hist.values()) == 2**((n-1)*(n-2)//2)
        output['normalized'][n] = {'minimum': min(hist), 'histogram': dict(sorted(hist.items()))}
        if n <= 5:
            full = enumeration(n, False)
            assert full == Counter({r: count * 2**(n-1) for r, count in hist.items()})
            output['full_signings_crosscheck'][n] = sum(full.values())
    examples = {3: [], 4: [], 5: [(1,2),(1,4),(2,3)], 6: [(1,4),(1,5),(2,3),(2,5),(3,4)], 7: [(1,2),(1,3),(1,6),(2,3),(2,5),(3,4)]}
    output['witnesses'] = {n: witness(n, neg) for n, neg in examples.items()}
    output['extended_K6'] = witness(7, examples[6])
    assert output['extended_K6'] == {'min_Q': -9, 'max_Q': 11, 'center': '21/10', 'all_faces': '3'}
    source = (SNAPSHOT/'sections/appendix-finite-signings.tex').read_text()
    printed = source.split('\\begin{verbatim}', 1)[1].split('\\end{verbatim}', 1)[0]
    namespace = {}
    exec(compile(printed, 'frozen-printed-code', 'exec'), namespace)
    output['printed_program'] = namespace['result']
    (HERE/'checks.json').write_text(json.dumps(output, indent=2)+'\n')
    print(json.dumps(output, indent=2))

if __name__ == '__main__':
    main()
