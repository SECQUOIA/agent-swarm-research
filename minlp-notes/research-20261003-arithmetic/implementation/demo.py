"""Small deterministic examples; these are diagnostics, not theorem proofs."""

from fractions import Fraction as Q
import json

from output_contracts import (ConvexityCertificate, Domain, EvenPower, Problem, Witness,
                              gradient_coefficient_rows, rank_and_kernel,
                              verify_distance_to_set, verify_minimum_norm, verify_value_gap)


def accepts(call):
    try:
        call()
    except ValueError:
        return False
    return True


def main():
    certificate = ConvexityCertificate((0, 0), 0, (EvenPower(1, (1, 0), 0, 2),))
    model = Problem(certificate.expand(2), certificate, Domain((-1, -1), (1, 1)))
    witness = Witness((0, 1), (0, 1))
    rank, kernel = rank_and_kernel(gradient_coefficient_rows(model.objective), 2)
    thin_certificate = ConvexityCertificate((0,), 0, (EvenPower(Q(1, 2 ** 80), (1,), 0, 2),))
    thin = Problem(thin_certificate.expand(1), thin_certificate, Domain((0,), (1,)))
    far_point = Witness((1,), (0,))

    # The recurrence is a compact exact representation of this rational.
    # Expanding its denominator explicitly needs exponentially many bits.
    steps = 12
    circuit_value = Q(1, 2)
    for _ in range(steps):
        circuit_value *= circuit_value
    result = {
        "nonunique_optimum": {
            "objective": "x^2 on [-1,1]^2",
            "candidate": [0, 1],
            "gradient_coefficient_rank": rank,
            "invariance_kernel_basis": [[str(x) for x in row] for row in kernel],
            "distance_to_set_1_over_100_certified": accepts(lambda: verify_distance_to_set(model, witness, Q(1, 100))),
            "distance_to_minimum_norm_1_over_100_certified": accepts(lambda: verify_minimum_norm(model, witness, Q(1, 100))),
            "minimum_norm_candidate_0_0_certified": accepts(lambda: verify_minimum_norm(model, Witness((0, 0), (0, 0)), Q(1, 100))),
        },
        "small_gap_far_point": {
            "objective": "2^(-80) z^2 on [0,1]",
            "candidate": 1,
            "exact_optimizer": 0,
            "proved_value_gap": str(verify_value_gap(thin, far_point, Q(1, 2 ** 80)).gap_bound),
            "actual_distance_to_optimizer": 1,
            "distance_1_over_2_certified": accepts(lambda: verify_distance_to_set(thin, far_point, Q(1, 2))),
        },
        "compact_exact_output": {
            "recurrence": "r_0=1/2; r_(i+1)=r_i*r_i",
            "squaring_steps": steps,
            "nodes_including_rational_seed": steps + 1,
            "expanded_denominator_bits": circuit_value.denominator.bit_length(),
            "formula_for_expanded_denominator_bits": "2^steps + 1",
            "scope": "Representation-size example, not an optimization algorithm or PosSLP solver.",
        },
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
