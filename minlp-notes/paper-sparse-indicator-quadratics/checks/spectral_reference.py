"""Exact reference for the spectral message algorithm (standard library only).

Inputs are valid rational data: Q is symmetric positive definite with the
supplied mu/H bounds, |c_i| <= C, and bags/parents are a valid rooted tree
decomposition. Vertices are 0,...,n-1; each bag lists distinct vertices.
Assume n >= 1, 0 < mu <= H, C and radius >= 0, epsilon and sigma > 0,
and |noise_i| <= sigma. Interior and boundary are disjoint ordered vertex sets.
Every numerical entry, bound, radius, accuracy, noise value, and perturbation
scale must be a Fraction; vertex indices and fixed bits are integers.
This small research implementation deliberately omits production validation,
numerical solvers, CAD, and recursive SDD methods.
The optimization oracle uses bag tables, never exhaustive support enumeration.
"""

from dataclasses import dataclass
from fractions import Fraction as F
from heapq import heappop, heappush
from itertools import product


@dataclass(frozen=True)
class Problem:
    Q: tuple
    c: tuple
    penalties: tuple
    mu: F
    H: F
    C: F
    bags: tuple
    parents: tuple

    @property
    def n(self):
        return len(self.c)


def solve_linear(matrix, rhs):
    """Rational elimination; the supplied principal matrices are nonsingular."""
    n = len(rhs)
    a = [[F(x) for x in row] + [F(rhs[i])] for i, row in enumerate(matrix)]
    for j in range(n):
        pivot = next(i for i in range(j, n) if a[i][j])
        a[j], a[pivot] = a[pivot], a[j]
        scale = a[j][j]
        a[j] = [x / scale for x in a[j]]
        for i in range(n):
            if i != j:
                scale = a[i][j]
                a[i] = [x - scale * y for x, y in zip(a[i], a[j])]
    return tuple(row[-1] for row in a)


@dataclass(frozen=True)
class Branch:
    """F_A(t) = constant + linear*t + t^T quadratic*t, including noise."""
    support: tuple
    constant: F
    linear: tuple
    quadratic: tuple
    intercept: tuple
    response: tuple

    def value(self, t):
        return (self.constant + sum(a * x for a, x in zip(self.linear, t))
                + sum(t[i] * a * t[j] for i, row in enumerate(self.quadratic)
                      for j, a in enumerate(row)))

    def optimizer(self, t):
        return {i: self.intercept[h] + sum(a * x for a, x in zip(self.response[h], t))
                for h, i in enumerate(self.support)}


def support_branch(problem, noise, support, boundary):
    """Full noisy Schur quadratic and its affine support minimizer."""
    A, S = tuple(support), tuple(boundary)
    matrix = tuple(tuple(problem.Q[i][j] for j in A) for i in A)
    inverse_c = solve_linear(matrix, tuple(problem.c[i] for i in A))
    inverse_columns = [solve_linear(matrix, tuple(problem.Q[i][j] for i in A))
                       for j in S]
    constant = (sum((problem.penalties[i] + noise[i] for i in A), F(0))
                - sum((problem.c[i] * inverse_c[h] for h, i in enumerate(A)), F(0)) / 4)
    linear = tuple(-sum((problem.Q[j][i] * inverse_c[h]
                         for h, i in enumerate(A)), F(0)) for j in S)
    quadratic = tuple(tuple(-sum((problem.Q[j][i] * inverse_columns[k][h]
                                  for h, i in enumerate(A)), F(0))
                            for k in range(len(S))) for j in S)
    intercept = tuple(-a / 2 for a in inverse_c)
    response = tuple(tuple(-column[h] for column in inverse_columns)
                     for h in range(len(A)))
    return Branch(A, constant, linear, quadratic, intercept, response)


def rooted_tree(problem):
    children = [[] for _ in problem.bags]
    root = problem.parents.index(None)
    for u, parent in enumerate(problem.parents):
        if parent is not None:
            children[parent].append(u)
    order, depth = [], [0] * len(children)

    stack = [root]
    while stack:
        u = stack.pop()
        order.append(u)
        for v in children[u]:
            depth[v] = depth[u] + 1
        stack.extend(reversed(children[u]))
    return root, children, order, depth


def factor_ownership(problem, interior):
    """Assign each unary/nonzero edge factor to its highest containing bag."""
    I = tuple(interior)
    _, _, _, depth = rooted_tree(problem)
    factors = [(i,) for i in I]
    factors += [(i, j) for h, i in enumerate(I) for j in I[h + 1:]
                if problem.Q[i][j] != 0]
    owned = [[] for _ in problem.bags]
    for factor in factors:
        owner = min((u for u, bag in enumerate(problem.bags)
                     if all(i in bag for i in factor)), key=lambda u: (depth[u], u))
        owned[owner].append(factor)
    return owned


def least_even_mesh(H, n, M, epsilon):
    """Least positive even B with B^2 epsilon >= H n M^2; no square roots."""
    threshold = H * n * M * M
    low, high = 0, 1
    while 4 * high * high * epsilon < threshold:
        high *= 2
    while high - low > 1:
        middle = (low + high) // 2
        if 4 * middle * middle * epsilon >= threshold:
            high = middle
        else:
            low = middle
    return 2 * high


def message_parameters(problem, boundary, radius, epsilon):
    # The message-specific bound M_k is valid; the theorem uses its common
    # upper bound only to express one work bound for all messages.
    M = (problem.n * problem.C + 2 * problem.H * len(boundary) * radius) / (2 * problem.mu)
    L = 2 * problem.H * M
    return M, L, least_even_mesh(problem.H, problem.n, M, epsilon)


@dataclass(frozen=True)
class GridResult:
    value: F
    support: tuple
    x: dict


def grid_minimize(problem, noise, interior, boundary, t, M, B, fixed):
    """Finite-domain tree DP with projected child tables and back-pointers."""
    I, S = tuple(interior), tuple(boundary)
    interior_set = set(I)
    bags = [tuple(i for i in bag if i in interior_set) for bag in problem.bags]
    root, children, order, _ = rooted_tree(problem)
    grid = tuple(-M + 2 * M * j / B for j in range(B + 1)) if M else (F(0),)
    states = ((0, F(0)),) + tuple((1, x) for x in grid)
    domains = {i: tuple(h for h, (z, _) in enumerate(states)
                        if i not in fixed or z == fixed[i]) for i in I}
    effective = {i: problem.c[i] + 2 * sum(problem.Q[i][j] * t[h]
                                          for h, j in enumerate(S)) for i in I}
    owned = factor_ownership(problem, I)
    tables, projected, separators = {}, {}, {}
    for u in reversed(order):
        table = {}
        for state in product(*(domains[i] for i in bags[u])):
            assignment = dict(zip(bags[u], state))
            value = F(0)
            for factor in owned[u]:
                i = factor[0]
                z, x = states[assignment[i]]
                if len(factor) == 1:
                    value += (problem.Q[i][i] * x * x + effective[i] * x
                              + (problem.penalties[i] + noise[i]) * z)
                else:
                    j = factor[1]
                    value += 2 * problem.Q[i][j] * x * states[assignment[j]][1]
            for v in children[u]:
                key = tuple(assignment[i] for i in separators[v])
                value += projected[v][key][0]
            table[state] = value
        tables[u] = table
        if u != root:
            separator = tuple(sorted(set(bags[u]) & set(bags[problem.parents[u]])))
            separators[u] = separator
            positions = tuple(bags[u].index(i) for i in separator)
            projection = {}
            for state, value in table.items():
                key = tuple(state[h] for h in positions)
                candidate = (value, state)
                if key not in projection or candidate < projection[key]:
                    projection[key] = candidate
            projected[u] = projection
    value, root_state = min((value, state) for state, value in tables[root].items())
    witness = {}

    pending = [(root, root_state)]
    while pending:
        u, state = pending.pop()
        assignment = dict(zip(bags[u], state))
        witness.update(assignment)
        for v in children[u]:
            key = tuple(assignment[i] for i in separators[v])
            pending.append((v, projected[v][key][1]))
    support = tuple(i for i in I if states[witness[i]][0])
    return GridResult(value, support, {i: states[witness[i]][1] for i in I})


@dataclass(frozen=True)
class Candidate:
    support: tuple
    value: F
    x: dict
    grid: GridResult


def restricted_oracle(problem, noise, interior, boundary, t, M, B, fixed):
    grid = grid_minimize(problem, noise, interior, boundary, t, M, B, fixed)
    branch = support_branch(problem, noise, grid.support, boundary)
    x = dict.fromkeys(interior, F(0))
    x.update(branch.optimizer(t))
    return Candidate(grid.support, branch.value(t), x, grid)


def enumerate_near(interior, oracle, epsilon, delta):
    """First-difference enumeration with fixed U and cached approximate values."""
    heap, outputs = [], []
    calls = serial = 0

    def query(fixed):
        nonlocal calls, serial
        calls += 1
        candidate = oracle(fixed)
        if candidate is not None:
            serial += 1
            heappush(heap, (candidate.value - epsilon, serial, fixed, candidate))
        return candidate

    upper = query({}).value
    while heap and heap[0][0] <= upper + delta:
        _, _, fixed, candidate = heappop(heap)
        outputs.append(candidate.support)
        active = set(candidate.support)
        prefix = dict(fixed)
        for i in interior:
            if i not in fixed:
                child = dict(prefix)
                child[i] = 1 - int(i in active)
                query(child)
                prefix[i] = int(i in active)
    return tuple(outputs), calls


def midpoint_net(radius, dimension, L, epsilon):
    if dimension == 0:
        return ((),)
    if radius == 0 or L == 0:
        return ((F(0),) * dimension,)
    ratio = 2 * dimension * radius * L / epsilon
    h = max(1, -(-ratio.numerator // ratio.denominator))
    points = tuple(-radius + radius * F(2 * j + 1, h) for j in range(h))
    return product(points, repeat=dimension)


@dataclass(frozen=True)
class Message:
    child: object
    interior: tuple
    boundary: tuple
    branches: tuple
    net_points: int
    oracle_calls: int

    def minimizing_branch(self, t):
        return min(self.branches, key=lambda branch: (branch.value(t), branch.support))


def construct_message(problem, noise, interior, boundary, radius, sigma, child=None):
    I, S = tuple(interior), tuple(boundary)
    epsilon = sigma / (6 * problem.n)
    M, L, B = message_parameters(problem, S, radius, epsilon)
    labels, points, calls = set(), 0, 0
    for t in midpoint_net(radius, len(S), L, epsilon):
        def oracle(fixed):
            return restricted_oracle(problem, noise, I, S, t, M, B, fixed)
        found, used = enumerate_near(I, oracle, epsilon, epsilon)
        labels.update(found)
        points += 1
        calls += used
    branches = tuple(support_branch(problem, noise, A, S) for A in sorted(labels))
    return Message(child, I, S, branches, points, calls)


def message_sets(problem):
    root, children, order, _ = rooted_tree(problem)
    subtree = {}
    for u in reversed(order):
        vertices = set(problem.bags[u])
        for v in children[u]:
            vertices.update(subtree[v])
        subtree[u] = vertices
    result = []
    for u in order:
        if u != root:
            S = set(problem.bags[u]) & set(problem.bags[problem.parents[u]])
            result.append((u, tuple(sorted(subtree[u] - S)), tuple(sorted(S))))
    result.append((None, tuple(range(problem.n)), ()))
    return tuple(result)


def sample_noise(n, sigma, rng):
    """Exactly log2(N) requested bits per coordinate, with minimal power N >= 2n.

    The noise model assumes rng.getrandbits(k) gives independent uniform k-bit
    integers; a seeded random.Random supplies reproducible diagnostic samples.
    """
    bits = (2 * n - 1).bit_length()
    N = 1 << bits
    return tuple(-sigma + 2 * sigma * F(rng.getrandbits(bits), N - 1)
                 for _ in range(n))


@dataclass(frozen=True)
class Result:
    messages: tuple
    support: tuple
    x: tuple
    value: F
    lower: F
    upper: F


def construct_all(problem, noise, radius, sigma):
    """Build messages directly with one supplied noise vector; return a certificate."""
    messages = tuple(construct_message(problem, noise, I, S, radius, sigma, child)
                     for child, I, S in message_sets(problem))
    winner = messages[-1].minimizing_branch(())
    active_values = winner.optimizer(())
    x = tuple(active_values.get(i, F(0)) for i in range(problem.n))
    value = winner.constant
    lower = value - sum(max(a, F(0)) for a in noise)
    upper = value - sum(noise[i] for i in winner.support)
    return Result(messages, winner.support, x, value, lower, upper)
