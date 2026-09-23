"""Review checks, importing no manuscript algorithms or author checkers."""
from fractions import Fraction as Q
from pathlib import Path
from itertools import permutations
from math import comb
from statistics import median
import hashlib,json

P=Path(__file__).resolve().parent
S=P/'relocated/verification/stage06'
raw=(P/'public.csv').read_bytes()
assert hashlib.sha256(raw).hexdigest()=='1ed44f0906dfe71654a2f263d354ee0046ae6211baa1ddfd4b5945293c900883'
data=[list(map(Q,line.split())) for line in raw.decode().splitlines()[1:]]
assert len(data)==12001
T=Q(12); rates=[]; A=[[Q(0)]*3]; times=[Q(0)]; normerr=Q(0); quanterr=Q(0)
for j,row in enumerate(data[:-1]):
    dt=data[j+1][0]-row[0]
    assert dt==Q(1,1000)
    original=row[3:]; weights=[v/sum(original) for v in original]
    parts=[divmod(v.numerator*10**6,v.denominator) for v in weights]
    counts=[v[0] for v in parts]
    ranks=sorted(range(3),key=lambda i:(-Q(parts[i][1],weights[i].denominator),i))
    for i in ranks[:10**6-sum(counts)]: counts[i]+=1
    quant=[Q(v,10**6) for v in counts]
    assert sum(quant)==1
    normerr=max(normerr,*(abs(x-y) for x,y in zip(weights,original)))
    quanterr=max(quanterr,*(abs(x-y) for x,y in zip(weights,quant)))
    rates.append(quant); A.append([x+dt*y for x,y in zip(A[-1],quant)]);times.append(data[j+1][0])
assert normerr<Q(4959,10**10) and quanterr<Q(1,10**6)
arch=json.loads((S/'results.json').read_text())
assert normerr==Q(arch['provenance']['normalization_max'])
assert quanterr==Q(arch['provenance']['quantization_max'])
derived=json.loads((S/'derived_public.json').read_text())
for grid in derived['grids']:
    M=grid['N']; stride=12000//M
    actual=[[A[(j+1)*stride][i]-A[j*stride][i] for i in range(3)] for j in range(M)]
    assert actual==[list(map(Q,row)) for row in grid['masses']]

def vector_error(p,q,t,At):
    # Complete vector endpoint evaluation; no dominant-final-mode formula.
    start=[At[i]-(t if i==p else 0) for i in range(3)]
    end=[A[-1][i]-(t if i==p else T-t if i==q else 0) for i in range(3)]
    return max(map(abs,start+end))

# Independently derive all candidate crossings from affine coefficients,
# retain every input endpoint too, and evaluate full vector discrepancies.
pairs=[]
for p,q in permutations(range(3),2):
    candidates=[(vector_error(p,q,t,a),t) for t,a in zip(times,A)]
    for j,alpha in enumerate(rates):
        intercept=A[j][p]-alpha[p]*times[j]
        root=(T-A[-1][q]+intercept)/(2-alpha[p])
        if times[j]<=root<=times[j+1]:
            a=[A[j][i]+(root-times[j])*alpha[i] for i in range(3)]
            candidates.append((vector_error(p,q,root,a),root))
    value,time=min(candidates)
    record=next(r for r in arch['public_continuous_one']['all_pairs'] if (r['p'],r['q'])==(p,q))
    assert value==Q(record['error'])
    # A flat omitted-mode maximum can give an earlier optimal time; compare
    # the error at the archived crossing, not the selected tie representative.
    pairs.append(dict(p=p,q=q,error=str(value),first_candidate_time=str(time)))
assert min(Q(r['error']) for r in pairs)==Q(4721469,2500000)
fine=min(vector_error(p,q,t,a) for p,q in permutations(range(3),2) for t,a in zip(times,A))
assert fine==Q(1889,1000)

# Uniform n=3, k=3: if a mode is omitted the error is >=1/3. Otherwise
# all three modes occur once and label symmetry reduces the optimization
# to two boundary indices and seven explicit endpoint expressions.
uniform=[]
for row in arch['uniform_convergence']:
    M=row['N']; best=Q(1,3)
    for j in range(1,M):
        for l in range(j+1,M):
            a,b=Q(j,M),Q(l,M)
            value=max(2*a/3,b/3,abs(b/3-a),abs(2*b/3-a),
                      abs(Q(1,3)-a),abs(Q(1,3)-b+a),abs(b-Q(2,3)))
            best=min(best,value)
    assert best==Q(row['error'])
    uniform.append([M,str(best)])

# Exact transition dimensions and independent sample-summary checks.
thresholds=[]
for s in (1,2,3):
    first=next(n for n in range(s+2,100) if 1/(n*((Q(n,n-1))**(s+1)-1))>Q(1,s+2))
    thresholds.append(first)
assert thresholds==[5,8,12]
for row in arch['controlled']:
    assert row['cases']==row['n']**(row['budget']+1)*comb(row['N']-1,row['budget'])
def timingcheck(obj):
    if isinstance(obj,dict):
        for prefix in ('wall','cpu'):
            key=prefix+'_samples_s'
            if key in obj:
                assert len(obj[key])==3 and min(obj[key])>=0
                assert median(obj[key])==obj[prefix+'_median_s']
        for v in obj.values(): timingcheck(v)
    elif isinstance(obj,list):
        for v in obj: timingcheck(v)
timingcheck(arch)
print(json.dumps(dict(profile_pairs=pairs,fine=str(fine),uniform_grid=uniform,
    transition_modes=thresholds,derived_cells=84,timing_medians='all passed'),indent=2))
