"""Replay of the authors' two branch-and-bound runs with leaf recording (reviewer's driver).

The authors' bounding code (ext_logs/ann_tm_v1_snapshot.py for run 1, ann_tm.py for run 2) is
used as a black box: only M.fbound_combo, incumbent and kkt_lag are called.  The loop below
re-implements the queue logic of ann_tm.bnb operation by operation (the same array operations in
the same order, so that argpartition ties and the order of children are reproduced), and in
addition records every region that the run closes:

  pre   : boxes popped with key >= UB - tol (closed without bounding)
  proc  : processed boxes with lb >= UB - tol (including lb = +inf: proved infeasible / emptied)
  mod   : processed boxes replaced by a domain-reduced sub-box (the removed part is closed)
  tiny  : boxes too narrow to split (closed with their lb)

It stops when the number of processed boxes reaches the count printed in the authors' log, prints
log lines in the authors' format for comparison, and saves the final open boxes and all records.

    python3 replay.py run1|run2 out.npz
"""
import os as _repro_os
_REPRO_ROOT = _repro_os.path.normpath(_repro_os.path.join(
    _repro_os.path.dirname(_repro_os.path.abspath(__file__)), '../../..'))
import importlib.util
import sys
import time

sys.dont_write_bytecode = True
import numpy as np  # noqa: E402

ANN = _REPRO_ROOT + "/research-20260929/open-instances-wave3/ann"
sys.path.insert(0, ANN)
INF = np.inf


def load(path):
    spec = importlib.util.spec_from_file_location("tmmod", path)
    T = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(T)
    return T


def main(which, out):
    if which == "run1":
        T = load(ANN + "/ext_logs/ann_tm_v1_snapshot.py")
        M = T.SepModel()
        target, init_file = 563656, None
    else:
        T = load(ANN + "/ann_tm.py")
        M = T.SepModel()
        M.full_mu = False
        M.old_min_relw = 1.0 / 16
        M.grad_small = True
        target, init_file = 2134528, ANN + "/ext_logs/open1800_v1.npz"
    UB, ub_u = T.incumbent(M)
    print(f"incumbent {UB!r}", flush=True)
    lag, res = T.kkt_lag(M, ub_u)
    M.lag = lag
    print("Lagrangian terms:", [(M.names[j], float(l), float(b), s) for j, l, b, s in lag], flush=True)
    tol_abs = 1e-6 * abs(UB)
    batch = 512
    if init_file is None:
        lo = M.lo0[None, :].copy(); hi = M.hi0[None, :].copy(); key = np.array([-INF])
        closed_min = INF
    else:
        Z = np.load(init_file)
        lo, hi, key = Z["lo"], Z["hi"], Z["key"]
        closed_min = float(Z["closed_min"])
    vol0 = float(np.prod(M.hi0 - M.lo0))
    vol = lambda a, b: float(np.prod(np.maximum(b - a, 0.0), axis=1).sum()) / vol0
    rec = {k: [] for k in ("pre_lo", "pre_hi", "pre_key", "pr_lo", "pr_hi", "pr_lb", "pr_rlb", "pr_bk", "pr_lbtm",
                           "pr_lbold", "pr_it", "md_lo", "md_hi", "md_nlo", "md_nhi", "md_lb", "md_it",
                           "ti_lo", "ti_hi", "ti_lb")}
    nan_count = 0
    vclosed = 0.0; vred = 0.0
    nproc = 0; it = 0
    t0 = time.time()
    while lo.shape[0] > 0 and nproc < target:
        it += 1
        if lo.shape[0] > batch:
            idx = np.argpartition(key, batch - 1)[:batch]
            rest = np.ones(lo.shape[0], bool); rest[idx] = False
            blo, bhi, bk = lo[idx], hi[idx], key[idx]
            lo, hi, key = lo[rest], hi[rest], key[rest]
        else:
            blo, bhi, bk = lo, hi, key
            lo, hi, key = lo[:0], hi[:0], key[:0]
        pre = bk >= UB - tol_abs
        if pre.any():
            m_ = pre & (bk <= UB)
            if m_.any():
                closed_min = min(closed_min, float(bk[m_].min()))
            vclosed += vol(blo[pre], bhi[pre])
            rec["pre_lo"].append(blo[pre]); rec["pre_hi"].append(bhi[pre]); rec["pre_key"].append(bk[pre])
            blo, bhi, bk = blo[~pre], bhi[~pre], bk[~pre]
            if blo.shape[0] == 0:
                continue
        nproc += blo.shape[0]
        R = M.fbound_combo(blo, bhi, UB)
        nan_count += int(np.isnan(R["lb"]).sum())
        lb = np.maximum(R["lb"], bk)
        j = int(np.argmin(R["ub"]))
        if R["ub"][j] < UB:
            print(f"UB update {R['ub'][j]!r} (replay keeps the authors' logic)", flush=True)
            UB = float(R["ub"][j])
        keep = lb < UB - tol_abs
        vclosed += vol(blo[~keep], bhi[~keep])
        fath = (~keep) & (lb <= UB)
        if fath.any():
            closed_min = min(closed_min, float(lb[fath].min()))
        nk = ~keep
        rec["pr_lo"].append(blo[nk]); rec["pr_hi"].append(bhi[nk]); rec["pr_lb"].append(lb[nk])
        rec["pr_rlb"].append(R["lb"][nk]); rec["pr_bk"].append(bk[nk])
        rec["pr_lbtm"].append(R["lb_tm"][nk]); rec["pr_lbold"].append(R["lb_old"][nk])
        rec["pr_it"].append(np.full(int(nk.sum()), it))
        blo, bhi, lb, smear = blo[keep], bhi[keep], lb[keep], R["smear"][keep]
        mod = R["mod"][keep]
        if mod.any():
            nlo, nhi = R["newlo"][keep][mod], R["newhi"][keep][mod]
            vred += vol(blo[mod], bhi[mod]) - vol(nlo, nhi)
            rec["md_lo"].append(blo[mod]); rec["md_hi"].append(bhi[mod]); rec["md_nlo"].append(nlo)
            rec["md_nhi"].append(nhi); rec["md_lb"].append(lb[mod]); rec["md_it"].append(np.full(int(mod.sum()), it))
            lo = np.concatenate([lo, nlo]); hi = np.concatenate([hi, nhi]); key = np.concatenate([key, lb[mod]])
            blo, bhi, lb, smear = blo[~mod], bhi[~mod], lb[~mod], smear[~mod]
        if blo.shape[0]:
            w = bhi - blo
            k = np.argmax(smear, axis=1)
            r = np.arange(len(k))
            tiny = w[r, k] <= 1e-15 * np.maximum(1.0, np.abs(blo[r, k]))
            if tiny.any():
                closed_min = min(closed_min, float(lb[tiny].min()))
                vclosed += vol(blo[tiny], bhi[tiny])
                rec["ti_lo"].append(blo[tiny]); rec["ti_hi"].append(bhi[tiny]); rec["ti_lb"].append(lb[tiny])
                blo, bhi, lb, k = blo[~tiny], bhi[~tiny], lb[~tiny], k[~tiny]
                r = np.arange(len(k))
            mid = 0.5 * (blo[r, k] + bhi[r, k])
            l1, h1 = blo.copy(), bhi.copy(); h1[r, k] = mid
            l2, h2 = blo.copy(), bhi.copy(); l2[r, k] = mid
            lo = np.concatenate([lo, l1, l2]); hi = np.concatenate([hi, h1, h2]); key = np.concatenate([key, lb, lb])
        if it % 25 == 0:
            glb = min(closed_min, key.min() if key.size else INF, UB)
            print(f"  it {it} processed {nproc} open {lo.shape[0]} UB {UB:.15g} LB {glb:.15g} closed-vol {vclosed:.6f} "
                  f"reduced-vol {vred:.6f} t {time.time()-t0:.0f}s nan {nan_count}", flush=True)
    omin = key.min() if key.size else INF
    LB = min(closed_min, omin, UB)
    print(f"END it {it} processed {nproc} open {lo.shape[0]} closed_min {closed_min!r} omin {omin!r} LB {LB!r} "
          f"vclosed {vclosed:.6f} vred {vred:.6f} nan {nan_count} t {time.time()-t0:.0f}s", flush=True)
    cat = {}
    for k, v in rec.items():
        cat[k] = np.concatenate(v) if v else np.zeros((0,))
    np.savez_compressed(out, lo=lo, hi=hi, key=key, UB=UB, LB=LB, closed_min=closed_min, nproc=nproc, it=it,
                        nan_count=nan_count, tol_abs=tol_abs, **cat)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
