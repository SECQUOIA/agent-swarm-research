"""Fresh exact checks; imports no repository implementation or certificates."""
from fractions import Fraction as F
from itertools import product
from random import Random


def cumulative(cols, t):
    n = len(cols[0])
    return [sum((max(F(0), min(F(1), t-j))*col[i]
                 for j, col in enumerate(cols)), F(0)) for i in range(n)]


def direct(cols, p, q, t):
    T = len(cols)
    times = sorted(set([F(j) for j in range(T+1)] + [t]))
    return max(abs(a - (min(x,t) if i == p else F(0))
                   - (max(F(0),x-t) if i == q else F(0)))
               for x in times for i,a in enumerate(cumulative(cols,x)))


def formula(cols,p,q,t):
    n,T=len(cols[0]),len(cols)
    m=cumulative(cols,F(T))
    return max(max((m[i] for i in range(n) if i not in (p,q)),default=F(0)),
               t-cumulative(cols,t)[p], T-m[q]-t)


def construct(cols):
    n,T=len(cols[0]),len(cols)
    E=T*max(F(1,3),F((n-1)**2,n*(2*n-1)))
    m=cumulative(cols,F(T))
    q,r=sorted(range(n),key=lambda i:m[i],reverse=True)[:2]
    if m[q]>=E:
        return r,q,max(F(0),T-m[q]-E),E
    t=T-m[q]-E
    a=cumulative(cols,t)
    p=max((i for i in range(n) if i!=q),key=lambda i:a[i])
    if formula(cols,p,q,t)<=E:
        return p,q,t,E
    return q,r,T-m[r]-E,E


def main():
    # Full cell-word enumeration includes repeated labels and constant schedules.
    uniform_cases=0
    uniform_words=0
    for n in range(2,7):
        for N in range(1,7):
            best=[10**9]*(n-1)
            for word in product(range(n),repeat=N):
                s=sum(word[j]!=word[j-1] for j in range(1,N))
                if s>n-2:
                    continue
                occ=[0]*n
                K=0
                for j,p in enumerate(word,1):
                    occ[p]+=1
                    K=max(K,max(abs(j-n*x) for x in occ))
                best[s]=min(best[s],K)
                uniform_words+=1
            for s in range(n-1):
                optimum=min(best[:s+1])
                for K in range(N,N*(n-1)+1):
                    b=0
                    for _ in range(s+1):
                        b=(n*b+K)//(n-1)
                    if b>=N:
                        break
                assert optimum==K,(n,N,s,optimum,K)
                r=F(n,n-1)
                E=N*max(F(1,n),1/(n*(r**(s+1)-1)))
                assert E<=F(K,n)<E+F(n-1,n)
                uniform_cases+=1
    rng=Random(713)
    profiles=0
    identities=0
    for n in range(2,13):
        for _ in range(160):
            T=rng.randrange(1,8)
            cols=[]
            for j in range(T):
                raw=[rng.randrange(5) for i in range(n)]
                if not sum(raw): raw[0]=1
                cols.append([F(x,sum(raw)) for x in raw])
            p,q=rng.sample(range(n),2)
            for t in (F(0),F(T),F(rng.randrange(3*T+1),3)):
                assert direct(cols,p,q,t)==formula(cols,p,q,t)
                identities+=1
            if n>=3:
                p,q,t,E=construct(cols)
                assert direct(cols,p,q,t)<=E,(n,cols,p,q,t,E)
            profiles+=1
    print(f'PASS: {uniform_cases} uniform budget/grid cases, {uniform_words} schedules enumerated')
    print(f'PASS: {profiles} random rational profiles, {identities} direct three-term identities')
    print('PASS: constructive one-switch bounds for 1600 profiles, including zero masses and endpoint switches')


if __name__=='__main__': main()
