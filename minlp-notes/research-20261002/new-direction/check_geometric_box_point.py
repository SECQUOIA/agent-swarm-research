"""Exact signed-grid certificate diagnostics, not a general box optimizer."""

from fractions import Fraction as Q
from itertools import product

from check_geometric_copositive import grid


def physical(z, widths):
    return tuple(value * widths[i][value > 0] if value else Q(0)
                 for i, value in enumerate(z))


def objective(z, matrix, linear, widths):
    d = physical(z, widths)
    return sum(a*x for a, x in zip(linear, d)) + sum(
        matrix[i][j] * d[i] * d[j] for i in range(len(d)) for j in range(len(d)))


def trial(matrix, linear, widths, bags, parents, delta):
    n = len(widths)
    endpoints = [sign * linear[i] * width + matrix[i][i] * width**2
                 for i, sides in enumerate(widths)
                 for sign, width in zip((-1, 1), sides) if width]
    assert all(sign * linear[i] >= 0 for i, sides in enumerate(widths)
               for sign, width in zip((-1, 1), sides) if width)
    assert min(endpoints) > 0
    ell = 2 * max(min(endpoints), max(matrix[i][i] * width**2
                                     for i, sides in enumerate(widths) for width in sides if width))
    sigma = ell * delta**2 / 8
    positive = grid(n, delta)
    states = [([ -x for x in reversed(positive[1:])] if sides[0] else [])
              + [Q(0)] + (positive[1:] if sides[1] else []) for sides in widths]
    owners = {i: next(t for t, bag in enumerate(bags) if i in bag) for i in range(n)}
    children = [[j for j in range(t+1, len(bags)) if parents[j] == t] for t in range(len(bags))]
    separators = [()] + [tuple(i for i in bag if i in bags[parents[t]])
                         for t, bag in enumerate(bags) if t]
    assigned = [[] for _ in bags]
    for i in range(n):
        assigned[owners[i]].append((i, i))
        for j in range(i+1, n):
            if matrix[i][j]:
                target = next(t for t, bag in enumerate(bags) if i in bag and j in bag)
                assigned[target].append((i, j))
    messages = {}
    for t in reversed(range(len(bags))):
        bag = bags[t]
        message = {}
        for values in product(*(states[i] for i in bag)):
            z = dict(zip(bag, values))
            d = {i: z[i] * widths[i][z[i] > 0] if z[i] else Q(0) for i in bag}
            local = sum((linear[i]*d[i] + matrix[i][i]*d[i]**2 - 2*sigma*z[i]**2)
                        if i == j else 2*matrix[i][j]*d[i]*d[j] for i, j in assigned[t])
            flag = int(any(abs(z[i]) == 1 for i in bag if owners[i] == t))
            costs = {flag: local}
            for child in children[t]:
                separator = tuple(z[i] for i in separators[child])
                combined = {}
                for f, cost in costs.items():
                    for child_flag in (0, 1):
                        child_cost = messages[child].get((separator, child_flag))
                        if child_cost is not None:
                            key = f | child_flag
                            value = cost + child_cost
                            combined[key] = min(combined.get(key, value), value)
                costs = combined
            separator = tuple(z[i] for i in separators[t])
            for flag, cost in costs.items():
                key = separator, flag
                message[key] = min(message.get(key, cost), cost)
        messages[t] = message
    m = messages[0][(), 1]
    brute = min(objective(z, matrix, linear, widths) - 2*sigma*sum(x*x for x in z)
                for z in product(*states) if max(map(abs, z)) == 1)
    assert m == brute
    return m - sigma/n, sigma, states


def rounding_check(matrix, linear, widths, states, sigma, z):
    distributions = []
    variances = []
    for value, nodes in zip(z, states):
        if value in nodes:
            distributions.append([(value, Q(1))])
            variances.append(Q(0))
            continue
        low, high = next((a, b) for a, b in zip(nodes, nodes[1:]) if a < value < b)
        assert low * high >= 0
        distributions.append([(low, (high-value)/(high-low)), (high, (value-low)/(high-low))])
        variances.append((value-low)*(high-value))
    expected = Q(0)
    for outcome in product(*distributions):
        values = tuple(v for v, _ in outcome)
        mass = Q(1)
        for _, weight in outcome:
            mass *= weight
        assert max(map(abs, values)) == 1
        expected += mass * (objective(values, matrix, linear, widths) - sigma*sum(x*x for x in values))
    direct = objective(z, matrix, linear, widths) - sigma*sum(x*x for x in z)
    correction = sum((matrix[i][i] * widths[i][z[i] > 0]**2 - sigma) * variance
                     for i, variance in enumerate(variances) if z[i])
    assert expected - direct == correction


def main():
    fixtures = [
        ("linear", [[Q(0)]], [Q(1)], [(Q(0), Q(1))], [(0,)], [-1], Q(1)),
        ("negative diagonal", [[Q(-1)]], [Q(2)], [(Q(0), Q(1))], [(0,)], [-1], Q(1)),
        ("asymmetric interior", [[Q(1)]], [Q(0)], [(Q(1, 8), Q(1))], [(0,)], [-1], Q(1, 64)),
        ("nonhomogeneous face", [[Q(1), Q(-1)], [Q(-1), Q(1)]],
         [Q(1), Q(0)], [(Q(0), Q(1)), (Q(1), Q(1))], [(0, 1)], [-1], Q(1, 2)),
        ("signed star", [[Q(2), Q(-1, 2), Q(-1, 2)], [Q(-1, 2), Q(2), Q(0)],
                         [Q(-1, 2), Q(0), Q(2)]],
         [Q(0), Q(1), Q(1)], [(Q(1), Q(1)), (Q(0), Q(1)), (Q(0), Q(1))],
         [(0, 1), (0, 2)], [-1, 0], Q(2)),
    ]
    trials = rounded = radial = 0
    for name, matrix, linear, widths, bags, parents, growth in fixtures:
        delta = Q(1, 2)
        while True:
            bound, sigma, states = trial(matrix, linear, widths, bags, parents, delta)
            trials += 1
            samples = [[Q(0), Q(1, 7), Q(1)] if not lo else
                       ([Q(-1), Q(-2, 7), Q(0), Q(1, 7), Q(1)] if hi else [Q(-1), Q(-2, 7), Q(0)])
                       for lo, hi in widths]
            for z in product(*samples):
                if max(map(abs, z)) != 1:
                    continue
                rounding_check(matrix, linear, widths, states, sigma, z)
                rounded += 1
                for r in (Q(1), Q(1, 3), Q(1, 11)):
                    point = tuple(r*x for x in z)
                    value = objective(point, matrix, linear, widths)
                    assert value >= r*r*objective(z, matrix, linear, widths)
                    assert value >= sigma*sum(x*x for x in point) + bound*max(map(abs, point))**2
                    radial += 1
            if bound > 0:
                assert growth/16 <= sigma < growth
                break
            delta /= 2
            assert trials < 30
        print(f"{name}: sigma={sigma}, verified residual={bound}")
    matrix = [[Q(1), Q(-1)], [Q(-1), Q(1)]]
    for delta in (Q(1, 2), Q(1, 4)):
        bound, _, _ = trial(matrix, [Q(0), Q(0)], [(Q(0), Q(1))]*2, [(0, 1)], [-1], delta)
        assert bound <= 0
    print(f"5 positive fixtures, {trials} discovery trials, {rounded} exact rounding identities, {radial} radial certificate checks; 2 nonunique checks")


if __name__ == '__main__':
    main()
