"""BARON (GAMS 54) on a MINLPLib OSiL instance, native or with the power links of link_detect.py.
python baron_link.py <instance> {native|linked} [tl]"""
import json, math, os, shutil, subprocess, sys, tempfile, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "univariate_envelopes"))
from uenv.osil import read_osil
import link_detect


def g(t, v):
    op = t[0]
    if op == "num": return repr(float(t[1]))
    if op == "var": return v[t[1]]
    k = [g(c, v) for c in t[1:]]
    if op == "sum": return "(" + " + ".join(k) + ")"
    if op == "negate": return "(-" + k[0] + ")"
    if op == "times": return "(" + "*".join(k) + ")"
    if op == "divide": return "(" + k[0] + "/" + k[1] + ")"
    if op == "square": return "sqr(" + k[0] + ")"
    if op == "power":
        e = float(t[2][1]) if t[2][0] == "num" else None
        if e is not None and e == int(e): return f"power({k[0]},{int(e)})"
        return "(" + k[0] + ")**(" + k[1] + ")"
    if op == "sqrt": return "sqrt(" + k[0] + ")"
    if op in ("exp", "log"): return op + "(" + k[0] + ")"
    raise NotImplementedError(op)


name, mode = sys.argv[1], sys.argv[2]
tl = float(sys.argv[3]) if len(sys.argv) > 3 else 60
inst = read_osil(os.path.expanduser(f"~/.cache/minlplib/minlplib/osil/{name}.osil"))
n = len(inst.var_lb)
v = [f"x{i}" for i in range(n)]
lines = ["Variables " + ", ".join(v) + ", objvar;"]
bins = [v[i] for i in range(n) if inst.var_type[i] == "B"]; ints = [v[i] for i in range(n) if inst.var_type[i] == "I"]
if bins: lines.append("Binary Variables " + ", ".join(bins) + ";")
if ints: lines.append("Integer Variables " + ", ".join(ints) + ";")
for i in range(n):
    if inst.var_type[i] != "B":
        if math.isfinite(inst.var_lb[i]): lines.append(f"{v[i]}.lo = {inst.var_lb[i]!r};")
        if math.isfinite(inst.var_ub[i]): lines.append(f"{v[i]}.up = {inst.var_ub[i]!r};")
eqs = []
def body(r):
    parts = [f"({c!r})*{v[i]}" for i, c in r["lin"].items()] + [f"({c!r})*{v[i]}*{v[j]}" for i, j, c in r["quad"]]
    if r["nl"] is not None: parts.append(g(r["nl"], v))
    return " + ".join(parts) if parts else "0"
for ridx, r in enumerate(inst.rows):
    b = body(r)
    if ridx == 0:
        eqs.append(("defobj", f"objvar =e= {b} + ({inst.obj_const!r})")); continue
    if r["lb"] == r["ub"]: eqs.append((f"e{ridx}", f"{b} =e= {r['lb']!r}"))
    else:
        if math.isfinite(r["lb"]): eqs.append((f"l{ridx}", f"{b} =g= {r['lb']!r}"))
        if math.isfinite(r["ub"]): eqs.append((f"u{ridx}", f"{b} =l= {r['ub']!r}"))
trig, pw = link_detect.detect(inst)
extra_vars, nlinks = [], 0
if mode == "linked":
    for vi, ps_ in pw.items():
        lo, hi = inst.var_lb[vi], inst.var_ub[vi]
        ref = min(ps_, key=abs); tv = {}
        for p in ps_:
            a, b = sorted((lo ** p, hi ** p)); tv[p] = f"t{vi}_{str(p).replace('.', 'p').replace('-', 'm')}"
            extra_vars.append((tv[p], a, b))
            eqs.append((f"d{tv[p]}", f"{tv[p]} =e= {g(('power', ('var', vi), ('num', p)), v)}"))
        for p in ps_:
            if p != ref:
                eqs.append((f"k{tv[p]}", f"{tv[p]} =e= ({tv[ref]})**({p / ref!r})")); nlinks += 1
if extra_vars:
    lines.append("Variables " + ", ".join(t for t, _, _ in extra_vars) + ";")
    for t, a, b in extra_vars: lines.append(f"{t}.lo = {a!r}; {t}.up = {b!r};")
lines.append("Equations " + ", ".join(e for e, _ in eqs) + ";")
lines += [f"{e}.. {b};" for e, b in eqs]
sense = "minimizing" if inst.obj_sense == "min" else "maximizing"
lines += ["Model m /all/;", f"option minlp=baron, reslim={tl!r}, optcr=1e-4, optca=0, threads=1;",
          f"solve m using minlp {sense} objvar;",
          "file res /res.txt/; put res; res.nd=10; res.nw=24;",
          "put m.modelstat, m.solvestat, m.objval, m.objest, m.nodusd, m.resusd /;"]
work = Path(tempfile.mkdtemp(prefix="bl-"))
try:
    (work / "model.gms").write_text("\n".join(lines) + "\n")
    t0 = time.time()
    subprocess.run(["gams", "model.gms", "lo=0"], cwd=work, check=False, timeout=tl + 300, capture_output=True)
    if not (work / "res.txt").exists():
        lst = (work / "model.lst").read_text(errors="ignore")
        err = [l for l in lst.splitlines() if "***" in l][:5]
        print(json.dumps({"name": name, "mode": mode, "error": err})); sys.exit(0)
    ms, ss, objval, objest, nodes, _ = (float(t) for t in (work / "res.txt").read_text().split("\n")[0].split())
    print(json.dumps({"name": name, "solver": "baron", "mode": mode, "links": nlinks, "sense": inst.obj_sense,
                      "modelstat": ms, "solvestat": ss, "primal": objval, "dual": objest, "nodes": nodes, "time": time.time() - t0}))
finally:
    shutil.rmtree(work, ignore_errors=True)
