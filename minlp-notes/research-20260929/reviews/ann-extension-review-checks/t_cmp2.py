"""Closure rates on the final run-2 frontier: authors' fbound_combo (processing the box once, with
the objective cut at UB) versus the reviewer's one-shot bound (full LP, no cut), same boxes."""
import os as _repro_os
_REPRO_ROOT = _repro_os.path.normpath(_repro_os.path.join(
    _repro_os.path.dirname(_repro_os.path.abspath(__file__)), '../../..'))
import sys
sys.dont_write_bytecode = True
import numpy as np
sys.path.insert(0, _REPRO_ROOT + "/research-20260929/open-instances-wave3/ann")
import importlib.util
spec = importlib.util.spec_from_file_location("tmmod", _REPRO_ROOT + "/research-20260929/open-instances-wave3/ann/ann_tm.py")
T = importlib.util.module_from_spec(spec); spec.loader.exec_module(T)
AM = T.SepModel(); AM.full_mu = False; AM.old_min_relw = 1.0 / 16; AM.grad_small = True
UB, ub_u = T.incumbent(AM); lag, _ = T.kkt_lag(AM, ub_u); AM.lag = lag
tol = 1e-6 * abs(UB)
Z = np.load(_REPRO_ROOT + "/research-20260929/open-instances-wave3/ann/ext_logs/open_run2.npz")
V = np.load("/tmp/annrev/ver_open_run2.npz")
rng = np.random.default_rng(21)
sel = rng.choice(len(Z["key"]), 4096, replace=False)
lb_a = np.concatenate([AM.fbound_combo(Z["lo"][sel[q:q+512]], Z["hi"][sel[q:q+512]], UB)["lb"] for q in range(0, 4096, 512)])
lb_a = np.maximum(lb_a, Z["key"][sel])
lb_m = V["lb1"][sel]
ca = lb_a >= UB - tol; cm = lb_m >= UB - tol
print(f"4096 random frontier boxes: closed by authors' bound (one processing) {ca.mean():.3f}, by reviewer's one-shot {cm.mean():.3f}, "
      f"both {np.mean(ca & cm):.3f}, only authors {np.mean(ca & ~cm):.3f}, only reviewer {np.mean(~ca & cm):.3f}")
both = np.isfinite(lb_a) & np.isfinite(lb_m)
print(f"  median (reviewer - authors) on boxes finite in both: {np.median((lb_m - lb_a)[both]):.3f}; "
      f"infeasible: authors {np.isinf(lb_a).mean():.3f}, reviewer {np.isinf(lb_m).mean():.3f}")
print(f"  min over sample: authors {lb_a.min():.4f}, reviewer {lb_m.min():.4f}")
