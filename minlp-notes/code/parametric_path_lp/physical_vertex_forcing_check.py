"""Independent original-network LP checks of the two-feed vertex interface.

Fixes only the actual pool quality. All other equations are physical
input supplies, output demands, pool balances, and upper quality rows.
"""
from fractions import Fraction as F
from itertools import product

import numpy as np
from scipy.optimize import linprog

from exact_shadow_check import vertex
from exact_rank_one_slab_check import coefficients


def solve(n, terminal):
    eps = F(1, 4)
    supplies = [eps ** (n-1-j) for j in range(n)]
    count = 2*n+7
    bypass_a, feed_a, feed_b, bypass_b, waste, primary, clean = range(2*n, count)
    q = 2-terminal
    eq, rhs, ub, upper = [], [], [], []

    def row(items):
        result = np.zeros(count)
        for j, value in items:
            result[j] += float(value)
        return result

    for j, supply in enumerate(supplies):
        eq.append(row([(2*j, 1), (2*j+1, 1)]))
        rhs.append(float(supply))
    for j in range(1, n):
        ub.append(row([(2*j-1, 1), (2*j, 1)]))
        upper.append(float(supplies[j]))
        previous_quality, quality = n-j, n-j-1
        bound = F(previous_quality+quality, 2)
        ub.append(row([(2*j-1, previous_quality-bound), (2*j, quality-bound)]))
        upper.append(0)
    for items, bound in [([(bypass_a, 1), (feed_a, 1)], 1),
                         ([(feed_b, 1), (bypass_b, 1)], 1),
                         ([(feed_a, 1), (feed_b, 1), (waste, -1), (primary, -1)], 0),
                         ([(waste, 1), (primary, 1)], 1),
                         ([(2*n-1, 1), (bypass_a, 1)], 1),
                         ([(bypass_b, 1), (waste, 1)], 1),
                         ([(feed_a, 1), (feed_b, 2), (waste, -q), (primary, -q)], 0)]:
        eq.append(row(items))
        rhs.append(bound)
    for items, bound in [([(2*n-1, -1)], 0),  # terminal upper quality1
                         ([(waste, q-2)], 0),  # waste upper quality2
                         ([(primary, q-1), (clean, -1)], 0),
                         ([(primary, 1), (clean, 1)], 2)]:
        ub.append(row(items))
        upper.append(bound)
    # Ordinary source costs and output revenues, assigned on actual arcs.
    reward = np.zeros(count)
    for j, supply in enumerate(supplies):
        right_revenue = supplies[j+1] if j+1 < n else F(1)
        reward[2*j] = 0  # left revenue and source cost both s_j
        reward[2*j+1] = float(right_revenue-supply)
    reward[feed_a] = reward[feed_b] = -1
    reward[waste] = reward[primary] = 1
    reward[clean] = -1
    bounds = [(0, float(s)) for s in supplies for _ in range(2)] + [(0, 1)]*7
    result = linprog(-reward, A_ub=np.array(ub), b_ub=upper,
                     A_eq=np.array(eq), b_eq=rhs, bounds=bounds, method='highs')
    assert result.success, result.message
    values = result.x
    assert abs(values[2*n-1]-float(terminal)) < 1e-8
    assert abs(values[feed_a]-float(terminal)) < 1e-8
    assert abs(values[feed_b]-float(1-terminal)) < 1e-8
    assert abs(values[primary]-float(terminal)) < 1e-8
    assert abs(values[waste]-float(1-terminal)) < 1e-8
    assert abs(values[clean]-float(terminal-terminal*terminal)) < 1e-8
    return -result.fun, [F(0) if abs(values[2*j+1]) < 1e-12 else values[2*j+1]/float(supplies[j]) for j in range(n)]


def main():
    optima = interiors = 0
    for n in range(2, 8):
        for bits in product((0, 1), repeat=n):
            x = vertex(bits, F(1, 4))
            profit, recovered = solve(n, x[-1])
            assert abs(profit) < 1e-8
            assert max(abs(float(a)-float(b)) for a, b in zip(x, recovered)) < 1e-7
            optima += 1
        for terminal in [F(1, 3), F(1, 2), F(2, 3)]:
            profit, _ = solve(n, terminal)
            assert profit < -F(1, 100)
            interiors += 1
    print(f'PASS: {optima} full physical vertex extensions recover the unique path vertex and zero economic profit.')
    print(f'PASS: {interiors} interior terminal values force strictly negative best physical profit.')
    print('All core flow identities and the minimum clean dilution were checked from original-network LP solutions.')


if __name__ == '__main__':
    main()
