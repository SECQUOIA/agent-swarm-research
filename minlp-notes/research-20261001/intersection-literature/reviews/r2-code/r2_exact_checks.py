"""Reviewer r2: independent exact checks (fractions only, plus numpy for random tests).
Covers: Theorem 14 corner facts used in note Section 4.4; the two Cor. 3.12 counterexamples
(Claim 4.4a); Proposition B parts (2)-(3) (general claims, random tests + exact minors);
Proposition A part (2) halfspace argument (sampled)."""
from fractions import Fraction as Fr
import itertools, math
import numpy as np

def sub(u, v): return tuple(a - b for a, b in zip(u, v))
def add(u, v): return tuple(a + b for a, b in zip(u, v))
def mul(s, u): return tuple(s * a for a in u)
def dot(u, v): return sum(a * b for a, b in zip(u, v))
def cross(u, v): return (u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0])
def solve3(cols, rhs):
    # Cramer's rule, exact
    def det3(a, b, c): return dot(a, cross(b, c))
    D = det3(*cols)
    return tuple(det3(*[rhs if k == i else cols[k] for k in range(3)]) / D for i in range(3))

print("== Theorem 14 corner")
sbar = (Fr(-9, 2), Fr(0), Fr(3, 2))
V = [(Fr(-1), Fr(-6), Fr(18)), (Fr(-5), Fr(6), Fr(-18)), (Fr(0), Fr(5, 2), Fr(5, 2))]
P = [sub(v, sbar) for v in V]
q = lambda s: s[2] - s[0] * s[1]
grad = lambda s: (-s[1], -s[0], Fr(1))
t = mul(Fr(1, 2), add(V[0], V[1]))
lam = solve3(P, sub(t, sbar))
print("t* =", t, "q(t*) =", q(t), "lambda =", lam, "cost =", sum(lam))
n = cross(P[0], P[1])
if dot(n, P[2]) > 0: n = mul(-1, n)
print("n =", n, "n.p1 =", dot(n, P[0]), "n.p2 =", dot(n, P[1]), "n.p3 =", dot(n, P[2]))
# q(t*+eps n) is a quadratic in eps; recover coefficients from 3 exact evaluations
vals = [q(add(t, mul(Fr(e), n))) for e in (0, 1, 2)]
c0 = vals[0]; c2 = (vals[2] - 2 * vals[1] + vals[0]) / 2; c1 = vals[1] - c0 - c2
print("q(t*+eps n) = %s + %s eps + %s eps^2  (note: 18 eps(-60 eps - 11) = -198 eps - 1080 eps^2)" % (c0, c1, c2))
for e in (Fr(1, 10), Fr(1, 10**4), Fr(1, 10**8)):
    pt = add(t, mul(e, n)); l = solve3(P, sub(pt, sbar))
    assert q(pt) < 0 and min(l) < 0
print("q<0 and a negative barycentric coordinate at eps = 1e-1, 1e-4, 1e-8: OK")
seg = [q(add(sbar, mul(Fr(k, 10), sub(t, sbar)))) for k in range(11)]
print("q(sbar + tau(t*-sbar)), tau=0..1 step 1/10:", seg, "(3/2(1-tau)?)",
      all(seg[k] == Fr(3, 2) * (1 - Fr(k, 10)) for k in range(11)))
print("grad q(t*).(sbar - t*) =", dot(grad(t), sub(sbar, t)))

print("== Claim 4.4a, counterexample 1 (KY Ex. 4.3), D2 = {(1/2,0)}")
# exact lower bound on squared distance from (1/2,0) to (1 - 1/sqrt n, -1/n), n = 1..10^5 (float check)
dmin = min(math.hypot(1 - 1/math.sqrt(k) - 0.5, -1/k) for k in range(1, 10**5 + 1))
print("min distance over n <= 1e5:", round(dmin, 6), ">= 1/8:", dmin >= 0.125)
print("== Counterexample 2 (Prop 2(b)), D2 = {(1/2,0),(0,1/2)}")
qq = lambda l: l[0] - l[0]**2 + (1 - l[1])**2
print("q(1/2,0) =", qq((Fr(1, 2), Fr(0))), " q(0,1/2) =", qq((Fr(0), Fr(1, 2))), " q(0,0) =", qq((Fr(0), Fr(0))))
# ray e1 is a limit ray of B2: points (T, -1/T) in B for large T
for T in (Fr(10), Fr(100), Fr(10**4)):
    assert qq((T, -1 / T)) < 0
print("(T,-1/T) in B2 for T = 10, 100, 1e4 (directions -> e1): OK")
for s in (Fr(1, 10), Fr(1, 1000)):
    assert qq((-s * s, 1 - s)) == -s**4
print("(-s^2, 1-s) in B2 with q = -s^4: OK")
# z_K = 1 for w = (1,1): brute force over a rational grid of lambda >= 0 with sum < 1 -> q > 0
bad = 0
for i in range(0, 200):
    for j in range(0, 200 - i):
        l = (Fr(i, 200), Fr(j, 200))
        if sum(l) < 1 and qq(l) <= 0: bad += 1
print("grid points with sum<1 and q<=0:", bad)

print("== Proposition B (general claims), random tests")
rng = np.random.default_rng(7)
J = np.array([[0., 1.], [-1., 0.]])
def sym(N): return (N + N.T) / 2
# (3): det F > 0 and sym(F^T M) > 0  =>  det M > 0
viol3 = 0
for _ in range(20000):
    F = rng.normal(size=(2, 2))
    if np.linalg.det(F) <= 0: F[:, 0] *= -1
    M = rng.normal(size=(2, 2))
    if np.linalg.eigvalsh(sym(F.T @ M)).min() > 1e-9 and np.linalg.det(M) <= 0: viol3 += 1
print("violations of (sym(F^T M) PD & det F>0 => det M>0):", viol3)
# (2): for F not a multiple of a rotation, exhibit M in C_F not in C'_G for G the rotation
# with the same lineality-space direction is impossible, i.e. lineality spaces differ for all G:
# lineality of C'_A is span(A^{-1}J); for a rotation G it is span(G^{-1}J) = span(G^T J).
# A^{-1}J parallel to G^T J iff A^{-1} parallel to G^T iff A parallel to G.
mx = 0
for _ in range(2000):
    A = rng.normal(size=(2, 2))
    L = np.linalg.inv(A) @ J
    # check kernel of M -> sym(AM) is spanned by L
    assert np.allclose(sym(A @ L), 0)
    Lmat = np.array([sym(A @ E).ravel()[[0, 1, 3]] for E in np.eye(4).reshape(4, 2, 2)]).T
    mx = max(mx, abs(np.linalg.matrix_rank(Lmat) - 3))
print("rank of M -> sym(AM) is 3 for 2000 random A:", mx == 0)
# Example in the note
FT = np.array([[2, 0], [0, .5]]); M1 = np.array([[1., 0], [3, 1]]); M2 = np.array([[1., -3], [0, 1]])
print("det sym(F^T M1), det sym(F^T M2):", np.linalg.det(sym(FT @ M1)), np.linalg.det(sym(FT @ M2)))

print("== Proposition A part (2): {w <= xy} in no closed halfspace (sampled a)")
worst = -np.inf
for _ in range(2000):
    a = rng.normal(size=3)
    if a[2] > 0: pt = lambda s: np.array([0, 0, -s])
    elif a[2] < 0: pt = lambda s: np.array([s, s, s * s])
    else: pt = lambda s: np.array([-s * a[0], -s * a[1], s * s * a[0] * a[1]])
    worst = max(worst, a @ pt(1e4))
print("max over sampled a of a.(point at s=1e4):", worst, "(should be very negative)")
