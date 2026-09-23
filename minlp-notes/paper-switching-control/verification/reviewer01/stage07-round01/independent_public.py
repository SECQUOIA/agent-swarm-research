from fractions import Fraction as F
from pathlib import Path
from itertools import combinations
from statistics import median
import json,hashlib,bisect,math
HERE=Path(__file__).resolve().parent
P=HERE/'relocated'
archive=json.loads((P/'verification/stage06/results.json').read_text())
derived=json.loads((P/'verification/stage06/derived_public.json').read_text())
raw=(HERE/'public-source.csv').read_bytes()
assert hashlib.sha256(raw).hexdigest()==archive['provenance']['sha256']
source=[list(map(F,line.split())) for line in raw.decode().splitlines()[1:]]
D=10**9; prefixes=[[0,0,0]]; normalize=F(0); quantize=F(0); cum=[F(0)]*3; cummax=F(0)
for j,row in enumerate(source[:-1]):
    assert source[j+1][0]-row[0]==F(1,1000)
    rates=row[3:]; normalized=[x/sum(rates) for x in rates]
    floors=[int(x*10**6) for x in normalized]
    need=10**6-sum(floors)
    # Independently select the integral allocation with minimum total deviation,
    # then resolve tied allocations by preferring earlier indices.
    candidates=[]
    for selected in combinations(range(3),need):
        counts=tuple(floors[i]+(i in selected) for i in range(3))
        candidates.append((sum(abs(F(counts[i],10**6)-normalized[i]) for i in range(3)),tuple(-x for x in counts),counts))
    counts=min(candidates)[2]
    assert sum(counts)==10**6
    normalize=max(normalize,*(abs(rates[i]-normalized[i]) for i in range(3)))
    quantize=max(quantize,*(abs(F(counts[i],10**6)-normalized[i]) for i in range(3)))
    cum=[cum[i]+(normalized[i]-F(counts[i],10**6))/1000 for i in range(3)]
    cummax=max(cummax,*map(abs,cum))
    prefixes.append([prefixes[-1][i]+counts[i] for i in range(3)])
assert len(prefixes)==12001 and sum(prefixes[-1])==12*D
for name,v in [('normalization_max',normalize),('quantization_max',quantize),('cumulative_quantization_max',cummax)]:
    assert v==F(archive['provenance'][name])
print('Pinned source hash, independent minimum-deviation quantization, and all perturbation summaries agree',flush=True)
T=12*D; totals=prefixes[-1]; finebest=None
pairs=[]
for p in range(3):
  for q in range(3):
    if p==q:continue
    # Exact monotone root indexed by binary search, in integer mass units.
    g=[2*j*10**6-prefixes[j][p]-T+totals[q] for j in range(12001)]
    j=max(0,bisect.bisect_left(g,0)-1)
    tau=F(j*10**6)-F(g[j]*10**6,g[j+1]-g[j])
    A_tau=[F(prefixes[j][i])+(tau-j*10**6)*F(prefixes[j+1][i]-prefixes[j][i],10**6) for i in range(3)]
    E=F(0)
    for t,A in [(l*10**6,a) for l,a in enumerate(prefixes)]+[(tau,A_tau)]:
      for i in range(3):
        w=min(t,tau) if i==p else max(0,t-tau) if i==q else 0
        E=max(E,abs(A[i]-w))
    pairs.append({'p':p,'q':q,'time':str(tau/D),'error':str(F(E)/D)})
    for l,A in enumerate(prefixes):
      t=l*10**6
      # Full signed residuals at the switch and final horizon: six constraints.
      atswitch=max(abs(A[i]-(t if i==p else 0)) for i in range(3))
      atend=max(abs(totals[i]-(t if i==p else T-t if i==q else 0)) for i in range(3))
      item=(max(atswitch,atend),p,q,t)
      if finebest is None or item<finebest:finebest=item
assert pairs==archive['public_continuous_one']['all_pairs']
assert F(finebest[0],D)==F(1889,1000)
print('Independent binary-search roots and full signed endpoint scans reproduce all six continuous pair values and fine optimum',finebest,flush=True)

def count_dp(A,h,S):
    # State holds cumulative service counts, last mode and actual switches.
    # Every cell label is extended; at a fixed state current error is fixed.
    # Thus smaller historical maximum dominates. No block partitioning used.
    states={(0,0,-1,0):0}
    for j in range(1,len(A)):
      nxt={}
      for (a,b,last,s),v in states.items():
        for label in range(3):
          sn=s+(last!=-1 and last!=label)
          if sn>S:continue
          aa=a+(label==0);bb=b+(label==1);cc=j-aa-bb
          e=max(v,abs(aa*h-A[j][0]),abs(bb*h-A[j][1]),abs(cc*h-A[j][2]))
          key=(aa,bb,label,sn)
          if key not in nxt or e<nxt[key]:nxt[key]=e
      states=nxt
    return [min(v for (*_,s),v in states.items() if s<=budget) for budget in range(S+1)]
for grid in derived['grids']:
    M=grid['N']; step=12000//M; A=[prefixes[j*step] for j in range(M+1)]
    assert [[F(A[j+1][i]-A[j][i],D) for i in range(3)] for j in range(M)]==[list(map(F,row)) for row in grid['masses']]
    answer=count_dp(A,12*D//M,3)
    for s,E in enumerate(answer):
      row=next(x for x in archive['public'] if x['N']==M and x['budget']==s)
      assert F(E,D)==F(row['error'])
      lower=F(E,D)-F(12,M)
      assert F(row['general_lower'])==max(0,lower) and row['lower_strict']==(lower>=0)
    print('All-prefix cumulative-count DP confirms all four public budgets at M',M,[str(F(v,D)) for v in answer],flush=True)
for row in archive['uniform_convergence']:
    M=row['N'];A=[[j]*3 for j in range(M+1)]
    exact=F(count_dp(A,3,2)[2],3*M)
    assert exact==F(row['error'])
print('Cumulative-count DP independently confirms every uniform convergence point',flush=True)
# Exact rational regime transition checks and comparison with the new sourced upper bound.
for s,start in [(1,5),(2,8),(3,12)]:
  for n in range(s+2,101):
    geo=1/(n*(F(n,n-1)**(s+1)-1)); plateau=F(1,s+2)
    assert (geo>plateau)==(n>=start)
    assert max(geo,plateau)<=F(2*n-3,(2*n-2)*(s+1))
for n in range(2,51):
  for k in range(1,101):
    assert (F(2*n-3,(2*n-2)*k)<F(1,k+1))==(k>2*n-3)
# Medians and archived table case counts, independent of solver execution.
def timing(x):
    for kind in ('cpu','wall'):
      values=x[kind+'_samples_s'];assert len(values)==3 and all(v>0 for v in values)
      assert median(values)==x[kind+'_median_s']
timing(archive['public_fine'])
for r in archive['public']+archive['scaling']:timing(r)
for r in archive['controlled']:
  for m in ['subset_dp','word_enumeration']:timing(r[m])
  k=min(r['budget']+1,r['N'])
  assert r['cases']==r['n']**k*math.comb(r['N']-1,k-1)
print('Headline thresholds, new classical comparison, case counts, and all stored timing medians verified',flush=True)
