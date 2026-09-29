"""Exp 13: (a) linear edge costs on random DAGs of boxes: predicted REL_hull == OPT,
while basic REL may be < OPT. (b) triangle (simplex) sets with Euclidean lengths:
predicted REL == REL_hull (basic relaxation already hull-feasible at simplex vertices)."""
import numpy as np
from gcs import *
rng = np.random.default_rng(2)

def rand_layered(d, L, k, kind):
    sets = {'s': ('point', np.zeros(d))}
    layers = []
    for i in range(1, L+1):
        lay = []
        for j in range(k):
            c = np.r_[2.0*i, rng.uniform(-2, 2, d-1)]
            if kind == 'box':
                w = rng.uniform(0.2, 1.5, d); sets[f"{i}_{j}"] = ('box', c - w, c + w)
            else:  # random triangle in 2D as polytope A x <= b
                P = c + rng.uniform(-1.2, 1.2, (3, 2))
                cen = P.mean(0); A = []; b = []
                for q in range(3):
                    p1, p2 = P[q], P[(q+1) % 3]
                    nrm = np.array([p2[1]-p1[1], -(p2[0]-p1[0])])
                    if nrm @ (cen - p1) > 0: nrm = -nrm
                    A.append(nrm); b.append(nrm @ p1)
                sets[f"{i}_{j}"] = ('poly', np.array(A), np.array(b))
            lay.append(f"{i}_{j}")
        layers.append(lay)
    sets['t'] = ('point', np.r_[2.0*(L+1), np.zeros(d-1)])
    E = [('s', v) for v in layers[0]] + [(v, 't') for v in layers[-1]]
    for a, b in zip(layers, layers[1:]): E += [(u, v) for u in a for v in b]
    for a, b in zip(layers, layers[2:]): E += [(u, v) for u in a for v in b if rng.random() < 0.3]
    return Inst(sets, E, 's', 't', d)

gl, gh = [], []
for trial in range(30):
    I = rand_layered(2, rng.integers(2, 4), rng.integers(2, 4), 'box')
    I.norm = 'lin'
    I.lin = {e: (rng.standard_normal(2), rng.standard_normal(2)) for e in I.edges}
    r = relax(I); rh = relax(I, hull=True); o = exact(I)
    gl.append(o - r); gh.append(o - rh)
gl, gh = np.array(gl), np.array(gh)
print(f"linear costs: max(OPT-REL)={gl.max():.4f} (#>1e-5: {(gl>1e-5).sum()}), max|OPT-REL_hull|={np.abs(gh).max():.2e}")
dd = []
for trial in range(30):
    I = rand_layered(2, rng.integers(2, 4), rng.integers(2, 4), 'tri')
    r = relax(I); rh = relax(I, hull=True)
    dd.append(rh - r)
print(f"triangles, Euclidean: max(REL_hull-REL)={np.max(dd):.2e}")
