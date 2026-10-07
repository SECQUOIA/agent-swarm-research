"""Split a saved B&B checkpoint (open boxes) into K files for parallel resumption.
Every open box goes to exactly one file (round robin over the boxes sorted by key), and each
file keeps the checkpoint's theta_min, forced_min, UB and incumbent, so the minimum of the
resumed runs' bounds is a bound for the union.

    python3 split_ckpt.py <in.npz> <K> <out_prefix>
"""
import sys

import numpy as np

z = np.load(sys.argv[1])
K = int(sys.argv[2])
o = np.argsort(z["key"])
for k in range(K):
    idx = o[k::K]
    np.savez(f"{sys.argv[3]}{k}.npz", lo=z["lo"][idx], hi=z["hi"][idx], key=z["key"][idx], UB=z["UB"],
             xbest=z["xbest"], theta_min=z["theta_min"], forced_min=z["forced_min"])
    print(f"{sys.argv[3]}{k}.npz: {len(idx)} boxes, min key {z['key'][idx].min():.6f}")
print(f"total {len(o)} boxes; theta_min {float(z['theta_min'])!r}")
