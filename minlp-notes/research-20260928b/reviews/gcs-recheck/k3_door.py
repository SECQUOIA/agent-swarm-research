"""Recheck of Proposition 10 on the ring family: door apertures and the door relaxation.

Door graph: start s=(-1.5,0), goal t=(1.5,0), doors LT, LB, RT, RB (boxes = region intersections);
an edge joins two vertices lying in a common region (both directions between doors), Euclidean lengths.
Checks: numerical sec(theta_door) (SOCP over vertex differences) vs max(sqrt5/2, sqrt(1+1/(4H^2)));
REL_H(door) with and without degree constraints; exact OPT by simple-path enumeration;
OPT <= sec(theta_door) * REL_H; closed form OPT = 2 + 2 sqrt(H^2 + 1/4)."""
import numpy as np
from rc import PSet, pt, box, G, relax, opt_exact, sec_aperture


def ring_door(H):
    sets = {"s": pt(-1.5, 0.0), "t": pt(1.5, 0.0),
            "LT": box([-2, H], [-1, H + 1]), "LB": box([-2, -H - 1], [-1, -H]),
            "RT": box([1, H], [2, H + 1]), "RB": box([1, -H - 1], [2, -H])}
    E = [("s", "LT"), ("s", "LB"), ("LT", "LB"), ("LB", "LT"),        # region L
         ("LT", "RT"), ("RT", "LT"),                                      # region T
         ("LB", "RB"), ("RB", "LB"),                                      # region B
         ("RT", "RB"), ("RB", "RT"), ("RT", "t"), ("RB", "t")]            # region R
    return G(sets, E, "s", "t", "l2")


for H in [0.125, 0.25, 0.5, 0.75, 1, 2, 5, 20]:
    g = ring_door(H)
    secs = {}
    for (u, v) in g.E:
        W = np.array([b - a for a in g.sets[u].V for b in g.sets[v].V])
        secs[(u, v)] = sec_aperture(W)
    sd = max(secs.values())
    formula = max(np.sqrt(5) / 2, np.sqrt(1 + 1 / (4 * H * H)))
    arg = max(secs, key=secs.get)
    rh_nd, _, st1 = relax(g, hull=True, degree=False)
    rh_d, _, st2 = relax(g, hull=True, degree=True)
    r_nd, _, st3 = relax(g, hull=False, degree=False)
    opt, path, _ = opt_exact(g)
    cf = 2 + 2 * np.sqrt(H * H + 0.25)
    print(f"H={H:6.3f} sec(theta_door)={sd:.6f} formula={formula:.6f} (argmax edge {arg}) | OPT={opt:.6f} closed={cf:.6f} "
          f"REL(no deg)={r_nd:.6f} REL_H(no deg)={rh_nd:.6f} REL_H(deg)={rh_d:.6f} | OPT <= sec*REL_H: {opt <= sd * rh_nd + 1e-7} "
          f"| OPT/REL_H-1={opt/rh_nd-1:.1e} [{st1},{st2},{st3}]")
