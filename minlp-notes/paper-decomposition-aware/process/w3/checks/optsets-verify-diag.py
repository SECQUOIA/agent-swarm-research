"""Verifier check: Remark rem:shor example and Proposition prop:sshard (H+Lambda = H_sq,
box KKT, optimal set) on small instances, exact arithmetic (sympy).
Run: python3 -B optsets-verify-diag.py
"""
import sympy as sp, itertools
ok = True
# rem:shor: F=(x-y+t/2)^2 + t(1-t)/8 on [0,1]^3
x, y, t = sp.symbols('x y t'); V = [x, y, t]
F = (x - y + t / 2) ** 2 + sp.Rational(1, 8) * t * (1 - t)
H = sp.hessian(F, V)
ok &= [H[i, i] for i in range(3)] == [2, 2, sp.Rational(1, 4)]
for pt in [(0, 0, 0), (sp.Rational(1, 3),) * 2 + (0,), (1, 1, 0), (0, sp.Rational(1, 2), 1), (sp.Rational(1, 2), 1, 1)]:
    sub = dict(zip(V, pt)); g = [sp.diff(F, v).subs(sub) for v in V]
    ok &= F.subs(sub) == 0
    lam = [2 * abs(gi) for gi in g]   # widths are 1
    # KKT signs
    for i in range(3):
        if pt[i] == 0: ok &= g[i] >= 0
        elif pt[i] == 1: ok &= g[i] <= 0
        else: ok &= g[i] == 0
    ok &= lam == [0, 0, sp.Rational(1, 4)]
a = sp.Matrix([1, -1, sp.Rational(1, 2)])
ok &= (H + sp.diag(0, 0, sp.Rational(1, 4))) == 2 * a * a.T
print("rem:shor ok" if ok else "rem:shor FAIL")
# prop:sshard on a = (3,-2,5), a0 = 3 (solutions: {3}, {-2,5}); m=3
avals = [3, -2, 5]; a0 = 3; m = 3; A = sum(abs(v) for v in avals)
xs = sp.symbols('x1:4'); xis = sp.symbols('xi1:4')
xi = [0] + list(xis)
F = sum((xi[i] - xi[i - 1] - avals[i - 1] * xs[i - 1]) ** 2 for i in range(1, m + 1)) + (xi[m] - a0) ** 2 \
    + sum(xs[i] * (1 - xs[i]) for i in range(m))
V = list(xs) + list(xis); H = sp.hessian(F, V)
Phi = sum((xi[i] - xi[i - 1] - avals[i - 1] * xs[i - 1]) ** 2 for i in range(1, m + 1)) + (xi[m] - a0) ** 2
Hsq = sp.hessian(Phi, V)
nsol = 0
for xb in itertools.product([0, 1], repeat=m):
    if sum(avals[i] * xb[i] for i in range(m)) != a0: continue
    nsol += 1
    ps = [sum(avals[k] * xb[k] for k in range(i)) for i in range(1, m + 1)]
    sub = dict(zip(V, list(xb) + ps)); ok &= F.subs(sub) == 0
    g = [sp.diff(F, v).subs(sub) for v in V]
    lo = [0] * m + [-A] * m; hi = [1] * m + [A] * m
    lam = [2 * abs(g[i]) / (hi[i] - lo[i]) for i in range(2 * m)]
    for i in range(2 * m):
        val = sub[V[i]]
        if val == lo[i]: ok &= g[i] >= 0
        elif val == hi[i]: ok &= g[i] <= 0
        else: ok &= g[i] == 0
    ok &= lam == [2] * m + [0] * m
    M = H + sp.diag(*lam); ok &= M == Hsq
    ok &= M.is_positive_semidefinite
print("sshard: solutions", nsol, "H+Lambda = H_sq PSD:", ok)
print("ALL PASS" if ok else "FAIL")
