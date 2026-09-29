#!/usr/bin/env python3
"""Independent exact finite checks of the spectral reference implementation.

Grid witnesses are compared with full grid enumeration. Continuous optima use
Cramer's rule with permutation determinants, independently of the reference
linear solver and Schur formulas. Boundary probes are finite checks, not a
proof of dictionary equality over a general continuous box.
"""

from collections import Counter
from fractions import Fraction as F
from itertools import permutations, product
from random import Random

from spectral_reference import (
    Problem, construct_all, construct_message, enumerate_near, factor_ownership,
    grid_minimize, least_even_mesh, message_parameters, midpoint_net,
    restricted_oracle, sample_noise, support_branch,
)


STATS = Counter()


def problem(Q, c, penalties, mu, H, C, bags, parents):
    return Problem(tuple(tuple(F(a) for a in row) for row in Q),
                   tuple(map(F, c)), tuple(map(F, penalties)), F(mu), F(H), F(C),
                   tuple(tuple(bag) for bag in bags), tuple(parents))


def det(matrix):
    n = len(matrix)
    answer = F(0)
    for perm in permutations(range(n)):
        term = F((-1) ** sum(perm[i] > perm[j] for i in range(n) for j in range(i + 1, n)))
        for i in range(n):
            term *= matrix[i][perm[i]]
        answer += term
    return answer


def conditional_objective(p, noise, I, S, t, support, x):
    return (sum((x[i] * p.Q[i][j] * x[j] for i in I for j in I), F(0))
            + sum((p.c[i] * x[i] for i in I), F(0))
            + 2 * sum((x[i] * p.Q[i][j] * t[h] for i in I for h, j in enumerate(S)), F(0))
            + sum((p.penalties[i] + noise[i] for i in support), F(0)))


def exact_support(p, noise, I, S, t, support):
    A = tuple(support)
    matrix = [[2 * p.Q[i][j] for j in A] for i in A]
    rhs = [-p.c[i] - 2 * sum(p.Q[i][j] * t[h] for h, j in enumerate(S)) for i in A]
    denominator = det(matrix)
    assert denominator > 0
    x = dict.fromkeys(I, F(0))
    for column, i in enumerate(A):
        replaced = [row.copy() for row in matrix]
        for h in range(len(A)):
            replaced[h][column] = rhs[h]
        x[i] = det(replaced) / denominator
    STATS['support_qps'] += 1
    return conditional_objective(p, noise, I, S, t, A, x), x


def exhaustive_supports(p, noise, I, S, t, fixed):
    values = {}
    for bits in product((0, 1), repeat=len(I)):
        z = dict(zip(I, bits))
        if all(z[i] == bit for i, bit in fixed.items()):
            A = tuple(i for i in I if z[i])
            values[A] = exact_support(p, noise, I, S, t, A)[0]
    return values


def check_stationarity(p, I, S, t, support, x):
    assert all(x[i] == 0 for i in I if i not in support)
    for i in support:
        assert (2 * sum(p.Q[i][j] * x[j] for j in I) + p.c[i]
                + 2 * sum(p.Q[i][j] * t[h] for h, j in enumerate(S))) == 0


def grid_exhaustion(p, noise, I, S, t, M, B, fixed):
    grid = [F(0)] if M == 0 else [-M + F(2 * j, B) * M for j in range(B + 1)]
    states = [(0, F(0))] + [(1, x) for x in grid]
    domains = [[s for s in states if i not in fixed or s[0] == fixed[i]] for i in I]
    best = None
    for assignment in product(*domains):
        A = tuple(i for i, (bit, _) in zip(I, assignment) if bit)
        x = {i: value for i, (_, value) in zip(I, assignment)}
        value = conditional_objective(p, noise, I, S, t, A, x)
        best = value if best is None else min(best, value)
        STATS['grid_assignments'] += 1
    return best


def check_grid_case(p, noise, I, S, t, radius, epsilon):
    M, L, B = message_parameters(p, S, radius, epsilon)
    assert M == (p.n * p.C + 2 * p.H * len(S) * radius) / (2 * p.mu)
    assert L == 2 * p.H * M
    assert B > 0 and B % 2 == 0
    assert B * B * epsilon >= p.H * p.n * M * M
    assert B == 2 or (B - 2) ** 2 * epsilon < p.H * p.n * M * M
    owned = factor_ownership(p, I)
    expected = Counter([(i,) for i in I] + [(i, j) for h, i in enumerate(I)
                                          for j in I[h + 1:] if p.Q[i][j]])
    assert Counter(factor for bag in owned for factor in bag) == expected
    for u, factors in enumerate(owned):
        assert all(set(factor) <= set(p.bags[u]) for factor in factors)
    for statuses in product((None, 0, 1), repeat=len(I)):
        fixed = {i: bit for i, bit in zip(I, statuses) if bit is not None}
        answer = restricted_oracle(p, noise, I, S, t, M, B, fixed)
        grid = answer.grid
        assert grid.value == grid_exhaustion(p, noise, I, S, t, M, B, fixed)
        assert grid.value == conditional_objective(p, noise, I, S, t, grid.support, grid.x)
        for i in I:
            if i not in grid.support:
                assert grid.x[i] == 0
            else:
                assert grid.x[i] in {(-M + F(2 * j, B) * M) for j in range(B + 1)}
        assert all(int(i in grid.support) == bit for i, bit in fixed.items())
        values = exhaustive_supports(p, noise, I, S, t, fixed)
        optimum = min(values.values())
        assert optimum <= answer.value <= optimum + epsilon
        assert answer.value == values[answer.support] <= grid.value
        assert answer.value == conditional_objective(p, noise, I, S, t, answer.support, answer.x)
        check_stationarity(p, I, S, t, answer.support, answer.x)
        STATS['strict_oracle_errors'] += answer.value > optimum
        STATS['reoptimization_improvements'] += answer.value < grid.value
        STATS['nonzero_edge_witnesses'] += any(
            p.Q[i][j] * grid.x[i] * grid.x[j] != 0
            for h, i in enumerate(I) for j in I[h + 1:])
        STATS['grid_restrictions'] += 1

    def oracle(fixed):
        return restricted_oracle(p, noise, I, S, t, M, B, fixed)
    outputs, calls = enumerate_near(I, oracle, epsilon, epsilon)
    values = exhaustive_supports(p, noise, I, S, t, {})
    optimum = min(values.values())
    assert len(outputs) == len(set(outputs))
    assert {A for A, v in values.items() if v <= optimum + epsilon} <= set(outputs)
    assert all(values[A] <= optimum + 3 * epsilon for A in outputs)
    assert calls <= 1 + len(I) * len(outputs)
    STATS['enumerations'] += 1


def check_branch_coefficients(p, noise, I, S):
    k = len(S)
    zero = (F(0),) * k
    unit = [tuple(F(i == j) for j in range(k)) for i in range(k)]
    for bits in product((0, 1), repeat=len(I)):
        A = tuple(i for i, bit in zip(I, bits) if bit)
        branch = support_branch(p, noise, A, S)

        def value(t):
            return exact_support(p, noise, I, S, t, A)[0]
        origin = value(zero)
        assert branch.constant == origin
        for j in range(k):
            plus, minus = value(unit[j]), value(tuple(-a for a in unit[j]))
            assert branch.linear[j] == (plus - minus) / 2
            assert branch.quadratic[j][j] == (plus + minus - 2 * origin) / 2
            for h in range(j):
                mixed = value(tuple(a + b for a, b in zip(unit[j], unit[h])))
                assert branch.quadratic[j][h] == branch.quadratic[h][j]
                assert 2 * branch.quadratic[j][h] == mixed - plus - value(unit[h]) + origin
        t = tuple(F(j + 1, 13) for j in range(k))
        x = dict.fromkeys(I, F(0))
        x.update(branch.optimizer(t))
        check_stationarity(p, I, S, t, A, x)
        assert branch.value(t) == conditional_objective(p, noise, I, S, t, A, x) == value(t)
        STATS['full_branches'] += 1


def independent_message_sets(p):
    result = set()
    for child, parent in enumerate(p.parents):
        if parent is None:
            continue
        descendants = []
        for u in range(len(p.bags)):
            ancestor = u
            while ancestor is not None and ancestor != child:
                ancestor = p.parents[ancestor]
            if ancestor == child:
                descendants.append(u)
        S = set(p.bags[child]) & set(p.bags[parent])
        I = set().union(*(set(p.bags[u]) for u in descendants)) - S
        result.add((child, tuple(sorted(I)), tuple(sorted(S))))
    result.add((None, tuple(range(p.n)), ()))
    return result


def check_all_messages(p, noise, radius, sigma):
    original_noise = tuple(noise)
    result = construct_all(p, noise, radius, sigma)
    assert tuple(noise) == original_noise
    assert len(result.messages) == len(p.bags)
    assert {(m.child, m.interior, m.boundary) for m in result.messages} == independent_message_sets(p)
    for message in result.messages:
        I, S = message.interior, message.boundary
        labels = {branch.support for branch in message.branches}
        for t in product(sorted({-radius, F(0), radius}), repeat=len(S)):
            exhaustive = exhaustive_supports(p, noise, I, S, t, {})
            best = min(exhaustive.values())
            winner = message.minimizing_branch(t)
            assert winner.value(t) == best
            assert {A for A, value in exhaustive.items() if value == best} <= labels
            x = dict.fromkeys(I, F(0))
            x.update(winner.optimizer(t))
            assert best == conditional_objective(p, noise, I, S, t, winner.support, x)
            check_stationarity(p, I, S, t, winner.support, x)
            STATS['boundary_probes'] += 1
        check_branch_coefficients(p, noise, I, S)
        STATS['messages'] += 1
        STATS['net_points'] += message.net_points
        STATS['dictionary_calls'] += message.oracle_calls
    I = tuple(range(p.n))
    original = min(exhaustive_supports(p, (F(0),) * p.n, I, (), (), {}).values())
    assert result.lower <= original <= result.upper
    assert result.upper - result.lower <= sum(abs(xi) for xi in noise) <= p.n * sigma
    x = dict(enumerate(result.x))
    assert result.value == conditional_objective(p, noise, I, (), (), result.support, x)
    assert result.upper == conditional_objective(p, (F(0),) * p.n, I, (), (), result.support, x)
    check_stationarity(p, I, (), (), result.support, x)
    STATS['certificates'] += 1
    return result


def check_sampling():
    class Bits:
        def __init__(self, values):
            self.values, self.calls = iter(values), []

        def getrandbits(self, bits):
            self.calls.append(bits)
            return next(self.values)

    for n in (1, 2, 3, 5):
        bits = (2 * n - 1).bit_length()
        N = 2 ** bits
        assert N >= 2 * n and N // 2 < 2 * n
        for endpoint in (0, N - 1):
            rng = Bits([endpoint] * n)
            sigma = F(7, 5)
            noise = sample_noise(n, sigma, rng)
            assert rng.calls == [bits] * n
            assert noise == ((-sigma if endpoint == 0 else sigma),) * n
            STATS['sampling_vectors'] += 1
        assert sample_noise(n, F(1), Random(51)) == sample_noise(n, F(1), Random(51))


def main():
    check_sampling()
    branching = problem(
        [[1, F(1, 4), 0, 0], [F(1, 4), 1, F(1, 4), 0],
         [0, F(1, 4), 1, 0], [0, 0, 0, 1]],
        [F(-1, 20), F(1, 30), F(-1, 40), F(1, 50)],
        [F(1, 10), F(-1, 20), 0, F(1, 5)],
        F(1, 2), F(3, 2), F(1, 20),
        [(1,), (0, 1), (1, 2), (), (3,), (1,)], [None, 0, 0, 0, 3, 0])
    signed = (F(1, 20), F(-1, 20), F(0), F(1, 10))
    check_grid_case(branching, signed, (0, 1, 2, 3), (), (), F(0), F(1, 4))
    check_grid_case(branching, signed, (0, 2, 3), (1,), (F(1, 10),), F(1, 10), F(1, 4))
    check_all_messages(branching, sample_noise(4, F(3, 2), Random(9)), F(1, 20), F(3, 2))

    coupled = problem([[1, F(-1, 4), 0], [F(-1, 4), 1, F(-1, 4)],
                       [0, F(-1, 4), 1]], [-1] * 3, [0] * 3,
                      F(1, 2), F(3, 2), 1,
                      [(1,), (0, 1), (1, 2)], [None, 0, 0])
    M, _, B = message_parameters(coupled, (), F(0), F(1, 2))
    witness = grid_minimize(coupled, (F(0),) * 3, (0, 1, 2), (), (), M, B, {})
    # Both child-owned edges have nonzero contributions in the optimal grid
    # witness, so this checks projection beyond all-zero minimizing assignments.
    assert all(coupled.Q[i][j] * witness.x[i] * witness.x[j] != 0
               for i, j in ((0, 1), (1, 2)))
    check_grid_case(coupled, (F(0),) * 3, (0, 1, 2), (), (), F(0), F(1, 2))

    nonsdd = problem([[1 if i == j else F(3, 5) for j in range(3)] for i in range(3)],
                     [F(1, 100), F(-1, 100), F(1, 200)],
                     [F(1, 10), F(-1, 20), 0], F(2, 5), F(11, 5), F(1, 100),
                     [(1, 2), (0, 1, 2)], [None, 0])
    # Q=(2/5)I+(3/5)11^T: eigenvalues 2/5,2/5,11/5; every row fails SDD.
    assert all(nonsdd.Q[i][j] == F(2, 5) * (i == j) + F(3, 5)
               for i in range(3) for j in range(3))
    assert nonsdd.mu == F(2, 5) and nonsdd.H == F(2, 5) + 3 * F(3, 5)
    assert all(sum(abs(nonsdd.Q[i][j]) for j in range(3) if j != i) > nonsdd.Q[i][i]
               for i in range(3))
    noise = sample_noise(3, F(3, 5), Random(7))
    check_grid_case(nonsdd, noise, (0, 1, 2), (), (), F(0), F(1, 20))
    check_grid_case(nonsdd, noise, (0,), (1, 2), (F(1, 100), F(-1, 100)), F(1, 100), F(1, 20))
    radius, epsilon = F(1, 50), F(1, 30)
    M, L, B = message_parameters(nonsdd, (1, 2), radius, epsilon)
    assert (M, L) == (F(103, 400), F(1133, 1000))
    net = tuple(midpoint_net(radius, 2, L, epsilon))
    expected_axis = (F(-1, 75), F(0), F(1, 75))
    assert net == tuple(product(expected_axis, repeat=2)) and len(net) == 9
    result = check_all_messages(nonsdd, noise, radius, F(3, 5))
    message = next(m for m in result.messages if m.boundary == (1, 2))
    assert message.net_points == 9
    for t in net:
        values = exhaustive_supports(nonsdd, noise, message.interior, message.boundary, t, {})
        assert message.minimizing_branch(t).value(t) == min(values.values())
        STATS['two_dimensional_net_probes'] += 1

    approximate = problem([[1]], [-1], [F(-11, 8)], 1, 1, 2, [(0,)], [None])
    noise, epsilon = (F(3, 2),), F(1, 4)
    M, _, B = message_parameters(approximate, (), F(0), epsilon)
    assert (M, B) == (F(1), 2)
    free = restricted_oracle(approximate, noise, (0,), (), (), M, B, {})
    active = restricted_oracle(approximate, noise, (0,), (), (), M, B, {0: 1})
    assert free.value == 0 and free.support == ()
    assert active.grid.value == F(1, 8) and active.value == F(-1, 8) and active.x[0] == F(1, 2)
    check_grid_case(approximate, noise, (0,), (), (), F(0), epsilon)
    result = check_all_messages(approximate, noise, F(0), F(3, 2))
    assert result.support == (0,) and result.value == F(-1, 8)

    constant = problem([[1]], [0], [F(-5, 6)], 1, 1, 0, [(0,)], [None])
    check_grid_case(constant, (F(1),), (0,), (), (), F(0), F(1, 6))
    check_grid_case(constant, (F(1),), (), (), (), F(0), F(1, 6))
    result = check_all_messages(constant, (F(1),), F(0), F(1))
    assert {b.support for b in result.messages[0].branches} == {(), (0,)}
    assert result.support == () and result.value == 0
    signed_zero = problem([[1]], [0], [-2], 1, 1, 0, [(), (0,), (0,)], [None, 0, 1])
    result = check_all_messages(signed_zero, (F(1),), F(0), F(1))
    assert result.support == (0,) and result.x == (F(0),)

    radius, sigma = F(1, 10), F(6, 5)
    for offset in (F(0), radius * radius / 16):
        noise = (sigma, -sigma)
        tie = problem([[1, F(1, 4)], [F(1, 4), 1]], [0, 0],
                      [offset - sigma, sigma + 1], F(3, 4), F(5, 4), F(1, 10),
                      [(1,), (0, 1)], [None, 0])
        message = construct_message(tie, noise, (0,), (1,), radius, sigma)
        M, L, B = message_parameters(tie, (1,), radius, sigma / 12)
        net = tuple(midpoint_net(radius, 1, L, sigma / 12))
        assert net == ((F(-1, 20),), (F(1, 20),))
        assert {b.support for b in message.branches} == {(), (0,)}
        active = next(b for b in message.branches if b.support)
        assert active.constant == offset and active.linear == (F(0),)
        assert active.quadratic == ((F(-1, 16),),)
        if offset == 0:
            assert active.value((F(0),)) == 0
            assert all(active.value(t) < 0 for t in net)
        else:
            assert active.value((-radius,)) == active.value((radius,)) == 0
            assert all(active.value(t) > 0 for t in net)
        check_all_messages(tie, noise, radius, sigma)
        check_grid_case(tie, noise, (0,), (1,), (F(0),), F(0), sigma / 12)
        STATS['designed_tie_cases'] += 1

    # A valid long decomposition must not be limited by Python recursion depth.
    long = problem([[1]], [0], [-2], 1, 1, 0, [(0,)] * 1100, [None] + list(range(1099)))
    grid = grid_minimize(long, (F(1),), (0,), (), (), F(0), 2, {})
    assert grid.support == (0,) and grid.x == {0: F(0)} and grid.value == -1
    for bound in (F(0), F(1, 13), F(3, 2), F(10)):
        B = least_even_mesh(F(7, 3), 4, bound, F(1, 17))
        assert B * B * F(1, 17) >= F(7, 3) * 4 * bound * bound
        assert B == 2 or (B - 2) ** 2 * F(1, 17) < F(7, 3) * 4 * bound * bound

    assert (STATS['strict_oracle_errors'] > 0 and STATS['reoptimization_improvements'] > 0
            and STATS['nonzero_edge_witnesses'] > 0)
    print(f"PASS: {STATS['grid_restrictions']} restricted bag-DP/oracle checks against "
          f"{STATS['grid_assignments']} grid assignments; {STATS['strict_oracle_errors']} strictly "
          f"suboptimal oracle returns; {STATS['reoptimization_improvements']} strict reoptimization improvements; "
          f"{STATS['nonzero_edge_witnesses']} witnesses with a nonzero edge term")
    print(f"PASS: {STATS['enumerations']} enumeration contracts; {STATS['messages']} direct messages; "
          f"{STATS['net_points']} net points; {STATS['dictionary_calls']} construction oracle calls; "
          f"{STATS['boundary_probes']} finite boundary probes; {STATS['full_branches']} coefficient checks")
    print(f"PASS: {STATS['support_qps']} independent support QPs; {STATS['certificates']} original-objective "
          f"certificates; {STATS['designed_tie_cases']} designed tie cases; {STATS['sampling_vectors']} "
          f"endpoint/bit-count sampling cases; {STATS['two_dimensional_net_probes']} two-dimensional "
          "net probes; non-SDD spectral example; 1100-bag path")


if __name__ == '__main__':
    main()
