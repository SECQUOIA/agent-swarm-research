"""Run the ratio search over hypergraph families; write results.csv and results.md.

Usage:  python run_experiments.py [--quick] [--workers N] [--out results]
"""
from __future__ import annotations

import argparse
import csv
import itertools
import multiprocessing as mp
import sys
import time

import numpy as np

import families as F
from search import exact_max, multistart, optimize_coefs


def job(spec):
    family, label, builder, kwargs, mode = spec
    f = builder(**kwargs)
    rng = np.random.default_rng(abs(hash(label)) % (2 ** 32))
    t0 = time.time()
    row = {"family": family, "instance": label, "n": f.n, "terms": len(f.terms),
           "degrees": "/".join(map(str, sorted(set(len(t) for _, t in f.terms))))}
    if mode == "coef":
        r, x, g = optimize_coefs(f, rng, n_rounds=2, n_starts=8)
        row.update(method="coef-opt", ratio=r, x=_fmt(x), coefs=_fmt([a for a, _ in g.terms]))
    else:
        ex = exact_max(f, budget=int(mode)) if mode != "heur" else None
        if ex is not None:
            r, x, nc = ex
            row.update(method=f"exact({nc} cand.)", ratio=r, x=_fmt(x), coefs="")
        else:
            r, x = multistart(f, rng, n_starts=24)
            row.update(method="multistart", ratio=r, x=_fmt(x), coefs="")
    row["time_s"] = round(time.time() - t0, 1)
    return row


def _fmt(x):
    return " ".join(f"{v:.4g}" for v in x)


def specs(quick):
    S = []
    E = "20000000"  # exact-enumeration budget (number of linear systems); falls back to heuristic
    # (0) bilinear check of Theorem 8 on complete graphs
    for n in range(3, 11):
        S.append(("bilinear K_n (check)", f"K{n}", F.complete, dict(n=n, k=2), E if n <= 7 else "heur"))
    # (a) 3-uniform families
    for n in range(4, 13 if not quick else 9):
        S.append(("complete 3-uniform K_n^(3)", f"K{n}^(3)", F.complete, dict(n=n, k=3), E if n <= 7 else "heur"))
    for n in range(4, 12 if not quick else 8):
        S.append(("cone/star {0,i,j}", f"cone{n}", F.cone, dict(n=n, k=3, apex=1), E if n <= 7 else "heur"))
    for m in range(2, 6):
        S.append(("sunflower core1 petals2", f"sunflower1x{m}", F.sunflower, dict(n_petals=m, core_size=1, petal_size=2), E if 2 * m + 1 <= 7 else "heur"))
    for m in range(2, 8):
        S.append(("sunflower core2 petals1", f"sunflower2x{m}", F.sunflower, dict(n_petals=m, core_size=2, petal_size=1), E if m + 2 <= 7 else "heur"))
    S.append(("Fano plane (STS(7))", "fano", F.fano, {}, E))
    S.append(("complete 4-uniform", "K6^(4)", F.complete, dict(n=6, k=4), E))
    S.append(("complete 4-uniform", "K7^(4)", F.complete, dict(n=7, k=4), E))
    S.append(("complete 4-uniform", "K8^(4)", F.complete, dict(n=8, k=4), "heur"))
    S.append(("complete 4-uniform", "K10^(4)", F.complete, dict(n=10, k=4), "heur"))
    for n, m, seed in [(6, 6, s) for s in range(4)] + [(6, 10, s) for s in range(4)] + [(7, 8, s) for s in range(4)] + [(7, 15, s) for s in range(4)] + [(8, 12, s) for s in range(3)] + [(8, 25, s) for s in range(3)] + ([(9, 20, s) for s in range(2)] + [(10, 30, s) for s in range(2)] if not quick else []):
        S.append(("random 3-uniform", f"r3_n{n}_m{m}_s{seed}", F.random_uniform, dict(n=n, k=3, m=m, seed=seed), E if n <= 7 else "heur"))
    for n, m, seed in [(6, 8, s) for s in range(3)] + [(7, 12, s) for s in range(3)]:
        S.append(("random 3-uniform, log-uniform coefs", f"r3lu_n{n}_m{m}_s{seed}", F.random_uniform, dict(n=n, k=3, m=m, seed=seed, coef_dist="loguniform"), E if n <= 7 else "heur"))
    # (b) mixed degrees
    for n in range(4, 9 if not quick else 7):
        S.append(("complete edges+triangles", f"K{n}^(2,3)", F.complete_mixed, dict(n=n, degrees=(2, 3)), E if n <= 7 else "heur"))
    S.append(("paper example (5 vars)", "paper5", F.paper_example, {}, E))
    for n, m2, m3, seed in [(6, 5, 5, s) for s in range(4)] + [(7, 8, 8, s) for s in range(4)] + [(8, 10, 12, s) for s in range(3)]:
        S.append(("random mixed 2+3", f"rm_n{n}_e{m2}_t{m3}_s{seed}", F.random_mixed, dict(n=n, m2=m2, m3=m3, seed=seed), E if n <= 7 else "heur"))
    for n, m, seed in [(6, 8, s) for s in range(3)] + [(7, 12, s) for s in range(3)] + [(8, 16, s) for s in range(3)]:
        S.append(("random degrees 2-4", f"rd_n{n}_m{m}_s{seed}", F.random_degrees, dict(n=n, m=m, seed=seed), E if n <= 7 else "heur"))
    # (c) chains / cycles
    for n in range(4, 13 if not quick else 9):
        S.append(("tight path (3-windows)", f"tpath{n}", F.tight_path, dict(n=n, k=3), E if n <= 7 else "heur"))
        S.append(("tight cycle (3-windows)", f"tcycle{n}", F.tight_cycle, dict(n=n, k=3), E if n <= 7 else "heur"))
    for m in range(2, 6):
        S.append(("loose path (share 1 vertex)", f"lpath{m}", F.loose_path, dict(n_edges=m, k=3), E if 2 * m + 1 <= 7 else "heur"))
        S.append(("loose cycle (share 1 vertex)", f"lcycle{m}", F.loose_cycle, dict(n_edges=m, k=3), E if 2 * m <= 7 else "heur"))
    # (d) coefficient optimisation
    for label, builder, kw in [("fano", F.fano, {}), ("K5^(3)", F.complete, dict(n=5, k=3)), ("K6^(3)", F.complete, dict(n=6, k=3)),
                               ("K5^(2,3)", F.complete_mixed, dict(n=5, degrees=(2, 3))), ("K6^(2,3)", F.complete_mixed, dict(n=6, degrees=(2, 3))),
                               ("cone6", F.cone, dict(n=6, k=3, apex=1)), ("tcycle6", F.tight_cycle, dict(n=6, k=3)), ("tcycle7", F.tight_cycle, dict(n=7, k=3)),
                               ("paper5", F.paper_example, {}), ("r3_n7_m15_s0", F.random_uniform, dict(n=7, k=3, m=15, seed=0)),
                               ("rd_n7_m12_s0", F.random_degrees, dict(n=7, m=12, seed=0)), ("K6", F.complete, dict(n=6, k=2))]:
        S.append(("coefficient optimisation", label + " (coef)", builder, kw, "coef"))
    return S


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--workers", type=int, default=max(1, mp.cpu_count() // 2))
    ap.add_argument("--out", default="results")
    args = ap.parse_args()
    S = specs(args.quick)
    print(f"{len(S)} instances, {args.workers} workers", flush=True)
    rows = []
    with mp.Pool(args.workers) as pool:
        for row in pool.imap_unordered(job, S):
            rows.append(row)
            print(f"[{len(rows)}/{len(S)}] {row['instance']:>22s} n={row['n']:2d} |T|={row['terms']:3d} ratio={row['ratio']:.6f} ({row['method']}, {row['time_s']}s) x={row['x']}", flush=True)
    order = {s[1] if s[4] != "coef" else s[1]: i for i, s in enumerate(S)}
    rows.sort(key=lambda r: order.get(r["instance"], 0))
    keys = ["family", "instance", "n", "terms", "degrees", "method", "ratio", "x", "coefs", "time_s"]
    with open(args.out + ".csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=keys)
        w.writeheader()
        w.writerows(rows)
    with open(args.out + ".md", "w") as fh:
        fh.write("| family | instance | n | terms | degrees | method | max ratio | x (maximizer) |\n|---|---|---|---|---|---|---|---|\n")
        for r in rows:
            fh.write(f"| {r['family']} | {r['instance']} | {r['n']} | {r['terms']} | {r['degrees']} | {r['method']} | {r['ratio']:.6f} | {r['x']} |\n")
    print("wrote", args.out + ".csv/.md")


if __name__ == "__main__":
    main()
