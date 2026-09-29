from fractions import Fraction as Q
from random import Random
rng=Random(731)
def tr(A): return list(map(list,zip(*A)))
def mul(A,B): return [[sum((x*y for x,y in zip(a,b)),Q()) for b in tr(B)] for a in A]
def inverse_lower(L):
    n=len(L); U=[[Q(i==j) for j in range(n)] for i in range(n)]
    for j in range(n):
        for i in range(j+1,n): U[i][j]=-sum(L[i][k]*U[k][j] for k in range(j,i))
    return U
cases=0
for n in range(1,6):
 for _ in range(50):
    M=[[Q(rng.randrange(-12,13),rng.randrange(1,8)) for j in range(n)] for i in range(n)]
    A=mul(M,tr(M))
    for i in range(n): A[i][i]+=Q(1, rng.randrange(1,100))
    L=[[Q(i==j) for j in range(n)] for i in range(n)]; D=[]
    for i in range(n):
        D.append(A[i][i]-sum(L[i][k]**2*D[k] for k in range(i)))
        assert D[i]>0
        for j in range(i+1,n): L[j][i]=(A[j][i]-sum(L[j][k]*L[i][k]*D[k] for k in range(i)))/D[i]
    S=[]
    for x in D:
        t=x.numerator.bit_length()-x.denominator.bit_length()
        p2=Q(2**t) if t>=0 else Q(1,2**(-t))
        m=t if x>=p2 else t-1
        k=-(m//2)
        s=Q(2**k) if k>=0 else Q(1,2**(-k))
        assert 1<=s*s*x<4
        S.append(s)
    U=inverse_lower(L)
    R=[[S[i]*u for u in U[i]] for i in range(n)]
    C=mul(mul(R,A),tr(R))
    assert all(C[i][j]==(S[i]**2*D[i] if i==j else 0) for i in range(n) for j in range(n))
    cases+=1
print(f'Exact rational LDL/dyadic normalization identities verified in {cases} SPD cases, dimensions 1 through 5.')
