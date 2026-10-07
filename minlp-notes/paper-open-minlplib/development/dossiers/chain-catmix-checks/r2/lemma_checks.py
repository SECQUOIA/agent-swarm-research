"""Fresh checks (dossier, 2026-10-04): (1) sympy: hyperbolic identities and the AM-GM remainder of
Lemma 3; (2) mpmath 40 digits: the interior inequality of Theorem 1 on random chains (any z),
sum_k lam_k (z_k+z_{k+1})/2 >= (V+L) z_N - V z_1 - G(V+L) + G(V) + (N-1) c, L = sum lam_k;
(3) Remark 1 multiplier formulas: dB/dV = dB/dH = 0 at the closed-form multipliers."""
import random
import sympy as sp
import mpmath as mp

# (1) symbolic identities with H = 1
pa, pb, t = sp.symbols('phi_a phi_b tau', real=True)
S, D = (pa + pb) / 2, (pb - pa) / 2
G = lambda v: (v * sp.sqrt(1 + v**2) + sp.asinh(v)) / 2
a, b = sp.sinh(pa), sp.sinh(pb)
def z(e): return sp.simplify(sp.expand(sp.expand_trig(e.rewrite(sp.exp))))
X = sp.sinh(D) * sp.cosh(D)
u2 = sp.sinh(S)**2
i1 = z((G(b) - G(a)).subs({sp.sqrt(1 + a**2): sp.cosh(pa), sp.sqrt(1 + b**2): sp.cosh(pb), sp.asinh(a): pa, sp.asinh(b): pb}) - (D + (1 + 2*u2) * X))
i2 = z((a + b) / 2 - sp.sinh(S) * sp.cosh(D))
h2 = 2 * sp.sinh(t)
i3 = z(((b - a)**2 - h2**2) / 4 - ((1 + u2) * sp.sinh(D)**2 - sp.sinh(t)**2))
i4 = z(2 * G(sp.sinh(t)).subs({sp.sqrt(1 + sp.sinh(t)**2): sp.cosh(t), sp.asinh(sp.sinh(t)): t}) - (t + sp.sinh(t) * sp.cosh(t)))
print('identities (expect 0):', i1, i2, i3, i4)
# AM-GM remainder: with p = u^2 cosh^2 D, q = Y, T = tanh D (all >= 0):  p T + q/T - 2 sqrt(p q) = (sqrt(pT) - sqrt(q/T))^2
uu, Dd, Y = sp.symbols('u D Y', positive=True)
T = sp.tanh(Dd); p = uu**2 * sp.cosh(Dd)**2
rem = sp.simplify(p * T + Y / T - 2 * uu * sp.cosh(Dd) * sp.sqrt(Y) - (sp.sqrt(p * T) - sp.sqrt(Y / T))**2)
print('AM-GM remainder (expect 0):', rem)
lhs = sp.simplify(p * T + Y / T)
print('pT + q/T with Y=(1+u^2)sinh^2D - sinh^2 tau  minus ((1+2u^2)X - sinh^2 tau coth D):',
      sp.simplify((lhs - ((1 + 2*uu**2) * sp.sinh(Dd) * sp.cosh(Dd) - sp.sinh(t)**2 / sp.tanh(Dd))).subs(Y, (1 + uu**2) * sp.sinh(Dd)**2 - sp.sinh(t)**2)))
phi = Dd - t - sp.sinh(t) * sp.cosh(t) + sp.sinh(t)**2 / sp.tanh(Dd)
print('phi(tau) =', sp.simplify(phi.subs(Dd, t)), ' phi\'(D) - (1 - sinh^2 tau/sinh^2 D) =', sp.simplify(sp.diff(phi, Dd) - (1 - sp.sinh(t)**2 / sp.sinh(Dd)**2)))

# (2) random interior inequality, 40 digits
mp.mp.dps = 40
rnd = random.Random(20261004)
def Gm(v, H): return (v * mp.sqrt(H**2 + v**2) + H**2 * mp.asinh(v / H)) / 2
worst = mp.inf; cnt = 0
for trial in range(3000):
    N = rnd.choice([2, 3, 5, 10, 50])
    h = mp.mpf(1) / N
    mode = trial % 3
    if mode == 0:     # generic random chain
        zz = [mp.mpf(rnd.uniform(-3, 5)) for _ in range(N)]
        V, H = mp.mpf(rnd.uniform(-3, 3)), mp.mpf(10) ** rnd.uniform(-3, 1)
    else:             # discrete catenary through random parameters: slopes sinh(phi0 + (2k+1) tau)
        H = mp.mpf(10) ** rnd.uniform(-2, 0.5)
        tau = mp.asinh(h / (2 * H)); phi0 = mp.mpf(rnd.uniform(-3, 1))
        zz = [mp.mpf(rnd.uniform(-1, 1))]
        for k in range(1, N):
            zz.append(zz[-1] + h * mp.sinh(phi0 + (2 * (k - 1) + 1) * tau))
        V = H * mp.sinh(phi0)
        if mode == 2:  # perturb
            zz = [v + mp.mpf(rnd.uniform(-1e-6, 1e-6)) for v in zz]; V += mp.mpf(rnd.uniform(-1e-6, 1e-6))
    lam = [mp.sqrt(h**2 + (zz[k + 1] - zz[k])**2) for k in range(N - 1)]
    L = sum(lam)
    lhs = sum(lam[k] * (zz[k] + zz[k + 1]) / 2 for k in range(N - 1))
    rhs = (V + L) * zz[-1] - V * zz[0] - Gm(V + L, H) + Gm(V, H) + (N - 1) * 2 * Gm(h / 2, H)
    sl = (lhs - rhs) / (1 + abs(lhs))
    worst = min(worst, sl); cnt += 1
    if mode == 1: assert abs(lhs - rhs) < mp.mpf(10)**-30 * (1 + abs(lhs)), (N, lhs - rhs)
print('interior inequality: %d trials, min relative slack %s (mode 1 = exact catenary: equality to 1e-30)' % (cnt, mp.nstr(worst, 5)))

# (3) Remark 1 multipliers make the (V, H) gradient vanish
for N in (50, 400):
    eta = mp.mpf(1) / (2 * N)
    z1, zN = mp.mpf('0.9678531188143804'), mp.mpf('2.9487346283043734')
    l0 = mp.sqrt(eta**2 + (z1 - 1)**2); lN = mp.sqrt(eta**2 + (3 - zN)**2); L = 4 - l0 - lN
    Dz = zN - z1
    Hs = mp.findroot(lambda H: H * mp.sinh((N - 1) * mp.asinh(eta / H)) - mp.sqrt(L**2 - Dz**2) / 2, 0.16)
    pm = mp.atanh(Dz / L); V = Hs * mp.sinh(pm - (N - 1) * mp.asinh(eta / Hs))
    B = lambda V, H: l0 + 3 * lN + (V + L) * zN - V * z1 - Gm(V + L, H) + Gm(V, H) + (N - 1) * 2 * Gm(eta, H)
    print('N=%d  dB/dV=%s  dB/dH=%s' % (N, mp.nstr(mp.diff(lambda v: B(v, Hs), V), 3), mp.nstr(mp.diff(lambda hh: B(V, hh), Hs), 3)))
