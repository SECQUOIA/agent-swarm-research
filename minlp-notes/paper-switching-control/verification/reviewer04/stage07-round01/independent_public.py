"""Independent integer-scaled public-profile audit; imports no paper checker."""
from pathlib import Path
from fractions import Fraction as Q
from itertools import product, combinations
from statistics import median
import hashlib,json

P=Path(__file__).resolve().parent
S=P/'relocated'
D=json.loads((S/'verification/stage06/results.json').read_text())
raw=(P/'public-source.csv').read_bytes()
assert hashlib.sha256(raw).hexdigest()==D['provenance']['sha256']
data=[list(map(Q,line.split())) for line in raw.decode().splitlines()[1:]]
assert len(data)==12001 and data[0][0]==0 and data[-1][0]==12
counts=[]; normmax=Q(0); quantmax=Q(0)
for a,b in zip(data,data[1:]):
    assert b[0]-a[0]==Q(1,1000)
    weights=a[3:]; assert len(weights)==3 and min(weights)>=0
    normalized=[x/sum(weights) for x in weights]
    scaled=[x*10**6 for x in normalized]
    floored=[x.numerator//x.denominator for x in scaled]
    extras=sorted(range(3),key=lambda i:(floored[i]-scaled[i],i))[:10**6-sum(floored)]
    rr=[x+int(i in extras) for i,x in enumerate(floored)]
    assert sum(rr)==10**6 and min(rr)>=0
    normmax=max(normmax,*(abs(x-y) for x,y in zip(weights,normalized)))
    quantmax=max(quantmax,*(abs(Q(x,10**6)-y) for x,y in zip(rr,normalized)))
    counts.append(rr)
assert normmax==Q(D['provenance']['normalization_max'])<Q(4959,10**10)
assert quantmax==Q(D['provenance']['quantization_max'])<Q(1,10**6)
print('PASS fresh CSV hash, normalization and quantization maxima',flush=True)

# Integrated masses in units of 10^-9; cell length is 10^6 units.
C=[[0]*3]
for rr in counts:C.append([a+b for a,b in zip(C[-1],rr)])
T=12*10**9; M=C[-1]
def sample(t):
    """Cumulative allocation at rational time in physical time units."""
    j=min(11999,int(t*1000))
    return [Q(C[j][i],10**9)+(t-Q(j,1000))*Q(counts[j][i],10**6) for i in range(3)]

# Independently scan all cells for affine intersections with t-W input terms.
pairrecords=[]
for p,q in product(range(3),repeat=2):
    if p==q:continue
    roots=[]
    for j,row in enumerate(counts):
        rate=Q(row[p],10**6)
        intercept=Q(C[j][p],10**9)-rate*Q(j,1000)
        t=(12-Q(M[q],10**9)+intercept)/(2-rate)
        if Q(j,1000)<=t<=Q(j+1,1000):roots.append(t)
    assert roots and len(set(roots))==1
    tau=roots[0]; value=Q(0)
    for t in [Q(j,1000) for j in range(12001)]+[tau]:
        aa=sample(t)
        ww=[min(t,tau) if i==p else max(Q(0),t-tau) if i==q else Q(0) for i in range(3)]
        value=max(value,*(abs(a-b) for a,b in zip(aa,ww)))
    saved=next(r for r in D['public_continuous_one']['all_pairs'] if r['p']==p and r['q']==q)
    assert tau==Q(saved['time']) and value==Q(saved['error'])
    pairrecords.append((value,tau,p,q))
best=min(pairrecords)
assert best[:2]==(Q(4721469,2500000),)*2 and best[2:]==(1,2)
print('PASS all six continuous crossings and full-knot attained errors:',best,flush=True)

fine=min(T-x for x in M)
finearg=None
for j in range(1,12000):
    t=j*10**6
    for p,q in product(range(3),repeat=2):
        if p==q:continue
        val=max(abs(C[j][i]-(t if i==p else 0)) for i in range(3))
        val=max(val,*(abs(M[i]-(t if i==p else T-t if i==q else 0)) for i in range(3)))
        if val<fine:fine,finearg=val,(j,p,q)
assert Q(fine,10**9)==Q(1889,1000) and finearg==(1889,1,2)
assert Q(fine,10**9)-best[0]==Q(1031,2500000)<Q(1,2000)
print('PASS independent fine-grid all-pair scan and exact discretization gap',flush=True)

derived=json.loads((S/'verification/stage06/derived_public.json').read_text())
for grid in derived['grids']:
    N=grid['N']; step=12000//N
    for j,row in enumerate(grid['masses']):
        assert list(map(Q,row))==[Q(b-a,10**9) for a,b in zip(C[j*step],C[(j+1)*step])]
print('PASS all source-to-derived coarse masses',flush=True)

def brute_grid(N,budget):
    # Enumerate ACTUAL runs, with adjacent labels different, including shorter words.
    step=12000//N; times=[j*step*10**6 for j in range(N+1)]
    ac=[C[j*step] for j in range(N+1)]
    best=T; cases=0
    for runs in range(1,budget+2):
        words=[w for w in product(range(3),repeat=runs) if all(a!=b for a,b in zip(w,w[1:]))]
        for middle in combinations(range(1,N),runs-1):
            ends=(0,)+middle+(N,)
            for word in words:
                service=[0]*3; err=0;cases+=1
                for label,l,r in zip(word,ends,ends[1:]):
                    service[label]+=times[r]-times[l]
                    err=max(err,*(abs(ac[r][i]-service[i]) for i in range(3)))
                    if err>=best:break
                best=min(best,err)
    return Q(best,10**9),cases

totalcases=0
for r in D['public']:
    N,s=r['N'],r['budget'];val,cases=brute_grid(N,s);totalcases+=cases
    assert val==Q(r['error'])
    h=Q(12,N);lo=max(Q(0),val-h)
    assert lo==Q(r['general_lower']) and (val-h>=0)==r['lower_strict']
    ts=list(map(Q,r['switch_times']));word=r['modes']
    for j in range(12001):
        t=Q(j,1000);ac=C[j]
        bounds=[Q(0)]+ts+[Q(12)]
        service=[sum(max(Q(0),min(t,b)-a) for label,a,b in zip(word,bounds,bounds[1:]) if label==i)
                 for i in range(3)]
        assert max(abs(Q(a,10**9)-b) for a,b in zip(ac,service))<=val
    print('PASS independent public actual-run enumeration',N,s,val,cases,flush=True)
print('Total independent public grid candidates:',totalcases,flush=True)

# Verify every archived timing median against all three samples.
timings=[D['public_fine']]+D['public']+D['scaling']
for r in D['controlled']:timings.extend([r['subset_dp'],r['word_enumeration']])
for r in timings:
    for kind in ('cpu','wall'):
        samples=r[kind+'_samples_s'];assert len(samples)==3 and min(samples)>0
        assert median(samples)==r[kind+'_median_s']
print('PASS all',len(timings),'CPU/wall timing median records',flush=True)

# Check integer-mode regime transitions independently from the plotted formula.
for s,threshold in [(1,5),(2,8),(3,12)]:
    assert next(n for n in range(s+2,100) if Q(1,n)/(Q(n,n-1)**(s+1)-1)>Q(1,s+2))==threshold
for n in range(2,20):
    for k in range(1,40):
        assert (Q(2*n-3,2*n-2)/k < Q(1,k+1))==(k>2*n-3)
print('PASS regime transitions and classical-bound improvement condition',flush=True)
