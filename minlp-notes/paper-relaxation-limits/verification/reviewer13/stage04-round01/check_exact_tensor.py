"""Finite exact tensor/Boolean-localizer checks; not a universal theorem proof."""
from fractions import Fraction as Q
from itertools import combinations,combinations_with_replacement
from pathlib import Path
import json

def falling(x,k):
    out=Q(1)
    for j in range(k):out*=x-j
    return out

def expect(indices,s,t):
    inds=set(indices)
    return falling(t,len(inds))/falling(s,len(inds))

def tensor(indices,s,t):
    return expect([i for i in indices if i<s],s,t)*expect([i for i in indices if i>=s],s,t)

def exact_psd(a):
    """Symmetric elimination: a zero diagonal must have a zero row in PSD."""
    a=[row[:] for row in a]; rank=0
    for k in range(len(a)):
        pivot=a[k][k]
        assert pivot>=0,(k,pivot)
        if not pivot:
            assert all(a[k][j]==0 for j in range(k+1,len(a))),('zero pivot row',k)
            continue
        rank+=1
        for i in range(k+1,len(a)):
            if a[i][k]:
                v=a[i][k]/pivot
                for j in range(i,len(a)):
                    a[j][i]=a[i][j]=a[i][j]-v*a[k][j]
    return rank

results=[]
for r,s,t in [(1,3,Q(3,2)),(2,7,Q(7,2))]:
    n=2*s
    basis=[()]+[(i,) for i in range(n)]
    if r==2:basis+=list(combinations_with_replacement(range(n),2))
    a=[[tensor(i+j,s,t) for j in basis] for i in basis]
    rank=exact_psd(a)
    eqcount=0
    for d in range(2*r):
        for v in combinations_with_replacement(range(n),d):
            for block in range(2):
                assert sum(tensor(v+(j,),s,t) for j in range(block*s,(block+1)*s))==t*tensor(v,s,t)
                eqcount+=1
    local=[]
    if r==2:
        lin=[()]+[(i,) for i in range(n)]
        # Repeated lower slack, and a product across blocks with an upper slack.
        for factors in ['repeated','cross_block']:
            def e(v):
                if factors=='repeated':return tensor(v+(0,0),s,t)
                return tensor(v+(0,),s,t)-tensor(v+(0,s),s,t)
            mat=[[e(i+j) for j in lin] for i in lin]
            local.append({'factor':factors,'size':len(lin),'rank':exact_psd(mat)})
    results.append({'r':r,'s':s,'t':str(t),'global_moment_matrix_size':len(basis),'exact_rank':rank,'balance_products':eqcount,'localizers':local})
Path(__file__).with_suffix('.json').write_text(json.dumps({'arithmetic':'exact rational','results':results,'limit':'Finite examples only; positivity for all parameters rests on the written Gram/tensor proofs.'},indent=2)+'\n')
print(json.dumps(results))
