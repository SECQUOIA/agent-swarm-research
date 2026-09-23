"""Compile, verify, and run the fixed nine-run particle experiment (standard library only)."""
from __future__ import annotations

import csv
from decimal import Decimal
import io
import json
import math
from pathlib import Path
import platform
import subprocess
import tempfile
import time


def main() -> None:
    directory = Path(__file__).resolve().parent
    rows = []
    timings = []
    started = time.monotonic()
    with tempfile.TemporaryDirectory(prefix="critical-particles-") as temporary:
        executable = Path(temporary) / "critical_particles"
        command = ["g++", "-O3", "-std=c++17", str(directory / "critical_additive_particles.cpp"), "-o", str(executable)]
        subprocess.run(command, check=True)
        test = subprocess.run([str(executable), "--self-test"], check=True, capture_output=True, text=True)
        print(test.stdout.strip(), flush=True)
        for n in (1000, 10000, 100000):
            for seed in (11, 29, 47):
                run_started = time.monotonic()
                result = subprocess.run([str(executable), str(n), str(seed)], check=True, capture_output=True, text=True)
                run_rows = list(csv.DictReader(io.StringIO(result.stdout)))
                assert len(run_rows) == 10
                rows.extend(run_rows)
                elapsed = time.monotonic() - run_started
                timings.append({"n": n, "seed": seed, "seconds": elapsed})
                print(f"n={n}, seed={seed}: {elapsed:.2f}s, final count={run_rows[-1]['count']}", flush=True)
    output = directory / "critical_additive_particles.csv"
    with output.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    summaries = []
    kappa = 3 - 2 * math.sqrt(2)
    for n in (1000, 10000, 100000):
        final = [row for row in rows if int(row["n"]) == n and float(row["time"]) == 10]
        def values(key):
            return [float(row[key]) for row in final]
        def extent(key):
            samples = values(key)
            return {"min": min(samples), "mean": sum(samples) / len(samples), "max": max(samples)}
        ratio = math.log(n) / (10 * math.log(2))
        p = min(1, math.log2((ratio + math.sqrt(ratio * ratio + 8)) / 2))
        exponent = 10 * (3 - 2**p - 2**(1-p)) - (1-p) * math.log(n)
        summaries.append({
            "n": n,
            "time": 10,
            "normalized_count": extent("normalized_count"),
            "count_exact_mean": n + 10,
            "count_exact_sd": math.sqrt((2 * n - 1) * 10 + 100),
            "count_standardized_residuals": [(value - (n + 10)) / math.sqrt((2 * n - 1) * 10 + 100) for value in values("count")],
            "M_half": extent("M_half"),
            "log_mean": extent("log_mean"),
            "log_variance": extent("log_variance"),
            "largest_mass_fraction": extent("largest_mass_fraction"),
            "mass_CDF_100": extent("mass_CDF_100"),
            "number_CDF_0.01": extent("number_CDF_0.01"),
            "continuum_half_moment_upper_bound": math.exp(-10 * kappa),
            "continuum_log_mean_lower_bound": -20 * math.log(2),
            "continuum_log_mean_upper_bound": -20 * math.log(2) + (1 - math.exp(-20 * kappa)) / (2 * kappa),
            "poisson_reference_log_variance": 20 * math.log(2) ** 2,
            "sufficient_asymptotic_breakdown_time_scale": math.log(n) / math.log(2),
            "best_fractional_bound_mass_CDF_discrepancy_lower_at_time_10": -math.expm1(-exponent),
            "fractional_bound_optimizer_p_at_time_10": p,
        })
    metadata = {
        "model": "initial unit masses, lambda=m=b=c=1; additive coagulation, equal halves",
        "seeds": [11, 29, 47],
        "compiler": subprocess.run(["g++", "--version"], check=True, capture_output=True, text=True).stdout.splitlines()[0],
        "platform": platform.platform(),
        "compile_flags": ["-O3", "-std=c++17"],
        "self_test": test.stdout.strip(),
        "run_timings": timings,
        "elapsed_seconds": time.monotonic() - started,
        "total_events": sum(int(row["births"]) + int(row["deaths"]) for row in rows if float(row["time"]) == 10),
        "maximum_absolute_normalized_mass_error": str(max(abs(Decimal(row["normalized_mass"]) - 1) for row in rows)),
        "summaries_at_time_10": summaries,
        "interpretation": "Continuum bounds are displayed as references; they are not asserted for finite stochastic realizations. Three seeds do not estimate confidence intervals reliably.",
    }
    (directory / "critical_additive_particles_summary.json").write_text(json.dumps(metadata, indent=2) + "\n")
    print(f"Wrote {len(rows)} snapshots to {output}", flush=True)


if __name__ == "__main__":
    main()
