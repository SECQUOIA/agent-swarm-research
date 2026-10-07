"""Aggregation checks on the replayed runs and extraction of all closed regions (leaves).

    python3 leaves.py /tmp/annrev/replay_run1.npz /tmp/annrev/replay_run2.npz /tmp/annrev/leaves.npz npoints
    python3 leaves.py extract replay_runX.npz out.npz     (closed regions of one run only)

1. The replay's final open boxes equal the authors' saved frontiers (open1800_v1.npz, open_run2.npz)
   as multisets of (lo, hi, key) rows, bit for bit.
2. Closed regions: 'pre' and 'proc' boxes; for 'mod' records the removed part (original box minus
   reduced box) as at most 10 slab boxes; 'tiny' boxes.  Also the least lb among closed boxes with
   finite lb, per run.
3. Volume accounting: closed + removed + final open volume = starting volume (floating point).
4. Coverage: random points of the input domain (uniform, and near frontier boxes of both runs)
   must each lie in a closed region of run 1 or run 2, or in a final open box of run 2.
Writes all closed regions of both runs to one npz (lo, hi, kind, run) for verify_boxes.py.
"""
import os as _repro_os
_REPRO_ROOT = _repro_os.path.normpath(_repro_os.path.join(
    _repro_os.path.dirname(_repro_os.path.abspath(__file__)), '../../..'))
import sys

sys.dont_write_bytecode = True
import numpy as np  # noqa: E402

ANN = _REPRO_ROOT + "/research-20260929/open-instances-wave3/ann/ext_logs/"


def rows(lo, hi, key):
    A = np.concatenate([lo, hi, key[:, None]], axis=1)
    return A[np.lexsort(A.T[::-1])]


def slabs(lo, hi, nlo, nhi):
    """boxes covering [lo, hi] minus the open interior of [nlo, nhi] (nlo, nhi inside [lo, hi])."""
    out_lo, out_hi = [], []
    for d in range(lo.shape[1]):
        cl, ch = lo.copy(), hi.copy()
        cl[:, :d] = nlo[:, :d]; ch[:, :d] = nhi[:, :d]
        a = nlo[:, d] > lo[:, d]
        l1, h1 = cl.copy(), ch.copy(); h1[:, d] = nlo[:, d]
        out_lo.append(l1[a]); out_hi.append(h1[a])
        b = nhi[:, d] < hi[:, d]
        l2, h2 = cl.copy(), ch.copy(); l2[:, d] = nhi[:, d]
        out_lo.append(l2[b]); out_hi.append(h2[b])
    return np.concatenate(out_lo), np.concatenate(out_hi)


def vol(lo, hi, V0):
    return float(np.prod(np.maximum(hi - lo, 0.0), axis=1).sum()) / V0


def main(f1, f2, fout, npts):
    R1, R2 = np.load(f1), np.load(f2)
    A1, A2 = np.load(ANN + "open1800_v1.npz"), np.load(ANN + "open_run2.npz")
    for tag, R, A in (("run 1", R1, A1), ("run 2", R2, A2)):
        same = R["lo"].shape == A["lo"].shape and np.array_equal(rows(R["lo"], R["hi"], R["key"]), rows(A["lo"], A["hi"], A["key"]))
        print(f"{tag}: replay processed {int(R['nproc'])} in {int(R['it'])} iterations; final open {R['lo'].shape[0]} "
              f"(authors {A['lo'].shape[0]}); identical frontier rows: {same}; replay LB {float(R['LB'])!r} "
              f"(authors {float(A['LB'])!r}); closed_min {float(R['closed_min'])!r} (authors {float(A['closed_min'])!r}); "
              f"NaN lower bounds {int(R['nan_count'])}")
    lo0 = np.array([0.0] * 5)
    import annx
    M = annx.Model()
    lo0, hi0 = M.lo0, M.hi0
    V0 = float(np.prod(hi0 - lo0))
    L = {"lo": [], "hi": [], "kind": [], "run": []}
    for run, R in ((1, R1), (2, R2)):
        sl_lo, sl_hi = slabs(R["md_lo"], R["md_hi"], R["md_nlo"], R["md_nhi"]) if R["md_lo"].size else (np.zeros((0, 5)),) * 2
        parts = [("pre", R["pre_lo"], R["pre_hi"]), ("proc", R["pr_lo"], R["pr_hi"]), ("slab", sl_lo, sl_hi),
                 ("tiny", R["ti_lo"], R["ti_hi"])]
        tot = 0.0
        for kind, lo, hi in parts:
            lo = lo.reshape(-1, 5); hi = hi.reshape(-1, 5)
            v = vol(lo, hi, V0); tot += v
            print(f"  run {run} {kind:5s}: {lo.shape[0]:8d} boxes, volume {v:.9f}")
            L["lo"].append(lo); L["hi"].append(hi)
            L["kind"].append(np.full(lo.shape[0], {"pre": 0, "proc": 1, "slab": 2, "tiny": 3}[kind]))
            L["run"].append(np.full(lo.shape[0], run))
        # removed volume computed as difference, as the authors log it
        vmod = vol(R["md_lo"].reshape(-1, 5), R["md_hi"].reshape(-1, 5), V0) - vol(R["md_nlo"].reshape(-1, 5), R["md_nhi"].reshape(-1, 5), V0)
        start = V0 / V0 if run == 1 else vol(A1["lo"], A1["hi"], V0)
        vopen = vol(R["lo"], R["hi"], V0)
        print(f"  run {run}: closed+slab volume {tot:.9f} (removed by reduction, as difference {vmod:.9f}); final open {vopen:.9f}; "
              f"sum {tot + vopen:.12f} vs start {start:.12f}")
        pl = R["pr_lb"]
        fin = pl[np.isfinite(pl)]
        print(f"  run {run}: processed-and-closed boxes with finite lb: {fin.size}, least lb {fin.min() if fin.size else np.inf!r}; "
              f"with lb = +inf: {int(np.isinf(pl).sum())}; pre-closed keys min {R['pre_key'].min() if R['pre_key'].size else np.inf!r}")
    for k in L:
        L[k] = np.concatenate(L[k])
    np.savez_compressed(fout, **L)
    # coverage test
    rng = np.random.default_rng(12)
    P = [lo0 + (hi0 - lo0) * rng.random((npts, 5))]
    for Z in (A1, A2):
        i = rng.choice(Z["lo"].shape[0], npts // 2)
        P.append(Z["lo"][i] + (Z["hi"][i] - Z["lo"][i]) * rng.random((npts // 2, 5)))
    P = np.concatenate(P)
    blo = np.concatenate([L["lo"], A2["lo"]]); bhi = np.concatenate([L["hi"], A2["hi"]])
    miss = 0; mult = []
    for p in P:
        inn = np.all((blo <= p) & (p <= bhi), axis=1)
        c = int(inn.sum())
        miss += c == 0
        mult.append(c)
    mult = np.array(mult)
    print(f"coverage: {len(P)} points ({npts} uniform, {npts} near frontier boxes); not covered: {miss}; "
          f"points in more than one region: {int((mult > 1).sum())} (possible only on shared faces or through overlapping slabs)")


def extract(fin, fout):
    """closed regions of one replay only (for verification before the other replay finishes)."""
    R = np.load(fin)
    sl_lo, sl_hi = slabs(R["md_lo"], R["md_hi"], R["md_nlo"], R["md_nhi"]) if R["md_lo"].size else (np.zeros((0, 5)),) * 2
    parts = [(0, R["pre_lo"], R["pre_hi"]), (1, R["pr_lo"], R["pr_hi"]), (2, sl_lo, sl_hi), (3, R["ti_lo"], R["ti_hi"])]
    lo = np.concatenate([p[1].reshape(-1, 5) for p in parts]); hi = np.concatenate([p[2].reshape(-1, 5) for p in parts])
    kind = np.concatenate([np.full(p[1].reshape(-1, 5).shape[0], p[0]) for p in parts])
    np.savez_compressed(fout, lo=lo, hi=hi, kind=kind)
    print(f"{fin}: {lo.shape[0]} closed regions (pre {int((kind == 0).sum())}, proc {int((kind == 1).sum())}, "
          f"slab {int((kind == 2).sum())}, tiny {int((kind == 3).sum())})")


if __name__ == "__main__":
    if sys.argv[1] == "extract":
        extract(sys.argv[2], sys.argv[3])
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]))
