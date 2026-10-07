"""Reviewer's exact box branch and bound for the two-switch toy (kappa-negative.md Section 9.1), own code.

Node = box {u_t in [lo_t, hi_t]} (only a few stages restricted; others in [-1, 1]).  Per node:
  anchor = target point clipped into the box, refined by exact coordinate descent near both switches;
  bound 1 (fixed) = calibration bound with P = -k anchored at the anchor;
  bound 2 (lifted, one stage w) = min over v in V_w of J(z(v)), valid on {u_w in V_w} x (rest of box),
    where V_w is the exact interval on which every other stage of z(v) has zero loss over the node box
    (all other anchor controls must be at a bound of the node box).
  Split: on the worst stage, at the anchor value if interior, else at the midpoint.
usage: python3 v_two_bb.py K f:t1 f:t2 N m1 v1 m2 v2   (target point: pattern(N, m1, v1, m2, v2))
"""
import json
import sys
import time
from fractions import Fraction as Fr

from vtoy import traj, H_entry, kkt_check, node_bound, stage_loss, coord_refine
from v_two import toy2, pattern


def lifted_interval_box(toy, A, P, w, lo, hi):
    N, h, k = A["N"], A["h"], A["k"]
    dlo, dhi = lo[w] - A["u"][w], hi[w] - A["u"][w]
    for t in range(N):
        if t == w:
            continue
        ut = A["u"][t]
        if ut == hi[t]:
            omf = lo[t] - ut
        elif ut == lo[t]:
            omf = hi[t] - ut
        else:
            return None
        kap = P[t + 1]
        e = H_entry(toy, N, k, t, w) / h
        if kap < 0:
            c0, c1 = h * A["sig"][t] * omf + h * h * kap * omf * omf / 2, h * e * omf
        else:
            c0, c1 = A["sig"][t] * omf, e * omf
        if c0 < 0:
            return None
        if c1 == 0:
            continue
        root = -c0 / c1
        if c1 > 0:
            dlo = max(dlo, root)
        else:
            dhi = min(dhi, root)
    if not dlo <= 0 <= dhi:
        return None
    assert h + P[w + 1] - P[w] >= 0
    return A["u"][w] + dlo, A["u"][w] + dhi


def main():
    k = Fr(sys.argv[1])
    t1, t2 = [Fr(float(s[2:])) if s.startswith('f:') else Fr(s) for s in sys.argv[2:4]]
    N, m1, v1, m2, v2 = int(sys.argv[4]), int(sys.argv[5]), Fr(sys.argv[6]), int(sys.argv[7]), Fr(sys.argv[8])
    t0 = time.time()
    toy = toy2(k, t1, t2)
    h = toy.T / N
    # target: the pattern with the given switch stages, fractional values re-optimized exactly (1-D each)
    Z = traj(toy, N, pattern(N, m1, v1, m2, v2))
    Z = coord_refine(toy, Z, [Fr(-1)] * N, [Fr(1)] * N, [m1, m2])
    ok, frac = kkt_check(Z)
    assert ok
    target = Z["J"]
    P = [-k] * (N + 1)
    near = sorted(set(range(m1 - 4, m1 + 5)) | set(range(m2 - 4, m2 + 5)))
    stack = [dict()]
    nodes = []
    better = None
    while stack and len(nodes) < 400:
        box = stack.pop()
        lo = [Fr(-1)] * N; hi = [Fr(1)] * N
        for t, (a, b) in box.items():
            lo[t], hi[t] = a, b
        u = [min(hi[t], max(lo[t], Z["u"][t])) for t in range(N)]
        A = coord_refine(toy, traj(toy, N, u), lo, hi, near)
        if A["J"] < target:
            better = (float((A["J"] - target) / h ** 2), {t: float(A["u"][t]) for t in near if A["u"][t] != Z["u"][t]})
        B, losses, LN = node_bound(toy, A, P, lo, hi)
        rec = dict(box={t: [float(a), float(b)] for t, (a, b) in box.items()},
                   anchor_minus_target_h2=float((A["J"] - target) / h ** 2),
                   fixed_minus_target_h2=float((B - target) / h ** 2))
        if B >= target:
            rec["kind"] = "fixed"
            nodes.append(rec)
            continue
        w = max(range(N), key=lambda t: losses[t])
        V = lifted_interval_box(toy, A, P, w, lo, hi)
        if V is not None and V[1] > V[0]:
            Hww = H_entry(toy, N, A["k"], w, w)
            cands = list(V)
            if Hww > 0:
                vs = A["u"][w] - h * A["sig"][w] / Hww
                if V[0] <= vs <= V[1]:
                    cands.append(vs)
            Bl = min(A["J"] + h * A["sig"][w] * (v - A["u"][w]) + Hww * (v - A["u"][w]) ** 2 / 2 for v in cands)
            if Bl >= target:
                # independent end check: rebuild z(v) at both ends, all other stages zero loss over the box
                for v in V:
                    uu = list(A["u"]); uu[w] = v
                    Zv = traj(toy, N, uu)
                    assert all(stage_loss(Zv, P, t, lo[t], hi[t], toy.R) == 0 for t in range(N) if t != w)
                rec.update(kind="lifted", stage=w, V=[float(V[0]), float(V[1])], lifted_minus_target_h2=float((Bl - target) / h ** 2))
                nodes.append(rec)
                for (a, b) in ((lo[w], V[0]), (V[1], hi[w])):
                    if b > a:
                        stack.append({**box, w: (a, b)})
                continue
        uw = A["u"][w]
        m = uw if lo[w] < uw < hi[w] else (lo[w] + hi[w]) / 2
        rec.update(kind="split", stage=w, at=float(m), worst_loss_h2=float(losses[w] / h ** 2))
        nodes.append(rec)
        stack.append({**box, w: (lo[w], m)})
        stack.append({**box, w: (m, hi[w])})
    leaves = [q for q in nodes if q["kind"] != "split"]
    out = dict(k=float(k), t1=float(t1), t2=float(t2), N=N, target_frac=frac,
               target_u_frac=[float(Z["u"][t]) for t in frac], complete=not stack, n_nodes=len(nodes),
               n_leaves=len(leaves), all_leaves_ok=all((q.get("fixed_minus_target_h2", -1) >= 0) or q["kind"] == "lifted" for q in leaves),
               better_point=better, nodes=nodes, time=round(time.time() - t0, 1))
    print(json.dumps(out), flush=True)


if __name__ == "__main__":
    main()
