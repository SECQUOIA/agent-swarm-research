"""Targeted rational checks for constant-coefficient scalar Bellman messages.

The imported routine assembles and solves support least-squares QPs from
residual rows. The approximation checks below evaluate exact rational values.
Neither finite enumeration nor this script proves the asymptotic theorems.
"""

from fractions import Fraction as F
from itertools import product

from check_message_complexity import direct_value


def main():
    qps = centers = approximation_checks = endpoint_checks = 0
    for theta in (F(1, 10), F(1, 20)):
        for n in range(1, 7):
            weights = [theta ** (n - i) for i in range(n)]
            base = sum(theta ** (2 * i) for i in range(n))
            data = {
                z: (sum(w * bit for w, bit in zip(weights, z)),
                    base + sum(w * w * bit for w, bit in zip(weights, z)))
                for z in product((0, 1), repeat=n)
            }
            ordered_centers = sorted(c for c, _ in data.values())
            assert len(set(ordered_centers)) == 2 ** n
            assert min(b - a for a, b in zip(ordered_centers, ordered_centers[1:])) == theta ** n
            centers += len(data)

            def q(z, t):
                c, d = data[z]
                return (t - c) ** 2 / d

            if n <= 4:
                for z, (c, _) in data.items():
                    for t in (F(0), c, F(1)):
                        assert direct_value(theta, [theta] * n, z, t) == q(z, t)
                        qps += 1
            for z, (c, _) in data.items():
                for t in (max(F(0), c - theta ** n / 3), c + theta ** n / 3):
                    assert q(z, t) < min(q(other, t) for other in data if other != z)
                    endpoint_checks += 1

            sample = set(ordered_centers) | {F(0), F(1), F(1, 2)}
            sample.update((a + b) / 2 for a, b in zip(ordered_centers, ordered_centers[1:]))
            for m in range(n + 1):
                prefix = n - m
                delta = sum(weights[:prefix])
                beta = sum(w * w for w in weights[:prefix])
                zero_set = [z for z in data if not any(z[:prefix])]
                extreme_set = [z for z in data if not any(z[:prefix]) or all(z[:prefix])]
                assert delta <= theta ** (m + 1) / (1 - theta)
                assert beta <= theta ** (2 * m + 2) / (1 - theta ** 2)
                for t in sample:
                    value = min(q(z, t) for z in data)
                    zero_value = min(q(z, t) for z in zero_set)
                    extreme_value = min(q(z, t) for z in extreme_set)
                    assert 0 <= zero_value - value <= 2 * delta + beta
                    assert 0 <= extreme_value - value <= delta ** 2 / 4 + beta
                    approximation_checks += 2
    print(f"PASS: {qps} exact support QPs, {centers} centers, "
          f"{endpoint_checks} active-neighborhood endpoints, "
          f"{approximation_checks} approximation checks; n=1..6, theta=1/10,1/20")


if __name__ == "__main__":
    main()
