"""Independent exact checks by the round-2 confirmation reviewer (second reviewer, r2b).
Uses only fractions and sympy; no code shared with the stream's scripts or with r2_exact_checks.py.
"""
from fractions import Fraction as Fr
import sympy as sp

print("== 1. Theorem 14 corner (q = w - x y) ==")
sbar = [Fr(-9, 2), Fr(0), Fr(3, 2)]
V = [[Fr(-1), Fr(-6), Fr(18)], [Fr(-5), Fr(6), Fr(-18)], [Fr(0), Fr(5, 2), Fr(5, 2)]]
P = [[V[j][i] - sbar[i] for j in range(3)] for i in range(3)]  # columns p_j
q = lambda s: s[2] - s[0] * s[1]
def solve3(M, b):  # Cramer's rule, exact
    d = sp.Matrix(M).det()
    out = []
    for k in range(3):
        Mk = [row[:] for row in M]
        for i in range(3):
            Mk[i][k] = b[i]
        out.append(Fr(str(sp.Matrix(Mk).det() / d)))
    return out
t = [(V[0][i] + V[1][i]) / 2 for i in range(3)]
lam = solve3(P, [t[i] - sbar[i] for i in range(3)])
print("t* =", t, "q(t*) =", q(t), "lambda =", lam, "cost =", sum(lam))
# direction leaving the cone through face {p1,p2}: use -p3 projected? use n = any vector with lambda_3 < 0
g = [-t[1], -t[0], Fr(1)]
print("grad q(t*) =", g, " grad.(sbar - t*) =", sum(g[i] * (sbar[i] - t[i]) for i in range(3)))
# note's normal n = (-18,-60,-18)
n = [Fr(-18), Fr(-60), Fr(-18)]
print("n.p1, n.p2, n.p3 =", [sum(n[i] * P[i][j] for i in range(3)) for j in range(3)])
for e in [Fr(1, 10), Fr(1, 10**4), Fr(1, 10**8)]:
    pt = [t[i] + e * n[i] for i in range(3)]
    l = solve3(P, [pt[i] - sbar[i] for i in range(3)])
    print(f"  eps={e}: q={q(pt)} formula 18e(-60e-11)={18*e*(-60*e-11)} lambda={[str(x) for x in l]}")
for k in range(0, 11):
    tau = Fr(k, 10)
    pt = [sbar[i] + tau * (t[i] - sbar[i]) for i in range(3)]
    assert q(pt) == Fr(3, 2) * (1 - tau)
print("  q(sbar + tau(t*-sbar)) = 3(1-tau)/2 at tau = 0, 0.1, ..., 1: OK")

print("== 2. Infinite case scaling (Remark 4.4) ==")
# cgf rho with rho(p_j) <= c_j = M w_j gives gauge(p_j) <= M w_j, alpha_j >= 1/(M w_j), w_j alpha_j >= 1/M.
Mval, w = Fr(5), [Fr(1), Fr(2)]
alphas = [1 / (Mval * wj) for wj in w]
print("  c = M w with M = 5: min_j w_j alpha_j =", min(w[j] * alphas[j] for j in range(2)),
      "(= 1/M, not M); with c = w/M: ", min(w[j] * (Mval / w[j]) for j in range(2)))

print("== 3. Proposition B identities (symbolic) ==")
a, b, c, d, p, r, s2, k, tt = sp.symbols('a b c d p r s2 k t', real=True)
A = sp.Matrix(2, 2, sp.symbols('A0:4', real=True))
J = sp.Matrix([[0, 1], [-1, 0]])
M = sp.Matrix([[a, b], [c, d]])
sym = lambda X: (X + X.T) / 2
# lineality: solutions of sym(A M) = 0
sol = sp.solve(list(sym(A * M)), [a, b, c, d], dict=True)
Ainv_J = A.inv() * J
if sol:
    Ms = M.subs(sol[0])
    free = [x for x in (a, b, c, d) if x not in sol[0]]
    print("  sym(AM)=0 solution free params:", free)
    # check Ms is a multiple of A^{-1}J
    cross = [sp.simplify(Ms[i] * Ainv_J[j] - Ms[j] * Ainv_J[i]) for i in range(4) for j in range(4)]
    print("  solution parallel to A^{-1}J:", all(x == 0 for x in cross))
S = sp.Matrix([[p, s2], [s2, r]])
print("  det(S + kJ) - det S - k^2 =", sp.expand((S + k * J).det() - S.det() - k**2))
G = sp.Matrix([[sp.cos(tt), sp.sin(tt)], [-sp.sin(tt), sp.cos(tt)]])
X = sym(G * M)
trace = sp.simplify(X.trace() - (sp.cos(tt) * (a + d) - sp.sin(tt) * (b - c)))
normsq = sp.simplify((X[0, 0] - X[1, 1])**2 + (2 * X[0, 1])**2 - ((b + c)**2 + (a - d)**2))
print("  (14a) trace identity:", trace, " traceless norm identity:", normsq)
print("  ||(b+c,a-d)||^2 - ||(a+d,b-c)||^2 - 4(bc-ad) =",
      sp.expand((b + c)**2 + (a - d)**2 - (a + d)**2 - (b - c)**2 - 4 * (b * c - a * d)))
# surjectivity of M -> sym(AM): rank of 3x4 matrix
L = sp.Matrix([[sp.diff(e, x) for x in (a, b, c, d)] for e in (sym(A * M)[0, 0], sym(A * M)[0, 1], sym(A * M)[1, 1])])
minors = [sp.factor(L[:, [i for i in range(4) if i != j]].det()) for j in range(4)]
print("  3x3 minors of M -> sym(AM):", minors)
F = sp.Matrix([[2, 0], [0, sp.Rational(1, 2)]])  # F^T = diag(2,1/2)
M1 = sp.Matrix([[1, 0], [3, 1]]); M2 = sp.Matrix([[1, -3], [0, 1]])
print("  det sym(F^T M1), det sym(F^T M2) =", sym(F.T * M1).det(), sym(F.T * M2).det(),
      " tr sym(F^T M1) =", sym(F.T * M1).trace())

print("== 4. Counterexamples to printed KY Cor. 3.12 ==")
qq = lambda l: l[0] - l[0]**2 + (1 - l[1])**2
print("  Prop 2(b): q(1/2,0) =", qq((Fr(1, 2), Fr(0))), " q(0,1/2) =", qq((Fr(0), Fr(1, 2))))
for T in [Fr(10), Fr(1000)]:
    print(f"  q(T, -1/T) at T={T}: {qq((T, -1/T))} (<0: e_1 axis is a limit ray of B_2)")
# z_K = 1 for Prop 2(b): minimize l1 + l2 over l >= 0, q <= 0 on the branch l1 >= 1
x = sp.symbols('x', positive=True)
f = x + 1 - sp.sqrt(x**2 - x)
print("  branch l1>=1 (l2 = 1 - sqrt(l1^2-l1) >= 0): f(1) =", f.subs(x, 1),
      " f(golden) =", sp.nsimplify(sp.simplify(f.subs(x, (1 + sp.sqrt(5)) / 2))),
      " f' < 0 on (1, golden):", sp.simplify(sp.diff(f, x).subs(x, sp.Rational(3, 2))) < 0)
# KY Ex 4.3: distance of (1/2,0) to B_2 points, exact lower bound by cases
mins = []
for nn in range(1, 200):
    bn1 = 1 - 1 / sp.sqrt(nn); bn2 = -sp.Rational(1, nn)
    mins.append(sp.sqrt((bn1 - sp.Rational(1, 2))**2 + bn2**2))
print("  KY Ex 4.3: min distance of (1/2,0) to b_n, n<200 =", float(min(mins)), "(>= 1/8 claimed)")
