"""Independent symbolic verification of new Stage 1 correction claims."""
import sympy as s

A, k1, k2, t = s.symbols("A k1 k2 t", positive=True)
mean = A*k1*(s.exp(-k1*t)-s.exp(-k2*t))/(k2-k1)
variables = (A, k1, k2)
sensitivities = s.Matrix([mean]).jacobian(variables)
F = s.Matrix.vstack(*[
    sensitivities.subs({A: 1, k1: 1, k2: 2, t: j*s.log(2)}).applyfunc(s.simplify)
    for j in range(1, 4)
])
determinant = s.factor(F.det())
assert determinant == -s.log(2)**2/2048
assert s.simplify(mean-mean.subs({A:A*k1/k2, k1:k2, k2:k1}, simultaneous=True)) == 0
print("PASS: differentiate mean before substitution; ordered determinant =", determinant)
print("PASS: rate swap preserves the entire mean trajectory")

J = s.Matrix([[2,1],[1,2]])
assert J.inv()[0,0] == s.Rational(2,3)
assert 1/J[0,0] == s.Rational(1,2)
assert 1/(J[0,0]-J[0,1]*J[1,0]/J[1,1]) == J.inv()[0,0]
print("PASS: nuisance-adjusted inverse agrees with contrast covariance; compression differs")

alpha = s.Rational(16,7)
u = s.symbols("u", positive=True)
assert s.limit(1/u, u, alpha, dir="-") == 1/alpha
assert s.limit(s.log(u), u, alpha, dir="-") == s.log(alpha)
assert s.diff(1/u,u) < 0 and s.diff(s.log(u),u) > 0
print("PASS: efficiency decreases to its infimum; log loss increases to its supremum")
