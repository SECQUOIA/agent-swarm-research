"""Run the chain B&B prototype on the probe3 family and append JSON lines.

Example:
  python3 run_proto.py --modes quad --amp 0.2 --eps 1e-4 1e-6 --n 2 4 8 --seeds 0 1 2 \
      --workers 4 --out proto.jsonl
"""
import argparse, json, os
from concurrent.futures import ProcessPoolExecutor, as_completed
import numpy as np
import instances as I
import chain_bb as CB


def run(n, seed, eps, mode, amp, unary_sub, tl, max_pairs):
    pr = I.Probe3Chain(I.coeffs(n, seed, amp))
    r = CB.chain_bb(pr, eps, mode=mode, unary_sub=unary_sub, time_limit=tl, max_pairs_iter=max_pairs)
    return dict(family="probe3" if amp == 0.3 else f"probe3_amp{amp}", amp=amp, n=n, seed=seed,
                eps=eps, mode=mode, unary_sub=unary_sub, status=r["status"], LB=r["LB"], UB=r["UB"],
                gap=r["UB"] - r["LB"], iters=r["iters"], pairs=r["pairs"], unary=r["unary"],
                nlocal=r["nlocal"], time=r["time"], final_cells=r["final_cells"],
                max_cells_per_var=max(h["maxK"] for h in r["hist"]) if r["hist"] else None,
                max_pairs_per_iter=int(max(np.diff([0] + [h["pairs"] for h in r["hist"]]))) if r["hist"] else None,
                x=[float(v) for v in r["x"]] if n <= 20 else None)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--modes", nargs="+", default=["quad"])
    ap.add_argument("--amp", type=float, default=0.3)
    ap.add_argument("--eps", nargs="+", type=float, default=[1e-4])
    ap.add_argument("--n", nargs="+", type=int, required=True)
    ap.add_argument("--seeds", nargs="+", type=int, default=[0, 1, 2, 3, 4])
    ap.add_argument("--unary_sub", type=int, default=16)
    ap.add_argument("--tl", type=float, default=600)
    ap.add_argument("--max_pairs", type=int, default=30_000_000)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    done = set()
    if os.path.exists(a.out):
        for line in open(a.out):
            r = json.loads(line)
            done.add((r["n"], r["seed"], r["eps"], r["mode"], r["amp"], r["unary_sub"]))
    jobs = [(n, s, e, m, a.amp, a.unary_sub, a.tl, a.max_pairs)
            for m in a.modes for e in a.eps for n in a.n for s in a.seeds]
    jobs = [j for j in jobs if j[:6] not in done]
    jobs.sort(key=lambda j: -j[0])
    with ProcessPoolExecutor(a.workers) as ex, open(a.out, "a") as f:
        futs = [ex.submit(run, *j) for j in jobs]
        for fu in as_completed(futs):
            r = fu.result()
            f.write(json.dumps(r) + "\n"); f.flush()
            print(r["mode"], r["amp"], r["n"], r["seed"], r["eps"], r["status"], f"{r['gap']:.2e}",
                  r["iters"], r["pairs"], round(r["time"], 2), flush=True)


if __name__ == "__main__":
    main()
