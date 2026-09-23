"""Independent exact dual certificates for the upper-only blending path.

Uses the theoretical M=(2*(2*n)**(2*n)+1), not an experimental small penalty.
All network variables are actual left/right arc flows. No lower supply,
quality equality, or hidden Klee--Minty row is included in the certificates.
"""
from fractions import Fraction as F
from itertools import product

from exact_shadow_check import instance, vertex, witness


def solve_square(matrix, rhs):
    n = len(rhs)
    aug = [[F(v) for v in row] + [F(value)] for row, value in zip(matrix, rhs)]
    for j in range(n):
        pivot = next(i for i in range(j, n) if aug[i][j])
        aug[j], aug[pivot] = aug[pivot], aug[j]
        factor = aug[j][j]
        aug[j] = [v / factor for v in aug[j]]
        for i in range(n):
            if i != j and aug[i][j]:
                factor = aug[i][j]
                aug[i] = [v - factor * w for v, w in zip(aug[i], aug[j])]
    return [row[-1] for row in aug]


def main():
    checks = 0
    for n in range(2, 8):
        eps, c = instance(n)
        supplies = [eps ** (n - 1 - i) for i in range(n)]
        width = 2 * n
        penalty = 2 * width**width + 1
        for bits in product((0, 1), repeat=n):
            lam = witness(bits, eps)
            z = vertex(bits, eps)
            right = [s * v for s, v in zip(supplies, z)]
            flow = [value for s, r in zip(supplies, right) for value in (s - r, r)]
            rewards = [F(1)]
            for j in range(n):
                increment = c[j] / supplies[j] if j < n - 1 else lam
                rewards.append(rewards[-1] + increment)
            assert all(0 <= r <= 2 for r in rewards)
            objective = [rewards[j + side] + penalty for j in range(n) for side in (0, 1)]
            rows, rhs = [], []
            for j, supply in enumerate(supplies):
                row = [F(0)] * width
                row[2*j] = row[2*j+1] = 1
                rows.append(row)
                rhs.append(supply)
            row = [F(0)] * width
            row[0 if bits[0] else 1] = -1
            rows.append(row)
            rhs.append(F(0))
            for j in range(1, n):
                row = [F(0)] * width
                row[2*j-1] = 1
                row[2*j] = -1 if bits[j] else 1
                rows.append(row)
                rhs.append(F(0) if bits[j] else supplies[j])
            assert all(sum(a*v for a, v in zip(row, flow)) == bound
                       for row, bound in zip(rows, rhs))
            dual = solve_square(list(map(list, zip(*rows))), objective)
            assert all(value > 0 for value in dual)
            assert sum(y*b for y, b in zip(dual, rhs)) == sum(a*v for a, v in zip(objective, flow))
            # All other physical upper bounds and homogeneous quality rows.
            assert all(0 <= flow[2*j+side] <= supplies[j]
                       for j in range(n) for side in (0, 1))
            assert all(right[j-1] + flow[2*j] <= supplies[j] and right[j-1] <= flow[2*j]
                       for j in range(1, n))
            assert flow[0] <= supplies[0] and right[-1] <= supplies[-1]
            base_constant = sum(rewards[j] * supplies[j] for j in range(n))
            expected = penalty * sum(supplies) + base_constant + sum(a*v for a, v in zip(c, z)) + lam*z[-1]
            assert expected == sum(a*v for a, v in zip(objective, flow))
            checks += 1
        print(f'n={n}: {2**n} exact upper-only physical primal/dual certificates PASS')
    print(f'PASS: {checks} unique-optimum certificates using the theoretical penalty.')


if __name__ == '__main__':
    main()
