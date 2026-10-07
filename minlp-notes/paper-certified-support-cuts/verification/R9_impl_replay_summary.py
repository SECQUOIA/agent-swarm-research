"""R9 implementation lens: summary of every replay.json of campaigns 3, 3D and 4.

Reports, per run directory: passed flag, records, admitted runs, cuts,
replayed cuts, missing cut logs, omitted runs, tamper controls per cut mode
(and whether each of the 14 mutations was rejected), config failures, and
whether controls cover all cut modes. Read-only.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "experiments"
DIRS = {"c3": ["v3/runs/partA-full", "v3/runs/partA-root", "v3/runs/partB", "v3/runs/partC"],
        "c3d": ["v3d/runs/partA-root-rowdir", "v3d/runs/partB-root-rowdir", "v3d/runs/partC-rowdir"],
        "c4": ["v4/runs/partC2", "v4/runs/partC3", "v4/runs/partC4", "v4/runs/partB2",
               "v4/runs/partD-root", "v4/runs/partD-full"]}
tot = {}
for g, dirs in DIRS.items():
    s = 0
    for d in dirs:
        r = json.loads((ROOT / d / "replay.json").read_text())
        ext = r.get("v3") or r.get("v4") or {}
        ctr = ext.get("tamper_controls_by_mode", {})
        ctr_s = {m: (len(c["rejections"]), sum(c["rejections"].values()), c["untampered_first_cut_passed"]) for m, c in ctr.items()}
        print(f"{d}: passed={r['passed']} archived={r.get('archived_passed')} records={r['records']} admitted={r['admitted_runs']} "
              f"cuts={r['cuts']} replayed={r['replayed_cuts']} missing_logs={r['missing_cut_logs']} omitted={len(r['omitted_runs'])} "
              f"config_failures={len(ext.get('config_failures', []))} cover_all={ext.get('tamper_controls_cover_all_cut_modes')} "
              f"controls={ctr_s} archived_controls={None if r.get('tamper_rejections') is None else (len(r['tamper_rejections']), sum(r['tamper_rejections'].values()))}")
        s += r["replayed_cuts"]
    tot[g] = s
    print("==", g, "replayed cuts", s)
print("total", sum(tot.values()))
