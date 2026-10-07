#!/usr/bin/env python3
"""Independent CPU-share sampler for the live campaign runs (reviewer code).

For each run dir under RUNS with a run.json carrying a pgid, sum over all live
processes of that process group: utime+stime (own) and cutime+cstime (reaped
children) from /proc/<pid>/stat. Cumulative share = that sum / (now - start time
of the group leader). Window share = delta(sum)/delta(t) over WINDOW seconds.
Also prints the busiest process per group (name, pid) and thread counts.
"""
import json, os, sys, time
from pathlib import Path

RUNS = Path(sys.argv[1])
WINDOW = float(sys.argv[2]) if len(sys.argv) > 2 else 60
HZ = os.sysconf("SC_CLK_TCK")
BTIME = int([l for l in open("/proc/stat") if l.startswith("btime")][0].split()[1])


def proc_table():
    t = {}
    for p in os.listdir("/proc"):
        if not p.isdigit():
            continue
        try:
            s = open(f"/proc/{p}/stat").read()
            comm = s[s.index("(") + 1:s.rindex(")")]
            f = s[s.rindex(")") + 2:].split()
        except OSError:
            continue
        # f[0]=state(3) f[1]=ppid(4) f[2]=pgrp(5) f[11]=utime(14) f[12]=stime(15)
        # f[13]=cutime(16) f[14]=cstime(17) f[17]=num_threads(20) f[19]=starttime(22)
        t[int(p)] = dict(comm=comm, state=f[0], pgrp=int(f[2]), own=(int(f[11]) + int(f[12])) / HZ,
                         child=(int(f[13]) + int(f[14])) / HZ, nthr=int(f[17]),
                         start=BTIME + int(f[19]) / HZ)
    return t


def groups():
    g = {}
    for d in sorted(RUNS.iterdir()):
        try:
            m = json.loads((d / "run.json").read_text())
        except (OSError, ValueError):
            continue
        if m.get("pgid") and not m.get("end_utc"):
            g[m["pgid"]] = d.name
    return g


G = groups()
t1 = time.time(); T1 = proc_table()
time.sleep(WINDOW)
t2 = time.time(); T2 = proc_table()
print(f"loadavg {os.getloadavg()}  window {t2 - t1:.1f} s")
for pg, name in G.items():
    m1 = {p: r for p, r in T1.items() if r["pgrp"] == pg}
    m2 = {p: r for p, r in T2.items() if r["pgrp"] == pg}
    c1 = sum(r["own"] + r["child"] for r in m1.values())
    c2 = sum(r["own"] + r["child"] for r in m2.values())
    lead = T2.get(pg) or T1.get(pg)
    if not lead:
        print(f"{name:26s} pgid {pg} gone"); continue
    wall = t2 - lead["start"]
    busiest = max(m2.items(), key=lambda kv: kv[1]["own"]) if m2 else None
    print(f"{name:26s} pgid {pg:7d} nproc {len(m2)} wall {wall:7.0f} s cum cpu {c2:7.0f} s cum share {c2 / wall:.3f}"
          f"  window share {(c2 - c1) / (t2 - t1):.3f}  busiest {busiest[1]['comm']}({busiest[0]}) thr {busiest[1]['nthr']} state {busiest[1]['state']}")
