"""Recompute the root Lagrangian bound exactly from the authors' stored multipliers
and check it against the MINLPLib p1 point.

    python3 run_root.py powerflow0030p
"""
import json
import os
import sys
import time
from fractions import Fraction as Fr

import mpmath as mp
import numpy as np

import pfv

mp.mp.dps = 50
name = sys.argv[1]
W3 = os.path.join(pfv.HERE, "..", "..", "..", "open-instances-wave3")
t0 = time.time()
M = pfv.build(name)
cert = json.load(open(os.path.join(W3, "logs", name + ".sdpcert.json")))
print("variant:", cert["variant"], "| stored bound", repr(cert["bound"]), "| eps", cert["eps"], "| sdp_numeric", cert["sdp_numeric"])
from collections import Counter
print("relaxed rows:", len(M["rows"]), Counter(r["kind"] for r in M["rows"]), "| raw entries:", len(cert["raw"]))
print("boxes:", len(M["box"]), "| boxes with an open side:",
      sum(1 for lo, hi in M["box"].values() if lo is None or hi is None))
res = pfv.lagrangian(M, cert["raw"])
A = res["A"]
An = np.array([[float(v) for v in r] for r in A])
ev = np.linalg.eigvalsh(An)
print("float eigenvalues of A(w): smallest", ev[:4], "largest", ev[-1])
t1 = time.time()
ok, piv, zeros = pfv.ldl_psd(A)
print(f"exact LDL^T: psd={ok}, positive pivots={len(piv)}, zero pivots={zeros}, min pivot={float(min(piv)):.3e}, {time.time()-t1:.1f}s")
assert ok
L = res["const"] + res["inner"]
print("const", float(res["const"]), "inner", float(res["inner"]))
print("L =", repr(float(L)), "| L - stored float bound =", float(L - Fr(cert["bound"])))
be = Fr(cert["bound_exact"])
print("L == bound_exact:", L == be, "| L - bound_exact =", float(L - be))
print("L (40 digits):", mp.nstr(mp.mpf(L.numerator) / L.denominator, 40))

# ------------------------------------------------ p1 point at 50 digits
I = M["I"]
names = I["names"]
sol = {}
for line in open(os.path.join(W3, "sol", name + ".p1.sol")):
    p = line.split()
    if len(p) == 2:
        sol[p[0]] = p[1]
missing = [nm for nm in names if nm not in sol]
print("p1: values", len(sol), "missing OSIL vars (set to 0):", missing)
x = [mp.mpf(sol.get(nm, "0")) for nm in names]
fns = {"sin": mp.sin, "cos": mp.cos}
o = I["obj"]
obj = mp.mpf(o["constant"]) + sum(mp.mpf(c) * x[j] for j, c in o["lin"].items()) \
    + sum(mp.mpf(c) * x[i] * x[j] for i, j, c in o["quad"])
viol = mp.mpf(0)
worst = None
for c in I["cons"]:
    v = pfv.osilx.ev_row(c, x, mp.mpf, fns)
    lb = None if pfv.osilx.isinf(c["lb"]) else mp.mpf(c["lb"])
    ub = None if pfv.osilx.isinf(c["ub"]) else mp.mpf(c["ub"])
    d = max([mp.mpf(0)] + ([lb - v] if lb is not None else []) + ([v - ub] if ub is not None else []))
    if d > viol:
        viol, worst = d, c["name"]
print("obj(p1) =", mp.nstr(obj, 20), "| max row violation", mp.nstr(viol, 3), "at", worst,
      "| objvar in sol:", sol.get("objvar"))
Lm = mp.mpf(L.numerator) / L.denominator
print("obj(p1) - L =", mp.nstr(obj - Lm, 6), "relative", mp.nstr((obj - Lm) / obj, 3), "| L <= obj(p1):", Lm <= obj)

# Lagrangian at the mapped p1 point (checks the minimization code: L <= Lagr(z))
if M["polar"]:
    V, TH = M["vmap"]["V"], M["vmap"]["TH"]
    X = []
    for v, t in zip(V, TH):
        X += [x[v] * mp.cos(x[t]), x[v] * mp.sin(x[t])]
else:
    X = [x[j] for j in M["vmap"]["X"]]
w = res["w"]
lag = obj
for k, r in enumerate(M["rows"]):
    if w[k] == 0 and r["kind"] != "flow":
        continue
    h = sum(mp.mpf(c.numerator) / c.denominator * x[j] for j, c in r["lin"].items()) \
        + sum(mp.mpf(c.numerator) / c.denominator * x[j] ** 2 for j, c in r["qy"].items()) \
        + sum(mp.mpf(c.numerator) / c.denominator * X[i] * X[j] for (i, j), c in r["Q"].items())
    rw = cert["raw"][k]
    wk = mp.mpf(w[k].numerator) / w[k].denominator
    if rw[0] == "eq":
        lag += wk * (h - mp.mpf(r["lb"].numerator) / r["lb"].denominator)
    else:
        vp = max(0.0, rw[1]) if rw[1] is not None else 0.0
        vm = max(0.0, rw[2]) if rw[2] is not None else 0.0
        if vp:
            lag += mp.mpf(vp) * (h - mp.mpf(r["ub"].numerator) / r["ub"].denominator)
        if vm:
            lag += mp.mpf(vm) * (mp.mpf(r["lb"].numerator) / r["lb"].denominator - h)
print("Lagrangian at mapped p1 =", mp.nstr(lag, 20), "| L <= Lagr(p1):", Lm <= lag,
      "| Lagr(p1) - L =", mp.nstr(lag - Lm, 6))
print(f"total {time.time()-t0:.1f}s")
