"""R9 implementation lens: host load and concurrency during campaigns 3, 3D and 4.

Reads load_start/load_end (one-minute load average) and the run timestamps of
every record, and computes the maximum number of runs active at the same time,
both within a run directory and across all directories of a campaign.
Read-only.
"""
import json, collections, statistics
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1] / "experiments"
GROUPS = {
    "campaign3": ["v3/runs/partA-full", "v3/runs/partA-root", "v3/runs/partB", "v3/runs/partC"],
    "campaign3D": ["v3d/runs/partA-root-rowdir", "v3d/runs/partB-root-rowdir", "v3d/runs/partC-rowdir"],
    "campaign4": ["v4/runs/partC2", "v4/runs/partC3", "v4/runs/partC4", "v4/runs/partB2",
                  "v4/runs/partD-root", "v4/runs/partD-full"],
}

def ts(x):
    if x is None: return None
    if isinstance(x, (int, float)): return float(x)
    try:
        return datetime.fromisoformat(x.replace("Z", "+00:00")).timestamp()
    except Exception:
        return None

def first_load(v):
    if isinstance(v, (list, tuple)): return float(v[0])
    if isinstance(v, dict):
        for k in ("1min", "load1", "one_minute", "1"):
            if k in v: return float(v[k])
        return float(list(v.values())[0])
    return float(v) if v is not None else None

intervals_all = {}
for g, dirs in GROUPS.items():
    loads, ivs = [], []
    for d in dirs:
        recs = [json.loads(l) for l in (ROOT / d / "records.jsonl").read_text().splitlines() if l.strip()]
        r0 = recs[0]
        tkeys = [k for k in r0 if "time" in k.lower() or "start" in k.lower() or "end" in k.lower() or "stamp" in k.lower()]
        dl = []
        for r in recs:
            for k in ("load_start", "load_end"):
                v = first_load(r.get(k))
                if v is not None:
                    dl.append(v)
            s = ts(r.get("started_utc"))
            e = ts(r.get("ended_utc"))
            if s and e:
                ivs.append((s, e, d))
        loads += dl
        print(f"{d}: load min {min(dl):.1f} median {statistics.median(dl):.1f} max {max(dl):.1f}; time keys {tkeys[:8]}")
    print(f"== {g}: load min {min(loads):.1f}, 5th pct {sorted(loads)[len(loads)//20]:.1f}, median {statistics.median(loads):.1f}, 95th pct {sorted(loads)[int(len(loads)*.95)]:.1f}, max {max(loads):.1f}")
    if ivs:
        events = sorted([(s, 1) for s, e, d in ivs] + [(e, -1) for s, e, d in ivs])
        cur = mx = 0
        for t, k in events:
            cur += k; mx = max(mx, cur)
        print(f"   max concurrent runs across the group: {mx}; span {min(s for s,_,_ in ivs)} - {max(e for _,e,_ in ivs)}")
    intervals_all[g] = ivs

# cross-group overlap
allv = [(s, e, g) for g, ivs in intervals_all.items() for s, e, _ in ivs]
if allv:
    events = sorted([(s, 1) for s, e, g in allv] + [(e, -1) for s, e, g in allv])
    cur = mx = 0
    for t, k in events:
        cur += k; mx = max(mx, cur)
    print("max concurrent runs across all campaigns:", mx)
    for g1 in intervals_all:
        for g2 in intervals_all:
            if g1 < g2 and intervals_all[g1] and intervals_all[g2]:
                a = (min(s for s,_,_ in intervals_all[g1]), max(e for _,e,_ in intervals_all[g1]))
                b = (min(s for s,_,_ in intervals_all[g2]), max(e for _,e,_ in intervals_all[g2]))
                ov = max(0, min(a[1], b[1]) - max(a[0], b[0]))
                print(f"overlap {g1} vs {g2}: {ov/60:.1f} min")
