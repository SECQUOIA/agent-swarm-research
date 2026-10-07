"""Reviewer's own polar AC OPF built from a MATPOWER case file (MATPOWER conventions:
pi-model branches with tap ratio, bus shunts, quadratic costs, rateA limits on both
ends), written as a GAMS NLP and solved locally with IPOPT and CONOPT.

usage: python3 opf_gams.py case30|case39 [notap] [ang026]
  notap : set every tap ratio to 1 (as the MINLPLib rows do, per the author's claim)
  noshunt: drop bus shunts Gs, Bs
  ang026: add |theta_f - theta_t| <= 0.26 rad on every branch (as in MINLPLib)
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[5])
_PUBLIC_HOME = str(_PublicPath.home())

import re
import subprocess
import sys
import os

SRC = (_PUBLIC_REPO + '/research-20260929/publication/literature/network/sources/')
GAMS = (_PUBLIC_HOME + '/.local/opt/gams/gams54.3_linux_x64_64_sfx/gams')


def table(text, name):
    m = re.search(r"mpc\.%s\s*=\s*\[(.*?)\];" % name, text, flags=re.S)
    rows = []
    for line in m.group(1).splitlines():
        line = line.split("%")[0].strip().rstrip(";").strip()
        if line:
            rows.append([float(v) for v in line.split()])
    return rows


case = sys.argv[1]
notap = "notap" in sys.argv
ang = "ang026" in sys.argv
noshunt = "noshunt" in sys.argv
t = open(SRC + f"matpower_{case}.m").read()
base = float(re.search(r"mpc\.baseMVA\s*=\s*([\d.]+)", t).group(1))
bus, gen, br, gc = table(t, "bus"), table(t, "gen"), table(t, "branch"), table(t, "gencost")
ids = [int(b[0]) for b in bus]
ref = [int(b[0]) for b in bus if int(b[1]) == 3][0]
L = []
L.append("Sets i /%s/, g /g1*g%d/, l /l1*l%d/;" % (",".join(f"b{k}" for k in ids), len(gen), len(br)))
L.append("Variables vm(i), va(i), pg(g), qg(g), pf(l), qf(l), pt(l), qt(l), obj;")
for b in bus:
    k = int(b[0])
    L.append(f"vm.lo('b{k}')=({b[12]!r}); vm.up('b{k}')=({b[11]!r}); vm.l('b{k}')=1;")
L.append(f"va.fx('b{ref}')=0;")
for n, gg in enumerate(gen, 1):
    L.append(f"pg.lo('g{n}')=({gg[9]/base!r}); pg.up('g{n}')=({gg[8]/base!r}); qg.lo('g{n}')=({gg[4]/base!r}); qg.up('g{n}')=({gg[3]/base!r});")
    L.append(f"pg.l('g{n}')=({(gg[8]+gg[9])/2/base!r});")
obj = " + ".join(f"({c[4]*base**2!r})*sqr(pg('g{n}')) + ({c[5]*base!r})*pg('g{n}') + ({c[6]!r})" for n, c in enumerate(gc, 1))
eqs = ["eobj.. obj =e= " + obj + ";"]
names = ["eobj"]
for n, r in enumerate(br, 1):
    f, tt = int(r[0]), int(r[1])
    R, X, BC, rate, tau = r[2], r[3], r[4], r[5], r[8]
    if tau == 0 or notap:
        tau = 1.0
    z2 = R * R + X * X
    G, B = R / z2, -X / z2
    vf, vt, af, at = f"vm('b{f}')", f"vm('b{tt}')", f"va('b{f}')", f"va('b{tt}')"
    eqs.append(f"epf{n}.. pf('l{n}') =e= ({G/tau**2!r})*sqr({vf}) - ({1/tau!r})*{vf}*{vt}*(({G!r})*cos({af}-{at}) + ({B!r})*sin({af}-{at}));")
    eqs.append(f"eqf{n}.. qf('l{n}') =e= ({-(B+BC/2)/tau**2!r})*sqr({vf}) - ({1/tau!r})*{vf}*{vt}*(({G!r})*sin({af}-{at}) - ({B!r})*cos({af}-{at}));")
    eqs.append(f"ept{n}.. pt('l{n}') =e= ({G!r})*sqr({vt}) - ({1/tau!r})*{vf}*{vt}*(({G!r})*cos({at}-{af}) + ({B!r})*sin({at}-{af}));")
    eqs.append(f"eqt{n}.. qt('l{n}') =e= ({-(B+BC/2)!r})*sqr({vt}) - ({1/tau!r})*{vf}*{vt}*(({G!r})*sin({at}-{af}) - ({B!r})*cos({at}-{af}));")
    names += [f"epf{n}", f"eqf{n}", f"ept{n}", f"eqt{n}"]
    if rate > 0:
        s2 = (rate / base) ** 2
        eqs.append(f"esf{n}.. sqr(pf('l{n}')) + sqr(qf('l{n}')) =l= ({s2!r});")
        eqs.append(f"est{n}.. sqr(pt('l{n}')) + sqr(qt('l{n}')) =l= ({s2!r});")
        names += [f"esf{n}", f"est{n}"]
    if ang:
        eqs.append(f"eau{n}.. {af} - {at} =l= 0.26;")
        eqs.append(f"eal{n}.. {af} - {at} =g= -0.26;")
        names += [f"eau{n}", f"eal{n}"]
for b in bus:
    k = int(b[0])
    if noshunt:
        b = b[:4] + [0.0, 0.0] + b[6:]
    gp = " + ".join(f"pg('g{n}')" for n, gg in enumerate(gen, 1) if int(gg[0]) == k and gg[7] > 0) or "0"
    gq = " + ".join(f"qg('g{n}')" for n, gg in enumerate(gen, 1) if int(gg[0]) == k and gg[7] > 0) or "0"
    outp = " + ".join([f"pf('l{n}')" for n, r in enumerate(br, 1) if int(r[0]) == k] + [f"pt('l{n}')" for n, r in enumerate(br, 1) if int(r[1]) == k]) or "0"
    outq = " + ".join([f"qf('l{n}')" for n, r in enumerate(br, 1) if int(r[0]) == k] + [f"qt('l{n}')" for n, r in enumerate(br, 1) if int(r[1]) == k]) or "0"
    eqs.append(f"ep{k}.. {gp} - ({b[2]/base!r}) - ({b[4]/base!r})*sqr(vm('b{k}')) =e= {outp};")
    eqs.append(f"eq{k}.. {gq} - ({b[3]/base!r}) + ({b[5]/base!r})*sqr(vm('b{k}')) =e= {outq};")
    names += [f"ep{k}", f"eq{k}"]
L.append("Equations " + ",\n ".join(names) + ";")
L += eqs
L.append("Model m /all/; option nlp=%SOLVER%; m.optfile=0;")
L.append("Solve m using nlp minimizing obj;")
L.append("file res /res_%SOLVER%.txt/; put res; put obj.l:20:10 ' ' m.modelstat:3:0 ' ' m.solvestat:3:0;")
tag = f"{case}{'_notap' if notap else ''}{'_ang' if ang else ''}{'_noshunt' if noshunt else ''}"
os.makedirs(tag, exist_ok=True)
open(f"{tag}/opf.gms", "w").write("\n".join(L) + "\n")
for solver in ("ipopt", "conopt"):
    p = subprocess.run([GAMS, "opf.gms", f"--SOLVER={solver}", "lo=0", "threads=1"], cwd=tag, capture_output=True, text=True)
    res = open(f"{tag}/res_{solver}.txt").read().strip() if os.path.exists(f"{tag}/res_{solver}.txt") else "no result: " + p.stdout[-300:]
    print(f"{tag} {solver}: objective, modelstat, solvestat = {res}")
