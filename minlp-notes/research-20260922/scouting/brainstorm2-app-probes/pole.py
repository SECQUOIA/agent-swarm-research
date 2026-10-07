from pathlib import Path as _CleanupPath
_NOTES_ROOT = _CleanupPath(__file__).resolve().parent.joinpath('../../..').resolve()

import sys, re, mpmath
sys.path.insert(0,(str(_NOTES_ROOT) + '/research-20260922/benchmark-observations/code'))
import pyscipopt as ps
from osil_eval import Model, mp_backend
mpmath.mp.dps = 60; B = mp_backend(60)
name = sys.argv[1]
path = f"{_CleanupPath.home()}/.cache/minlplib/minlplib/osil/{name}.osil"
import os
lst = f"run_{name}/{name}.lst"; fixb = {}
if os.path.exists(lst):
    for line in open(lst):
        mm = re.match(r'---- VAR (b\d+)\s+(\S+)\s+(\S+)', line)
        if mm: fixb[mm.group(1)] = 0.0 if mm.group(3) == '.' else float(mm.group(3))
m = ps.Model(); m.hideOutput(); m.readProblem(path)
for v in m.getVars():
    if v.name in fixb: m.fixVar(v, fixb[v.name])
m.setParam("limits/time", float(sys.argv[2]) if len(sys.argv)>2 else 60); m.optimize()
sol = m.getBestSol(); val = {v.name: sol[v] for v in m.getVars()}
print("fixed binaries from GAMS listing:", fixb)
print("SCIP 60s incumbent", m.getObjVal(), "dual", m.getDualbound())
M = Model(path); idx = {n: i for i, n in enumerate(M.vnames)}
print("names sample", M.vnames[:3], M.vnames[36:39])
x = [mpmath.mpf(repr(val.get(n, 0.0))) for n in M.vnames]
for j, t in enumerate(M.vtype):
    if t in "BI": x[j] = mpmath.mpf(round(float(x[j])))
print("incumbent obj (mp)", M.objective(x, B), "viol", {k: float(v[0]) for k, v in M.check(x, B).items()})
# parse gms for LMTD rows, area rows, and dT upper-bound rows
g = open(f"{name}.gms").read()
body = {e: ' '.join(b.split()) for e, b in re.findall(r'^(e\d+)\.\.(.*?);', g, re.M | re.S)}
lm, ar = [], []
for e, b in body.items():
    mm = re.match(r'-\((.*?)\)/log\((.*?)\) \+ (x\d+) =E= 0$', b)
    if mm:
        num = mm.group(1)
        a = re.match(r'^(x\d+) - (x\d+)$', num)
        if a: lm.append((mm.group(3), a.group(1), a.group(2), None))
        else:
            a = re.match(r'^-([\d.]+) \+ (x\d+)$', num); c = re.search(r'log\(([\d.]+)\*x', b).group(1)
            lm.append((mm.group(3), a.group(2), a.group(1), c))
    mm = re.match(r'-([\d.]+)\*(x\d+)/\(0\.01 \+ (x\d+)\) \+ (x\d+) =E= 0$', b)
    if mm: ar.append((mm.group(4), mm.group(1), mm.group(2), mm.group(3)))
print(len(lm), "LMTD rows,", len(ar), "area rows")
def ubound(v):
    """max value of variable v allowed by <= rows where v has coefficient +1, others fixed."""
    j = idx[v]; best = mpmath.mpf(M.vub[j]) if M.vub[j] != "INF" else mpmath.inf
    for r in range(M.m):
        c = M.lin[r].get(j)
        if c is None or r in M.nl or M.quad.get(r): continue
        c = mpmath.mpf(c); x0 = x[j]; x[j] = mpmath.mpf(0); a = M.row_value(r, x, B); x[j] = x0
        if M.cub[r] != "INF" and c > 0: best = min(best, (mpmath.mpf(M.cub[r]) - a) / c)
        if M.clb[r] != "-INF" and c < 0: best = min(best, (mpmath.mpf(M.clb[r]) - a) / c)
    return best
eps = mpmath.mpf('1e-6'); tiny = mpmath.mpf(sys.argv[3] if len(sys.argv)>3 else '1e-30')
# process-process LMTD rows: pairs (a,b) with L=(a-b)/log(a/(1e-6+b)); pole at a=b+1e-6
activeL = {L for Av, k, Q, L in ar if x[idx[Q]] > 1e-9}
pairs = [(a, b) for L, a, b, c in lm if c is None and L in activeL]
print("active LMTD rows", sorted(activeL))
succ = {a: b for a, b in pairs}; preds = {b for a, b in pairs}
heads = [a for a, b in pairs if a not in preds]
d = eps + tiny
for h in heads:
    ch = [h]
    while ch[-1] in succ: ch.append(succ[ch[-1]])
    k = len(ch) - 1
    base = min(ubound(v) - (k - i) * d for i, v in enumerate(ch))
    lbs = [mpmath.mpf(M.vlb[idx[v]]) for v in ch]
    if base < lbs[-1]:
        print("skip chain", ch); continue
    for i, v in enumerate(ch): x[idx[v]] = base + (k - i) * d
    print("chain", ch, "base", mpmath.nstr(base, 8))
for L, a, b, c in lm:
    if c is None:
        A, Bv = x[idx[a]], x[idx[b]]
        x[idx[L]] = (A - Bv) / mpmath.log(A / (eps + Bv))
    else:
        pole = 1 / mpmath.mpf(c); U = ubound(a)
        if L in activeL and pole + tiny <= U and pole >= 10: x[idx[a]] = pole + tiny
        v = x[idx[a]]; x[idx[L]] = (v - mpmath.mpf(b)) / mpmath.log(mpmath.mpf(c) * v)
for Av, k, Q, L in ar:
    x[idx[Av]] = mpmath.mpf(k) * x[idx[Q]] / (mpmath.mpf('0.01') + x[idx[L]])
# recompute objective variable from its defining row (objvar appears linearly in last row)
ov = idx.get('objvar')
rs = [r for r in range(M.m) if ov is not None and ov in M.lin[r]]
if rs:
    r = rs[0]; x[ov] = mpmath.mpf(0); a = M.row_value(r, x, B); x[ov] = (mpmath.mpf(M.clb[r]) - a) / mpmath.mpf(M.lin[r][ov])
res = M.check(x, B)
print("pole point objective", mpmath.nstr(M.objective(x, B), 12), "viol", {k: (mpmath.nstr(v[0], 3), v[1]) for k, v in res.items()})
print("min dT gap check", [mpmath.nstr(x[idx[a]] - x[idx[b]], 5) for L, a, b, c in lm if c is None][:4])
from osil_eval import FloatB
xf = [float(v) for v in x]
print("float eval objective", M.objective(xf, FloatB), "viol", {k: (float(v[0]), v[1]) for k, v in M.check(xf, FloatB).items()})
print("areas", [(Av, mpmath.nstr(x[idx[Av]], 4)) for Av, k, Q, L in ar if x[idx[Q]] > 1e-9])
