"""Generic batched branch and bound over boxes (depth-first stack of chunks).

bound_fn(lo, hi) must return a dict with
    lb     (N,)   rigorous lower bounds (inf = infeasible box)
    ub     (N,)   rigorous objective upper bounds at feasible candidate points (inf if none)
    x      (N, d) the candidate points
    smear  (N, d) branching scores
optionally
    newlo, newhi, mod : boxes reduced by a (valid) monotonicity argument; reduced
                        boxes are re-queued and re-bounded, since their lb is stale
    isint  (d,) bool  : integer coordinates (split at integers)

A box is discarded when lb >= UB - tol_abs; the minimum lb over discarded boxes with
lb <= UB, over boxes that cannot be split, and over boxes left open is the
certified lower bound (together with UB).
"""
import time

import numpy as np

INF = np.inf


def run(bound_fn, lo0, hi0, tol_abs, tlim, UB=INF, xbest=None, batch=4096, log=print, isint=None,
        log_every=200, tiny_rel=1e-15, max_open=40_000_000, mode="depth"):
    """mode 'depth': depth-first stack of chunks; mode 'best': best-first (lowest parent bound first),
    which makes the reported global lower bound increase steadily under a time limit."""
    t0 = time.time()
    d = lo0.shape[0]
    if isint is None:
        isint = np.zeros(d, bool)
    stack = [(lo0[None, :].copy(), hi0[None, :].copy(), np.array([-INF]))]
    nopen = 1
    closed_min = INF
    vol0 = float(np.prod(np.maximum(hi0 - lo0, 1e-300)))
    vclosed = 0.0

    def vol(a, b):
        return float(np.prod(np.maximum(b - a, 0.0), axis=1).sum()) / vol0
    nproc = 0
    it = 0
    while stack:
        it += 1
        if time.time() - t0 > tlim or nopen > max_open:
            break
        if mode == "best" and len(stack) > 1:
            lo = np.concatenate([t[0] for t in stack]); hi = np.concatenate([t[1] for t in stack])
            key = np.concatenate([t[2] for t in stack])
            if lo.shape[0] > batch:
                idx = np.argpartition(key, batch - 1)
                sel, rest = idx[:batch], idx[batch:]
                stack = [(lo[rest], hi[rest], key[rest])]
                lo, hi, key = lo[sel], hi[sel], key[sel]
            else:
                stack = []
        else:
            lo, hi, key = stack.pop()
        if lo.shape[0] > batch:
            stack.append((lo[batch:], hi[batch:], key[batch:]))
            lo, hi, key = lo[:batch], hi[:batch], key[:batch]
        nopen -= lo.shape[0]
        # boxes whose inherited key already exceeds UB - tol need no work
        pre = key >= UB - tol_abs
        if pre.any():
            m = pre & (key <= UB)
            if m.any():
                closed_min = min(closed_min, float(key[m].min()))
            vclosed += vol(lo[pre], hi[pre])
            lo, hi, key = lo[~pre], hi[~pre], key[~pre]
            if lo.shape[0] == 0:
                continue
        nproc += lo.shape[0]
        R = bound_fn(lo, hi)
        lb = np.maximum(R["lb"], key)          # parent bounds remain valid
        j = int(np.argmin(R["ub"]))
        if R["ub"][j] < UB:
            UB, xbest = float(R["ub"][j]), R["x"][j].copy()
        keep = lb < UB - tol_abs
        vclosed += vol(lo[~keep], hi[~keep])
        fath = (~keep) & (lb <= UB)
        if fath.any():
            closed_min = min(closed_min, float(lb[fath].min()))
        lo, hi, lb, smear = lo[keep], hi[keep], lb[keep], R["smear"][keep]
        if "mod" in R:
            mod = R["mod"][keep]
            if mod.any():
                nlo, nhi = R["newlo"][keep][mod], R["newhi"][keep][mod]
                stack.append((nlo, nhi, lb[mod]))
                nopen += nlo.shape[0]
                lo, hi, lb, smear = lo[~mod], hi[~mod], lb[~mod], smear[~mod]
        if lo.shape[0] == 0:
            continue
        w = hi - lo
        k = np.argmax(smear, axis=1)
        r = np.arange(len(k))
        small = w[r, k] <= tiny_rel * np.maximum(1.0, np.abs(lo[r, k]))
        k = np.where(small, np.argmax(w / np.maximum(hi0 - lo0, 1e-300), axis=1), k)
        tiny = w[r, k] <= tiny_rel * np.maximum(1.0, np.abs(lo[r, k]))
        if tiny.any():
            closed_min = min(closed_min, float(lb[tiny].min()))
            lo, hi, lb, k = lo[~tiny], hi[~tiny], lb[~tiny], k[~tiny]
            r = np.arange(len(k))
        mid = 0.5 * (lo[r, k] + hi[r, k])
        isi = isint[k]
        mlo = np.where(isi, np.floor(mid), mid)
        mhi = np.where(isi, np.floor(mid) + 1, mid)
        lo1, hi1 = lo.copy(), hi.copy(); hi1[r, k] = mlo
        lo2, hi2 = lo.copy(), hi.copy(); lo2[r, k] = mhi
        stack.append((np.concatenate([lo1, lo2]), np.concatenate([hi1, hi2]), np.concatenate([lb, lb])))
        nopen += 2 * lo.shape[0]
        if it % log_every == 0:
            omin = min((float(s[2].min()) for s in stack if s[2].size), default=INF)
            log(f"  it {it} processed {nproc} open {nopen} UB {UB:.15g} LB {min(closed_min, omin, UB):.15g}"
                f" closed-volume {vclosed:.6f} t {time.time()-t0:.0f}s")
    omin = min((float(s[2].min()) for s in stack if s[2].size), default=INF)
    LB = min(closed_min, omin, UB)
    return dict(LB=LB, UB=UB, x=xbest, processed=nproc, open=nopen, done=not stack, time=time.time() - t0)
