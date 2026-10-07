"""Refinement-rule ablation (theta) for the prototype; prints one line per run."""
import instances as I, chain_bb as CB
print("amp n theta status gap iters pairs max_cells_per_var seconds")
for amp in (0.2, 0.3):
    for n in (1024, 8192):
        for th in (1.0, 0.5, 0.2, 0.05, 0.0):
            pr = I.Probe3Chain(I.coeffs(n, 0, amp))
            r = CB.chain_bb(pr, 1e-6, mode="quad", unary_sub=16, theta=th, time_limit=300, max_iter=200,
                            max_pairs_iter=40_000_000)
            print(amp, n, th, r["status"], f"{r['UB'] - r['LB']:.2e}", r["iters"], r["pairs"],
                  max(h["maxK"] for h in r["hist"]), round(r["time"], 2), flush=True)
