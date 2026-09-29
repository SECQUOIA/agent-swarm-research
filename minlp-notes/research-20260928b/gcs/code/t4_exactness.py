"""T4: exactness classes and REL vs REL_H separations.

(a) affine lengths, random DAGs of boxes/triangles:            REL_H = OPT  (Cor. A); REL may be < OPT
(b) nonnegative affine crossing at a square:                  REL = 0 < REL_H = OPT = 2
(c) 1D, every edge joins disjoint intervals, lengths a w+ + b w-:  REL = REL_H = OPT (acyclic);
    cyclic graphs with a common (a, b) and no degree constraints:  REL = OPT
(d) triangles (2-simplices), Euclidean and squared lengths:     REL = REL_H (Prop. 2(ii))
(e) crossing family (square vertex, R -> infinity): closed forms
      OPT = 2*sqrt2*R + 2*sqrt(R^2 - sqrt2*R + 1),  REL <= 2*sqrt2*R + 2R - 2*sqrt2,
    so OPT/REL - 1 = Theta(1/R) while OPT/REL_H - 1 <= sec(theta) - 1 = O(1/R^2).
Usage: python3 t4_exactness.py [seed]
"""
import sys
import numpy as np
from gcslib import *

rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 0)


def rand_dag_sets(d, L, k, tri=False, w=(0.2, 1.5)):
    sets = {"s": point(np.zeros(d))}
    layers = []
    for i in range(1, L + 1):
        lay = []
        for j in range(k):
            c = np.r_[2.0 * i, rng.uniform(-2, 2, d - 1)]
            if tri:
                sets[f"{i}_{j}"] = poly_from_vertices2d(c + rng.uniform(-1.2, 1.2, (3, 2)))
            else:
                ww = rng.uniform(*w, d)
                sets[f"{i}_{j}"] = box(c - ww, c + ww)
            lay.append(f"{i}_{j}")
        layers.append(lay)
    sets["t"] = point(np.r_[2.0 * (L + 1), np.zeros(d - 1)])
    E = [("s", v) for v in layers[0]] + [(v, "t") for v in layers[-1]]
    for a, b in zip(layers, layers[1:]):
        E += [(u, v) for u in a for v in b]
    for a, b in zip(layers, layers[2:]):
        E += [(u, v) for u in a for v in b if rng.random() < 0.3]
    return sets, E


# (a)
gl, gh = [], []
for trial in range(30):
    sets, E = rand_dag_sets(2, int(rng.integers(2, 4)), int(rng.integers(2, 4)), tri=rng.random() < 0.3)
    costs = {e: Cost("aff", c=rng.standard_normal(2), d=rng.standard_normal(2), b0=0.0) for e in E}
    g = GCS(sets, E, "s", "t", costs)
    r, rh, o = relax(g), relax(g, hull=True), opt(g)
    gl.append(o - r)
    gh.append(o - rh)
gl, gh = np.array(gl), np.array(gh)
print(f"(a) affine: n=30 max|OPT-REL_H|={np.abs(gh).max():.2e}; #(OPT-REL>1e-5)={np.sum(gl>1e-5)}, max(OPT-REL)={gl.max():.4f}")

# (b)
Z = np.zeros(2)
sets = {"s": point(Z), "u1": point(Z), "u2": point(Z), "v": box([-1, -1], [1, 1]), "w1": point(Z), "w2": point(Z), "t": point(Z)}
E = [("s", "u1"), ("s", "u2"), ("u1", "v"), ("u2", "v"), ("v", "w1"), ("v", "w2"), ("w1", "t"), ("w2", "t")]
costs = {e: Cost("zero") for e in E}
costs[("u1", "v")] = Cost("aff", c=Z, d=-np.array([1.0, 1.0]), b0=2.0)
costs[("u2", "v")] = Cost("aff", c=Z, d=np.array([1.0, 1.0]), b0=2.0)
costs[("v", "w1")] = Cost("aff", c=-np.array([1.0, -1.0]), d=Z, b0=2.0)
costs[("v", "w2")] = Cost("aff", c=np.array([1.0, -1.0]), d=Z, b0=2.0)
g = GCS(sets, E, "s", "t", costs)
print(f"(b) nonnegative affine crossing: REL={relax(g):.6f} REL_H={relax(g, hull=True):.6f} OPT={opt(g):.6f}")

# (c) 1D disjoint intervals
bad_acyc, bad_cyc, hd = 0, 0, 0.0
for trial in range(40):
    nv = int(rng.integers(5, 8))
    iv = []
    x = 0.0
    for v in range(nv):
        w = rng.uniform(0, 0.8)
        c = rng.uniform(-6, 6)
        iv.append((c - w, c + w))
    sets = {v: box([iv[v][0]], [iv[v][1]]) for v in range(nv)}
    sets[0] = point([iv[0][0]])
    sets[nv - 1] = point([iv[nv - 1][1]])
    disj = lambda u, v: sets[u].hi[0] < sets[v].lo[0] if sets[u].kind == "box" or True else True

    def lohi(S):
        return (S.c[0], S.c[0]) if S.kind == "point" else (S.lo[0], S.hi[0])

    def disjoint(u, v):
        a, b = lohi(sets[u]), lohi(sets[v])
        return a[1] < b[0] or b[1] < a[0]

    a, bcoef = float(rng.uniform(0.5, 2)), float(rng.uniform(0.5, 2))
    cyc = trial % 2 == 1
    E = [(u, v) for u in range(nv) for v in range(nv) if u != v and v != 0 and u != nv - 1
         and disjoint(u, v) and (cyc or u < v) and rng.random() < 0.55]
    g = GCS(sets, E, 0, nv - 1, Cost("asym", a=a, bb=bcoef))
    if not all_paths(g, 1):
        continue
    r = relax(g, degree=not cyc)
    rh = relax(g, hull=True, degree=not cyc)
    o = opt(g)
    hd = max(hd, abs(rh - r))
    if cyc:
        bad_cyc += abs(o - r) > 1e-5 * max(1, abs(o))
    else:
        bad_acyc += abs(o - r) > 1e-5 * max(1, abs(o))
print(f"(c) 1D disjoint intervals, asym lengths: #(OPT!=REL) acyclic={bad_acyc}, cyclic(no degree cons)={bad_cyc}; max|REL_H-REL|={hd:.2e}")

# (d) triangles
dd = []
for trial in range(30):
    sets, E = rand_dag_sets(2, int(rng.integers(2, 4)), int(rng.integers(2, 4)), tri=True)
    g = GCS(sets, E, "s", "t", L2 if trial % 2 == 0 else SQ)
    dd.append(relax(g, hull=True) - relax(g))
print(f"(d) triangles: n=30 max(REL_H-REL)={np.max(dd):.2e}")

# (e) crossing family
for R in [5, 20, 80, 320]:
    a = R / np.sqrt(2)
    sets = {"s": point([0, 0, -R]), "u1": point([a, a, 0]), "u2": point([-a, -a, 0]),
            "v": box([-1, -1, 0], [1, 1, 0]), "w1": point([a, -a, 0]), "w2": point([-a, a, 0]), "t": point([0, 0, R])}
    E = [("s", "u1"), ("s", "u2"), ("u1", "v"), ("u2", "v"), ("v", "w1"), ("v", "w2"), ("w1", "t"), ("w2", "t")]
    g = GCS(sets, E, "s", "t", L2)
    r, rh, o = relax(g), relax(g, hull=True), opt(g)
    o_cf = 2 * np.sqrt(2) * R + 2 * np.sqrt(R * R - np.sqrt(2) * R + 1)
    r_ub = 2 * np.sqrt(2) * R + 2 * R - 2 * np.sqrt(2)
    km = max(kappa_l2(sets[u], sets[v]) for u, v in E)
    print(f"(e) R={R:4d} OPT={o:.6f} (closed form {o_cf:.6f}) REL={r:.6f} (<= {r_ub:.6f}) REL_H={rh:.6f} "
          f"OPT-REL={o-r:.4f} R*(OPT/REL-1)={R*(o/r-1):.4f} R^2*(OPT/REL_H-1)={R*R*(o/rh-1):.4f} R^2*(kmax-1)={R*R*(km-1):.4f}")

# (f) Prop. 3 (repair): REL_H <= REL + sum_v W1(mu_in_v, mu_out_v)  (l2 lengths: Lipschitz 1 in the tail)
#     and the a-priori first-order bound OPT <= kappa_max * (REL + max_P sum_{v in P} diam X_v).
import cvxpy as cp


def w1_vertex(g, sol, v):
    I = [e for e in g.inn[v] if sol["y"][e] > 1e-8]
    O = [f for f in g.out[v] if sol["y"][f] > 1e-8]
    if not I or not O:
        return 0.0
    a = {e: sol["zp"][e] / sol["y"][e] for e in I}
    b = {f: sol["z"][f] / sol["y"][f] for f in O}
    P = cp.Variable((len(I), len(O)), nonneg=True)
    C = np.array([[np.linalg.norm(a[e] - b[f]) for f in O] for e in I])
    cons = [cp.sum(P, axis=1) == np.array([sol["y"][e] for e in I]),
            cp.sum(P, axis=0) == np.array([sol["y"][f] for f in O])]
    pr = cp.Problem(cp.Minimize(cp.sum(cp.multiply(C, P))), cons)
    pr.solve(solver=SOLVER)
    return pr.value


bad3, badfo = 0, 0
for trial in range(25):
    sets, E = rand_dag_sets(2, int(rng.integers(2, 4)), int(rng.integers(2, 4)), w=(0.2, 0.9))
    g = GCS(sets, E, "s", "t", L2)
    r, sol = relax(g, return_sol=True)
    rh, o = relax(g, hull=True), opt(g)
    w1 = sum(w1_vertex(g, sol, v) for v in g.V if v not in (g.s, g.t))
    bad3 += rh > r + w1 + 1e-6
    km = max(kappa_l2(sets[u], sets[v]) for u, v in E)
    diam = {e: 2 * sets[e[1]].circ()[1] if e[1] != "t" else 0.0 for e in E}
    fo = km * (r + max_path_weight(g, diam)) if np.isfinite(km) else np.inf
    badfo += o > fo + 1e-6
print(f"(f) Prop 3 repair: n=25 violations={bad3}; first-order bound OPT <= kmax(REL + maxP sum diam): violations={badfo}")
