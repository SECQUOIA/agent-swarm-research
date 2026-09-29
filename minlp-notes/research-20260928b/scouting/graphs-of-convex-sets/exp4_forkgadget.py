"""Exp 4: symmetric fork-merge gadget in 2D with disjoint balls; measure how close
OPT/REL_hull gets to sec(theta_max). Local random search over geometry."""
import numpy as np
from gcs import *

def gadget(D1, r, h, D2):
    sets = {'s': ('point', [0., 0.]), 'A': ('ball', [D1, 0.], r),
            'P': ('point', [D1 + D2, h]), 'M': ('point', [D1 + D2, -h]),
            'B': ('ball', [D1 + 2*D2, 0.], r), 't': ('point', [2*D1 + 2*D2, 0.])}
    E = [('s','A'), ('A','P'), ('A','M'), ('P','B'), ('M','B'), ('B','t')]
    return Inst(sets, E, 's', 't', 2)

def aperture(I):
    th = 0
    for u, v in I.edges:
        Su, Sv = I.sets[u], I.sets[v]
        cu, cv = np.asarray(Su[1], float), np.asarray(Sv[1], float)
        rr = (Su[2] if Su[0]=='ball' else 0) + (Sv[2] if Sv[0]=='ball' else 0)
        dd = np.linalg.norm(cv - cu)
        if rr >= dd: return np.pi/2
        th = max(th, np.arcsin(rr/dd))
    return th

def score(p):
    D1, r, h, D2 = p
    if min(p) <= 0: return -1, None
    I = gadget(*p)
    th = aperture(I)
    if th >= np.pi/2 - 1e-6: return -1, None
    rh = relax(I, hull=True); o = exact(I)
    return (o/rh - 1)/(1/np.cos(th) - 1), (o/rh, 1/np.cos(th), np.degrees(th))

if __name__ == "__main__":
    rng = np.random.default_rng(1)
    best, bp, binfo = -1, None, None
    for it in range(150):
        p = np.array([rng.uniform(0.5, 5), rng.uniform(0.05, 2), rng.uniform(0.05, 3), rng.uniform(0.5, 5)]) if bp is None or rng.random() < 0.3 else bp*np.exp(0.15*rng.standard_normal(4))
        sc, info = score(p)
        if sc > best:
            best, bp, binfo = sc, p, info
            print(f"it={it} ratio_of_excess={sc:.4f} OPT/REL_hull={info[0]:.5f} sec={info[1]:.5f} theta={info[2]:.1f} params={np.round(p,3)}")
