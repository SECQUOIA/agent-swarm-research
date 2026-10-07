"""Targeted checks for the third revision of report.md (round-2 confirmation, issue 1).

Scalar example for Remark 3.3 (float, not certified). Run from theory-bangbang/:
    OMP_NUM_THREADS=1 timeout 120 python3 revision3_checks.py > logs/revision3_checks.log

Problem: x' = u, |u| <= 1 (Delta = 2), cost int x^2/2 dt + Phi(x(T)),
Phi(x) = -phi x^2/2 + k x, x(0) = x0. Candidate extremal: u = -1 on [0, tau), u = +1 on
(tau, T], with x(tau) = xt > 0. Then b = 1, l_1 = 0, so w = 0, beta = P, eta = P, and
g_x = 0, H_xx = 1 (the N = 0 case of [E]).

Checks:
1. exact (sympy): minimum-principle signs, sigma_dot(tau), D, eta_L, F'(tau) = 0, F''(tau);
2. global form (Prop. 3.2 on the whole last arc): the maximal backward solution of
   P' = -(1 - 2 eps) + P^2/|sigma|, P(T) = -phi - 2 eps, by two methods:
   (a) the linearization P = -(1 - 2 eps) phi_lin / phi_lin' (phi_lin'' = (1 - 2 eps) phi_lin / |sigma|),
       blow-up where phi_lin' = 0; (b) direct integration of y = -1/P until y = 0;
3. local formulation: P = Q on [tau + delta_0, T], singular equation only on the layer;
4. the forward direction eta_L < 0 with the SSC holding (second parameter set).
"""
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp


def exact_data(xt, tau, T, phi):
    t, th = sp.symbols("t theta", real=True)
    xt, tau, T, phi = (sp.nsimplify(v) for v in (xt, tau, T, phi))
    x0 = xt + tau
    xT = xt + (T - tau)
    psiT = -sp.integrate(xt + (t - tau), (t, tau, T))  # psi(tau) = 0 and psi' = -x on the last arc
    k = psiT + phi * xT  # transversality: psi(T) = Phi'(x(T)) = -phi x(T) + k
    sig_after = sp.expand(psiT + sp.integrate(xt + (t - tau), (t, t, T)))  # sigma = psi (b = 1, l_1 = 0)
    sig_before = sp.expand(sp.integrate(x0 - t, (t, t, tau)))  # psi(tau) = 0, x = x0 - t
    # sign checks: sigma > 0 before tau (u = -1), sigma < 0 after (u = +1)
    s = sp.symbols("s", positive=True)
    sb = sp.simplify(sig_before.subs(t, tau - s))
    sa = sp.simplify(sig_after.subs(t, tau + s))
    sigdot = sp.diff(sig_after, t).subs(t, tau)
    D = abs(sigdot) * 2
    Qtau = -phi + (T - tau)  # Q' = -H_xx = -1, Q(T) = Phi_xx = -phi
    etaL = Qtau
    xth = x0 - th
    Fth = (sp.integrate((x0 - t) ** 2 / 2, (t, 0, th))
           + sp.integrate((xth + (t - th)) ** 2 / 2, (t, th, T))
           - phi * (xth + T - th) ** 2 / 2 + k * (xth + T - th))
    F1 = sp.simplify(sp.diff(Fth, th).subs(th, tau))
    F2 = sp.simplify(sp.diff(Fth, th, 2).subs(th, tau))
    return dict(x0=x0, k=k, sig_before=sb, sig_after=sa, sigdot=sigdot, D=D, etaL=etaL,
                F1=F1, F2=F2, formula=D + 4 * etaL, sig_after_expr=sig_after)


def global_blowup(xt, tau, T, phi, eps):
    """Maximal backward solution of the global form on the last arc; returns blow-up time or None."""
    a = 1.0 - 2 * eps
    absig = lambda t: xt * (t - tau) + (t - tau) ** 2 / 2  # |sigma| after tau
    PT = -phi - 2 * eps
    stop = tau + 1e-9
    # (a) linearization: phi_lin'' = a phi_lin / |sigma|, P = -a phi_lin / phi_lin'
    #     (then P' = -a + P^2/|sigma|); start phi_lin(T) = 1, phi_lin'(T) = -a / PT.
    ev = lambda t, z: z[1]
    ev.terminal = True
    sa = solve_ivp(lambda t, z: [z[1], a * z[0] / absig(t)], [T, stop], [1.0, -a / PT],
                   events=ev, method="DOP853", rtol=1e-12, atol=1e-14)
    tb_a = sa.t_events[0][0] if sa.t_events[0].size else None
    # (b) y = -1/P > 0 while P < 0: y' = -a y^2 + 1/|sigma|; blow-up of P where y = 0
    evy = lambda t, y: y[0]
    evy.terminal = True
    sb = solve_ivp(lambda t, y: [-a * y[0] ** 2 + 1.0 / absig(t)], [T, stop], [-1.0 / PT],
                   events=evy, method="Radau", rtol=1e-11, atol=1e-13)
    tb_b = sb.t_events[0][0] if sb.t_events[0].size else None
    return tb_a, tb_b


def local_layer(xt, tau, T, phi, delta0, s_end=1e-12):
    """Local formulation, eps = 0: P = Q on [tau + delta0, T], then P' = -1 + P^2/|sigma| on the layer.
    Integrated in log s; returns (P at s_end or None, blow-up s or None)."""
    absig = lambda s: xt * s + s ** 2 / 2
    P0 = -phi + (T - tau - delta0)
    # d P / d(log s) = s * (-1 + P^2/|sigma|)
    rhs = lambda ls, P: [np.exp(ls) * (-1.0 + P[0] ** 2 / absig(np.exp(ls)))]
    ev = lambda ls, P: P[0] + 1e8
    ev.terminal = True
    sol = solve_ivp(rhs, [np.log(delta0), np.log(s_end)], [P0], events=ev, method="Radau",
                    rtol=1e-10, atol=1e-13)
    if sol.t_events[0].size:
        return None, float(np.exp(sol.t_events[0][0]))
    return float(sol.y[0, -1]), None


for label, (xt, tau, T, phi) in [("example (eta_L > 0)", (0.01, 1.0, 2.0, 0.9)),
                                   ("forward direction (eta_L < 0)", (0.5, 1.0, 2.0, 1.1))]:
    d = exact_data(xt, tau, T, phi)
    print(f"== {label}: xt={xt}, tau={tau}, T={T}, phi={phi}")
    print(f"  x0 = {d['x0']}, k = {d['k']}")
    print(f"  sigma(tau - s) = {d['sig_before']}  (> 0 for 0 < s <= tau, u = -1)")
    print(f"  sigma(tau + s) = {d['sig_after']}  (< 0 for 0 < s <= T - tau, u = +1)")
    print(f"  sigma_dot(tau) = {d['sigdot']}, D = {d['D']}, eta_L = Q(tau+) = {d['etaL']}")
    print(f"  F'(tau) = {d['F1']}, F''(tau) = {d['F2']} (formula D + Delta^2 eta_L = {d['formula']})")
    for eps in (0.0, 0.01):
        tb_a, tb_b = global_blowup(xt, tau, T, phi, eps)
        eta_eps = -phi - 2 * eps + (1 - 2 * eps) * (T - tau)
        print(f"  global form, eps = {eps} (eta_eps = {eta_eps:.3f}): P-hat -> -inf at "
              f"t = {tb_a:.6f} (linearization), t = {tb_b:.6f} (y = -1/P)"
              if tb_a is not None and tb_b is not None else
              f"  global form, eps = {eps}: no blow-up found ({tb_a}, {tb_b})")
    for delta0 in (0.05, 0.2):
        Pend, sb = local_layer(xt, tau, T, phi, delta0)
        print(f"  local formulation, delta_0 = {delta0}: "
              + (f"P(tau + 1e-12) = {Pend:.4f}, bounded" if sb is None else f"P -> -inf at s = {sb:.3e}"))
