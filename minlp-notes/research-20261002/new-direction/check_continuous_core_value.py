"""Exact prefix-family and adaptive-cell checks for a lazy noise value oracle.

F0(v,z)=sum((v_i-1/3)^2)+(z-v_0/2)^4 on a unit box.
The residual is convex but has zero Hessian at its optimum. Its exact
conditional value and every box-restricted core minimum are rational
for the coefficient fixtures, so all certificate checks use Fraction.
"""

from fractions import Fraction as Q
from itertools import product
import json
from pathlib import Path


SIGMA, L = Q(3, 4), Q(5)


def clip(value, lower, upper):
    return min(upper, max(lower, value))


def prefix(number, bits, alternate=False):
    if bits == 0:
        return 0
    scaled = number * (1 << bits)
    value = scaled.numerator // scaled.denominator
    if alternate and 0 < number < 1 and scaled.denominator == 1:
        value -= 1
    return min((1 << bits) - 1, value)


def coefficient_box(streams, bits):
    lower, upper = [], []
    for number, alternate in streams:
        m = prefix(number, bits, alternate)
        lower.append(SIGMA * (Q(2 * m, 1 << bits) - 1))
        upper.append(SIGMA * (Q(2 * (m + 1), 1 << bits) - 1))
    return tuple(lower), tuple(upper)


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), Q(0))


def base_value(v):
    return sum(((x - Q(1, 3)) ** 2 for x in v), Q(0))


def objective(v, z, gamma):
    return base_value(v) + (z - v[0] / 2) ** 4 + dot(gamma, v)


def minimum(gamma, lower=None, upper=None):
    if lower is None:
        lower, upper = [Q(0)] * len(gamma), [Q(1)] * len(gamma)
    a = tuple(clip(Q(1, 3) - g / 2, lo, hi)
              for g, lo, hi in zip(gamma, lower, upper))
    return base_value(a) + dot(gamma, a), a


def run_case(streams, last_level, counts):
    k = len(streams)
    gamma = tuple(SIGMA * (2 * number - 1) for number, _ in streams)
    masks = list(product((0, 1), repeat=k))
    incumbent = None
    selected = None
    retained = []
    previous_box = None
    last_bits = 0
    levels = []
    for j in range(last_level + 1):
        h = Q(1, 1 << j)
        e = k * L * h * h / 8
        bits = 0
        while k * SIGMA / (1 << bits) > e / 4:
            bits += 1
        assert bits >= last_bits
        last_bits = bits
        lo, hi = coefficient_box(streams, bits)
        for i in range(k):
            assert lo[i] <= gamma[i] <= hi[i]
            assert hi[i] - lo[i] == 2 * SIGMA / (1 << bits)
            if previous_box is not None:
                assert previous_box[0][i] <= lo[i] <= hi[i] <= previous_box[1][i]
            counts["prefix_enclosures"] += 1
        previous_box = lo, hi
        coefficient_vertices = [tuple(hi[i] if mask[i] else lo[i]
                                      for i in range(k)) for mask in masks]
        if j == 0:
            generated = [(0,) * k]
        else:
            generated = [tuple(2 * parent[i] + mask[i] for i in range(k))
                         for parent in retained for mask in masks]
        assert len(set(generated)) == len(generated)
        records = []
        for index in generated:
            corners = []
            for mask in masks:
                v = tuple((index[i] + mask[i]) * h for i in range(k))
                offset = Q(1, 1 << (j + 3))
                z = v[0] / 2 + offset
                assert 0 <= z <= 1
                u0 = base_value(v) + offset ** 4
                tangent = u0 - 4 * offset ** 3 * z
                ell0 = u0 - e / 2
                assert ell0 <= tangent <= base_value(v) <= u0
                lower, upper = ell0 + dot(lo, v), u0 + dot(hi, v)
                assert upper - lower <= e
                for completion in coefficient_vertices:
                    true_conditional = base_value(v) + dot(completion, v)
                    true_point = objective(v, z, completion)
                    assert lower <= true_conditional <= true_point <= upper
                    counts["corner_completion_checks"] += 1
                if incumbent is None or upper < incumbent:
                    incumbent, selected = upper, (v, z)
                corners.append((lower, v))
            lower, witness = min(corners)
            lb = lower - e
            cell_lower = tuple(i * h for i in index)
            cell_upper = tuple((i + 1) * h for i in index)
            for completion in coefficient_vertices:
                cell_minimum, _ = minimum(completion, cell_lower, cell_upper)
                assert lb <= cell_minimum
                counts["cell_lower_bound_checks"] += 1
            records.append((index, lb, witness))
        retained = []
        actual_optimum, _ = minimum(gamma)
        for index, lb, witness in records:
            if lb > incumbent:
                continue
            retained.append(index)
            for completion in coefficient_vertices:
                optimum, _ = minimum(completion)
                assert base_value(witness) + dot(completion, witness) <= optimum + 4 * e
                counts["retained_witness_checks"] += 1
            assert base_value(witness) + dot(gamma, witness) <= actual_optimum + 4 * e
            for i in range(k):
                if witness[i] in (0, 1):
                    continue
                left, right = list(witness), list(witness)
                left[i] -= h
                right[i] += h
                low = (base_value(witness) - base_value(right) - 4 * e) / h
                high = (base_value(left) - base_value(witness) + 4 * e) / h
                assert low <= gamma[i] <= high
                assert high - low <= (1 + k) * L * h
                counts["true_noise_strip_checks"] += 1

        lower = incumbent - 2 * e
        for completion in coefficient_vertices:
            optimum, a = minimum(completion)
            true_point = objective(*selected, completion)
            assert lower <= optimum <= true_point <= incumbent
            assert any(all(index[i] * h <= a[i] <= (index[i] + 1) * h
                           for i in range(k)) for index in retained)
            counts["global_prefix_certificate_checks"] += 1
        counts["levels"] += 1
        counts["generated_cells"] += len(generated)
        levels.append({"level": j, "prefix_bits": bits,
                       "generated": len(generated), "retained": len(retained),
                       "certified_width": str(2 * e)})
    return {"dimension": k, "stream_values": [str(s[0]) for s in streams],
            "alternate_dyadic_encodings": [s[1] for s in streams], "levels": levels}


def main():
    counts = {key: 0 for key in ["prefix_enclosures", "corner_completion_checks",
                              "cell_lower_bound_checks", "retained_witness_checks",
                              "true_noise_strip_checks", "global_prefix_certificate_checks",
                              "levels", "generated_cells"]}
    cases = []
    patterns = [((Q(0), False), (Q(1), False), (Q(1, 3), False)),
                ((Q(1, 2), False), (Q(2, 3), False), (Q(1, 4), False)),
                ((Q(1, 2), True), (Q(2, 3), False), (Q(1, 4), True))]
    for k in (1, 2, 3):
        for pattern in patterns:
            cases.append(run_case(pattern[:k], 3 if k <= 2 else 2, counts))
    result = {"status": "pass", **counts, "cases": cases,
              "scope": "exact prefix-family and adaptive-cell certificates; no stochastic performance estimate"}
    Path(__file__).with_name("continuous-core-value-results.json").write_text(
        json.dumps(result, indent=2) + "\n")
    print(json.dumps({key: value for key, value in result.items() if key != "cases"}, indent=2))


if __name__ == "__main__":
    main()
