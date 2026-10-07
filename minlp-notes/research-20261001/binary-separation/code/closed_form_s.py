"""Closed form of s = delta^T M^-1 delta for two families (note.md, remark after Lemma 5; review r2, item o3).

Family A: n copies of {0,1,2} plus {3,4,5} (p = 6, eta2 = 5/4).  M is positive definite (Lemma 1), so M w = delta
has a unique solution; it is invariant under permutations of the copies, so w = (a, ..., a, b, c).  The three
remaining equations are solved symbolically in n, which gives s(n) for every n >= 1.  The result is compared with
the exact Fraction computation of check_binary_separation.py for several n.

Family B: n singletons {0}, ..., {n-1} with p = n (every set used once in the unique exact cover).  Here the
bound of Lemma 5, 4n + p + 1/(4(p-1)), is nearly attained.
"""
import sys
from fractions import Fraction as F

import sympy as sp

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from check_binary_separation import binary_point, build_M  # noqa: E402

n, a, b, c = sp.symbols("n a b c", positive=True)
# M entries: copies M_ii = 7, M_ij = 3 (i != j), M_iB = 0, M_ig = 3/2; B: M_BB = 7, M_Bg = 3/2; g: M_gg = 11/4.
eqs = [
    sp.Eq(7 * a + 3 * (n - 1) * a + sp.Rational(3, 2) * c, 7),       # row of a copy
    sp.Eq(7 * b + sp.Rational(3, 2) * c, 7),                          # row of {3,4,5}
    sp.Eq(sp.Rational(3, 2) * n * a + sp.Rational(3, 2) * b + sp.Rational(11, 4) * c, sp.Rational(11, 4)),  # row of g
]
sol = sp.solve(eqs, [a, b, c], dict=True)[0]
s_n = sp.factor(sp.simplify(7 * n * sol[a] + 7 * sol[b] + sp.Rational(11, 4) * sol[c]))
limit = sp.limit(s_n, n, sp.oo)
print("Family A: s(n) =", s_n, "; limit n -> oo:", limit, "=", float(limit))
target = sp.Rational(77, 4) * (193 * n + 108) / (141 * n + 272)
print("Family A: equals 77(193n+108)/(4(141n+272)):", sp.simplify(s_n - target) == 0)
ok = True
for nn in (1, 2, 5, 20, 40, 100):
    sets = [(0, 1, 2)] * nn + [(3, 4, 5)]
    _, _, s_exact = binary_point(build_M(sets, 6, F(5, 4)), 6)
    sym = sp.Rational(s_n.subs(n, nn))
    same = F(int(sym.p), int(sym.q)) == s_exact
    ok &= same
    print(f"  n = {nn:3d}: exact s = {s_exact} = {float(s_exact):.4f}; closed form agrees: {same}")
print("Family A: closed form matches the exact computation:", ok)

for nn in (4, 8, 12, 20):
    sets = [(i,) for i in range(nn)]
    _, _, s_exact = binary_point(build_M(sets, nn, F(nn - 1, 4)), nn)
    bound = 4 * nn + nn + F(1, 4 * (nn - 1))
    print(f"Family B: {nn} singletons, p = {nn}: s = {float(s_exact):.4f}, bound = {float(bound):.4f}, "
          f"ratio = {float(s_exact / bound):.5f}")
