"""Write sections/B-tables.tex from the archived campaign-3 records (standard library only)."""
import json, collections, math
from fractions import Fraction
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
EXP = ROOT / "experiments"
def load(p): return [json.loads(l) for l in open(p)]
def tex(name): return "\\code{" + name.replace("_", "\\_") + "}"
def fmt(x):
    if x is None: return "--"
    if abs(x) >= 1000: return f"{x:.0f}"
    return f"{x:.4g}"
out = []
# Part B per model
recs = load(EXP / "v3/runs/partB/records.jsonl")
sel = json.load(open(EXP / "v3/scan/partB-selection.json"))["selected"]
by = collections.defaultdict(dict)
for r in recs: by[(r["name"], r["phase"], r["seed"])][r["mode"]] = r
out.append(r"""\begin{table}[ht]
\centering\scriptsize
\caption{Campaign 3, Part B: structure-selected models. Root dual bounds
(one node) for the baseline and the raised-limit diagnostic mode, and
seed-0 full runs: status (o optimal, g gap limit, t time limit), seconds and
cuts for the baseline and mode \code{all}.}\label{tab:partB}
\begin{tabular}{@{}lrrrrr@{}}
\toprule
Model & Root bound, baseline & Root bound, \code{all-diag} & Baseline & \code{all} & Cuts\\
\midrule""")
for e in sel:
    n = e["name"]
    rb = by[(n, "root", 0)]["baseline"]["dual"]; rd = by[(n, "root", 0)]["all-diag"]["dual"]
    fb = by[(n, "full", 0)]["baseline"]; fa = by[(n, "full", 0)]["all"]
    st = lambda r: {"optimal": "o", "gaplimit": "g", "timelimit": "t"}.get(r["status"], r["status"])
    out.append(f"{tex(n)} & {fmt(rb)} & {fmt(rd)} & {st(fb)} {fb['total_seconds']:.1f} & {st(fa)} {fa['total_seconds']:.1f} & {len(fa['cuts'] or [])}\\\\")
out.append(r"""\bottomrule
\end{tabular}
\end{table}
""")
# model lists for Part A
hs = json.load(open(ROOT.parent / "research-20261003-convexification/experiments/holdout-selection.json"))["selected"]
names = [h["name"] if isinstance(h, dict) else h for h in hs]
out.append("\\paragraph{Models of campaigns 2 and 3 (Part A).} " + ", ".join(tex(n) for n in names) + ".\n")
# mechanism per instance
orig = collections.defaultdict(dict); diag = collections.defaultdict(dict)
for r in load(EXP / "v3/runs/partC/records.jsonl"): orig[(r["name"], r["phase"])][r["mode"]] = r
for r in load(EXP / "v3d/runs/partC-rowdir/records.jsonl"): diag[(r["name"], r["phase"])][r["mode"]] = r
cases = {json.loads(p.read_text())["name"]: json.loads(p.read_text()) for p in (EXP / "v3/runs/partC/cases").glob("*.json")}
out.append(r"""\begin{table}[ht]
\centering\scriptsize
\caption{The path family: optimum, baseline root bound, fraction of the root
gap closed by the frozen separator and by the row-direction diagnostic with
wide limits, and full runs (status, nodes, seconds) for the baseline, the
frozen separator and the diagnostic.}\label{tab:mechanism-detail}
\begin{tabular}{@{}rrrrrrlll@{}}
\toprule
$n$ & seed & Optimum & Root, baseline & Closed, frozen & Closed, diag. & Baseline & Frozen & Diagnostic\\
\midrule""")
def rd(r): return r["root_dual"] if r.get("root_dual") is not None else r["dual"]
names = sorted(cases, key=lambda n: (cases[n]["mechanism"]["n"], cases[n]["mechanism"]["seed"]))
for n in names:
    c = cases[n]; o = float(Fraction(c["known_optimum_exact"]))
    b = rd(orig[(n, "root")]["baseline"]); m = rd(orig[(n, "root")]["all-diag-mech"])
    db = rd(diag[(n, "root")]["baseline"]); w = rd(diag[(n, "root")]["all-diag-mech-wide"])
    f = lambda r: f"{ {'optimal':'o','gaplimit':'g','timelimit':'t'}[r['status']] } {r['nodes']} {r['total_seconds']:.0f}"
    out.append(f"{c['mechanism']['n']} & {c['mechanism']['seed']} & {o:.5f} & {b:.3f} & {(m-b)/(o-b):.2f} & {(w-db)/(o-db):.2f} & {f(orig[(n,'full')]['baseline'])} & {f(orig[(n,'full')]['all-diag-mech'])} & {f(diag[(n,'full')]['all-diag-mech-wide'])}\\\\")
out.append(r"""\bottomrule
\end{tabular}
\end{table}
""")
(ROOT / "sections/B-tables.tex").write_text("\n".join(out) + "\n")
print("written", len(out))
