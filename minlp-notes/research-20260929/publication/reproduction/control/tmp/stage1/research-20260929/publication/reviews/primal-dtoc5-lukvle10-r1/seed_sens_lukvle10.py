"""Reviewer's numerical (not rigorous) spot check of the track's seed-sensitivity illustration.
Seeds: p5's 15-digit values, and the stored KKT point's x1, x2 rounded to D decimals.
Forward propagation of the rows at 1500 digits."""
import json, os
from mpmath import mp, mpf, log, exp, nstr
mp.dps = 1500
import os as _os  # repository root, from this file's location (no absolute paths)
_REPO = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "../../../.."))
TRACK = _REPO + "/research-20260929/publication/primal/dtoc5-lukvle10"
P5 = _REPO + "/research-20260929/open-instances/minlplib_sol/lukvle10.p5.sol"
kkt = {}
for line in open(TRACK + "/logs/lukvle10_kkt_x.txt"):
    k, v = line.split(); kkt[k] = mpf(v)
xk = [kkt[f"x{i+1}"] for i in range(1000)]
def prop(s0, s1):
    x = [s0, s1]
    for j in range(998):
        nx = (1 - x[j] + 3 * x[j + 1] - 2 * x[j + 1] ** 2) / 2
        x.append(nx)
        if abs(nx) > 10:
            return x, j + 2
    return x, None
def obj(x):
    f = mpf(0)
    for i in range(500):
        A, B = x[2*i]**2, x[2*i+1]**2
        f += exp((B + 1) * log(A)) + exp((A + 1) * log(B))
    return f
out = {}
p5 = {}
for line in open(P5):
    p = line.split()
    if len(p) == 2 and p[0].startswith("x"): p5[p[0]] = mpf(p[1])
x, esc = prop(p5["x1"], p5["x2"])
out["p5_seeds_first_index_abs_gt_10"] = esc
for D in (420, 440, 460, 640):
    s0 = mp.nint(xk[0] * mpf(10) ** D) / mpf(10) ** D
    s1 = mp.nint(xk[1] * mpf(10) ** D) / mpf(10) ** D
    x, esc = prop(s0, s1)
    if esc is None:
        dev = max(abs(x[i] - xk[i]) for i in range(1000))
        out[f"D={D}"] = dict(max_dev=nstr(dev, 3), objective=nstr(obj(x), 20))
    else:
        out[f"D={D}"] = dict(escaped_at=esc)
print(json.dumps(out, indent=1))
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs", "seed_sens_lukvle10.json"), "w"), indent=1)
