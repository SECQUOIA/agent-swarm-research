"""Coverage and status recounts for the pattern-theory dossier.

Reads only data files (no scientific module is imported). It copies the
needed JSON files from research-20260929/ into a fresh temporary directory
first, so nothing in the main tree is opened for writing.

Run:  python3 coverage_checks.py > logs/coverage_checks.log
"""
import json, math, os, shutil, tempfile, collections
from fractions import Fraction as F

R = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "..", "research-20260929")
R = os.path.abspath(R)
tmp = tempfile.mkdtemp(prefix="pattern-theory-")
src = {
    "fetched.json": "open-instances-scout/fetched.json",
    "pages.json": "bound-audit/pages.json",
    "census_merged.json": "treewidth-census/census_merged.json",
}
for k, v in src.items():
    shutil.copy(os.path.join(R, v), os.path.join(tmp, k))
Fd = json.load(open(os.path.join(tmp, "fetched.json")))
P = {r["name"]: r for r in json.load(open(os.path.join(tmp, "pages.json")))}
C = {r["name"]: r for r in json.load(open(os.path.join(tmp, "census_merged.json")))}

def num(x):
    try:
        return float(x)
    except Exception:
        return None

def best_gap(p):
    """MINLPLib convention |p-d|/min(|p|,|d|) from the audit's own page parse."""
    sense = p["sense"]
    pts = [num(q["value"]) for q in p["points"]
           if num(q["value"]) is not None and num(q["infeas"]) is not None and num(q["infeas"]) <= 1e-8]
    ds = [num(d["value"]) for d in p["duals"] if num(d["value"]) is not None]
    if not pts or not ds:
        return math.inf
    pb = min(pts) if sense == "min" else max(pts)
    db = max(ds) if sense == "min" else min(ds)
    if pb == db:
        return 0.0
    if pb * db <= 0:
        return math.inf
    return abs(pb - db) / min(abs(pb), abs(db))

def rule(c):
    return ((c["tw_fac_ub"] is not None and c["tw_fac_ub"] <= 16) or
            (c["tw_nlprimal_ub"] is not None and c["tw_nlprimal_ub"] <= 6 and (c["n_nl"] or 0) >= 50))

def meta_open(c):
    try:
        return float(c["gap"]) > 1e-4
    except Exception:
        return True

print("1. Scout file: candidates", len(Fd), "kept (best single-solver gap > 1e-4)", sum(r["keep"] for r in Fd))
keep = [r for r in Fd if r["keep"]]
print("   no listed feasible point:", sum(r["best_primal"] is None for r in keep))
print("   no finite listed dual (with a point):", [r["name"] for r in keep if r["best_primal"] is not None and r["best_dual"] is None])
bands = collections.Counter()
for r in keep:
    if r["best_primal"] is None or r["best_dual"] is None:
        continue
    g = r["gap_best"]
    if g is None or (isinstance(g, float) and math.isinf(g)):
        bands["inf"] += 1
    elif g >= 1: bands[">=1"] += 1
    elif g >= 0.1: bands["[0.1,1)"] += 1
    elif g >= 0.01: bands["[0.01,0.1)"] += 1
    else: bands["(1e-4,0.01)"] += 1
print("   gap bands:", dict(bands))
print("   absolute gap < 1e-5:", [(r["name"], r["abs_gap_best"]) for r in keep if r["abs_gap_best"] is not None and r["abs_gap_best"] < 1e-5])

mism = [r["name"] for r in Fd if (best_gap(P[r["name"]]) > 1e-4) != r["keep"]]
print("2. Independent recount from the audit's page parse: open", sum(best_gap(P[r["name"]]) > 1e-4 for r in Fd), "mismatches", mism)
print("   candidates with a solved mark:", [r["name"] for r in Fd if P[r["name"]]["solved"]])

nc = [n for n, p in P.items() if not p["convex"]]
ncu = [n for n in nc if not P[n]["solved"]]
w = [n for n in ncu if n in C and rule(C[n])]
wg = [n for n in w if meta_open(C[n])]
openb = [n for n in wg if best_gap(P[n]) > 1e-4]
print("3. Funnel: pages", len(P), "nonconvex", len(nc), "nonconvex without S mark", len(ncu),
      "+ width rule", len(w), "+ metadata gap > 1e-4", len(wg), "+ best single-solver gap > 1e-4", len(openb))
print("   solved instances meeting rule and metadata gap:", [n for n in nc if P[n]["solved"] and n in C and rule(C[n]) and meta_open(C[n])])
print("   missing from census:", sorted(set(P) - set(C)))

first = ["lnts50", "lnts100", "lnts200", "lnts400", "camshape100", "camshape200", "camshape400", "camshape800", "dtoc5", "lukvle10", "optcdeg2"]
wave = ["hvycrash", "ex6_2_7", "ex6_2_5", "etamac", "pricing050", "chain50", "chain100", "chain200", "chain400",
        "catmix100", "catmix200", "catmix400", "catmix800", "powerflow0030p", "powerflow0039p", "powerflow0039r",
        "pindyck", "eg_int_s", "eg_disc_s", "eg_disc2_s"]
other = ["kan_r3_h1_n4", "kan_r3_h1_n5", "kan_r3_h1_n9", "kan_r5_h1_n3", "kan_r5_h1_n5", "kan_r5_h1_n8",
         "waterno2_06", "waterno2_09", "waterno2_12", "waterno2_18", "waterno2_24", "ann_cumene_tanh"]
closed = first + wave
print("4. Paper instances: closed", len(closed), "other", len(other))
print("   any with a solved mark:", [n for n in closed + other if P[n]["solved"]])
print("   first wave meeting rule and metadata gap:", [n for n in first if rule(C[n]) and meta_open(C[n])])
print("   first wave with best single-solver gap <= 1e-4:", [(n, "%.4g" % best_gap(P[n])) for n in first if best_gap(P[n]) <= 1e-4])
print("   closed among the", len(openb), "rule-open:", sum(n in openb for n in closed), "; other paper instances among them:", sum(n in openb for n in other))

big = [r for r in C.values() if not r["convex"] and (r["n_nl"] or 0) >= 100]
print("5. Census: nonconvex", sum(not r["convex"] for r in C.values()), "with >= 100 nonlinear variables", len(big))
for k in (4, 8, 12, 20):
    f = sum(1 for r in big if r["tw_fac_ub"] is not None and r["tw_fac_ub"] <= k)
    g = sum(1 for r in big if r["tw_nlprimal_ub"] is not None and r["tw_nlprimal_ub"] <= k)
    print("   width <= %d: factor-incidence %d (%.1f%%), nonlinear primal %d (%.1f%%)" % (k, f, 100 * f / len(big), g, 100 * g / len(big)))

print("6. Exact ratios from summary displays")
print("   camshape100 (opt - listed)/|listed| =", float((F("-4.28414712174675") - F("-4.28415233")) / F("4.28415233")))
print("   lnts50 (ours - listed)/listed =", float((F("0.5546687649381") - F("0.55464755")) / F("0.55464755")))
for n, new, old in [("06 wave2", "263.735099", "165.19"), ("06 now", "278.230573", "165.19"), ("09", "824.834692", "273.90"),
                    ("12", "2089.754565", "479.51"), ("18", "4790.820715", "770.74"), ("24", "6576.151388", "1095.13")]:
    print("   waterno2_%s dual ratio %.4f" % (n, float(F(new) / F(old))))
print("   waterno2_06 (p-d)/d with displays =", float((F("282.888038") - F("278.230573")) / F("278.230573")))
print("   ann (p-d)/|p| =", float((F("-3379.9823940") - F("-3386.5403")) / F("3379.9823940")),
      " (p-d)/|d| =", float((F("-3379.9823940") - F("-3386.5403")) / F("3386.5403")))
rows = [("chain50", "5.0722614939828627", "5.0722614939828723164454381769845467731844"),
        ("chain100", "5.0697846107387505", "5.0697846107387605574911913664186759056714"),
        ("chain200", "5.0689173417931616", "5.0689173417931710001847965010674364416892"),
        ("chain400", "5.068621694604009", "5.0686216946040190143614896914450892607015"),
        ("catmix100", "-0.048069432031144562", "-0.048069432030959562924734533987703146187132711788665927218259922377"),
        ("catmix200", "-0.048059145599072769", "-0.048059145580114393563745030822862486164614881950414095897713142991"),
        ("catmix400", "-0.048056547824671288", "-0.048056547756611554855186829086783477043026066787866243854864283091"),
        ("catmix800", "-0.048055901479675652", "-0.048055901331230800339383491203")]
for n, d, p in rows:
    print("   %s gap from safe dual display and primal upper end: %.4e" % (n, float(F(p) - F(d))))
shutil.rmtree(tmp)
