"""Summarize scan.jsonl as Markdown tables.  Usage: python summarize.py scan.jsonl instancedata.csv > summary.md"""
import csv
import json
import sys
from collections import Counter

recs = [json.loads(line) for line in open(sys.argv[1])]
meta = {r["name"]: r for r in csv.DictReader(open(sys.argv[2]), delimiter=";")}
ok = [r for r in recs if r["status"] == "ok"]
for r in ok:                                  # identical rows are stored once with a count
    r["rows"] = [q for q in r["rows"] for _ in range(q["count"])]

# Variants of condition (i).  Each maps a row record to its number of secant items.
VARIANTS = {
    "declared": lambda q: q["n_sec"],          # secant items with finite declared bounds
    "wide": lambda q: q["n_sec_inf"],          # ... or bounds from one round of inference
    "strict": lambda q: q["n_sec_strict"],     # wide, and the model bounds the term on its secant side
    "separable": lambda q: q["n_sec_sep"],     # strict, and the variable is in no multivariate term of that row
}


def is_eq(q):
    return q["sense"] == "E"


def applicable(q):
    if q["bounded"] == "no":
        return False
    return q["degenerate"] is False if is_eq(q) else q["can_be_tight"]


def bins(values, edges):
    c = Counter()
    for v in values:
        for lo, hi in edges:
            if lo <= v <= hi:
                c[(lo, hi)] += 1
                break
    return [(f"{lo}" if lo == hi else f"{lo}-{hi}" if hi < 10**9 else f">={lo}", c[(lo, hi)]) for lo, hi in edges]


def table(header, rows):
    print("| " + " | ".join(header) + " |")
    print("|" + "|".join("---" for _ in header) + "|")
    for row in rows:
        print("| " + " | ".join(str(x) for x in row) + " |")
    print()


print("### Files\n")
status = Counter(r["status"].split(":")[0] for r in recs)
table(["status", "files"], sorted(status.items()))
bad = [r for r in recs if r["status"] != "ok"]
if bad:
    print("Skipped files:\n")
    for r in bad:
        size = f" ({r['size_bytes'] / 1e6:.0f} MB)" if "size_bytes" in r else ""
        print(f"- `{r['name']}`{size}: {r['status']}")
    print()

print("### Univariate additive terms (per row and variable)\n")
tc = Counter()
for r in ok:
    tc.update(r["term_counts"])
table(["curvature on the variable's interval", "terms", "instances"],
      [(k, tc[k], sum(1 for r in ok if r["term_counts"].get(k))) for k in sorted(tc) if tc[k]])
table(["instances with", "count"], [
    ("any secant variable, declared bounds", sum(1 for r in ok if r["n_secant_vars"])),
    ("any secant variable, declared or inferred bounds",
     sum(1 for r in ok if r["n_secant_vars"] + r["n_secant_vars_inferred_bounds"])),
    ("any strict secant variable", sum(1 for r in ok if r["n_secant_vars_strict"])),
    ("any separable secant variable", sum(1 for r in ok if r["n_secant_vars_separable"])),
    ("binary variables with a curved term (excluded)", sum(1 for r in ok if r["n_secant_vars_binary_excluded"])),
])

print("### Funnel\n")
rows = []
for kind, pick in (("equality", is_eq), ("inequality", lambda q: not is_eq(q))):
    for vname, nsec in VARIANTS.items():
        cand = [(r["name"], q) for r in ok for q in r["rows"] if pick(q) and nsec(q) >= 2]
        bnd = [(n, q) for n, q in cand if q["bounded"] != "no"]
        decl = [(n, q) for n, q in bnd if q["bounded"] == "declared"]
        app = [(n, q) for n, q in bnd if applicable(q)]
        extra = ""
        if kind == "equality":
            d = Counter(str(q["degenerate"]) for _, q in bnd)
            extra = f"degenerate {d['True']}, unknown {d['unknown']}, infeasible-by-bounds {d['infeasible']}"
        else:
            extra = f"cannot be tight {sum(1 for _, q in bnd if not q['can_be_tight'])}"
        rows.append((kind, vname, f"{len(cand)} / {len({n for n, _ in cand})}",
                     f"{len(bnd)} / {len({n for n, _ in bnd})}", f"{len(decl)} / {len({n for n, _ in decl})}",
                     f"{len(app)} / {len({n for n, _ in app})}", extra))
table(["row kind", "variant of (i)", "(i): rows / instances", "(i)+(ii)", "of which all bounds declared",
       "applicable (i)+(ii)+(iii)", "dropped at (iii)"], rows)

for vname, nsec in VARIANTS.items():
    either = {r["name"] for r in ok for q in r["rows"] if nsec(q) >= 2 and applicable(q)}
    print(f"- variant `{vname}`: {len(either)} instances have at least one applicable row of either kind.")
print()

SIZE_EDGES = [(2, 2), (3, 3), (4, 5), (6, 10), (11, 25), (26, 100), (101, 10**9)]
SEC_EDGES = [(2, 2), (3, 3), (4, 5), (6, 10), (11, 25), (26, 10**9)]
for vname, nsec in VARIANTS.items():
    print(f"### Applicable rows, variant `{vname}`\n")
    eq = [q for r in ok for q in r["rows"] if is_eq(q) and nsec(q) >= 2 and applicable(q)]
    iq = [q for r in ok for q in r["rows"] if not is_eq(q) and nsec(q) >= 2 and applicable(q)]
    a, b = bins([q["size"] for q in eq], SIZE_EDGES), bins([q["size"] for q in iq], SIZE_EDGES)
    table(["row size (nonzeros)", "equality rows", "inequality rows"], [(x[0], x[1], y[1]) for x, y in zip(a, b)])
    a, b = bins([nsec(q) for q in eq], SEC_EDGES), bins([nsec(q) for q in iq], SEC_EDGES)
    table(["secant items in row", "equality rows", "inequality rows"], [(x[0], x[1], y[1]) for x, y in zip(a, b)])
    frac = Counter()
    for q in eq + iq:
        frac["all items secant" if nsec(q) == q["n_items"] else "some items without a term"] += 1
    ew = [q for q in eq if q["equal_widths"]]
    esw = [q for q in eq if q["equal_secant_widths"]]
    insts_ew = {r["name"] for r in ok for q in r["rows"]
                if is_eq(q) and nsec(q) >= 2 and applicable(q) and q["equal_widths"]}
    print(f"- applicable equality rows with equal widths over all items (Theorem 2 applies exactly): "
          f"{len(ew)} rows in {len(insts_ew)} instances ({', '.join(sorted(insts_ew)[:30])}"
          f"{', ...' if len(insts_ew) > 30 else ''}).")
    print(f"- applicable equality rows whose secant items alone have equal widths: {len(esw)}.")
    print(f"- applicable rows with integer or binary items: {sum(1 for q in eq + iq if q['n_int'])} of {len(eq + iq)}.")
    print(f"- {dict(frac)}.")
    print()

def ranking(nsec):
    top = []
    for r in ok:
        qs = [q for q in r["rows"] if nsec(q) >= 2 and applicable(q)]
        if qs:
            e = sum(1 for q in qs if is_eq(q))
            ew = sum(1 for q in qs if is_eq(q) and q["equal_widths"])
            top.append((len(qs), e, len(qs) - e, ew, r))
    top.sort(key=lambda t: (-t[0], t[4]["name"]))
    return top


for vname in ("separable", "strict", "declared"):
    print(f"### Top 40 instances by applicable rows (variant `{vname}`)\n")
    top = ranking(VARIANTS[vname])
    out = []
    for n, e, i, ew, r in top[:40]:
        m = meta.get(r["name"], {})
        out.append((f"`{r['name']}`", n, e, i, ew, r["nvars"], r["nrows"], m.get("probtype", "?"),
                    m.get("convex", "?"), m.get("primalbound", "?"), m.get("dualbound", "?")))
    table(["instance", "applicable rows", "equality", "inequality", "eq. with equal widths", "vars", "rows",
           "type", "convex", "primal bound", "dual bound"], out)
    print(f"### Instances with applicable rows by problem type and convexity (variant `{vname}`)\n")
    c = Counter()
    for n, e, i, ew, r in top:
        m = meta.get(r["name"], {})
        c[(m.get("probtype", "?"), m.get("convex", "?") or "unknown")] += 1
    table(["type", "convex", "instances"], [(*k, v) for k, v in sorted(c.items())])
    if vname != "declared":
        eqi = [f"`{r['name']}` ({e})" for n, e, i, ew, r in top if e]
        print(f"All {len(eqi)} instances with applicable equality rows (rows in parentheses): {', '.join(eqi)}.\n")

print("### Open instances (variant `separable`, any applicable row)\n")
openi = []
for r in ok:
    qs = [q for q in r["rows"] if q["n_sec_sep"] >= 2 and applicable(q)]
    m = meta.get(r["name"], {})
    try:
        p, d = float(m.get("primalbound", "nan")), float(m.get("dualbound", "nan"))
        gap = abs(p - d) / max(abs(p), abs(d), 1e-9)
    except ValueError:
        continue
    if qs and gap > 1e-4:
        openi.append((f"`{r['name']}`", len(qs), sum(1 for q in qs if is_eq(q)), m.get("probtype"), m.get("convex"), m.get("primalbound"),
                      m.get("dualbound"), f"{100 * gap:.2f}%"))
table(["instance", "applicable rows", "of which equality", "type", "convex", "primal bound", "dual bound", "gap"],
      openi)
