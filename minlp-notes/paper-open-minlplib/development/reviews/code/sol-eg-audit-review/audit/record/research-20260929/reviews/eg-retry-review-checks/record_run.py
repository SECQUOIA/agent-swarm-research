"""Review tool: replay a retry B&B run (egbb.py, unchanged models and bounding) with a copy of
BB.run that records every node, so that the tree can be checked for coverage and every leaf
re-certified with independent code (indep_cert.py).

The loop below is egbb.BB.run with recording lines added (marked '# REC'); nothing else
changed.  The replay must reproduce the processed-box count and certified value of the
original log, which shows that it follows the same tree.

Recorded per processed box: lo, hi (box as popped), theta, key (parent bound), lb (after
max with key and the NaN guard), reduced box nlo/nhi, kept flag (split), split coordinate
and children, tiny flag; per pre-closed box (key >= theta): lo, hi, key, theta.

    python3 record_run.py <name> <tol_rel> <time_s> <out.npz> [k K]
"""
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RETRY = os.path.join(HERE, "..", "..", "open-instances-wave3", "eg", "retry")
sys.path.insert(0, RETRY)
import egbb  # noqa: E402

INF = np.inf


class RecBB(egbb.BB):
    def run(self, tlim, UB, xbest, lo0=None, hi0=None, init=None, batch=256, log_every=20, save=None,
            polish=None, ncand=4):
        M = self.M
        t0 = time.time()
        REC = dict(P_lo=[], P_hi=[], P_theta=[], P_key=[], P_lb=[], P_nlo=[], P_nhi=[], P_keep=[],
                   P_tiny=[], P_k=[], P_UBafter=[], C_lo=[], C_hi=[], C_key=[], C_theta=[])  # REC
        self.REC = REC  # REC
        if init is not None:
            lo, hi, key = init
        else:
            lo = (M.lo0 if lo0 is None else lo0)[None, :].copy()
            hi = (M.hi0 if hi0 is None else hi0)[None, :].copy()
            key = np.array([-INF])
        theta_min = INF
        forced_min = INF
        nproc = 0
        it = 0
        polished = set()
        while lo.shape[0] > 0 and time.time() - t0 < tlim:
            it += 1
            theta = UB - self.tol
            assert np.isfinite(theta)
            m = min(batch, lo.shape[0])
            if lo.shape[0] > m:
                idx = np.argpartition(key, m - 1)
                sel, rest = idx[:m], idx[m:]
                blo, bhi, bkey = lo[sel], hi[sel], key[sel]
                lo, hi, key = lo[rest], hi[rest], key[rest]
            else:
                blo, bhi, bkey = lo, hi, key
                lo, hi, key = lo[:0], hi[:0], key[:0]
            theta_min = min(theta_min, theta)
            pre = bkey >= theta
            REC["C_lo"].append(blo[pre]); REC["C_hi"].append(bhi[pre])  # REC
            REC["C_key"].append(bkey[pre]); REC["C_theta"].append(np.full(int(pre.sum()), theta))  # REC
            blo, bhi, bkey = blo[~pre], bhi[~pre], bkey[~pre]
            if blo.shape[0] == 0:
                continue
            nproc += blo.shape[0]
            lb, nlo, nhi, sc = self.bound(blo, bhi, theta)
            lb = np.where(np.isnan(lb), -INF, lb)
            lb = np.maximum(lb, bkey)
            order = np.argsort(np.where(np.isfinite(lb), lb, INF))[:ncand]
            cand = 0.5 * (nlo[order] + nhi[order])
            cand[:, M.isint] = np.clip(np.round(cand[:, M.isint]), nlo[order][:, M.isint], nhi[order][:, M.isint])
            cand = np.clip(cand, M.lo_in, M.hi_in)
            if len(order):
                fc = self.fpoint(cand, fast=True)
                j = int(np.argmin(fc))
                if fc[j] < UB:
                    f = self.fpoint(cand[j][None])[0]
                    if f < UB:
                        UB, xbest = float(f), cand[j].copy()
                if polish is not None:
                    ci = tuple(cand[0][M.isint].astype(int))
                    if ci not in polished:
                        polished.add(ci)
                        xp = polish(cand[0])
                        if xp is not None:
                            f = self.fpoint(xp[None])[0]
                            if f < UB:
                                UB, xbest = float(f), xp.copy()
            keep = lb < UB - self.tol
            # REC: per processed box
            w_all = nhi - nlo
            sc_all = np.where(w_all > 0, sc, -1.0)
            k_all = np.argmax(sc_all, axis=1)
            tiny_all = w_all[np.arange(len(k_all)), k_all] <= 1e-13 * np.maximum(1.0, np.abs(nlo[np.arange(len(k_all)), k_all]))
            REC["P_lo"].append(blo); REC["P_hi"].append(bhi); REC["P_theta"].append(np.full(len(lb), theta))
            REC["P_key"].append(bkey); REC["P_lb"].append(lb.copy()); REC["P_nlo"].append(nlo.copy())
            REC["P_nhi"].append(nhi.copy()); REC["P_keep"].append(keep.copy()); REC["P_tiny"].append(tiny_all & keep)
            REC["P_k"].append(k_all); REC["P_UBafter"].append(np.full(len(lb), UB))
            # end REC
            nlo, nhi, lb, sc = nlo[keep], nhi[keep], lb[keep], sc[keep]
            if nlo.shape[0] == 0:
                continue
            w = nhi - nlo
            sc = np.where(w > 0, sc, -1.0)
            k = np.argmax(sc, axis=1)
            r_ = np.arange(len(k))
            tiny = w[r_, k] <= 1e-13 * np.maximum(1.0, np.abs(nlo[r_, k]))
            if tiny.any():
                forced_min = min(forced_min, float(lb[tiny].min()))
                nlo, nhi, lb, k = nlo[~tiny], nhi[~tiny], lb[~tiny], k[~tiny]
                r_ = np.arange(len(k))
            mid = 0.5 * (nlo[r_, k] + nhi[r_, k])
            isi = M.isint[k]
            mlo = np.where(isi, np.floor(mid), mid)
            mhi = np.where(isi, np.floor(mid) + 1, mid)
            lo1, hi1 = nlo.copy(), nhi.copy(); hi1[r_, k] = mlo
            lo2, hi2 = nlo.copy(), nhi.copy(); lo2[r_, k] = mhi
            lo = np.concatenate([lo, lo1, lo2]); hi = np.concatenate([hi, hi1, hi2])
            key = np.concatenate([key, lb, lb])
            if it % log_every == 0:
                omin = key.min() if key.size else INF
                self.log(f"  it {it} processed {nproc} open {lo.shape[0]} UB {UB:.12g} LB "
                         f"{min(theta_min, omin, forced_min, UB):.12g} lp {self.lp.n} ({self.lp.t:.0f}s) "
                         f"{self.stats} t {time.time()-t0:.0f}s")
                sys.stdout.flush()
        omin = key.min() if key.size else INF
        theta_min = min(theta_min, UB - self.tol)
        LB = min(theta_min, omin, forced_min, UB)
        REC["open_lo"] = lo; REC["open_hi"] = hi  # REC
        return dict(LB=LB, UB=UB, x=xbest, processed=nproc, open=lo.shape[0], done=lo.shape[0] == 0,
                    time=time.time() - t0, theta_min=theta_min, omin=omin, forced_min=forced_min)


def main():
    name, tol_rel, tlim, out = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
    sys.path.insert(0, os.path.join(RETRY, "..", "..", "..", "open-instances-wave2", "small"))
    import ev
    bb = RecBB(name, 0.0)
    M = bb.M
    vals = ev.read_sol(os.path.join(RETRY, "..", "..", "sol", f"{name}.p1.sol"))
    x0 = np.array([float(vals.get(n, "0")) for n in M.D.M["names"]])
    pol = egbb.make_polish(bb)
    xp = pol(x0)
    f0 = bb.fpoint(x0[None])[0]
    fp = bb.fpoint(xp[None])[0] if xp is not None else INF
    UB, xb = (fp, xp) if fp < f0 else (f0, x0)
    print(f"== {name}: listed p1 rigorous F = {f0!r}; polished F = {fp!r}", flush=True)
    bb.tol = tol_rel * max(1.0, abs(UB) if np.isfinite(UB) else 10.0)
    lo0, hi0 = M.lo0.copy(), M.hi0.copy()
    if len(sys.argv) > 6:
        k, K = int(sys.argv[5]), int(sys.argv[6])
        ii = np.where(M.isint)[0]
        j = ii[np.argmax(hi0[ii] - lo0[ii])]
        vals_j = np.arange(lo0[j], hi0[j] + 1)
        chunks = np.array_split(vals_j, K)
        lo0[j], hi0[j] = chunks[k][0], chunks[k][-1]
        print(f"part {k} of {K}: {M.D.M['names'][j]} in [{lo0[j]:g}, {hi0[j]:g}]")
    r = bb.run(tlim, UB, xb, lo0=lo0, hi0=hi0, polish=pol)
    print(f"B&B: done={r['done']} processed {r['processed']} open {r['open']} time {r['time']:.0f}s "
          f"lp {bb.lp.n} ({bb.lp.t:.0f}s) {bb.stats}")
    print(f"  certified lower bound {r['LB']!r} (theta_min {r['theta_min']!r}, open min {r['omin']!r}, "
          f"forced {r['forced_min']!r}); UB {r['UB']!r} at {np.asarray(r['x']).tolist()}")
    R = bb.REC
    cat = lambda L, shape: np.concatenate(L) if L else np.zeros(shape)
    d = M.d
    np.savez_compressed(out, root_lo=lo0, root_hi=hi0, tol=bb.tol, LB=r["LB"], UB=r["UB"], x=np.asarray(r["x"]),
                        isint=M.isint,
                        P_lo=cat(R["P_lo"], (0, d)), P_hi=cat(R["P_hi"], (0, d)), P_theta=cat(R["P_theta"], (0,)),
                        P_key=cat(R["P_key"], (0,)), P_lb=cat(R["P_lb"], (0,)), P_nlo=cat(R["P_nlo"], (0, d)),
                        P_nhi=cat(R["P_nhi"], (0, d)), P_keep=cat(R["P_keep"], (0,)), P_tiny=cat(R["P_tiny"], (0,)),
                        P_k=cat(R["P_k"], (0,)), P_UBafter=cat(R["P_UBafter"], (0,)),
                        C_lo=cat(R["C_lo"], (0, d)), C_hi=cat(R["C_hi"], (0, d)), C_key=cat(R["C_key"], (0,)),
                        C_theta=cat(R["C_theta"], (0,)), open_lo=R["open_lo"], open_hi=R["open_hi"])
    print(f"recorded {sum(len(a) for a in R['P_lb'])} processed and {sum(len(a) for a in R['C_key'])} pre-closed boxes -> {out}")


if __name__ == "__main__":
    main()
