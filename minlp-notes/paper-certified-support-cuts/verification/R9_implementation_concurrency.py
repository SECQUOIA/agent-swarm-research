"""R9 implementation lens: how many runs of this project were active at the
same time, within and across the run directories of campaign 3, the post hoc
3D diagnostic and campaign 4?

Counts, for every run start t, the runs with started <= t < ended
(timestamps have one-second resolution, so a run that ends in the second in
which another starts is not counted twice). Reports the maximum per group and the prospective
campaign-3 runs that overlapped a moment with more than six active runs.
Read-only.
"""
import collections
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "experiments"
DIRS = ["v3/runs/partA-full", "v3/runs/partA-root", "v3/runs/partB", "v3/runs/partC",
        "v3d/runs/partA-root-rowdir", "v3d/runs/partB-root-rowdir", "v3d/runs/partC-rowdir",
        "v4/runs/partC2", "v4/runs/partC3", "v4/runs/partC4", "v4/runs/partB2",
        "v4/runs/partD-root", "v4/runs/partD-full", "v4/scanD/screen"]


def ts(text):
    return datetime.fromisoformat(text.replace("Z", "+00:00")).timestamp()


def utc(t):
    return datetime.fromtimestamp(t, timezone.utc).strftime("%m-%d %H:%M:%S")


runs = []
for d in DIRS:
    for line in (ROOT / d / "records.jsonl").read_text().splitlines():
        if line.strip():
            r = json.loads(line)
            runs.append((ts(r["started_utc"]), ts(r["ended_utc"]), d, r["run_id"]))

span = collections.defaultdict(lambda: [float("inf"), float("-inf")])
for s, e, d, _ in runs:
    span[d][0] = min(span[d][0], s)
    span[d][1] = max(span[d][1], e)
for d in DIRS:
    print(f"{d:30s} {utc(span[d][0])} - {utc(span[d][1])} UTC")


def peak(subset):
    best, where = 0, None
    for s, *_ in subset:
        active = [x for x in subset if x[0] <= s < x[1]]
        if len(active) > best:
            best, where = len(active), (s, collections.Counter(x[2] for x in active))
    return best, where


for name, prefixes in [("campaign 3 (prospective)", ("v3/",)), ("3D diagnostic", ("v3d/",)),
                       ("campaign 3 incl. 3D", ("v3/", "v3d/")), ("campaign 4", ("v4/",))]:
    subset = [x for x in runs if x[2].startswith(prefixes)]
    best, (t, counter) = peak(subset)
    print(f"{name}: max simultaneously active runs {best} at {utc(t)} UTC: {dict(counter)}")

subset = [x for x in runs if x[2].startswith(("v3/", "v3d/"))]
hit = collections.Counter()
for s, e, d, _ in subset:
    if not d.startswith("v3/"):
        continue
    t = s
    while t <= e:
        if sum(1 for y in subset if y[0] <= t < y[1]) > 6:
            hit[d] += 1
            break
        t += 1
print("prospective campaign-3 runs that overlapped a moment with more than six active runs:", dict(hit))
