"""Audit of link_detect.detect on the 48 instances: exponent sets, bounds, types, sources of the exponents."""
import sys, os, math, collections
from pathlib import Path
D = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(D)); sys.path.insert(0, str(D.parent / "univariate_envelopes"))
from uenv.osil import read_osil
import link_detect

def times_nodes(t, out):
    if t[0] in ("num", "var"): return
    if t[0] == "times":
        vs = [c[1] for c in t[1:] if c[0] == "var"]
        if len(vs) != len(set(vs)): out.append(t)
    for c in t[1:]: times_nodes(c, out)

def short(t, d=0):
    if t[0] == "num": return repr(t[1])
    if t[0] == "var": return f"x{t[1]}"
    if d > 2: return t[0] + "(..)"
    return t[0] + "(" + ",".join(short(c, d + 1) for c in t[1:]) + ")"

for name in open(D / "link_instances.txt").read().split():
    inst = read_osil(os.path.expanduser(f"~/.cache/minlplib/minlplib/osil/{name}.osil"))
    trig, pw = link_detect.detect(inst)
    sets = collections.Counter(tuple(p) for p in pw.values())
    types = collections.Counter(inst.var_type[v] for v in pw)
    lb0 = sum(1 for v in pw if inst.var_lb[v] == 0)
    negexp = sum(1 for v, p in pw.items() if min(p) < 0)
    nonint = sum(1 for v, p in pw.items() if any(q != int(q) for q in p))
    maxub = max((inst.var_ub[v] for v in pw), default=None)
    maxt = max((max(inst.var_ub[v] ** q if q > 0 else inst.var_lb[v] ** q for q in p) for v, p in pw.items()), default=None)
    tn = []
    for r in inst.rows:
        if r["nl"] is not None: times_nodes(r["nl"], tn)
    mixed = [t for t in tn if len(t) - 1 > sum(1 for c in t[1:] if c[0] == "var") or len({c[1] for c in t[1:] if c[0] == "var"}) > 1]
    print(f"{name:18s} trig {len(trig):3d} pwvars {len(pw):3d} sets {dict(sets)} types {dict(types)} lb0 {lb0} negexp {negexp} nonint {nonint} max ub {maxub} max t-bound {maxt}")
    if tn: print("    repeated-variable times nodes:", len(tn), "with other factors:", len(mixed), "e.g.", short(tn[0]), "|", short(mixed[0]) if mixed else "")
    trig_lb = [(inst.var_lb[v], inst.var_ub[v]) for v in trig][:2]
    if trig: print("    trig var bounds e.g.", trig_lb)
