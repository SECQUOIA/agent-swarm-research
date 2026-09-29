"""Exp 3: 'diagonal crossing' vertex. v = square [-1,1]^2, in-neighbours u1,u2 far
along diagonals (1,1),(-1,-1); out-neighbours w1,w2 far along (1,-1),(-1,1).
Basic relaxation can route arrivals to corners (1,1),(-1,-1) and departures from
(1,-1),(-1,1) (equal means, not hull-feasible). Compare REL, REL_hull, OPT vs R."""
import numpy as np
from gcs import *
for R in [3, 5, 10, 20, 40, 80]:
    a = R/np.sqrt(2)
    sets = {'s': ('point', [0., 0., -R]), 'u1': ('point', [a, a, 0.]), 'u2': ('point', [-a, -a, 0.]),
            'v': ('box', [-1., -1., 0.], [1., 1., 0.]),
            'w1': ('point', [a, -a, 0.]), 'w2': ('point', [-a, a, 0.]), 't': ('point', [0., 0., R])}
    E = [('s','u1'), ('s','u2'), ('u1','v'), ('u2','v'), ('v','w1'), ('v','w2'), ('w1','t'), ('w2','t')]
    I = Inst(sets, E, 's', 't', 3)
    r = relax(I); rh = relax(I, hull=True); o = exact(I)
    th = np.arcsin(np.sqrt(2)/R)  # aperture of u_i->v edges (square radius sqrt2)
    print(f"R={R:3}: REL={r:.5f} REL_hull={rh:.5f} OPT={o:.5f}  OPT/REL-1={o/r-1:.2e}  OPT/REL_hull-1={o/rh-1:.2e}  sec(th)-1={1/np.cos(th)-1:.2e}")
