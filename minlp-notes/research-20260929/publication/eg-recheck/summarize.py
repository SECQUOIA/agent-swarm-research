"""Collect the results of the full re-certification of eg_disc2_s run G.

Per part: chunk files complete (every leaf index exactly once), the coverage check of the
reviewer's code passed, leaf counts by kind, failures, certificates used, smallest margin
(certified lower bound minus theta*), and a comparison with the author's own bounds of the
closed boxes.  Across parts: the 8 root boxes, read against the variable bounds of the OSIL file
(parsed here with xml.etree, independent of osilx, egdata and gms_model), cover the domain:
continuous ranges contain the exact bounds, i5 and i6 span their full ranges, and the i7 ranges
are disjoint, consecutive and span [lb, ub]."""
import glob
import os
import xml.etree.ElementTree as ET
from fractions import Fraction as Fr

import numpy as np

OUT = os.path.dirname(os.path.abspath(__file__))
TH = Fr("5.642100574331458")
NCH = {0: 4, 1: 5, 2: 6, 3: 7, 4: 7, 5: 5, 6: 3, 7: 1}
HOW = ["row", "side", "lp", "farkas", "empty", "split"]
KIND = ["closed box", "pre-closed", "slab", "tiny", "open"]

ns = {"o": "os.optimizationservices.org"}
root = ET.parse(os.path.expanduser("~/.cache/minlplib/minlplib/osil/eg_disc2_s.osil")).getroot()
V = [(v.get("name"), v.get("type", "C"), v.get("lb"), v.get("ub")) for v in root.find("o:instanceData/o:variables", ns)]
V = [v for v in V if v[0] != "objvar"]
print("OSIL variables:", V)

tot = dict(leaves=0, fail=0, time=0.0)
roots = []
allok = True
for k in range(8):
    files = sorted(glob.glob(os.path.join(OUT, "res", f"p{k}_c*.npz")))
    if len(files) != NCH[k]:
        print(f"part {k}: {len(files)} of {NCH[k]} chunk files present -- INCOMPLETE")
        allok = False
        continue
    Z = [np.load(f) for f in files]
    n = int(Z[0]["n_leaves"])
    assert all(int(z["n_leaves"]) == n for z in Z)
    sel = np.concatenate([z["sel"] for z in Z])
    complete = np.array_equal(np.sort(sel), np.arange(n))
    cov = all(bool(z["cov_ok"]) for z in Z) and all(int(z["nbad_red"]) == 0 for z in Z)
    z0 = Z[0]
    ok = np.concatenate([z["ok"] for z in Z]); mg = np.concatenate([z["mg"] for z in Z])
    how = np.concatenate([z["how"] for z in Z]); kind = np.concatenate([z["kind"] for z in Z])
    plb = np.concatenate([z["plb"] for z in Z])
    lo = np.concatenate([z["lo"] for z in Z]); hi = np.concatenate([z["hi"] for z in Z])
    t = sum(float(z["time"]) for z in Z)
    nfail = int((~ok).sum())
    allok &= complete and cov and nfail == 0 and int(z0["n_open"]) == 0 and int(z0["n_tiny"]) == 0
    tot["leaves"] += n; tot["fail"] += nfail; tot["time"] += t
    roots.append((k, z0["root_lo"], z0["root_hi"]))
    print(f"\n== part {k}: root i7 in [{z0['root_lo'][6]:g}, {z0['root_hi'][6]:g}]; processed boxes {int(z0['n_proc'])}, "
          f"generated {int(z0['n_gen'])}, pre-closed {int(z0['n_pre'])}, open {int(z0['n_open'])}, tiny {int(z0['n_tiny'])}")
    print(f"   coverage check (reviewer's code, every chunk): {cov}; every leaf index in exactly one chunk: {complete}")
    kc = z0["kind_counts"]
    print(f"   leaves {n}: " + ", ".join(f"{KIND[i]} {int(kc[i])}" for i in range(5) if kc[i]))
    print(f"   certified {int(ok.sum())}/{n}; failures {nfail}; wall time {t:.0f}s (summed over chunks) ({1000 * t / n:.1f} ms per leaf)")
    hc = np.bincount(how[how >= 0], minlength=6)
    print("   certificate at the leaf itself: " + ", ".join(f"{HOW[i]} {int(hc[i])}" for i in range(6)))
    fin = np.isfinite(mg)
    print(f"   leaves proved infeasible (side/Farkas/empty, possibly after splitting): {int((mg == np.inf).sum())}")
    if fin.any():
        j = np.where(fin)[0][np.argmin(mg[fin])]
        print(f"   smallest margin {mg[j]:.4g} (leaf kind {KIND[kind[j]]}, certificate {HOW[how[j]]}); "
              f"box lo {lo[j].tolist()} hi {hi[j].tolist()}")
        for kd in (0, 2):
            m = fin & (kind == kd)
            if m.any():
                print(f"   smallest margin over {KIND[kd]}s: {mg[m].min():.4g}; "
                      f"quantiles 1%/50% {np.quantile(mg[m], 0.01):.3g}/{np.quantile(mg[m], 0.5):.3g}")
    cb = (kind == 0) & np.isfinite(plb)
    if cb.any():
        am = plb[cb] - float(TH)
        im = mg[cb]
        both = np.isfinite(im) & np.isfinite(am)
        print(f"   closed boxes: author's smallest margin (P_lb - theta*) {am.min():.4g}; "
              f"independent margin >= author's on {int((im[both] >= am[both]).sum())} of {int(both.sum())} with both finite; "
              f"author bound infinite on {int((~np.isfinite(am)).sum())}")
        lt = both & (im < am)
        if lt.any():
            print(f"   where the independent margin is smaller: median ratio indep/author {np.median(im[lt] / am[lt]):.3g}")

print("\n== domain coverage by the parts")
names = [v[0] for v in V]
cont_ok = True
for k, rlo, rhi in roots:
    for i, (nm, ty, lb, ub) in enumerate(V):
        if ty == "C":
            cont_ok &= Fr(float(rlo[i])) <= Fr(lb) and Fr(float(rhi[i])) >= Fr(ub)
        elif nm != "i7":
            cont_ok &= Fr(float(rlo[i])) == Fr(lb) and Fr(float(rhi[i])) == Fr(ub)
print(f"continuous ranges contain the OSIL bounds and i5, i6 span their full ranges in every part: {cont_ok}")
j7 = names.index("i7")
rng = sorted((float(rlo[j7]), float(rhi[j7]), k) for k, rlo, rhi in roots)
print("i7 ranges:", [(a, b, k) for a, b, k in rng])
v7 = V[j7]
cons = (len(rng) == 8 and Fr(rng[0][0]) == Fr(v7[2]) and Fr(rng[-1][1]) == Fr(v7[3])
        and all(rng[i + 1][0] == rng[i][1] + 1 for i in range(len(rng) - 1))
        and all(a == int(a) and b == int(b) and a <= b for a, b, _ in rng))
print(f"i7 ranges are integral, disjoint, consecutive and span [{v7[2]}, {v7[3]}]: {cons}")
allok &= cont_ok and cons
print(f"\nTOTAL: {tot['leaves']} leaves, {tot['fail']} failures, {tot['time']:.0f}s wall time summed over certification chunks")
print("RESULT:", "every leaf of every part certified against theta* = 5.642100574331458 and the parts cover the domain"
      if allok else "NOT COMPLETE OR FAILURES -- see above")
