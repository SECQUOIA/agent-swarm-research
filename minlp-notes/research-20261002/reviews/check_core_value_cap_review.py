"""Exact finite-law diagnostics for the k<=2 capped growth moment.

The fixture is V_gamma(v)=sum((gamma_i-1)*v_i), v in [0,1]^k.
An independent residual z^4 on [0,1] has this conditional value and
no positive uniform residual Hessian bound. This is a probability/cap
diagnostic, not an implementation of the grid or convex value oracle.
"""

from fractions import Fraction as Q
from itertools import product
from math import isqrt
import json
from pathlib import Path


def ceiling(q):
    return (q.numerator + q.denominator - 1) // q.denominator


def ceiling_sqrt(q):
    root = isqrt(q.numerator // q.denominator)
    return root if root * root * q.denominator == q.numerator else root + 1


def run():
    rows = []
    atom_checks = tail_checks = 0
    for k in (1, 2):
        for budget in (2, 4, 8):
            for multiple in (1, 2, 4):
                m = k * budget * multiple
                assert m & (m - 1) == 0
                beta = Q(k, m)
                assert beta * budget <= 1
                noises = [Q(-1) + Q(2 * j, m - 1) for j in range(m)]
                growths, capped_counts, fallback = [], 0, 0
                for gamma in product(noises, repeat=k):
                    growth = min(1 - coefficient for coefficient in gamma)
                    growths.append(growth)
                    if growth == 0:
                        count, cap = budget, True
                    else:
                        z = max(Q(1), 1 / growth)
                        count = ceiling_sqrt(z) if k == 1 else ceiling(z)
                        cap = count > budget
                        if cap:
                            assert growth < Q(1, budget ** (2 // k))
                        count = min(budget, count)
                    capped_counts += count
                    fallback += cap
                    atom_checks += 1
                total = m ** k
                mean_count = Q(capped_counts, total)
                fallback_work = Q(budget * fallback, total)

                # A ceiling increases the continuous truncated moment by <=1.
                # log_2(budget)>=ln(budget) is a rational upper bound here.
                logarithm_bound = budget.bit_length() - 1
                moment_bound = (2 + k + beta * budget if k == 1
                                else 2 + k * logarithm_bound + beta * budget)
                fallback_bound = (Q(k, budget) + beta * budget if k == 1
                                  else k + beta * budget)
                assert mean_count <= moment_bound
                assert fallback_work <= fallback_bound
                assert fallback > 0  # The endpoint law contains flat core draws.

                for threshold in [Q(1, budget ** (2 // k)), Q(1, 1000),
                                  Q(1, 2), Q(1), Q(2), Q(3)]:
                    probability = Q(sum(g < threshold for g in growths), total)
                    assert probability <= k * threshold + beta
                    tail_checks += 1
                rows.append({
                    "core_dimension": k, "fallback_budget": budget,
                    "noise_atoms_per_coordinate": m,
                    "expected_capped_ceiling_count": str(mean_count),
                    "expected_fallback_work": str(fallback_work),
                    "fallback_probability": str(Q(fallback, total)),
                })

    result = {"status": "pass", "finite_laws": len(rows),
              "exact_draw_checks": atom_checks,
              "threshold_tail_checks": tail_checks, "cases": rows,
              "scope": "finite-law truncated moments and tied atoms only; no grid/oracle implementation"}
    Path(__file__).with_name("core-value-cap-review-results.json").write_text(
        json.dumps(result, indent=2) + "\n")
    print(json.dumps({key: value for key, value in result.items() if key != "cases"}, indent=2))


if __name__ == "__main__":
    run()
