"""Targeted exact checks for geometric-copositive-certificate.md.

This is a diagnostic finite-grid DP, not a general copositivity solver.
All objective calculations and comparisons use exact integers/Fractions.
"""

from fractions import Fraction as F
from itertools import product
from math import lcm


def grid(n, delta):
    out = [F(0), delta / n]
    while out[-1] < 1:
        out.append(min(F(1), out[-1] * (1 + delta)))
    assert len(out) == len(set(out))
    return out


def prepared(a, delta, corrected=True):
    n = len(a)
    ell = 2 * max(a[i][i] for i in range(n))
    sigma = ell * delta**2 / 8
    nodes = grid(n, delta)
    node_den = lcm(*(v.denominator for v in nodes))
    ints = [int(v * node_den) for v in nodes]
    terms = {(i, i): a[i][i] - (2 * sigma if corrected else 0) for i in range(n)}
    terms.update({(i, j): 2 * a[i][j]
                  for i in range(n) for j in range(i + 1, n)
                  if a[i][j]})
    coeff_den = lcm(*(v.denominator for v in terms.values()))
    scaled = {ij: int(v * coeff_den) for ij, v in terms.items()}
    return sigma, nodes, ints, node_den, coeff_den, scaled


def dp(a, delta, bags, parent, corrected=True):
    n = len(a)
    sigma, nodes, ints, node_den, coeff_den, terms = prepared(a, delta, corrected)
    bags = [tuple(sorted(b)) for b in bags]
    children = [[] for _ in bags]
    depth = [0] * len(bags)
    for t in range(1, len(bags)):
        assert 0 <= parent[t] < t
        children[parent[t]].append(t)
        depth[t] = depth[parent[t]] + 1
    owner = {i: min((t for t, b in enumerate(bags) if i in b),
                    key=lambda t: depth[t]) for i in range(n)}
    # Check running intersection for the diagnostic input.
    for i in range(n):
        for t, bag in enumerate(bags):
            if i in bag and t != owner[i]:
                assert i in bags[parent[t]]
    local_terms = [[] for _ in bags]
    for (i, j), coeff in terms.items():
        t = owner[i] if i == j else next(
            t for t, b in enumerate(bags) if i in b and j in b)
        local_terms[t].append((bags[t].index(i), bags[t].index(j), coeff))
    separators = [()] + [tuple(i for i in bags[t] if i in bags[parent[t]])
                         for t in range(1, len(bags))]
    messages = {}
    visited = 0
    for t in reversed(range(len(bags))):
        msg = {}
        own_positions = [j for j, i in enumerate(bags[t]) if owner[i] == t]
        for assignment in product(ints, repeat=len(bags[t])):
            visited += 1
            value = sum(c * assignment[i] * assignment[j]
                        for i, j, c in local_terms[t])
            flag = int(any(assignment[j] == node_den for j in own_positions))
            costs = {flag: value}
            for child in children[t]:
                sep = tuple(assignment[bags[t].index(i)] for i in separators[child])
                next_costs = {}
                for f1, c1 in costs.items():
                    for f2 in (0, 1):
                        c2 = messages[child].get((sep, f2))
                        if c2 is None:
                            continue
                        key = f1 | f2
                        candidate = c1 + c2
                        next_costs[key] = min(next_costs.get(key, candidate), candidate)
                costs = next_costs
            sep = tuple(assignment[bags[t].index(i)] for i in separators[t])
            for flag, value in costs.items():
                key = (sep, flag)
                msg[key] = min(msg.get(key, value), value)
        messages[t] = msg
    m = F(messages[0][((), 1)], coeff_den * node_den**2)
    return m, sigma, nodes, visited


def brute(a, delta, corrected=True, witness=False):
    sigma, nodes, ints, node_den, coeff_den, terms = prepared(a, delta, corrected)
    best = None
    argmin = None
    for y in product(ints, repeat=len(a)):
        if max(y) != node_den:
            continue
        val = sum(c * y[i] * y[j] for (i, j), c in terms.items())
        if best is None or val < best:
            best = val
            argmin = y
    value = F(best, coeff_den * node_den**2)
    return (value, tuple(F(v, node_den) for v in argmin)) if witness else value


def laplacian(n, edges, weight):
    a = [[F(i == j) for j in range(n)] for i in range(n)]
    for i, j in edges:
        a[i][i] += weight
        a[j][j] += weight
        a[i][j] -= weight
        a[j][i] -= weight
    return a


def run():
    horn = [[F(6, 5) if i == j else
             F(-1 if (i - j) % 5 in (1, 4) else 1)
             for j in range(5)] for i in range(5)]
    star = laplacian(5, [(0, i) for i in range(1, 5)], F(1, 2))
    path = laplacian(4, [(i, i + 1) for i in range(3)], F(1, 3))
    fixtures = [
        ("non-SPN Horn perturbation", horn, [(0, 1, 2, 3, 4)], [-1], F(1, 5)),
        ("branching star", star, [(0, 1), (0, 2), (0, 3), (0, 4)],
         [-1, 0, 0, 0], F(1)),
        ("path", path, [(0, 1), (1, 2), (2, 3)], [-1, 0, 1], F(1)),
        ("large positive cross coefficient", [[F(1), F(10**50)],
                                               [F(10**50), F(1)]],
         [(0, 1)], [-1], F(1)),
        ("small diagonal margin", [[F(1, 1024), F(0)], [F(0), F(1)]],
         [(0,), (1,)], [-1, 0], F(1, 1024)),
        ("one coordinate", [[F(7, 3)]], [(0,)], [-1], F(7, 3)),
    ]
    trials = visits = comparisons = rounding_checks = 0
    for name, a, bags, parent, g in fixtures:
        delta = F(1, 2)
        while True:
            m, sigma, nodes, count = dp(a, delta, bags, parent)
            visits += count
            trials += 1
            if len(nodes) ** len(a) <= 100_000:
                assert m == brute(a, delta), name
                comparisons += 1
            b = m - sigma / len(a)
            # Check the bound that forces acceptance, whenever applicable.
            if sigma <= g / 4:
                assert b >= g / 4
            for low, high in zip(nodes, nodes[1:]):
                for t in (F(0), F(1, 7), F(1, 2), F(6, 7), F(1)):
                    x = low + t * (high - low)
                    variance = (x - low) * (high - x)
                    ey2 = x*x + variance
                    assert 4 * variance <= delta**2 * ey2 + (delta/len(a))**2
                    if low:
                        assert 4 * variance <= delta**2 * ey2
                        assert 4 * variance <= delta**2 * x*x
                    rounding_checks += 1
            if b > 0:
                assert g / 16 <= sigma < g
                print(f"{name}: delta={delta}, nodes={len(nodes)}, "
                      f"sigma={sigma}, b={b}, sigma/g={sigma/g}")
                break
            delta /= 2
            assert trials < 100
    # Boundary and negative forms cannot pass a positive-margin certificate.
    nonstrict_checks = 0
    for cross in (F(-1), F(-3, 2)):
        a = [[F(1), cross], [cross, F(1)]]
        for delta in (F(1, 2), F(1, 4), F(1, 8)):
            m, sigma, nodes, count = dp(a, delta, [(0, 1)], [-1])
            assert m - sigma / 2 < 0
            assert m == brute(a, delta)
            visits += count
            nonstrict_checks += 1
    # A narrow negative cone requires refinement; it is not sampled at a
    # normalized endpoint. Its exact witness supplies a lower bound on |g|.
    ratio, eps = F(3, 7), F(1, 4096)
    a = [[F(1), -ratio], [-ratio, ratio**2 - eps]]
    delta = F(1, 2)
    negative_trials = 0
    while True:
        m0, sigma, nodes, count = dp(a, delta, [(0, 1)], [-1], corrected=False)
        mcheck, witness = brute(a, delta, corrected=False, witness=True)
        assert m0 == mcheck
        assert m0 == sum(a[i][j] * witness[i] * witness[j]
                         for i in range(2) for j in range(2))
        negative_trials += 1
        visits += count
        if sigma <= eps / (4 * (1 + ratio**2)):
            assert m0 < 0
        if m0 < 0:
            print(f"narrow negative cone: {negative_trials} trials, delta={delta}, "
                  f"negative rational witness checked; "
                  f"coordinate denominator bits={max(v.denominator.bit_length() for v in witness)}")
            break
        delta /= 2
        assert negative_trials < 12
    print(f"PASS: {len(fixtures)} positive fixtures, {trials} search trials, "
          f"{visits} bag assignments, {comparisons} positive brute-force comparisons, "
          f"{rounding_checks} exact interval checks, "
          f"{nonstrict_checks} boundary/negative checks, "
          f"{negative_trials} uncorrected negative-witness trials.")


if __name__ == "__main__":
    run()
