"""Aggregate tiny_kappa.py outputs (tiny_n*.jsonl)."""
import json, glob, collections
import numpy as np
rows = []
for fn in sorted(glob.glob("tiny_n*.jsonl")):
    rows += [json.loads(l) for l in open(fn)]
print("instances:", len(rows))
print("chain omega_mid <= omega_seg <= chi_seg <= kappa <= L_var <= L_static violated:",
      sum(not r["chain_ok"] for r in rows))
print("kappa exact:", sum(r["kappa_exact"] for r in rows), " borderline admissibility decisions:",
      sum(r["border"] for r in rows))
e0 = [r for r in rows if r["mid_edges"] == 0]
print("edgeless midpoint graph:", len(e0), " of which kappa >= 2:",
      sum((r["kappa"] or r["chi_seg"]) >= 2 for r in e0),
      " kappa >= 3:", sum((r["kappa"] or 0) >= 3 for r in e0))
gap = [r for r in rows if r["kappa_exact"] and r["kappa"] > r["chi_seg"]]
print("exact kappa > chi(G^seg) (class number above every pairwise bound):", len(gap))
for r in gap[:6]:
    print("   ", {k: r[k] for k in ("N", "beta", "rho", "seed", "omega_mid", "chi_seg", "kappa", "L_var", "L_static")})
print("kappa < L_var:", sum(r["kappa_exact"] and r["kappa"] < r["L_var"] for r in rows),
      "  L_var < L_static:", sum(r["L_var"] < r["L_static"] for r in rows))
g = collections.defaultdict(list)
for r in rows:
    g[(r["N"], r["beta"], r["rho"])].append(r)
print()
print("| N | beta | rho | inst | x* opt | mid edges=0 | omega_mid | chi_seg | kappa (exact/inst) | L_var | L_static |")
print("|---:|---:|---:|---:|---:|---:|---|---|---|---|---|")
def rng_(v):
    v = [x for x in v if x is not None]
    return "%.1f [%d, %d]" % (np.mean(v), min(v), max(v)) if v else "-"
for k in sorted(g):
    L = g[k]
    print("| %d | %g | %g | %d | %d | %d | %s | %s | %s (%d/%d) | %s | %s |" % (
        k[0], k[1], k[2], len(L), sum(r["xstar_opt"] for r in L), sum(r["mid_edges"] == 0 for r in L),
        rng_([r["omega_mid"] for r in L]), rng_([r["chi_seg"] for r in L]),
        rng_([r["kappa"] for r in L]), sum(r["kappa_exact"] for r in L), len(L),
        rng_([r["L_var"] for r in L]), rng_([r["L_static"] for r in L])))
