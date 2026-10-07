"""Exact diagnostics for bounded PosSLP gates and weighted convexification.

The paired amplifier has its own independent checker; it is not repeated here.
All Hessians are tested after the rational congruence D^-1 H_G D^-1.
"""

from fractions import Fraction as Q
from itertools import product
import json
from pathlib import Path
import random


def poly(terms):
    out = {}
    for coefficient, indices in terms:
        key = tuple(sorted(indices))
        out[key] = out.get(key, Q(0)) + coefficient
    return {key: value for key, value in out.items() if value}


def jet(p, x):
    n = len(x)
    value, gradient = Q(0), [Q(0)] * n
    hessian = [[Q(0)] * n for _ in range(n)]
    for indices, coefficient in p.items():
        term = coefficient
        for i in indices:
            term *= x[i]
        value += term
        for position, i in enumerate(indices):
            term = coefficient
            for other, j in enumerate(indices):
                if other != position:
                    term *= x[j]
            gradient[i] += term
            for other, j in enumerate(indices):
                if other != position:
                    assert len(indices) == 2
                    hessian[i][j] += coefficient
    return value, gradient, hessian


def build(source):
    gates, pairs, integers = [], [], []
    for operation, left, right in source:
        if operation == "constant":
            numerator = poly([(Q(left, 4), ())])
            denominator = poly([(Q(1, 4), ())])
            integer = left
        else:
            u1, v1 = pairs[left]
            u2, v2 = pairs[right]
            denominator = poly([(Q(1, 4), (v1, v2))])
            if operation in ("add", "subtract"):
                sign = 1 if operation == "add" else -1
                numerator = poly([(Q(1, 4), (u1, v2)),
                                  (Q(sign, 4), (u2, v1))])
                integer = integers[left] + sign * integers[right]
            else:
                assert operation == "multiply"
                numerator = poly([(Q(1, 4), (u1, u2))])
                integer = integers[left] * integers[right]
        pairs.append((len(gates), len(gates) + 1))
        gates.extend([numerator, denominator])
        integers.append(integer)
    u, v = pairs[-1]
    gates.append(poly([(Q(1, 2), (u,)), (-Q(1, 4), (v,))]))
    return gates, pairs, integers


def pow8(exponent):
    return Q(8 ** exponent) if exponent >= 0 else Q(1, 8 ** (-exponent))


def positive_definite(a):
    n = len(a)
    lower = [[Q(0)] * n for _ in range(n)]
    diagonal = [Q(0)] * n
    for i in range(n):
        diagonal[i] = a[i][i] - sum(lower[i][k] ** 2 * diagonal[k]
                                  for k in range(i))
        assert diagonal[i] > 0
        lower[i][i] = Q(1)
        for j in range(i + 1, n):
            lower[j][i] = (a[j][i] - sum(lower[j][k] * lower[i][k] * diagonal[k]
                                       for k in range(i))) / diagonal[i]


def run():
    base = [("constant", 0, None), ("constant", 1, None),
            ("add", 1, 1), ("subtract", 1, 1),
            ("multiply", 2, 2), ("subtract", 3, 4),
            ("add", 5, 1), ("multiply", 3, 6)]
    fixtures = [base[:7], base, base + [("add", 4, 6)]]
    # Many later gates reuse the same old coordinates; source input order varies.
    fixtures.append(base[:2] + [("add", 1, 0), ("multiply", 1, 1),
                              ("subtract", 0, 1)] * 5)
    rng = random.Random(2601002)
    matrices = gate_jets = exact_pairs = local_vertices = 0
    outputs = []
    for source in fixtures:
        gates, pairs, integers = build(source)
        n = len(gates)
        exact = [Q(0)] * n
        for i, p in enumerate(gates):
            assert len(p) <= 2
            assert all(len(term) <= 2 and all(j < i for j in term) for term in p)
            exact[i] = jet(p, exact)[0]
            assert -Q(1, 4) <= exact[i] <= Q(1, 4)
        for (u, v), integer in zip(pairs, integers):
            assert exact[v] > 0 and exact[u] / exact[v] == integer
            exact_pairs += 1
        assert exact[-1] != 0
        assert (exact[-1] > 0) == (integers[-1] > 0)
        outputs.append(integers[-1])

        # Enumerate each gate's own local box vertices, including repeated inputs.
        for p in gates:
            support = sorted({j for term in p for j in term})
            for vertex in product([-Q(1, 4), Q(1, 4)], repeat=len(support)):
                x = [Q(0)] * n
                for j, value in zip(support, vertex):
                    x[j] = value
                value, gradient, hp = jet(p, x)
                assert abs(value) <= Q(1, 4)
                assert sum(map(abs, gradient)) <= 1
                # Symmetric absolute row sums bound the spectral norm.
                assert max(sum(map(abs, row)) for row in hp) <= 1
                local_vertices += 1

        points = [[Q(0)] * n, [Q(1, 4)] * n, [-Q(1, 4)] * n,
                  [Q((-1) ** j, 4) for j in range(n)], exact]
        points += [[Q(rng.randint(-4, 4), 16) for _ in range(n)] for _ in range(3)]
        for x in points:
            jets = [jet(p, x) for p in gates]
            e = [[jets[i][1][j] * pow8(j - i) if j < i else Q(0)
                  for j in range(n)] for i in range(n)]
            assert max(sum(map(abs, row)) for row in e) <= Q(1, 8)
            assert max(sum(abs(e[i][j]) for i in range(n)) for j in range(n)) <= Q(1, 7)
            jmat = [[Q(i == j) - e[i][j] for j in range(n)] for i in range(n)]
            a = [[2 * sum(jmat[i][j] * jmat[i][k] for i in range(n))
                  for k in range(n)] for j in range(n)]
            for i, (value, gradient, hp) in enumerate(jets):
                residual = x[i] - value
                assert abs(residual) <= Q(1, 2)
                assert sum(map(abs, gradient)) <= 1
                for j in range(i):
                    for k in range(i):
                        a[j][k] -= 2 * residual * hp[j][k] * pow8(j + k - 2 * i)
                gate_jets += 1
            coefficient = Q(9, 8) - Q(1, 63)
            shifted = [[a[j][k] - (coefficient if j == k else 0)
                        for k in range(n)] for j in range(n)]
            positive_definite(shifted)
            matrices += 1

    assert set(outputs) >= {-3, 0, 1}
    result = {
        "status": "pass",
        "source_circuits": len(fixtures),
        "source_outputs": outputs,
        "exact_normalized_pairs": exact_pairs,
        "local_gate_vertex_checks": local_vertices,
        "gate_jets_in_global_hessian_checks": gate_jets,
        "exact_weighted_hessian_positive_definiteness_checks": matrices,
        "certified_comparison_coefficient": str(Q(9, 8) - Q(1, 63)),
        "scope": "new gate and weighted-convexification diagnostics; no amplifier rerun",
    }
    Path(__file__).with_name("posslp-gate-review-results.json").write_text(
        json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    run()
