from fractions import Fraction as Q
from itertools import combinations_with_replacement, product
from math import comb
from pathlib import Path
import runpy

snap = Path(__file__).resolve().parents[3] / 'process/snapshots/stage02-round01'
runpy.run_path(str(snap / 'verification/check_stage02_finite.py'))

def integral_product(breaks, probabilities):
    return sum((b-a)*probabilities((a+b)/2) for a,b in zip(breaks,breaks[1:]))

def deficiency(x):
    n=len(x)
    breaks=sorted(set([Q(0),Q(1),*x,*[1-v for v in x]]))
    o=Q(0)
    for bits in product([0,1],repeat=n):
        def at(t):
            return int(all(t<=v if k==0 else t>=1-v for v,k in zip(x,bits)))
        o += integral_product(breaks,at)/2**n
    breaks=sorted(set([Q(0),Q(1),*[v if v<=Q(1,2) else 2*(1-v) for v in x]]))
    def at(t):
        p=Q(1)
        for v in x:
            p *= int(t<=v) if v<=Q(1,2) else Q(1,2) if t<=2*(1-v) else 1
        return p
    b=integral_product(breaks,at)
    i=Q(1)
    for v in x: i*=v
    return (x[0]-o,x[0]-i,x[0]-b)

cases=zero=0
for n in [2,3]:
    for x in combinations_with_replacement([Q(i,12) for i in range(13)],n):
        ds=deficiency(x)
        t=min(x[0],sum(1-v for v in x[1:]))
        assert min(ds)>=0
        assert sum(w*d for w,d in zip([18,6,7],ds))>=12*t
        assert ds[0]>=(1-Q(1,2**(n-1)))/(n-1)*t
        if not t:
            zero+=1
            assert ds==(0,0,0)
        cases+=1
print('Exact integrated cubic/quadratic laws:',cases,'including',zero,'zero gaps')

for L in range(2,31):
    w=[Q(1,2**(l+1)) if l<L else Q(1,2**L) for l in range(L+1)]
    B=lambda q: Q(L-q+2,2**q)
    cuts=[s for s in range(1,L) if B(s+1)<=1<=B(s)]
    values=[]
    for s in cuts:
        mix=(1-B(s+1))/(B(s)-B(s+1))
        er=ed=Q(0)
        for q,weight in [(s,mix),(s+1,1-mix)]:
            for l,wl in enumerate(w):
                r=0 if l<q else 2**(l-q+1)
                h=sum(min(2**j,r) for j in range(1,l+1))
                fl=0 if l<=s else 2**(l-s+1)-2
                assert h==s*r+fl
                er+=weight*wl*r
                ed+=weight*wl*h
        assert er==1
        assert ed==s+Q(L-s,2**s)
        values.append(ed)
    assert len(set(values))==1
print('Exact dyadic endpoint profiles and all cutoff ties: L=2,...,30')

assert Q(3131,2275)-Q(1,2)==Q(3987,4550)>0
assert 25002-Q(1000**3,23200)<0
for n in range(2,15):
    for u in [Q(1,100),Q(1,4),Q(1,2),Q(3,4),Q(99,100),*[Q(k,n) for k in range(1,n)]]:
        b=int(n*u);theta=n*u-b
        for d in range(2,n+1):
            q=((1-theta)*comb(b,d)+theta*comb(b+1,d))/comb(n,d)
            assert 0<=q<=u**d<u
            t=min(u,(d-1)*(1-u))
            assert 1<=t/(u-q)<=2
print('Exact equal-mean endpoints near 0 and 1, integral nu, d=2 and d=n: passed')
