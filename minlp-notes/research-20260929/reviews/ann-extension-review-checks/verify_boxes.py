"""Prove f >= target on R intersected with each of many boxes, with the reviewer's bound (annx).

    python3 verify_boxes.py in.npz out.npz target nproc [max_nodes]

in.npz: arrays lo, hi (n, 5).  Per box: one-shot bound (plain affine bound, single-side
infeasibility, LP dual); boxes below the target are subdivided (annx.Model.prove) up to max_nodes.
out.npz: lb1 (one-shot bound), ok (proved), nodes, short (lowest bound of a leaf that fell short).
"""
import sys
import time
from multiprocessing import Pool

sys.dont_write_bytecode = True
import numpy as np  # noqa: E402

import annx  # noqa: E402

_M = None


def _init():
    global _M
    _M = annx.Model()


def work(args):
    lo, hi, target, max_nodes = args
    n = lo.shape[0]
    lb = np.empty(n)
    for q in range(0, n, 64):
        lb[q:q + 64] = _M.bound(lo[q:q + 64], hi[q:q + 64], target=target)[0]
    ok = lb >= target
    nodes = np.ones(n, dtype=np.int64)
    short = np.full(n, np.inf)
    for i in np.nonzero(~ok)[0]:
        good, nd, sh, _ = _M.prove(lo[i], hi[i], target, max_nodes=max_nodes)
        ok[i] = good; nodes[i] = nd; short[i] = sh
    return lb, ok, nodes, short


def main(fin, fout, target, nproc, max_nodes=4000):
    Z = np.load(fin)
    lo, hi = Z["lo"], Z["hi"]
    n = lo.shape[0]
    t0 = time.time()
    chunks = [(lo[q:q + 1024], hi[q:q + 1024], target, max_nodes) for q in range(0, n, 1024)]
    out = []
    with Pool(nproc, initializer=_init) as P:
        for k, r in enumerate(P.imap(work, chunks)):
            out.append(r)
            if k % 20 == 0:
                done = sum(len(o[0]) for o in out)
                print(f"  {done}/{n} boxes, not proved so far {sum(int((~o[1]).sum()) for o in out)}, {time.time()-t0:.0f}s", flush=True)
    lb = np.concatenate([o[0] for o in out]); ok = np.concatenate([o[1] for o in out])
    nodes = np.concatenate([o[2] for o in out]); short = np.concatenate([o[3] for o in out])
    np.savez_compressed(fout, lb1=lb, ok=ok, nodes=nodes, short=short, target=target)
    fin_lb = lb[np.isfinite(lb)]
    print(f"DONE {n} boxes in {time.time()-t0:.0f}s: proved {int(ok.sum())}, not proved {int((~ok).sum())}; "
          f"one-shot: infeasible {int(np.isinf(lb).sum())}, >= target {int((lb >= target).sum())}, "
          f"min finite one-shot lb {fin_lb.min() if fin_lb.size else np.inf!r}; subdivided {int((nodes > 1).sum())}, "
          f"max nodes {int(nodes.max())}", flush=True)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], float(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]) if len(sys.argv) > 5 else 4000)
