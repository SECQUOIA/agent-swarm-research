"""Independent exact continuous three-block optimization; no author code imported.

On each switch-time cell the active block-end errors are affine in (u,v,E).
Enumerate every vertex of every such epigraph using integer determinants.
Zero-length blocks and all 27 words cover every schedule with <=3 blocks.
"""
from fractions import Fraction as F
from itertools import combinations, product
from math import lcm
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[3]
SNAP = ROOT / 'process/snapshots/stage02-round02'
manifest = json.loads((SNAP / 'snapshot-manifest.json').read_text())
assert len(manifest) == 40
assert all(hashlib.sha256((SNAP / p).read_bytes()).hexdigest() == h
           for p, h in manifest.items())
print('All 40 immutable snapshot hashes verified.')

raw = [(0,0,0,0),(146,98,48,0),(194,110,48,36),(256,110,78,68),
       (408,224,116,68),(516,224,178,114),(580,240,178,162),(971,417,309,245)]
knots = [tuple(F(x,146) for x in row) for row in raw]
L = F(57,8)
knots.append((L, *(knots[-1][i] + (L-knots[-1][0])/3 for i in (1,2,3))))
affine = []
for left,right in zip(knots, knots[1:]):
    slopes = [(right[i]-left[i])/(right[0]-left[0]) for i in (1,2,3)]
    assert sum(slopes) == 1 and all(0 <= x <= F(3,4) for x in slopes)
    affine.append([(a,left[i+1]-a*left[0]) for i,a in enumerate(slopes)])

def allocation(i,t):
    for j in range(len(affine)):
        if knots[j][0] <= t <= knots[j+1][0]:
            a,b = affine[j][i]
            return a*t+b
    raise AssertionError(t)

def reach(i,b,E):
    target = b+E
    if L-allocation(i,L) <= target:
        return L
    for j in range(len(affine)):
        a,c = affine[j][i]
        root = (target+c)/(1-a)
        if knots[j][0] <= root <= knots[j+1][0]:
            return root
    raise AssertionError((i,b,E))

delta = F(277,18396)
opt = 1+delta
R = [reach(i,0,1) for i in range(3)]
M = [max(reach(q,reach(p,0,1),1) for p,q in product(range(3),repeat=2)
         if p != q and i not in (p,q)) for i in range(3)]
assert R == [F(128,73),F(97,73),F(1)]
assert M == [F(204,73),F(258,73),F(290,73)]
for w in product(range(3), repeat=3):
    if len(set(w)) == 3:
        t=0
        for i in w: t=reach(i,t,1)
        assert t == F(971,146)
assert L-F(971,146) == F(63,2)*delta
u,v=R[0]+4*delta,M[1]+20*delta
assert (u,v)==(F(8341,4599),F(17639,4599))
assert (u-allocation(0,u),v-u-allocation(2,v),L-v-allocation(1,L)) == (opt,)*3
m=[allocation(i,L) for i in range(3)]
assert m == [F(5281,1752),F(3985,1752),F(3217,1752)]
assert m[0]>2*opt and m[1]>2*opt
assert M[2]+20*delta < L
assert [L-m[p]-opt-(M[2]-R[p]+16*delta) for p in (0,1)] == [F(2923,4599),F(4372,4599)]
assert opt/L == F(37346,262143) > F(8,57)
print('Slopes, six initial reaches, suffix identity, witness, support and middle-service arithmetic verified.')

def row(*xs):
    xs=list(map(F,xs)); scale=lcm(*(x.denominator for x in xs))
    return tuple(int(x*scale) for x in xs)

def det(a,b,c):
    return a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0])

def minimum(rows):
    best=None; witness=None
    for a,b,c in combinations(rows,3):
        d=det(a,b,c)
        if not d: continue
        nums=[det((a[3],a[1],a[2]),(b[3],b[1],b[2]),(c[3],c[1],c[2])),
              det((a[0],a[3],a[2]),(b[0],b[3],b[2]),(c[0],c[3],c[2])),
              det((a[0],a[1],a[3]),(b[0],b[1],b[3]),(c[0],c[1],c[3]))]
        if d<0: d=-d; nums=[-x for x in nums]
        if best is not None and nums[2]*best.denominator >= best.numerator*d: continue
        if all(sum(a*x for a,x in zip(r,nums)) <= r[3]*d for r in rows):
            best=F(nums[2],d); witness=[F(x,d) for x in nums]
    assert best is not None
    return best,witness

word_results={}
cells=0
for p,q,r in product(range(3),repeat=3):
    best=None; witness=None
    for j in range(len(affine)):
        for k in range(j,len(affine)):
            ap,bp=affine[j][p]; aq,bq=affine[k][q]
            rows=[row(-1,0,0,-knots[j][0]),row(1,0,0,knots[j+1][0]),
                  row(0,-1,0,-knots[k][0]),row(0,1,0,knots[k+1][0]),
                  row(1,-1,0,0),row(0,0,-1,0),
                  row(1-ap,0,-1,bp),
                  row(int(p==q)-1,1-aq,-1,bq),
                  row(int(p==r)-int(q==r),int(q==r)-1,-1,m[r]-L)]
            e,x=minimum(rows); cells+=1
            if best is None or e<best: best,witness=e,x
    word=''.join(map(str,(p,q,r)))
    word_results[word]={'error':str(best),'u':str(witness[0]),'v':str(witness[1])}
    print(word, word_results[word], flush=True)
assert cells==27*36
assert min(F(x['error']) for x in word_results.values()) == opt
assert F(word_results['021']['error']) == opt
assert all(F(x['error'])>opt for w,x in word_results.items() if len(set(w))<3)
print('Exact exhaustive LP result: global optimum',opt,'over',cells,'word/cell polyhedra.')
(Path(__file__).parent/'exact_word_optima.json').write_text(json.dumps(word_results,indent=2)+'\n')
