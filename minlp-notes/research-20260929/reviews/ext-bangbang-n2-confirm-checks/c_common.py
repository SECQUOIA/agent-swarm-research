"""Independent re-derivation of the double-integrator family of extension-n2.md (Section 6.1).
Written from the problem statement only; does not import the author's model.py or discrete.py.

x1' = x2, x2' = u, u in [-1, 1], x(0) = (0, x20), T = 2.
J = int e x2 + q/2 x1^2 - c/2 x2^2 + (k1 x1 + k2 x2) u dt - a x1(T) + rho/2 x2(T)^2.
Control +1 on [0, tau), -1 on (tau, T].
H = l0 + l1 u + psi1 x2 + psi2 u; psi1' = -(q x1 + k1 u); psi2' = -(e - c x2 + k2 u + psi1);
psi(T) = (-a, rho x2(T)); sigma = k1 x1 + k2 x2 + psi2 (u = +1 needs sigma <= 0).
"""
import sympy as sp

EX = {
    "A": dict(rho=2, k1=sp.Rational(-3, 10), k2=sp.Rational(-3, 10), q=sp.Rational(3, 10), c=1, x20=sp.Rational(1, 2), e=0),
    "B": dict(rho=1, k1=sp.Rational(6, 10), k2=sp.Rational(-12, 10), q=1, c=sp.Rational(1, 2), x20=sp.Rational(1, 2), e=sp.Rational(3, 10)),
    "B2": dict(rho=sp.Rational(1, 2), k1=sp.Rational(1, 2), k2=sp.Rational(-6, 10), q=sp.Rational(3, 10), c=sp.Rational(1, 5), x20=0, e=0),
    "C": dict(rho=sp.Rational(1, 2), k1=sp.Rational(1, 2), k2=sp.Rational(-1, 5), q=sp.Rational(3, 10), c=sp.Rational(1, 5), x20=0, e=0),
}
TAU_GUESS = {"A": 1.3155, "B": 1.198, "B2": 1.5955, "C": 1.4056}
T = 2
a = 1

t, th = sp.symbols("t th", real=True)


def arcs_sym(P):
    rho, k1, k2, q, c, x20, e = (P[k] for k in ("rho", "k1", "k2", "q", "c", "x20", "e"))
    x2a = x20 + t
    x1a = x20 * t + t ** 2 / 2
    x2b = x2a.subs(t, th) - (t - th)
    x1b = x1a.subs(t, th) + x2a.subs(t, th) * (t - th) - (t - th) ** 2 / 2
    # costates on arc b (u = -1), backward from T
    x2T = x2b.subs(t, T)
    s = sp.Symbol("s")
    psi1b = -a + sp.integrate((q * x1b + k1 * (-1)).subs(t, s), (s, t, T))
    psi2b = rho * x2T + sp.integrate((e - c * x2b + k2 * (-1) + psi1b).subs(t, s), (s, t, T))
    # arc a (u = +1), continuous at th
    psi1a = psi1b.subs(t, th) + sp.integrate((q * x1a + k1 * 1).subs(t, s), (s, t, th))
    psi2a = psi2b.subs(t, th) + sp.integrate((e - c * x2a + k2 * 1 + psi1a).subs(t, s), (s, t, th))
    siga = sp.expand(k1 * x1a + k2 * x2a + psi2a)
    sigb = sp.expand(k1 * x1b + k2 * x2b + psi2b)
    return dict(x1a=x1a, x2a=x2a, x1b=x1b, x2b=x2b, psi1a=psi1a, psi2a=psi2a, psi1b=psi1b, psi2b=psi2b,
                siga=siga, sigb=sigb)


def setup(name, digits=30):
    P = EX[name]
    ar = arcs_sym(P)
    eq = sp.expand(ar["siga"].subs(t, th))  # sigma(th) = 0 with the switch at th
    tau = sp.nsolve(eq, th, TAU_GUESS[name], prec=digits)
    num = {k: sp.lambdify(t, sp.expand(v.subs(th, tau)), "math") for k, v in ar.items()}
    sdot = float(sp.diff(ar["sigb"], t).subs(th, tau).subs(t, tau))
    sdot_a = float(sp.diff(ar["siga"], t).subs(th, tau).subs(t, tau))
    x2T = float(ar["x2b"].subs(th, tau).subs(t, T))
    return dict(P={k: float(v) for k, v in P.items()}, tau=float(tau), f=num, sdot=sdot, sdot_a=sdot_a, x2T=x2T)
