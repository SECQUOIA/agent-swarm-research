"""SCIP and prototype runs on the lot-sizing chain; one JSON line per run.

  python3 run_lotsizing.py scip  --T 5 10 --seeds 0 1 2 --eps 1e-4 --tl 300 --workers 4 --out f.jsonl
  python3 run_lotsizing.py proto --T 5 10 --seeds 0 1 2 --eps 1e-4 --workers 4 --out f.jsonl
"""
import argparse, json, os, time
from concurrent.futures import ProcessPoolExecutor, as_completed
import lotsizing as LS
import chain_bb as CB


def scip(T, seed, eps, tl):
    m, d = LS.build_scip(T, seed)
    m.setParam("timing/clocktype", 1)
    m.setParam("limits/time", tl)
    m.setParam("limits/absgap", eps)
    m.setParam("limits/gap", 0.0)
    t0 = time.time(); m.optimize()
    pb, db = m.getPrimalbound(), m.getDualbound()
    return dict(family="lotsizing", solver="scip", n=T, seed=seed, eps=eps, tl=tl, status=m.getStatus(),
                nodes=m.getNNodes(), time=m.getSolvingTime(), wall=time.time() - t0, primal=pb, dual=db,
                absgap=pb - db, clock="cpu")


def proto(T, seed, eps, tl, mode="split"):
    pr = LS.LotSizingChain(LS.demands(T, seed))
    r = CB.chain_bb(pr, eps, mode=mode, time_limit=tl, max_pairs_iter=40_000_000)
    return dict(family="lotsizing", solver="proto", mode=mode, n=T, seed=seed, eps=eps, status=r["status"],
                LB=r["LB"], UB=r["UB"], gap=r["UB"] - r["LB"], iters=r["iters"], pairs=r["pairs"],
                time=r["time"], max_cells_per_var=max(h["maxK"] for h in r["hist"]) if r["hist"] else None,
                n_idle_periods=int(((r["x"][1:] - r["x"][:-1] + pr.d) < 1e-6).sum()))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("solver", choices=["scip", "proto"])
    ap.add_argument("--T", nargs="+", type=int, required=True)
    ap.add_argument("--seeds", nargs="+", type=int, default=[0, 1, 2])
    ap.add_argument("--eps", nargs="+", type=float, default=[1e-4])
    ap.add_argument("--tl", type=float, default=300)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    done = set()
    if os.path.exists(a.out):
        done = {(r["solver"], r["n"], r["seed"], r["eps"]) for r in map(json.loads, open(a.out))}
    jobs = [(T, s, e, a.tl) for e in a.eps for T in a.T for s in a.seeds if (a.solver, T, s, e) not in done]
    jobs.sort(key=lambda j: -j[0])
    fn = scip if a.solver == "scip" else proto
    with ProcessPoolExecutor(a.workers) as ex, open(a.out, "a") as f:
        futs = [ex.submit(fn, *j) for j in jobs]
        for fu in as_completed(futs):
            r = fu.result()
            f.write(json.dumps(r) + "\n"); f.flush()
            print(r["solver"], r["n"], r["seed"], r["eps"], r["status"], r.get("nodes", r.get("pairs")),
                  round(r["time"], 1), flush=True)


if __name__ == "__main__":
    main()
