"""Summarize the JSONL results into markdown tables (printed to stdout).

  python3 analyze.py > tables.md
"""
import collections, glob, json, math
import numpy as np

D = "data/"


def load(pattern):
    """Load JSONL files; SCIP runs repeated in two batches are counted once."""
    rows, seen = [], set()
    for fn in sorted(glob.glob(D + pattern)):
        for l in open(fn):
            r = json.loads(l)
            if "variant" in r:
                key = (r.get("amp"), r["variant"], r["n"], r["seed"], r["eps"], r["tl"])
                if key in seen:
                    continue
                seen.add(key)
            rows.append(r)
    return rows


def gmean(v):
    return float(math.exp(np.mean(np.log(np.maximum(v, 1)))))


def fit(ns, ys, kind):
    """Least squares on log y: kind 'exp' -> log y = a + b n; 'pow' -> log y = a + k log n."""
    x = np.array(ns, float) if kind == "exp" else np.log(np.array(ns, float))
    y = np.log(np.array(ys, float))
    A = np.vstack([np.ones_like(x), x]).T
    coef, res, *_ = np.linalg.lstsq(A, y, rcond=None)
    yhat = A @ coef
    r2 = 1 - ((y - yhat) ** 2).sum() / max(((y - y.mean()) ** 2).sum(), 1e-300)
    return coef, r2


def solved(r):
    return r["status"] in ("optimal", "gaplimit")


def scip_table(rows, title, seeds_expected):
    print(f"\n#### {title}\n")
    by = collections.defaultdict(dict)
    for r in rows:
        by[r["n"]][r["seed"]] = r
    print("| n | solved | nodes per seed | geo. mean nodes (solved) | median CPU s | max final gap (unsolved) |")
    print("|---|---|---|---|---|---|")
    fitpts = []
    for n in sorted(by):
        rr = [by[n][s] for s in sorted(by[n])]
        sol = [r for r in rr if solved(r)]
        nodes = " ".join(f"{r['nodes']}{'' if solved(r) else '+'}" for r in rr)
        gm = gmean([r["nodes"] for r in sol]) if sol else float("nan")
        uns = [r["absgap"] for r in rr if not solved(r)]
        print(f"| {n} | {len(sol)}/{len(rr)} | {nodes} | {gm:.0f} | {np.median([r['time'] for r in rr]):.1f} | "
              f"{max(uns):.2e} |" if uns else
              f"| {n} | {len(sol)}/{len(rr)} | {nodes} | {gm:.0f} | {np.median([r['time'] for r in rr]):.1f} | - |")
        if len(sol) == len(rr) == seeds_expected and n >= 4:
            fitpts.append((n, gm))
    return fitpts


def report_fit(fitpts, label):
    if len(fitpts) < 3:
        print(f"\n{label}: too few fully solved sizes for a fit")
        return
    ns, ys = zip(*fitpts)
    (a, b), r2e = fit(ns, ys, "exp")
    (a2, k), r2p = fit(ns, ys, "pow")
    print(f"\n{label}: fit on n = {min(ns)}..{max(ns)} (geometric means): "
          f"exponential nodes ~ {math.exp(a):.3g} * {math.exp(b):.3f}^n (factor {math.exp(2*b):.2f} per +2 variables, R^2 = {r2e:.4f}); "
          f"power law nodes ~ n^{k:.2f} (R^2 = {r2p:.4f}).")
    return (a, b), (a2, k)


def main():
    # ------------------------------------------------------------ SCIP probe3
    print("### SCIP, probe3 family (default settings, CPU-time limit 300 s)")
    fits = {}
    for amp in (0.3, 0.2):
        rows = [r for r in load(f"scip_default_amp{amp}.jsonl")]
        for eps in (1e-4, 1e-6):
            rr = [r for r in rows if r["eps"] == eps and r["variant"] == "default"]
            if not rr:
                continue
            pts = scip_table(rr, f"amp = {amp}, eps = {eps:g}", 5)
            fits[(amp, eps)] = report_fit(pts, f"amp {amp}, eps {eps:g}")
    # extended runs
    long_rows = load("scip_long_amp*.jsonl")
    if long_rows:
        print("\n#### Extended runs (CPU-time limit 1800 s, eps = 1e-4)\n")
        print("| amp | n | seed | status | nodes | CPU s | final gap | 300 s-fit prediction (nodes) |")
        print("|---|---|---|---|---|---|---|---|")
        for r in sorted(long_rows, key=lambda r: (r["amp"], r["n"], r["seed"])):
            f = fits.get((r["amp"], 1e-4))
            pred = f"{math.exp(f[0][0] + f[0][1] * r['n']):.0f} (exp) / {math.exp(f[1][0]) * r['n'] ** f[1][1]:.0f} (pow)" if f else "-"
            print(f"| {r['amp']} | {r['n']} | {r['seed']} | {r['status']} | {r['nodes']} | {r['time']:.0f} | {r['absgap']:.1e} | {pred} |")

    # ------------------------------------------------------------ variants
    rows = load("scip_variants_amp0.3.jsonl") + [r for r in load("scip_default_amp0.3.jsonl")
                                                 if r["eps"] == 1e-4 and r["seed"] < 3 and r["n"] <= 14]
    print("\n### SCIP robustness variants (probe3, amp 0.3, eps 1e-4, seeds 0-2, CPU limit 300 s)\n")
    variants = ["default", "single", "bestfirst", "obbt", "emph_opt", "combo", "warm"]
    ns = sorted({r["n"] for r in rows})
    by = {(r["variant"], r["n"], r["seed"]): r for r in rows}
    print("| variant | " + " | ".join(f"n={n}" for n in ns) + " | factor per +2 (fit) |")
    print("|---|" + "---|" * (len(ns) + 1))
    for v in variants:
        cells, pts = [], []
        for n in ns:
            rr = [by.get((v, n, s)) for s in range(3)]
            rr = [r for r in rr if r]
            if not rr:
                cells.append("-"); continue
            sol = [r for r in rr if solved(r)]
            if len(sol) == len(rr):
                gm = gmean([r["nodes"] for r in rr]); cells.append(f"{gm:.0f}")
                if n >= 4:
                    pts.append((n, gm))
            else:
                cells.append(f"{len(sol)}/{len(rr)} solved; gap<= {max(r['absgap'] for r in rr if not solved(r)):.1e}")
        fe = ""
        if len(pts) >= 3:
            (a, b), r2 = fit(*zip(*pts), "exp"); fe = f"{math.exp(2*b):.2f} (R^2 {r2:.3f}, n={pts[0][0]}..{pts[-1][0]})"
        print(f"| {v} | " + " | ".join(cells) + f" | {fe} |")

    # determinism check: solved node counts, wall-clock runs vs CPU-clock runs
    wall = load("wallclock/*.jsonl")
    cpu = {(r["variant"], r["n"], r["seed"], r["eps"]): r for r in load("scip_default_amp0.3.jsonl") + load("scip_variants_amp0.3.jsonl")}
    same = diff = 0
    for r in wall:
        k = (r["variant"], r["n"], r["seed"], r["eps"])
        if k in cpu and solved(r) and solved(cpu[k]):
            if r["nodes"] == cpu[k]["nodes"]:
                same += 1
            else:
                diff += 1
    print(f"\nDeterminism check: {same} solved runs repeated with identical node counts, {diff} differ "
          f"(first batch with wall-clock limits vs. second batch with CPU-time limits).")

    # ------------------------------------------------------------ verification
    ver = load("verify.jsonl")
    print("\n### Instance verification (5 seeds per row)\n")
    print("| amp | n | certified unique+interior | multistart: instances with >1 local min | min lambda_min(H) at x* | lambda_min(H) over box | max abs x*_i |")
    print("|---|---|---|---|---|---|---|")
    vb = collections.defaultdict(list)
    for r in ver:
        vb[(r["amp"], r["n"])].append(r)
    for k in sorted(vb):
        rr = vb[k]
        print(f"| {k[0]} | {k[1]} | {sum(r['cert_certified'] for r in rr)}/{len(rr)} | "
              f"{sum(r['n_distinct_local_min'] > 1 for r in rr)} | {min(r['lmin_hess_at_min'] for r in rr):.3f} | "
              f"{rr[0]['lmin_hess_over_box']:.3f} | {max(r['max_abs_xstar'] for r in rr):.3f} |")
    bad = [r for r in ver if r["cert_UB_minus_multistart"] < -1e-9]
    print(f"\nInstances where the certificate run found a better point than 250-start multistart: {len(bad)}")
    rc = load("recheck_n1000_amp0.3.jsonl")
    if rc:
        print("\nRecheck of amp 0.3, n = 1000 at eps-optimal points (prototype, eps 1e-6; after review):\n")
        print("| seed | status | UB | multistart worse by | lambda_min(H) at x | max abs x_i | coordinates at bounds |")
        print("|---|---|---|---|---|---|---|")
        for r in rc:
            print(f"| {r['seed']} | {r['status']} | {r['UB']:.6f} | {r['multistart_minus_UB']:.2e} | {r['lmin_hess_at_x']:.3f} | "
                  f"{r['max_abs_x']:.3f} | {r['coords_at_bound']} |")
    print(f"\nNon-certified runs by status: {dict(collections.Counter(r['cert_status'] for r in ver if not r['cert_certified']))}; "
          f"smallest certified lambda_min(M): amp 0.2 {min(r['cert_lmin'] for r in ver if r['amp'] == 0.2 and r['cert_certified']):.4f}, "
          f"amp 0.3 {min(r['cert_lmin'] for r in ver if r['amp'] == 0.3 and r['cert_certified']):.4f}")

    # ------------------------------------------------------------ prototype
    print("\n### Prototype (chain DP B&B)\n")
    for fn, label in (("proto_amp0.2.jsonl", "amp 0.2, mode quad"), ("proto_amp0.3.jsonl", "amp 0.3 (probe3), mode quad"),
                      ("proto_ablation_amp0.2.jsonl", "amp 0.2, ablations")):
        rows = load(fn)
        by = collections.defaultdict(list)
        for r in rows:
            by[(r["mode"], r["eps"], r["n"])].append(r)
        print(f"\n#### {label}\n")
        print("| mode | eps | n | solved | median pair bounds | max pair bounds | median s | max cells/var | median iters |")
        print("|---|---|---|---|---|---|---|---|---|")
        fitd = collections.defaultdict(list)
        for k in sorted(by):
            rr = by[k]
            ok = [r for r in rr if r["status"] == "optimal"]
            print(f"| {k[0]} | {k[1]:g} | {k[2]} | {len(ok)}/{len(rr)} | {np.median([r['pairs'] for r in rr]):.0f} | "
                  f"{max(r['pairs'] for r in rr)} | {np.median([r['time'] for r in rr]):.2f} | "
                  f"{max(r['max_cells_per_var'] or 0 for r in rr)} | {np.median([r['iters'] for r in rr]):.0f} |")
            if len(ok) == len(rr) and k[2] >= 16:
                fitd[(k[0], k[1])].append((k[2], np.median([r["pairs"] for r in rr])))
        for key, pts in fitd.items():
            if len(pts) >= 3:
                (a, kk), r2 = fit(*zip(*pts), "pow")
                print(f"\nPower-law fit {label} {key}: median pairs ~ n^{kk:.2f} for n = {pts[0][0]}..{pts[-1][0]} (R^2 {r2:.3f}); "
                      f"pairs per variable at the largest n: {pts[-1][1] / pts[-1][0]:.0f}")

    # ------------------------------------------------------------ compact prototype tables
    print("\n### Compact prototype tables (mode quad; seeds 0-4)\n")
    for fn, label in (("proto_amp0.2.jsonl", "amp 0.2"), ("proto_amp0.3.jsonl", "amp 0.3 (probe3)")):
        rows = [r for r in load(fn) if r["mode"] == "quad"]
        print(f"\n#### {label}\n")
        print("| n | eps 1e-4: solved | median pair bounds | max pair bounds | median s | eps 1e-6: solved | median pair bounds | max pair bounds | median s | max cells per variable |")
        print("|---|---|---|---|---|---|---|---|---|---|")
        for n in sorted({r["n"] for r in rows}):
            cols = []
            for eps in (1e-4, 1e-6):
                rr = [r for r in rows if r["n"] == n and r["eps"] == eps]
                cols.append(f"{sum(r['status'] == 'optimal' for r in rr)}/{len(rr)} | {np.median([r['pairs'] for r in rr]):.0f} | "
                            f"{max(r['pairs'] for r in rr)} | {np.median([r['time'] for r in rr]):.2f}")
            mk = max(r["max_cells_per_var"] or 0 for r in rows if r["n"] == n)
            print(f"| {n} | " + " | ".join(cols) + f" | {mk} |")

    # ------------------------------------------------------------ compact ablation
    print("\n### Compact ablation (amp 0.2; median pair bounds over 5 seeds, solved count in parentheses)\n")
    rows = [r for r in load("proto_ablation_amp0.2.jsonl") + load("proto_amp0.2.jsonl")]
    print("| n | plain 1e-4 | affine 1e-4 | quad 1e-4 | plain 1e-6 | affine 1e-6 | quad 1e-6 |")
    print("|---|---|---|---|---|---|---|")
    for n in (2, 4, 6, 8, 10, 16, 20, 32, 64, 128, 256):
        cols = []
        for eps in (1e-4, 1e-6):
            for mode in ("plain", "affine", "quad"):
                rr = [r for r in rows if r["n"] == n and r["eps"] == eps and r["mode"] == mode]
                cols.append(f"{np.median([r['pairs'] for r in rr]):.3g} ({sum(r['status'] == 'optimal' for r in rr)})" if rr else "-")
        print(f"| {n} | " + " | ".join(cols) + " |")

    # ------------------------------------------------------------ side by side
    print("\n### Side-by-side comparison (same instances, same absolute tolerance)\n")
    proto_all = load("proto_amp*.jsonl") + load("proto_loose_amp*.jsonl")
    scip_all = load("scip_default_amp*.jsonl") + load("scip_loose*.jsonl")
    for amp in (0.2, 0.3):
        for eps in (1e-2, 1e-3, 1e-4, 1e-6):
            ss = [r for r in scip_all if r["amp"] == amp and r["eps"] == eps]
            pp = [r for r in proto_all if r["amp"] == amp and r["eps"] == eps and r["mode"] == "quad"]
            if not ss or not pp:
                continue
            print(f"\n#### amp {amp}, eps {eps:g}\n")
            print("| n | SCIP solved | SCIP nodes (geo. mean; + = lower bound) | SCIP median CPU s | SCIP median final gap | prototype solved | prototype median pair bounds | prototype median s |")
            print("|---|---|---|---|---|---|---|---|")
            ns = sorted({r["n"] for r in ss} | {r["n"] for r in pp})
            spts = []
            for n in ns:
                sr = [r for r in ss if r["n"] == n]; pr = [r for r in pp if r["n"] == n]
                if sr:
                    sol = [r for r in sr if solved(r)]
                    gm = gmean([r["nodes"] for r in sr])
                    scol = (f"{len(sol)}/{len(sr)} | {gm:.0f}{'' if len(sol) == len(sr) else '+'} | "
                            f"{np.median([r['time'] for r in sr]):.1f} | {np.median([r['absgap'] for r in sr]):.1e}")
                    if len(sol) == len(sr) and n >= 4:
                        spts.append((n, gm))
                else:
                    scol = "- | - | - | -"
                if pr:
                    pcol = (f"{sum(r['status'] == 'optimal' for r in pr)}/{len(pr)} | {np.median([r['pairs'] for r in pr]):.0f} | "
                            f"{np.median([r['time'] for r in pr]):.2f}")
                else:
                    pcol = "- | - | -"
                print(f"| {n} | {scol} | {pcol} |")
            report_fit(spts, f"SCIP amp {amp}, eps {eps:g}")

    # ------------------------------------------------------------ local exponents
    print("\n### Local power-law exponents of SCIP node counts (after review)\n")
    print("ln(ratio) / ln((n+2)/n) for consecutive fully solved sizes (geometric means over 5 seeds).")
    print("A fixed-degree polynomial gives constant values; an exact 5x-per-2 exponential gives ln5/ln((n+2)/n).\n")
    print("| family, eps | step n -> n+2 | ratio | local exponent | exact 5x-per-2 exponential |")
    print("|---|---|---|---|---|")
    for amp, eps, pat in ((0.2, 1e-4, "scip_default_amp0.2.jsonl"), (0.2, 1e-2, "scip_loose*.jsonl"),
                          (0.3, 1e-4, "scip_default_amp0.3.jsonl")):
        rr = [r for r in load(pat) if r["eps"] == eps and r["variant"] == "default"]
        gm = {}
        for n in sorted({r["n"] for r in rr}):
            x = [r for r in rr if r["n"] == n]
            if n >= 4 and len(x) == 5 and all(solved(r) for r in x):
                gm[n] = gmean([r["nodes"] for r in x])
        for n in sorted(gm):
            if n + 2 in gm:
                ratio = gm[n + 2] / gm[n]
                print(f"| amp {amp}, eps {eps:g} | {n} -> {n + 2} | {ratio:.2f} | {math.log(ratio) / math.log((n + 2) / n):.2f} | "
                      f"{math.log(5) / math.log((n + 2) / n):.2f} |")

    # ------------------------------------------------------------ consistency
    print("\n### Consistency of optimal values (SCIP vs prototype)\n")
    proto = {}
    for r in load("proto_amp*.jsonl"):
        if r["mode"] == "quad":
            proto[(r["amp"], r["n"], r["seed"], r["eps"])] = r
    scip = load("scip_default_amp*.jsonl") + load("scip_long_amp*.jsonl")
    both = [(s, proto[(s["amp"], s["n"], s["seed"], s["eps"])]) for s in scip
            if (s["amp"], s["n"], s["seed"], s["eps"]) in proto and proto[(s["amp"], s["n"], s["seed"], s["eps"])]["status"] == "optimal"]
    sol = [(s, p) for s, p in both if solved(s)]
    uns = [(s, p) for s, p in both if not solved(s)]
    if sol:
        d = np.array([s["primal"] - p["UB"] for s, p in sol])
        dd = np.array([s["dual"] - p["UB"] for s, p in sol])
        dl = np.array([p["LB"] - s["primal"] for s, p in sol])
        print(f"- SCIP solved and prototype solved: {len(sol)} runs. SCIP primal - prototype UB: min {d.min():.2e}, max {d.max():.2e}; "
              f"max(SCIP dual - prototype UB) = {dd.max():.2e}; max(prototype LB - SCIP primal) = {dl.max():.2e}.")
        for eps in (1e-4, 1e-6):
            de = np.array([s["primal"] - p["UB"] for s, p in sol if s["eps"] == eps])
            if len(de):
                print(f"  - eps {eps:g}: |SCIP primal - prototype UB| <= {abs(de).max():.2e} over {len(de)} runs")
    if uns:
        d = np.array([s["primal"] - p["UB"] for s, p in uns])
        dd = np.array([s["dual"] - p["UB"] for s, p in uns])
        print(f"- SCIP hit the time limit: {len(uns)} runs. SCIP primal - prototype UB: min {d.min():.2e}, median {np.median(d):.2e}, max {d.max():.2e}; "
              f"max(SCIP dual - prototype UB) = {dd.max():.2e} (must be <= 0 up to tolerances).")

    # ------------------------------------------------------------ lot-sizing
    ls = load("lotsizing_scip.jsonl")
    lp = load("lotsizing_proto.jsonl")
    if ls:
        print("\n### Lot-sizing chain\n")
        pts = scip_table(ls, "SCIP, default settings, eps 1e-4, CPU limit 300 s", 5)
        report_fit(pts, "lot-sizing SCIP")
    if lp:
        by = collections.defaultdict(list)
        for r in lp:
            by[(r["eps"], r["n"])].append(r)
        print("\n#### Prototype (mode split)\n")
        print("| eps | T | solved | median pair bounds | max pair bounds | median s | max cells/var | idle periods (median) |")
        print("|---|---|---|---|---|---|---|---|")
        fitd = collections.defaultdict(list)
        for k in sorted(by):
            rr = by[k]; ok = [r for r in rr if r["status"] == "optimal"]
            print(f"| {k[0]:g} | {k[1]} | {len(ok)}/{len(rr)} | {np.median([r['pairs'] for r in rr]):.0f} | {max(r['pairs'] for r in rr)} | "
                  f"{np.median([r['time'] for r in rr]):.2f} | {max(r['max_cells_per_var'] or 0 for r in rr)} | {np.median([r['n_idle_periods'] for r in rr]):.0f} |")
            if len(ok) == len(rr) and k[1] >= 8:
                fitd[k[0]].append((k[1], np.median([r["pairs"] for r in rr])))
        for e, pts in fitd.items():
            if len(pts) >= 3:
                (a, kk), r2 = fit(*zip(*pts), "pow")
                print(f"\nPower-law fit lot-sizing prototype eps {e:g}: median pairs ~ T^{kk:.2f} for T = {pts[0][0]}..{pts[-1][0]} (R^2 {r2:.3f})")
                p2 = [q for q in pts if q[0] != 9]
                (a, kk), r2 = fit(*zip(*p2), "pow")
                print(f"Same without the T = 9 outlier: T^{kk:.2f} (R^2 {r2:.3f})")
        pl = {(r["n"], r["seed"], r["eps"]): r for r in lp}
        both = [(s, pl[(s["n"], s["seed"], s["eps"])]) for s in ls if (s["n"], s["seed"], s["eps"]) in pl]
        sol = [(s, p) for s, p in both if solved(s) and p["status"] == "optimal"]
        uns = [(s, p) for s, p in both if not solved(s) and p["status"] == "optimal"]
        if sol:
            d = np.array([s["primal"] - p["UB"] for s, p in sol])
            print(f"\n- Both solved: {len(sol)} runs; SCIP primal - prototype UB in [{d.min():.2e}, {d.max():.2e}]; "
                  f"max(SCIP dual - prototype UB) = {max(s['dual'] - p['UB'] for s, p in sol):.2e}")
        if uns:
            d = np.array([s["primal"] - p["UB"] for s, p in uns])
            print(f"- SCIP time limit: {len(uns)} runs; SCIP primal - prototype UB in [{d.min():.2e}, {d.max():.2e}]; "
                  f"max(SCIP dual - prototype UB) = {max(s['dual'] - p['UB'] for s, p in uns):.2e}")


if __name__ == "__main__":
    main()
