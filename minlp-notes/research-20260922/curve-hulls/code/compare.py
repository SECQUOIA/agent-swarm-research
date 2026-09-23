"""Markdown table from results/*_<tl>.out and listed_bounds.json.  python compare.py [tl]"""
import glob, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
tl = sys.argv[1] if len(sys.argv) > 1 else "1800"
L = json.load(open(os.path.join(HERE, "listed_bounds.json")))
R = {}
for f in glob.glob(os.path.join(HERE, "results", f"*_{tl}.out")):
    for line in open(f):
        if line.startswith("{"):
            d = json.loads(line)
            R.setdefault(d["name"], {})[d["mode"]] = d
fmt = lambda v: "-" if v is None else f"{v:.6g}"
print("| instance | curves (vars) | root cuts | root bound orig / sub / cuts | final dual orig | sub | cuts | soc | listed best dual (solver) | best primal | cuts > listed? |")
print("|---|---|---|---|---|---|---|---|---|---|---|")
for name in sorted(R, key=lambda n: list(L).index(n) if n in L else 999):
    r = R[name]
    lb = L.get(name, {})
    sense = next(iter(r.values()))["sense"]
    duals = lb.get("duals", {})
    best = (max if sense == "min" else min)(duals.items(), key=lambda kv: kv[1][0]) if duals else None
    g = lambda m, k="dual": r[m][k] if m in r else None
    root = lambda m: r[m]["root"]["dual"] if m in r and "root" in r[m] else None
    c = r.get("cuts", {})
    better = None
    if c.get("dual") is not None and best:
        tol = 1e-6 * max(1.0, abs(best[1][0]))  # strict improvement beyond a relative 1e-6
        better = (c["dual"] > best[1][0] + tol) if sense == "min" else (c["dual"] < best[1][0] - tol)
    print(f"| {name} | {c.get('nsel', r.get('sub', {}).get('nsel', '-'))} | {c.get('ncuts', '-')} | "
          f"{fmt(root('orig'))} / {fmt(root('sub'))} / {fmt(root('cuts'))} | {fmt(g('orig'))} | {fmt(g('sub'))} | "
          f"{fmt(g('cuts'))} | {fmt(g('soc'))} | {fmt(best[1][0]) + ' (' + best[0] + ')' if best else '-'} | "
          f"{fmt(lb.get('best_primal'))} | {'yes' if better else ('no' if better is not None else '-')} |")
