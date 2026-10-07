"""Independent exact checks for robust-chains.md (reviewer's code; sympy / Fractions).

1. Prop C.1 / C.4 identities (m = 1..4) and the end brackets.
2. Prop C.2 two-point family: exact consistency and value (Fractions) at the two parameter points.
3. Continuum optimality of the two-point family for the per-bond P_1 / P_2 LP (new): with
   c1 = -(g-ev)(3g+ev)/(8g), s = x+y, d = x-y,
      W(x,y) + c1 (x - y) + g_inf = g (d/2 + 1)(d/2 - q)^2 + s^2 (b/2 + ev/4 - g d/8),
   so W + c1(x-y) >= -g_inf on [-1,1]^2 whenever g <= 2b (+ev); this is a linear (P_1) shift.
   Consequence for the n-chain: P_1 and P_2 root gaps <= (n-1) g_inf + c1^2/a.
4. Degree-3 sparse Putinar certificate of f_n >= 0 with multipliers (1+y), (1-x), (1 +- t):
   shows that the order-2 sparse moment-SOS relaxation (pair cliques, linear box constraints) is exact.
"""
import sympy as sp
from fractions import Fraction as Fr

x, y, b, g, ev, t, p = sp.symbols("x y b g ev t p", real=True)
a = b + ev


def W(m=1):
    return sp.Rational(1, 2) * a * (x**2 + y**2) + b * x * y + g / 2 * (x * y**(2 * m) - x**(2 * m) * y)


print("1. identities")
for m in (1, 2, 3, 4):
    h = lambda s: -g / 2 * s**(2 * m + 1)
    S = sum(x**(2 * j) * y**(2 * (m - 1 - j)) for j in range(m))
    rhs = (x + y)**2 * (b / 2 + g / 2 * (y - x) * S) + ev / 2 * (x**2 + y**2)
    print(f"   m={m}: W + h(x) - h(y) - rhs = {sp.expand(W(m) + h(x) - h(y) - rhs)}")
h = lambda s: -g / 2 * s**3
print("   end brackets:", sp.factor(a / 2 * t**2 - h(t)), "|", sp.factor(a / 2 * t**2 + h(t)))
# telescoping: f_n = sum_e [W + h(x_e) - h(x_{e+1})] + [a/2 x1^2 - h(x1)] + [a/2 xn^2 + h(xn)]
n = 5
xs = sp.symbols("x1:%d" % (n + 1), real=True)
fn = sum(a * xi**2 for xi in xs) + sum(b * xs[i] * xs[i + 1] + g / 2 * xs[i] * xs[i + 1] * (xs[i + 1] - xs[i]) for i in range(n - 1))
tele = sum(W().subs({x: xs[i], y: xs[i + 1]}, simultaneous=True) + h(xs[i]) - h(xs[i + 1]) for i in range(n - 1)) \
    + (a / 2 * xs[0]**2 - h(xs[0])) + (a / 2 * xs[-1]**2 + h(xs[-1]))
print("   telescoping (n=5): f_n - sum of brackets =", sp.expand(fn - tele))
fW = sum(W().subs({x: xs[i], y: xs[i + 1]}, simultaneous=True) for i in range(n - 1)) + a / 2 * (xs[0]**2 + xs[-1]**2)
print("   f_n = sum W + (a/2)(x1^2+xn^2):", sp.expand(fn - fW) == 0)

print("2. two-point family (exact rationals)")
for (B, Gm, EV) in [(Fr(3, 5), Fr(3, 10), Fr(1, 20)), (Fr(3, 5), Fr(3, 10), Fr(1, 10))]:
    A = B + EV
    q = (Gm - EV) / (2 * Gm)
    law = [(Fr(-1), q / (1 + q)), (q, 1 / (1 + q))]       # law of p (x-marginal); y = -p
    mom = lambda k, sgn: sum(w * (sgn * v)**k for v, w in law)
    Wv = lambda u, v: A / 2 * (u * u + v * v) + B * u * v + Gm / 2 * (u * v * v - u * u * v)
    val = sum(w * Wv(v, -v) for v, w in law)
    ginf = (Gm - EV)**2 / (4 * Gm)
    print(f"   b={B} g={Gm} ev={EV}: q={q}; moments of p: {[mom(k, 1) for k in range(4)]}; of -p: {[mom(k, -1) for k in range(4)]};"
          f" E W = {val} = -g_inf ({-ginf}); end term a E p^2 = {A * mom(2, 1)} = a q ({A * q}); g_inf as float {float(ginf):.6f}")

print("3. continuum dual certificate for the per-bond LP")
q = (g - ev) / (2 * g)
ginf = (g - ev)**2 / (4 * g)
c1 = -(g - ev) * (3 * g + ev) / (8 * g)
s, d = x + y, x - y
lhs = W() + c1 * (x - y) + ginf
rhs = g * (d / 2 + 1) * (d / 2 - q)**2 + s**2 * (b / 2 + ev / 4 - g * d / 8)
print("   W + c1 (x-y) + g_inf - [g (d/2+1)(d/2-q)^2 + s^2 (b/2 + ev/4 - g d/8)] =", sp.simplify(sp.expand(lhs - rhs)))
print("   c1 at (0.6,0.3,0.05):", sp.nsimplify(c1.subs({b: sp.Rational(3, 5), g: sp.Rational(3, 10), ev: sp.Rational(1, 20)})),
      "; c1^2/a =", float((c1**2 / a).subs({b: 0.6, g: 0.3, ev: 0.05})))
# end factors with the linear split r_i = -c1 x_i at every interior variable:
#   first factor W(x1,x2) + a/2 x1^2 + c1 (x1 - x2) - c1 x1  ->  >= -g_inf + min_t (a/2 t^2 - c1 t) = -g_inf - c1^2/(2a)
print("   => P_1 and P_2 root gaps of the n-chain lie in [(n-1) g_inf - a q, (n-1) g_inf + c1^2/a]")

print("4. sparse Putinar certificate (degree <= 3 products)")
br = (x + y)**2 * (b / 2 + g / 2 * (y - x)) + ev / 2 * (x**2 + y**2)
cert = ((b / 2 - g) * (x + y)**2 + ev / 2 * (x**2 + y**2)) + (g / 2) * (x + y)**2 * (1 + y) + (g / 2) * (x + y)**2 * (1 - x)
print("   bracket - [sigma0 + sigma1 (1+y) + sigma2 (1-x)] =", sp.expand(br - cert), " (sigma0 SOS iff g <= b/2)")
print("   ends: a/2 t^2 + g/2 t^3 - [(a-g)/2 t^2 + g/2 t^2 (1+t)] =", sp.expand(a / 2 * t**2 + g / 2 * t**3 - ((a - g) / 2 * t**2 + g / 2 * t**2 * (1 + t))))
