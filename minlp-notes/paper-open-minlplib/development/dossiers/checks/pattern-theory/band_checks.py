# Independent checks of the band identity (one separator) and the tree lower
# bound on random finite instances, plus the exact per-edge counterexample.
from fractions import Fraction as Fr
import itertools, random
import numpy as np
from scipy.optimize import linprog

# 1. Proposition 3.3 counterexample, exact rationals on the vertices
#    (F multilinear, so the minimum over [0,1]^2 is at a vertex).
a = lambda s1: 10*(1-s1); c = lambda s2: 10*(1-s2); b = lambda s1,s2: s1+s2-s1*s2
fstar = min(a(s1)+b(s1,s2)+c(s2) for s1 in (0,1) for s2 in (0,1))
rho_const = 0 + 0 + 0  # min a = 0 (s1=1), min b = 0 (s=(0,0)), min c = 0
# V_1(s1) = min_{s2} b + c is affine in s2, coefficient -9-s1 < 0 -> s2 = 1
V1 = lambda s1: b(s1,1)+c(1)
print("Prop 3.3: f* =", fstar, " constant-split bound =", rho_const,
      " V1(0), V1(1/2), V1(1) =", V1(Fr(0)), V1(Fr(1,2)), V1(Fr(1)))

# 2. Band identity on random finite one-separator instances, affine class.
rng = np.random.default_rng(1)
def gap_affine(S, U, L):
    # min_{a,b,t1,t2} t1 + t2 s.t. a+b s - U <= t1, L - a - b s <= t2
    n = len(S); A=[]; ub=[]
    for s,u,l in zip(S,U,L):
        A.append([1, s, -1, 0]); ub.append(u)
        A.append([-1, -s, 0, -1]); ub.append(-l)
    r = linprog([0,0,1,1], A_ub=A, b_ub=ub, bounds=[(None,None)]*4, method="highs")
    return r.fun
def two_dist(S, U, L):
    # min 2 t s.t. |a + b s - psi_s| <= t, L <= psi <= U
    n=len(S); nv = 3+n; A=[]; ub=[]
    for k,s in enumerate(S):
        row=[1,s,-1]+[0]*n; row[3+k]=-1; A.append(row); ub.append(0)
        row=[-1,-s,-1]+[0]*n; row[3+k]=1; A.append(row); ub.append(0)
    bnds=[(None,None)]*3+[(l,u) for l,u in zip(L,U)]
    r = linprog([0,0,2]+[0]*n, A_ub=A, b_ub=ub, bounds=bnds, method="highs")
    return r.fun
worst=0
for trial in range(300):
    n = rng.integers(3,9); S = np.sort(rng.uniform(-1,1,n))
    U = rng.normal(size=n); V = rng.normal(size=n)
    fs = np.min(U+V); L = fs - V
    g1 = gap_affine(S,U,L); g2 = two_dist(S,U,L)
    worst=max(worst,abs(g1-g2))
print("band identity, 300 random 1-separator instances, affine class: max |gap - 2 dist| =", worst)

# 3. Tree lower bound on random 3-bag paths a(s1) - b(s1,s2) - c(s2), affine classes.
def path_gap(S1,S2,A,B,C):
    # variables: p1,q1 (split on s1), p2,q2 (split on s2), ma, mb, mc ; maximize ma+mb+mc
    # bags: a(s1) - (p1+q1 s1) >= ma ; b + (p1+q1 s1) - (p2+q2 s2)... root b, children a, c:
    # F_a^phi = a - phi1, F_c^phi = c - phi2, F_b^phi = b + phi1 + phi2
    Aub=[];bub=[]
    for i,s in enumerate(S1):
        Aub.append([-1,-s,0,0,1,0,0]); bub.append(A[i])
    for j,s in enumerate(S2):
        Aub.append([0,0,-1,-s,0,0,1]); bub.append(C[j])
    for i,s1 in enumerate(S1):
        for j,s2 in enumerate(S2):
            Aub.append([1,s1,1,s2,0,1,0]); bub.append(B[i,j])
    r=linprog([0,0,0,0,-1,-1,-1],A_ub=Aub,b_ub=bub,bounds=[(None,None)]*7,method="highs")
    fstar=min(A[i]+B[i,j]+C[j] for i in range(len(S1)) for j in range(len(S2)))
    return fstar+r.fun, fstar
viol=0; att=0
for trial in range(200):
    n1,n2=rng.integers(3,7,2); S1=np.sort(rng.uniform(-1,1,n1)); S2=np.sort(rng.uniform(-1,1,n2))
    A=rng.normal(size=n1); C=rng.normal(size=n2); B=rng.normal(size=(n1,n2))
    g,fs=path_gap(S1,S2,A,B,C)
    # edge 1: child a, U1 = A, V1(s1) = min_s2 B + C
    U1=A; V1=np.min(B+C[None,:],axis=1); L1=fs-V1
    U2=C; V2=np.min(B+A[:,None],axis=0); L2=fs-V2
    lb=max(two_dist(S1,U1,L1), two_dist(S2,U2,L2))
    if g < lb-1e-7: viol+=1
    if abs(g-lb)<1e-7: att+=1
print("tree lower bound 2 max_e dist <= gap: violations", viol, "of 200; lower end attained in", att)
