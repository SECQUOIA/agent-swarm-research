"""Independent targeted checks for the round-2 confirmation of theory-bangbang/report.md.

Reads stored results only (no certificate or screening run is repeated), plus one small
scalar ODE integration. Run from this directory:
    OMP_NUM_THREADS=1 timeout 120 python3 c_checks.py > logs/c_checks.log
"""
import json
from fractions import Fraction as F

import numpy as np
from scipy.integrate import solve_ivp

TB = "../../theory-bangbang/logs/"
VER = "../bangbang-verification/logs/"

# R1 / M7: gaps in exact rationals, from the raw stored files -------------------------
cert = json.load(open(TB + "optcdeg2_qcal_certify.json"))
lb = F(cert["certified_bound"])                       # stored double, exactly
fp = F(cert["J_float"])                               # author's float primal point
prim = json.load(open(VER + "primal_check.json"))["rigorous_primal"]
ub_end = F(prim["J_upper"].strip("[]").split(",")[1].strip())   # upper end of enclosure
ub_q = F("293.87607509587509328")
ex_s = json.load(open(VER + "qcal_exact.json"))["bound_str"]
ex = F(ex_s[:3] + "." + ex_s[3:])
tr = F("293.876075095875092379")
print("certified bound (exact double):", float(lb), "=", lb.numerator / lb.denominator)
print("quoted UB >= enclosure upper end:", ub_q >= ub_end, " quoted-UB rounding:", float(ub_q - ub_end))
print("truncated quote <= exact LB:", tr <= ex, " exact LB:", ex_s[:3] + "." + ex_s[3:])
for name, v in [("UB_q - LB", ub_q - lb), ("UB_end - LB", ub_end - lb), ("rel (UB_q-LB)/UB_q", (ub_q - lb) / ub_q),
                ("FP - UB_end", fp - ub_end), ("FP - LB", fp - lb), ("UB_q - exact", ub_q - ex),
                ("UB_end - exact", ub_end - ex), ("exact - LB", ex - lb),
                ("first-wave FP - LB", F("293.876075095886") - lb)]:
    print(f"  {name}: {float(v):.4e}")

# R2: p_v(3092) --------------------------------------------------------------------------
d = np.load(TB + "optcdeg2_qcal_data.npz")
print("npz pv[3090:3095]:", d["pv"][3090:3095])
print("npz u[3091] (fractional):", d["u"][3091], " u[47290]:", d["u"][47290])
ref = [json.loads(s) for s in open(TB + "refine_primal.log") if s.strip()][-1]
print("refine_primal.log final pv_k1p1:", ref["pv_k1p1"], " s1:", ref["s1"], " s2:", ref["s2"])
e1 = [json.loads(s) for s in open(TB + "explore1.log") if s.strip()]
print("explore1 first line pv_s1p1:", e1[0]["pv_s1p1"])
print("explore1 worst losses (kh>0 configs):", sorted({round(r.get("worst", 0), 10) for r in e1[1:] if "worst" in r})[:6])

# M5: arc lengths --------------------------------------------------------------------------
h = 4e-4
print(f"head arc {ref['s1'] * h:.4f}, tail arc {(50000 - ref['s2']) * h:.4f}, sum {(ref['s1'] + 50000 - ref['s2']) * h:.4f}")

# M2: toy windows ----------------------------------------------------------------------------
for dom in ("box", "reach"):
    for r in json.load(open(VER + f"window_toy_k-0.5_{dom}.json")):
        a = r["A"]
        print(f"toy {dom:5s} N={r['N']:5d} A fails {a['fail']:4d} dur {a['duration']:.5f} range {a['range']} B fails {r['B']['fail']}")

# R5 follow-up: scalar global-form P-hat with eta_L > 0 ----------------------------------------
# Problem: x' = u, |u| <= 1 (Delta = 2), cost int x^2/2 + Phi(x(T)), Phi = -phi x^2/2 + k x.
# Extremal: u = -1 on [0, tau), u = +1 on (tau, T]; x(tau) = xt > 0; psi' = -x, sigma = psi.
# b = 1, l_1 = 0, so w = 0, beta = P, eta = P; A = g_x = 0, H_xx = 1 (N = 0 case).
xt, tau, T, phi = 0.01, 1.0, 2.0, 0.9
S = T - tau
x0 = xt + tau
psiT = -(xt * S + S ** 2 / 2)
k = psiT + phi * (xt + S)              # transversality psi(T) = Phi'(x(T))
sig = lambda t: -(xt * (t - tau) + (t - tau) ** 2 / 2) if t > tau else (xt * (tau - t) + (tau - t) ** 2 / 2)
ts = np.linspace(0, T, 2001)
ok_sign = all((sig(t) > 0) for t in ts if t < tau) and all((sig(t) < 0) for t in ts if t > tau)
print(f"scalar example: x0={x0}, k={k:.4f}, sign pattern consistent with u=-1 then u=+1: {ok_sign}; "
      f"sigma_dot(tau) = {-xt}; D = |sigma_dot| Delta = {2 * xt}")
QtauP = -phi + 1.0 * S                 # Lyapunov: Q' = -H_xx, Q(T) = Phi_xx
etaL = QtauP
print(f"  eta_L = Q(tau+) b - w = {etaL:.3f} (> 0); F''(tau) = D + Delta^2 eta_L = {2 * xt + 4 * etaL:.3f}")
# global form (Prop. 3.2, eps = 0): P' = -H_xx + (Delta / (2|sigma|)) (P b - w)^2, backward from P(T) = Phi_xx
rhs = lambda t, P: [-1.0 + (2.0 / (2 * abs(sig(t)))) * P[0] ** 2]
ev = lambda t, P: P[0] + 1e8
ev.terminal = True
sol = solve_ivp(rhs, [T, tau + 1e-9], [-phi], events=ev, rtol=1e-10, atol=1e-12, method="LSODA")
if sol.t_events[0].size:
    tb = sol.t_events[0][0]
    print(f"  global-form P-hat reaches -1e8 at t = {tb:.6f} (s = t - tau = {tb - tau:.6f}), after tau")
else:
    print("  global-form P-hat reaches tau+ without blow-up; P(tau+) =", sol.y[0, -1])


def F_switch(theta):
    """Cost of u = -1 on [0, theta), +1 on [theta, T] (closed form)."""
    xth = x0 - theta
    run1 = (x0 ** 3 - xth ** 3) / 6.0                  # int_0^theta (x0 - t)^2 / 2
    xT = xth + (T - theta)
    run2 = (xT ** 3 - xth ** 3) / 6.0                  # int_theta^T (xth + t - theta)^2 / 2
    return run1 + run2 - phi * xT ** 2 / 2 + k * xT


hh = 1e-3
print(f"  F'(tau) by central difference = {(F_switch(tau + hh) - F_switch(tau - hh)) / (2 * hh):.2e}; "
      f"F''(tau) = {(F_switch(tau + hh) - 2 * F_switch(tau) + F_switch(tau - hh)) / hh ** 2:.4f}")
for eps in (0.0, 0.01):
    rhs_e = lambda t, P, e=eps: [-1.0 + 2 * e + (2.0 / (2 * abs(sig(t)))) * P[0] ** 2]
    s2 = solve_ivp(rhs_e, [T, tau + 1e-9], [-phi - 2 * eps], events=ev, rtol=1e-10, atol=1e-12, method="LSODA")
    print(f"  eps = {eps}: eta_eps = {-phi - 2 * eps + (1 - 2 * eps) * S:.3f}; global-form P-hat blow-up at t = "
          f"{s2.t_events[0][0] if s2.t_events[0].size else None}")
