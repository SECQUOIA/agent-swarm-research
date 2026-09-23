"""Independent covariance/regression enumeration for Stage 2 review 4."""
from itertools import combinations
from math import comb, ceil
import numpy as np
import sympy as sp

def subsets(n):
    return [tuple(i for i in range(n) if mask >> i & 1) for mask in range(1 << n)]

count = 0
n = 8
ss = subsets(n)
for P, r, a in [(1., 1., .1), (3., .2, .6), (.2, 3., -.9)]:
    R = P * a ** np.abs(np.arange(n)[:, None] - np.arange(n)) + r * np.eye(n)
    for L in range(n):
        residuals = {}
        for S in ss:
            if not S:
                continue
            RR = R[np.ix_(S, S)]
            A = np.eye(len(S))
            for ti, t in enumerate(S):
                H = [j for j, v in enumerate(S) if t-L <= v < t]
                if H:
                    A[ti, H] = -np.linalg.solve(RR[np.ix_(H, H)], RR[H, ti])
            V = A @ RR @ A.T
            d = np.diag(V)
            norm = np.linalg.norm(V / np.sqrt(d[:, None] * d[None, :]) - np.eye(len(S)), 2)
            residuals[S] = V, d, norm
        for g in range(1, n+2):
            b, kappa = abs(a), P/(P+r)
            x = P
            for _ in range(L//g):
                x = P*(1-b**(2*g)) + b**(2*g)*r*x/(r+x)
            floor = r + x
            phi = [0.] * n
            for h in range(g, n):
                phi[h] = P*b**h if h>L else P*kappa*(1-kappa)*b**h*sum(b**(2*d) for d in range(max(g,L+1-h), L+1, g))
            B = [0.] * n
            for M in range(g, n):
                B[M] = max(B[M-1], phi[M] + B[M-g])
                brute = max(sum(phi[d] for d in D) for D in subsets(M+1) if all(d>=g for d in D) and all(y-x>=g for x,y in zip(D,D[1:])))
                assert abs(B[M]-brute) < 1e-10
            delta = max(B[t]+B[n-1-t] for t in range(n))/floor
            for S, (V, d, norm) in residuals.items():
                if any(y-x < g for x,y in zip(S,S[1:])):
                    continue
                assert min(d) >= floor - 1e-10, (P,r,a,L,g,S,d,floor)
                for j in range(len(S)):
                    for i in range(j):
                        assert abs(V[j,i]) <= phi[S[j]-S[i]]+1e-10, (L,g,S,V,phi)
                assert norm <= delta+1e-10, (L,g,S,norm,delta)
                count += 1

for L in range(13):
    for g in range(1,16):
        masks = [S for S in subsets(L) if all(y-x>=g for x,y in zip(S,S[1:]))]
        predicted = 1+sum(comb(L-(g-1)*(q-1),q) for q in range(1,ceil(L/g)+1))
        assert len(masks) == predicted

# Exact nonstationary witness and all printed pivot matrices/determinants.
q = sp.Rational
R = sp.Matrix([[2,q(1,2),q(1,4)],[q(1,2),q(5,4),q(1,8)],[q(1,4),q(1,8),q(17,16)]])
A = sp.Matrix([[1,0,0],[-q(1,4),1,0],[0,-q(1,10),1]])
assert (A*R*A.T)[2,1] == -q(1,20)
R = sp.Matrix([[1,0,q(3,5)],[0,1,q(3,5)],[q(3,5),q(3,5),1]])
ratios = []
for pivots in [(),(0,),(1,),(0,1)]:
    A = sp.eye(3)
    for j in range(3):
        H = [i for i in pivots if i<j]
        if H:
            b = R.extract([j],H)*R.extract(H,H).inv()
            for v,i in enumerate(H): A[j,i] = -b[v]
    V = A*R*A.T
    Q = A.T*sp.diag(*[1/V[j,j] for j in range(3)])*A
    assert sp.trace(Q*R) == 3
    ratios.append(1/(Q.det()*R.det()))
assert ratios == [q(25,7),q(16,7),q(16,7),1]
assert ratios[0]*ratios[3]/(ratios[1]*ratios[2]) == q(175,256)
assert R.det() == q(7,25)
assert R.inv()[0,0] == q(16,7)
assert 16**8 > 25**5 * 7**3

# Random-intercept information, including L=0 and complete-history boundary.
for n in range(1,10):
    R = sp.eye(n) + sp.ones(n)
    assert (sp.ones(1,n)*R.inv()*sp.ones(n,1))[0] == q(n,n+1)
    for L in range(n+1):
        summed = sum(q(1,(min(i,L)+1)*(min(i,L)+2)) for i in range(n))
        assert summed == q(L,L+1)+q(n-L,(L+1)*(L+2))
print(f'PASS: {count} stationary separated schedule/window cases; all row-DP brute comparisons; 195 mask counts; exact stationarity, pivot, and intercept witnesses.')
