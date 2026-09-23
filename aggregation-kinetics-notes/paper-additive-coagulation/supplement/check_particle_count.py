"""Optional count-law diagnostic: reproduce the 2,000-seed implementation check.

This is separate from the nine retained research runs and does not overwrite
any supplied data. Requires Python 3 and g++.
"""
from __future__ import annotations

import csv
import io
import json
import math
from pathlib import Path
import statistics
import subprocess
import tempfile


def main() -> None:
    directory = Path(__file__).resolve().parent
    with tempfile.TemporaryDirectory(prefix="particle-count-check-") as temporary:
        executable = Path(temporary) / "critical_particles"
        subprocess.run([
            "g++", "-O3", "-std=c++17",
            str(directory / "critical_additive_particles.cpp"), "-o", str(executable),
        ], check=True)
        counts = []
        for seed in range(2000):
            result = subprocess.run(
                [str(executable), "50", str(seed)],
                check=True, capture_output=True, text=True,
            )
            rows = list(csv.DictReader(io.StringIO(result.stdout)))
            assert len(rows) == 10 and float(rows[-1]["time"]) == 10
            counts.append(int(rows[-1]["count"]))
    exact_mean, exact_variance = 60, 1090
    sample_mean = statistics.mean(counts)
    print(json.dumps({
        "initial_n": 50, "time": 10, "seeds": "0 through 1999",
        "sample_mean": sample_mean,
        "sample_variance_unbiased": statistics.variance(counts),
        "exact_mean": exact_mean, "exact_variance": exact_variance,
        "mean_standardized_error": (
            (sample_mean - exact_mean) / math.sqrt(exact_variance / len(counts))
        ),
        "minimum_count": min(counts),
        "interpretation": "Implementation diagnostic, separate from the nine research runs.",
    }, indent=2))


if __name__ == "__main__":
    main()
