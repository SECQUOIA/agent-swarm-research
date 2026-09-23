"""Fetch MINLPLib pages: best primal bound (bold) with its sol file id, and all dual bounds by solver.
python listed.py <names...>  -> listed_bounds.json (merged)"""
import json, os, re, sys, urllib.request, datetime
HERE = os.path.dirname(os.path.abspath(__file__))
out_f = os.path.join(HERE, "listed_bounds.json")
out = json.load(open(out_f)) if os.path.exists(out_f) else {}
for name in sys.argv[1:]:
    html = urllib.request.urlopen(f"https://www.minlplib.org/{name}.html", timeout=60).read().decode()
    rowp = re.search(r"Primal Bounds.*?</TR>", html, re.S).group(0)
    rowd = re.search(r"Dual Bounds.*?</TR>", html, re.S).group(0)
    prim = re.findall(r'<div title="Added on ([^"]*)">(<B>)?([-+0-9.eE]+)(?:</B>)? <A href=[^>]*\.(p\d+)\.html', rowp)
    best = [p for p in prim if p[1]]
    duals = re.findall(r'<div title="Last updated: ([^"]*)">(?:<B>)?([-+0-9.eE]+)(?:</B>)? \(([^)]*)\)', rowd)
    sense = "max" if re.search(r"Objective Sense.*?max", html, re.S | re.I) and "maximize" in html.lower() else "min"
    out[name] = {"fetched": str(datetime.date.today()),
                 "best_primal": float(best[0][2]) if best else None, "best_point": best[0][3] if best else None,
                 "duals": {s: [float(v), d] for d, v, s in duals}}
    print(name, out[name], flush=True)
json.dump(out, open(out_f, "w"), indent=1)
