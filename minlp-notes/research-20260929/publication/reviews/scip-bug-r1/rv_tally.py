#!/usr/bin/env python3
"""Reviewer's own tally of the track's scan logs: re-applies the WRONG rule (status optimal and
claimed dual bound > exact witness value + 1e-4) with witness values from rv_cip_exact.py."""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[4])

import glob, os, re
from collections import defaultdict
T = (_PUBLIC_REPO + '/research-20260929/publication/scip-bug/')
W = {"p0": 168.108652029808, "p4": -6.73064369981647, "p5": -232.172853003462, "pair2236": 55.689908409449,
     "pumps_default": 0.612, "fm336_v1010": 187/270, "fm318_master": 1.458, "tiny2": -1.337}
files = sorted(glob.glob(T + "logs/*.log")) + sorted(glob.glob(T + "gams/logs/scan_*.txt"))
res = defaultdict(list)
for f in files:
    buf = []
    base = os.path.basename(f)
    for ln in open(f, errors="replace"):
        m = re.match(r"(?:(\S+) )?seed\s+(\d+):? (?:status (\w+)\s+claimed|(problem is solved \[optimal[^\]]*\]?|.*?)\s+dual) (\S+)", ln.strip())
        if base.startswith("scan_") and f.endswith(".txt"):
            m2 = re.match(r"(\S+) seed (\d+): (.*?) dual (\S+)", ln.strip())
            if m2:
                key = (base, "GAMS/SCIP 10.0.3", m2.group(1), "{}")
                opt = m2.group(3).startswith("problem is solved [optimal")
                res[key].append((int(m2.group(2)), opt, float(m2.group(4))))
            continue
        if m and ("claimed" in ln or "dual" in ln) and "seed" in ln:
            label = m.group(1) or "wheel"
            opt = (m.group(3) == "optimal") or ("problem is solved [optimal" in ln)
            try:
                val = float(m.group(5))
            except ValueError:
                continue
            buf.append((label, int(m.group(2)), opt, val))
            continue
        if ln.startswith("# ") and "extra=" in ln:
            mm = re.search(r"(\S+)\.cip extra=(\{.*?\}):", ln)
            if not mm:
                continue
            model = os.path.basename(mm.group(1))
            for label, seed, opt, val in buf:
                res[(base, label, model, mm.group(2))].append((seed, opt, val))
            buf = []
    if buf:
        print("UNASSIGNED lines in", base, len(buf))
print("%-34s %-8s %-18s %-46s %7s  %s" % ("log", "label", "model", "extra", "wrong", "min..max wrong claim"))
for key in sorted(res):
    base, label, model, extra = key
    w = W.get(model)
    rows = res[key]
    if w is None:
        continue
    wr = [v for s, o, v in rows if o and v > w + 1e-4]
    print("%-34s %-8s %-18s %-46s %3d/%-3d  %s" % (base, label, model, extra, len(wr), len(rows),
          ("%.9g .. %.9g" % (min(wr), max(wr))) if wr else ""))
