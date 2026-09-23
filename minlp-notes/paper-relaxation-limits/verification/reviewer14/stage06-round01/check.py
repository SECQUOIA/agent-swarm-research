"""Independent finite checks; no universal claim follows from these samples."""
from fractions import Fraction as F
from itertools import combinations, product
from math import comb
from pathlib import Path
import json

# Evaluate quadratic forms directly, rather than the manuscript's cut-bit-count code.
signing = {}
for n in range(2, 8):
    edges = list(combinations(range(n), 2))
    free = [(i,j) for i,j in edges if i]
    spins = [(1,)+s for s in product((-1,1), repeat=n-1)]
    best = 10**9
    for a in product((-1,1), repeat=len(free)):
        values = [sum(s[j] for j in range(1,n)) +
                  sum(c*s[i]*s[j] for c,(i,j) in zip(a,free)) for s in spins]
        best = min(best,(max(values)-min(values))//2)
    signing[n] = best
assert list(signing.values()) == [1,2,4,4,5,8]

# LRS interpolation on the Hamming levels; exact moments and sup-norm bound.
density = {}
for k in range(3,20,2):
    t = F(k,2)
    c = []
    for j in range(k+1):
        a = F(1)
        for i in range(k+1):
            if i != j: a *= (t-i)/(j-i)
        c.append(a)
    d = [2**k * c[j]/comb(k,j) for j in range(k+1)]
    f = [((F(j)-t)**2-F(1,4))/k**2 for j in range(k+1)]
    assert sum(c) == 1
    assert sum(cj*fj for cj,fj in zip(c,f)) == -F(1,4*k*k)
    assert max(abs(v) for v in d)**2 <= k**3
    assert all(0 <= fj+F(1,8*k*k) <= 1 for fj in f)
    density[k] = {'EDf':str(sum(cj*fj for cj,fj in zip(c,f))),
                  'norm':str(max(abs(v) for v in d))}

# Full tightened RLT inequalities for both covariance matrices, every pair.
packing = {}
for n in range(5,41):
    k=(n+3)//4; nx=(n+1)//2
    bounds = [[(F(1,2),F(1)) if i<limit else (F(0),F(1))
               for i in range(n)] for limit in (nx,k)]
    means = [[(l+u)/2 for l,u in bb] for bb in bounds]
    matrices=[]
    for coord in range(2):
        M=[]
        for i in range(n):
            row=[]
            for j in range(n):
                cov = F(0)
                if i==j: cov=(bounds[coord][i][1]-bounds[coord][i][0])**2/4
                elif i<k and j<k: cov=-F(1,16*(k-1))
                row.append(means[coord][i]*means[coord][j]+cov)
            M.append(row)
        for i in range(n):
            for j in range(n):
                li,ui=bounds[coord][i]; lj,uj=bounds[coord][j]
                mi,mj=means[coord][i],means[coord][j]
                assert M[i][j]>=li*mj+lj*mi-li*lj
                assert M[i][j]>=ui*mj+uj*mi-ui*uj
                assert M[i][j]<=ui*mj+lj*mi-ui*lj
                assert M[i][j]<=li*mj+uj*mi-li*uj
        matrices.append(M)
    distances=[sum(M[i][i]-2*M[i][j]+M[j][j] for M in matrices)
               for i,j in combinations(range(n),2)]
    assert min(distances)==F(k,4*(k-1))
    packing[n]=str(min(distances))

result={'arithmetic':'exact integers and fractions', 'complete_signings':signing,
        'LRS_Hamming_level_checks':density, 'packing_SYM_RLT_feasibility':packing,
        'limits':'Finite checks only. Pseudo-density PSD and covariance PSD are not tested here; they were checked analytically.'}
Path(__file__).with_name('results.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS: full signing minima n=2..7; LRS level identities odd k=3..19; packing RLT and minimum distances n=5..40.')
