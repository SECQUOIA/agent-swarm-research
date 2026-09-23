"""Certify the overlap constant and evaluate illustrative tail-dissipation examples."""
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR, localcontext
from fractions import Fraction
import json
import math
from pathlib import Path


def log_psi(q):
    result = 0.0
    argument = q / 2
    for _ in range(256):
        result -= math.log1p(argument)
        argument /= 2
    # The omitted logarithmic sum is at most q*2**(-256).
    return result


def outward_decimal(value, rounding):
    with localcontext() as context:
        context.prec = 100
        context.rounding = rounding
        result = Decimal(value.numerator) / Decimal(value.denominator)
        return str(result.quantize(Decimal("1e-30"), rounding=rounding))


product = Fraction(1)
for k in range(1, 129):
    product *= Fraction(2**k, 2**k + 1)
lower = 1 - product
upper = 1 - product * (1 - Fraction(1, 2**128))
certificate = {
    "c_star_lower": outward_decimal(lower, ROUND_FLOOR),
    "c_star_upper": outward_decimal(upper, ROUND_CEILING),
    "method": "Exact rational P_128(1)(1-2^-128) <= Psi(1) <= P_128(1); outward decimal endpoints.",
}
examples = []
for epsilon in (0.1, 0.01, 0.001, 0.0003):
    delta = math.exp(-math.log(1 / epsilon) ** 3)
    assert delta > 0  # Keep the illustrative examples inside the positive-size model.
    large = (1 - (1 - epsilon) * delta) / epsilon
    values = [delta, large]
    weights = [1 - epsilon, epsilon]
    tail = sum(weight * -math.expm1(log_psi(value)) for value, weight in zip(values, weights))
    dissipation = sum(
        weights[i] * weights[j] * values[i] * math.exp(log_psi(values[i] + values[j]))
        for i in range(2) for j in range(2)
    )
    examples.append({"epsilon": epsilon, "small_atom": delta, "large_atom": large,
                     "h": tail, "minus_h_derivative_over_b": dissipation,
                     "relative_hazard_over_b": dissipation / tail})

result = {"overlap_constant_certificate": certificate,
          "two_point_dissipation_examples": examples,
          "limits": "Only the overlap endpoints are certified by exact rational bounds. Example evaluations use floating point and illustrate the proved counterexample; they do not prove asymptotics."}
path = Path(__file__).with_suffix(".json")
path.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
