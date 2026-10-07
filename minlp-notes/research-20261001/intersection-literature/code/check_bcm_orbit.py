"""Check that the Bienstock-Chen-Munoz sets (14a) (arXiv:1610.04604v7, Lemma 22)
    lam1 (a + d) + lam2 (b - c) >= || (b + c, a - d) ||_2,   lam = (cos t, -sin t),
are exactly the sets {M = [[a, b], [c, d]] : sym(G_t M) is PSD} with G_t the rotation
[[cos t, sin t], [-sin t, cos t]], i.e. the members of the orbit family
C_F = {M : sym(F^T M) PSD} of the sfree note (Lemma 10) with F^T = G_t in SO(2).

Part 1 (exact, sympy): trace and the norm of the traceless part of sym(G_t M) equal
the two sides of (14a).  A symmetric 2x2 matrix is PSD iff trace >= norm of
(diag difference, 2 * offdiag), so the two descriptions coincide.
Part 2 (random): 20000 random (M, t) agree on membership.
Part 3 (exact): F^T = diag(2, 1/2) (det 1) gives an orbit set that is neither a (14a) nor a (14b)
set.  This is one witness only; it illustrates, but does not prove, the general claim.
Part 4 (exact, sympy): the two algebraic facts behind the general proof in the note (Prop. B):
  (a) for invertible A, the linear map M -> sym(A M) has rank 3 (all 3x3 minors are
      +-(entry of A) * det(A)/2), and A^{-1} J lies in its kernel; so the lineality space
      of C_A = {M : sym(A M) PSD} is span(A^{-1} J), J = [[0, 1], [-1, 0]];
  (b) det(S + k J) = det(S) + k^2 for symmetric 2x2 S, so sym(N) positive definite implies
      det N > 0.
(Revised after review round 1: Part 3's printed conclusion no longer claims generality.)
"""
import numpy as np
import sympy as sp

a, b, c, d, t = sp.symbols('a b c d t', real=True)
M = sp.Matrix([[a, b], [c, d]])
G = sp.Matrix([[sp.cos(t), sp.sin(t)], [-sp.sin(t), sp.cos(t)]])
S = (G * M + (G * M).T) / 2
tr = sp.simplify(S.trace())
diff = sp.simplify(S[0, 0] - S[1, 1])
off2 = sp.simplify(2 * S[0, 1])
lhs = sp.cos(t) * (a + d) - sp.sin(t) * (b - c)
ok1 = sp.simplify(tr - (sp.cos(t) * (a + d) + sp.sin(t) * (c - b))) == 0
ok2 = sp.simplify(diff**2 + off2**2 - ((b + c)**2 + (a - d)**2)) == 0
print("Part 1: trace(sym(G_t M)) = cos t (a+d) + sin t (c-b):", ok1)
print("Part 1: |traceless part|^2 = (b+c)^2 + (a-d)^2:", ok2)

rng = np.random.default_rng(0)
bad = 0
for _ in range(20000):
    Mn = rng.normal(size=(2, 2)); tt = rng.uniform(0, 2 * np.pi)
    Gn = np.array([[np.cos(tt), np.sin(tt)], [-np.sin(tt), np.cos(tt)]])
    Sn = (Gn @ Mn + (Gn @ Mn).T) / 2
    psd = np.linalg.eigvalsh(Sn).min() >= 0
    l1, l2 = np.cos(tt), -np.sin(tt)
    A, B, C, D = Mn[0, 0], Mn[0, 1], Mn[1, 0], Mn[1, 1]
    in14a = l1 * (A + D) + l2 * (B - C) >= np.hypot(B + C, A - D)
    bad += (psd != in14a)
print("Part 2: disagreements in 20000 random tests:", bad)

# Part 3: F^T = diag(2, 1/2) (det F = 1).  Every (14a) set is invariant under
# (b, c) -> (-c, -b) (b - c and |b + c| are unchanged); C_F is not.
FT = sp.diag(2, sp.Rational(1, 2))
S3 = (FT * M + (FT * M).T) / 2
print("Part 3: sym(F^T M) for F^T = diag(2,1/2):", S3.tolist())
def in_CF(Mt):
    St = (FT * Mt + (FT * Mt).T) / 2
    return St.trace() > 0 and St.det() > 0, St.det()
M1 = sp.Matrix([[1, 0], [3, 1]]); M2 = sp.Matrix([[1, -3], [0, 1]])
r1, r2 = in_CF(M1), in_CF(M2)
print("  M1 =", M1.tolist(), "in int C_F:", r1[0], "det sym =", r1[1])
print("  M2 =", M2.tolist(), "in int C_F:", r2[0], "det sym =", r2[1])
# (14b): lam1 (b + c) + lam2 (a - d) >= |(a + d, b - c)|; for M1: b + c = 3, a - d = 0,
# |(a + d, b - c)| = sqrt(13) > 3 >= lam1 * 3, so M1 lies in no (14b) set.
print("  M1 in some (14b) set:", 3 >= sp.sqrt(13))
print("Part 3 conclusion (this F only): C_F is neither a (14a) nor a (14b) set:",
      r1[0] and not r2[0] and not (3 >= sp.sqrt(13)))

# Part 4 (general facts used in the proof of Proposition B).
import itertools
p, q, r, s, k = sp.symbols('p q r s k', real=True)
A = sp.Matrix([[p, q], [r, s]])
SA = (A * M + (A * M).T) / 2
Lmap = sp.Matrix([[sp.diff(e, v) for v in (a, b, c, d)] for e in (SA[0, 0], SA[0, 1], SA[1, 1])])
minors = [sp.factor(Lmap[:, list(cols)].det()) for cols in itertools.combinations(range(4), 3)]
print("Part 4(a): 3x3 minors of M -> sym(AM):", minors)
detA = A.det()
ok_minors = all(sp.simplify(m / detA) in (-r / 2, p / 2, s / 2, -q / 2) for m in minors)
J = sp.Matrix([[0, 1], [-1, 0]])
K = A.inv() * J
symAK = sp.simplify((A * K + (A * K).T) / 2)
print("Part 4(a): minors = (entry of A) * det(A) / 2:", ok_minors, "; sym(A A^{-1} J) = 0:", symAK == sp.zeros(2, 2))
x, y, z = sp.symbols('x y z', real=True)
Ssym = sp.Matrix([[x, y], [y, z]])
print("Part 4(b): det(S + kJ) - det(S) - k^2 =", sp.expand((Ssym + k * J).det() - Ssym.det() - k**2))
