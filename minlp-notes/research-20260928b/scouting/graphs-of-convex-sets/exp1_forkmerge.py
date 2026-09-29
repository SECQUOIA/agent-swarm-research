"""Exp 1: 1D fork-merge instance, all edges |x_v - x_u|, singleton s,t.
s={0} -> A=[-1,1] -> {P={1} | M={-1}} -> B=[-1,1] -> t={delta}.
Expect REL = delta, OPT = 2 - delta (0 <= delta <= 1): unbounded OPT/REL."""
from gcs import *
for delta in [0.0, 0.01, 0.1, 0.5, 0.9, 1.0]:
    sets = {'s': ('point', [0.]), 'A': ('box', [-1.], [1.]), 'P': ('point', [1.]),
            'M': ('point', [-1.]), 'B': ('box', [-1.], [1.]), 't': ('point', [delta])}
    E = [('s','A'), ('A','P'), ('A','M'), ('P','B'), ('M','B'), ('B','t')]
    I = Inst(sets, E, 's', 't', 1)
    r = relax(I); rh = relax(I, hull=True); o = exact(I)
    print(f"delta={delta:4}: REL={r:.4f} REL_hull={rh:.4f} OPT={o:.4f}")
