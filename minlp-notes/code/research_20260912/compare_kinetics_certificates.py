"""Match the four kinetics models and compare their exact certificate files."""

from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import sys

from certify_dense_design import Problem


def main():
    sys.set_int_max_str_digits(0)
    base = Path(__file__).parent/"results"
    rows = []
    files = {}
    def read(name):
        path = base/name
        files[name] = hashlib.sha256(path.read_bytes()).hexdigest()
        return json.loads(path.read_text(), parse_float=str)
    for n, source_name in ((48, "noisy-markov-kinetics-probe.json"),
                           (96, "noisy-markov-kinetics-n96-probe.json")):
        source = read(source_name)
        dense = read(f"dense-design-kinetics-n{n}-certificates.json")
        uniform = read(f"dense-all-splits-kinetics-n{n}-certificates.json")
        assert len(source["results"]) == len(dense["results"]) == len(uniform["results"]) == 2
        for case, record in enumerate(source["results"]):
            regime = record["kinetics"]["regime"]
            problem = Problem.read(record)
            assert problem.n == n
            d, a = dense["results"][case], uniform["results"][case]
            assert d["case"] == a["case"] == case and d["status"] == "certified"
            memory_name = f"noisy-markov-kinetics-certificate-n{n}-{regime}.json"
            memory = read(memory_name)
            assert memory["status"] == "certified"
            assert all(Problem.read(x["problem_data"]) == problem for x in (d, a, memory))
            memory_upper = Q(memory["upper_bound"])
            fixed_difference = Q(d["continuous_lower_bound"])-memory_upper
            uniform_difference = Q(a["all_splits_lower_bound"])-memory_upper
            assert fixed_difference > 0 and uniform_difference > 0
            rows.append({"n": n, "regime": regime, "case": case,
                         "exact_problem_data_match": True,
                         "dense_continuous_lower_bound": d["continuous_lower_bound"],
                         "dense_continuous_upper_bound": d["upper_bound"],
                         "dense_continuous_certificate_gap": d["continuous_certificate_gap"],
                         "best_incumbent_lower_bound": d["incumbent_lower_bound"],
                         "memory_upper_bound": str(memory_upper), "memory_L": memory["L"],
                         "all_splits_lower_bound": a["all_splits_lower_bound"],
                         "exact_fixed_split_separation": str(fixed_difference),
                         "exact_all_splits_separation": str(uniform_difference),
                         "display_memory_upper_bound": float(memory_upper),
                         "display_fixed_split_separation": float(fixed_difference),
                         "display_all_splits_separation": float(uniform_difference),
                         "numerical_tangent_seconds": d["numerical_tangent_seconds"],
                         "exact_tangent_seconds": d["exact_tangent_seconds"],
                         "exact_incumbent_seconds": d["exact_incumbent_seconds"],
                         "dense_total_seconds": d["total_case_seconds"],
                         "all_splits_additional_seconds": a["total_case_seconds"]})
            print(json.dumps({key: rows[-1][key] for key in
                              ("n", "regime", "display_memory_upper_bound",
                               "display_fixed_split_separation", "display_all_splits_separation")}))
    report = {"status": "strict all-splits bound separation in all four kinetics cases",
              "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "input_sha256": files, "results": rows,
              "scope": "Exact-decimal frozen sensitivity inputs; no new MIP experiments"}
    (base/"kinetics-dense-memory-certified-comparison.json").write_text(json.dumps(report, indent=2)+"\n")


if __name__ == "__main__":
    main()
