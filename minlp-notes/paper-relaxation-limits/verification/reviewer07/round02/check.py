"""Independent exact Gray-code quadratic evaluation; run from any directory."""
from collections import Counter
from contextlib import redirect_stdout
from fractions import Fraction
from io import StringIO
from itertools import combinations, product
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
SNAP = HERE.parents[2] / 'process/snapshots/stage01-round02'


def enumerate_q(n, normalize=True):
    edges = list(combinations(range(n), 2))
    free = [e for e in edges if not normalize or 0 not in e]
    signs = [(1,) + s for s in product((-1, 1), repeat=n-1)]
    chars = [[s[i]*s[j] for s in signs] for i, j in free]
    values = [sum(s[i]*s[j] for i, j in edges) for s in signs]
    hist = Counter()
    previous = 0
    for index in range(1 << len(free)):
        gray = index ^ (index >> 1)
        if index:
            k = (gray ^ previous).bit_length()-1
            old_sign = -1 if previous & (1 << k) else 1
            values = [v - 2*old_sign*c for v, c in zip(values, chars[k])]
        spread = max(values)-min(values)
        assert spread % 2 == 0
        hist[spread//2] += 1
        previous = gray
    return hist


def witness(n, negatives):
    negatives = set(negatives)
    out = []
    for k in range(2, n+1):
        for face in combinations(range(n), k):
            edges = list(combinations(face, 2))
            vals = []
            for signs in product((-1, 1), repeat=k):
                s = dict(zip(face, signs))
                vals.append(sum((-1 if e in negatives else 1)*s[e[0]]*s[e[1]] for e in edges))
            out.append((Fraction(2*len(edges), max(vals)-min(vals)), face, min(vals), max(vals)))
    center = next(r for r in out if len(r[1]) == n)
    best = max(out)
    return {'center_extrema': center[2:], 'center_ratio': str(center[0]),
            'max_face_ratio': str(best[0]), 'max_face': best[1]}


manifest = json.loads((SNAP/'manifest.json').read_text())
assert all(hashlib.sha256((SNAP/p).read_bytes()).hexdigest() == h for p, h in manifest.items())
printed = (SNAP/'sections/appendix-finite-signings.tex').read_text().split('\\begin{verbatim}')[1].split('\\end{verbatim}')[0]
stream = StringIO()
with redirect_stdout(stream):
    exec(printed, {})
saved = json.loads((SNAP/'verification/complete_signings.json').read_text())
rows = []
for n in range(2, 8):
    hist = enumerate_q(n)
    reference = saved['rows'][n-2]
    assert dict(hist) == {int(k):v for k,v in reference['cut_range_histogram'].items()}
    if n <= 5:
        full = enumerate_q(n, False)
        assert full == Counter({k: v*(1 << (n-1)) for k,v in hist.items()})
    rows.append({'n':n,'count':sum(hist.values()),'min_R':min(hist),
                 'histogram':dict(sorted(hist.items()))})
negative = {3:[], 4:[], 5:[(1,2),(1,4),(2,3)],
            6:[(1,4),(1,5),(2,3),(2,5),(3,4)],
            7:[(1,2),(1,3),(1,6),(2,3),(2,5),(3,4)]}
witnesses = {n:witness(n,e) for n,e in negative.items()}
assert [witnesses[n]['center_extrema'] for n in range(3,8)] == [(-1,3),(-2,6),(-4,4),(-5,5),(-7,9)]
extended = witness(7,negative[6])
assert extended['center_ratio'] == '21/10' and extended['max_face_ratio'] == '3'
output = {'arithmetic':'Python unbounded integers and Fraction; no numerical solver',
          'all_snapshot_hashes_match':True, 'printed_output':stream.getvalue().strip(),
          'gray_code_enumeration':rows,'table_witnesses':witnesses,'extended_K6':extended,
          'limits':'Exact finite results only; universal statements checked by proof review.'}
(HERE/'results.json').write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps(output,indent=2))
