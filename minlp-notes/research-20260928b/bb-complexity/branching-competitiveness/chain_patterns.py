"""LP check of chain patterns (R = right split, L = left split of the chain around s)
with N_opt = 2: best achievable invalidity margin delta over random split positions.
Negative delta = no instance realizes the pattern with those positions."""
import sys; sys.path.insert(0, '.')
import numpy as np
from chain_lp import solve
for s in (0.9, 0.99, 0.5, 0.1):
    for pat in ("RR","RRR","RRRR","LRL","RLR","RRL","LLR","RLRL","RRLL"):
        best=None
        rng=np.random.default_rng(1)
        for trial in range(1500):
            ys=[]; l,u=0.0,1.0
            for ch in pat:
                f=np.exp(rng.uniform(-10,0))
                if ch=='R':
                    y=s+f*(u-s); u=y
                else:
                    y=s-f*(s-l); l=y
                ys.append(y)
            r=solve(s,ys)
            if r is not None and (best is None or r[0]>best[0]): best=(r[0],ys)
        print(s,pat,"%.3g"%best[0],["%.3g"%(y-s) for y in best[1]],flush=True)
