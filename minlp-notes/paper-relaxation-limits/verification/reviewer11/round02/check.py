from itertools import combinations, product
from fractions import Fraction
from pathlib import Path
import json
import numpy as np

root = Path(__file__).resolve().parents[3]
rows = []
for n in range(2, 8):
    edges = list(combinations(range(n), 2))
    free = [e for e in edges if 0 not in e]
    s = np.array([(1,) + t for t in product((-1, 1), repeat=n-1)], dtype=np.int64)
    char = np.array([s[:, i]*s[:, j] for i,j in edges], dtype=np.int64)
    best = len(edges)*2+1
    histogram = {}
    for start in range(0, 1 << len(free), 1024):
        masks = np.arange(start, min(start+1024, 1 << len(free)), dtype=np.int64)
        a = np.ones((len(masks), len(edges)), dtype=np.int64)
        for k,e in enumerate(free):
            a[:, edges.index(e)] = 1-2*((masks >> k)&1)
        q = a @ char
        widths = q.max(axis=1)-q.min(axis=1)
        for width in widths.tolist():
            assert width % 2 == 0
            r = width//2
            histogram[r] = histogram.get(r, 0)+1
            best = min(best, r)
    rows.append(dict(n=n, minimum_range=best, ratio=str(Fraction(len(edges),best)), histogram=histogram))
assert [r['minimum_range'] for r in rows] == [1,2,4,4,5,8]
# All matrix summands are +/-1 and there are at most 21; int64 cannot overflow.
witnesses = {3: [], 4: [], 5: [(1,2),(1,4),(2,3)], 6: [(1,4),(1,5),(2,3),(2,5),(3,4)], 7: [(1,2),(1,3),(1,6),(2,3),(2,5),(3,4)]}
def check_witness(n, neg):
    result = {}
    best = Fraction(0)
    for k in range(2,n+1):
        for vertices in combinations(range(n),k):
            es = list(combinations(vertices,2))
            vals = []
            for signs in product((-1,1),repeat=k):
                sd = dict(zip(vertices,signs))
                vals.append(sum((-1 if e in neg else 1)*sd[e[0]]*sd[e[1]] for e in es))
            ratio = Fraction(2*len(es),max(vals)-min(vals))
            best = max(best,ratio)
            if k==n: result.update(min_Q=min(vals),max_Q=max(vals),center_ratio=str(ratio))
    result['max_face_ratio'] = str(best)
    return result
ws = {n:check_witness(n,neg) for n,neg in witnesses.items()}
assert [(ws[n]['min_Q'],ws[n]['max_Q']) for n in range(3,8)] == [(-1,3),(-2,6),(-4,4),(-5,5),(-7,9)]
extended = check_witness(7,witnesses[6])
assert extended == dict(min_Q=-9,max_Q=11,center_ratio='21/10',max_face_ratio='3')
appendix = (root/'process/snapshots/stage01-round02/sections/appendix-finite-signings.tex').read_text()
printed = appendix.split('\\begin{verbatim}')[1].split('\\end{verbatim}')[0]
namespace = {}
exec(compile(printed,'printed_appendix','exec'),namespace)
assert namespace['result'] == [r['minimum_range'] for r in rows]
output = dict(arithmetic='Exact int64 quadratic matrix products (absolute sums at most 21), Python integers and Fraction; no float comparisons',enumeration=rows,witnesses=ws,extended=extended,printed_code_result=namespace['result'])
Path(__file__).with_name('results.json').write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps(dict(ranges=[r['minimum_range'] for r in rows], witnesses=ws,extended=extended),indent=2))
