"""Rigorous re-certification of a sample of leaves with the verifier's own interval code (own_ia.py).

    python3 own_sample.py <parts comma list> <ntight> <nrandom> <nlow> <max_pieces> <out tag>

Per part: the <ntight> leaves with the smallest margins recorded by the eg-recheck run, <nrandom>
uniformly random leaves (seed 7 + part), and the <nlow> leaves with the smallest float F at a
feasible sample point (minF_p<k>.npy from own_consistency.py; skipped if absent).  Leaf boxes
come from leaves_p<k>.npz (re-derived from the recorded tree by own_bookkeeping.py and checked
equal to the certified boxes).  Threshold theta* = 5.642100574331458 (exact decimal).
"""
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from own_ia import Cert  # noqa: E402

parts = [int(v) for v in sys.argv[1].split(",")]
ntight, nrand, nlow, maxp, tag = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
C = Cert("5.642100574331458")
print(f"theta* = {C.theta} (exact), compared against the double {C.th_up!r} >= theta*", flush=True)
for p in parts:
    z = np.load(os.path.join(HERE, f"leaves_p{p}.npz"))
    lo, hi, mg, how = z["lo"], z["hi"], z["mg"], z["how"]
    n = len(lo)
    fin = np.flatnonzero(np.isfinite(mg))
    tight = fin[np.argsort(mg[fin], kind="stable")[:ntight]]
    rnd = np.random.default_rng(7 + p).choice(n, size=nrand, replace=False)
    low = np.array([], int)
    f = os.path.join(HERE, f"minF_p{p}.npy")
    if nlow and os.path.exists(f):
        mf = np.load(f)
        low = np.argsort(mf, kind="stable")[:nlow]
    groups = {"tight": tight, "random": rnd, "lowF": low}
    sel = np.unique(np.concatenate([tight, rnd, low]))
    t0 = time.time()
    st, pieces, minmg, ninf, maxd = C.certify(lo[sel], hi[sel], max_pieces=maxp, log=sys.stdout)
    dt = time.time() - t0
    print(f"part {p}: {len(sel)} distinct leaves; certified {int(st.sum())}/{len(sel)}; pieces {int(pieces.sum())} "
          f"(max {int(pieces.max())}); max depth {int(maxd.max())}; {dt:.0f}s", flush=True)
    for g, idx in groups.items():
        if not len(idx):
            continue
        m = np.isin(sel, idx)
        ok = st[m]
        mm = minmg[m]
        print(f"   {g:6s}: {len(idx)} leaves, certified {int(ok.sum())}, failures {int((ok == 0).sum())}; "
              f"own smallest margin {np.min(mm):.4g}; indep_cert margins of the group: min {np.min(mg[sel[m]]):.4g}; "
              f"pieces median {int(np.median(pieces[m]))}, max {int(pieces[m].max())}; leaves with infeasible pieces "
              f"{int((ninf[m] > 0).sum())}", flush=True)
    for j in np.flatnonzero(st == 0)[:20]:
        print(f"   NOT CERTIFIED by own code: leaf {sel[j]} (indep_cert margin {mg[sel[j]]:.3g}, how {how[sel[j]]}), "
              f"pieces {pieces[j]}, box lo {lo[sel[j]].tolist()} hi {hi[sel[j]].tolist()}", flush=True)
    np.savez_compressed(os.path.join(HERE, f"sample_{tag}_p{p}.npz"), sel=sel, st=st, pieces=pieces, minmg=minmg,
                        ninf=ninf, maxd=maxd, tight=tight, rnd=rnd, low=low, mg=mg[sel], how=how[sel])
