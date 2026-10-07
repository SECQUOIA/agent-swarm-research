"""Check the saved 2008 trace sizes and independently count CAMINO bounds."""

import csv
import json
from collections import defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path


sources = Path(__file__).resolve().parents[1] / "sources"
instances = {"eg_int_s", "eg_disc_s", "eg_disc2_s"}
size_fields = (
    "NumberOfEquations",
    "NumberOfVariables",
    "NumberOfNonZeros",
    "NumberOfNonlinearNonZeros",
)
for filename in ("BARON-2.trc.canall", "LINDOGLOBAL-1.trc.canall"):
    lines = (sources / "coinor_2008" / filename).read_text().splitlines()
    header_start = next(i for i, line in enumerate(lines) if line.startswith("* InputFileName,"))
    fields = (lines[header_start][2:] + lines[header_start + 1][2:]).split(",")
    records = list(csv.DictReader((line for line in lines if not line.startswith("*")), fieldnames=fields))
    matches = [record for record in records if record["InputFileName"] in instances]
    assert len(matches) == 3 and {r["InputFileName"] for r in matches} == instances
    for record in matches:
        size = tuple(int(record[field]) for field in size_fields)
        assert size == (28, 8, 220, 196), (filename, record)
        print(filename, record["InputFileName"], dict(zip(size_fields, size)))

benchmark = sources / "eg" / "camino_benchmark"
limits = json.loads(
    (benchmark / "wall_time_noncvx_sbmiqp.json").read_text(), parse_float=Decimal
)["noncvx_sbmiqp.calc_time"]
groups = defaultdict(list)
with (benchmark / "noncvx_gurobi.csv").open() as stream:
    for record in csv.DictReader(stream):
        name = Path(record["path"]).stem
        try:
            objective, bound, elapsed = (
                Decimal(record[field]) for field in ("obj", "dual_obj", "calc_time")
            )
        except InvalidOperation:
            groups["failed"].append(name)
            continue
        assert all(value.is_finite() for value in (objective, bound, elapsed)), record
        if elapsed >= Decimal("0.99") * limits[name]:
            groups["at_limit"].append(name)
        elif abs(bound) >= Decimal("1e99"):
            groups["early_placeholder"].append(name)
            print("placeholder", name, "objective", objective, "bound", bound, "time", elapsed)
        elif bound == objective:
            groups["early_equal"].append(name)
        else:
            groups["early_real_unequal"].append(name)

counts = {group: len(names) for group, names in groups.items()}
print("Early means elapsed < 0.99 * the per-instance S-B-MIQP limit.")
print("CAMINO counts:", counts, "total:", sum(counts.values()))
assert counts == {
    "at_limit": 165,
    "failed": 4,
    "early_placeholder": 2,
    "early_equal": 32,
    "early_real_unequal": 59,
}, counts
assert set(groups["early_placeholder"]) == {"eg_all_s", "hadamard_9"}
assert instances <= set(groups["early_equal"])
print("All six trace sizes and the CAMINO classification match the review.")
