"""Numbers quoted in Section 9 for campaign 3, recomputed from the archived records.

Standard library only. Usage: python analyze_v3.py
"""
import json, collections, math, statistics
from pathlib import Path
EXP = Path(__file__).resolve().parents[1] / "experiments"
def load(p): return [json.loads(l) for l in open(p)]
def solved(r):
    pc = r.get("primal_check") or {}
    return r["status"] in ("optimal", "gaplimit") and r.get("primal") is not None and pc.get("passed", pc.get("feasible", False))
for part in ["v3/runs/partA-full", "v3/runs/partA-root", "v3/runs/partB", "v3/runs/partC",
             "v3d/runs/partC-rowdir", "v3d/runs/partA-root-rowdir", "v3d/runs/partB-root-rowdir"]:
    p = EXP / part / "records.jsonl"
    if not p.exists(): continue
    recs = load(p)
    print("==", part, len(recs), "records")
    by_mode = collections.defaultdict(list)
    for r in recs: by_mode[(r["phase"], r["mode"])].append(r)
    for (phase, mode), rs in sorted(by_mode.items()):
        models_with_cuts = sorted({r["name"] for r in rs if r.get("cuts")})
        inc = [r for r in rs if r.get("primal") is not None]
        checks = [r.get("primal_check") or {} for r in inc]
        passed = sum(1 for c in checks if c.get("passed", c.get("feasible", False)))
        sep = [((r.get("separation") or {}).get("callback_seconds") or 0.0) for r in rs]
        disc = [((r.get("separation") or {}).get("discovery_seconds") or 0.0) for r in rs]
        cert = [((r.get("separation") or {}).get("certification_seconds") or 0.0) for r in rs]
        cand = [((r.get("separation") or {}).get("candidate_seconds") or 0.0) for r in rs]
        print(f"  {phase:5s} {mode:20s} runs {len(rs):3d} solved {sum(map(solved, rs)):3d} cuts {sum(len(r.get('cuts') or []) for r in rs):5d} "
              f"models-with-cuts {len(models_with_cuts):2d} incumbents {len(inc)} passed {passed} "
              f"callback {sum(sep):.1f}s discovery {sum(disc):.1f}s directionLP {sum(cand):.1f}s certification {sum(cert):.1f}s")
