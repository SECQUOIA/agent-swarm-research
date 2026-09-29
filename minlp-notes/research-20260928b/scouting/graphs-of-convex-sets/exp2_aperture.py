"""Exp 2: random layered DAGs of disjoint balls in R^d with Euclidean lengths.
Test conjectured bound OPT <= sec(theta_max) * REL_hull, theta_e = aperture of
X_v - X_u = arcsin((r_u+r_v)/|c_v-c_u|). Also report OPT/REL (basic)."""
import numpy as np, sys
from gcs import *

def make(rng, L, k, d, D, spread, rmax, skip):
    sets = {'s': ('point', np.r_[0., np.zeros(d-1)])}
    layers = []
    for i in range(1, L+1):
        lay = []
        for j in range(k):
            c = np.r_[i*D, rng.uniform(-spread, spread, d-1)]
            r = rng.uniform(0.2, 1.0)*rmax
            name = f"{i}_{j}"
            sets[name] = ('ball', c, r)
            lay.append(name)
        layers.append(lay)
    sets['t'] = ('point', np.r_[(L+1)*D, rng.uniform(-spread, spread, d-1)])
    E = [('s', v) for v in layers[0]] + [(v, 't') for v in layers[-1]]
    for a, b in zip(layers, layers[1:]):
        E += [(u, v) for u in a for v in b]
    for a, b in zip(layers, layers[2:]):
        E += [(u, v) for u in a for v in b if rng.random() < skip]
    return Inst(sets, E, 's', 't', d)

def aperture(inst):
    th = 0.0
    for u, v in inst.edges:
        Su, Sv = inst.sets[u], inst.sets[v]
        cu = np.asarray(Su[1], float); cv = np.asarray(Sv[1], float)
        ru = Su[2] if Su[0] == 'ball' else 0.0
        rv = Sv[2] if Sv[0] == 'ball' else 0.0
        dist = np.linalg.norm(cv - cu)
        if ru + rv >= dist:
            return np.pi/2
        th = max(th, np.arcsin((ru + rv)/dist))
    return th

if __name__ == "__main__":
    rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
    worst = 0
    rows = []
    for trial in range(60):
        d = rng.choice([2, 3])
        rmax = rng.choice([0.5, 1.0, 1.5])
        I = make(rng, L=rng.integers(2, 5), k=rng.integers(2, 4), d=d, D=3.0,
                 spread=rng.choice([1.0, 2.0, 4.0]), rmax=rmax, skip=0.3)
        th = aperture(I)
        if th >= np.pi/2 - 1e-9:
            continue
        r = relax(I); rh = relax(I, hull=True); o = exact(I)
        sec = 1/np.cos(th)
        rows.append((o/r, o/rh, sec))
        flag = 'VIOLATION' if o > sec*rh*(1+1e-6) + 1e-6 else ''
        print(f"d={d} |E|={len(I.edges):3} th={np.degrees(th):5.1f}deg sec={sec:.4f} OPT/REL={o/r:.5f} OPT/REL_hull={o/rh:.5f} {flag}")
    rows = np.array(rows)
    print("max OPT/REL", rows[:,0].max(), "max OPT/REL_hull", rows[:,1].max(),
          "max (OPT/REL_hull-1)/(sec-1)", ((rows[:,1]-1)/(rows[:,2]-1)).max())
    print("fraction exact (1e-5): basic", np.mean(rows[:,0] < 1+1e-5), "hull", np.mean(rows[:,1] < 1+1e-5))
