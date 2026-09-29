"""Exp 11: does the vertex-hull (edge-pair coupling, no immediate backtracking) close
MP-GCS gaps on simply connected corridors and on the ring-with-hole?"""
import numpy as np, sys
from mp import MP, relax_hull
from exp9_corridor import corridor
from exp8_mp import simply_connected, ring
rng = np.random.default_rng(0)
out = []
for trial in range(40):
    boxes, pts = corridor(rng, legs=rng.integers(2, 4), W=rng.uniform(0.8, 2.0))
    B = [(np.array(a), np.array(b)) for a, b in boxes]
    if not simply_connected(B): continue
    m = MP(boxes, pts[0], pts[-1], two_cycle=True)
    if not m.paths() or len(m.paths()) > 3000: continue
    r, _ = m.relax(); rh, _ = relax_hull(m); o = m.exact()
    out.append(((o - r)/o, (o - rh)/o))
    print(f"regions={len(boxes):2} gap_basic={(o-r)/o:.3%} gap_hull={(o-rh)/o:.3%}")
out = np.array(out)
print(f"n={len(out)} mean gap basic={out[:,0].mean():.3%} hull={out[:,1].mean():.3%}; max basic={out[:,0].max():.3%} hull={out[:,1].max():.3%}; #hull exact(1e-4)={(out[:,1]<1e-4).sum()}")
for eps in [0.0, 0.2]:
    m = ring(eps); r, _ = m.relax(); rh, _ = relax_hull(m); o = m.exact()
    print(f"ring eps={eps}: basic gap={(o-r)/o:.3%} hull gap={(o-rh)/o:.3%}")
