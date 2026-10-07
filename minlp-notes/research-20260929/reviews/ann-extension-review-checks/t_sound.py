"""Soundness sampling of (a) the reviewer's bound annx and (b) the authors' fbound_combo (black box),
on boxes near the optimum, uniform boxes and saved frontier boxes.  For each box: rigorous lb of
both; float-feasible sample points and SLSQP local minimizers (verifier's annv.local_min); any point
with f - lb < 1e-3 is re-evaluated at 50 digits.  A violation is a point feasible at 50 digits
(slack >= 0) inside the box with f < lb.

    python3 t_sound.py nbox_per_family nsamp seed
"""
import os as _repro_os
_REPRO_ROOT = _repro_os.path.normpath(_repro_os.path.join(
    _repro_os.path.dirname(_repro_os.path.abspath(__file__)), '../../..'))
import sys, time
sys.dont_write_bytecode = True
import numpy as np, mpmath as mp
import annx
sys.path.insert(0, _REPRO_ROOT + "/research-20260929/open-instances-wave3/ann")
import importlib.util
spec = importlib.util.spec_from_file_location("tmmod", _REPRO_ROOT + "/research-20260929/open-instances-wave3/ann/ann_tm.py")
T = importlib.util.module_from_spec(spec); spec.loader.exec_module(T)
import annv

nb = int(sys.argv[1]); nsamp = int(sys.argv[2]); seed = int(sys.argv[3])
rng = np.random.default_rng(seed)
M = annx.Model(); D = M.D; FM = annx.float_model()
AM = T.SepModel(); AM.full_mu = False; AM.old_min_relw = 1.0 / 16; AM.grad_small = True
UB, ub_u = T.incumbent(AM); lag, _ = T.kkt_lag(AM, ub_u); AM.lag = lag
lo0, hi0 = M.lo0, M.hi0; W = hi0 - lo0
ustar = np.array(T.U_WAVE3)
Z = np.load(_REPRO_ROOT + "/research-20260929/open-instances-wave3/ann/ext_logs/open_run2.npz")
fams = []
for rho in [0.1, 0.03, 0.01, 0.003, 0.001, 1e-4]:
    B = []
    for _ in range(nb):
        w = W * rho * rng.uniform(0.5, 1.5, 5)
        c = ustar + (rng.random(5) - 0.5) * w
        B.append((np.maximum(lo0, c - w / 2), np.minimum(hi0, c + w / 2)))
    fams.append((f"near-opt rho={rho:g}", B))
for rho in [0.1, 0.01]:
    B = []
    for _ in range(nb):
        w = W * rho * rng.uniform(0.5, 1.5, 5)
        a = lo0 + rng.random(5) * (W - w)
        B.append((a, a + w))
    fams.append((f"uniform rho={rho:g}", B))
order = np.argsort(Z["key"])
pick = np.concatenate([order[:nb], rng.choice(len(order), nb, replace=False)])
fams.append(("run-2 frontier (lowest keys + random)", [(Z["lo"][i], Z["hi"][i]) for i in pick]))
tot_pts = 0; viol_mine = 0; viol_auth = 0; minmarg_mine = np.inf; minmarg_auth = np.inf
t0 = time.time()
for name, B in fams:
    blo = np.array([b[0] for b in B]); bhi = np.array([b[1] for b in B])
    lbm, info, _ = M.bound(blo, bhi)
    Ra = AM.fbound_combo(blo, bhi, np.inf)
    Rb = AM.fbound_combo(blo, bhi, UB + 10.0)
    lba = Ra["lb"]; lbb = np.minimum(Rb["lb"], UB + 10.0)
    npts = 0; fam_min_m = np.inf; fam_min_a = np.inf
    for q in range(len(B)):
        U = blo[q] + (bhi[q] - blo[q]) * rng.random((nsamp, 5))
        f, s, _ = FM.eval(U)
        cand = [U[k] for k in np.nonzero(s >= 0)[0]]
        feas = s >= 0
        for k in range(3):
            u0 = U[feas][np.argmin(f[feas])] if (feas.any() and k == 0) else U[rng.integers(nsamp)]
            fl, sl, ul = annv.local_min(FM, blo[q], bhi[q], u0)
            if sl >= -1e-9:
                cand.append(ul)
        if not cand:
            continue
        C = np.array(cand)
        fc, sc, _ = FM.eval(C)
        for k in range(len(C)):
            fk = fc[k]
            if sc[k] < -1e-9:
                continue
            npts += 1
            mm = fk - lbm[q]; ma = fk - lba[q]; mb = fk - lbb[q] if fk <= UB + 10 else np.inf
            if min(mm, ma, mb) < 1e-3:
                f50, sl50, inb = annx.mp_eval(D, C[k])
                if sl50 >= 0 and inb:
                    mm = float(f50 - mp.mpf(float(lbm[q]))); ma = float(f50 - mp.mpf(float(lba[q])))
                    mb = float(f50 - mp.mpf(float(lbb[q]))) if f50 <= UB + 10 else np.inf
                else:
                    continue
            if mm < 0: viol_mine += 1
            if ma < 0 or mb < 0: viol_auth += 1
            fam_min_m = min(fam_min_m, mm); fam_min_a = min(fam_min_a, ma, mb)
    tot_pts += npts
    minmarg_mine = min(minmarg_mine, fam_min_m); minmarg_auth = min(minmarg_auth, fam_min_a)
    fin = np.isfinite(lbm) & np.isfinite(lba)
    diff = (lba - lbm)[fin]
    print(f"{name:40s} boxes {len(B)} feasible test points {npts:6d} min margin mine {fam_min_m:.4g} authors {fam_min_a:.4g} | "
          f"infeasible: mine {int(np.isinf(lbm).sum())} authors {int(np.isinf(lba).sum())} | "
          f"median (authors lb - mine) {np.median(diff) if diff.size else np.nan:.4g}, max {diff.max() if diff.size else np.nan:.4g} "
          f"({time.time()-t0:.0f}s)", flush=True)
print(f"TOTAL feasible test points {tot_pts}; violations mine {viol_mine}, authors {viol_auth}; "
      f"min margin mine {minmarg_mine:.4g}, authors {minmarg_auth:.4g}")
