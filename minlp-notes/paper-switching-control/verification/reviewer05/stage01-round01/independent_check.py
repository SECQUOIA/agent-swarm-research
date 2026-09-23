from fractions import Fraction as Q
from itertools import product
from random import Random

# Enumerate every grid word, including repeated modes, rather than block words.
configs = 0
for n in range(2, 7):
    for N in range(1, 7):
        best = [None] * (n-1)
        for word in product(range(n), repeat=N):
            s = sum(a != b for a,b in zip(word,word[1:]))
            if s > n-2:
                continue
            occ = [0]*n
            numerator = 0
            for t, p in enumerate(word, 1):
                occ[p] += 1
                numerator = max(numerator, *(abs(t-n*w) for w in occ))
            for budget in range(s,n-1):
                best[budget] = numerator if best[budget] is None else min(best[budget],numerator)
        for s, exact_num in enumerate(best):
            K = N
            while True:
                b = 0
                for _ in range(s+1):
                    b = (n*b+K)//(n-1)
                if b >= N: break
                K += 1
            assert K == exact_num, (n,N,s,K,exact_num)
            r = Q(n,n-1)
            continuous = N*max(Q(1,n),1/(n*(r**(s+1)-1)))
            assert continuous <= Q(K,n) < continuous+Q(n-1,n)
            configs += 1
print('PASS uniform recurrence and strict gap against exhaustive grid words:',configs,'parameter triples')

rng = Random(52026)
def cumulative(cells,t):
    n = len(cells[0])
    return [sum(c[i]*min(Q(1), max(Q(0),t-j)) for j,c in enumerate(cells)) for i in range(n)]
def error(cells,p,q,tau):
    n = len(cells[0]); T = len(cells)
    direct = Q(0)
    for t in sorted(set([Q(j) for j in range(T+1)]+[tau])):
        vals = cumulative(cells,t)
        for i in range(n):
            w = (min(t,tau) if i==p else Q(0)) + (max(Q(0),t-tau) if i==q else Q(0))
            direct = max(direct,abs(vals[i]-w))
    m = cumulative(cells,Q(T))
    formula = max(max((m[i] for i in range(n) if i not in [p,q]),default=Q(0)),tau-cumulative(cells,tau)[p],T-m[q]-tau)
    assert direct == formula
    return direct
cases=0
for n in range(2,10):
    for _ in range(100):
        T = rng.randrange(1,6)
        cells=[]
        for j in range(T):
            weights=[rng.randrange(4) for i in range(n)]
            if not sum(weights): weights[0]=1
            cells.append([Q(w,sum(weights)) for w in weights])
        p,q=rng.sample(range(n),2)
        for tau in [Q(0),Q(T),Q(T,2),Q(rng.randrange(3*T+1),3)]:
            error(cells,p,q,tau)
        if n>=3:
            E = T*max(Q(1,3),Q((n-1)**2,n*(2*n-1)))
            m=cumulative(cells,Q(T)); order=sorted(range(n),key=lambda i:m[i],reverse=True)
            q,r=order[:2]
            if m[q]>=E:
                p=r; tau=max(Q(0),T-m[q]-E)
            else:
                tau=T-m[q]-E
                v=cumulative(cells,tau)
                p=max((i for i in range(n) if i!=q),key=lambda i:v[i])
                if error(cells,p,q,tau)>E:
                    p,q=q,r; tau=T-m[q]-E
            assert error(cells,p,q,tau)<=E,(n,cells,p,q,tau,E)
        cases+=1
print('PASS independent three-term/endpoint and constructive bound checks:',cases,'rational profiles')
