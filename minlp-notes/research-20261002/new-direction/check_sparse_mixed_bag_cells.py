#!/usr/bin/env python3
"""Exact finite checks of integer cell refinement and mixed convex closure."""

import json
from pathlib import Path

from check_sparse_bag_cells import Instance, Q, check_instance, from_shifted


def instances():
    # The optimal integer is strictly inside [0,4], and its derivative is
    # positive there. A continuous-gradient integer-fixing rule would fail.
    h = [[Q(2), Q(0), Q(1, 10)], [Q(0), Q(2), Q(0)],
         [Q(1, 10), Q(0), Q(2)]]
    center = [Q(3, 10), Q(2, 5), Q(2)]
    one = from_shifted("interior_integer_positive_gradient", h, center,
                       [(Q(0), Q(1)), (Q(0), Q(1)), (Q(0), Q(4))],
                       [(0, 2), (1, 2)], [(0, 1)], 6)
    one.integers = frozenset({2})
    one.linear[2] += Q(1, 2)
    one.constant -= 1
    one.extra_optima = [tuple(center)]
    assert one.linear[2] + sum(h[2][j] * center[j] for j in range(3)) == Q(1, 2)

    # PSD curvature is insufficient for convex closure while two different
    # integer labels remain globally optimal.
    two = Instance("two_integer_labels_and_flat_continuum",
                   [[Q(2), Q(-2), Q(0)], [Q(-2), Q(2), Q(0)],
                    [Q(0), Q(0), Q(2)]],
                   [Q(0), Q(0), Q(-3)], Q(2),
                   [(Q(0), Q(1)), (Q(0), Q(1)), (Q(0), Q(3))],
                   [(0, 1), (1, 2)], [(0, 1)],
                   [(t, t, z) for t in [Q(1, 3), Q(2, 5)] for z in [Q(1), Q(2)]],
                   6, frozenset({2}))

    # Two interior integer labels and a nonconvex continuous boundary
    # coordinate must all be fixed before the remaining continuous QP is PSD.
    h3 = [[Q(1), Q(0), Q(1, 10), Q(0)],
          [Q(0), Q(-1, 2), Q(0), Q(1, 20)],
          [Q(1, 10), Q(0), Q(2), Q(1, 10)],
          [Q(0), Q(1, 20), Q(1, 10), Q(2)]]
    center3 = [Q(2, 5), Q(-1, 4), Q(0), Q(2)]
    three = from_shifted("two_integer_coordinates_nonconvex_closure", h3, center3,
                         [(Q(0), Q(1)), (Q(-1, 4), Q(3, 4)),
                          (Q(-2), Q(2)), (Q(0), Q(3))],
                         [(0, 2), (2, 3), (1, 3)], [(0, 1), (1, 2)], 6)
    three.integers = frozenset({2, 3})
    perturbation = [Q(0), Q(2, 5), Q(-2, 5), Q(2, 5)]
    three.linear = [a + b for a, b in zip(three.linear, perturbation)]
    three.constant -= sum(a * b for a, b in zip(perturbation, center3))
    three.extra_optima = [tuple(center3)]

    # With no continuous variables, singleton labels give a vacuous PSD
    # closure. Positive gradients at interior integer optima remain harmless.
    h4 = [[Q(2), Q(1, 10), Q(0)], [Q(1, 10), Q(2), Q(1, 10)],
          [Q(0), Q(1, 10), Q(2)]]
    center4 = [Q(2), Q(0), Q(2)]
    four = from_shifted("pure_integer_interior_closure", h4, center4,
                        [(Q(0), Q(4)), (Q(-2), Q(2)), (Q(0), Q(3))],
                        [(0, 1), (1, 2)], [(0, 1)], 6)
    four.integers = frozenset({0, 1, 2})
    perturbation = [Q(1, 2), Q(1, 2), Q(-2, 5)]
    four.linear = [a + b for a, b in zip(four.linear, perturbation)]
    four.constant -= sum(a * b for a, b in zip(perturbation, center4))
    four.extra_optima = [tuple(center4)]
    return [one, two, three, four]


def main():
    records = [check_instance(instance) for instance in instances()]
    assert records[0]["fixed_coordinates"].get("2") == "2"
    assert "closure_stage" not in records[1] and "2" not in records[1]["fixed_coordinates"]
    assert records[2]["fixed_coordinates"].get("2") == "0"
    assert records[2]["fixed_coordinates"].get("3") == "2"
    assert records[2]["fixed_coordinates"].get("1") == "-1/4"
    assert len(records[3]["fixed_coordinates"]) == 3
    stages = [stage for record in records for stage in record["stages"]]
    keys = ["bag_rows", "dp_row_visits", "brute_assignments_examined", "allowed_assignments",
            "min_marginals_checked", "rounding_atoms", "retained_cells", "removed_cells",
            "gradient_intervals", "new_endpoint_fixes", "new_integer_fixes"]
    report = {"status": "passed", "scope": "exact finite mixed checks; no expectation or performance claim",
              "instances": len(records), "stages": len(stages),
              "closure_cases": sum("closure_stage" in record for record in records),
              "totals": {key: sum(stage[key] for stage in stages) for key in keys}, "records": records}
    destination = Path(__file__).with_name("sparse-mixed-bag-cell-check-results.json")
    destination.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({key: report[key] for key in ["status", "instances", "stages", "closure_cases", "totals"]}))


if __name__ == "__main__":
    main()
