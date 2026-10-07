"""Distribution of the recorded indep_cert margins over all 1,114,361 eg_disc2_s leaves (eg-recheck res/)."""
import numpy as np, glob
HOW = ["row", "side", "lp", "farkas", "empty", "split"]
th = [1e-8, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2]
M, H = [], []
for p in range(8):
    fs = sorted(glob.glob(f'res/p{p}_c*.npz'))
    mg = np.concatenate([np.load(f)['mg'] for f in fs]); how = np.concatenate([np.load(f)['how'] for f in fs])
    M.append(mg); H.append(how)
    print(f"part {p}: leaves {mg.size}, +inf {int(np.isinf(mg).sum())}, min {mg.min():.3e}; counts below {th}: {[int((mg < t).sum()) for t in th]}")
mg = np.concatenate(M); how = np.concatenate(H)
print("all:", mg.size, "leaves; +inf", int(np.isinf(mg).sum()), "; below", dict(zip(th, [int((mg < t).sum()) for t in th])))
for i, h in enumerate(HOW):
    s = how == i
    if s.any(): print(f"  certificate {h}: {int(s.sum())} leaves, finite margins {int(np.isfinite(mg[s]).sum())}, min {mg[s].min():.3e}")
