"""Theorem 1 audit on random DAGs with exact enumeration of the Markov chain.

For each instance: solve REL and REL_H (with or without degree constraints),
enumerate every trajectory of the chain with its probability, and check
  * Pr(e in P) = y_e, Pr(d,e consecutive) = lambda_de,
  * conditional independence of previous and next edge given e,
  * E[x_u | e] = zbar_e, E[x_v | e] = zbar'_e,
  * closed form E[cost] = sum_e sum_{d,f} lam_de lam_ef / y_e * l_e(...),
  * REL <= REL_H <= OPT <= min over chain paths <= E[cost] <= sum y cav
        <= REL_H + sum y Delta <= REL_H + max_P sum Delta.
Lengths are drawn from l2, sq, l1 and random affine (possibly negative) ones.
Usage: python3 r2_theorem1.py seed n_instances scale
"""
import sys
import numpy as np
from rgcs import *

seed = int(sys.argv[1]) if len(sys.argv) > 1 else 0
NI = int(sys.argv[2]) if len(sys.argv) > 2 else 20
SCALE = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
HARD = len(sys.argv) > 4 and sys.argv[4] == "hard"
rng = np.random.default_rng(seed)
TOL = 2e-5


def rand_set(dim, center, scale):
    k = rng.choice(["pt", "box", "tri", "seg"], p=[0.2, 0.4, 0.25, 0.15])
    if HARD:
        k = rng.choice(["box", "tri"], p=[0.6, 0.4])
    if k == "pt" or (k == "tri" and dim < 2):
        return Pt(center)
    if k == "box":
        h = rng.uniform(0.1, 1.0, dim) * scale
        return Box(center - h, center + h)
    if k == "seg":
        d = rng.standard_normal(dim)
        d *= scale / np.linalg.norm(d)
        return Seg(center - d, center + d)
    # random triangle in the first two coordinates (dim >= 2)
    P = center + rng.standard_normal((3, dim)) * scale
    if dim > 2:
        P[:, 2:] = center[2:]
    # H-rep via hull of three points in 2D coordinates + equalities in others
    P2 = P[:, :2]
    cen = P2.mean(0)
    A, b = [], []
    for i in range(3):
        p1, p2 = P2[i], P2[(i + 1) % 3]
        nrm = np.array([p2[1] - p1[1], -(p2[0] - p1[0])])
        if nrm @ (cen - p1) > 0:
            nrm = -nrm
        row = np.zeros(dim)
        row[:2] = nrm
        A.append(row)
        b.append(nrm @ p1)
    for j in range(2, dim):
        row = np.zeros(dim)
        row[j] = 1
        A.append(row)
        b.append(center[j])
        A.append(-row)
        b.append(-center[j])
    return Poly(np.array(A), np.array(b), P)


def rand_instance():
    dim = int(rng.integers(1, 4))
    nl = int(rng.integers(2, 4))
    widths = [int(rng.integers(1, 4)) for _ in range(nl)]
    if HARD:
        dim = 2
        widths = [int(rng.integers(2, 4)) for _ in range(nl)]
        hard_len = rng.choice(["sq", "l2"])
    sets = {"s": Pt(np.zeros(dim))}
    layers = [["s"]]
    for i, wdt in enumerate(widths):
        L = []
        for j in range(wdt):
            name = f"v{i}_{j}"
            c = np.zeros(dim)
            c[0] = 2.0 * (i + 1)
            if dim > 1:
                c[1:] = rng.standard_normal(dim - 1) * 1.5
            sets[name] = rand_set(dim, c, SCALE)
            L.append(name)
        layers.append(L)
    ct = np.zeros(dim)
    ct[0] = 2.0 * (nl + 1)
    sets["t"] = Pt(ct)
    layers.append(["t"])
    E = []
    for a, b in zip(layers[:-1], layers[1:]):
        for u in a:
            outs = [v for v in b if rng.random() < 0.8] or [b[int(rng.integers(len(b)))]]
            E += [(u, v) for v in outs]
    # skip edges (still a DAG)
    for i in range(len(layers) - 2):
        for u in layers[i]:
            if rng.random() < 0.25:
                v = layers[i + 2][int(rng.integers(len(layers[i + 2])))]
                if (u, v) not in E:
                    E.append((u, v))
    # make sure every vertex with in-edges has out-edges and vice versa (fix dead ends)
    for L_i, L in enumerate(layers[1:-1], start=1):
        for v in L:
            if not any(e[0] == v for e in E):
                E.append((v, layers[L_i + 1][0]))
            if not any(e[1] == v for e in E):
                E.append((layers[L_i - 1][0], v))
    lens = {}
    for e in E:
        k = rng.choice(["l2", "sq", "l1", "aff"], p=[0.35, 0.25, 0.2, 0.2])
        if HARD:
            k = hard_len
        if k == "aff":
            lens[e] = Len("aff", c=rng.standard_normal(dim), d=rng.standard_normal(dim), b0=float(rng.standard_normal()))
        else:
            lens[e] = Len(k)
    return G(sets, E, "s", "t", lens)


def enumerate_chain(g, sol, tol=1e-6):
    P = pair_positions(g, sol, tol)
    nxt = {}
    for (d, e), (l, x) in P.items():
        nxt.setdefault(d, []).append((e, l, x))
    # normalized transition probabilities (row sums of the cleaned lambdas)
    y = {e: sum(l for (_, l, _) in nxt.get(e, [])) for e in g.E}
    traj = []  # list of (prob, [edges], [positions of vertices])

    def rec(prob, edges, pos, e):
        # current edge e entered; pos holds positions so far (tail of e already placed)
        for (f, l, x) in nxt.get(e, []):
            p = prob * l / y[e]
            if f == "*":
                traj.append((p, edges, pos + [x]))
            else:
                rec(p, edges + [f], pos + [x], f)

    for (d, e), (l, x) in P.items():
        if d == "*":
            rec(l, [e], [x], e)
    return traj


viol = {k: 0 for k in ["order", "marg", "pair", "indep", "means", "closed"]}
worst = {k: 0.0 for k in viol}
n_gap = 0
for it in range(NI):
    g = rand_instance()
    deg = bool(rng.random() < 0.5)
    rl = relax(g, deg=deg)
    rh, sol = relax(g, hull=True, deg=deg, return_vars=True)
    o = opt(g)
    if rh is None or o is None:
        print("solver issue", it)
        continue
    traj = enumerate_chain(g, sol)
    y = sol["y"]
    tot = sum(p for p, _, _ in traj)
    # marginals
    pe, ppair, pos_u, pos_v, trip = {}, {}, {}, {}, {}
    Ecost = 0.0
    minpath = np.inf
    for p, edges, pos in traj:
        c = sum(g.len[e].val(pos[i], pos[i + 1]) for i, e in enumerate(edges))
        Ecost += p * c
        minpath = min(minpath, c)
        for i, e in enumerate(edges):
            pe[e] = pe.get(e, 0) + p
            pos_u[e] = pos_u.get(e, 0) + p * pos[i]
            pos_v[e] = pos_v.get(e, 0) + p * pos[i + 1]
            d = edges[i - 1] if i > 0 else "*"
            f = edges[i + 1] if i + 1 < len(edges) else "*"
            trip[(d, e, f)] = trip.get((d, e, f), 0) + p
            if i > 0:
                ppair[(d, e)] = ppair.get((d, e), 0) + p
    err_marg = max([abs(tot - 1)] + [abs(pe.get(e, 0) - y[e]) for e in g.E])
    err_pair = max([abs(ppair.get(k, 0) - v) for k, v in sol["lam"].items()] + [0])
    err_means = 0.0
    for e in g.E:
        if y[e] > 1e-4 and e in pe:
            err_means = max(err_means, np.max(np.abs(pos_u[e] / pe[e] - sol["z"][e] / y[e])),
                            np.max(np.abs(pos_v[e] / pe[e] - sol["zp"][e] / y[e])))
    # conditional independence: P(d,e,f) = P(d,e) P(e,f) / y_e
    err_ind = 0.0
    lam_ext = dict(sol["lam"])
    for e in g.out[g.s]:
        lam_ext[("*", e)] = y[e]
    for e in g.inn[g.t]:
        lam_ext[(e, "*")] = y[e]
    for (d, e, f), p in trip.items():
        err_ind = max(err_ind, abs(p - lam_ext.get((d, e), 0) * lam_ext.get((e, f), 0) / y[e]))
    Eclosed, mix = chain_stats(g, sol)
    # Jensen bound pieces
    ycav = 0.0
    yD = 0.0
    Dl = {}
    for e in g.E:
        Vu, Vv = g.sets[e[0]].V, g.sets[e[1]].V
        Dl[e] = delta_max(g.len[e], Vu, Vv)
        if y[e] > 1e-7:
            ycav += y[e] * cav_lp(g.len[e], Vu, Vv, sol["z"][e] / y[e], sol["zp"][e] / y[e])
            yD += y[e] * Dl[e]
    maxPD = max(sum(Dl[e] for e in p) for p in g.paths())
    chain = [rl, rh, o, minpath, Ecost, ycav, rh + yD, rh + maxPD]
    names = ["REL", "REL_H", "OPT", "minpath", "E", "ycav", "REL_H+yD", "REL_H+maxPD"]
    bad = [f"{names[i]}>{names[i+1]}" for i in range(len(chain) - 1)
           if chain[i] > chain[i + 1] + TOL * max(1, abs(chain[i + 1]))]
    viol["order"] += bool(bad)
    for k, v in [("marg", err_marg), ("pair", err_pair), ("indep", err_ind), ("means", err_means),
                 ("closed", abs(Eclosed - Ecost))]:
        worst[k] = max(worst[k], v)
        viol[k] += v > 1e-4
    n_gap += o > rh + 1e-5
    print(f"#{it:2d} |V|={len(g.sets):2d} |E|={len(g.E):2d} deg={int(deg)} ntraj={len(traj):4d} "
          + " ".join(f"{n}={v:.5f}" for n, v in zip(names, chain)) + (f"  VIOL {bad}" if bad else ""), flush=True)
print("violations:", viol)
print("worst errors:", {k: f"{v:.2e}" for k, v in worst.items()})
print("instances with OPT > REL_H:", n_gap, "of", NI)
