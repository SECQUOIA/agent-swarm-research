"""Recheck of the delta thresholds of Theorems 3.4 and 3.5 (SymPy, exact).

Theorem 3.4: r0^2 = (1-d)^2 - d, R^2 = rho r0^2, rho in (1, 4/3); V = R^n > 1 for some
             admissible rho iff (4/3) r0^2 > 1.  Claimed threshold (3 - sqrt 8)/2.
Theorem 3.5: R^2 = (3/2)(1-d)^2 - d; V_c > 1 iff R^2 > 1.  Claimed (4 - sqrt 13)/3.
Also: the stated ranges (0, 0.08) and (0, 0.1) lie inside the non-vacuous ranges; the
algebra of the proof of Theorem 3.4 (theta, a^2, monotonicity iff rho >= 2/n); the
Theorem 3.5 cap-ball radius a^2 <= (1-d)^2/2; and the exponents 0.2075, 0.2925.
"""
import sympy as sp

d, rho, n, r0 = sp.symbols('delta rho n r0', positive=True)

# Theorem 3.4
g34 = sp.Rational(4, 3) * ((1 - d) ** 2 - d) - 1
roots34 = sp.solve(sp.Eq(g34, 0), d)
t34 = min(roots34, key=lambda r: float(r))
print("Theorem 3.4: (4/3)((1-d)^2 - d) = 1 at d =", roots34, "-> threshold", sp.nsimplify(t34), "=", sp.N(t34, 12))
print("   equals (3 - sqrt 8)/2:", sp.simplify(t34 - (3 - sp.sqrt(8)) / 2) == 0)
print("   at d = 0.08: (4/3) r0^2 =", sp.N(sp.Rational(4, 3) * ((1 - sp.Rational(8, 100)) ** 2 - sp.Rational(8, 100)), 8),
      "> 1, so rho in (1/r0^2, 4/3) is nonempty:", sp.N(1 / ((1 - sp.Rational(8, 100)) ** 2 - sp.Rational(8, 100)), 8), "< 4/3")
print("   (4/3) r0^2 is decreasing in d on (0, 1/2):", sp.simplify(sp.diff((1 - d) ** 2 - d, d)), "< 0")

# Theorem 3.5
g35 = sp.Rational(3, 2) * (1 - d) ** 2 - d - 1
roots35 = sp.solve(sp.Eq(g35, 0), d)
t35 = min(roots35, key=lambda r: float(r))
print("Theorem 3.5: (3/2)(1-d)^2 - d = 1 at d =", roots35, "-> threshold", t35, "=", sp.N(t35, 12))
print("   equals (4 - sqrt 13)/3:", sp.simplify(t35 - (4 - sp.sqrt(13)) / 3) == 0)
print("   at d = 0.1: R^2 =", sp.N(g35.subs(d, sp.Rational(1, 10)) + 1, 8), "> 1")
a2 = (sp.Rational(3, 2) * (1 - d) ** 2 - d) - ((1 - d) ** 2 - d)
print("   cap ball: R^2 - ((1-d)^2 - d) =", sp.factor(a2), "(= (1-d)^2/2)")

# Theorem 3.4 proof algebra
R2 = rho * r0 ** 2
s1sq = 4 * (R2 - r0 ** 2)
one_m_theta = s1sq / (2 * R2)
theta = sp.simplify(1 - one_m_theta)
A = (1 - theta) * R2 + theta * s1sq
b = theta * (1 - theta)
a_sq = sp.simplify(A - b * R2)
print("Theorem 3.4 algebra: 1 - theta =", sp.simplify(one_m_theta), "; theta =", theta,
      "; A - bR^2 =", sp.factor(a_sq), "; equals s1^2 - s1^4/(4R^2):", sp.simplify(a_sq - (s1sq - s1sq ** 2 / (4 * R2))) == 0)
cond = sp.simplify((1 - 1 / n) * a_sq - b * R2)
print("   (1 - 1/n) a^2 - b R^2 =", sp.factor(cond), " -> >= 0 iff rho >= 2/n (rho > 1)")
# monotonicity of r^(n-1) (A - b r^2)^(n/2): derivative sign at r = R
r = sp.symbols('r', positive=True)
deriv_sign = sp.simplify((n - 1) * (A - b * r ** 2) - n * b * r ** 2)
print("   sign of d/dr log(r^(n-1)(A-br^2)^(n/2)) * r (A - b r^2):", sp.factor(deriv_sign), "(decreasing in r, so check r = R)")
print("   at r = R equals n((1-1/n)a^2 - bR^2):", sp.simplify(deriv_sign.subs(r, sp.sqrt(R2)) - n * cond) == 0)
print("   4(rho-1)/rho < 1 iff rho < 4/3:", sp.solve(sp.Lt(4 * (rho - 1) / rho, 1), rho))

print("Exponents: (1/2) log2(4/3) =", sp.N(sp.log(sp.Rational(4, 3), 2) / 2, 8),
      "; (1/2) log2(3/2) =", sp.N(sp.log(sp.Rational(3, 2), 2) / 2, 8))
