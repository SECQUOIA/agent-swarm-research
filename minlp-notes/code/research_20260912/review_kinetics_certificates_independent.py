"""Narrow independent exact replay of the four new kinetics certificate pairs.

Reuses independently reviewed reference calculations, without repeating library
tests or the separate review of the chemical mean model.
"""

from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import sys
from time import perf_counter

import sympy as sp

import certify_all_splits
import certify_dense_design
from certify_dense_design import Problem
from review_dense_certificate_independent import direct, integer_information, sm, fq, assert_saved_log
from review_all_splits_independent import point_information


HERE = Path(__file__).resolve().parent
BASE = HERE/"results"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_split_factor(problem, a, pivots):
    """Reconstruct the saved exact LDL factor in scaled precision coordinates."""
    rho = sp.Rational(problem.rho)
    M = sp.diag(1, *((1+rho*rho,)*(problem.n-2)), 1)
    for i in range(problem.n-1):
        M[i, i+1] = M[i+1, i] = -rho
    G = sp.Rational(problem.latent)*(1-rho*rho)*sp.eye(problem.n)
    G += (sp.Rational(problem.nugget)-sp.Rational(a))*M
    pivots = tuple(map(sp.Rational, pivots))
    assert len(pivots) == problem.n
    assert all(value > 0 for value in pivots[:-1])
    L = sp.eye(problem.n)
    for i in range(1, problem.n):
        L[i, i-1] = G[i, i-1]/pivots[i-1]
    assert L*sp.diag(*pivots)*L.T == G
    # Strict diagonal dominance independently establishes M is SPD.
    assert all(M[i, i] > sum(abs(M[i, j]) for j in range(problem.n) if j != i)
               for i in range(problem.n))


def main():
    sys.set_int_max_str_digits(0)
    started = perf_counter()
    comparison_path = BASE/"kinetics-dense-memory-certified-comparison.json"
    comparison = json.loads(comparison_path.read_text())
    assert comparison["source_sha256"] == sha(HERE/"compare_kinetics_certificates.py")
    for name, expected in comparison["input_sha256"].items():
        assert sha(BASE/name) == expected
    rows = []
    for n, source_name in ((48, "noisy-markov-kinetics-probe.json"),
                           (96, "noisy-markov-kinetics-n96-probe.json")):
        source_path = BASE/source_name
        source = json.loads(source_path.read_text(), parse_float=str)
        dense_path = BASE/f"dense-design-kinetics-n{n}-certificates.json"
        dense = json.loads(dense_path.read_text())
        uniform_path = BASE/f"dense-all-splits-kinetics-n{n}-certificates.json"
        uniform = json.loads(uniform_path.read_text())
        assert dense["source_sha256"] == sha(Path(certify_dense_design.__file__))
        assert uniform["source_sha256"] == sha(Path(certify_all_splits.__file__))
        assert dense["input_sha256"] == sha(source_path)
        assert uniform["dense_certificate_sha256"] == sha(dense_path)
        assert len(source["results"]) == len(dense["results"]) == len(uniform["results"]) == 2
        for index, original in enumerate(source["results"]):
            case_started = perf_counter()
            regime = original["kinetics"]["regime"]
            memory_path = BASE/f"noisy-markov-kinetics-certificate-n{n}-{regime}.json"
            memory = json.loads(memory_path.read_text())
            d, u = dense["results"][index], uniform["results"][index]
            problem = Problem.read(original)
            assert all(Problem.read(x["problem_data"]) == problem for x in (d, u, memory))
            assert problem.n == n and d["case"] == u["case"] == memory["input_case_index"] == index
            assert memory["input_sha256"] == sha(source_path)
            assert Path(memory["input_file"]).name == source_name
            z, a = tuple(map(Q, d["tangent_z"])), Q(d["a"])
            assert sum(z) == problem.k and all(0 <= value <= 1 for value in z)
            assert len(z) == n and a > 0
            _, J, gradient = direct(problem, z, a)
            assert J == sm(d["information"]) and gradient == tuple(map(Q, d["gradient"]))
            determinant = fq(J.det())
            assert determinant == Q(d["information_determinant"])
            assert_saved_log(d["tangent_logdet_lower"], d["tangent_logdet_upper"], determinant)
            assert all(Q(pivot) > 0 for pivot in d["split_ldl_pivots"])
            verify_split_factor(problem, a, d["split_ldl_pivots"])
            price = sum(sorted(gradient, reverse=True)[:problem.k], Q(0))
            assert len(set(d["priced_selection"])) == problem.k
            assert sum(gradient[i] for i in d["priced_selection"]) == price
            tangent_gap = price-sum(g*value for g, value in zip(gradient, z))
            assert tangent_gap == Q(d["tangent_gap"]) and tangent_gap >= 0
            assert Q(d["upper_bound"]) == Q(d["tangent_logdet_upper"])+tangent_gap
            assert Q(d["continuous_lower_bound"]) == Q(d["tangent_logdet_lower"])
            selected = d["incumbent_selection"]
            assert len(selected) == len(set(selected)) == problem.k
            assert all(type(i) is int and 0 <= i < n for i in selected)
            incumbent = fq(integer_information(problem, selected).det())
            assert incumbent == Q(d["incumbent_determinant"])
            assert_saved_log(d["incumbent_lower_bound"], d["incumbent_upper_bound"], incumbent)
            upper = Q(u["upper_split"])
            assert upper > 0 and tuple(map(Q, u["feasible_point"])) == z
            upper_J = point_information(problem, z, upper)
            assert upper_J == sm(u["information_at_upper_split"])
            upper_det = fq(upper_J.det())
            assert upper_det == Q(u["information_determinant"])
            assert_saved_log(u["all_splits_lower_bound"], u["point_value_upper_bound"], upper_det)
            witness = u["spectral_upper_witness"]
            assert witness["failed_index"] == len(witness["positive_prefix_pivots"]) == n-1
            assert all(Q(value) > 0 for value in witness["positive_prefix_pivots"])
            assert Q(witness["nonpositive_pivot"]) <= 0
            verify_split_factor(problem, upper,
                                witness["positive_prefix_pivots"]+[witness["nonpositive_pivot"]])
            expected_row = next(r for r in comparison["results"] if r["n"] == n and r["regime"] == regime)
            fixed_difference = Q(d["continuous_lower_bound"])-Q(memory["upper_bound"])
            all_difference = Q(u["all_splits_lower_bound"])-Q(memory["upper_bound"])
            assert fixed_difference == Q(expected_row["exact_fixed_split_separation"]) > 0
            assert all_difference == Q(expected_row["exact_all_splits_separation"]) > 0
            for key, expected in (("dense_continuous_lower_bound", d["continuous_lower_bound"]),
                                  ("dense_continuous_upper_bound", d["upper_bound"]),
                                  ("all_splits_lower_bound", u["all_splits_lower_bound"]),
                                  ("memory_upper_bound", memory["upper_bound"])):
                assert Q(expected_row[key]) == Q(expected)
            rows.append({"n": n, "regime": regime, "status": "exact replay passed",
                         "fixed_split_separation": str(fixed_difference),
                         "all_splits_separation": str(all_difference),
                         "display_fixed_split_separation": float(fixed_difference),
                         "display_all_splits_separation": float(all_difference),
                         "memory_certificate_sha256": sha(memory_path),
                         "wall_seconds": perf_counter()-case_started})
            print(json.dumps({k: v for k, v in rows[-1].items() if k.startswith("display")
                              or k in ("n", "regime", "wall_seconds")}), flush=True)
    report = {"status": "passed", "scope": "Four new kinetics artifacts; unchanged core tests not repeated",
              "reviewer_sha256": sha(Path(__file__)),
              "comparison_sha256": sha(comparison_path),
              "input_sha256": comparison["input_sha256"],
              "dense_source_sha256": sha(Path(certify_dense_design.__file__)),
              "all_splits_source_sha256": sha(Path(certify_all_splits.__file__)),
              "results": rows, "wall_seconds": perf_counter()-started}
    (BASE/"kinetics-dense-certificates-independent-review.json").write_text(json.dumps(report, indent=2)+"\n")


if __name__ == "__main__":
    main()
