"""Check the retained experiment and its summary without running particle paths."""
from __future__ import annotations

import csv
from decimal import Decimal
import json
import math
from pathlib import Path


def main() -> None:
    directory = Path(__file__).resolve().parent
    with (directory / "critical_additive_particles.csv").open() as stream:
        rows = list(csv.DictReader(stream))
    metadata = json.loads((directory / "critical_additive_particles_summary.json").read_text())
    assert len(rows) == 90
    expected_times = [0, .5, 1, 2, 3, 4, 5, 6, 8, 10]
    for n in (1000, 10000, 100000):
        for seed in (11, 29, 47):
            run = [r for r in rows if int(r["n"]) == n and int(r["seed"]) == seed]
            assert [float(r["time"]) for r in run] == expected_times
    for row in rows:
        n, count = int(row["n"]), int(row["count"])
        assert count == n + int(row["births"]) - int(row["deaths"])
        assert math.isclose(float(row["normalized_count"]), count / n, rel_tol=1e-14)
        assert abs(Decimal(row["normalized_mass"]) - 1) < Decimal("1e-10")
        assert 0 < float(row["min_size"]) <= n
        assert 0 < float(row["largest_mass_fraction"]) <= 1 + 1e-10
        assert float(row["M_half"]) >= 1 / math.sqrt(n) - 1e-14
        for key, value in row.items():
            if "CDF" in key:
                assert 0 <= float(value) <= 1 + 1e-10
    final = [r for r in rows if float(r["time"]) == 10]
    total_events = sum(int(r["births"]) + int(r["deaths"]) for r in final)
    assert total_events == metadata["total_events"]
    mass_error = max(abs(Decimal(r["normalized_mass"]) - 1) for r in rows)
    assert mass_error == Decimal(metadata["maximum_absolute_normalized_mass_error"])
    for summary in metadata["summaries_at_time_10"]:
        n = summary["n"]
        subset = [r for r in final if int(r["n"]) == n]
        for key in ("normalized_count", "M_half", "log_mean", "log_variance",
                    "largest_mass_fraction", "mass_CDF_100", "number_CDF_0.01"):
            values = [float(r[key]) for r in subset]
            for statistic, result in (("min", min(values)), ("max", max(values)),
                                      ("mean", sum(values) / len(values))):
                assert math.isclose(summary[key][statistic], result, rel_tol=1e-13)
        assert summary["count_exact_mean"] == n + 10
        assert math.isclose(summary["count_exact_sd"], math.sqrt((2*n-1)*10+100))
    print("Verified 90 snapshots, all nine declared runs, count identities, normalizations,")
    print(f"mass ceiling, finite half-moment floor, CDF ranges, {total_events:,} events, and saved summaries.")


if __name__ == "__main__":
    main()
