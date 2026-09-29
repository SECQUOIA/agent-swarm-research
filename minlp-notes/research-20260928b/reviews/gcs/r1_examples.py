"""Recompute the note's explicit examples with the reviewer's own code.

Prop A', Prop B', Example C', Prop 4 (crossing), Prop 5.2 (C2, C3),
Prop 6 (translation constraints), Prop 8 (1D overlap).
"""
import numpy as np
from rgcs import *

np.set_printoptions(precision=6, suppress=True)


def hdr(s):
    print("\n==== " + s)


# ---------------------------------------------------------------- Prop A'
hdr("Prop A' (nonnegative affine lengths, square vertex)")
O = Pt([0, 0])
sets = dict(s=O, u1=O, u2=O, v=Box([-1, -1], [1, 1]), w1=O, w2=O, t=O)
E = [("s", "u1"), ("s", "u2"), ("u1", "v"), ("u2", "v"), ("v", "w1"), ("v", "w2"), ("w1", "t"), ("w2", "t")]
z2 = np.zeros(2)
lens = {e: ZERO for e in E}
lens[("u1", "v")] = Len("aff", c=z2, d=np.array([-1.0, -1.0]), b0=2.0)
lens[("u2", "v")] = Len("aff", c=z2, d=np.array([1.0, 1.0]), b0=2.0)
lens[("v", "w1")] = Len("aff", c=np.array([-1.0, 1.0]), d=z2, b0=2.0)
lens[("v", "w2")] = Len("aff", c=np.array([1.0, -1.0]), d=z2, b0=2.0)
g = G(sets, E, "s", "t", lens)
print("REL =", round(relax(g), 6), " REL_H =", round(relax(g, hull=True), 6), " OPT =", round(opt(g), 6))

# ---------------------------------------------------------------- Prop B'
hdr("Prop B' (tangent family, balls, Euclidean)")
for th_deg in [3, 10, 20, 30]:
    th = np.radians(th_deg)
    D = 10.0
    r = D * np.sin(th)
    sA = np.array([-D, 0.0])
    up = np.array([np.cos(th), np.sin(th)])
    um = np.array([np.cos(th), -np.sin(th)])
    Pp = sA + 2 * np.sqrt(D * D - r * r) * up
    Pm = sA + 2 * np.sqrt(D * D - r * r) * um
    X0 = Pp[0]
    cB = np.array([2 * X0, 0.0])
    tpt = np.array([2 * X0 + D, 0.0])
    sets = dict(s=Pt(sA), A=Ball([0, 0], r), Pp=Pt(Pp), Pm=Pt(Pm), B=Ball(cB, r), t=Pt(tpt))
    E = [("s", "A"), ("A", "Pp"), ("A", "Pm"), ("Pp", "B"), ("Pm", "B"), ("B", "t")]
    g = G(sets, E, "s", "t", L2)
    o = opt(g)
    rh = relax(g, hull=True)
    rl = relax(g)
    expl = 2 * (D * D - r * r) / D + 2 * np.sqrt(D * D - r * r)
    sec = 1 / np.cos(th)
    print(f"theta={th_deg:2d}  |Pp|={np.linalg.norm(Pp):.6f} (D={D})  OPT={o:.6f} (4sqrt={4*np.sqrt(D*D-r*r):.6f})"
          f"  REL={rl:.6f} REL_H={rh:.6f} explicit={expl:.6f}  score=(OPT/REL_H-1)/(sec-1)={(o/rh-1)/(sec-1):.5f}"
          f"  cos/(1+cos)={np.cos(th)/(1+np.cos(th)):.5f}  OPT<=sec*REL_H: {o <= sec*rh + 1e-6}")

# ---------------------------------------------------------------- Example C'
hdr("Example C' (1D disjoint intervals)")
sets = dict(s=Pt([0]), A=Box([1], [3]), P=Pt([3.5]), Q=Pt([4.5]), t=Pt([6]))
E = [("s", "A"), ("A", "P"), ("A", "Q"), ("P", "t"), ("Q", "t")]
for name, L in [("sq", SQ), ("l2", L2)]:
    g = G(sets, E, "s", "t", L)
    print(name, "REL =", round(relax(g), 6), "REL_H =", round(relax(g, hull=True), 6), "OPT =", round(opt(g), 6),
          "route values:", [round(restriction(g, p), 6) for p in g.paths()])

# ---------------------------------------------------------------- Prop 4
hdr("Prop 4 (crossing family in R^3, Euclidean)")
sq = Poly(np.array([[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]], float),
          np.array([1, 1, 1, 1, 0, 0], float),
          np.array([[1, 1, 0], [1, -1, 0], [-1, 1, 0], [-1, -1, 0]], float))
for R in [5, 10, 20, 40, 80]:
    a = R / np.sqrt(2)
    sets = dict(s=Pt([0, 0, -R]), u1=Pt([a, a, 0]), u2=Pt([-a, -a, 0]), v=sq,
                w1=Pt([a, -a, 0]), w2=Pt([-a, a, 0]), t=Pt([0, 0, R]))
    E = [("s", "u1"), ("s", "u2"), ("u1", "v"), ("u2", "v"), ("v", "w1"), ("v", "w2"), ("w1", "t"), ("w2", "t")]
    g = G(sets, E, "s", "t", L2)
    o, rl, rh = opt(g), relax(g), relax(g, hull=True)
    of = 2 * np.sqrt(2) * R + 2 * np.sqrt(R * R - np.sqrt(2) * R + 1)
    relf = 2 * np.sqrt(2) * R + 2 * R - 2 * np.sqrt(2)
    print(f"R={R:3d} OPT={o:.6f} (formula {of:.6f})  REL={rl:.6f} (upper formula {relf:.6f})  REL_H={rh:.6f}"
          f"  OPT-REL={o-rl:.4f}  R(OPT/REL-1)={R*(o/rl-1):.4f}  R^2(OPT/REL_H-1)={R*R*(o/rh-1):.4f}"
          f"  bound 1/(R^2-2)*R^2={R*R/(R*R-2):.4f}")

# ---------------------------------------------------------------- Prop 5.2
hdr("Prop 5.2 (cyclic, squared lengths) C2 and C3")
sets = dict(s=Pt([-1]), n1=Box([-0.5], [0.5]), n2=Pt([0]), n3=Pt([0]), t=Pt([1]))
E = [("s", "n1"), ("n1", "n2"), ("n2", "n1"), ("n1", "t"), ("s", "n3"), ("n3", "t")]
g = G(sets, E, "s", "t", SQ)
print("C2: OPT =", round(opt(g), 6),
      " REL(deg) =", round(relax(g), 6), " REL_H(deg) =", round(relax(g, hull=True), 6),
      " REL_H(no deg) =", round(relax(g, hull=True, deg=False), 6),
      " REL_H(deg)+2cyc =", round(relax(g, hull=True, two_cycle=True), 6))
val, sol = relax(g, hull=True, return_vars=True)
print("   y:", {k: round(v, 4) for k, v in sol["y"].items()})
print("   lam:", {k: round(v, 4) for k, v in sol["lam"].items() if v > 1e-6})
# shortest walk by brute force on walk patterns s 1 (2 1)^k t
best = np.inf
for k in range(0, 5):
    walk = [("s", "n1")] + [("n1", "n2"), ("n2", "n1")] * k + [("n1", "t")]
    import cvxpy as cp
    xs = [cp.Variable(1) for _ in range(len(walk) + 1)]
    verts = ["s"] + [e[1] for e in walk]
    cons = []
    for v, x in zip(verts, xs):
        cons += sets[v].persp(x, 1.0)
    obj = sum(cp.sum_squares(xs[i + 1] - xs[i]) for i in range(len(walk)))
    val = solve(cp.Problem(cp.Minimize(obj), cons))
    best = min(best, val)
    print(f"   walk with {k} loops: {val:.6f}")

sets3 = dict(s=Pt([-1]), n1=Box([-0.5], [0.5]), n2=Pt([0]), n4=Pt([0]), n3=Pt([0]), t=Pt([1]))
E3 = [("s", "n1"), ("n1", "n2"), ("n2", "n4"), ("n4", "n1"), ("n1", "t"), ("s", "n3"), ("n3", "t")]
g3 = G(sets3, E3, "s", "t", SQ)
print("C3: OPT =", round(opt(g3), 6), " REL_H(deg) =", round(relax(g3, hull=True), 6),
      " +2cyc =", round(relax(g3, hull=True, two_cycle=True), 6),
      " +GSEC{1,2,4} =", round(relax(g3, hull=True, gsec=[("n1", "n2", "n4")]), 6))

# ---------------------------------------------------------------- Prop 6
hdr("Prop 6 (translation constraints x_v = x_u + 10)")
sets = dict(s=Pt([0]), A=Box([9], [11]), P=Pt([21]), M=Pt([19]), B=Box([29], [31]), t=Pt([40]))
E = [("s", "A"), ("A", "P"), ("A", "M"), ("P", "B"), ("M", "B"), ("B", "t")]
ec = {e: (np.array([[-1.0]]), np.array([[1.0]]), np.array([10.0])) for e in E}
g = G(sets, E, "s", "t", ZERO, ec)
print("MICP OPT =", opt(g), " REL =", relax(g), " REL_H =", relax(g, hull=True))
E2 = E + [("s", "t")]
lens = {e: ZERO for e in E}
lens[("s", "t")] = Len("aff", c=np.zeros(1), d=np.zeros(1), b0=1.0)
g = G(sets, E2, "s", "t", lens, ec)
print("with bypass: OPT =", opt(g), " REL =", round(relax(g), 6), " REL_H =", round(relax(g, hull=True), 6))

# ---------------------------------------------------------------- Prop 8
hdr("Prop 8 (1D overlap) and additive bounds")
for dl in [0.0, 0.3, 0.7, 1.0]:
    sets = dict(s=Pt([0]), A=Box([-1], [1]), P=Pt([1]), M=Pt([-1]), B=Box([-1], [1]), t=Pt([dl]))
    E = [("s", "A"), ("A", "P"), ("A", "M"), ("P", "B"), ("M", "B"), ("B", "t")]
    g = G(sets, E, "s", "t", L2)
    D = {e: delta_max(L2, sets[e[0]].V, sets[e[1]].V) for e in E}
    mp = max(sum(D[e] for e in p) for p in g.paths())
    print(f"delta={dl}: REL={relax(g):.6f} REL_H={relax(g, hull=True):.6f} OPT={opt(g):.6f}"
          f"  max_P sum Delta={mp:.6f} (2-d^2={2-dl*dl:.6f})")
