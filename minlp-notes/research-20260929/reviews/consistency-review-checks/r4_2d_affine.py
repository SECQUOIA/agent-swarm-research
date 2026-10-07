"""Referee check R4: the 2D example after Proposition 5.4.

(1) The band [max(0, x+y-1), min(x,y)] on [0,1]^2 is the band of a box problem
    with bilinear data: child bag  G_A = u*s1 + (1-u)*s2, u in [0,1]
    (U = min(s1,s2)); parent bag G_B = v*(1 - s1 - s2), v in [0,1]
    (V = min(0, 1-s1-s2), f* = 0, L = max(0, s1+s2-1)).
    The affine split relaxation is computed on the bag data directly.
(2) Formal cell version with U + delta: affine bracket = 1/2 - delta.
"""
import numpy as np
from scipy.optimize import linprog

OPT = {"primal_feasibility_tolerance": 1e-10, "dual_feasibility_tolerance": 1e-10}
g = np.linspace(0, 1, 41)
S1, S2 = [a.ravel() for a in np.meshgrid(g, g, indexing="ij")]
B = np.column_stack([np.ones_like(S1), S1, S2])
u = np.linspace(0, 1, 21)


def split_lp():
    # max mA + mB s.t. GA(s,u) - B c >= mA, GB(s,v) + B c >= mB
    rows, rhs = [], []
    k = len(S1)
    for uu in u:
        R = np.zeros((k, 5)); R[:, :3] = B; R[:, 3] = 1
        rows.append(R); rhs.append(uu * S1 + (1 - uu) * S2)
    for vv in u:
        R = np.zeros((k, 5)); R[:, :3] = -B; R[:, 4] = 1
        rows.append(R); rhs.append(vv * (1 - S1 - S2))
    cost = np.array([0, 0, 0, -1, -1.0])
    r = linprog(cost, A_ub=np.vstack(rows), b_ub=np.concatenate(rhs), bounds=[(None, None)] * 5,
                method="highs", options=OPT)
    return -r.fun


U = np.minimum(S1, S2)
V = np.minimum(0, 1 - S1 - S2)
fs = np.min(U + V)
print(f"(1) bilinear realization: f* = {fs:.3f}, max|L - max(0,s1+s2-1)| = "
      f"{np.max(np.abs((fs - V) - np.maximum(0, S1 + S2 - 1))):.1e}; "
      f"affine split gap from the bag LP = {fs - split_lp():.6f}; "
      f"pinch set = boundary of the square: min width in interior = "
      f"{np.min((U - (fs - V))[(S1 > 0) & (S1 < 1) & (S2 > 0) & (S2 < 1)]):.3f}")


def bracket(Uv, Lv):
    k = len(S1)
    A1 = np.hstack([B, -np.ones((k, 1)), np.zeros((k, 1))])
    A2 = np.hstack([-B, np.zeros((k, 1)), -np.ones((k, 1))])
    r = linprog(np.array([0, 0, 0, 1, 1.0]), A_ub=np.vstack([A1, A2]), b_ub=np.concatenate([Uv, -Lv]),
                bounds=[(None, None)] * 5, method="highs", options=OPT)
    return r.fun


for delta in [0.0, 0.1, 0.25, 0.4, 0.5]:
    gD = bracket(U + delta, np.maximum(0, S1 + S2 - 1))
    print(f"(2) delta={delta:.2f}: affine cell bracket g_D = {gD:.6f} (claim 1/2 - delta = {0.5 - delta:.6f}); "
          f"1D bound (a) would give ((M_L+M_U)/2) r^2 - w_min = {-delta:.2f}")
