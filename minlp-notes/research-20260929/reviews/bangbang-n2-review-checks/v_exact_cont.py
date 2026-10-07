"""Independent check of the continuous quantities of extension-n2.md (examples A, A0, B, B2, C).

Everything is done symbolically with exact rationals (sympy), not with the author's numpy
polynomials and finite differences:
  F(th)   = exact cost of u = +1 on [0, th), u = -1 on [th, T]  (polynomial in th)
  tau     = root of F'(th) in (0, T), evaluated to 40 digits
  F''(tau) exact from the polynomial
  psi, sigma from the adjoint equations of the extremal (exact polynomials in t)
  D = Delta |sigma'(tau)|,  Q = Lyapunov solution of the last arc with Q(T) = Phi_xx,
  eta_L = b^T (Q(tau+) b - w),  beta_L = Q(tau+) b - w
Checks: F''(tau) == D + Delta^2 eta_L; the O-M form Omega computed by integrating the linearized
state (independent of Q); strict bang-bang ratio min |sigma(t)| / |t - tau|; PMP signs.
"""
import json
import sympy as sp

t, th = sp.symbols("t th", real=True)
R = sp.Rational
EX = {
    "A": dict(rho="2", k1="-0.3", k2="-0.3", q="0.3", c="1", x20="0.5", e="0"),
    "A0": dict(rho="1", k1="-0.3", k2="-0.3", q="0.3", c="0.2", x20="0.5", e="0"),
    "B": dict(rho="1", k1="0.6", k2="-1.2", q="1", c="0.5", x20="0.5", e="0.3"),
    "B2": dict(rho="0.5", k1="0.5", k2="-0.6", q="0.3", c="0.2", x20="0", e="0"),
    "C": dict(rho="0.5", k1="0.5", k2="-0.2", q="0.3", c="0.2", x20="0", e="0"),
}
T, a, x10 = R(2), R(1), R(0)
DIG = 40


def run(name, d):
    rho, k1, k2, q, c, x20, e = (R(d[k]) for k in ("rho", "k1", "k2", "q", "c", "x20", "e"))
    L = lambda x1, x2, u: e * x2 + q / 2 * x1 ** 2 - c / 2 * x2 ** 2 + (k1 * x1 + k2 * x2) * u
    # arcs as functions of (t, th)
    x2a = x20 + t
    x1a = x10 + x20 * t + t ** 2 / 2
    x1s, x2s = x1a.subs(t, th), x2a.subs(t, th)
    x2b = x2s - (t - th)
    x1b = x1s + x2s * (t - th) - (t - th) ** 2 / 2
    F = sp.integrate(L(x1a, x2a, 1), (t, 0, th)) + sp.integrate(L(x1b, x2b, -1), (t, th, T)) \
        + (-a * x1b.subs(t, T) + rho / 2 * x2b.subs(t, T) ** 2)
    F = sp.expand(F)
    dF = sp.Poly(sp.diff(F, th), th)
    roots = [r for r in dF.nroots(n=DIG) if abs(sp.im(r)) < 1e-30 and 0 < sp.re(r) < 2]
    roots = [sp.re(r) for r in roots]
    out = dict(example=name, roots=[float(r) for r in roots])
    tau = None
    for r in roots:
        # extremal candidate: sigma must be <= 0 before and >= 0 after (u = +1 then -1)
        tau = r
        break
    # exact adjoint for the extremal with switch at tau (tau is a float with 40 digits -> use sp.Float)
    xa1, xa2 = x1a, x2a
    xb1, xb2 = x1b.subs(th, tau), x2b.subs(th, tau)
    # psi1' = -(q x1 + k1 u), psi2' = -(e - c x2 + k2 u + psi1); psi(T) = (-a, rho x2(T))
    s = sp.symbols("s")
    psi1b = -a + sp.integrate((q * xb1 + k1 * (-1)).subs(t, s), (s, t, T))
    psi2b = rho * xb2.subs(t, T) + sp.integrate((e - c * xb2 + k2 * (-1) + psi1b).subs(t, s), (s, t, T))
    psi1a = psi1b.subs(t, tau) + sp.integrate((q * xa1 + k1 * 1).subs(t, s), (s, t, tau))
    psi2a = psi2b.subs(t, tau) + sp.integrate((e - c * xa2 + k2 * 1 + psi1a).subs(t, s), (s, t, tau))
    siga = sp.expand(k1 * xa1 + k2 * xa2 + psi2a)
    sigb = sp.expand(k1 * xb1 + k2 * xb2 + psi2b)
    sdot_a = sp.diff(siga, t).subs(t, tau)
    sdot_b = sp.diff(sigb, t).subs(t, tau)
    Delta = 2
    D = Delta * abs(sdot_a)
    # Lyapunov on the last arc: Q' = -(A^T Q + Q A + Hxx), Q(T) = diag(0, rho); A = [[0,1],[0,0]]
    Q11 = q * (T - t)
    Q12 = q * (T - t) ** 2 / 2
    Q22 = rho + q * (T - t) ** 3 / 3 - c * (T - t)
    # verify the ODE symbolically
    assert sp.simplify(sp.diff(Q11, t) + q) == 0
    assert sp.simplify(sp.diff(Q12, t) + Q11) == 0
    assert sp.simplify(sp.diff(Q22, t) - (-2 * Q12 + c)) == 0
    w = sp.Matrix([-k1, -k2])
    b = sp.Matrix([0, 1])
    Qt = sp.Matrix([[Q11, Q12], [Q12, Q22]]).subs(t, tau)
    beta = Qt * b - w
    eta = (b.T * beta)[0]
    Fpp = sp.diff(F, th, 2).subs(th, tau)
    # O-M quadratic form, computed without Q: xbar(tau+) = [xdot] xi = b * (ub - ua) * xi, xi = 1,
    # xbar' = A xbar on (tau, T]; Omega = D xi^2 + 2 [H_x] xbar_av xi + int Hxx(xbar) + Phi_xx(xbar(T))
    du = -2
    xb_1 = du * 0 + du * 1 * (t - tau) * 0  # placeholder, compute properly below
    # xbar = (x1bar, x2bar): x2bar' = 0, x1bar' = x2bar; x2bar(tau+) = du, x1bar(tau+) = 0
    xbar2 = sp.Integer(du)
    xbar1 = du * (t - tau)
    Hx_jump = sp.Matrix([k1, k2]) * du  # [H_x] = (dl1/dx)(ub - ua) (b constant)
    xav = sp.Matrix([0, du]) / 2
    Omega = D + 2 * (Hx_jump.T * xav)[0] + sp.integrate(q * xbar1 ** 2 - c * xbar2 ** 2, (t, tau, T)) \
        + rho * xbar2 ** 2
    # strict bang-bang ratio and PMP sign check on a fine grid (exact polynomials evaluated in floats)
    fa = sp.lambdify(t, siga, "mpmath")
    fb = sp.lambdify(t, sigb, "mpmath")
    import mpmath as mp
    mp.mp.dps = 30
    taum = mp.mpf(str(tau))
    ratio = mp.inf
    viol = 0
    n = 4000
    for i in range(n + 1):
        tt = taum * i / n
        va = fa(tt)
        viol = max(viol, va)  # need sigma <= 0 before tau
        if i < n:
            ratio = min(ratio, abs(va) / (taum - tt))
        tt2 = taum + (2 - taum) * i / n
        vb = fb(tt2)
        viol = max(viol, -vb)
        if i > 0:
            ratio = min(ratio, abs(vb) / (tt2 - taum))
    kappa = Delta / (2 * abs(sdot_b))
    out.update(tau=float(tau), J=float(F.subs(th, tau)), eta_L=float(eta), beta_L=[float(beta[0]), float(beta[1])],
               D=float(D), Fpp_exact=float(Fpp), Fpp_formula=float(D + 4 * eta), diff=float(Fpp - (D + 4 * eta)),
               Omega_OM=float(Omega), Omega_minus_Fpp=float(Omega - Fpp),
               sigdot_a=float(sdot_a), sigdot_b=float(sdot_b), sigma_continuity=float(siga.subs(t, tau) - sigb.subs(t, tau)),
               sigma_tau=float(siga.subs(t, tau)), strict_ratio=float(ratio), pmp_viol=float(viol),
               ratio_D=float(4 * abs(eta) / D), kappa=float(kappa),
               Pmax_tau=[[float(Qt[0, 0] - beta[0] ** 2 / eta), float(Qt[0, 1] - beta[0] * beta[1] / eta)],
                         [float(Qt[0, 1] - beta[0] * beta[1] / eta), float(Qt[1, 1] - beta[1] ** 2 / eta)]],
               Qplus=[[float(Qt[0, 0]), float(Qt[0, 1])], [float(Qt[1, 0]), float(Qt[1, 1])]])
    return out


if __name__ == "__main__":
    res = {}
    for name, d in EX.items():
        r = run(name, d)
        res[name] = r
        print(json.dumps(r), flush=True)
    json.dump(res, open("logs/v_exact_cont.json", "w"), indent=1)
