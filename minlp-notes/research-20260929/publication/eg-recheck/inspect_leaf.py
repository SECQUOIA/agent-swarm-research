"""Details of one certified leaf: author's bound, and the reviewer certifier's per-row lower bounds.
    python3 inspect_leaf.py <part> <leaf index>"""
import glob
import os
import sys
from fractions import Fraction as Fr

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from margin_cert import MarginCertifier, F, lin_min_exact  # noqa: E402

k, j = int(sys.argv[1]), int(sys.argv[2])
Z = [np.load(f) for f in sorted(glob.glob(os.path.join(HERE, "res", f"p{k}_c*.npz")))]
sel = np.concatenate([z["sel"] for z in Z]); pos = int(np.where(sel == j)[0][0]) if False else None
cat = lambda key: np.concatenate([z[key] for z in Z])
lo, hi, mg, how, plb = cat("lo")[j], cat("hi")[j], cat("mg")[j], cat("how")[j], cat("plb")[j]
TH = "5.642100574331458"
print(f"part {k} leaf {j}: lo {lo.tolist()} hi {hi.tolist()}")
print(f"  recorded margin {mg:.6e}, certificate {how}; author's bound minus theta*: {plb - float(TH):.6e}")
C = MarginCertifier("eg_disc2_s", TH)
M = C.M
c, r, beta, aL, aU = M.taylor(lo[None], hi[None])
nlo, nhi = M.natural(lo[None], hi[None])
dl = [F(a) - F(b) for a, b in zip(lo, c[0])]; dh = [F(a) - F(b) for a, b in zip(hi, c[0])]
rows = []
for kk in range(24):
    tay = F(aL[0, kk]) + lin_min_exact([F(v) for v in beta[0, kk]], dl, dh) if np.isfinite(aL[0, kk]) else None
    nat = F(nlo[0, kk])
    rows.append((float(M.qc[kk] + max(v for v in (tay, nat) if v is not None) - Fr(TH)), kk,
                 float(M.qc[kk] + tay - Fr(TH)) if tay is not None else None, float(M.qc[kk] + nat - Fr(TH))))
rows.sort(reverse=True)
for m_, kk, t_, n_ in rows[:4]:
    print(f"  row e{kk + 1}: c_k + lower bound - theta* = {m_:.6e} (Taylor {t_}, natural {n_})")
ok = C.certify_batch(lo[None], hi[None])
print(f"  re-certified now: {ok.tolist()}, margin {C.last_mg.tolist()}, how {C.last_how.tolist()}, stats {C.stats}")
