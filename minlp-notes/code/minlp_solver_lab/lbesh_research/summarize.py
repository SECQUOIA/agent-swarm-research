"""Conservative summaries: validated witnesses plus solver-reported dual bounds.

No objective consensus, local status, or best observed objective is a proof.
Bounds remain numerical solver results, not independently checked certificates.
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
from pathlib import Path
from .validation import finite


def assessed(record, *, abs_tol=1e-6, rel_tol=1e-4, reference=None):
    validation = record.get("validation") or {}
    objective = finite(validation.get("objective"))
    bound = finite(record.get("dual_bound"))
    feasible = (validation.get("feasible") is True and objective is not None
                and validation.get("objective_sense") in ("minimize", "maximize"))
    direction = 1 if validation.get("objective_sense") == "minimize" else -1
    gap = direction*(objective-bound) if feasible and bound is not None else None
    tol = abs_tol + rel_tol*max(1, abs(objective)) if objective is not None else None
    inconsistent_bound = gap is not None and gap < -tol
    # A bounded numerical solve can legitimately finish at a limit with a
    # closed gap. Do not make status text substitute for the gap calculation.
    solved = (feasible and gap is not None and abs(gap) <= tol and
              record.get("bound_valid") is True and record.get("outcome") == "completed")
    reference_consistent = None
    if reference is not None:
        if reference.get("verified") is not True or not reference.get("evidence"):
            raise ValueError("References require verified=true and explicit evidence")
        ref = finite(reference.get("objective"))
        if ref is None:
            raise ValueError("Reference objective must be finite")
        reference_consistent = feasible and abs(objective-ref) <= abs_tol + rel_tol*max(1, abs(ref))
        solved = solved and reference_consistent
    return dict(feasible=feasible, solved=bool(solved), absolute_gap=gap,
                inconsistent_bound=inconsistent_bound,
                reference_consistent=reference_consistent)


def shifted_geomean(values, shift=1.0):
    return math.expm1(sum(math.log1p(v/shift) for v in values)/len(values))*shift if values else None


def summarize(records, references=None, *, penalty=10.0, schedule=None):
    """Use the common scheduled instance set; absent/failed solves pay PAR penalty.

    A duplicate (instance, method) is rejected instead of silently choosing a
    favorable run. Repetitions should be summarized separately by repetition.
    """
    if penalty < 1:
        raise ValueError("penalty must be at least one")
    references = references or {}
    by = {}
    for r in records:
        key = (r["instance"], r["method"])
        if key in by:
            raise ValueError(f"Duplicate run: {key}")
        by[key] = r
    instances = sorted(schedule["instances"] if schedule else {key[0] for key in by})
    methods = sorted(schedule["methods"] if schedule else {key[1] for key in by})
    if not instances or not methods:
        raise ValueError("A nonempty run set or schedule is required")
    if any(i not in instances or m not in methods for i,m in by):
        raise ValueError("Records include unscheduled runs")
    caps = {finite(r.get("wall_limit")) for r in records}
    if schedule:
        caps.add(finite(schedule.get("wall_limit")))
    if len(caps) != 1 or None in caps or next(iter(caps)) <= 0:
        raise ValueError("Comparisons require one positive common wall limit")
    cap = next(iter(caps))
    scores = {key: assessed(r, reference=references.get(key[0])) for key, r in by.items()}

    def runtime(key):
        value = finite(by[key].get("wall_time"))
        return min(cap, max(0, value)) if value is not None else cap

    result = dict(instances=instances, wall_limit=cap, penalty=penalty,
                  meaning="validated primal plus reported global dual bound; not exact certification",
                  methods={}, pairs={})
    common_all = [i for i in instances if all(scores.get((i,m), {}).get("solved") for m in methods)]
    for m in methods:
        present = [(i,m) for i in instances if (i,m) in by]
        solved = [key for key in present if scores[key]["solved"]]
        times = [runtime((i,m)) if (i,m) in solved else penalty*cap for i in instances]
        result["methods"][m] = dict(
            scheduled=len(instances), present=len(present), solved=len(solved),
            validated_feasible=sum(scores[key]["feasible"] for key in present),
            inconsistent_bounds=sum(scores[key]["inconsistent_bound"] for key in present),
            reference_disagreements=sum(scores[key]["reference_consistent"] is False for key in present),
            par_mean=sum(times)/len(times), penalized_shifted_geomean=shifted_geomean(times),
            common_all_solved=len(common_all),
            common_all_shifted_geomean=shifted_geomean([runtime((i,m)) for i in common_all]),
            outcomes={o: sum(by[key].get("outcome") == o for key in present)
                      for o in sorted({by[key].get("outcome", "missing") for key in present})})
    for a,b in itertools.combinations(methods,2):
        common = [i for i in instances if scores.get((i,a),{}).get("solved") and scores.get((i,b),{}).get("solved")]
        result["pairs"][a+" / "+b] = dict(instances=common, count=len(common),
            first_shifted_geomean=shifted_geomean([runtime((i,a)) for i in common]),
            second_shifted_geomean=shifted_geomean([runtime((i,b)) for i in common]),
            first_faster=sum(runtime((i,a)) < runtime((i,b)) for i in common),
            second_faster=sum(runtime((i,b)) < runtime((i,a)) for i in common))
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("results")
    p.add_argument("--references", help="JSON instance -> verified objective and evidence")
    p.add_argument("--penalty", type=float, default=10)
    p.add_argument("--schedule", help="Defaults to adjacent .runs/schedule.json when present")
    args = p.parse_args()
    with open(args.results) as f:
        records = [json.loads(line) for line in f if line.strip()]
    with open(args.references) if args.references else open("/dev/null") as f:
        refs = json.load(f) if args.references else {}
    schedule_path = Path(args.schedule or (args.results+".runs/schedule.json"))
    schedule = json.loads(schedule_path.read_text()) if schedule_path.exists() else None
    print(json.dumps(summarize(records, refs, penalty=args.penalty,schedule=schedule), indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
