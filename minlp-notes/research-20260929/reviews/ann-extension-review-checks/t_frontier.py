import os as _repro_os
_REPRO_ROOT = _repro_os.path.normpath(_repro_os.path.join(
    _repro_os.path.dirname(_repro_os.path.abspath(__file__)), '../../..'))
import sys, time
sys.dont_write_bytecode = True
import numpy as np
import annx
M = annx.Model()
Z = np.load(_REPRO_ROOT + "/research-20260929/open-instances-wave3/ann/ext_logs/open_run2.npz")
Lstar = float(Z["LB"])
order = np.argsort(Z["key"])
rng = np.random.default_rng(3)
sel = list(order[:10]) + list(rng.choice(len(order), 20, replace=False))
t0 = time.time()
lb, info, plain = M.bound(Z["lo"][sel], Z["hi"][sel])
print(f"one-shot bound on 30 frontier boxes: {time.time()-t0:.1f}s")
for q, i in enumerate(sel):
    relw = (Z["hi"][i] - Z["lo"][i]) / (M.hi0 - M.lo0)
    print(f"  key {Z['key'][i]:.4f} mine {lb[q]:.4f} plain {plain[q]:.4f} {info[q]} relw max {relw.max():.2e} min {relw.min():.2e}")
for i in sel[:3] + sel[10:13]:
    t0 = time.time()
    ok, nodes, short, worst = M.prove(Z["lo"][i], Z["hi"][i], Lstar, max_nodes=3000)
    print(f"prove >= L* on box key {Z['key'][i]:.4f}: ok {ok} nodes {nodes} short {short:.4f} worst {worst:.4f} {time.time()-t0:.1f}s", flush=True)
