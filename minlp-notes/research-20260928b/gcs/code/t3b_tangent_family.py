"""T3b: analytic lower-bound family for Corollary B (tangent fork-merge gadget) and a local
search seeded from it.

Gadget (2D): A = B(0, r), s = (-D, 0), u_pm = (cos th, +-sin th) with sin th = r/D,
P_pm = s + 2 sqrt(D^2 - r^2) u_pm, B = B((2 x_P, 0), r), t = (2 x_P + D, 0).
Edges s->A, A->P_pm, P_pm->B, B->t.  Every edge has aperture exactly th, and
  OPT = 4 sqrt(D^2 - r^2),  REL_H <= 2 (D^2 - r^2)/D + 2 sqrt(D^2 - r^2),
so OPT/REL_H - 1 >= tan^2(th/2) and (OPT/REL_H - 1)/(sec th - 1) >= cos th/(1 + cos th) -> 1/2.
For squared lengths the same geometry is evaluated against kappa^sq_max = sec^2(th).
Usage: python3 t3b_tangent_family.py [l2|sq] [iters] [seed]
"""
import sys
import numpy as np
from gcslib import *

NORM = sys.argv[1] if len(sys.argv) > 1 else "l2"
IT = int(sys.argv[2]) if len(sys.argv) > 2 else 200
rng = np.random.default_rng(int(sys.argv[3]) if len(sys.argv) > 3 else 0)
sys.argv = [sys.argv[0], NORM]          # t3_adversarial reads the norm from argv[1]
from t3_adversarial import build, score, KAP  # noqa: E402


def gadget_params(D, r):
    th = np.arcsin(r / D)
    s = np.array([-D, 0.0])
    ell = np.sqrt(D * D - r * r)
    Pp = s + 2 * ell * np.array([np.cos(th), np.sin(th)])
    Pm = s + 2 * ell * np.array([np.cos(th), -np.sin(th)])
    xP = Pp[0]
    # order in template: s(p) A(b) P(p) M(p) B(b) t(p); build() uses radius |prm| + 1e-3,
    # so pass r - 1e-3 to get radius exactly r (the first version passed r, inflating radii by 1e-3)
    return np.r_[s, 0.0, 0.0, r - 1e-3, Pp, Pm, 2 * xP, 0.0, r - 1e-3, 2 * xP + D, 0.0], th


for th_deg in [2.866, 5.739, 10.0, 11.537, 20.0, 23.578, 30.0]:
    D = 10.0
    r = D * np.sin(np.radians(th_deg))
    p, th = gadget_params(D, r)
    g = build("forkmerge", p, 2)
    km = max(KAP(g.sets[u], g.sets[v]) for u, v in g.edges)
    kex = 1 / np.cos(th) if NORM == "l2" else 1 / np.cos(th) ** 2   # exact kappa_max of the family
    rh, o = relax(g, hull=True), opt(g)
    ell = np.sqrt(D * D - r * r)
    sc = (o / rh - 1) / (kex - 1)
    print(f"[{NORM}] theta={th_deg:6.3f}deg kappa_max(numeric)={km:.6f} kappa_max(exact)={kex:.6f} "
          f"OPT={o:.6f} (4*ell={4*ell:.6f}) REL_H={rh:.6f} (explicit point {2*(D*D-r*r)/D+2*ell:.6f}) "
          f"score(exact kappa)={sc:.6f} score-1/2={sc-0.5:.2e} (score-1/2)/theta^4={(sc-0.5)/th**4:.3f} "
          f"(cos/(1+cos)={np.cos(th)/(1+np.cos(th)):.4f})", flush=True)

# local search in the full forkmerge parameter space seeded at the gadget (D=10, r=2)
p0, _ = gadget_params(10, 2.0)
best, _ = score("forkmerge", p0, 2)
bp = p0
for it in range(IT):
    p = bp + rng.standard_normal(len(bp)) * rng.choice([0.01, 0.03, 0.1])
    sc, info = score("forkmerge", p, 2)
    if sc > best:
        best, bp = sc, p
print(f"[{NORM}] local search from gadget (D=10, r=2, theta=11.5deg; scored with numerical kappa_max): best score {best:.4f}")
