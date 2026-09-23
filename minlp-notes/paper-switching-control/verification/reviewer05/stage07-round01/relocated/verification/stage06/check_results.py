"""Offline exact checks of all archived derived tables; no timing assertions."""
if not __debug__:
    raise SystemExit('Do not use -O: exact verification requires assertions.')

from fractions import Fraction as F
from pathlib import Path
import json, sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from experiments import solve, exhaustive, continuous_one
from rounding import optimal_few_switches, schedule_error

def main():
    data=json.loads((HERE/'results.json').read_text())
    derived=json.loads((HERE/'derived_public.json').read_text())
    assert derived['source_sha256']==data['provenance']['sha256']
    grids={r['N']:r for r in derived['grids']}
    previous={}
    for row in data['public']:
        M,s=row['N'],row['budget']; g=grids[M]; h=F(g['width'])
        masses=[list(map(F,x)) for x in g['masses']];dt=[h]*M
        assert len(masses)==M and all(sum(x)==h and min(x)>=0 for x in masses)
        ans=solve(masses,dt,s)
        assert ans.error==F(row['error'])==schedule_error(masses,dt,ans.schedule())
        knots=[F(t) for t in row['switch_times']]
        modes=row['modes']
        assert len(modes)==len(knots)+1 and len(knots)<=s
        assert knots==sorted(set(knots)) and all(0<t<M*h and (t/h).denominator==1 for t in knots)
        assert all(type(i) is int and 0<=i<3 for i in modes)
        archived=tuple(modes[sum(t<=j*h for t in knots)] for j in range(M))
        assert sum(a!=b for a,b in zip(archived,archived[1:]))<=s
        assert schedule_error(masses,dt,archived)==F(row['error'])
        assert F(row['general_lower'])==max(F(0),ans.error-h)
        assert row['lower_strict']==(ans.error-h>=0)
        if s in previous: assert ans.error<=previous[s]
        previous[s]=ans.error
        if M==12:
            value,cases=exhaustive(masses,dt,s)
            assert value==ans.error and cases==row['independent_cases']
    assert [(r['N'],r['budget']) for r in data['public']]==[(N,s) for N in (12,24,48) for s in range(4)]
    assert F(data['public_fine']['error'])==F(1889,1000)
    pairs=data['public_continuous_one']['all_pairs']
    assert len(pairs)==6 and min(F(x['error']) for x in pairs)==F(4721469,2500000)
    assert F(data['public_fine']['error'])-F(4721469,2500000)==F(1031,2500000)<F(1,2000)
    # All-pair crossing routine has independent exact analytic oracle cases.
    for n in (2,3,4,5):
        got=continuous_one([[F(1,n)]*n],[1])
        want=max(F(1,n),F((n-1)**2,n*(2*n-1))) if n>2 else F(1,6)
        assert F(got['best']['error'])==want
    assert F(continuous_one([[F(1,2),0],[0,F(1,2)]],[F(1,2)]*2)['best']['error'])==0
    for row in data['uniform_convergence']:
        M=row['N'];width=F(1,M);masses=[[width/3]*3 for _ in range(M)]
        answer=optimal_few_switches(masses,[width]*M,2)
        assert answer.error==F(row['error']) and F(row['lower'])==max(F(0),answer.error-width)
        assert F(row['lower'])<=F(1,6)<=answer.error
        assert exhaustive(masses,[width]*M,2)[0]==answer.error
    for row in data['scaling']:
        n,N=row['n'],row['N'];sample=[[F(1,n*N)]*n for _ in range(N)]
        assert optimal_few_switches(sample,[F(1,N)]*N,2).error==F(row['error'])
    for row in data['controlled']:
        n,N,s=row['n'],row['N'],row['budget'];sample=[]
        for j in range(N):
            w=[1+((j+2)*(i+3)+i*i)%11 for i in range(n)]
            sample.append([F(x,N*sum(w)) for x in w])
        value,cases=exhaustive(sample,[F(1,N)]*N,s)
        assert value==F(row['error']) and cases==row['cases']
    print('PASS: derived public grids and budgets, exact brackets, crossing oracles, convergence, scaling and independent enumeration')
    print('Fine-source provenance and off-grid public crossing require experiments.py --fetch (or --data); archived summaries alone do not revalidate the source.')
if __name__=='__main__': main()
