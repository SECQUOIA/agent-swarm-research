"""Exact rational recursive checks of the arbitrary-block one-sided CIA bound."""
from fractions import Fraction as F
from random import Random
from two_switch_equal_mass_certificate import integral


def coefficient(n, k):
    assert 1 <= k < n
    return F(n*(n-1)+(n-k)*(n-k-1), n*k*(2*n-k-1))


def construct(a, k, T=F(1)):
    n = len(a)
    E = coefficient(n, k) * T
    masses = [integral(row, T) for row in a]
    q = max(range(n), key=masses.__getitem__)
    if k == 1 or masses[q] >= T-E:
        return [(q, F(0), T)]
    L = T-masses[q]-E
    Eprime = E-masses[q]/(n-1)
    assert Eprime > 0
    assert coefficient(n-1,k-1)*L <= Eprime
    indices = [i for i in range(n) if i != q]
    completed = [[v+a[q][j]/(n-1) for j,v in enumerate(a[i])] for i in indices]
    prefix = construct(completed, k-1, L)
    return [(indices[i], b, e) for i,b,e in prefix] + [(q,L,T)]


def errors(a, blocks, T=F(1)):
    N = len(a[0])
    endpoints = {F(j,N) for j in range(N+1) if F(j,N)<=T}
    endpoints.add(T)
    for _, b, e in blocks:
        endpoints.update((b,e))
    assert len({i for i,_,_ in blocks}) == len(blocks)
    assert blocks[0][1] == 0 and blocks[-1][2] == T
    assert all(blocks[j][2] == blocks[j+1][1] for j in range(len(blocks)-1))
    negative = positive = F(0)
    for t in endpoints:
        occupation = [F(0)]*len(a)
        for i,b,e in blocks:
            occupation[i] += max(F(0),min(t,e)-b)
        for i,row in enumerate(a):
            delta = occupation[i]-integral(row,t)
            negative = max(negative,delta)
            positive = max(positive,-delta)
    return negative, positive


def verify():
    rng = Random(909432)
    arbitrary = equal = 0
    for n in range(2,13):
        for k in range(1,n):
            C = coefficient(n,k)
            if k > 1:
                prev = coefficient(n-1,k-1)
                assert C == ((n-1)**2*prev+1)/(n*(n-1)*(1+prev))
            assert C >= F(1,n)
            for trial in range(5):
                N = 5
                columns = []
                for _ in range(N):
                    weights = [rng.randrange(10) for _ in range(n)]
                    weights[rng.randrange(n)] += 1
                    columns.append([F(w,sum(weights)) for w in weights])
                a = [list(row) for row in zip(*columns)]
                blocks = construct(a,k)
                assert len(blocks) <= k
                assert errors(a,blocks)[0] <= C
                arbitrary += 1
            # Each cyclic family of columns has exact equal terminal masses.
            weights = [rng.randrange(1,10) for _ in range(n)]
            columns = [[F(weights[(i-j)%n],sum(weights)) for i in range(n)] for j in range(n)]
            rng.shuffle(columns)
            a = [list(row) for row in zip(*columns)]
            assert all(integral(row,F(1)) == F(1,n) for row in a)
            blocks = construct(a,k)
            assert max(errors(a,blocks)) <= C
            equal += 1
    print(f'Arbitrary-block bound: {arbitrary} arbitrary profiles and {equal} equal-total profiles passed exactly; all k<n through n=12.')


if __name__ == '__main__':
    verify()
