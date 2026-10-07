"""Verifier's own check of repro-cops manifest.json against the raw logs and the worktree.

- .time (GNU time -v) and .meta files vs manifest wall/cpu/RSS/exit/load fields;
- totals;
- every number with >= 6 significant digits quoted in 'observed' must occur in the run's
  log or in one of its output files (string search, commas removed);
- every listed output file in the worktree vs its blob at c3514f03: identical, or the
  difference is limited to JSON keys containing 'seconds' / the 'source_point' string.
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[5])

import json, os, re, subprocess, sys

TRACK = (_PUBLIC_REPO + '/research-20260929/publication/reproduction/cops')
WT = (_PUBLIC_REPO + '-clean')
m = json.load(open(os.path.join(TRACK, "manifest.json")))

def parse_time(p):
    t = open(p).read()
    el = re.search(r"Elapsed \(wall clock\) time \(h:mm:ss or m:ss\): (\S+)", t).group(1)
    parts = [float(x) for x in el.split(":")]
    wall = sum(v * 60 ** (len(parts) - 1 - i) for i, v in enumerate(parts))
    u = float(re.search(r"User time \(seconds\): (\S+)", t).group(1))
    s = float(re.search(r"System time \(seconds\): (\S+)", t).group(1))
    rss = int(re.search(r"Maximum resident set size \(kbytes\): (\d+)", t).group(1))
    return wall, u + s, rss / 1024.0

def parse_meta(p):
    t = open(p).read()
    ex = int(re.search(r"^exit: (-?\d+)", t, re.M).group(1))
    la = re.findall(r"load average: ([\d.]+), ([\d.]+), ([\d.]+)", t)
    return ex, [[float(x) for x in a] for a in la]

def blob(path):
    r = subprocess.run(["git", "-C", WT, "show", "c3514f03:" + path], capture_output=True)
    return r.stdout if r.returncode == 0 else None

def strip_seconds(o):
    if isinstance(o, dict):
        return {k: strip_seconds(v) for k, v in o.items() if "seconds" not in k and k != "source_point"}
    if isinstance(o, list):
        return [strip_seconds(v) for v in o]
    return o

problems = []
wall_sum = cpu_sum = 0.0
rows = []
for r in m["runs"]:
    n = r["name"]
    w, c, rss = parse_time(os.path.join(TRACK, r["time_file"]))
    ex, loads = parse_meta(os.path.join(TRACK, "logs", n + ".meta"))
    wall_sum += w; cpu_sum += c
    if abs(w - r["wall_s"]) > 0.02: problems.append((n, "wall", w, r["wall_s"]))
    if abs(c - r["cpu_s"]) > 0.02: problems.append((n, "cpu", c, r["cpu_s"]))
    if abs(rss - r["peak_rss_mb"]) > 0.1: problems.append((n, "rss", rss, r["peak_rss_mb"]))
    if ex != r["exit"]: problems.append((n, "exit", ex, r["exit"]))
    if loads[0] != r["load_start"] or loads[-1] != r["load_end"]: problems.append((n, "load", loads, r["load_start"], r["load_end"]))
    # observed numbers present in log / outputs
    hay = open(os.path.join(TRACK, r["log"]), errors="replace").read().replace(",", "")
    for o in r.get("outputs", []):
        p = os.path.join(WT, o)
        if os.path.exists(p) and os.path.getsize(p) < 50_000_000 and not p.endswith(".npy"):
            hay += open(p, errors="replace").read().replace(",", "")
    obs = r.get("observed", "")
    missing = []
    for tok in re.findall(r"[-−]?\d[\d,]*\.?\d*(?:e[-+]?\d+)?", obs):
        t = tok.replace(",", "").replace("−", "-")
        digits = re.sub(r"[^\d]", "", t.split("e")[0]).lstrip("0")
        if len(digits) < 6: continue
        if t not in hay and t.lstrip("-") not in hay:
            missing.append(t)
    if missing: problems.append((n, "observed-not-in-log", missing))
    # outputs vs HEAD
    outcmp = {}
    for o in r.get("outputs", []):
        p = os.path.join(WT, o)
        b = blob(o)
        if not os.path.exists(p): outcmp[o] = "MISSING in worktree"; continue
        cur = open(p, "rb").read()
        if b is None: outcmp[o] = "not tracked at c3514f03"; continue
        if cur == b: outcmp[o] = "identical"; continue
        try:
            same = strip_seconds(json.loads(cur)) == strip_seconds(json.loads(b))
            outcmp[o] = "json equal except seconds/source_point" if same else "JSON DIFFERS"
        except Exception:
            outcmp[o] = "BYTES DIFFER (non-JSON)"
    bad = {k: v for k, v in outcmp.items() if v not in ("identical", "json equal except seconds/source_point")}
    if bad: problems.append((n, "outputs", bad))
    rows.append((n, round(w, 2), round(c, 2), round(rss, 1), ex, outcmp))

print("runs:", len(m["runs"]), "wall_sum %.1f cpu_sum %.1f (manifest %.1f %.1f)" %
      (wall_sum, cpu_sum, m["totals"]["wall_s_sum"], m["totals"]["cpu_s_sum"]))
for row in rows:
    print(row[0], row[1], row[2], row[3], "exit", row[4], {os.path.basename(k): v for k, v in row[5].items()})
print("PROBLEMS:", len(problems))
for p in problems: print(" ", p)
