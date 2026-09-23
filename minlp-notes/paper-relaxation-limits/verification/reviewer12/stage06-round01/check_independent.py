"""Reviewer 12 exact finite checks, transcribed from the frozen mathematics.

No manuscript implementation is imported. These checks supplement the proofs;
finite instances do not establish universally quantified results.
"""
from fractions import Fraction as Q
from itertools import combinations, product
from math import comb
from pathlib import Path
import json
import random

out = {}
packing_checks = 0
packing_cases = 0
for n in range(2, 41):
    for sym in (False, True):
        if sym and n < 5:
            continue
        k, nx = (n + 3)//4, (n + 1)//2
        means, moments = [], []
        for coord in (0, 1):
            half = nx if coord == 0 else k
            lo = [Q(1, 2) if sym and i < half else Q(0) for i in range(n)]
            mu = [(l + 1)/2 for l in lo]
            Z = [[Q(0) for j in range(n)] for i in range(n)]
            for i in range(n):
                for j in range(n):
                    if not sym:
                        Z[i][j] = Q(n, 4*(n-1)) * (int(i == j)-Q(1,n))
                    elif i < k and j < k:
                        Z[i][j] = Q(k, 16*(k-1)) * (int(i == j)-Q(1,k))
                    elif i == j:
                        Z[i][j] = (1-lo[i])**2/4
            X = [[mu[i]*mu[j]+Z[i][j] for j in range(n)] for i in range(n)]
            # PSD is established analytically by the projection/diagonal blocks;
            # the finite test checks their entries, secants, RLT and distances.
            for i in range(n):
                assert X[i][i] == (lo[i]+1)*mu[i]-lo[i]
                for j in range(n):
                    slacks = [X[i][j]-lo[i]*mu[j]-lo[j]*mu[i]+lo[i]*lo[j],
                              mu[i]-X[i][j]-lo[i]+lo[i]*mu[j],
                              mu[j]-X[i][j]-lo[j]+lo[j]*mu[i],
                              1-mu[i]-mu[j]+X[i][j]]
                    assert min(slacks) >= 0
                    packing_checks += 4
            means.append(mu)
            moments.append(X)
        dist = [sum(X[i][i]-2*X[i][j]+X[j][j] for X in moments)
                for i,j in combinations(range(n),2)]
        assert min(dist) == (Q(k,4*(k-1)) if sym else Q(n,n-1))
        packing_cases += 1
out['packing'] = {'n_range':[2,40], 'covariance_cases':packing_cases,
                  'exact_RLT_inequalities':packing_checks}

def fall(v,j):
    a=Q(1)
    for i in range(j):
        a *= v-i
    return a

gram_checks=0
for d in range(1,5):
    for s in range(2*d, 4*d+6):
        for twice_t in range(4*d-2, 2*(s-2*d+1)+1):
            t=Q(twice_t,2)
            coefficients=[fall(t,2*d-j)*fall(s-t,j)/fall(s,2*d) for j in range(d+1)]
            assert min(coefficients)>=0
            for ell in range(d+1):
                assert sum(coefficients[j]*comb(ell,j) for j in range(ell+1)) == fall(t,2*d-ell)/fall(s,2*d-ell)
                gram_checks+=1
out['fractional_Gram_exact_entries']=gram_checks

rng=random.Random(120601)
stability_checks=0
for m in range(1,11):
    n=2*m
    for case in range(200):
        r=[Q(rng.randrange(11),10) for _ in range(n)]
        c=list(r);rng.shuffle(c)
        S=sum(r)
        if not S:
            continue
        # Change marginals while retaining their total and coordinate capacities.
        for _ in range(n):
            i,j=rng.sample(range(n),2)
            move=min(c[i],1-c[j])*Q(rng.randrange(11),10)
            c[i]-=move;c[j]+=move
        W=[[r[i]*c[j]/S for j in range(n)] for i in range(n)]
        D=1-sum(W[i][i] for i in range(n))
        B=sum(W[i][m+i] for i in range(m))
        g=m-S+(2*m+1)*B+(4*m+1)*D
        assert g>=B+D>=0
        a=[int(x>=Q(1,2)) for x in r];b=list(a)
        for i in range(m):
            if b[i]+b[m+i]==0:b[i]=1
            if b[i]+b[m+i]==2:b[m+i]=0
        error=sum(abs(W[i][j]-Q(b[i]*b[j],m)) for i in range(n) for j in range(n))
        assert error<=4*S*B+58*S*D+5*abs(S-m)
        assert error<=(136*m+10)*g
        assert error<=28*m*B+156*m*D+5*(m-S)
        stability_checks+=1
out['rank_one_exact_rational_roundings']=stability_checks

primitive_checks=0
for b in (Q(1,4),Q(1,16),Q(1,256),Q(1,65536)):
    c=1-b
    for iz, iw in product(range(33),repeat=2):
        z=Q(iz,32);w=c*z*Q(iw,32)
        # Exact hull update for z=b+w, with upper z=1, upper w>=c.
        zn=max(z,b+w);wn=max(w,z-b)
        assert 0<=wn<=c*zn<=c
        assert zn<=b+c*z
        # Exact hull update for w=c*z.
        zp=max(z,w/c);wp=max(w,c*z)
        assert zp==z and wp==c*z
        primitive_checks+=1
out['FBBT_exact_primitive_transitions']=primitive_checks

parity_checks=0
for n in range(2,9):
    for _ in range(50):
        rows=[rng.randrange(1,1<<n) for _ in range(rng.randrange(1,16))]
        basis={}
        chosen=[]
        for row in rows:
            x=row
            while x:
                pivot=x.bit_length()-1
                if pivot in basis:x^=basis[pivot]
                else:
                    basis[pivot]=x;chosen.append(row);break
        union=0;basis_union=0
        for row in rows:union|=row
        for row in chosen:basis_union|=row
        assert union==basis_union
        D=max(row.bit_count() for row in rows)
        assert union.bit_count()<=D*len(basis)
        witness=rng.randrange(1<<n)
        count=sum(all(((x^witness)&row).bit_count()%2==0 for row in rows) for x in range(1<<n))
        assert count==1<<(n-len(basis))
        parity_checks+=1
out['exact_parity_systems']=parity_checks

# Rational P-split witness and exact retained-box lifts, with no optimization.
psplit_checks=0
for D in (Q(2),Q(5,2),Q(7),Q(101,3)):
    v=(3*D,4*D);p=(2*D,4*D/3)
    t=(3*p[0]+4*p[1])/5;w=(4*p[0]-3*p[1])/5
    assert t==34*D/15 and w==4*D/5 and 0<t<5*D
    for vi,pi in zip(v,p):
        assert pi*pi<=vi*vi/2 and (pi-vi)**2<=vi*vi/2
        assert 2*pi*pi<=(vi+1)**2 and 2*(pi-vi)**2<=(vi+1)**2
    psplit_checks+=1
for it,iw in product(range(31),range(-10,11)):
    t=Q(it,10);w=Q(iw,10)
    assert t*t<=3*t and (t-3)**2<=9-3*t and w*w<=1
    psplit_checks+=1
out['P_split_exact_witnesses']=psplit_checks
out['scope']='All arithmetic exact; randomized selection is deterministic finite sampling. No general theorem inferred solely from checks.'
path=Path(__file__).with_suffix('.json')
path.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
