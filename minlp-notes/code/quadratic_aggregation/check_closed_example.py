"""Closed-system example: T = {x1 x2 = 1, x1^2 <= x2^2} in R^3 (x3 free).
Constraints: f1 = x1 x2 - 1 <= 0, f2 = -(x1 x2 - 1) <= 0, f3 = x1^2 - x2^2 <= 0.
Checks: (a) all points of T have |x1| <= 1 (so conv T is proper); (b) 0 is interior to conv T
(exhibit four points of T whose hull contains a ball around 0 in the (x1,x2) plane);
(c) every nonnegative aggregation with c_lambda < 0 (needed for 0 in S_lambda) has Q_lambda with
two negative eigenvalues, so the set Omega_T of good aggregations is empty; (d) all PSD
A_lambda are zero (only trivial convex certificates)."""
import numpy as np, itertools
J = np.zeros((3,3)); J[0,1]=J[1,0]=0.5
A = [J, -J, np.diag([1.0,-1.0,0.0])]; b = [np.zeros(3)]*3; c = [-1.0, 1.0, 0.0]
Q = [np.block([[Ai, bi[:,None]],[bi[None,:], np.array([[ci]])]]) for Ai,bi,ci in zip(A,b,c)]
# (a)
for a in np.linspace(-3,3,601):
    if abs(a)<1e-9: continue
    x = np.array([a, 1/a, 0.0])
    if x[0]**2 <= x[1]**2 + 1e-12:
        assert abs(a) <= 1+1e-9
print("(a) every point of T has |x1| <= 1: ok")
# (b) hull of (1,1),(0.5,2),(-1,-1),(-0.5,-2) contains 0 in interior: check 0 is strict convex combination
P = np.array([[1,1],[0.5,2],[-1,-1],[-0.5,-2]])
lam = np.array([0.25,0.25,0.25,0.25]); assert np.allclose(lam@P, 0)
print("(b) 0 is the barycenter of four points of T with affinely spanning (x1,x2): ok")
# (c) sample lambda >= 0 with c_lambda < 0 i.e. lambda2 < lambda1
rng = np.random.default_rng(1); worst = -np.inf
for _ in range(20000):
    l = rng.random(3); 
    if l[1] >= l[0]: l[0], l[1] = l[1], l[0]
    if l[1] == l[0]: continue
    Ql = sum(li*Qi for li,Qi in zip(l,Q)); ev = np.linalg.eigvalsh(Ql)
    worst = max(worst, ev[1])  # second smallest eigenvalue must be < 0
assert worst < 0
print(f"(c) every aggregation with c_lambda < 0 has >= 2 negative eigenvalues (max second-smallest eigenvalue {worst:.3e}): ok")
# (d) PSD A_lambda only when zero: A_lambda = (l1-l2) J + l3 diag(1,-1,0), trace 0
print("(d) trace(A_lambda) = 0 for all lambda, so PSD implies zero: ok (algebraic)")
print("all checks passed")
