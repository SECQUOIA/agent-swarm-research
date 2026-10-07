"""eg-recheck: copy of reviews/eg-retry-review-checks/verify_tree.py, modified only to
(a) certify ALL leaves, split into interleaved chunks (leaf index = chunk mod nchunks) so that
several processes can share a part, (b) use MarginCertifier (margin_cert.py: the reviewer's
certifier with margin recording), and (c) save per-leaf results to an npz file.  The coverage
check and the leaf construction are unchanged (see logs/diff_verify_tree.txt).

    python3 recheck_leaves.py <rec.npz> <name> <theta*> <chunk> <nchunks> <out.npz>

Original docstring of verify_tree.py:

Review check of a recorded retry B&B tree (record_run.py output):

1. Coverage: the root box contains the exact (part) domain; every popped box (processed,
   pre-closed, or open at the end) was generated exactly once (root or a child of a kept box);
   children are recomputed here from the reduced box and cover it (continuous: bisection
   with a shared face; integer: [a, m] and [m + 1, b]); reduced boxes lie in their boxes and
   have integral integer bounds; no box was left open and none was forced closed as tiny.
2. Leaves: every closed processed box (whole box, not only its reduced part), every
   pre-closed box, and every slab removed by domain reduction (box minus reduced box,
   decomposed into disjoint slabs; integer slabs start at the next integer) is re-certified
   with the independent code of indep_cert.py against theta* = the claimed bound.

    python3 verify_tree.py <rec.npz> <name> <theta*> [sample_fraction] [seed]
"""
import os
import sys
import time
from fractions import Fraction as Fr

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from margin_cert import MarginCertifier as Certifier  # noqa: E402


def key(lo, hi):
    return lo.tobytes() + hi.tobytes()


def main():
    path, name, theta = sys.argv[1], sys.argv[2], sys.argv[3]
    chunk, nchunks, out = int(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
    frac, seed = 1.0, 0
    z = np.load(path)
    isint = z["isint"]
    C = Certifier(name, theta)
    M = C.M
    # ---------------- 1. coverage
    rlo, rhi = z["root_lo"], z["root_hi"]
    for i in range(M.d):
        if isint[i]:
            assert rlo[i] == np.ceil(rlo[i]) and rhi[i] == np.floor(rhi[i])
            assert Fr(rlo[i]) >= M.qlb[i] and Fr(rhi[i]) <= M.qub[i]      # part of the integer range
        else:
            assert Fr(rlo[i]) <= M.qlb[i] and Fr(rhi[i]) >= M.qub[i]      # contains the exact interval
    part = [(i, rlo[i], rhi[i]) for i in range(M.d) if isint[i] and (Fr(rlo[i]) != M.qlb[i] or Fr(rhi[i]) != M.qub[i])]
    Plo, Phi, Pnlo, Pnhi = z["P_lo"], z["P_hi"], z["P_nlo"], z["P_nhi"]
    keep, tiny, kk = z["P_keep"].astype(bool), z["P_tiny"].astype(bool), z["P_k"]
    gen = {key(rlo, rhi): 1}
    nbad_red = 0
    for n in range(len(Plo)):
        lo, hi, nlo, nhi = Plo[n], Phi[n], Pnlo[n], Pnhi[n]
        if keep[n]:
            nbad_red += int(np.any(nlo < lo) or np.any(nhi > hi) or np.any(nlo > nhi)
                            or np.any(isint & ((nlo != np.ceil(nlo)) | (nhi != np.floor(nhi)))))
            if tiny[n]:
                continue
            k = kk[n]
            mid = 0.5 * (nlo[k] + nhi[k])
            if isint[k]:
                a, b = np.floor(mid), np.floor(mid) + 1
                assert nlo[k] <= a < nhi[k]
            else:
                a = b = mid
                assert nlo[k] <= mid <= nhi[k] and nhi[k] > nlo[k]
            h1 = nhi.copy(); h1[k] = a
            l2 = nlo.copy(); l2[k] = b
            for kb in (key(nlo, h1), key(l2, nhi)):
                gen[kb] = gen.get(kb, 0) + 1
    popped = {}
    for L, H in ((Plo, Phi), (z["C_lo"], z["C_hi"]), (z["open_lo"], z["open_hi"])):
        for lo, hi in zip(L, H):
            kb = key(lo, hi)
            popped[kb] = popped.get(kb, 0) + 1
    cov_ok = gen == popped
    print(f"{os.path.basename(path)}: part {part}; processed {len(Plo)}, pre-closed {len(z['C_lo'])}, "
          f"open {len(z['open_lo'])}, tiny {int(tiny.sum())}; recorded LB {float(z['LB'])!r}")
    print(f"  coverage: generated == popped multiset: {cov_ok} ({sum(gen.values())} boxes); "
          f"bad reduced boxes {nbad_red}")
    # ---------------- 2. leaves
    leaves_lo, leaves_hi, kind = [], [], []
    for n in np.where(~keep)[0]:
        leaves_lo.append(Plo[n]); leaves_hi.append(Phi[n]); kind.append(0)
    for lo, hi in zip(z["C_lo"], z["C_hi"]):
        leaves_lo.append(lo); leaves_hi.append(hi); kind.append(1)
    nslab = 0
    for n in np.where(keep)[0]:
        lo, hi, nlo, nhi = Plo[n].copy(), Phi[n].copy(), Pnlo[n], Pnhi[n]
        cur_lo, cur_hi = lo.copy(), hi.copy()
        for i in range(M.d):
            if nlo[i] > cur_lo[i]:
                s_lo, s_hi = cur_lo.copy(), cur_hi.copy()
                s_hi[i] = nlo[i] - 1 if isint[i] else nlo[i]
                leaves_lo.append(s_lo); leaves_hi.append(s_hi); kind.append(2); nslab += 1
            if nhi[i] < cur_hi[i]:
                s_lo, s_hi = cur_lo.copy(), cur_hi.copy()
                s_lo[i] = nhi[i] + 1 if isint[i] else nhi[i]
                leaves_lo.append(s_lo); leaves_hi.append(s_hi); kind.append(2); nslab += 1
            cur_lo[i], cur_hi[i] = nlo[i], nhi[i]
        if tiny[n]:
            leaves_lo.append(nlo.copy()); leaves_hi.append(nhi.copy()); kind.append(3)
    for lo, hi in zip(z["open_lo"], z["open_hi"]):
        leaves_lo.append(lo); leaves_hi.append(hi); kind.append(4)
    leaves_lo, leaves_hi, kind = np.array(leaves_lo), np.array(leaves_hi), np.array(kind)
    # margin of the original bound over theta* for closed processed boxes (to pick the hardest ones)
    rng = np.random.default_rng(seed)
    sel = np.arange(len(kind))
    if frac < 1.0:
        lbm = np.full(len(kind), np.inf)
        lbm[:int((~keep).sum())] = z["P_lb"][~keep]
        hard = np.argsort(lbm)[:2000]                      # always include the 2000 tightest closures
        rnd = np.where(rng.random(len(kind)) < frac)[0]
        sel = np.union1d(hard, rnd)
    sel = sel[chunk::nchunks]                                  # eg-recheck: this chunk of all leaves
    print(f"  leaves: closed boxes {int((kind == 0).sum())}, pre-closed {int((kind == 1).sum())}, "
          f"slabs {nslab}, tiny {int((kind == 3).sum())}, open {int((kind == 4).sum())}; certifying {len(sel)}")
    t0 = time.time()
    ok = np.zeros(len(kind), bool)
    mg = np.full(len(kind), np.nan)                            # eg-recheck: per-leaf margin
    how = np.full(len(kind), -1, dtype=np.int8)                # eg-recheck: per-leaf certificate
    for s in range(0, len(sel), 512):
        idx = sel[s:s + 512]
        ok[idx] = C.certify_batch(leaves_lo[idx], leaves_hi[idx])
        mg[idx], how[idx] = C.last_mg, C.last_how              # eg-recheck
        if (s // 512) % 10 == 0:
            print(f"    {s + len(idx)}/{len(sel)} done, failures so far {int((~ok[sel[:s + len(idx)]]).sum())}, "
                  f"{time.time() - t0:.0f}s, stats {C.stats}", flush=True)
    fails = sel[~ok[sel]]
    print(f"  independent certification vs theta* = {theta}: certified {len(sel) - len(fails)}/{len(sel)}; "
          f"failures {len(fails)} (by kind {np.bincount(kind[fails], minlength=5).tolist() if len(fails) else []}); "
          f"stats {C.stats}; min LP margin {float(C.min_margin) if C.min_margin is not None else None}; "
          f"time {time.time() - t0:.0f}s")
    for n in fails[:10]:
        print("    failed leaf", kind[n], leaves_lo[n].tolist(), leaves_hi[n].tolist())
    # eg-recheck: save per-leaf results of this chunk
    plb = np.full(len(kind), np.nan)
    plb[:int((~keep).sum())] = z["P_lb"][~keep]                # author's bound of closed processed boxes
    np.savez_compressed(out, n_leaves=len(kind), chunk=chunk, nchunks=nchunks, cov_ok=cov_ok, nbad_red=nbad_red,
                        n_gen=sum(gen.values()), n_proc=len(Plo), n_pre=len(z["C_lo"]), n_open=len(z["open_lo"]),
                        n_tiny=int(tiny.sum()), kind_counts=np.bincount(kind, minlength=5), part=str(part),
                        root_lo=rlo, root_hi=rhi, sel=sel, ok=ok[sel], mg=mg[sel], how=how[sel], kind=kind[sel],
                        plb=plb[sel], lo=leaves_lo[sel], hi=leaves_hi[sel], stats=str(C.stats),
                        min_lp_margin=float(C.min_margin) if C.min_margin is not None else np.nan,
                        time=time.time() - t0)
    print(f"  saved {out}; smallest leaf margin {np.min(mg[sel]) if len(sel) else None}")


if __name__ == "__main__":
    main()
