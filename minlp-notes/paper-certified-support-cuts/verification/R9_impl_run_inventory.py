"""R9 implementation lens: inventory of what was actually run in campaigns 3, 3D and 4.

For every run directory: modes, soft time limit, node limit, seed, status
counts, Config overrides (as recorded), SCIP parameters, Gurobi parameters,
load averages at start/end, concurrency, and replay summary.
Read-only; prints a report to stdout.
"""
import json, sys, collections, statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "experiments"
DIRS = ["v3/runs/partA-full", "v3/runs/partA-root", "v3/runs/partB", "v3/runs/partC",
        "v3d/runs/partA-root-rowdir", "v3d/runs/partB-root-rowdir", "v3d/runs/partC-rowdir",
        "v4/runs/partC2", "v4/runs/partC3", "v4/runs/partC4", "v4/runs/partB2",
        "v4/runs/partD-root", "v4/runs/partD-full"]

def load(d):
    return [json.loads(l) for l in (ROOT / d / "records.jsonl").read_text().splitlines() if l.strip()]

for d in DIRS:
    recs = load(d)
    print("=" * 100)
    print(d, "records", len(recs))
    keys = collections.Counter()
    for r in recs:
        keys[(r.get("mode"), r.get("time_limit_requested", r.get("soft_time_limit")), r.get("node_limit"), r.get("seed"))] += 1
    # find fields for the requested limits
    sample = recs[0]
    top = sorted(k for k in sample.keys())
    print(" top-level keys:", [k for k in top if k in ("mode","seed","node_limit","time_limit","soft_limit","hard_limit","job","run_id","load_start","load_end","attempt","driver_active_runs")])
    modes = collections.Counter(r.get("mode") for r in recs)
    print(" modes:", dict(modes))
    tl = collections.Counter((r.get("mode"), r.get("node_limit"), r.get("seed")) for r in recs)
    print(" (mode,node_limit,seed):", dict(tl))
    st = collections.Counter((r.get("mode"), r.get("status")) for r in recs)
    print(" statuses:", dict(st))
    # config overrides
    ov = collections.Counter()
    for r in recs:
        o = r.get("config_overrides")
        ov[(r.get("mode"), json.dumps(o, sort_keys=True) if o is not None else None)] += 1
    for (m, o), c in sorted(ov.items(), key=lambda x: str(x)):
        if o and o != "{}":
            print("  override", m, o if len(o) < 300 else o[:300], c)
    sp = collections.Counter((r.get("mode"), json.dumps(r.get("scip_params"), sort_keys=True)) for r in recs if r.get("scip_params"))
    for (m, p), c in sp.items():
        print("  scip_params", m, p, c)
    gp = collections.Counter(json.dumps({k: v for k, v in (r.get("gurobi_params") or {}).items() if k != "TimeLimit"}, sort_keys=True) for r in recs if r.get("mode") == "gurobi")
    for p, c in gp.items():
        print("  gurobi_params", p, c)
    cfg_rounds = collections.Counter((r.get("mode"), (r.get("config") or {}).get("max_rounds")) for r in recs if r.get("config"))
    print(" config max_rounds by mode:", dict(cfg_rounds))
    tls = collections.Counter((r.get("mode"), round(r.get("time_limit"), 0) if isinstance(r.get("time_limit"), (int, float)) else None) for r in recs)
    print(" run_instance time_limit (rounded):", dict(tls))
