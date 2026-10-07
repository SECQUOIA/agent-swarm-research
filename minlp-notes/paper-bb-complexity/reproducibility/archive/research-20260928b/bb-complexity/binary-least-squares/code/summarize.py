"""Print the tables of Section 7 (markdown) from the result files in data/.
Usage (from data/): python3 ../code/summarize.py
"""
import json, os, collections
import numpy as np


def load(fn):
    if not os.path.exists(fn):
        return []
    return [json.loads(l) for l in open(fn) if l.strip()]


def t_root():
    rows = load("root.jsonl")
    b = [r for r in rows if r["part"] == "b"]
    print("\nTable 7.1a (root exactness, tiny N; 20000 trials per cell)\n")
    print("| beta | N | rho | P(x* box minimizer) | 2^-N | P(vertex minimizer) | bound of Thm 1.2 |")
    print("|---:|---:|---:|---:|---:|---:|---:|")
    for r in b:
        print("| %d | %d | %g | %.4f | %.4f | %.4f | %.4f |" % (r["beta"], r["N"], r["rho"], r["p_xstar"], r["two_pow"], r["p_vertex"], r["bound"]))
    a = [r for r in rows if r["part"] == "a"]
    g = collections.defaultdict(list)
    for r in a:
        g[(r["beta"], r["N"])].append(r)
    print("\nTable 7.1b (root gain; all rho values pooled: 2 log N, 4 log N, 8 log N, N/4)\n")
    print("| beta | N | instances | mean G/N | var(G_inf)/N | mean active/N | var(active)/N | G = G_inf | median max u°(1) |")
    print("|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for k in sorted(g):
        L = g[k]; N = k[1]
        G = np.array([r["G"] for r in L]); Gi = np.array([r["Ginf"] for r in L])
        act = np.array([r["active"] for r in L])
        eq = sum(abs(r["G"] - r["Ginf"]) < 1e-8 * r["W"] for r in L)
        # G_inf does not depend on rho for a given seed: use one rho for the variance
        rho0 = L[0]["rho"]
        Gi0 = np.array([r["Ginf"] for r in L if r["rho"] == rho0])
        a0 = np.array([r["active"] for r in L if r["rho"] == rho0])
        um = np.median([r["umax_nnls"] * np.sqrt(r["rho"]) for r in L])
        print("| %d | %d | %d | %.3f | %.2f | %.3f | %.3f | %d/%d | %.2f |" % (k[0], N, len(Gi0), G.mean() / N, Gi0.var() / N, a0.mean() / N, a0.var() / N, eq, len(L), um))


def t_c1():
    rows = load("c1.jsonl")
    g = collections.defaultdict(list)
    for r in rows:
        g[(r["beta"], r["N"], r["theta"])].append(r)
    print("\nTable 7.2 (condition C1 at x*; theta = rho/N)\n")
    print("| beta | N | theta | theta_c | runs | C1 certified | C1 refuted | predictor | mean min_i (r_i - W)/N | mean r_i/norm(v_i)^2 | law 1-(N-1)/(2M) | nodes box-inactive |")
    print("|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for k in sorted(g):
        L = g[k]; b = k[0]
        print("| %d | %d | %.3f | %.3f | %d | %d | %d | %d | %.3f | %.3f | %.3f | %.2f |" % (
            b, k[1], k[2], 1 / (4 * (2 * b - 1)), len(L), sum(r["c1"] for r in L), sum(r["refuted"] for r in L),
            sum(r["pred_c1"] for r in L), np.mean([r["min_margin"] for r in L]), np.mean([r["mean_ratio"] for r in L]),
            L[0]["law_ratio"], np.mean([r["frac_node_inactive"] for r in L])))


def t_trees():
    rows = load("trees_b1.jsonl") + load("trees_b1_256.jsonl") + load("trees_b2.jsonl")
    g = collections.defaultdict(list)
    for r in rows:
        g[(r["beta"], r["N"], r["tag"], r["rule"])].append(r)
    print("\nTable 7.3 (B&B nodes, incumbent x*, best-first; geometric mean [min, max])\n")
    print("| beta | N | rho | rho/log N | N/rho | x* optimal | maxfrac nodes | static nodes | (N/(4(2b-1)rho)) log rho |")
    print("|---:|---:|---:|---:|---:|---:|---|---|---:|")
    keys = sorted({(k[0], k[1], k[2]) for k in g}, key=lambda k: (k[0], k[1], -g[(k[0], k[1], k[2], "maxfrac")][0]["rho"] if (k[0], k[1], k[2], "maxfrac") in g else 0))
    for k in keys:
        cells = []
        rho = None; xo = None
        for rule in ("maxfrac", "static"):
            L = g.get(k + (rule,), [])
            if not L:
                cells.append("-"); continue
            rho = L[0]["rho"]
            nd = [r["nodes"] for r in L]
            done = sum(r["done"] for r in L)
            seeds_done = {r["seed"]: r["xstar_opt"] for rr in ("maxfrac", "static")
                          for r in g.get(k + (rr,), []) if r["done"]}
            xo = "%d/%d" % (sum(seeds_done.values()), len(seeds_done))
            cap = "" if done == len(L) else " (%d capped)" % (len(L) - done)
            cells.append("%.0f [%d, %d]%s" % (np.exp(np.mean(np.log(nd))), min(nd), max(nd), cap))
        b, N = k[0], k[1]
        pred = N / (4 * (2 * b - 1) * rho) * np.log(rho)
        print("| %g | %d | %.1f | %.1f | %.1f | %s | %s | %s | %.2f |" % (b, N, rho, rho / np.log(N), N / rho, xo, cells[0], cells[1], pred))


def t_thr():
    rows = load("thresholds.jsonl")
    print("\nTable 7.4a (single-coordinate law: P(some one-bit flip beats x*) / P(some half move beats x*); c = rho beta/log N)\n")
    cs = sorted({r["c"] for r in rows if r["part"] == "law"})
    print("| beta | N | " + " | ".join("c=%g" % c for c in cs) + " |")
    print("|---:|---:|" + "---|" * len(cs))
    for beta in (1, 2):
        for N in (100, 1000, 10000, 100000):
            L = {r["c"]: r for r in rows if r["part"] == "law" and r["beta"] == beta and r["N"] == N}
            if not L:
                continue
            print("| %d | %d | " % (beta, N) + " | ".join("%.2f/%.2f" % (L[c]["p_ml_fail"], L[c]["p_half_conflict"]) for c in cs) + " |")
    print("\nTable 7.4b (real instances, 20 seeds: instances with a single / pair half-move conflict)\n")
    print("| beta | N | c | single | pair | pair without single |")
    print("|---:|---:|---:|---:|---:|---:|")
    for r in rows:
        if r["part"] == "pairs":
            print("| %d | %d | %g | %d | %d | %d |" % (r["beta"], r["N"], r["c"], r["single"], r["pair"], r["pair_without_single"]))


def t_sdp():
    rows = load("sdp.jsonl")
    a = [r for r in rows if r["part"] == "a"]
    g = collections.defaultdict(list)
    for r in a:
        g[(r["beta"], r["N"])].append(r)
    print("\nTable 7.5a (SDP exactness threshold per instance: c* = rho*/log N)\n")
    print("| beta | N | instances | median c* | [min, max] | median log(rho*)/log N | median one-bit (ML) threshold / log N | heuristic 2b/(b-1)^2 | proved sufficient 2b/(sqrt b - 1)^4 |")
    print("|---:|---:|---:|---:|---|---:|---:|---:|---:|")
    for k in sorted(g):
        L = g[k]; b, N = k
        cs = np.array([r["c_star"] for r in L])
        rs = np.array([r["rho_star"] for r in L])
        h = "%.2f" % (2 * b / (b - 1) ** 2) if b > 1 else "-"
        s = "%.1f" % (2 * b / (np.sqrt(b) - 1) ** 4) if b > 1 else "-"
        print("| %g | %d | %d | %.3g | [%.3g, %.3g] | %.2f | %.2f | %s | %s |" % (b, N, len(L), np.median(cs), cs.min(), cs.max(), np.median(np.log(rs) / np.log(N)), np.median([r["c_diag"] for r in L]), h, s))
    bb = [r for r in rows if r["part"] == "b"]
    if bb:
        g = collections.defaultdict(list)
        for r in bb:
            g[(r["N"], r["tag"])].append(r)
        print("\nTable 7.5b (square systems: relative root gaps (OPT - bound)/OPT, 6 seeds)\n")
        print("| N | rho | box gap, median | SDP gap, median [max] | SDP exact | x* optimal |")
        print("|---:|---:|---:|---|---:|---:|")
        for k in sorted(g, key=lambda k: (k[0], g[k][0]["rho"])):
            L = g[k]
            sg = [max(r["sdp_gap_rel"], 0.0) for r in L]
            print("| %d | %.1f | %.3f | %.4f [%.4f] | %d/%d | %d/%d |" % (k[0], L[0]["rho"], np.median([r["box_gap_rel"] for r in L]), np.median(sg), max(sg), sum(r["sdp_gap_rel"] < 1e-6 for r in L), len(L), sum(r["xstar_opt"] for r in L), len(L)))


def t_knap():
    rows = load("knapsack.jsonl")
    if not rows:
        return
    print("\nTable 7.3c (knapsack extrapolation of the exact-law predictor; mean log(#nodes) over samples)\n")
    tags = ["c4", "c8", "r8", "r32", "r128"]
    print("| beta | N | " + " | ".join("%s: log tree / (N/(4(2b-1)rho)) log rho" % t for t in tags) + " |")
    print("|---:|---:|" + "---|" * len(tags))
    g = {(r["beta"], r["N"], r["tag"]): r for r in rows}
    for beta in (1.0, 2.0):
        for N in sorted({r["N"] for r in rows}):
            cells = []
            for t in tags:
                r = g.get((beta, N, t))
                if r is None or not r["log_tree"]:
                    cells.append("-")
                else:
                    lt = float(np.mean(r["log_tree"]))
                    cells.append("%.1f / %.1f" % (lt, r["pred_const"]))
            print("| %g | %d | " % (beta, N) + " | ".join(cells) + " |")


if __name__ == "__main__":
    t_root(); t_c1(); t_trees(); t_knap(); t_thr(); t_sdp()
