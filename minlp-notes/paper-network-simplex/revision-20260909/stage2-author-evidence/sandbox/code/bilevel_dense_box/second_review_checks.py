"""Exact diagnostics for the dense-box bilevel hardness proof.

These checks supplement the symbolic proof; they are not a bilevel solver.
Run with a standard Python installation.
"""

from fractions import Fraction as F
from itertools import product


def residuals(x, y):
    return [
        y[i] - 3 ** (i + 1) * x
        + 2 * sum(3 ** (i - j) * y[j] for j in range(i)) + 1
        for i in range(len(y))
    ]


def check_boolean_responses():
    checked = 0
    extended = 0
    for n in range(1, 9):
        rho = F(1, 100 * 3**n)
        weights = [rho**i for i in range(n)]
        eta = rho**n
        for bits in product((0, 1), repeat=n):
            x = sum(F(2 * bits[i], 3 ** (i + 1)) for i in range(n))
            x += F(1, 2 * 3**n)
            assert 0 < x < 1
            y = list(map(F, bits))
            p, q = y[:], [1 - a for a in y]
            base = residuals(x, y)
            rp = [p[i] - 2 * y[i] + 1 for i in range(n)]
            rq = [q[i] + 2 * y[i] - 1 for i in range(n)]
            gy = [F(0) for _ in range(n)]
            # Differentiate each affine residual square independently.
            for k in range(n):
                for j in range(k + 1):
                    coefficient = 1 if j == k else 2 * 3 ** (k - j)
                    gy[j] += weights[k] * base[k] * coefficient
            for i in range(n):
                assert (1 - 2 * bits[i]) * gy[i] > weights[i] / 3**n
                gy[i] += eta * (-2 * rp[i] + 2 * rq[i])
                assert (1 - 2 * bits[i]) * gy[i] > 0
                assert (1 - 2 * p[i]) * eta * rp[i] >= 0
                assert (1 - 2 * q[i]) * eta * rq[i] >= 0
            assert n - sum(p) - sum(q) == 0
            if n >= 3:
                triples = [tuple((j + k) % n for k in range(3)) for j in range(n)]
                clause_families = [
                    [(triple, (True, True, True)) for triple in triples],
                    [(triple, signs) for triple in triples
                     for signs in product((False, True), repeat=3)],
                ]
                for clauses in clause_families:
                    xi = eta / (len(clauses) + 1)
                    extra = [F(0) for _ in range(n)]
                    violations = []
                    for indices, signs in clauses:
                        literal_sum = sum(y[j] if sign else 1 - y[j]
                                          for j, sign in zip(indices, signs))
                        v = max(F(0), 1 - literal_sum)
                        residual = v - 1 + literal_sum
                        assert 0 <= v <= 1
                        assert (1 - 2 * v) * xi * residual >= 0
                        for j, sign in zip(indices, signs):
                            extra[j] += xi * residual * (1 if sign else -1)
                        violations.append(v)
                    for i in range(n):
                        assert abs(extra[i]) < 2 * eta
                        assert (1 - 2 * bits[i]) * (gy[i] + extra[i]) > 0
                        # Final presentation deletes q and its derivative.
                        without_q = gy[i] - 2 * eta * rq[i] + extra[i]
                        assert (1 - 2 * bits[i]) * without_q > 0
                    if not any(violations):
                        assert n - sum(p) - sum(q) + 2 * sum(violations) == 0
                    extended += 1
            checked += 1
        assert all(a == 0 for a in residuals(F(1, 2), [F(1, 2)] * n))
    return checked, extended


def check_readout_and_rounding():
    values = [F(i, 4) for i in range(5)]
    checked = 0
    gap_cases = 0
    no_upper_gap_cases = 0
    for y in product(values, repeat=3):
        p = [max(F(0), 2 * a - 1) for a in y]
        q = [max(F(0), 1 - 2 * a) for a in y]
        cost = 3 - sum(p) - sum(q)
        assert cost == 2 * sum(min(a, 1 - a) for a in y)
        assert cost == 2 * sum(y) - 2 * sum(p)
        bits = [int(a >= F(1, 2)) for a in y]
        # All eight clauses on three variables form an unsatisfiable formula.
        violation_sum = F(0)
        for positive in product((False, True), repeat=3):
            literals = [y[i] if positive[i] else 1 - y[i] for i in range(3)]
            violation_sum += max(F(0), 1 - sum(literals))
            boolean_literals = [bits[i] if positive[i] else 1 - bits[i] for i in range(3)]
            if not any(boolean_literals):
                assert literals == [min(a, 1 - a) for a in y]
                if sum(literals) >= 1:
                    assert cost >= 2
                    gap_cases += 1
            checked += 1
        assert cost + 2 * violation_sum >= 2
        no_upper_gap_cases += 1
    return checked, gap_cases, no_upper_gap_cases


if __name__ == "__main__":
    boolean_count, extended_count = check_boolean_responses()
    clause_count, gap_count, no_upper_count = check_readout_and_rounding()
    print(f"PASS: {boolean_count} exact Boolean response KKT certificates; "
          f"8 midpoint identities; {clause_count} literal/readout checks "
          f"including {gap_count} feasible false-clause gap cases; "
          f"{extended_count} clause-feedback KKT certificates; "
          f"{no_upper_count} gap checks without upper constraints.")
