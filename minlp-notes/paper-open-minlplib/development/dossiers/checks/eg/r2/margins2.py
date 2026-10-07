"""Distribution of the recorded independent margins over all 1,114,361 eg_disc2_s leaves
(copies of publication/eg-recheck/res/*.npz) and total certifier statistics (pieces, splits)."""
import numpy as np, glob, ast
th = [1e-9, 1e-8, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1]
allm, allh, allp = [], [], []
tot = {}; T = 0.0
for p in range(8):
    fs = sorted(glob.glob(f'res/p{p}_c*.npz'))
    mg = np.concatenate([np.load(f)['mg'] for f in fs]); how = np.concatenate([np.load(f)['how'] for f in fs])
    for f in fs:
        z = np.load(f, allow_pickle=True)
        st = z['stats'].item() if z['stats'].dtype == object else ast.literal_eval(str(z['stats']))
        for k, v in st.items(): tot[k] = tot.get(k, 0) + v
        T += float(z['time'])
    allm.append(mg); allh.append(how); allp.append(np.full(mg.size, p))
    print(f"part {p}: {mg.size} leaves; +inf {int(np.isinf(mg).sum())}; min {mg.min():.4e}; #below {[int((mg < t).sum()) for t in th]}")
mg = np.concatenate(allm); how = np.concatenate(allh); pp = np.concatenate(allp)
print("total", mg.size, "; +inf", int(np.isinf(mg).sum()), "; #below", dict(zip(th, [int((mg < t).sum()) for t in th])))
for h in np.unique(how):
    s = how == h
    print(f"  how {int(h)} (0 row, 1 side, 2 lp, 3 farkas, 5 split): {int(s.sum())} leaves, finite {int(np.isfinite(mg[s]).sum())}, min {mg[s].min():.3e}")
print("leaves with margin < 1e-6 outside part 1:", [(int(p), float(m)) for p, m in zip(pp, mg) if m < 1e-6 and p != 1])
print("certifier statistics summed over the 38 chunks:", tot, "; chunk wall time", round(T), "s; pieces per leaf", round(tot['pieces'] / mg.size, 4))
