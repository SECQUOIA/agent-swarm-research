"""Independent exact integer Q enumeration and frozen printed-code replay."""
from collections import Counter
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path
import contextlib
import io
import json
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
FROZEN = ROOT / 'process/snapshots/stage01-round02'
WITNESSES = {3: [], 4: [], 5: [(1,2),(1,4),(2,3)],
             6: [(1,4),(1,5),(2,3),(2,5),(3,4)],
             7: [(1,2),(1,3),(1,6),(2,3),(2,5),(3,4)]}

def extrema(n, negative, vertices=None):
    vertices = list(range(n)) if vertices is None else vertices
    edges = list(combinations(vertices,2))
    vals = []
    for signs in product((-1,1), repeat=len(vertices)):
        s = dict(zip(vertices, signs))
        vals.append(sum((-1 if (i,j) in negative else 1)*s[i]*s[j]
                        for i,j in edges))
    return min(vals), max(vals)

rows=[]
for n in range(2,8):
    edges=list(combinations(range(n),2))
    configurations=np.array([(1,)+s for s in product((-1,1),repeat=n-1)],dtype=np.int64)
    chars=np.stack([configurations[:,i]*configurations[:,j] for i,j in edges],axis=0)
    free=[k for k,(i,j) in enumerate(edges) if i>0]
    histogram=Counter()
    for start in range(0,1<<len(free),1024):
        ids=np.arange(start,min(start+1024,1<<len(free)),dtype=np.int64)
        a=np.ones((len(ids),len(edges)),dtype=np.int64)
        a[:,free]=1-2*((ids[:,None]>>np.arange(len(free)))&1)
        q=a@chars
        ranges=q.max(axis=1)-q.min(axis=1)
        assert np.all(ranges%2==0)
        histogram.update(map(int,ranges//2))
    best=min(histogram)
    row={'n':n,'representatives':sum(histogram.values()),'min_cut_range':best,
         'max_center_ratio':str(Fraction(len(edges),best)),
         'cut_range_histogram':dict(sorted(histogram.items()))}
    if n in WITNESSES:
        lo,hi=extrema(n,WITNESSES[n])
        assert (hi-lo)//2==best
        row['displayed_witness_extrema']=[lo,hi]
    rows.append(row)
assert [r['min_cut_range'] for r in rows]==[1,2,4,4,5,8]
assert extrema(7,WITNESSES[6])==(-9,11)
assert extrema(7,WITNESSES[6],list(range(6)))==(-5,5)
source=(FROZEN/'sections/appendix-finite-signings.tex').read_text()
code=source.split(r'\begin{verbatim}')[1].split(r'\end{verbatim}')[0]
stream=io.StringIO()
with contextlib.redirect_stdout(stream):
    exec(compile(code,'frozen-appendix-program','exec'),{})
report={'arithmetic':'Exact int64 matrix products; absolute Q <= 21, no overflow possible. Python integer printed-code replay.',
        'rows':rows,'printed_program_stdout':stream.getvalue(),
        'extended_K6_center_extrema':[-9,11], 'extended_K6_six_vertex_extrema':[-5,5]}
Path(__file__).with_name('check_signings.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
