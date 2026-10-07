"""Solve one period subproblem of waterno2_T with BARON (GAMS 54.3) as an
independent, non-rigorous cross-check.  The GAMS model is written from the
verifier's own model data (vmodel; OSIL decimal strings kept verbatim).
usage: python3 vbaron.py T t multipliers.json [reslim]
"""
import json
import os
import re
import subprocess
import sys
from fractions import Fraction as F

import vmodel

GAMS = 'gams'


def write(T, t, lam, mu, path, reslim, extra=None):
    I = vmodel.instance(T)
    m = I["m"]
    V = I["per_vars"][t]
    nm = m["names"]
    obj = vmodel.period_objective(I, t, lam, mu)
    L = ["$offlisting", "option limrow=0, limcol=0;", "Variables z;"]
    L.append("Variables " + ",".join(nm[v] for v in V if m["vt"][v] != "B") + ";")
    bins = [nm[v] for v in V if m["vt"][v] == "B"]
    L.append("Binary Variables " + ",".join(bins) + ";")
    for v in V:
        if m["vt"][v] == "B":
            continue
        if m["lb"][v].upper() != "-INF":
            L.append(f"{nm[v]}.lo = {m['lb'][v]};")
        else:
            L.append(f"{nm[v]}.lo = -inf;")
        if m["ub"][v].upper() not in ("INF", "+INF"):
            L.append(f"{nm[v]}.up = {m['ub'][v]};")
        if extra and nm[v] in extra:
            a, b = extra[nm[v]]
            L.append(f"{nm[v]}.lo = max({nm[v]}.lo, {a}); {nm[v]}.up = min({nm[v]}.up, {b});")
    eqs = []
    body = []
    for i in I["per_rows"][t]:
        c = m["cons"][i]
        terms = []
        for mono, a in vmodel.poly(c).items():
            if len(mono) == 1:
                f = nm[mono[0]]
            elif len(set(mono)) == 1:
                f = f"power({nm[mono[0]]},{len(mono)})"
            else:
                f = f"{nm[mono[0]]}*{nm[mono[1]]}"
            terms.append(f"({a.numerator}/{a.denominator})*{f}" if a.denominator != 1 else f"({a})*{f}")
        expr = " + ".join(terms)
        lb, ub = c["lb"], c["ub"]
        if lb == ub:
            eqs.append(c["name"])
            body.append(f"{c['name']}.. {expr} =e= {lb};")
        else:
            if lb.upper() != "-INF":
                eqs.append(c["name"] + "_lo")
                body.append(f"{c['name']}_lo.. {expr} =g= {lb};")
            if ub.upper() not in ("INF", "+INF"):
                eqs.append(c["name"] + "_up")
                body.append(f"{c['name']}_up.. {expr} =l= {ub};")
    eqs.append("objdef")
    body.append("objdef.. z =e= " + " + ".join(f"({float(a)!r})*{nm[v]}" for v, a in obj.items()) + ";")
    L.append("Equations " + ",".join(eqs) + ";")
    L += body
    L += ["Model per /all/;", "option minlp=baron, optcr=0, optca=1e-7;", f"per.reslim={reslim};",
          "per.optfile=0;", "Solve per using minlp minimizing z;",
          "file res /res.txt/; put res; put 'OBJ ' z.l:0:12 /; put 'EST ' per.objest:0:12 /;"
          " put 'MS ' per.modelstat:0:0 /; put 'SS ' per.solvestat:0:0 /;",
          "loop(" + "", ]
    L = L[:-1]
    L.append("put 'CONF';")
    for b in bins:
        L.append(f"put ' ' {b}.l:0:0;")
    L.append("put /; putclose res;")
    L.append("file sol /sol.txt/; sol.nr = 2; sol.nd = 16; sol.nw = 26; put sol;")
    for v in V:
        L.append(f"put '{nm[v]} ' {nm[v]}.l /;")
    L.append("putclose sol;")
    open(path, "w").write("\n".join(L) + "\n")


if __name__ == "__main__":
    T, t = int(sys.argv[1]), int(sys.argv[2])
    K = json.load(open(sys.argv[3]))
    lam = [[float(v) for v in l] for l in K["lam"]]
    mu = float(K["mu"])
    reslim = float(sys.argv[4]) if len(sys.argv) > 4 else 300
    extra = json.load(open(sys.argv[5])) if len(sys.argv) > 5 else None
    d = f"/tmp/wv_gams/T{T}_p{t}_{os.path.basename(sys.argv[3]).split('.')[0]}" + ("_impl" if extra else "")
    os.makedirs(d, exist_ok=True)
    write(T, t, lam, mu, d + "/per.gms", reslim, extra)
    subprocess.run([GAMS, "per.gms", "lo=2", "threads=1"], cwd=d, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    out = open(d + "/res.txt").read() if os.path.exists(d + "/res.txt") else "no result"
    print(f"BARON T={T} period {t} mult {os.path.basename(sys.argv[3])} implied={bool(extra)}: " + " | ".join(out.strip().splitlines()))
