"""Independent exact quadratic-value enumeration, with safe int64 arithmetic."""
from pathlib import Path
from itertools import combinations, product
from fractions import Fraction
from collections import Counter
import contextlib, io, json
import numpy as np
ROOT = Path(__file__).resolve().parents[3]
rows=[]
for n in range(2,8):
    edges=list(combinations(range(n),2))
    spins=np.array([(1,)+s for s in product((-1,1),repeat=n-1)],dtype=np.int64)
    chars=np.array([spins[:,i]*spins[:,j] for i,j in edges],dtype=np.int64)
    hist=Counter()
    for free_signs in product((-1,1),repeat=(n-1)*(n-2)//2):
        coeff=np.array([1]*(n-1)+list(free_signs),dtype=np.int64)
        vals=coeff@chars
        osc=int(vals.max()-vals.min())
        assert osc%2==0
        hist[osc//2]+=1
    minimum=min(hist)
    rows.append({'n':n,'representatives':sum(hist.values()),'min_R':minimum,'M':str(Fraction(len(edges),minimum)),'histogram':dict(sorted(hist.items()))})
assert [r['min_R'] for r in rows]==[1,2,4,4,5,8]
witnesses={3:[],4:[],5:[(1,2),(1,4),(2,3)],6:[(1,4),(1,5),(2,3),(2,5),(3,4)],7:[(1,2),(1,3),(1,6),(2,3),(2,5),(3,4)]}
def check_witness(n,neg):
    values=[]
    best=Fraction(0)
    for k in range(2,n+1):
        for vertices in combinations(range(n),k):
            pairs=list(combinations(vertices,2))
            v=[]
            for spins in product((-1,1),repeat=k):
                s=dict(zip(vertices,spins))
                v.append(sum((-1 if (i,j) in neg else 1)*s[i]*s[j] for i,j in pairs))
            ratio=Fraction(2*len(pairs),max(v)-min(v))
            best=max(best,ratio)
            if k==n: center={'min_Q':min(v),'max_Q':max(v),'ratio':str(ratio)}
    return {'center':center,'max_face':str(best)}
w={str(n):check_witness(n,neg) for n,neg in witnesses.items()}
assert [(w[str(n)]['center']['min_Q'],w[str(n)]['center']['max_Q']) for n in range(3,8)]==[(-1,3),(-2,6),(-4,4),(-5,5),(-7,9)]
extended=check_witness(7,witnesses[6])
assert extended=={'center':{'min_Q':-9,'max_Q':11,'ratio':'21/10'},'max_face':'3'}
tex=(ROOT/'process/snapshots/stage01-round02/sections/appendix-finite-signings.tex').read_text()
code=tex.split('\\begin{verbatim}')[1].split('\\end{verbatim}')[0]
printed=io.StringIO()
with contextlib.redirect_stdout(printed): exec(compile(code,'printed-appendix','exec'),{})
result={'arithmetic':'int64 exact; each Q sum has at most 21 unit terms, no overflow','rows':rows,'witnesses':w,'extended_K6':extended,'printed_appendix_stdout':printed.getvalue().strip()}
Path(__file__).with_name('result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
