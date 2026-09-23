"""Independent exact checks of cross-representation Schur identities.
No imports from paper implementations. Non-Markov K tests the claimed algebraic scope.
"""
from itertools import combinations
from pathlib import Path
import json
import sympy as s

R=s.Rational
n,p=4,2
J0=s.diag(R(1,3),R(2,5))
F=s.Matrix([[1,R(1,2)],[-1,2],[R(1,3),-2],[2,1]])
A=[1];B=[0,1,3]
subsets=[list(c) for k in range(5) for c in combinations(range(n),k)]

def schur(M, keep):
    rem=[i for i in range(M.rows) if i not in keep]
    if not rem:return M.extract(keep,keep)
    return M.extract(keep,keep)-M.extract(keep,rem)*M.extract(rem,rem).inv()*M.extract(rem,keep)

def psd(M):
    assert M==M.T
    return all(M.extract(c,c).det()>=0 for k in range(1,M.rows+1) for c in combinations(range(M.rows),k))

def aug(K, anchors, S):
    H=K[:,anchors]*K.extract(anchors,anchors).inv()
    D=K-H*K.extract(anchors,anchors)*H.T+s.eye(n)/3
    Q=s.diag(J0,K.extract(anchors,anchors).inv())
    if S:
        E=F.extract(S,range(p)).row_join(H.extract(S,range(len(anchors))))
        Q+=E.T*D.extract(S,S).inv()*E
    return Q
count=0
for seed in range(5):
    T=s.Matrix(n,n,lambda i,j:R(((i+2)*(j+3)+seed*3)%11-5,7))
    K=T*T.T+s.eye(n)
    ma=[];mb=[]
    for S in subsets:
        small=aug(K,A,S);big=aug(K,B,S)
        keep=[0,1]+[p+B.index(a) for a in A]
        assert schur(big,keep)==small
        J=J0 if not S else J0+F.extract(S,range(p)).T*(K+s.eye(n)/3).extract(S,S).inv()*F.extract(S,range(p))
        assert schur(small,list(range(p)))==J
        assert schur(big,list(range(p)))==J
        count+=3;ma.append(small);mb.append(big)
    weights=[R(i+1,sum(range(1,17))) for i in range(16)]
    M1=sum((w*M for w,M in zip(weights,ma)),s.zeros(p+len(A)))
    M2=sum((w*M for w,M in zip(weights,mb)),s.zeros(p+len(B)))
    assert psd(schur(M2,[0,1,3])-M1)
    assert psd(schur(M2,[0,1])-schur(M1,[0,1]))
    count+=2
print(json.dumps({'passed':True,'exact_matrix_checks':count,'models':5,'schedules_each':16,'scope':'Non-Markov SPD latent covariance; nested A={1}, B={0,1,3}; nonuniform exact mixture; all nuisance prior cross terms retained'},indent=2))
