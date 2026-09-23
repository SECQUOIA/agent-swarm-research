"""Independent exact Stage 1 checks. Only writes this directory's result.json."""
from collections import Counter
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
FROZEN = HERE.parents[2] / 'process/snapshots/stage01-round02'

def histogram(n, normalize=True):
    edges = list(combinations(range(n), 2))
    free = [(i,j) for i,j in edges if not normalize or i > 0]
    vertices = [(1,) + tail for tail in product((-1,1), repeat=n-1)]
    characters = [[s[i]*s[j] for s in vertices] for i,j in free]
    values = [sum(s[i]*s[j] for i,j in edges) for s in vertices]
    hist = Counter()
    previous = 0
    for index in range(1 << len(free)):
        gray = index ^ (index >> 1)
        if index:
            bit = (gray ^ previous).bit_length()-1
            change = -2 if gray & (1 << bit) else 2
            values = [q + change*c for q,c in zip(values, characters[bit])]
        assert (max(values)-min(values)) % 2 == 0
        hist[(max(values)-min(values))//2] += 1
        previous = gray
    return dict(sorted(hist.items()))

def witness(n, negative):
    negative = set(map(tuple,negative))
    best = Fraction(0)
    for k in range(2,n+1):
        for face in combinations(range(n), k):
            values=[]
            for signs in product((-1,1), repeat=k):
                s=dict(zip(face,signs))
                values.append(sum((-1 if (i,j) in negative else 1)*s[i]*s[j]
                                  for i,j in combinations(face,2)))
            ratio=Fraction(k*(k-1),max(values)-min(values))
            best=max(best,ratio)
            if k==n:
                center=[min(values),max(values),str(ratio)]
    return {'center':center,'max_face_ratio':str(best)}

manifest=json.loads((FROZEN/'manifest.json').read_text())
for path,digest in manifest.items():
    assert hashlib.sha256((FROZEN/path).read_bytes()).hexdigest()==digest, path
expected=json.loads((FROZEN/'verification/complete_signings.json').read_text())
rows=[]
for original in expected['rows']:
    n=original['n']
    hist=histogram(n)
    assert hist=={int(k):v for k,v in original['cut_range_histogram'].items()}
    row={'n':n,'histogram':hist,'M_n':str(Fraction(n*(n-1)//2,min(hist)))}
    if n<=5:
        full=histogram(n,False)
        assert full=={k:v*(1 << (n-1)) for k,v in hist.items()}
        row['unnormalized_signings_checked']=sum(full.values())
    row['witness']=witness(n,original['negative_edges'])
    assert row['witness']['center'][:2]==[original['witness_check']['center']['min_Q'],original['witness_check']['center']['max_Q']]
    rows.append(row)
extended=witness(7,expected['extended_K6_face_witness']['negative_edges'])
assert extended=={'center':[-9,11,'21/10'],'max_face_ratio':'3'}
printed=re.search(r'\\begin\{verbatim\}\n(.*?)\\end\{verbatim\}',(FROZEN/'sections/appendix-finite-signings.tex').read_text(),re.S).group(1)
namespace={}
exec(compile(printed,'frozen appendix','exec'),namespace)
assert namespace['result']==[1,2,4,4,5,8]

# Independent exact checks on every signed simple graph on four vertices.
# Zero is an absent edge. These are finite regression checks, not proofs
# of the manuscript's universal real-coefficient assertions.
n=4
edges=list(combinations(range(n),2))
graph_count=0
for coeff in product((-1,0,1),repeat=len(edges)):
    a=dict(zip(edges,coeff))
    def entry(i,j):
        return 0 if i==j else a[tuple(sorted((i,j)))]
    vertices=list(product((-1,1),repeat=n))
    values=[sum(a[i,j]*s[i]*s[j] for i,j in edges) for s in vertices]
    R=Fraction(max(values)-min(values),2)
    L=sum(abs(v) for v in coeff)
    subsets=[tuple(i for i in range(n) if mask & (1<<i)) for mask in range(1<<n)]
    rho=max([Fraction(0)]+[Fraction(sum(a[i,j]!=0 for i,j in combinations(S,2)),len(S)) for S in subsets if S])
    beta=max([Fraction(0)]+[Fraction(sum(entry(i,j)!=0 for i in S for j in T),len(S)+len(T)) for S in subsets for T in subsets if S or T])
    assert beta==rho
    polar=0
    for S in subsets:
        T=tuple(i for i in range(n) if i not in S)
        for signs in product((-1,1),repeat=len(T)):
            polar=max(polar,sum(abs(sum(entry(i,j)*s for j,s in zip(T,signs))) for i in S))
    assert R==polar
    assert L*L <= 16*rho*R*R
    delta=max(sum(entry(i,j)!=0 for j in range(n)) for i in range(n))
    assert L*L <= 4*delta*R*R
    # Two-colorability of both requested edge sets as cuts, allowing disconnected support.
    pos_cut=any(all((s[i]!=s[j])==(a[i,j]>0) for i,j in edges if a[i,j]) for s in vertices)
    neg_cut=any(all((s[i]!=s[j])==(a[i,j]<0) for i,j in edges if a[i,j]) for s in vertices)
    assert (R==L)==(pos_cut and neg_cut)
    graph_count+=1
output={'arithmetic':'unbounded Python integers and Fraction; no solver or floating point',
        'manifest_files_checked':len(manifest),'rows':rows,'extended':extended,'printed_result':namespace['result'],
        'signed_graphs_n4_checked':graph_count}
(HERE/'result.json').write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps(output,indent=2))
