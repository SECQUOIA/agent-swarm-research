"""Independent exact finite checks; no manuscript or author checker imports.

Run with Python 3. All arithmetic uses Fraction/integer operations. PSD is
checked by rational symmetric elimination, including zero-pivot rows.
These finite checks supplement, and cannot establish, universal theorems.
"""
from fractions import Fraction as Q
from itertools import combinations, combinations_with_replacement, product
from math import comb, prod
from pathlib import Path
import json


def fall(t, j):
    return prod(t-i for i in range(j))


def basis(n, d):
    return [sum(1 << i for i in inds) for j in range(d+1)
            for inds in combinations(range(n), j)]


def psd(matrix):
    """Exact Schur elimination; zero diagonal of a PSD matrix forces zero row."""
    a = [row[:] for row in matrix]
    rank = 0
    for k in range(len(a)):
        pivot = a[k][k]
        assert pivot >= 0, (k, pivot)
        if not pivot:
            assert all(a[k][j] == 0 for j in range(k+1, len(a)))
            continue
        rank += 1
        for i in range(k+1, len(a)):
            if not a[i][k]:
                continue
            factor = a[i][k]/pivot
            for j in range(i, len(a)):
                a[i][j] -= factor*a[k][j]
                a[j][i] = a[i][j]
    return rank


def moment(s, t, mask):
    a = mask.bit_count()
    return Q(fall(t, a), fall(s, a))


def indicator(s, t, ones, zeros, monomial=0):
    """Expand upper slacks directly; no conditional-moment formula is used."""
    ans = Q(0)
    sub = zeros
    while True:
        ans += (-1)**sub.bit_count()*moment(s, t, ones | sub | monomial)
        if not sub:
            return ans
        sub = (sub-1) & zeros


def local_matrices():
    outputs = []
    identities = 0
    for s, t, r in [(2,Q(1),1),(3,Q(3,2),1),(6,Q(3),2),
                     (7,Q(3),2),(7,Q(7,2),2),(7,Q(4),2)]:
        matrices = 0
        for a in range(2*r+1):
            for b in range(2*r-a+1):
                ones, zeros = (1 << a)-1, ((1 << b)-1) << a
                d = (2*r-a-b)//2
                inds = basis(s,d)
                mat = [[indicator(s,t,ones,zeros,u|v) for v in inds] for u in inds]
                psd(mat)
                matrices += 1
                weight = Q(fall(t,a)*fall(s-t,b),fall(s,a+b))
                assert mat[0][0] == weight
        for mon in basis(s,2*r-1):
            assert sum(moment(s,t,mon|(1<<i)) for i in range(s)) == t*moment(s,t,mon)
            identities += 1
        outputs.append(dict(s=s,t=str(t),r=r,localizing_matrices=matrices))
    # Conflicting slacks reduce to zero; repetitions reduce to one assignment.
    for s,t,r in [(3,Q(3,2),1),(7,Q(7,2),2)]:
        for mon in basis(s,2*r-2):
            assert indicator(s,t,1,1,mon) == 0
    return outputs, identities


def tensor_matrices():
    outputs = []
    # Two fractional blocks, then one fractional and one deterministic block.
    for deterministic in [False, True]:
        n, size, order = 14,7,2
        low = (1 << size)-1
        witness = [Q(1)]*3+[Q(1,2)]+[Q(0)]*3
        def E(*masks):
            mask=0
            for v in masks:
                mask |= v
            m0,m1 = mask & low,mask >> size
            # A deterministic half-coordinate is not Boolean: count its
            # multiplicity across factors before evaluating the product.
            second = (prod(witness[i] for v in masks for i in range(size)
                           if (v >> size) >> i & 1)
                      if deterministic else moment(size,Q(7,2),m1))
            return moment(size,Q(7,2),m0)*second
        def full_basis(d):
            return [tuple(1<<i for i in ind) for j in range(d+1)
                    for ind in combinations_with_replacement(range(n),j)]
        inds = full_basis(order)
        mat = [[E(*u,*v) for v in inds] for u in inds]
        rank = psd(mat)
        # Degree-two product across blocks and every global affine square.
        inds1 = basis(n,1)
        cross = [[E(u,v,1)-E(u,v,1,(1<<(size+6))) for v in inds1] for u in inds1]
        crossrank = psd(cross)
        equations = 0
        for mon in full_basis(3):
            for block in range(2):
                assert sum(E(*mon,(1<<(block*size+i))) for i in range(size)) == Q(7,2)*E(*mon)
                equations += 1
        outputs.append(dict(deterministic_second=deterministic,
                            moment_dimension=len(mat),rank=rank,
                            cross_localizer_dimension=len(cross),cross_rank=crossrank,
                            balance_products=equations))
    return outputs


def avoidance():
    checked = 0
    n=4
    for k in range(n):
        for m in range(1,n-k+1):
            z=n-k-m
            witnesses=[]
            for H in combinations(range(n),k):
                for M in combinations([i for i in range(n) if i not in H],m):
                    witnesses.append([4 if i in H else 2 if i in M else 1 for i in range(n)])
            assert len(witnesses) == comb(n,k)*comb(n-k,m)
            for local in product(range(1,8),repeat=n):
                count=sum(all(a&b for a,b in zip(local,w)) for w in witnesses)
                R=sum((a&1)==0 or (a&4)==0 for a in local)
                rho=Q(count,len(witnesses))
                # Squared comparison keeps the real half-exponent check exact.
                assert rho*rho <= max(Q(n-k,n),Q(n-z,n))**R
                checked += 1
    return checked


def sdp():
    cases=0
    for n in range(3,9):
        for k in range(1,n-1):
            for m in range(1,n-k):
                z=n-k-m; p=Q(1,2*m); K=k+Q(1,2)
                w=[Q(1)]*k+[p]*m+[Q(0)]*z
                for count in range(min(k,z)):
                    for Rtuple in combinations(range(n),count):
                        R=set(Rtuple); U=[i for i in range(n) if i not in R]
                        s=len(U); t=K-sum(w[i] for i in R)
                        c=t/s; off=t*(t-1)/(s*(s-1))
                        mu=[w[i] if i in R else c for i in range(n)]
                        X=[[mu[i]*mu[j] if i in R or j in R else c if i==j else off for j in range(n)] for i in range(n)]
                        bounds=[(w[i],w[i]) if i in R else (Q(0),Q(1)) for i in range(n)]
                        aug=[[Q(1)]+mu]+[[mu[i]]+X[i] for i in range(n)]
                        psd(aug)
                        assert sum(mu)==K
                        for i in range(n):
                            assert sum(X[i])==K*mu[i]
                            for j in range(n):
                                a,b=bounds[i]; a2,b2=bounds[j]
                                assert min(X[i][j]-a*mu[j]-a2*mu[i]+a*a2,
                                           b2*mu[i]-X[i][j]-a*b2+a*mu[j],
                                           b*mu[j]-X[i][j]-b*a2+a2*mu[i],
                                           b*b2-b*mu[j]-b2*mu[i]+X[i][j])>=0
                        assert sum(mu[i]-X[i][i] for i in range(n))==sum(w[i]*(1-w[i]) for i in R)
                        cases+=1
    return cases


if __name__=='__main__':
    local, identities=local_matrices()
    out=dict(status='PASS',arithmetic='exact Fraction and integer',
             scope='Finite tests, not a universal theorem proof',
             local_matrices=local,local_balance_products=identities,
             tensor=tensor_matrices(),endpoint_domain_cases=avoidance(),sdp_cases=sdp())
    Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
