"""R5-impl: count recorded cuts with one column (SCIP may apply them as bound
changes after addCut) and whether lhs/coefficient is exact in binary64."""
import collections, json, sys
from fractions import Fraction as Q
from pathlib import Path

BASE = Path(__file__).resolve().parents[1] / "experiments"
for part in sys.argv[1:]:
    counts = collections.Counter()
    for line in open(BASE / part / "records.jsonl"):
        r = json.loads(line)
        for cut in r.get("cuts") or []:
            row = cut["actual_row"]
            cols = row["columns"]
            counts["cuts"] += 1
            if len(cols) != 1:
                continue
            (name, coef), = cols.items()
            side = float(row["lhs"]) - float(row["constant"])
            exact = Q(side) / Q(coef)
            rounded = Q(side / coef)
            counts["single_column"] += 1
            counts["coef_pm1"] += abs(coef) == 1.0
            counts["division_inexact"] += exact != rounded
            counts["division_rounds_up"] += (coef > 0 and rounded > exact) or (coef < 0 and rounded < exact)
    print(part, dict(counts))
