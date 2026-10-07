"""Verifier's own bookkeeping check of the eg-recheck results (review r1).  Own code: it reads the
recorded trees (rec/*.npz) and the per-chunk results (res/*.npz) with numpy only.

Per part:
  * re-derives the leaf list from the recorded tree with its own loop (closed processed boxes,
    then the slabs B \\ R of every kept box, peeled coordinate by coordinate; integer slabs start
    at the next integer) and checks it equals, box for box, the boxes certified in the chunks;
  * chunk index sets partition {0..n-1} (none missing, none repeated);
  * every saved result: ok True, margin > 0 (or +inf), certificate code in 0..5;
  * tree shape: processed = 1 + 2 * (kept boxes), no tiny / pre-closed / open boxes;
  * per-part statistics (leaves, closed, slabs, infeasible, certificate counts, smallest margin
    with its leaf kind and certificate, CPU seconds) for comparison with the report;
  * the threshold string printed in every chunk log.
Writes leaves_p<k>.npz (lo, hi, kind, mg, how) for the other checks.
"""
import glob
import os
import re
import sys

import numpy as np

TR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "eg-recheck")
OUT = os.path.dirname(os.path.abspath(__file__))
HOW = ["row", "side", "lp", "farkas", "empty", "split"]

tot_leaves = tot_cpu = 0
allgood = True
for p in range(8):
    z = np.load(os.path.join(TR, "rec", f"rec_disc2_p{p}.npz"))
    isint = z["isint"]
    Plo, Phi, Pnlo, Pnhi, keep = z["P_lo"], z["P_hi"], z["P_nlo"], z["P_nhi"], z["P_keep"].astype(bool)
    assert len(z["C_lo"]) == 0 and len(z["open_lo"]) == 0 and not z["P_tiny"].any()
    nproc, nkeep = len(Plo), int(keep.sum())
    shape_ok = nproc == 1 + 2 * nkeep
    # own leaf derivation
    L_lo = [Plo[~keep]]
    L_hi = [Phi[~keep]]
    kinds = [np.zeros(int((~keep).sum()), int)]
    slo, shi = [], []
    for n in np.flatnonzero(keep):
        blo, bhi = Plo[n].copy(), Phi[n].copy()
        rlo, rhi = Pnlo[n], Pnhi[n]
        assert np.all(rlo >= blo) and np.all(rhi <= bhi) and np.all(rlo <= rhi)
        for i in range(7):
            if rlo[i] > blo[i]:
                a, b = blo.copy(), bhi.copy()
                b[i] = rlo[i] - 1 if isint[i] else rlo[i]
                slo.append(a); shi.append(b)
            if rhi[i] < bhi[i]:
                a, b = blo.copy(), bhi.copy()
                a[i] = rhi[i] + 1 if isint[i] else rhi[i]
                slo.append(a); shi.append(b)
            blo[i], bhi[i] = rlo[i], rhi[i]
    if slo:
        L_lo.append(np.array(slo)); L_hi.append(np.array(shi)); kinds.append(np.full(len(slo), 2))
    Llo, Lhi, Lk = np.concatenate(L_lo), np.concatenate(L_hi), np.concatenate(kinds)
    n = len(Llo)
    # chunks
    files = sorted(glob.glob(os.path.join(TR, "res", f"p{p}_c*.npz")))
    Z = [np.load(f) for f in files]
    nch = len(Z)
    assert all(int(c["nchunks"]) == nch for c in Z) and sorted(int(c["chunk"]) for c in Z) == list(range(nch))
    sel = np.concatenate([c["sel"] for c in Z])
    part_ok = len(sel) == n and np.array_equal(np.sort(sel), np.arange(n)) and all(int(c["n_leaves"]) == n for c in Z)
    mg = np.full(n, np.nan); how = np.full(n, -9); ok = np.zeros(n, bool)
    box_ok = True
    for c in Z:
        s = c["sel"]
        box_ok &= bool(np.array_equal(c["lo"], Llo[s]) and np.array_equal(c["hi"], Lhi[s]) and np.array_equal(c["kind"], Lk[s]))
        box_ok &= bool(np.array_equal(c["root_lo"], z["root_lo"]) and np.array_equal(c["root_hi"], z["root_hi"]))
        mg[s], how[s], ok[s] = c["mg"], c["how"], c["ok"]
    cpu = sum(float(c["time"]) for c in Z)
    good = part_ok and box_ok and ok.all() and bool(np.all(mg > 0)) and bool(np.all((how >= 0) & (how <= 5))) and shape_ok
    allgood &= good
    tot_leaves += n; tot_cpu += cpu
    hc = np.bincount(how, minlength=6)
    fin = np.isfinite(mg)
    j = np.flatnonzero(fin)[np.argmin(mg[fin])]
    # thresholds in the chunk logs
    th = set()
    for f in glob.glob(os.path.join(TR, "logs", f"cert_p{p}_c*.log")):
        th |= set(re.findall(r"vs theta\* = ([0-9.]+): certified (\d+)/(\d+); failures (\d+)", open(f).read()))
    th_ok = all(t[0] == "5.642100574331458" and t[1] == t[2] and t[3] == "0" for t in th) and len(th) >= 1
    nlog = sum(int(t[2]) for t in th) if len(th) == nch else None
    print(f"part {p}: root lo {z['root_lo'].tolist()} hi {z['root_hi'].tolist()}")
    print(f"  processed {nproc}, kept {nkeep}, processed == 1 + 2 kept: {shape_ok}; leaves {n} "
          f"(closed {int((Lk == 0).sum())}, slabs {int((Lk == 2).sum())}); chunks {nch}; partition ok {part_ok}; "
          f"boxes identical to own derivation {box_ok}")
    print(f"  ok {int(ok.sum())}/{n}; all margins > 0: {bool(np.all(mg > 0))}; infeasible (+inf) {int((mg == np.inf).sum())}; "
          f"how " + ", ".join(f"{HOW[i]} {int(hc[i])}" for i in range(6)))
    print(f"  smallest margin {mg[j]:.4g} at leaf {j} (kind {'closed' if Lk[j] == 0 else 'slab'}, how {HOW[how[j]]}); "
          f"smallest LP-certified (how=lp) margin {mg[how == 2].min() if (how == 2).any() else None}; CPU {cpu:.0f}s")
    print(f"  chunk logs: thresholds {sorted(set(t[0] for t in th))}, all certified with 0 failures: {th_ok}, "
          f"log total {nlog}")
    print(f"  PART {p} {'GOOD' if good and th_ok else 'PROBLEM'}")
    allgood &= th_ok
    np.savez_compressed(os.path.join(OUT, f"leaves_p{p}.npz"), lo=Llo, hi=Lhi, kind=Lk, mg=mg, how=how,
                        root_lo=z["root_lo"], root_hi=z["root_hi"], isint=isint)
    sys.stdout.flush()
print(f"total leaves {tot_leaves}; total CPU {tot_cpu:.0f}s; ALL GOOD: {allgood}")
