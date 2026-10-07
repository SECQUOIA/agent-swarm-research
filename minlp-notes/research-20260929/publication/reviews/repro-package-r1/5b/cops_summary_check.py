"""Exact check of every COPS (chain50-400, catmix100-800) number shown in
research-20260929/open-instances-summary.md, plus a search for the five unsafe
detailed-note decimals.

Read-only. Uses only saved outputs and fractions.Fraction (no optimization is rerun).
Both families are minimization problems (checked from the cached OSIL files).
A displayed lower bound s is safe iff Fraction(s) <= exact certified binary64 bound.
A displayed absolute gap g is safe iff g >= (upper bound on primal value) - (exact bound).

usage: python3 cops_summary_check.py   (run from anywhere; prints a report)
"""
import json
import math
import os
import re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.abspath(os.path.join(HERE, "../../../.."))  # research-20260929
OSIL = os.path.expanduser("~/.cache/minlplib/minlplib/osil")
W2 = os.path.join(R, "open-instances-wave2/cops/logs")
CV = os.path.join(R, "reviews/cops-verification/logs")
CR = os.path.join(R, "reviews/catmix-recheck-checks/logs")
PC = os.path.join(R, "publication/primal/chain/logs")
SUMMARY = os.path.join(R, "open-instances-summary.md")


def objs(path):
    """all JSON objects printed in a log file"""
    s, out, dec, i = open(path).read(), [], json.JSONDecoder(), 0
    while True:
        j = s.find("{", i)
        if j < 0:
            return out
        try:
            o, k = dec.raw_decode(s[j:])
            out.append(o)
            i = j + k
        except ValueError:
            i = j + 1


def e(q, d=4):
    return "%.*e" % (d, float(q))


def dec(q, places=40):
    """exact rational -> decimal string truncated toward zero at `places` places (for display only)"""
    sgn = "-" if q < 0 else ""
    a = abs(q)
    n = a.numerator * 10 ** places // a.denominator
    s = str(n).rjust(places + 1, "0")
    return sgn + s[:-places] + "." + s[-places:]


def up_sig(q, sig):
    """smallest decimal with `sig` significant digits that is >= q > 0 (string in e-notation)"""
    ex = math.floor(math.log10(float(q)))
    while F(10) ** ex > q:
        ex -= 1
    while F(10) ** (ex + 1) <= q:
        ex += 1
    unit = F(10) ** (ex - sig + 1)
    m = -((-q) // unit)  # ceil
    v = m * unit
    return v, ("%.*e" % (sig - 1, float(v)))


def double_upper(s):
    """rigorous upper bound on an exact value printed as '%.20g' % float(exact)"""
    d = float(s)
    return F(d) + F(math.ulp(d)) / 2 + F(1, 10 ** 22)


print("== objective sense from cached OSIL")
for n in ("chain50", "chain100", "chain200", "chain400", "catmix100", "catmix200", "catmix400", "catmix800"):
    m = re.search(r'<obj [^>]*maxOrMin="(\w+)"', open(os.path.join(OSIL, n + ".osil")).read())
    print("  %-10s %s" % (n, m.group(1)))
    assert m.group(1) == "min"

summ = open(SUMMARY).read().split("\n")


def find_line(sub):
    hits = [i + 1 for i, l in enumerate(summ) if sub in l]
    assert len(hits) == 1, (sub, hits)
    return hits[0]


ln_chain = find_line("| chain50–400 | 0.0826–0.1745 | 5.06862 … 5.07226 | same to 1e-14 | ≤ 1.0e-14 |")
ln_cat = find_line("| catmix100–800 | −0.0666 … −1.489 | −0.04806944 … −0.04805591 | improved primal points | 1.65e-13 (100) … 1.5e-10 (800, verifier) |")
ln_note = find_line("For lnts50–400, dtoc5, lukvle10, chain50–400 and")
print("== summary lines: chain row %d, catmix row %d, tolerance-primal note starts %d" % (ln_chain, ln_cat, ln_note))
print("   convention (summary lines 9-11): absolute gaps unless marked; displayed duals rounded outward")
other = [i + 1 for i, l in enumerate(summ) if re.search(r"5\.0[67]\d|0\.0480|catmix|chain\d", l)
         and i + 1 not in (ln_chain, ln_cat, ln_note)]
print("   other summary lines mentioning chain/catmix numbers or names:", other)

# ---------------- chain ----------------
print("\n== chain (min). Displays on summary line %d: dual range '5.06862 … 5.07226', primal 'same to 1e-14', gap '≤ 1.0e-14'" % ln_chain)
ver_v = {}
for fn in ("chain50_bnb.log", "chain100_200_bnb.log", "chain400_bnb.log"):
    for o in objs(os.path.join(CV, fn)):
        if "certified_bound" in o:
            ver_v[o["N"]] = o
ver_p = {o["instance"]: o for o in objs(os.path.join(PC, "verify.log"))}
chain = {}
for N in (50, 100, 200, 400):
    a = json.load(open(os.path.join(W2, "chain%d_bound.json" % N)))
    assert a["bnb"]["unresolved"] == 0 and ver_v[N]["unresolved"] == 0
    L = F(a["bnb"]["bound"])
    assert F(ver_v[N]["certified_bound"]) == L
    # tolerance-feasible double point (row viol. <= 3.6e-16): value printed to 20 digits; allow 1 unit in last digit
    pd = F(a["primal"]["obj_double_point"]) + F(1, 10 ** 19)
    kkt = F(a["primal"]["kkt_value"]) + F(1, 10 ** 24)
    px = F(ver_p["chain%d" % N]["objective_hi"])  # exactly feasible point (publication/primal/chain)
    chain[N] = dict(L=L, pd=pd, kkt=kkt, px=px)
    print("  chain%-3d L = %s (binary64 %r)" % (N, dec(L), a["bnb"]["bound"]))
    print("           gap vs tolerance double point (summary's stated primal) <= %s ; vs KKT value <= %s ; vs exact point <= %s"
          % (e(pd - L), e(kkt - L), e(px - L)))
for s, N in (("5.06862", 400), ("5.07226", 50)):
    ok = F(s) <= chain[N]["L"]
    print("  range end %s for chain%d: %s <= L ? %s (margin %s)" % (s, N, s, F(s) <= chain[N]["L"], e(chain[N]["L"] - F(s))))
    assert ok
print("  every chain bound lies in [5.06862, 5.07227):", all(F("5.06862") <= c["L"] < F("5.07227") for c in chain.values()))
lim = F("1.0e-14")
for key, lab in (("pd", "tolerance-feasible double points (current summary primal)"),
                 ("kkt", "60-digit KKT value"), ("px", "exactly feasible points (publication/primal/chain)")):
    worst = max((c[key] - c["L"], N) for N, c in chain.items())
    print("  max gap vs %s: chain%d %s -> '≤ 1.0e-14' %s; 'same to 1e-14' %s"
          % (lab, worst[1], e(worst[0], 5), "VALID" if worst[0] <= lim else "UNDERSTATED",
             "VALID" if worst[0] <= F("1e-14") else "UNDERSTATED"))
    if worst[0] > lim:
        print("     safe 2-digit replacement '≤ %s'; safe 1-digit replacement 'same to %s'; 3-digit '%s'"
              % (up_sig(worst[0], 2)[1], up_sig(worst[0], 1)[1], up_sig(worst[0], 3)[1]))

# ---------------- catmix ----------------
print("\n== catmix (min). Displays on summary line %d: dual range '−0.04806944 … −0.04805591', gaps '1.65e-13 (100) … 1.5e-10 (800, verifier)'" % ln_cat)
cat = {}
for N in (100, 200, 400, 800):
    a = json.load(open(os.path.join(W2, "catmix%d_bound_1e-05_200_1e-07_band0.0685_0.0725_1e-06.json" % N)))
    p = json.load(open(os.path.join(W2, "catmix%d_primal.json" % N)))
    pa = F(p["exact_point_objective_enclosure"][1].strip("[]").split(",")[0].strip())
    cat[N] = dict(La=F(a["dual_bound"]), pa=pa)
snap = json.load(open(os.path.join(W2, "catmix800_primal_snap.json")))
cat[800]["pa"] = min(cat[800]["pa"], F(snap["exact_point_objective_enclosure"][1].strip("[]").split(",")[0].strip()))
vlogs = {100: os.path.join(CV, "catmix100_cfgB.log"), 200: os.path.join(CV, "catmix200_cfgA.log"),
         400: os.path.join(CR, "catmix400_final.log"), 800: os.path.join(CR, "catmix800_final.log")}
for N, path in vlogs.items():
    cat[N]["Lv"] = F([o for o in objs(path) if "dual_bound" in o][0]["dual_bound"])
# reviewer primal points: catmix100 Newton point (printed '%.20g' % float(exact J)); 400/800 DP policy points (floor(J*1e30))
nl = open(os.path.join(CV, "catmix100_newton.log")).read()
newton = nl.split("final double controls: exact J =")[1].split()[0]
cat[100]["pr"] = double_upper(newton)
for N in (400, 800):
    s = open(os.path.join(CR, "policy_exact_%d.log" % N)).read().split("(floor) = ")[1].split()[0]
    cat[N]["pr"] = F(int(s) + 1, 10 ** 30)
for N, c in cat.items():
    c["L"] = max(c["La"], c["Lv"])
    c["P"] = min(c["pa"], c.get("pr", c["pa"]))
    print("  catmix%-3d author L %s | verifier L %s | best primal upper %s | best gap %s (author-bound gap %s)"
          % (N, dec(c["La"], 21), dec(c["Lv"], 21), dec(c["P"], 21), e(c["P"] - c["L"], 5), e(c["P"] - c["La"], 4)))
for s, N in (("-0.04806944", 100), ("-0.04805591", 800)):
    print("  range end %s for catmix%d: <= author L %s, <= verifier L %s (margin to author L %s)"
          % (s, N, F(s) <= cat[N]["La"], F(s) <= cat[N]["Lv"], e(cat[N]["La"] - F(s))))
    assert F(s) <= cat[N]["La"] and F(s) <= cat[N]["Lv"]
print("  every catmix bound lies in [−0.04806944, −0.04805590]:",
      all(F("-0.04806944") <= c["La"] <= F("-0.0480559") for c in cat.values()))
g100 = cat[100]["P"] - cat[100]["Lv"]
g800 = cat[800]["P"] - cat[800]["Lv"]
g800a = cat[800]["pa"] - cat[800]["Lv"]
print("  catmix100 gap (verifier cfg B bound, Newton point) <= %s ; displayed 1.65e-13 %s (margin %s)"
      % (e(g100, 6), "VALID" if g100 <= F("1.65e-13") else "UNDERSTATED", e(F("1.65e-13") - g100, 2)))
print("     (vs authors' own primal the catmix100 gap would be %s, so 1.65e-13 depends on the reviewer's Newton point)"
      % e(cat[100]["pa"] - cat[100]["Lv"], 4))
print("  catmix800 gap (recheck bound, policy point) <= %s ; vs authors' snap point %s ; displayed 1.5e-10 %s"
      % (e(g800, 5), e(g800a, 5), "VALID" if max(g800, g800a) <= F("1.5e-10") else "UNDERSTATED"))
gaps = {N: c["P"] - c["L"] for N, c in cat.items()}
print("  best gaps 100..800 inside [1.65e-13, 1.5e-10]:",
      all(F("1.6e-13") <= g <= F("1.5e-10") for g in gaps.values()), {N: e(g, 3) for N, g in gaps.items()})
print("  primal sanity: every best primal >= its bound:", all(c["P"] >= c["L"] for c in cat.values()))

# ---------------- listed duals (context column, not our certificates) ----------------
print("\n== 'best listed dual' column (MINLPLib page values from bound-audit/pages, saved 2026-09-30)")
listed = {}
for n in ("chain50", "chain100", "chain200", "chain400", "catmix100", "catmix200", "catmix400", "catmix800"):
    t = re.sub(r"<[^>]+>", " ", open(os.path.join(R, "bound-audit/pages/%s.html" % n)).read())
    t = re.sub(r"\s+", " ", t)
    seg = t.split("Dual Bounds")[1].split("References")[0]
    vals = [F(x) for x in re.findall(r"(-?\d+\.\d+) \(", seg)]
    listed[n] = max(vals)
    print("  %-10s best listed dual %s" % (n, float(listed[n])))
for s, n in (("0.0826", "chain200"), ("0.1745", "chain50"), ("-0.0666", "catmix100"), ("-1.489", "catmix800")):
    print("  display %-8s for %-9s listed %-12s display <= listed (outward)? %s"
          % (s, n, float(listed[n]), F(s) <= listed[n]))

# ---------------- detailed documents with the five unsafe strings ----------------
print("\n== documents (.md/.tex, excluding logs/ and before/ snapshots) containing the five unsafe decimals")
unsafe = {"chain50 author/verifier": "5.072261493982863", "chain200 author/verifier": "5.068917341793162",
          "catmix200 author": "0.04805914560067171", "catmix100 verifier cfg B": "0.04806943203114456",
          "catmix800 recheck": "0.04805590147967565"}
dbl = {"5.072261493982863": chain[50]["L"], "5.068917341793162": chain[200]["L"],
       "0.04805914560067171": -cat[200]["La"], "0.04806943203114456": -cat[100]["Lv"], "0.04805590147967565": -cat[800]["Lv"]}
for lab, s in unsafe.items():
    sq = F(s) if not s.startswith("0.048") else -F(s)
    d = dbl[s] if not s.startswith("0.048") else -dbl[s]
    print("  %s %s%s: display - double = %s" % (lab, "" if not s.startswith("0.048") else "−", s, e(sq - d, 3)))
    rx = re.compile(r"(?<![\d.])" + re.escape(s) + r"(?!\d)")
    for root, dirs, files in os.walk(R):
        dirs[:] = [x for x in dirs if x not in ("logs", "before", ".git", "5b")]
        for fn in sorted(files):
            if not fn.endswith((".md", ".tex")):
                continue
            p = os.path.join(root, fn)
            for i, l in enumerate(open(p, errors="replace").read().split("\n")):
                if rx.search(l):
                    print("    %s:%d" % (os.path.relpath(p, R), i + 1))
assert not any(s in open(SUMMARY).read() for s in unsafe.values())
print("  none of the five strings occurs in open-instances-summary.md")

# ---------------- gap columns of the wave-2 note (detailed document) ----------------
print("\n== wave-2 note (open-instances-wave2/cops/report.md) gap columns vs exact gaps (absolute)")
note_gap = {"chain50": "9.4e-15", "chain100": "9.9e-15", "chain200": "9.0e-15", "chain400": "1.0e-14",
            "catmix100": "7.9e-12", "catmix200": "2.1e-11", "catmix400": "1.9e-10", "catmix800": "5.1e-10"}
for N in (50, 100, 200, 400):
    g = chain[N]["pd"] - chain[N]["L"]
    print("  chain%-3d note %s exact (double point vs binary64 L) <= %s -> %s"
          % (N, note_gap["chain%d" % N], e(g, 4), "ok" if g <= F(note_gap["chain%d" % N]) else "understated; safe " + up_sig(g, 2)[1]))
for N in (100, 200, 400, 800):
    # note pairs authors' bound with authors' primal (catmix800: the snap point)
    g = cat[N]["pa"] - cat[N]["La"]
    print("  catmix%-3d note %s exact (authors' primal vs authors' L) %s -> %s"
          % (N, note_gap["catmix%d" % N], e(g, 4), "ok" if g <= F(note_gap["catmix%d" % N]) else "understated; safe " + up_sig(g, 2)[1]))

# ---------------- bracket widths quoted in the reviews (detailed documents) ----------------
print("\n== bracket widths quoted in reviews (absolute), exact")
for lab, g, shown in (("catmix100 verification-report 1.65e-13 (cfg B, Newton)", cat[100]["P"] - cat[100]["Lv"], "1.65e-13"),
                      ("catmix100 verification-report 1.85e-13 (cfg B, authors' primal)", cat[100]["pa"] - cat[100]["Lv"], "1.85e-13"),
                      ("catmix400 catmix-recheck width 6.8e-11", cat[400]["pa"] - cat[400]["Lv"], "6.8e-11"),
                      ("catmix800 catmix-recheck width 1.48e-10 (policy point)", cat[800]["pr"] - cat[800]["Lv"], "1.48e-10"),
                      ("catmix800 catmix-recheck 1.49e-10 (snap point)", cat[800]["pa"] - cat[800]["Lv"], "1.49e-10")):
    sig = len(shown.split("e")[0].replace(".", ""))
    print("  %-62s exact %s -> %s" % (lab, e(g, 6), "ok" if g <= F(shown) else "understated; safe " + up_sig(g, sig)[1]))
