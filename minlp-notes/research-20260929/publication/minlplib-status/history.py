"""Part B: compare archived versions of MINLPLib instances with the current
model files.

Archived sources (all on disk under pages/sources/):
  gamsworld  GAMS-dev/gamsworld (GitHub copy of the closed GAMS World site):
             GlobalLib/scalar_models, MINLPLib/Scalar_models (MINLPLib 1),
             PrincetonLib/Cute/Scalar_models. The GAMS Convert header line
             of each file gives its conversion date.
  jl2017     lanl-ansi/MINLPLib.jl, instances/minlp2/<name>.jl as first
             committed (commit 9002dfa, 2017-11-23), translated to GAMS by
             jl2gms.py.
Each source and the current MINLPLib .gms are converted by the same GAMS
54.3 Convert run (scalar GAMS + OSiL). Two checks per source:
  text:  canonical scalar GAMS of the source == that of the current .gms
         (ignoring the "written by GAMS Convert at" line);
  osil:  osil_compare(source OSiL, current MINLPLib OSIL), see osil_compare.py.
A control check compares the OSiL of the current .gms with the current
MINLPLib OSIL (the file the audit used).

Usage: python3 history.py [names...]   (default: the Part B list)
Output: data/history/<name>.json, logs/history.log
"""
from pathlib import Path as _PublicPath
_PUBLIC_HOME = str(_PublicPath.home())

import json
import os
import re
import shutil
import subprocess
import sys
import time

import instances as I
import jl2gms
import osil_compare

HERE = os.path.dirname(os.path.abspath(__file__))
GAMS = (_PUBLIC_HOME + '/.local/opt/gams/gams54.3_linux_x64_64_sfx/gams')
SRC = os.path.join(HERE, "pages", "sources")
CANON = os.path.join(HERE, "pages", "canon")
CACHE = os.path.expanduser("~/.cache/minlplib/minlplib/osil")
PARTB = I.AUDIT_I + I.AUDIT_IR + I.ROCKET
GW_DIRS = ["GlobalLib/scalar_models", "MINLPLib/Scalar_models", "PrincetonLib/Cute/Scalar_models"]


def convert_header(path):
    with open(path, errors="replace") as f:
        for _ in range(5):
            m = re.search(r"written by GAMS Convert at (\S+ \S+)", f.readline())
            if m:
                return m.group(1)
    return None


def canon(src_gms, name, tag):
    d = os.path.join(CANON, name, tag)
    if os.path.exists(d):
        shutil.rmtree(d)
    os.makedirs(d)
    shutil.copy(src_gms, os.path.join(d, name + ".gms"))
    with open(os.path.join(d, "convert.opt"), "w") as f:
        f.write(f"Gams canon.gms\nOSiL {name}.osil\n")
    t0 = time.time()
    p = subprocess.run([GAMS, name + ".gms", "solver=convert", "optfile=1", "lo=2", f"o={name}.lst"],
                       cwd=d, capture_output=True, text=True, timeout=1800)
    lst = open(os.path.join(d, name + ".lst"), errors="replace").read() if os.path.exists(
        os.path.join(d, name + ".lst")) else ""
    errs = len(re.findall(r"^\*\*\*\*\s+\$", lst, re.M)) + lst.count("*** Error")
    ok = p.returncode == 0 and os.path.exists(os.path.join(d, name + ".osil"))
    return dict(dir=os.path.relpath(d, HERE), gams_rc=p.returncode, listing_errors=errs, ok=ok,
                seconds=round(time.time() - t0, 1))


def canon_text(name, tag):
    p = os.path.join(CANON, name, tag, "canon.gms")
    lines = open(p, errors="replace").read().split("\n")
    return "\n".join(l for l in lines if "written by GAMS Convert at" not in l)


def short(rep):
    keep = dict(verdict=rep["verdict"], summary=rep["summary"], nvars=rep["nvars"], ncons=rep["ncons"],
                obj_sense=rep["obj_sense"])
    keep["var_diffs"] = rep["var_diffs"][:20]
    keep["row_diffs_not_equal"] = [d for d in rep["row_diffs"]
                                   if not d["verdict"].startswith("equal (numerically")][:20]
    keep["row_diffs_equal_count"] = sum(1 for d in rep["row_diffs"] if d["verdict"].startswith("equal (numerically"))
    for k in ("vars_only_a", "vars_only_b", "cons_only_a", "cons_only_b"):
        keep[k] = rep[k][:20]
    return keep


def sources_for(name):
    out = []
    gw = os.path.join(SRC, "gamsworld")
    for d in GW_DIRS:
        p = os.path.join(gw, d, name + ".gms")
        if os.path.exists(p):
            out.append(dict(tag="gamsworld-" + d.split("/")[0], path=p, kind="gms",
                            origin=f"github.com/GAMS-dev/gamsworld {d}/{name}.gms",
                            date=convert_header(p)))
    p = os.path.join(SRC, "jl2017", name + ".jl")
    if os.path.exists(p) and os.path.getsize(p) > 0:
        out.append(dict(tag="jl2017", path=p, kind="jl",
                        origin=f"github.com/lanl-ansi/MINLPLib.jl commit 9002dfa instances/minlp2/{name}.jl",
                        date="2017-11-23 (commit date; the source version it was converted from is not stated)"))
    return out


def run(name):
    res = dict(name=name, group=I.GROUP.get(name))
    cur_gms = os.path.join(HERE, "pages", "models", "gms", name + ".gms")
    ml_osil = os.path.join(CACHE, name + ".osil")
    res["current"] = canon(cur_gms, name, "current")
    if res["current"]["ok"]:
        rep = osil_compare.compare(os.path.join(CANON, name, "current", name + ".osil"), ml_osil)
        res["control_current_gms_vs_minlplib_osil"] = short(rep)
    res["sources"] = []
    for s in sources_for(name):
        rec = dict(s)
        rec["path"] = os.path.relpath(s["path"], HERE)
        src = s["path"]
        if s["kind"] == "jl":
            gpath = os.path.join(CANON, name, "jl2017.gms")
            os.makedirs(os.path.dirname(gpath), exist_ok=True)
            try:
                txt, info = jl2gms.translate(open(src).read())
            except Exception as e:  # noqa: BLE001
                rec["translate_error"] = repr(e)[:300]
                res["sources"].append(rec)
                continue
            open(gpath, "w").write(txt)
            rec["translate_info"] = info
            src = gpath
        c = canon(src, name, s["tag"])
        rec["convert"] = c
        if c["ok"] and res["current"]["ok"]:
            rec["canonical_text_identical"] = canon_text(name, s["tag"]) == canon_text(name, "current")
            rep = osil_compare.compare(os.path.join(CANON, name, s["tag"], name + ".osil"), ml_osil)
            rec["vs_minlplib_osil"] = short(rep)
        res["sources"].append(rec)
    os.makedirs(os.path.join(HERE, "data", "history"), exist_ok=True)
    json.dump(res, open(os.path.join(HERE, "data", "history", name + ".json"), "w"), indent=1, default=str)
    return res


def line(res):
    out = [res["name"]]
    c = res.get("control_current_gms_vs_minlplib_osil")
    out.append("control:" + (c["verdict"][:20] if c else "FAILED " + str(res["current"])))
    for s in res["sources"]:
        if "vs_minlplib_osil" in s:
            out.append(f"{s['tag']}[{s.get('date')}]: text={'same' if s['canonical_text_identical'] else 'diff'} "
                       f"osil={s['vs_minlplib_osil']['verdict'][:20]} {s['vs_minlplib_osil']['summary']}")
        else:
            out.append(f"{s['tag']}: FAILED {s.get('translate_error') or s.get('convert')}")
    return " | ".join(out)


if __name__ == "__main__":
    names = sys.argv[1:] or PARTB
    for n in names:
        t0 = time.time()
        r = run(n)
        print(line(r), f"({round(time.time() - t0)} s)", flush=True)
