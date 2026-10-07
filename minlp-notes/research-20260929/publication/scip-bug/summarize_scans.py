"""Summarize all seed-scan logs of this folder into logs/scan_summary.csv and
print a table: per (log, version, model, extra settings) the number of seeds,
the number of WRONG runs and the smallest / largest wrong claim.

Formats read: run_binary.py logs (lines '<ver> seed N ... dual X ... WRONG|ok'
followed by '# <ver> (...) <model> extra=...: wrong in k of n seeds'),
seed_scan.py logs ('seed N status S claimed X ... WRONG|ok', then
'# <model> extra=...: wrong in k of n seeds') and gams/logs/scan_*.txt.
usage: python3 summarize_scans.py"""
import csv
import glob
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
rows = []


def flush(src, ver, model, extra, runs):
    wrong = [c for c, w in runs if w]
    rows.append(dict(log=src, version=ver, model=model, extra=extra, seeds=len(runs), wrong=len(wrong),
                     min_wrong_claim=min(wrong) if wrong else "", max_wrong_claim=max(wrong) if wrong else ""))


for path in sorted(glob.glob(os.path.join(HERE, "logs", "*.log"))):
    src = os.path.relpath(path, HERE)
    runs = []
    for line in open(path, errors="replace"):
        m = re.match(r"^(\S+) seed +\d+ .* dual (\S+) primal \S+ nodes \S+ (WRONG|ok)", line)
        if m:
            runs.append((float(m.group(2)) if m.group(2) != "None" else None, m.group(3) == "WRONG"))
            continue
        m = re.match(r"^seed +\d+ status \S+ +claimed (\S+) .* (WRONG|ok)$", line.strip())
        if m:
            runs.append((float(m.group(1)), m.group(2) == "WRONG"))
            continue
        m = re.match(r"^# (\S+) \(SCIP version ([^ ]+) .*?GitHash: ([^\]]+)\]\) (\S+) extra=(.*): wrong in (\d+) of (\d+)", line)
        if m:
            assert int(m.group(7)) == len(runs) and int(m.group(6)) == sum(w for _, w in runs), (src, line)
            flush(src, f"{m.group(1)} ({m.group(2)} {m.group(3)})", m.group(4), m.group(5), runs)
            runs = []
            continue
        m = re.match(r"^# (\S+) extra=(.*): wrong in (\d+) of (\d+)", line)
        if m and runs:
            assert int(m.group(4)) == len(runs) and int(m.group(3)) == sum(w for _, w in runs), (src, line)
            flush(src, "PySCIPOpt 6.2.1 (SCIP 10.0.2 wheel)", os.path.basename(m.group(1)), m.group(2), runs)
            runs = []
for path in sorted(glob.glob(os.path.join(HERE, "gams", "logs", "scan_*.txt"))):
    runs = []
    for line in open(path):
        m = re.match(r"^\S+ seed \d+: .* dual (\S+) primal \S+ nodes \S+ (WRONG|ok)", line)
        if m:
            runs.append((float(m.group(1)), m.group(2) == "WRONG"))
    key = os.path.basename(path)[5:-4]
    flush(os.path.relpath(path, HERE), "GAMS 54.3 / SCIP 10.0.3", key + ".gms", "{}", runs)

with open(os.path.join(HERE, "logs", "scan_summary.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
for r in rows:
    print(f"{r['log']:38s} {r['version'][:34]:34s} {r['model']:22s} {r['extra'][:45]:45s} "
          f"{r['wrong']:3d}/{r['seeds']:<3d} {r['min_wrong_claim']!s:>18s} {r['max_wrong_claim']!s:>18s}")
