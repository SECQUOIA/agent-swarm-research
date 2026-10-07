#!/usr/bin/env python3
"""Reviewer point check: evaluate a GAMS savepoint against the scalar MINLPLib .gms model.

Independent of the author's check_points.py (which uses OSIL + audit_eval):
parses the GAMS model text directly, reads exact binary64 levels with
gdxdump dFormat=hexponential, evaluates rows and bounds with mpmath at 60 digits.
usage: pointcheck.py <instance> <solver> [...pairs]
"""
import re
import subprocess
import sys
from pathlib import Path

import mpmath as mp

mp.mp.dps = 60
SR = Path(__file__).resolve().parents[2] / "solver-runs"


def gdx_levels(gdx):
    out = subprocess.run(["gdxdump", str(gdx), "dFormat=hexponential"], capture_output=True, text=True,
                         check=True).stdout
    lv = {}
    for m in re.finditer(r"Variable (\w+) /L ([^,/]+)", out):
        tok = m.group(2).strip().rstrip(",")
        lv[m.group(1)] = mp.mpf(float.fromhex(tok)) if tok not in ("0", "Eps") else mp.mpf(0)
    for m in re.finditer(r"Variable (\w+) /(?!L )", out):  # level omitted means 0
        lv.setdefault(m.group(1), mp.mpf(0))
    return lv


FUN = {"sqr": lambda a: a * a, "sqrt": mp.sqrt, "exp": mp.exp, "log": mp.log, "sin": mp.sin, "cos": mp.cos,
       "tanh": mp.tanh, "power": lambda a, b: a ** b, "abs": abs, "log10": mp.log10,
       "rpower": lambda a, b: a ** b, "cvpower": lambda a, b: a ** b, "vcpower": lambda a, b: a ** b,
       "errorf": lambda a: (1 + mp.erf(a / mp.sqrt(2))) / 2, "signpower": lambda a, b: mp.sign(a) * abs(a) ** b}


def model(gms):
    t = gms.read_text()
    body = t.split("Model m", 1)[0]
    eqs = {}
    for m in re.finditer(r"^(e\d+)\.\.(.*?);", body, re.M | re.S):
        txt = " ".join(m.group(2).split())
        mm = re.match(r"(.*)=([ELG])=(.*)", txt, re.I)
        eqs[m.group(1)] = (mm.group(1), mm.group(2).upper(), mm.group(3))
    bnd = {}
    for m in re.finditer(r"(?<![\w.])(\w+)\.(lo|up|fx)\s*=\s*([^;]+);", t):
        bnd.setdefault(m.group(1), {})[m.group(2)] = m.group(3).strip()
    kinds = {}
    for kind in ("Positive", "Negative", "Binary", "Integer"):
        for m in re.finditer(rf"^{kind} Variables(.*?);", t, re.M | re.S):
            for v in m.group(1).replace("\n", " ").split(","):
                if v.strip():
                    kinds[v.strip()] = kind
    return eqs, bnd, kinds


def ev(expr, env):
    py = expr.replace("**", "^^")
    py = re.sub(r"(?<![\w.])(\d+\.?\d*(?:[eE][-+]?\d+)?)", r"mp.mpf('\1')", py)
    py = py.replace("^^", "**")
    return eval(py, {"mp": mp, **FUN}, env)


def check(inst, solver):
    d = SR / "runs" / f"{inst}__{solver}"
    lv = gdx_levels(d / "m_p.gdx")
    eqs, bnd, kinds = model(SR / "gms" / f"{inst}.gms")
    worst, wrow = mp.mpf(0), None
    for name, (lhs, sense, rhs) in eqs.items():
        r = ev(lhs, lv) - ev(rhs, lv)
        v = max(r, 0) if sense == "L" else max(-r, 0) if sense == "G" else abs(r)
        if v > worst:
            worst, wrow = v, name
    bworst = mp.mpf(0)
    for v, k in kinds.items():
        x = lv.get(v, mp.mpf(0))
        if k in ("Positive", "Binary", "Integer"):
            bworst = max(bworst, -x)
        if k == "Negative":
            bworst = max(bworst, x)
        if k == "Binary":
            bworst = max(bworst, x - 1)
    for v, b in bnd.items():
        x = lv.get(v, mp.mpf(0))
        if "fx" in b:
            bworst = max(bworst, abs(x - mp.mpf(b["fx"])))
        if "lo" in b:
            bworst = max(bworst, mp.mpf(b["lo"]) - x)
        if "up" in b:
            bworst = max(bworst, x - mp.mpf(b["up"]))
    iworst = max([abs(lv.get(v, 0) - mp.nint(lv.get(v, 0))) for v, k in kinds.items() if k in ("Binary", "Integer")]
                 or [mp.mpf(0)])
    print(f"{inst:16s} {solver:6s} objvar {mp.nstr(lv['objvar'], 20)}  max row viol {mp.nstr(worst, 6)} ({wrow})  "
          f"bound viol {mp.nstr(bworst, 4)}  int viol {mp.nstr(iworst, 4)}  rows {len(eqs)}")


if __name__ == "__main__":
    a = sys.argv[1:]
    for i in range(0, len(a), 2):
        check(a[i], a[i + 1])
