"""Exact check: at the Theorem 14 corner of the sfree note, points of S outside the
cone sbar + cone(P) accumulate at the corner minimizer t*, so the strict condition
(iii) of Kilinc-Karzan-Yang (draft 2017, Prop. 3.11 / Cor. 3.12 in the corrected reading of
note Section 4.4: the ray of each D_2 point must avoid cl(B_2)) fails there
(sigma_{D_c}(t* - sbar) = 1 with c = w / z_K), while Theorem 1(4) of the sfree note
still gives attainment of the corner bound.
S = {(x, y, w) : w - x y <= 0}, sbar = (-9/2, 0, 3/2), v1 = (-1,-6,18), v2 = (-5,6,-18),
v3 = (0,5/2,5/2), weights w = (1,1,1), z_K = 1, t* = (v1 + v2)/2 = (-3, 0, 0)."""
from sympy import Matrix, Rational as R, symbols, simplify
sbar = Matrix([R(-9, 2), 0, R(3, 2)])
V = [Matrix([-1, -6, 18]), Matrix([-5, 6, -18]), Matrix([0, R(5, 2), R(5, 2)])]
P = Matrix.hstack(*[v - sbar for v in V])
q = lambda s: s[2] - s[0] * s[1]
grad = lambda s: Matrix([-s[1], -s[0], 1])
t = (V[0] + V[1]) / 2
print("t* =", list(t), " q(t*) =", q(t), " grad q(t*) =", list(grad(t)))
lam = P.solve(t - sbar)
print("lambda(t*) =", list(lam), " cost w^T lambda =", sum(lam), "(= z_K = 1 => sigma_{D_c}(t*-sbar) = 1)")
n = P[:, 0].cross(P[:, 1])
if n.dot(P[:, 2]) > 0:
    n = -n                      # outward normal of the face cone{p1, p2}
print("outward normal n of face {p1,p2}:", list(n), " grad q . n =", grad(t).dot(n))
eps = symbols('eps', positive=True)
qq = simplify(q(t + eps * n))
print("q(t* + eps n) =", qq, "  (negative for small eps > 0 => points of int S just outside the cone)")
for e in [R(1, 10**3), R(1, 10**6)]:
    pt = t + e * n
    lam_pt = P.solve(pt - sbar)
    print("  eps =", e, " q =", q(pt), " min lambda coordinate =", min(lam_pt), "(< 0: outside the cone)")
tau = symbols('tau', real=True)
print("q(sbar + tau (t* - sbar)) =", simplify(q(sbar + tau * (t - sbar))),
      "(> 0 for tau < 1: t* - sbar is the first point of its ray in S, hence the only admissible D_1 point)")
print("Theorem 1(4) hypothesis: grad q(t*) . (sbar - t*) =", grad(t).dot(sbar - t), "(> 0)")
