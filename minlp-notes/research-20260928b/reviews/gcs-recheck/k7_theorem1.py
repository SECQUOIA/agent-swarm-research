"""Independent audit of Theorem 1 (Jensen-defect rounding on acyclic graphs) by exact enumeration
of the Markov chain built from a REL_H solution.

Chain: first edge f w.p. y_f; after e=(u,v), v != t, next edge f w.p. lam_ef / y_e; positions
s at zbar_f, internal v at wbar_ef, t at zbar'_e.  Checks, per instance:
  Pr(e in P) = y_e;  Pr(d,e consecutive) = lam_de;  Pr(d,e,f consecutive) = lam_de lam_ef / y_e;
  E[x_u | e] = zbar_e, E[x_v | e] = zbar'_e;  E[cost] = closed form;
  REL <= REL_H <= OPT <= reopt(best pair path) <= min pair path <= E[cost] <= sum y cav
      <= REL_H + sum y Delta <= REL_H + max_P sum Delta.
Solver noise: pair variables with lam < 1e-7 are dropped, transition rows renormalised, and
barycentres projected onto their sets; tolerances are 1e-5 (relative where appropriate)."""
import sys
import itertools
import numpy as np
from rc import PSet, pt, box, G, relax, opt_exact, path_cost, lval, cav, jensen_defect, longest_path_dag, topo

TOL = 1e-5


def rand_set(rng, c, dim, big):
    k = rng.integers(0, 4)
    sc = big * rng.uniform(0.3, 1.0)
    if k == 0:
        return pt(*c)
    if k == 1:  # segment
        d = rng.normal(size=dim)
        return PSet(V=[c - sc * d / np.linalg.norm(d), c + sc * d / np.linalg.norm(d)])
    if k == 2 and dim >= 2:  # triangle
        return PSet(V=c + sc * rng.normal(size=(3, dim)))
    return box(c - sc * rng.uniform(0.3, 1, dim), c + sc * rng.uniform(0.3, 1, dim))


def rand_len(rng, dim):
    r = rng.random()
    if r < 0.35:
        return "l2"
    if r < 0.6:
        return "sq"
    if r < 0.8:
        return "l1"
    return ("aff", rng.normal(size=dim), rng.normal(size=dim), float(rng.normal()))


def instance(rng, big, rich=False):
    dim = int(rng.integers(1, 4))
    lo = 2 if rich else 1
    layers = [1] + [int(rng.integers(lo, 4)) for _ in range(int(rng.integers(2, 4)))] + [1]
    names, sets = [], {}
    for li, k in enumerate(layers):
        row = []
        for j in range(k):
            nm = f"{li}{j}"
            c = np.r_[2.0 * li, rng.normal(size=dim - 1) * 1.5] if dim > 1 else np.array([2.0 * li + 0.5 * rng.normal()])
            sets[nm] = pt(*c) if li in (0, len(layers) - 1) else rand_set(rng, c, dim, big)
            row.append(nm)
        names.append(row)
    E = []
    for li in range(len(layers) - 1):
        for a in names[li]:
            for b in names[li + 1]:
                if rich or rng.random() < 0.85:
                    E.append((a, b))
            if li + 2 < len(layers) and rng.random() < 0.25:   # skip edges: non-layered DAG
                E.append((a, names[li + 2][rng.integers(len(names[li + 2]))]))
    E = list(dict.fromkeys(E))
    g = G(sets, E, names[0][0], names[-1][0], {})
    g.len = {e: rand_len(rng, dim) for e in E}
    return g


def random_objective(rng):
    import cvxpy as cp

    def obj(g, y, z, zp, lam, w):
        terms = [cp.square(y[e] - rng.uniform(0, 1)) for e in g.E]
        for (e, f), wv in w.items():
            V = g.sets[e[1]].V
            p = rng.dirichlet(np.ones(len(V))) @ V
            terms.append(cp.sum_squares(wv - lam[(e, f)] * p))
        for e in g.E:
            terms.append(0.1 * cp.square(sum(lam[(e, f)] for f in g.out[e[1]] if (e, f) in lam) - rng.uniform(0, 1))
                         if any((e, f) in lam for f in g.out[e[1]]) else 0)
        return sum(terms)
    return obj


def sym_instance(rng, big):
    """2D instance invariant under x2 -> -x2: axis-symmetric sets or mirrored pairs; full layers."""
    R = np.diag([1.0, -1.0])
    nl = int(rng.integers(2, 4))
    names, sets = [["s"]], {"s": pt(0.0, 0.0)}
    for li in range(1, nl + 1):
        x = 2.0 * li
        if rng.random() < 0.4:   # one axis-symmetric set
            hw = big * rng.uniform(0.3, 1.0, 2)
            if rng.random() < 0.5:
                sets[f"{li}a"] = box([x - hw[0], -hw[1]], [x + hw[0], hw[1]])
            else:
                sets[f"{li}a"] = PSet(V=[[x - hw[0], 0.0], [x + hw[0], hw[1]], [x + hw[0], -hw[1]]])
            names.append([f"{li}a"])
        else:                    # mirrored pair
            c = np.array([x, rng.uniform(0.3, 2.0)])
            S = rand_set(rng, c, 2, big * 0.6)
            sets[f"{li}p"] = S
            sets[f"{li}m"] = PSet(V=S.V @ R)
            names.append([f"{li}p", f"{li}m"])
    names.append(["t"])
    sets["t"] = pt(2.0 * (nl + 1), 0.0)
    E = [(a, b) for li in range(len(names) - 1) for a in names[li] for b in names[li + 1]]
    kinds = ["l2", "sq", "l1"]
    lk = {li: kinds[rng.integers(3)] for li in range(len(names) - 1)}
    layer = {v: li for li, row in enumerate(names) for v in row}
    g = G(sets, E, "s", "t", {e: lk[layer[e[0]]] for e in E})
    return g


def audit(g, degree, rng=None):
    """rng given: audit a random fractional feasible REL_H point (parts 1-3 of Theorem 1);
    otherwise audit the optimal point and the full chain of consequences."""
    if rng is None:
        val_h, sol, st = relax(g, hull=True, degree=degree)
        val_r, _, st_r = relax(g, hull=False, degree=degree)
    else:
        _, sol, st = relax(g, hull=True, degree=degree, objective=random_objective(rng))
    if sol is None:
        return None
    y, z, zp, lam, w = sol["y"], sol["z"], sol["zp"], sol["lam"], sol["w"]
    if rng is not None:  # true objective value of this feasible point
        val_h = sum(y[e] * lval(g.len[e], z[e] / y[e], zp[e] / y[e]) for e in g.E if y[e] > 1e-9)
        val_r = -np.inf
    s, t = g.s, g.t
    live = {e: y[e] for e in g.E if y[e] > 1e-7}
    # transitions from e (head v != t) with renormalised rows; positions
    trans, pos = {}, {}
    for e in live:
        v = e[1]
        if v == t:
            continue
        row = {f: lam[(e, f)] for f in g.out[v] if lam.get((e, f), 0) > 1e-7}
        tot = sum(row.values())
        trans[e] = {f: p / tot for f, p in row.items()}
        for f in row:
            pos[(e, f)] = g.sets[v].proj(w[(e, f)] / lam[(e, f)])
    start = {f: y[f] for f in g.out[s] if f in live}
    tot = sum(start.values())
    start = {f: p / tot for f, p in start.items()}
    zbar = {e: g.sets[e[0]].proj(z[e] / y[e]) for e in live}
    zpbar = {e: g.sets[e[1]].proj(zp[e] / y[e]) for e in live}

    def place(prev, e, nxt):
        xu = zbar[e] if prev is None else pos[(prev, e)]
        xv = zpbar[e] if nxt is None else pos[(e, nxt)]
        return xu, xv

    # exact enumeration of trajectories
    traj = []

    def dfs(seq, p):
        e = seq[-1]
        if e[1] == t:
            traj.append((list(seq), p))
            return
        for f, q in trans[e].items():
            seq.append(f)
            dfs(seq, p * q)
            seq.pop()

    for f, p in start.items():
        dfs([f], p)
    Pe, Pde, Pdef = {}, {}, {}
    Ex_u, Ex_v = {}, {}
    Ecost, best = 0.0, (np.inf, None)
    for seq, p in traj:
        cost = 0.0
        for k, e in enumerate(seq):
            prev = seq[k - 1] if k > 0 else None
            nxt = seq[k + 1] if k + 1 < len(seq) else None
            xu, xv = place(prev, e, nxt)
            cost += lval(g.len[e], xu, xv)
            Pe[e] = Pe.get(e, 0) + p
            Ex_u[e] = Ex_u.get(e, 0) + p * xu
            Ex_v[e] = Ex_v.get(e, 0) + p * xv
            if prev is not None:
                Pde[(prev, e)] = Pde.get((prev, e), 0) + p
                if nxt is not None:
                    Pdef[(prev, e, nxt)] = Pdef.get((prev, e, nxt), 0) + p
        Ecost += p * cost
        if cost < best[0]:
            best = (cost, seq)
    err = {}
    err["marg"] = max(abs(Pe.get(e, 0) - y[e]) for e in g.E)
    err["pair"] = max([abs(Pde.get(k, 0) - lam[k]) for k in lam] + [0])
    err["triple"] = max([abs(p - lam[(d, e)] * lam[(e, f)] / y[e]) for (d, e, f), p in Pdef.items()] + [0])
    # unnormalised form E[x_u 1{e in P}] = z_e (normalising by tiny y_e only amplifies solver noise)
    err["mean"] = max(max(np.max(np.abs(Ex_u[e] - z[e])), np.max(np.abs(Ex_v[e] - zp[e]))) for e in Pe)
    # closed form of E[cost]: sum_e sum_{d,f} P(d|e) P(f|e) y_e l_e(...)
    closed = 0.0
    for e in live:
        prevs = [(None, 1.0)] if e[0] == s else [(d, lam[(d, e)] / y[e]) for d in g.inn[e[0]] if lam.get((d, e), 0) > 1e-7]
        nexts = [(None, 1.0)] if e[1] == t else [(f, q) for f, q in trans[e].items()]
        pn = sum(q for _, q in prevs)
        for d, pd in prevs:
            for f, pf in nexts:
                xu, xv = place(d, e, f)
                closed += y[e] * (pd / pn) * pf * lval(g.len[e], xu, xv)
    err["closed"] = abs(closed - Ecost) / max(1, abs(Ecost))
    # pair-graph DP (independent of the enumeration)
    node_cost = {}
    order = topo(g)
    rank = {v: i for i, v in enumerate(order)}
    pairs = [(None, f) for f in start] + [k for k in pos]
    pairs.sort(key=lambda k: rank[k[1][0]])
    dist = {(None, f): 0.0 for f in start}
    pair_min = np.inf
    for (d, e) in pairs:
        if (d, e) not in dist:
            continue
        if e[1] == t:
            xu, xv = place(d, e, None)
            pair_min = min(pair_min, dist[(d, e)] + lval(g.len[e], xu, xv))
            continue
        for f in trans[e]:
            xu, xv = place(d, e, f)
            c = dist[(d, e)] + lval(g.len[e], xu, xv)
            if c < dist.get((e, f), np.inf):
                dist[(e, f)] = c
    # re-optimised positions on the best trajectory
    vpath = [best[1][0][0]] + [e[1] for e in best[1]]
    reopt = path_cost(g, vpath)[0]
    opt = opt_exact(g)[0]
    ycav, yDelta = 0.0, 0.0
    Delta = {e: jensen_defect(g, e) for e in g.E}
    for e in live:
        cv, slack = cav(g, e, zbar[e], zpbar[e])
        ycav += y[e] * cv
        yDelta += y[e] * Delta[e]
    maxP = longest_path_dag(g, Delta)
    head = [("REL", val_r), ("REL_H", val_h)] if rng is None else []   # any feasible point: no lower-bound links
    chain = head + [("OPT", opt), ("reopt", reopt), ("pairDP", pair_min), ("minTraj", best[0]),
             ("E", Ecost), ("sum y cav", ycav), ("REL_H+sum yD", val_h + yDelta), ("REL_H+maxP", val_h + maxP)]
    viol = []
    for (a, va), (b, vb) in zip(chain[:-1], chain[1:]):
        if va > vb + TOL * max(1, abs(vb)):
            viol.append(f"{a}={va:.6f}>{b}={vb:.6f}")
    if abs(pair_min - best[0]) > TOL * max(1, abs(best[0])):
        viol.append(f"pairDP {pair_min} != minTraj {best[0]}")
    for k, v in err.items():
        if v > 1e-4:
            viol.append(f"{k} err {v:.2e}")
    return dict(chain=dict(chain), err=err, viol=viol, ntraj=len(traj), gap=opt - val_h,
                hull_nontrivial=sum(1 for v in g.sets if len([e for e in g.inn[v] if e in live]) >= 2 and len([f for f in g.out[v] if f in live]) >= 2),
                negative=any(isinstance(g.len[e], tuple) for e in g.E))


def main(seed=0, n=40, big=1.0, mode="opt"):
    rng = np.random.default_rng(seed)
    nviol = ngap = nhull = ndone = 0
    maxerr = {}
    for it in range(n):
        g = sym_instance(rng, big) if mode == "sym" else instance(rng, big, rich=(mode == "random"))
        from rc import simple_paths
        if not simple_paths(g):
            continue
        degree = bool(rng.random() < 0.5)
        r = audit(g, degree, rng if mode == "random" else None)
        if r is None:
            print(f"  instance {it}: relaxation failed")
            continue
        ndone += 1
        for k, v in r["err"].items():
            maxerr[k] = max(maxerr.get(k, 0), v)
        nviol += bool(r["viol"])
        ngap += r["gap"] > 1e-5
        nhull += r["hull_nontrivial"] > 0
        if r["viol"]:
            print(f"  instance {it} VIOLATION: {r['viol']}")
    print(f"[{mode}] seed={seed} big={big}: instances={ndone}, with violations={nviol}, with OPT>REL_H={ngap}, "
          f"with a live vertex of in/out-degree>=2={nhull}; max errors: " + ", ".join(f"{k}={v:.1e}" for k, v in maxerr.items()))


if __name__ == "__main__":
    a = sys.argv[1:]
    main(int(a[0]) if a else 0, int(a[1]) if len(a) > 1 else 40, float(a[2]) if len(a) > 2 else 1.0, a[3] if len(a) > 3 else "opt")
