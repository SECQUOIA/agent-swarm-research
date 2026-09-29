"""Recheck of Proposition B' (tangent family) and its numerics.

Scale D = 1, r = sin(theta).  Then P+ = (cos 2theta, sin 2theta), |P+| = 1, OPT = 4 cos(theta).
Exact value (note §3.2): REL_H = 2 min_{a in B(0,r)} (a_1 + 1 + |P+ - a|).  For theta < 60 deg the
minimum lies on the circle (an interior stationary point needs a_2 = P_2 = sin 2theta <= sin theta),
so it is a 1D minimisation over the boundary angle, done here in high precision (mpmath).
Also: an independent full REL_H / OPT solve of the graph with cvxpy at several theta (Euclidean and
squared lengths, both squared-length formulations), and the limit of (ratio - 1/2)/theta^4."""
import numpy as np
import mpmath as mp
from rc import PSet, pt, G, relax, opt_exact

mp.mp.dps = 60


def relh_exact(th):
    th = mp.mpf(th)
    r = mp.sin(th)
    P = (mp.cos(2 * th), mp.sin(2 * th))
    g = lambda phi: r * mp.cos(phi) + mp.sqrt((P[0] - r * mp.cos(phi)) ** 2 + (P[1] - r * mp.sin(phi)) ** 2)
    dg = lambda phi: mp.diff(g, phi)
    # minimiser is near the tangent point T+ at phi = pi/2 + theta
    phi = mp.findroot(dg, mp.pi / 2 + th)
    val = g(phi)
    # sanity: compare with a coarse scan
    grid = [g(mp.pi / 2 + th + k * mp.mpf("0.01")) for k in range(-100, 101)]
    assert val <= min(grid) + mp.mpf("1e-30")
    return 2 * (1 + val), phi


def score(th):
    rel, _ = relh_exact(th)
    opt = 4 * mp.cos(th)
    return (opt / rel - 1) / (1 / mp.cos(th) - 1), rel


print("exact formula (mpmath):")
for deg in [2.866, 5.739, 6, 10, 11.537, 20, 23.578, 23.6, 30, 45]:
    th = mp.radians(deg)
    s, rel = score(th)
    expl = 2 * mp.cos(th) ** 2 + 2 * mp.cos(th)
    print(f"  theta={deg:7.3f}: ratio={mp.nstr(s, 10)}  ratio-1/2={mp.nstr(s - 0.5, 4)}  (ratio-1/2)/theta^4={mp.nstr((s - 0.5) / th ** 4, 6)}"
          f"  REL_H/(D)={mp.nstr(rel, 12)} explicit point={mp.nstr(expl, 12)}  cos/(1+cos)={mp.nstr(mp.cos(th)/(1+mp.cos(th)), 6)}")

print("limit of (ratio - 1/2)/theta^4 as theta -> 0:")
for th in [mp.mpf("0.2"), mp.mpf("0.1"), mp.mpf("0.05"), mp.mpf("0.02"), mp.mpf("0.01"), mp.mpf("0.005")]:
    s, _ = score(th)
    print(f"  theta={mp.nstr(th, 4)} rad: {mp.nstr((s - 0.5) / th ** 4, 10)}")


# independent cvxpy solve of the whole graph
def family(th, Dd=10.0, kind="l2"):
    r = Dd * np.sin(th)
    s = np.array([-Dd, 0.0])
    ell = np.sqrt(Dd * Dd - r * r)
    up, um = np.array([np.cos(th), np.sin(th)]), np.array([np.cos(th), -np.sin(th)])
    Pp, Pm = s + 2 * ell * up, s + 2 * ell * um
    x0 = Pp[0]                               # vertical mirror line x = x0
    refl = lambda p: np.array([2 * x0 - p[0], p[1]])
    sets = {"s": pt(*s), "A": PSet(center=[0.0, 0.0], radius=r), "Pp": pt(*Pp), "Pm": pt(*Pm),
            "B": PSet(center=refl(np.zeros(2)), radius=r), "t": pt(*refl(s))}
    E = [("s", "A"), ("A", "Pp"), ("A", "Pm"), ("Pp", "B"), ("Pm", "B"), ("B", "t")]
    # apertures of every edge (ball-ball/point closed form): sin theta_e = (r_u + r_v)/|c_v - c_u|
    cen = {"s": s, "A": np.zeros(2), "Pp": Pp, "Pm": Pm, "B": refl(np.zeros(2)), "t": refl(s)}
    rad = {"s": 0, "A": r, "Pp": 0, "Pm": 0, "B": r, "t": 0}
    ap = [np.degrees(np.arcsin((rad[u] + rad[v]) / np.linalg.norm(cen[v] - cen[u]))) for u, v in E]
    return G(sets, E, "s", "t", kind), ap, 4 * ell


print("independent cvxpy solve (D=10):")
for deg in [10, 20, 23.578, 30]:
    th = np.radians(deg)
    g, ap, opt4 = family(th)
    rh, _, st = relax(g, hull=True, degree=False)
    rhd, _, _ = relax(g, hull=True, degree=True)
    opt, _, _ = opt_exact(g)
    ex_rel = float(relh_exact(th)[0]) * 10
    print(f"  l2 theta={deg:7.3f}: edge apertures={np.round(ap, 6)} OPT={opt:.6f} (4 sqrt(D^2-r^2)={opt4:.6f}) REL_H={rh:.6f} "
          f"REL_H(deg)={rhd:.6f} exact formula={ex_rel:.6f} ratio(cvx)={(opt/rh-1)/(1/np.cos(th)-1):.6f} [{st}]")

print("squared lengths, both formulations (t3b_sq reports REL_H=258.875037 at 30 deg, 398.500791 at 2.866 deg, 376.215122 at 11.537 deg):")
for deg in [2.866, 11.537, 30]:
    th = np.radians(deg)
    g, _, _ = family(th, kind="sq")
    out = []
    for mode in ["cone", "qol"]:
        for solver in ["CLARABEL", "SCS"]:
            v, _, st = relax(g, hull=True, degree=False, sq_mode=mode, solver=solver)
            out.append(f"{mode}/{solver}={v:.6f}({st})")
    opt, _, _ = opt_exact(g)
    print(f"  sq theta={deg:7.3f}: OPT={opt:.6f}  " + "  ".join(out))
