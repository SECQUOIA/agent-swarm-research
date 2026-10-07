"""Decode the BOUNDS section of HVYCRASH.SIF for a given N and compare it
with Yurttan's AMPL file (N = 50) and with MINLPLib's hvycrash.gms.

Bound cards are applied in file order; an individual card overwrites the
earlier bound of the same variable (SIFDecode, subroutine SBOUND in
sources/hvycrash/sifdecode.f90: B_l(ncol,nbnd) = value4 and
B_u(ncol,nbnd) = value4 are assigned unconditionally). The 'FR DEFAULT'
card makes every variable free first. DO loops are expanded in place.

This is a small special-purpose reader for this one file, not a general
SIF decoder. Usage: python3 hvycrash_sif_bounds.py [N]
"""
import math
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "sources"
N = int(sys.argv[1]) if len(sys.argv) > 1 else 50
INF = math.inf


def sif_bounds(path, n):
    lines = Path(path).read_text().splitlines()
    i0 = next(i for i, l in enumerate(lines) if l.startswith("BOUNDS"))
    i1 = next(i for i, l in enumerate(lines) if l.startswith("START POINT"))
    body = [l for l in lines[i0 + 1:i1] if l.strip() and not l.startswith("*")]
    names = [f"X({k},{t})" for t in range(n + 1) for k in (1, 2, 3)]
    names += [f"U({t})" for t in range(n + 1)]
    lo = {v: 0.0 for v in names}
    up = {v: INF for v in names}

    def subst(tok, env):
        return tok.replace("N", str(n)) if "T" not in env else tok

    def apply(card, var, val):
        if card == "FR":
            lo[var], up[var] = -INF, INF
        elif card == "XX":
            lo[var] = up[var] = val
        elif card == "XL":
            lo[var] = val
        elif card == "XU":
            up[var] = val
        else:
            raise ValueError(card)

    def expand(var, t):
        var = var.replace("(T)", f"({t})").replace(",T)", f",{t})")
        return var.replace(",N)", f",{n})")

    k = 0
    while k < len(body):
        f = body[k].split()
        if f[0] == "FR" and f[2] == "'DEFAULT'":
            for v in names:
                lo[v], up[v] = -INF, INF
            k += 1
        elif f[0] == "DO":
            a = 0 if f[2] == "0" else int(f[2])
            b = n if f[3] == "N" else int(f[3])
            j = k + 1
            inner = []
            while body[j].split()[0] != "OD":
                inner.append(body[j].split())
                j += 1
            for t in range(a, b + 1):
                for g in inner:
                    apply(g[0], expand(g[2], t), float(g[3]))
            k = j + 1
        else:
            apply(f[0], expand(f[2], None), float(f[3]))
            k += 1
    return lo, up


def ampl_bounds(path):
    lo, up = {}, {}
    for m in re.finditer(r"var\s+(\w+)\s*(?:>=\s*([-\d.eE+]+))?\s*,?\s*(?:<=\s*([-\d.eE+]+))?",
                         Path(path).read_text()):
        v = m.group(1)
        lo[v] = float(m.group(2)) if m.group(2) else -INF
        up[v] = float(m.group(3)) if m.group(3) else INF
    return lo, up


def show(tag, lo, up, keys):
    for v in keys:
        print(f"  {tag:5s} {v:8s} [{lo[v]}, {up[v]}]")


for label, path in (("2026", SRC / "hvycrash/HVYCRASH.SIF"),
                    ("2013", SRC / "hvycrash/HVYCRASH_2013_a4c9117d7d.SIF")):
    lo, up = sif_bounds(path, N)
    fixed = [v for v in lo if lo[v] == up[v]]
    print(f"SIF {label} version, N = {N}: {len(lo)} variables, fixed: {fixed}")
    show("SIF", lo, up, ["X(1,0)", "X(2,0)", "X(3,0)", f"X(3,{N})", "U(0)", f"U({N})", f"X(2,{N})"])
    th = [(lo[f"X(3,{t})"], up[f"X(3,{t})"]) for t in range(N + 1)]
    print(f"  all theta_t bounds equal [0, 6.2831854]: {all(b == (0.0, 6.2831854) for b in th)}")

if N == 50:
    lo, up = ampl_bounds(SRC / "hvycrash/hvycrash.mod")
    fixed = [v for v in lo if lo[v] == up[v]]
    print(f"AMPL hvycrash.mod: {len(lo)} variables, fixed: {fixed}")
    show("AMPL", lo, up, ["x1_0", "x2_0", "x3_0", "x3_50", "u0", "u50"])
    th = [(lo[f"x3_{t}"], up[f"x3_{t}"]) for t in range(51)]
    print(f"  all x3_t bounds equal [0, 6.2831854]: {all(b == (0.0, 6.2831854) for b in th)}")
    g = (SRC / "minlplib_gms/hvycrash.gms").read_text()
    ups = re.findall(r"x(\d+)\.up = 6\.2831854;", g)
    print(f"MINLPLib hvycrash.gms: {len(ups)} variables with .up = 6.2831854 "
          f"(x{ups[0]}..x{ups[-1]}); .fx statements: {len(re.findall(r'.fx', g))}")
    slo, sup = sif_bounds(SRC / "hvycrash/HVYCRASH.SIF", 50)
    amap = {}
    for v in slo:
        m = re.match(r"X\((\d),(\d+)\)", v)
        amap[v] = f"x{m.group(1)}_{m.group(2)}" if m else "u" + v[2:-1]
    diff = [v for v in slo if (slo[v], sup[v]) != (lo[amap[v]], up[amap[v]])]
    print(f"SIF (2026, N = 50) vs AMPL: variables with different bounds: {diff}")
