"""Reviewer's independent exact re-check of the single-switch lifted certificates (kappa-negative.md
Section 5.3) and of the q < 0 toy.  Uses only vtoy.py (reviewer code).

usage: OMP_NUM_THREADS=1 python3 v_single.py validate | cert K N [N ...] | qneg N [N ...]
"""
import json
import random
import sys
import time
from fractions import Fraction as Fr

from vtoy import (Toy, traj, H_entry, best_single_switch, kkt_check, stage_loss, stage_min_direct,
                  node_bound, coord_refine, terminal_loss)


def plus(k, phi2=0, R=None):
    if R is None:
        R = 3 if k > Fr(1, 2) else 2
    return Toy(a_pts=((0, 2), (1, -1)), k_pts=((0, k),), phi1=1, phi2=phi2, R=R)


def validate():
    """Closed-form stage loss vs direct evaluation of the residual; Hessian formula vs second differences;
    dJ/du_t = h sigma_t."""
    random.seed(7)
    out = {}
    for k in (Fr(1, 2), Fr(1)):
        toy = plus(k)
        N = 40
        u = [Fr(random.randint(-100, 100), 100) for _ in range(N)]
        E = traj(toy, N, u)
        P = [-k] * (N + 1)
        mism = 0
        for t in range(N):
            for (lo, hi) in ((Fr(-1), Fr(1)), (Fr(-1, 3), Fr(1, 2))):
                if not lo <= u[t] <= hi:
                    continue
                a = stage_loss(E, P, t, lo, hi, toy.R)
                b = stage_min_direct(toy, E, P, t, lo, hi)
                mism += (a != b)
        # gradient and Hessian
        gmis = 0
        for t in range(N):
            up = list(u); up[t] += 1
            gmis += (traj(toy, N, up)["J"] - E["J"] - (E["h"] * E["sig"][t] + H_entry(toy, N, E["k"], t, t) / 2)) != 0
        hmis = 0
        for (i, j) in [(3, 3), (3, 9), (9, 3), (0, 39), (20, 21), (39, 39)]:
            ui = list(u); ui[i] += 1
            uj = list(u); uj[j] += 1
            uij = list(u); uij[i] += 1; uij[j] += 1
            d2 = traj(toy, N, uij)["J"] - traj(toy, N, ui)["J"] - traj(toy, N, uj)["J"] + E["J"]
            if i == j:
                ui2 = list(u); ui2[i] += 2
                d2 = (traj(toy, N, ui2)["J"] - 2 * traj(toy, N, ui)["J"] + E["J"])
            hmis += (d2 != H_entry(toy, N, E["k"], i, j))
        out[str(k)] = dict(stage_loss_mismatches=mism, grad_mismatches=gmis, hess_mismatches=hmis)
    print(json.dumps(out))


def weakest(E):
    ok, frac = kkt_check(E)
    assert ok, ("not KKT", frac)
    if frac:
        assert len(frac) == 1
        return frac[0], "fractional"
    h = E["h"]
    t = min(range(E["N"]), key=lambda s: abs(E["sig"][s]))
    return t, "vertex"


def lifted_interval(toy, E, P, n):
    """Affine zero-loss conditions in delta = v - ubar_n for every t != n (vertex stages, kap = P_{t+1} < 0)."""
    N, h, k = E["N"], E["h"], E["k"]
    dlo, dhi = Fr(-1) - E["u"][n], Fr(1) - E["u"][n]
    for t in range(N):
        if t == n:
            continue
        ut = E["u"][t]
        assert ut in (Fr(-1), Fr(1))
        omf = Fr(-2) if ut == 1 else Fr(2)
        kap = P[t + 1]
        e = H_entry(toy, N, k, t, n) / h                    # d sigma_t / d u_n
        if kap < 0:
            c0 = h * E["sig"][t] * omf + h * h * kap * omf * omf / 2
            c1 = h * e * omf
        else:
            c0, c1 = E["sig"][t] * omf, e * omf
        if c1 == 0:
            assert c0 >= 0
            continue
        root = -c0 / c1
        if c1 > 0:
            dlo = max(dlo, root)
        else:
            dhi = min(dhi, root)
    assert dlo <= 0 <= dhi, (dlo, dhi)
    return E["u"][n] + dlo, E["u"][n] + dhi


def check_lifted_end(toy, E, P, n, v):
    """Rebuild z(v) from scratch and return the largest stage loss over t != n (u_t in U), the stage-n
    loss with u_n fixed, the terminal loss, and J(z(v))."""
    N = E["N"]
    u = list(E["u"]); u[n] = v
    Z = traj(toy, N, u)
    mx = max(stage_loss(Z, P, t, Fr(-1), Fr(1), toy.R) for t in range(N) if t != n)
    Ln = stage_loss(Z, P, n, v, v, toy.R)
    return mx, Ln, terminal_loss(toy, Z, P), Z["J"]


def outer_node(toy, E, P, n, l, r):
    """Node {u_n in [l, r]}: anchor = zbar with u_n at the end nearest ubar_n, refined by exact coordinate
    descent on stages near the switch; bound by the closed-form losses."""
    N = E["N"]
    u = list(E["u"])
    u[n] = r if E["u"][n] > r else l
    lo = [Fr(-1)] * N; hi = [Fr(1)] * N
    lo[n], hi[n] = l, r
    A = coord_refine(toy, traj(toy, N, u), lo, hi, [j for j in range(max(0, n - 4), min(N, n + 5))])
    B, losses, LN = node_bound(toy, A, P, lo, hi)
    return dict(l=float(l), r=float(r), anchor_un=float(A["u"][n]),
                anchor_minus_J_h2=float((A["J"] - E["J"]) / E["h"] ** 2),
                bound_minus_J_h2=float((B - E["J"]) / E["h"] ** 2), certified=bool(B >= E["J"]),
                max_loss_h2=float(max(losses) / E["h"] ** 2), terminal_loss=float(LN))


def cert(k, N, phi2=0):
    t0 = time.time()
    toy = plus(k, phi2)
    E = best_single_switch(toy, N)
    n, kind = weakest(E)
    h = E["h"]
    P = [-k] * (N + 1)
    lo = [Fr(-1)] * N; hi = [Fr(1)] * N
    B0, losses, LN = node_bound(toy, E, P, lo, hi)
    rec = dict(k=float(k), N=N, J=float(E["J"]), n=n, kind=kind, u_n=float(E["u"][n]),
               sig_over_h=[round(float(E["sig"][t] / h), 4) for t in range(n - 2, n + 3)],
               plain_gap_h2=float((E["J"] - B0) / h ** 2),
               failing=[(t, float(v / h ** 2)) for t, v in enumerate(losses) if v > 0])
    if B0 == E["J"]:
        rec["certificate"] = "plain family exact"
    else:
        V = lifted_interval(toy, E, P, n)
        ends = [check_lifted_end(toy, E, P, n, v) for v in V]
        Hnn = H_entry(toy, N, E["k"], n, n)
        # J(z(v)) = J + h sig_n (v - u_n) + Hnn (v - u_n)^2 / 2; check the formula at both ends
        form_ok = all(e[3] == E["J"] + h * E["sig"][n] * (v - E["u"][n]) + Hnn * (v - E["u"][n]) ** 2 / 2
                      for e, v in zip(ends, V))
        cands = list(V)
        if Hnn > 0:
            vs = E["u"][n] - h * E["sig"][n] / Hnn
            if V[0] <= vs <= V[1]:
                cands.append(vs)
        Blift = min(E["J"] + h * E["sig"][n] * (v - E["u"][n]) + Hnn * (v - E["u"][n]) ** 2 / 2 for v in cands)
        rec.update(V=[float(V[0]), float(V[1])], ends_max_loss=[float(e[0]) for e in ends],
                   ends_stage_n_loss=[float(e[1]) for e in ends], ends_terminal=[float(e[2]) for e in ends],
                   formula_ok=form_ok, Hnn_h2=float(Hnn / h ** 2), lifted_minus_J=float(Blift - E["J"]))
        outs = []
        if V[0] > -1:
            outs.append(outer_node(toy, E, P, n, Fr(-1), V[0]))
        if V[1] < 1:
            outs.append(outer_node(toy, E, P, n, V[1], Fr(1)))
        rec["outer"] = outs
        rec["certified"] = (Blift >= E["J"] and all(e[0] == 0 and e[1] == 0 and e[2] == 0 for e in ends)
                            and all(o["certified"] for o in outs))
    rec["time"] = round(time.time() - t0, 1)
    print(json.dumps(rec), flush=True)
    return rec


if __name__ == "__main__":
    what = sys.argv[1]
    if what == "validate":
        validate()
    elif what == "cert":
        k = Fr(sys.argv[2])
        for N in sys.argv[3:]:
            cert(k, int(N))
