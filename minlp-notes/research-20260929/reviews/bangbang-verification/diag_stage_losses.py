"""Diagnostic: per-stage losses rho_t(x*_t, u*_t) - m_t at the high-precision feasible trajectory
(u_{s2} from logs/primal_check.json), for a set of stages, with exact m_t from v_qcal_exact.stage."""
import json, sys
from fractions import Fraction as Fr
import numpy as np
from mpmath import mp
import v_qcal_exact as Q

mp.prec = 300
D = dict(np.load(Q.TB + "logs/optcdeg2_qcal_data.npz")); Vb = np.load("logs/vt_reviewer.npy")
pc = json.load(open("logs/primal_check.json"))["rigorous_primal"]
s1, s2 = pc["s1"], pc["s2"]; u = D["u"]
us2 = Fr(pc["u_s2"])  # 25 digits suffice for a diagnostic
def uex(t):
    if t == s1: return Fr(float(u[s1]))
    if t == s2: return us2
    return Fr(1, 5) if u[t] > 0 else Fr(-1, 5)
# exact-ish trajectory: Fractions rounded to 2^-300 each step
SC = 1 << 300
rd = lambda x: Fr((x.numerator * SC) // x.denominator, SC)
y, v = [Fr(10)], [Fr(0)]
for t in range(Q.N):
    y.append(rd(y[t] + Q.H * v[t])); v.append(rd(v[t] + Q.H * uex(t) - Q.AY * y[t] - Q.BV * v[t] ** 2))
print("v_N of diagnostic trajectory", float(v[Q.N]))
def rho(t):
    P0y, P0v, Q0, C0 = (Fr(float(D[k][t])) for k in ("py", "pv", "q", "c"))
    P1y, P1v, Q1, C1 = (Fr(float(D[k][t + 1])) for k in ("py", "pv", "q", "c"))
    y1, v1 = y[t] + Q.H * v[t], v[t] + Q.H * uex(t) - Q.AY * y[t] - Q.BV * v[t] ** 2
    return Q.W * y[t] ** 2 + P1y * y1 + P1v * v1 + Q1 / 2 * (v1 - C1) ** 2 - P0y * y[t] - P0v * v[t] - Q0 / 2 * (v[t] - C0) ** 2
ts = sorted(set(list(range(1, 6)) + list(range(s1 - 4, s1 + 5)) + list(range(s2 - 4, s2 + 5)) + list(range(Q.N - 3, Q.N)) + [1000, 20000, 48000]))
for t in ts:
    m = Q.stage(t, D, Vb)[0]
    print(t, "loss_at_exact_traj", float(rho(t) - m), "pv[t+1]", float(D["pv"][t + 1]), "u", float(uex(t)))

# ---- full telescoping decomposition at the diagnostic trajectory
J = sum(Q.W * a * a for a in y)
s0min, _ = Q.stage0(D)
P1y, P1v, Q1, C1 = (Fr(float(D[k][1])) for k in ("py", "pv", "q", "c"))
s0val = Q.W * 100 + P1y * y[1] + P1v * v[1] + Q1 / 2 * (v[1] - C1) ** 2
PNy, PNv, QN, CN = (Fr(float(D[k][Q.N])) for k in ("py", "pv", "q", "c"))
teval = Q.W * y[Q.N] ** 2 - PNy * y[Q.N] - PNv * v[Q.N] - QN / 2 * (v[Q.N] - CN) ** 2
temin = Q.terminal(D)
tot_rho = Fr(0); tot_m = Fr(0); neg = []
G = 1 << 200
lb_int = (s0min.numerator * G) // s0min.denominator + (temin.numerator * G) // temin.denominator
for t in range(1, Q.N):
    r = rho(t); m = Q.stage(t, D, Vb)[0]
    tot_rho += r; tot_m += m
    lb_int += (m.numerator * G) // m.denominator
    if r - m < 0:
        neg.append((t, float(r - m)))
tele = s0val + tot_rho + teval
LB = s0min + tot_m + temin
print("J_diag", float(J), "telescoped - J", float(tele - J))
print("J - LB_exact", float(J - LB), "LB_exact - LB_grid", float(LB - Fr(lb_int, G)))
print("stage0 loss", float(s0val - s0min), "terminal loss", float(teval - temin), "sum stage losses", float(tot_rho - tot_m))
print("negative stage losses", len(neg), neg[:10])
print("LB_exact 25 digits", str(LB.numerator * 10**22 // LB.denominator), "J 25 digits", str(J.numerator * 10**22 // J.denominator))
