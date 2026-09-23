"""Apply an already reviewed tighter error bound to saved numerical prices.

No additional optimization or pricing is performed. The saved surrogate upper
bound remains numerical, so this does not produce an exact certificate.
"""

from fractions import Fraction as Q
import hashlib
import json
import math
from pathlib import Path
from time import perf_counter

from noisy_markov_spacing_bound import spacing_bound


HERE = Path(__file__).resolve().parent


def main():
    source = HERE/"results/fixed-physical-grid-benchmark.json"
    original = json.loads(source.read_text())
    if not original["metadata"]["complete"]:
        raise ValueError("The benchmark must be complete")
    rows = []
    for case in original["results"]:
        for index, hull in enumerate(case["hulls"]):
            started = perf_counter()
            row = {"n": case["n"], "L": hull["L"], "hull_index": index,
                   "original_status": hull["status"],
                   "true_lower_bound": hull["combined_true_lower_bound"],
                   "original_true_upper_bound": hull["combined_true_upper_bound"],
                   "original_true_gap": hull["combined_true_gap"]}
            surrogate = hull.get("surrogate_upper_bound")
            if surrogate is None:
                row.update(status="unavailable", reason="No completed surrogate upper bound")
            else:
                delta = spacing_bound(case["n"], hull["L"], 1, Q(case["rho"]),
                                      Q(case["latent_variance"]), Q(case["nugget_variance"]),
                                      refined_pairs=True)["delta"]
                if delta >= 1:
                    row.update(status="unavailable", reason="Refined delta is not below one")
                else:
                    transferred = surrogate-case["p"]*math.log1p(-float(delta))
                    upper = min(transferred, hull["combined_true_upper_bound"])
                    gap = upper-hull["combined_true_lower_bound"]
                    if gap < -1e-7:
                        raise ArithmeticError("Numerical upper bound is below feasible lower bound")
                    row.update(status="numerical_transfer", refined_delta_exact=str(delta),
                               refined_delta=float(delta), surrogate_upper_bound=surrogate,
                               transferred_upper_bound=transferred, combined_true_upper_bound=upper,
                               combined_true_gap=gap, target_gap_met_numerically=gap <= .01)
            row["reanalysis_seconds"] = perf_counter()-started
            row["pipeline_plus_reanalysis_seconds"] = hull["pipeline_seconds"]+row["reanalysis_seconds"]
            rows.append(row)
    result = {"status": "complete", "formula": "U_true <= U_surrogate - p*log(1-delta_refined)",
              "scope": "Numerical reanalysis of stored bounds. No new solve or exact certificate; no added spacing restriction (gap=1).",
              "source_artifact": str(source), "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
              "reviewed_bound_sha256": hashlib.sha256((HERE/"noisy_markov_spacing_bound.py").read_bytes()).hexdigest(),
              "driver_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), "results": rows}
    output = HERE/"results/fixed-physical-grid-refined-transfer.json"
    output.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps([{key: value for key, value in row.items() if key != "refined_delta_exact"}
                      for row in rows], indent=2))


if __name__ == "__main__":
    main()
