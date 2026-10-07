"""Second-pass checks for the pattern-theory dossier (2026-10-04, r2).

Reads only data files and saved logs. Every input is first copied from
research-20260929/ (and the local MINLPLib OSIL cache) into a fresh temporary
directory; no research script or module is imported or executed.

Run:  OMP_NUM_THREADS=1 python3 r2_checks.py > logs/r2_checks.log
"""
import csv, json, math, os, re, shutil, tempfile
import xml.etree.ElementTree as ET
from collections import Counter
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "..", "research-20260929"))
OSIL = os.path.expanduser("~/.cache/minlplib/minlplib/osil")
tmp = tempfile.mkdtemp(prefix="pt-r2-")
for src, dst in [("bound-audit/pages.json", "pages.json"),
                 ("open-instances-scout/fetched.json", "fetched.json"),
                 ("open-instances-scout/candidates.json", "candidates.json"),
                 ("treewidth-census/census_merged.json", "census.json"),
                 ("publication/solver-runs/results_table.csv", "results.csv")]:
    shutil.copy(os.path.join(R, src), os.path.join(tmp, dst))
NAMES = ("lnts50 lnts400 dtoc5 camshape100 lukvle10 optcdeg2 hvycrash ex6_2_5 ex6_2_7 etamac "
         "pricing050 chain50 chain400 catmix100 catmix800 powerflow0030p powerflow0039p "
         "powerflow0039r pindyck eg_int_s eg_disc_s eg_disc2_s waterno2_06 ann_cumene_tanh kan_r5_h1_n8").split()
os.makedirs(os.path.join(tmp, "osil"))
for n in NAMES:
    shutil.copy(os.path.join(OSIL, n + ".osil"), os.path.join(tmp, "osil", n + ".osil"))
J = lambda f: json.load(open(os.path.join(tmp, f)))
P = {r["name"]: r for r in J("pages.json")}
C = {r["name"]: r for r in J("census.json")}
cand = {r["name"] for r in J("candidates.json")}
Fd = {r["name"]: r for r in J("fetched.json")}

def q(x):
    try: return Fr(x)
    except Exception: return None
def best(r):
    pts = [q(t["value"]) for t in r["points"]
           if q(t["infeas"]) is not None and q(t["infeas"]) <= Fr(1, 10**8) and q(t["value"]) is not None]
    ds = sorted([q(d["value"]) for d in r["duals"] if q(d["value"]) is not None], reverse=(r["sense"] == "min"))
    p = (min(pts) if r["sense"] == "min" else max(pts)) if pts else None
    return p, ds
def relgap(p, d):
    if p is None or d is None: return math.inf
    if p == d: return 0.0
    if p * d <= 0: return math.inf
    return float(abs(p - d) / min(abs(p), abs(d)))
def width_ok(c):
    a, b, n = c.get("tw_fac_ub"), c.get("tw_nlprimal_ub"), c.get("n_nl") or 0
    return (a is not None and a <= 16) or (b is not None and b <= 6 and n >= 50)
def meta_gap(c):
    try: return float(c.get("gap"))
    except Exception: return math.inf

first = "lnts50 lnts100 lnts200 lnts400 camshape100 camshape200 camshape400 camshape800 dtoc5 lukvle10 optcdeg2".split()
later = ("hvycrash ex6_2_7 ex6_2_5 etamac pricing050 chain50 chain100 chain200 chain400 catmix100 catmix200 "
         "catmix400 catmix800 powerflow0030p powerflow0039p powerflow0039r pindyck eg_int_s eg_disc_s eg_disc2_s").split()
other = ("kan_r3_h1_n4 kan_r3_h1_n5 kan_r3_h1_n9 kan_r5_h1_n3 kan_r5_h1_n5 kan_r5_h1_n8 "
         "waterno2_06 waterno2_09 waterno2_12 waterno2_18 waterno2_24 ann_cumene_tanh").split()

print("== A. Scout rule over the census (census convex flag and metadata gap, as the scout used)")
rule = {n for n, c in C.items() if not c["convex"] and width_ok(c) and meta_gap(c) > 1e-4}
print("census instances:", len(C), "| rule set:", len(rule))
print("rule set minus scout candidates:", sorted(rule - cand))
print("scout candidates minus rule set:", sorted(cand - rule))
print("solved (S) marks in rule set:", sorted(n for n in rule if P[n]["solved"]))
print("census/page convex-flag disagreements:", [n for n in C if n in P and C[n]["convex"] != P[n]["convex"]])
op = {n for n in rule if relgap(*(lambda pd: (pd[0], pd[1][0] if pd[1] else None))(best(P[n]))) > 1e-4}
print("rule-open (best single-solver relative gap > 1e-4):", len(op), "| scout keep:", sum(r["keep"] for r in Fd.values()))
print("rule-open first-wave:", sorted(op & set(first)))
print("paper closures in rule-open:", sum(n in op for n in first + later), "| other paper instances:", sum(n in op for n in other))
print("paper instances outside the rule set:", [n for n in first + later + other if n not in rule])
print("paper instances with an S mark:", [n for n in first + later + other if P[n]["solved"]])
missing = sorted(set(P) - set(C)); print("pages missing from census:", missing)
for n in missing:
    r = P[n]; p, ds = best(r)
    print("  ", n, "convex", r["convex"], "solved", r["solved"], "nvars", r["nvars"], "listing dual", repr(r["listing_dual"]),
          "best single-solver gap", relgap(p, ds[0] if ds else None))

print("\n== B. Listing (metadata) dual versus third-best single-solver dual")
ok = bad = 0; worst = 0.0
for n, r in P.items():
    p, ds = best(r); ld = q(r.get("listing_dual"))
    if ld is None or len(ds) < 3 or not math.isfinite(float(ds[2])): continue
    rel = abs(float(ld - ds[2])) / max(1.0, abs(float(ds[2])))
    if rel <= 1e-4: ok += 1
    else:
        bad += 1; worst = max(worst, rel)
        print("  exception:", n, "listing dual", r.get("listing_dual"), "| raw duals:", [d["raw"] for d in r["duals"]])
print("instances with >= 3 finite duals: listing dual within 1e-4 (rel. to max(1,|d3|)) of third-best:", ok, "| not:", bad)
r = P["4stufen"]; p, ds = best(r)
print("4stufen: solved", r["solved"], "| #duals equal to best primal:", sum(d == p for d in ds), "| listing dual", r["listing_dual"])

print("\n== C. Bands of the 146 (audit page parse, independent of the scout's parser)")
keep = [n for n, r in Fd.items() if r["keep"]]
nopt = 0; nodual = []; bands = Counter(); small = []
for n in keep:
    p, ds = best(P[n])
    if p is None: nopt += 1; continue
    if not ds: nodual.append(n); continue
    d = ds[0]; g = relgap(p, d)
    bands["inf" if math.isinf(g) else ">=1" if g >= 1 else "[0.1,1)" if g >= 0.1 else "[0.01,0.1)" if g >= 0.01 else "(1e-4,0.01)"] += 1
    if abs(p - d) < Fr(1, 10**5): small.append((n, float(abs(p - d))))
print("kept", len(keep), "| no point", nopt, "| no dual", nodual, "|", dict(bands), "| abs gap < 1e-5:", small)
for n in ["camshape100", "lnts50"]:
    p, ds = best(P[n]); print(n, "listed relative gap (listed primal vs best dual): %.5e" % relgap(p, ds[0]))
print("camshape100 vs exact optimum: %.5e" % float((Fr("-4.28414712174675") - Fr("-4.28415233")) / Fr("4.28415233")))
print("lnts50 vs certified dual:      %.5e" % float((Fr("0.5546687649381") - Fr("0.55464755")) / Fr("0.55464755")))

print("\n== D. Variable bound types in the OSIL files (free = both bounds infinite)")
for n in NAMES:
    s = open(os.path.join(tmp, "osil", n + ".osil")).read()
    vs = re.findall(r"<var ([^>]*?)/?>", s); c = Counter()
    for v in vs:
        lb = re.search(r'\blb="([^"]*)"', v); ub = re.search(r'\bub="([^"]*)"', v)
        lbv = lb.group(1) if lb else "0"; ubv = ub.group(1) if ub else "INF"
        li, ui = lbv.upper() == "-INF", ubv.upper() == "INF"
        c["free" if li and ui else "lower-only" if ui else "upper-only" if li else "boxed"] += 1
    print(f"{n:16s} vars {len(vs):6d}  " + "  ".join(f"{k} {c[k]}" for k in ("free", "lower-only", "upper-only", "boxed")))

print("\n== E. chain50 nonlinear-primal graph with constant factors distributed over sums")
ns = {"o": "os.optimizationservices.org"}
root = ET.parse(os.path.join(tmp, "osil", "chain50.osil")).getroot()
tag = lambda e: e.tag.split("}")[1]
def vset(e): return {int(x.get("idx")) for x in e.iter() if tag(x) == "variable"}
def terms(e):
    t, ch = tag(e), list(e)
    if t == "sum": return [u for c in ch for u in terms(c)]
    if t == "negate": return terms(ch[0])
    if t in ("product", "times"):
        nz = [c for c in ch if vset(c)]
        if len(nz) == 1: return terms(nz[0])
    return [e]
edges = set(); top = []
for nl in root.findall(".//o:nonlinearExpressions/o:nl", ns):
    e0 = list(nl)[0]; top.append((nl.get("idx"), tag(e0), [tag(c) for c in e0][:3]))
    for tm in terms(e0):
        v = sorted(vset(tm)); edges |= {(v[i], v[j]) for i in range(len(v)) for j in range(i + 1, len(v))}
deg = Counter(); [deg.update([a, b]) for a, b in edges]
print("top-level nl nodes (idx, tag, first children):", top)
print("edges", len(edges), "| max degree", max(deg.values()), "| census tw_nlprimal_ub:", C["chain50"]["tw_nlprimal_ub"])

print("\n== F. One-hour solver duals versus certificates (saved campaign table)")
rows = list(csv.DictReader(open(os.path.join(tmp, "results.csv"))))
by = {}
for r in rows: by.setdefault(r["instance"], {})[r["solver"]] = r
fl = lambda x: (float(x) if x not in ("", None) else None)
order = ("lnts50 lnts100 lnts200 lnts400 dtoc5 lukvle10 optcdeg2 chain50 chain100 chain200 chain400 "
         "catmix100 catmix200 catmix400 catmix800 camshape100 camshape200 camshape400 camshape800 hvycrash "
         "ex6_2_5 ex6_2_7 pricing050 etamac pindyck powerflow0030p powerflow0039p powerflow0039r "
         "eg_int_s eg_disc_s eg_disc2_s").split()
print("instance | listed dual | certificate | BARON | GUROBI | SCIP | best unqualified | (best-listed)/(cert-listed) | flags")
for n in order:
    d = by[n]; r0 = next(iter(d.values())); s = r0["sense"]
    L, Ct = fl(r0["listed_dual"]), fl(r0["certificate_dual"]); cells = []; cand_v = []; flags = []
    for sv in ("BARON", "GUROBI", "SCIP"):
        r = d.get(sv)
        if r is None or fl(r["dual"]) is None: cells.append("—"); continue
        v = fl(r["dual"]); f = ""
        if r["globality_warning"] == "True": f += "*"
        if r["scip_argument_bounds_tightened"] == "True": f += "t"
        if r["loaded_first_batch"] == "True": f += "o"
        cells.append("%.6g%s" % (v, f))
        if "*" not in f and math.isfinite(v): cand_v.append(v)
    b = (max(cand_v) if s == "min" else min(cand_v)) if cand_v else None
    frac = None if b is None else ((b - L) / (Ct - L) if s == "min" else (L - b) / (L - Ct))
    print(n, "|", r0["listed_dual"], "|", r0["certificate_dual"], "|", " | ".join(cells), "|",
          "none" if b is None else "%.6g" % b, "|", "n/a" if frac is None else "%.3f" % frac)
print("flags: * globality not guaranteed (excluded from 'best unqualified'); t SCIP tightened argument bounds; o overloaded first batch")

print("\n== G. camshape100 cell-constant DP (first-wave report, Section 8.1): local convergence order")
opt = -4.28414712174675; data = [(1e-3, -5.279), (4e-4, -5.096), (2e-4, -4.900), (1e-4, -4.711), (5e-5, -4.580), (2.5e-5, -4.451)]
prev = None
for dd, bb in data:
    e = opt - bb
    print("d = %-7g error %.3f" % (dd, e) + ("" if prev is None else "   local order log(e1/e2)/log(d1/d2) = %.2f" % (math.log(prev[1] / e) / math.log(prev[0] / dd))))
    prev = (dd, e)

print("\n== H. S mark versus a naive three-displayed-duals test (points with infeasibility <= 1e-6)")
from collections import Counter as _C
agree = _C()
def near(v, p):
    return v == p or (v * p > 0 and abs(v - p) / min(abs(v), abs(p)) <= Fr(1, 10**6))
for n, r in P.items():
    pts = [q(t["value"]) for t in r["points"] if q(t["infeas"]) is not None and q(t["infeas"]) <= Fr(1, 10**6) and q(t["value"]) is not None]
    p = (min(pts) if r["sense"] == "min" else max(pts)) if pts else None
    k = sum(1 for d in r["duals"] if q(d["value"]) is not None and p is not None and near(q(d["value"]), p))
    kinf = sum(1 for d in r["duals"] if str(d["value"]).strip().lower() in ("inf", "-inf", "infeasible"))
    agree[(r["solved"], k >= 3 or (p is None and kinf >= 3))] += 1
print("(S mark, naive test) counts:", dict(agree), "| agreeing:", agree[(True, True)] + agree[(False, False)], "of", len(P))
for tol in (8, 6):
    hits = []
    for n in first + later + other:
        r = P[n]
        pts = [q(t["value"]) for t in r["points"] if q(t["infeas"]) is not None and q(t["infeas"]) <= Fr(1, 10**tol) and q(t["value"]) is not None]
        p = (min(pts) if r["sense"] == "min" else max(pts)) if pts else None
        k = sum(1 for d in r["duals"] if q(d["value"]) is not None and p is not None and near(q(d["value"]), p))
        if k: hits.append((n, k))
    print("paper instances with listed duals within 1e-6 of the best point (point infeasibility <= 1e-%d):" % tol, hits)
shutil.rmtree(tmp)
