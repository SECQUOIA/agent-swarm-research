"""R9 referee lens: two read-only checks behind findings of review2-referee.md.

(1) Replay totals of campaigns 3 and 4 (Section 8.2: 143,267 cuts) and their
    split into MINLPLib cuts and path-family cuts. The abstract and the
    introduction cite only the total.
(2) Solve times of the C4 reference optimum (experiments/v4/c4-references.json):
    the paper calls the reference "a convex mixed-integer quadratic
    reformulation"; the record shows which formulation Gurobi solved and how fast.

No solver is run; only archived JSON records are read.
"""
import glob
import json
import statistics
from pathlib import Path

EXP = Path(__file__).resolve().parents[1] / "experiments"

total = path = minlp = 0
all_passed = True
for camp in ("v3", "v3d", "v4"):
    for f in sorted(glob.glob(str(EXP / camp / "runs" / "*" / "replay.json"))):
        d = json.load(open(f))
        c = d.get("replayed_cuts", d.get("cuts"))
        all_passed &= bool(d.get("passed"))
        total += c
        part = Path(f).parent.name
        if "partC" in part:
            path += c
        else:
            minlp += c
print(f"(1) replayed cuts: total {total:,}, all passed: {all_passed}")
print(f"    path family {path:,} ({100 * path / total:.1f}%), MINLPLib {minlp:,}")

refs = json.load(open(EXP / "v4" / "c4-references.json"))["instances"]
final = []
for v in refs:
    att = v["gurobi"]["attempts"]
    last = att[-1]
    final.append((v["name"], last.get("formulation", "?"), last["runtime_seconds"], last["status"]))
forms = {f for _, f, _, _ in final}
times = [t for _, _, t, _ in final]
print("(2) C4 reference formulation(s):", forms)
print(f"    runtime of the final (optimal) attempt: median {statistics.median(times):.3f} s,"
      f" range {min(times):.3f}-{max(times):.1f} s; under 1 s on"
      f" {sum(t < 1 for t in times)} of {len(times)}")
slow = [(n, round(t, 1)) for n, _, t, _ in final if t >= 1]
print("    instances with >= 1 s:", slow)
