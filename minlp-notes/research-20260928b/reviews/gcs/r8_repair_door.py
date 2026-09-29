"""(a) Prop 3: REL_H <= REL + Lambda * sum_v W1(mu_in_v, mu_out_v) at an optimal REL point, and bound (4)
    OPT <= kappa_max (REL + Lambda max_P sum diam X_v), Euclidean lengths (Lambda = 1), random 2D box DAGs.
(b) Door aperture on the ring for H < 1 (note: sec(theta_door) = 1.118 'for every H')."""
import itertools
import numpy as np
import cvxpy as cp
from rgcs import *
import r5_ring_door as R

rng = np.random.default_rng(3)


def w1(A, wa, B, wb):
    C = np.array([[np.linalg.norm(a - b) for b in B] for a in A])
    P = cp.Variable(C.shape, nonneg=True)
    pr = cp.Problem(cp.Minimize(cp.sum(cp.multiply(C, P))), [cp.sum(P, 1) == wa, cp.sum(P, 0) == wb])
    pr.solve(solver="CLARABEL")
    return pr.value


def sec_ap(V):
    U = V / np.linalg.norm(V, axis=1, keepdims=True)
    a = cp.Variable(V.shape[1]); t = cp.Variable()
    cp.Problem(cp.Maximize(t), [U @ a >= t, cp.norm(a, 2) <= 1]).solve(solver="CLARABEL")
    return 1 / t.value if t.value > 1e-9 else np.inf


viol = 0; n = 0; gaps = 0
for it in range(25):
    nl = 3
    sets = {"s": Pt([0, 0])}; layers = [["s"]]
    for i in range(nl):
        L = []
        for j in range(int(rng.integers(2, 4))):
            c = np.array([4.0 * (i + 1), rng.uniform(-3, 3)]); h = rng.uniform(0.3, 1.5, 2)
            sets[f"v{i}{j}"] = Box(c - h, c + h); L.append(f"v{i}{j}")
        layers.append(L)
    sets["t"] = Pt([4.0 * (nl + 1), 0]); layers.append(["t"])
    E = [(u, v) for A, B in zip(layers[:-1], layers[1:]) for u in A for v in B]
    g = G(sets, E, "s", "t", L2)
    rl, sol = relax(g, return_vars=True)
    rh = relax(g, hull=True)
    o = opt(g)
    y = sol["y"]
    W = 0.0
    for v in sets:
        if v in ("s", "t"): continue
        ins = [e for e in g.inn[v] if y[e] > 1e-7]; outs = [f for f in g.out[v] if y[f] > 1e-7]
        if not ins or not outs: continue
        A = [sol["zp"][e] / y[e] for e in ins]; B = [sol["z"][f] / y[f] for f in outs]
        wa = np.array([y[e] for e in ins]); wb = np.array([y[f] for f in outs]); wb *= wa.sum() / wb.sum()
        W += w1(A, wa, B, wb)
    kmax = max(sec_ap(np.array([b - a for a in sets[u].V for b in sets[v].V])) for (u, v) in E)
    diam = {v: max(np.linalg.norm(p - q) for p in sets[v].V for q in sets[v].V) for v in sets}
    maxdiam = max(sum(diam[e[1]] for e in p[:-1]) for p in g.paths())
    b3 = rl + W; b4 = kmax * (rl + maxdiam)
    ok = rh <= b3 + 1e-6 and o <= b4 + 1e-6
    viol += not ok; n += 1; gaps += o > rh + 1e-5
    print(f"#{it:2d} REL={rl:.5f} REL_H={rh:.5f} OPT={o:.5f} REL+W1={b3:.5f} bound(4)={b4:.5f} kmax={kmax:.4f}" + ("" if ok else "  VIOL"))
print(f"(a) {n} instances, {gaps} with OPT>REL_H, violations: {viol}")

print("(b) door aperture on the ring for small H")
for H in [0.25, 0.5, 1.0, 2.0]:
    regions = dict(L=Box([-2, -H - 1], [-1, H + 1]), R=Box([1, -H - 1], [2, H + 1]),
                   T=Box([-2, H], [2, H + 1]), B=Box([-2, -H - 1], [2, -H]))
    und = [("L", "T"), ("T", "L"), ("L", "B"), ("B", "L"), ("T", "R"), ("R", "T"), ("B", "R"), ("R", "B")]
    gd, member = R.door_gcs(regions, und, np.array([-1.5, 0.0]), np.array([1.5, 0.0]), ["L"], ["R"])
    secmax = 0; arg = None
    for r, vs in member.items():
        for a, b in itertools.permutations(vs, 2):
            s_ = sec_ap(np.array([vb - va for va in gd.sets[a].V for vb in gd.sets[b].V]))
            if s_ > secmax: secmax, arg = s_, (r, a, b)
    od = opt(gd); rd = relax(gd, hull=True)
    print(f"H={H}: sec(theta_door)={secmax:.4f} attained at {arg}; OPT_door={od:.5f} REL_H,door={rd:.5f}")
