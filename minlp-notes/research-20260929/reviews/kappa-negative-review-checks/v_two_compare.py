"""Compare the author's zbar, the author's certified incumbent, and the reviewer's best pattern at
(t1, t2) = (0.7, 1.3), N = 2000, kappa = -0.5 (exact)."""
import json
from fractions import Fraction as Fr
from vtoy import traj, H_entry, kkt_check
from v_two import toy2, pattern, qp2
N = 2000
toy = toy2(Fr(1, 2), Fr(7, 10), Fr(13, 10))
h = toy.T / N
_, k = toy.data(N)

def opt1(u, j):
    """exact 1-D optimum of stage j (others fixed)"""
    u = list(u); u[j] = Fr(0)
    E0 = traj(toy, N, u)
    H = H_entry(toy, N, k, j, j)
    g = h * E0["sig"][j]
    c = [Fr(-1), Fr(1)]
    if H > 0:
        c.append(min(Fr(1), max(Fr(-1), -g / H)))
    v = min(c, key=lambda w: g * w + H * w * w / 2)
    u[j] = v
    return u

# (A) author's zbar: +1 until 596, -1 from 597, u_778 fractional (optimal), +1 after
uA = pattern(N, 597, Fr(-1), 778, Fr(0)); uA = opt1(uA, 778)
# (B) author's incumbent: u_597 fractional, -1 after, second switch at a vertex: try m2 = 777, 778, 779
res = {}
EA = traj(toy, N, uA)
res["A_author_zbar"] = dict(u597=float(uA[597]), u778=float(uA[778]), kkt=kkt_check(EA)[0], J=float(EA["J"]))
for m2 in (777, 778, 779):
    uB = pattern(N, 597, Fr(0), m2, Fr(1)); uB = opt1(uB, 597)
    EB = traj(toy, N, uB)
    ok, fr = kkt_check(EB)
    res[f"B_frac597_switch2_at_{m2}"] = dict(u597=float(uB[597]), kkt=ok, frac=fr if ok else None,
                                            J_minus_A_h2=float((EB["J"] - EA["J"]) / h**2))
uC = pattern(N, 597, Fr(1), 777, Fr(-1))
EC = traj(toy, N, uC)
res["C_reviewer_bangbang"] = dict(switch_stages=[t for t in range(1, N) if uC[t] != uC[t-1]], kkt=kkt_check(EC)[0],
                                  J_minus_A_h2=float((EC["J"] - EA["J"]) / h**2))
print(json.dumps(res, indent=1))
