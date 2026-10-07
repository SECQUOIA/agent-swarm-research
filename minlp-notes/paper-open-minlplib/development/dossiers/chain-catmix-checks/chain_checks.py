"""Dossier checks for the chain certificate: (1) sympy identities behind the calibration lemma,
(2) symbolic gradient of B vs the formula used in both B&B codes, (3) random/adversarial
mpmath test of the lemma, (4) B at the primal end values with the closed-form multipliers."""
import random
import sympy as sp
import mpmath as mp

# (1) lemma identities, H' = 1
D, S, tau = sp.symbols('D S tau', positive=True)
pa, pb = S - D, S + D
G = lambda phi: (sp.sinh(phi) * sp.cosh(phi) + phi) / 2       # G(sinh phi)
e1 = sp.simplify((G(pb) - G(pa) - (D + (1 + 2 * sp.sinh(S)**2) * sp.sinh(D) * sp.cosh(D))).rewrite(sp.exp))
e2 = sp.simplify(((sp.sinh(pa) + sp.sinh(pb)) / 2 - sp.sinh(S) * sp.cosh(D)).rewrite(sp.exp))
e3 = sp.simplify((((sp.sinh(pb) - sp.sinh(pa))**2 - 4 * sp.sinh(tau)**2) / 4
                  - ((1 + sp.sinh(S)**2) * sp.sinh(D)**2 - sp.sinh(tau)**2)).rewrite(sp.exp))
e4 = sp.simplify((2 * G(tau) - (tau + sp.sinh(tau) * sp.cosh(tau))))
# AM-GM remainder: (1+2u^2)X - 2u cosh D sqrt(Y) - [ (1+2u^2)X - sinh^2 tau coth D ] + ... ;
u, Y = sp.symbols('u Y', nonnegative=True)
X = sp.sinh(D) * sp.cosh(D)
lhs = (1 + 2 * u**2) * X - 2 * u * sp.cosh(D) * sp.sqrt(Y)
fD = (1 + 2 * u**2) * X - ((1 + u**2) * sp.sinh(D)**2 - Y) * sp.cosh(D) / sp.sinh(D)   # Y = (1+u^2)sinh^2 D - sinh^2 tau
sq = (sp.sqrt(sp.tanh(D)) * u * sp.cosh(D) - sp.sqrt(Y / sp.tanh(D)))**2
e5 = sp.simplify((lhs - ((1 + u**2) * sp.sinh(D)**2 - Y) * sp.cosh(D) / sp.sinh(D) - sq).rewrite(sp.exp))
fprime = sp.simplify(sp.diff(D - tau - sp.sinh(tau) * sp.cosh(tau) + sp.sinh(tau)**2 * sp.cosh(D) / sp.sinh(D), D)
                     - (1 - sp.sinh(tau)**2 / sp.sinh(D)**2))
print('identities (expect 0):', e1, e2, e3, e4, e5, fprime)

# (2) gradient formula
z1, zN, V, eta, N = sp.symbols('z1 zN V eta N', real=True); H = sp.symbols('H', positive=True)
Gs = lambda v: (v * sp.sqrt(H**2 + v**2) + H**2 * sp.asinh(v / H)) / 2
l0 = sp.sqrt(eta**2 + (z1 - 1)**2); lN = sp.sqrt(eta**2 + (3 - zN)**2); L = 4 - l0 - lN
B = l0 + 3 * lN + (V + L) * zN - V * z1 - Gs(V + L) + Gs(V) + (N - 1) * 2 * Gs(eta)
gg = sp.sqrt(H**2 + (V + L)**2); d0 = (z1 - 1) / l0; dN = (zN - 3) / lN
g1 = d0 * (1 - zN + gg) - V; gN = dN * (3 - zN + gg) + V + L
r1 = sp.diff(B, z1) - g1; rN = sp.diff(B, zN) - gN
vals = [{z1: sp.Rational(97, 100), zN: sp.Rational(295, 100), V: sp.Rational(-96, 100), H: sp.Rational(16, 100), eta: sp.Rational(1, 100), N: 50},
        {z1: sp.Rational(-3, 2), zN: sp.Rational(51, 10), V: sp.Rational(7, 3), H: sp.Rational(3, 7), eta: sp.Rational(1, 800), N: 400}]
print('gradient residuals (expect ~0):', [sp.N(r.subs(v), 40) for r in (r1, rN) for v in vals])
print('G\'(v) check:', sp.simplify(sp.diff(Gs(V), V) - sp.sqrt(H**2 + V**2)))

# (3) random + adversarial lemma test at 50 digits
mp.mp.dps = 50
def slack(a, b, h, Hp):
    Gm = lambda v: (v * mp.sqrt(Hp**2 + v**2) + Hp**2 * mp.asinh(v / Hp)) / 2
    return Gm(b) - Gm(a) - 2 * Gm(h / 2) - abs((a + b) / 2) * mp.sqrt(max(mp.mpf(0), (b - a)**2 - h**2))
rnd = random.Random(20261004)
worst = mp.inf; worst_rel_eq = 0
for k in range(20000):
    Hp = mp.mpf(10) ** rnd.uniform(-3, 2); h = mp.mpf(10) ** rnd.uniform(-4, 0.5)
    a = mp.mpf(rnd.uniform(-5, 5)) * Hp
    mode = k % 3
    if mode == 0:
        b = a + h + mp.mpf(10) ** rnd.uniform(-6, 1) * h
    elif mode == 1:   # equality manifold: asinh(b/H) - asinh(a/H) = 2 tau, perturbed
        t = mp.asinh(h / (2 * Hp)); b = Hp * mp.sinh(mp.asinh(a / Hp) + 2 * t * (1 + mp.mpf(10) ** rnd.uniform(-12, -1) * rnd.choice([-1, 1])))
        if b - a < h: b = a + h
    else:
        b = a + h
    s = slack(a, b, h, Hp)
    worst = min(worst, s / (Hp**2))
print('lemma: min slack/H^2 over 20000 cases =', mp.nstr(worst, 5))

# (4) tightness: B at the primal end values with the closed-form maximizing multipliers
import json
for Nn in (50, 100, 200, 400):
    X = [mp.mpf(s) for s in open('/tmp/dossier_cc/chain%d_primal.txt' % Nn).read().split()]
    e = mp.mpf(1) / (2 * Nn)
    Z1 = X[0] + e * X[Nn + 1]; ZN = X[Nn] - e * X[2 * Nn + 1]
    L0 = mp.sqrt(e**2 + (Z1 - 1)**2); LN = mp.sqrt(e**2 + (3 - ZN)**2); LL = 4 - L0 - LN
    T = mp.sqrt(LL**2 - (ZN - Z1)**2) / 2
    Hp = mp.findroot(lambda Hh: Hh * mp.sinh((Nn - 1) * mp.asinh(e / Hh)) - T, 0.16)
    pm = mp.atanh((ZN - Z1) / LL); Vv = Hp * mp.sinh(pm - (Nn - 1) * mp.asinh(e / Hp))
    Gm = lambda v: (v * mp.sqrt(Hp**2 + v**2) + Hp**2 * mp.asinh(v / Hp)) / 2
    Bv = L0 + 3 * LN + (Vv + LL) * ZN - Vv * Z1 - Gm(Vv + LL) + Gm(Vv) + (Nn - 1) * 2 * Gm(e)
    d = json.load(open('/tmp/dossier_cc/chain%d_bound.json' % Nn))
    print(Nn, 'B(double-point ends) =', mp.nstr(Bv, 30), ' KKT value =', d['primal']['kkt_value'], ' V,H\' =', mp.nstr(Vv, 8), mp.nstr(Hp, 8))
