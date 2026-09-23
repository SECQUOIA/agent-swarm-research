from itertools import combinations, product
from collections import Counter
from fractions import Fraction
from pathlib import Path
import json, re, contextlib, io

base=Path('process/snapshots/stage01-round02')
text=(base/'sections/appendix-finite-signings.tex').read_text()
printed=re.search(r'\\begin\{verbatim\}(.*?)\\end\{verbatim\}',text,re.S).group(1)
buf=io.StringIO()
with contextlib.redirect_stdout(buf):
    exec(printed,{})

# Independent computation: maintain every Q value under Gray-code edge-sign flips.
# No cut masks or cut weights are used. Python integers are exact.
rows=[]
for n in range(2,8):
    edges=list(combinations(range(n),2))
    free=[e for e in edges if 0 not in e]
    states=[(1,)+s for s in product((-1,1),repeat=n-1)]
    chars={e:[s[e[0]]*s[e[1]] for s in states] for e in edges}
    values=[sum(chars[e][k] for e in edges) for k in range(len(states))]
    histogram=Counter()
    old=0
    for k in range(1<<len(free)):
        gray=k^(k>>1)
        if k:
            changed=gray^old
            idx=changed.bit_length()-1
            delta=-2 if gray&changed else 2
            values=[v+delta*c for v,c in zip(values,chars[free[idx]])]
        width=max(values)-min(values)
        assert width%2==0
        histogram[width//2]+=1
        old=gray
    rows.append({'n':n,'count':sum(histogram.values()),'min_range':min(histogram),'histogram':dict(sorted(histogram.items()))})
assert [r['min_range'] for r in rows]==[1,2,4,4,5,8]
negatives={3:[],4:[],5:[(1,2),(1,4),(2,3)],6:[(1,4),(1,5),(2,3),(2,5),(3,4)],7:[(1,2),(1,3),(1,6),(2,3),(2,5),(3,4)]}
def witness(n,neg):
    edges=list(combinations(range(n),2))
    coeff={e:-1 if e in neg else 1 for e in edges}
    extrema={}
    best=Fraction(0)
    for mask in range(1<<n):
        vertices=[i for i in range(n) if mask>>i&1]
        es=[e for e in edges if all(i in vertices for i in e)]
        vals=[]
        for signs in product((-1,1),repeat=len(vertices)):
            s=dict(zip(vertices,signs))
            vals.append(sum(coeff[e]*s[e[0]]*s[e[1]] for e in es))
        lo,hi=min(vals),max(vals)
        ratio=Fraction(2*len(es),hi-lo) if es else Fraction(0)
        best=max(best,ratio)
        extrema[mask]=(lo,hi,str(ratio))
    return {'full':extrema[(1<<n)-1],'max_face':str(best),'old_six_face':extrema.get(63)}
witnesses={n:witness(n,es) for n,es in negatives.items()}
assert [witnesses[n]['full'][:2] for n in range(3,8)]==[(-1,3),(-2,6),(-4,4),(-5,5),(-7,9)]
extended=witness(7,negatives[6])
assert extended['full']==(-9,11,'21/10') and extended['max_face']=='3'
result={'printed_program_stdout':buf.getvalue().strip(),'independent_Q_enumeration':rows,'witnesses':witnesses,'extended_K6':extended}
Path('verification/reviewer03/round02/check.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'printed':result['printed_program_stdout'],'min_ranges':[r['min_range'] for r in rows],'witnesses':witnesses,'extended':extended},indent=2))
