"""Reviewer r1: recompute the note's tables from the raw logs.

Independent of the stream's code (reads only logs/*.jsonl, logs/*.txt and
data/points_*/*.npz).  Run from split-practice/:
    OMP_NUM_THREADS=1 python3 reviews/r1-code/r1_tables.py
"""
import collections
import glob
import json
import os
import statistics as st
from fractions import Fraction as F

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
L = lambda p: [json.loads(l) for l in open(os.path.join(ROOT, p))]
opt = {d["name"]: d for d in L("logs/opt_gurobi.jsonl")}
OPEN = open(os.path.join(ROOT, "logs/open_gap.txt")).read().split()
NEAR = ["bt_n20_p16_s2", "bt_n30_p0_s1", "bt_n50_p25_s0", "dm_QUTO_t2_n30_p25_s0"]


def q_float(Y, v):
    v = np.asarray(v, float)
    return float(v @ Y @ v + v @ Y[:, 0])


def q_exact(Y, v):
    """exact value of q at the float matrix Y (each double read exactly)"""
    N = len(v)
    v = [int(a) for a in v]
    nz = [i for i in range(N) if v[i]]
    s = F(0)
    for i in nz:
        for j in nz:
            s += v[i] * v[j] * F(float(Y[i, j]))
        s += v[i] * F(float(Y[i, 0]))
    return s


def pct(L, p):
    return float(np.percentile(L, p))  # linear interpolation


print("=" * 20, "Section 6: points")
pts = {}
for s in ["BT10", "BT20", "BT30", "BT50", "DM30", "DM60"]:
    for d in L(f"logs/points_{s}.jsonl"):
        pts.setdefault(s, collections.defaultdict(dict))[d["name"]][d["stage"]] = d
nrec = sum(len(st_) for s in pts for st_ in pts[s].values())
print("stage records", nrec)
fails = []
for s in pts:
    for nm, d in pts[s].items():
        for stg in ("cut_trace", "cut_rand"):
            if stg not in d or d[stg].get("status") in (None,) or "error" in d[stg]:
                fails.append((nm, stg, d.get(stg, {}).get("status"), str(d.get(stg, {}).get("error", ""))[:60]))
print("face stages missing/failed:", len(fails))
for f in fails:
    print("   ", f)
inacc_root = inacc_cut = 0
allrows = []
for s in pts:
    rr, rc, gaps, gaps2, cls, cls2, ncl, ncl2 = [], [], [], [], [], [], 0, 0
    for nm, d in pts[s].items():
        r, c = d["root"], d["cut"]
        inacc_root += r["status"] != "optimal"; inacc_cut += c["status"] != "optimal"
        if r["opt"] is not None:
            o_inc = r["opt"]
        else:
            o_inc = opt[nm]["best"]
        # best known (minimisation): min(incumbent, value of an integral rank-1 final point)
        o = o_inc
        x = np.load(os.path.join(ROOT, f"data/points_{s}/{nm}__{'BT' if s.startswith('BT') else 'DM'}__cut.npz"))
        Yc = x["Y"]
        xr = Yc[0, 1:]
        integral = c["rank"]["1e-05"] == 1 and np.abs(xr - np.round(xr)).max() < 1e-3
        if integral:
            xi = np.round(xr)
            fval = float(xi @ x["Q"] @ xi + x["c"] @ xi)
            if bool(x["linear"]) and abs(xi.sum()) > 0.5:
                integral = False
            elif fval < o:
                o = fval
        rr.append(r["rank"]["1e-05"]); rc.append(c["rank"]["1e-05"])
        for (oo, G, C, tag) in ((o_inc, gaps, cls, 0), (o, gaps2, cls2, 1)):
            G.append(100 * (oo - r["obj"]) / abs(oo))
            C.append(min(100.0, 100 * (c["obj"] - r["obj"]) / (oo - r["obj"])) if oo - r["obj"] > 1e-9 else 100.0)
        ncl += (o_inc - c["obj"]) <= 1e-4 * abs(o_inc)
        ncl2 += (o - c["obj"]) <= 1e-4 * abs(o)
        allrows.append((nm, s, r["rank"]["1e-05"], c["rank"]["1e-05"], 100 * (o - c["obj"]) / abs(o), integral,
                        r["eig"], c["eig"], r["rank"]["0.001"], c["rank"]["0.001"]))
    f = lambda L: f"{min(L)}/{st.median(L):g}/{max(L)}"
    print(f"{s} inst {len(pts[s])} root rank {f(rr)} | gap% incumbent {np.mean(gaps):.2f} best-known {np.mean(gaps2):.2f}"
          f" | closed (incumbent rule) {ncl}/{np.mean(cls):.1f}  (best-known rule) {ncl2}/{np.mean(cls2):.1f} | final rank {f(rc)}")
print("inaccurate root/cut:", inacc_root, inacc_cut)
r1 = [a for a in allrows if a[3] == 1]
print("final rank-1 (1e-5):", len(r1), " of which integral (x within 1e-3 of Z^n):", sum(a[5] for a in r1))
others = [a for a in allrows if a[3] != 1]
print("non-rank-1 finals:", len(others))
for a in sorted(others, key=lambda a: a[4]):
    print(f"   {a[0]:28s} rank {a[3]:3d} (1e-3: {a[9]}) remaining gap {a[4]:.5f}%  eig1,2 {a[7][0]:.4g} {a[7][1]:.4g}")
op = [a for a in allrows if a[0] in OPEN]
print("open: n", len(op), "gap range %.4f..%.4f" % (min(a[4] for a in op), max(a[4] for a in op)),
      "rank1e-5", min(a[3] for a in op), max(a[3] for a in op), "rank1e-3", min(a[9] for a in op), max(a[9] for a in op),
      "eig2 range %.3g..%.3g" % (min(a[7][1] for a in op), max(a[7][1] for a in op)))
# sharpness of root gap
rat = []
for a in allrows:
    e = a[6]; k = a[2]
    rat.append(e[k] / e[k - 1] if k < len(e) else 0)
print("root lambda_{r+1}/lambda_r median %.3g max %.3g" % (np.median(rat), max(rat)))

print("=" * 20, "Section 7: BT10 loops")
for fn in ("logs/loop_bt_BT10.jsonl", "logs/loop_btfam_BT10.jsonl"):
    rows = L(fn)
    byp = collections.defaultdict(list)
    for r in rows:
        p = int(r["name"].split("_p")[1].split("_")[0])
        byp[p].append(r)
    allc = []
    nround_gen = nround = 0
    for p in sorted(byp):
        cl, gaps, rounds, gen = [], [], [], []
        for r in byp[p]:
            o = r["opt"]
            gaps.append(100 * (o - r["root"]) / abs(o))
            if o - r["root"] > 1e-7:
                cl.append(100 * (r["final"] - r["root"]) / (o - r["root"]))
            rounds.append(r["rounds"])
            g = sum(1 for h in r["hist"] if h["fam_viol"].get("3", 0) <= 1e-6 and h["fam_viol"].get("2", 0) <= 1e-6
                    and h["fam_viol"].get("1", 0) <= 1e-6 and -(h["ratio_q"] or 0) > 1e-6)
            gen.append(g)
            nround += len(r["hist"]); nround_gen += g
        allc += cl
        print(f"  {fn[5:]} p={p}: gap {np.mean(gaps):.2f} closed {np.mean(cl):.1f} (open {len(cl)}) rounds {np.mean(rounds):.1f} gen-only {np.mean(gen):.1f}")
    print(f"  {fn[5:]} ALL closed mean {np.mean(allc):.2f} over {len(allc)}; rounds total {nround}, gen-only rounds {nround_gen}")
rows = L("logs/loop_bt_BT10.jsonl")
sup, vm, viol, times = [], [], [], []
for r in rows:
    for h in r["hist"]:
        times.append(h["ratio_time"])
        if all(h["fam_viol"].get(k, 0) <= 1e-6 for k in ("1", "2", "3")) and -(h["ratio_q"] or 0) > 1e-6:
            sup.append(h["ratio_supp"]); vm.append(h["ratio_vmax"]); viol.append(-h["ratio_q"])
print("  gen-only rounds: supp %d..%d, vmax max %d, viol median %.4f max %.3f; supp<=3 among them %d" % (
    min(sup), max(sup), max(vm), np.median(viol), max(viol), sum(s <= 3 for s in sup)))
t10 = times
r20 = L("logs/loop_bt_BT20.jsonl")
t20 = [h["ratio_time"] for r in r20 for h in r["hist"]]
inc = sum(not h["ratio_complete"] for fn in ("logs/loop_bt_BT10.jsonl", "logs/loop_btfam_BT10.jsonl",
                                               "logs/loop_bt_BT20.jsonl", "logs/loop_btfam_BT20.jsonl")
          for r in L(fn) for h in r["hist"])
ncalls = sum(len(r["hist"]) for fn in ("logs/loop_bt_BT10.jsonl", "logs/loop_btfam_BT10.jsonl",
                                       "logs/loop_bt_BT20.jsonl", "logs/loop_btfam_BT20.jsonl") for r in L(fn))
print("  sep_ratio calls in 4 BT loops: %d, incomplete %d" % (ncalls, inc))
print("  bt BT10 ratio time median %.4f max %.4f min %.5f; BT20 median %.3f max %.3f" % (
    np.median(t10), max(t10), min(t10), np.median(t20), max(t20)))
t10all = [h["ratio_time"] for fn in ("logs/loop_bt_BT10.jsonl", "logs/loop_btfam_BT10.jsonl") for r in L(fn) for h in r["hist"]]
t20all = [h["ratio_time"] for fn in ("logs/loop_bt_BT20.jsonl", "logs/loop_btfam_BT20.jsonl") for r in L(fn) for h in r["hist"]]
print("  both modes: BT10 median %.4f max %.4f min %.5f; BT20 median %.3f max %.3f" % (
    np.median(t10all), max(t10all), min(t10all), np.median(t20all), max(t20all)))
for fn in ("logs/loop_bt_BT20.jsonl", "logs/loop_btfam_BT20.jsonl"):
    rr = L(fn)
    cl = [100 * (r["final"] - r["root"]) / (opt[r["name"]]["best"] - r["root"]) for r in rr]
    print(f"  {fn[5:]}: closed mean {np.mean(cl):.1f}; hit 150 rounds {sum(r['rounds'] >= 150 for r in rr)}; stopped {collections.Counter(r.get('stopped') for r in rr)}")
    print("     final ranks of capped:", sorted(r["final_rank"]["1e-05"] for r in rr if r["rounds"] >= 150),
          " max hist rank", max(h["rank"]["1e-05"] for r in rr for h in r["hist"]))
a = {r["name"]: r["final"] for r in L("logs/loop_bt_BT10.jsonl")}
b = {r["name"]: r["final"] for r in L("logs/loop_bt_BT10_firstrun.jsonl")}
print("  BT10 rerun max |final diff|:", max(abs(a[k] - b[k]) for k in a), len(a), len(b))
print("  BT10 loop ranks max", max(h["rank"]["1e-05"] for r in L("logs/loop_bt_BT10.jsonl") for h in r["hist"]))

print("=" * 20, "Section 8: separation records")
recs = []
for k in range(3):
    R = L(f"logs/sep_run2_s{k}.jsonl")
    print("shard", k, len(R))
    recs += R
sel = set()
for fn in ("logs/sep_selection_A.txt", "logs/sep_selection_B.txt"):
    s = [os.path.basename(x) for x in open(os.path.join(ROOT, fn)).read().split()]
    print(fn, len(s), len(set(s)))
    sel |= set(s)
files = [d["file"] for d in recs]
print("records", len(recs), "distinct", len(set(files)), "selection", len(sel), "equal", set(files) == sel)


def cls(d):
    nm, stg = d["file"][:-4].split("__")[0], d["file"][:-4].split("__")[-1]
    if stg == "root":
        return "root"
    if nm in OPEN:
        return "open"
    if nm in NEAR:
        return "near"
    return "OTHER"


C = collections.defaultdict(list)
for d in recs:
    C[cls(d)].append(d)
print({k: len(v) for k, v in C.items()})
print("stages:", collections.Counter(d["file"][:-4].split("__")[-1] for d in recs))
setdir = lambda f: "points_" + ("BT" if f.startswith("bt") else "DM") + f.split("_n")[1].split("_")[0]
maxdq = 0
rows_check = []
for g in ("root", "open", "near"):
    R = C[g]
    ra = [d["ratio"] for d in R]
    tm = [r["time"] for r in ra]
    fin = sum(r["complete"] for r in ra)
    nv = [r["ratio"] for r in ra if r["v"] is not None]
    vv = [-r["q"] for r in ra if r["q"] is not None]
    sup = collections.Counter(r["supp"] for r in ra if r["q"] is not None and -r["q"] > 1e-3)
    print(f"  {g}: {len(R)} points; finished {fin}; time median {np.median(tm):.3f} p90 {pct(tm, 90):.3f} max {max(tm):.3f};"
          f" ratio median {np.median(nv):.4g}; viol median {np.median(vv):.4g}; supports(viol>1e-3) {dict(sorted(sup.items()))}")
    vmaxall = max(max(abs(a) for a in r["v"]) for r in ra if r["v"] is not None)
    print(f"     max |coef| incl v0 among returned: {vmaxall}; no-vector records: {sum(r['v'] is None for r in ra)}")
    if g == "root":
        bysize = collections.defaultdict(list)
        for d in R:
            bysize[d["N"] - 1].append(d["ratio"])
        for n_ in sorted(bysize):
            print(f"     n={n_}: {len(bysize[n_])} finished {sum(r['complete'] for r in bysize[n_])} median time {np.median([r['time'] for r in bysize[n_]]):.3f}")
        print("     best support:", collections.Counter(r["supp"] for r in ra))
        imp = 0; neg = 0
        for d in R:
            fam = max(d[f"fam{k}"]["max_ratio"] for k in (1, 2, 3) if f"fam{k}" in d)
            if d["ratio"]["ratio"] > fam + 1e-8:
                imp += 1
            if d["ratio"]["ratio"] < fam - 1e-8:
                neg += 1
        print(f"     root ratio improves best fam ratio by >1e-8: {imp}; lower by >1e-8: {neg}")
    if g in ("open", "near"):
        for d in R:
            fam3 = max(d[f"fam{k}"]["max_viol"] for k in (1, 2, 3))
            famr = max(d[f"fam{k}"]["max_ratio"] for k in (1, 2, 3))
            r = d["ratio"]
            print(f"     {d['file']:40s} rank {d['rank']['1e-05']:2d} famviol {fam3:.4f} famratio {famr:.5f} ratio {r['ratio']:.6g} "
                  f"q {r['q']} supp {r['supp']} vmax {r['vmax']} complete {r['complete']} t {r['time']:.2f}")
        fin_t = [d["ratio"]["time"] for d in R if d["ratio"]["complete"]]
        print(f"     finished-call time median {np.median(fin_t):.3f} max {max(fin_t):.3f}")
    # Gurobi
    for K in (1, 3, 10):
        G = [d[f"grb{K}"] for d in R]
        print(f"     grb{K}: statuses {dict(collections.Counter(x['status'] for x in G))}; time median {np.median([x['time'] for x in G]):.1f};"
              f" viol median {np.median([-x['q'] for x in G if x['q'] is not None]):.4g}; below -0.250001: {sum(1 for x in G if x['q'] is not None and x['q'] < -0.250001)}"
              f" min q {min(x['q'] for x in G if x['q'] is not None):.6f}")

# exact re-evaluation of every returned vector at the stored matrix
print("  re-evaluating returned vectors at stored Y (exact rational of the doubles)")
maxd_ratio = 0; maxd_grb = 0; nvec = 0; lost = 0; nonint = 0; bad_ratio_formula = 0
for d in recs:
    Y = np.load(os.path.join(ROOT, "data", setdir(d["file"]), d["file"]))["Y"]
    Y = (Y + Y.T) / 2
    r = d["ratio"]
    if r["v"] is not None:
        nvec += 1
        v = r["v"]
        if any(int(a) != a for a in v):
            nonint += 1
        qe = float(q_exact(Y, v))
        maxd_ratio = max(maxd_ratio, abs(qe - r["q"]))
        if -r["q"] > 1e-3 and not qe < -1e-3 * 0.99:
            lost += 1
        w2 = sum(int(a) ** 2 for a in v[1:])
        if abs(-r["q"] / w2 - r["ratio"]) > 1e-12 * max(1, r["ratio"]):
            bad_ratio_formula += 1
    for K in (1, 3, 10):
        g = d[f"grb{K}"]
        if g["v"] is not None:
            qe = float(q_exact(Y, g["v"]))
            maxd_grb = max(maxd_grb, abs(qe - g["q"]))
            if max(abs(a) for a in g["v"]) > K:
                nonint += 1
print(f"  ratio vectors {nvec}: max |q_exact - logged q| {maxd_ratio:.3g}; violations>1e-3 lost {lost}; ratio formula mismatches {bad_ratio_formula};"
      f" grb max |q_exact - logged| {maxd_grb:.3g}; non-integer/out-of-box {nonint}")

# Theorem 3
print("  Theorem 3:")
att = [d for d in recs if "thm3" in d]
err = [d for d in att if "error" in d["thm3"]]
ok = [d for d in att if "error" not in d["thm3"]]
print(f"   attempts {len(att)} errors {len(err)} {[d['file'] for d in err]} values {len(ok)}; ranks>12 skipped {sum(1 for d in recs if 'thm3' not in d)}")
print("   error texts:", set(d["thm3"]["error"][:80] for d in err))
for g in ("root", "open", "near"):
    T = [d["thm3"] for d in ok if cls(d) == g]
    near = sum(abs(t["q"] + 0.25) <= 1e-9 for t in T)
    ex = sum(t["q"] == -0.25 for t in T)
    comp = sum(t["complete"] for t in T)
    dig = [t["vmax_digits"] for t in T if t["q"] < 0]
    errm = max(t["err"] for t in T)
    tm = [t["time"] for t in T]
    sane = sum(1 for t in T if t["q_at_Y"] is not None and not isinstance(t["q_at_Y"], str) and -0.25 - 1e-6 <= t["q_at_Y"] < 0)
    ret = sum(1 for t in T if t["q_at_Y"] is not None)
    print(f"   {g}: {len(T)} values; within 1e-9 of -1/4: {near}; ==-0.25: {ex}; complete {comp}; returned splits {ret}; sane {sane};"
          f" digits median {np.median(dig) if dig else None} max {max(dig) if dig else None}; err max {errm:.3g}; time median {np.median(tm):.3f} max {max(tm):.2f}")
    if g == "root":
        sv = [t for t in T if t["q_at_Y"] is not None and not isinstance(t["q_at_Y"], str) and -0.25 - 1e-6 <= t["q_at_Y"] < 0]
        print("     sane ones: rank", sorted(t["rank"] for t in sv), "supp", sorted(t["supp"] for t in sv), "vmax", sorted(t["vmax"] for t in sv))
    nonv = [t for t in T if t["q_at_Y"] is None]
    if nonv:
        print("     no split returned:", len(nonv))
print("   total returned splits", sum(1 for d in ok if d["thm3"]["q_at_Y"] is not None))

print("=" * 20, "Section 9: DM loops")
fam = {d["name"]: d for d in L("logs/loop_dmfam_open.jsonl")}
plus = {d["name"]: d for d in L("logs/loop_dmplus_open.jsonl")}
allpts = {nm: d for s in pts for nm, d in pts[s].items()}
for nm in OPEN:
    o = opt[nm]["best"]
    g = lambda b: 100 * (o - b) / abs(o)
    a, b = fam[nm], plus[nm]
    print(f"  {nm:24s} root {g(allpts[nm]['root']['obj']):.2f} fam {g(allpts[nm]['cut']['obj']):.4f} dmfam {g(a['final']):.4f} ({a['rounds']},{a['stopped']},{a['time']:.0f},rk{a['final_rank']['1e-05']}) "
          f"dmplus {g(b['final']):.6f} ({b['rounds']},{b['stopped']},{b['time']:.0f}) rank {b['final_rank']['1e-05']} retries {a.get('retries')},{b.get('retries')}")
for nm in ("dm_QUTO_t1_n60_p50_s0", "dm_LIN_t3_n60_p75_s0"):
    b = plus[nm]
    H = b["hist"]
    nofam = sum(1 for h in H if all(h["fam_viol"].get(k, 0) <= 1e-6 for k in ("1", "2", "3")))
    gen = [h for h in H if all(h["fam_viol"].get(k, 0) <= 1e-6 for k in ("1", "2", "3")) and h["ratio_supp"] is not None]
    print(f"  {nm}: rounds {len(H)} no-fam-violated {nofam}; gen supp {min(h['ratio_supp'] for h in gen)}..{max(h['ratio_supp'] for h in gen)}"
          f" vmax {max(h['ratio_vmax'] for h in gen)} viol {min(-h['ratio_q'] for h in gen):.3f}..{max(-h['ratio_q'] for h in gen):.3f};"
          f" incomplete calls {sum(not h['ratio_complete'] for h in H)}/{len(H)}; median ratio_time {np.median([h['ratio_time'] for h in H]):.2f}")
    print(f"     bound moved (pp of |opt|) {100 * (b['final'] - fam[nm]['final']) / abs(opt[nm]['best']):.6f} vs dmfam;"
          f" vs families-only cut {100 * (b['final'] - allpts[nm]['cut']['obj']) / abs(opt[nm]['best']):.6f}")
    print(f"     dmfam rounds fam-violated: {[(h['round'], max(h['fam_viol'].values())) for h in fam[nm]['hist']][:3]} ...")
for nm in OPEN:
    b = plus[nm]
    H = b["hist"]
    print(f"  {nm:24s} dmplus ranks {[h['rank']['1e-05'] for h in H]} median ratio_time {np.median([h['ratio_time'] for h in H]):.2f} max {max(h['ratio_time'] for h in H):.2f} incomplete {sum(not h['ratio_complete'] for h in H)}/{len(H)}")
for nm in ("dm_QUTO_t1_n30_p75_s0", "dm_LIN_t2_n30_p75_s0", "dm_QUTO_t2_n60_p25_s0", "dm_QUTO_t1_n60_p75_s0"):
    h = fam[nm]["hist"][-1]
    print(f"  final dmfam diag {nm}: supp {h['ratio_supp']} vmax {h['ratio_vmax']} viol {-(h['ratio_q'] or 0):.3f} complete {h['ratio_complete']} famviol {h['fam_viol']}")
print("  failed attempts:", [(d.get("name") or d.get("spec"), d.get("mode")) for d in L("logs/loop_failed_attempts.jsonl")])
for fn in ("logs/opt_gurobi_long_1.jsonl", "logs/opt_gurobi_long_2.jsonl"):
    for d in L(fn):
        print("  long:", d)
        nm = d["name"]
        pb = plus[nm]["final"]
        print(f"     gap vs incumbent {100 * (d['best'] - pb) / abs(d['best']):.6f}%  vs bound {100 * (d['bound'] - pb) / abs(d['bound']):.6f}%  "
              f"opt gap {100 * (d['best'] - d['bound']) / abs(d['best']):.8f}%")

print("=" * 20, "Section 10: hard instances")
H = L("logs/hard_run2.jsonl")
print("records", len(H), "enum complete", sum(h["enum"]["complete"] for h in H))
mx = 0
for h in H:
    if h["enum"]["complete"]:
        mx = max(mx, abs(h["enum"]["q"] - h["predicted_min_q"]) if h["enum"]["q"] is not None else 0)
print("max |enum q - predicted| over complete:", mx)
print("fam3 detects violation (q>=3):", sum(1 for h in H if h["q"] >= 3 and max(h[f"fam{k}"]["max_viol"] for k in (1, 2, 3)) > 1e-12))
big = [h for h in H if h["N"] >= 47]
print("N>=47 records", len(big), "grb not optimal", sum(not h["grb1"]["status"].startswith("Optimal") for h in big),
      "cor5:", sum(1 for h in big if h["kind"] == "cor5"), sum(1 for h in big if h["kind"] == "cor5" and not h["grb1"]["status"].startswith("Optimal")))
for h in H:
    if h["kind"] == "cor5" and h["q"] in (3, 6, 10, 15, 20, 25):
        print(f"  q={h['q']} n={h['n']} N={h['N']} planted={h['planted']} cover={h['cover']} cond={h['cond']:.0f} pred={h['predicted_min_q']:.2g}"
              f" fam={max(h[f'fam{k}']['max_viol'] for k in (1, 2, 3)):.2g} enum={h['enum']['time']:.2f}{'' if h['enum']['complete'] else '*'} q={h['enum']['q']}"
              f" grb={h['grb1']['time']:.1f} {h['grb1']['status'][:4]} q={h['grb1']['q']} scip={h.get('scip1', {}).get('time')}")
ratios = []
for h in H:
    if "scip1" in h and h["grb1"]["status"].startswith("Optimal") and h["scip1"]["status"] == "optimal":
        ratios.append(h["scip1"]["time"] / h["grb1"]["time"])
print("SCIP/Gurobi time ratio where both finish: %.2f..%.1f (n=%d)" % (min(ratios), max(ratios), len(ratios)))
print("scip statuses", collections.Counter(h["scip1"]["status"] for h in H if "scip1" in h))
print("thm1 scip timeouts:", [(h["n"], h["planted"]) for h in H if "scip1" in h and h["scip1"]["status"] != "optimal"])
c5 = [h for h in H if h["kind"] == "cor5" and h["cover"]]
print("cor5 cover: violation <1e-3 for N>=18?", all(-h["predicted_min_q"] < 1e-3 for h in c5 if h["N"] >= 18),
      "max at N>=18 %.3g" % max(-h["predicted_min_q"] for h in c5 if h["N"] >= 18),
      "; <1e-4 for N>=62?", all(-h["predicted_min_q"] < 1e-4 for h in c5 if h["N"] >= 62),
      "; N=11..:", sorted(set((h["N"], round(-h["predicted_min_q"], 6)) for h in c5))[:6])
print("cond range", min(h["cond"] for h in H), max(h["cond"] for h in H))
print("violations (cover) range", min(-h["predicted_min_q"] for h in H if h["cover"]), max(-h["predicted_min_q"] for h in H if h["cover"]))
for h in L("logs/hard_long.jsonl"):
    print("  long", h)

print("=" * 20, "machine load")
ld = [l.split() for l in open(os.path.join(ROOT, "logs/machine_load_run2.txt")) if l.strip()]
one = [float(a[1]) for a in ld]
print(len(ld), ld[0][0], ld[-1][0], "min %.2f max %.2f median %.2f p90 %.2f" % (min(one), max(one), np.median(one), pct(one, 90)))
