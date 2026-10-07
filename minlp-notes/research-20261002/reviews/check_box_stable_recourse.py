"""Exact small-instance diagnostics for excluded-region QP closure.

Face enumeration is a diagnostic oracle, not the claimed forest algorithm.
The tested interface is containment and closure, not the full random search.
"""
from fractions import Fraction as Q
from itertools import product


def solve(matrix, rhs):
    n = len(rhs)
    aug = [list(matrix[i]) + [rhs[i]] for i in range(n)]
    for j in range(n):
        pivot = next((i for i in range(j, n) if aug[i][j]), None)
        if pivot is None:
            return None
        aug[j], aug[pivot] = aug[pivot], aug[j]
        scale = aug[j][j]
        aug[j] = [v / scale for v in aug[j]]
        for i in range(n):
            if i != j:
                scale = aug[i][j]
                aug[i] = [v - scale*w for v, w in zip(aug[i], aug[j])]
    return [row[-1] for row in aug]


def value(A, b, c, x):
    return c + sum(bi*xi for bi, xi in zip(b, x)) + sum(
        A[i][j]*x[i]*x[j]/2 for i in range(len(x)) for j in range(len(x)))


def qp(A, b, c, bounds):
    n = len(b)
    winner = None
    for status in product((-1, 0, 1), repeat=n):
        free = [i for i in range(n) if status[i] == 0]
        x = [bounds[i][status[i] == 1] if status[i] else Q(0) for i in range(n)]
        mat = [[A[i][j] for j in free] for i in free]
        rhs = [-b[i] - sum(A[i][j]*x[j] for j in range(n) if j not in free) for i in free]
        sol = solve(mat, rhs)
        if sol is None:
            continue
        for i, xi in zip(free, sol):
            x[i] = xi
        if all(lo <= xi <= hi for xi, (lo, hi) in zip(x, bounds)):
            candidate = (value(A, b, c, x), tuple(x))
            if winner is None or candidate < winner:
                winner = candidate
    assert winner is not None
    return winner


def positive_definite(A):
    A = [list(row) for row in A]
    for i in range(len(A)):
        assert A[i][i] > 0
        for j in range(i+1, len(A)):
            for k in range(j, len(A)):
                A[j][k] -= A[i][j]*A[i][k]/A[i][i]
                A[k][j] = A[j][k]


# Coordinates x,y,w,z; residual interaction graph z--y--w is a forest.
# F=(x-1/2)^2+(y-x/4)^2+(w-y/3)^2+z(3-z)+zy/10.
A = [[Q(17,8),Q(-1,2),Q(0),Q(0)],
     [Q(-1,2),Q(20,9),Q(-2,3),Q(1,10)],
     [Q(0),Q(-2,3),Q(2),Q(0)],
     [Q(0),Q(1,10),Q(0),Q(-2)]]
b0 = [Q(-1),Q(0),Q(0),Q(3)]
constant = Q(1,4)
unit = [(Q(0),Q(1))]*4
L, sigma, g0, tau = Q(17,8), Q(1,100), Q(1,16), Q(1,2)
M1 = max(Q(1), max(sum(abs(v) for v in row) for row in A))
G = max(Q(1),abs(b0[0])+sigma+sum(abs(v) for v in A[0]))
r = min(Q(1,8),tau/(16*M1))
amplification = 2+L/g0
h = Q(1)
while h > min(r/(4*amplification),g0*r*r/(16*G*amplification)):
    h /= 2

slab_calls = 0
for gamma in ([Q(0)]*4,
              [sigma,-sigma,sigma,-sigma],
              [-sigma,sigma,-sigma,sigma],
              [sigma]*4):
    b = [bi+gi for bi,gi in zip(b0,gamma)]
    optimum, a = qp(A,b,constant,unit)
    assert a[3] == 0 and all(0<a[i]<1 for i in range(3))
    index = (a[0]/h + Q(1,2)).numerator // (a[0]/h + Q(1,2)).denominator
    core = index*h
    query_box = [(core,core)]+unit[1:]
    vcore, witness = qp(A,b,constant,query_box)
    e = L*h*h/8
    assert vcore-optimum <= e
    D = (core-h,core+h)
    assert D[0] <= a[0] <= D[1]
    patch = [D]+[(max(Q(0),witness[i]-r),min(Q(1),witness[i]+r)) for i in range(1,4)]
    assert all(lo<=ai<=hi for ai,(lo,hi) in zip(a,patch))
    exclusions=[]
    for i in range(1,4):
        for sign in (-1,1):
            threshold=witness[i]+sign*r
            if 0<threshold<1:
                bounds=list(query_box)
                bounds[i]=(Q(0),threshold) if sign==-1 else (threshold,Q(1))
                exclusions.append(qp(A,b,constant,bounds)[0])
                slab_calls+=1
    assert min(exclusions)-vcore > 2*G*(D[1]-D[0])
    # Wrongly retaining the clipped original-bound singleton would fail.
    wrong=list(query_box)
    wrong[3]=(Q(0),Q(0))
    assert qp(A,b,constant,wrong)[0] == vcore
    fixed=[]
    for i in range(4):
        lower=b[i]+sum(A[i][j]*(patch[j][0] if A[i][j]>=0 else patch[j][1]) for j in range(4))
        upper=b[i]+sum(A[i][j]*(patch[j][1] if A[i][j]>=0 else patch[j][0]) for j in range(4))
        if lower>0 and patch[i][0]==0:
            fixed.append(i)
            patch[i]=(Q(0),Q(0))
        elif upper<0 and patch[i][1]==1:
            fixed.append(i)
            patch[i]=(Q(1),Q(1))
    assert fixed == [3]
    free=[0,1,2]
    positive_definite([[A[i][j]-(g0 if i==j else 0) for j in free] for i in free])
    assert qp(A,b,constant,patch) == (optimum,a)

# A second residual minimizer must prevent exclusion-based closure.
Atie=[[Q(2),Q(0)],[Q(0),Q(-2)]]
btie=[Q(-1),Q(1)]
tie_box=[(Q(1,2),Q(1,2)),(Q(0),Q(1))]
tie_value,tie_point=qp(Atie,btie,Q(1,4),tie_box)
assert tie_point[1] == 0
outside=[tie_box[0],(Q(1,8),Q(1))]
assert qp(Atie,btie,Q(1,4),outside)[0] == tie_value

# Exact inequalities in the base-only cutoff on widely separated scales.
budgets=0
for n,k,curvature,noise,rowbound,gradient in (
    (1,1,Q(1),Q(1),Q(1),Q(1)),
    (7,2,Q(17,8),Q(1,100),Q(2**50),Q(2**80)),
    (100,5,Q(2**100),Q(1,2**120),Q(2**150),Q(2**200))):
    B=max(2,3**n); Ct=8*(B+1)**2; K=max(1,n*B); rho=Q(1,4*B)
    grow=rho*noise/(2*n); margin=rho*noise/(2*K)
    radius=min(Q(1,8),margin/(16*rowbound)); amp=2+k*curvature/grow
    mesh=Q(1); J=0
    while mesh>min(radius/(4*amp),grow*radius**2/(16*gradient*amp)):
        mesh/=2; J+=1
    M=2
    while M<max(2,2**J,4*n*Ct/rho,2*K/rho):
        M*=2
    assert n*grow/noise+Q(2*n*Ct,M) <= rho
    assert K*(margin/noise+Q(1,M)) <= rho
    assert M*mesh>=1
    assert 4*gradient*amp*mesh <= grow*radius**2/4
    budgets+=1

print(f"PASS: 4 nonconvex-forest closure fixtures; {slab_calls} exact excluded-slab solves; clipped-bound and tied-mode guards; {budgets} finite-law budgets")
