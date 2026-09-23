"""Exact fourth-moment and affine-contact checks for whole-paper reviewer 01."""
from fractions import Fraction as F
from random import Random

rng = Random(41001)
def dot(a, b):
    return sum((x*y for x,y in zip(a,b)), F(0))
def mv(A,x):
    return [dot(row,x) for row in A]
def mm(A,B):
    return [[dot(row,col) for col in zip(*B)] for row in A]
def tr(A):
    return sum((A[i][i] for i in range(len(A))), F(0))
def form(H,x):
    return dot(x,mv(H,x))

distributions = scalar_identities = grouped_identities = midpoint_identities = 0
for n in range(1,6):
    for trial in range(12):
        pts = [[F(rng.randrange(-13,14),rng.randrange(1,8)) for _ in range(n)] for _ in range(n+4)]
        weights = [rng.randrange(1,10) for _ in pts]
        weights = [F(w,sum(weights)) for w in weights]
        mean = [sum((w*x[i] for w,x in zip(weights,pts)),F(0)) for i in range(n)]
        centered = [[v-m for v,m in zip(x,mean)] for x in pts]
        S = [[sum((w*x[i]*x[j] for w,x in zip(weights,centered)),F(0)) for j in range(n)] for i in range(n)]
        hs=[]
        for j in range(3):
            A=[[F(rng.randrange(-4,5),rng.randrange(1,5)) for _ in range(n)] for _ in range(n)]
            H=[[A[i][k]+A[k][i] for k in range(n)] for i in range(n)]
            hs.append(H)
        # Include signed scalar combinations, not only individual Hessians.
        combos=hs+[[[hs[0][i][j]-2*hs[1][i][j]+F(3,2)*hs[2][i][j] for j in range(n)] for i in range(n)]]
        energies=[]
        pair_values=[]
        for H in combos:
            vals=[form(H,x) for x in centered]
            pairs=[(wx*wy,form(H,[a-b for a,b in zip(x,y)])/2) for wx,x in zip(weights,centered) for wy,y in zip(weights,centered)]
            lhs=sum((w*v*v for w,v in pairs),F(0))
            energy=tr(mm(mm(mm(H,S),H),S))
            rhs=sum((w*v*v for w,v in zip(weights,vals)),F(0))/2+dot(weights,vals)**2/2+energy
            assert lhs==rhs and energy>=0 and lhs>=energy
            scalar_identities+=1
            energies.append(energy); pair_values.append(pairs)
        C=[[F(rng.randrange(-3,4),rng.randrange(1,5)) for _ in range(3)] for _ in range(2)]
        gram=[[tr(mm(mm(mm(H,S),G),S)) for G in hs] for H in hs]
        grouped_energy=sum((C[a][j]*C[a][k]*gram[j][k] for a in range(2) for j in range(3) for k in range(3)),F(0))
        grouped_lhs=F(0)
        for wx,x in zip(weights,centered):
            for wy,y in zip(weights,centered):
                d=[a-b for a,b in zip(x,y)]
                v=[form(H,d)/2 for H in hs]
                grouped_lhs+=wx*wy*sum((dot(row,v)**2 for row in C),F(0))
        assert grouped_lhs>=grouped_energy>=0
        grouped_identities+=1
        H=hs[0]; affine=[F(rng.randrange(-9,10)) for _ in range(n)]; intercept=F(11,7)
        def f(x): return form(H,x)/2+dot(affine,x)+intercept
        for x,y in zip(pts,pts[1:]):
            mid=[(a+b)/2 for a,b in zip(x,y)]
            assert (f(x)+f(y))/2-f(mid)==form(H,[a-b for a,b in zip(x,y)])/8
            midpoint_identities+=1
        distributions+=1
print(f'PASS: {distributions} rational distributions, {scalar_identities} exact fourth-moment identities, {grouped_identities} grouped PSD inequalities, {midpoint_identities} affine-invariant midpoint identities.')
