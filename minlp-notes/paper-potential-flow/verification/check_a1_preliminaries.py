#!/usr/bin/env python3
"""Deterministic numerical checks of A1; no third-party dependencies.

The state solver minimizes the whole graph's primitive energy in a generic
fundamental-cycle basis. It receives no blocks or aggregated nominations.
Exact line minimization uses Decimal bisection; a global cycle-gradient
check and all passive-equation residuals guard convergence. Blocks are
found separately by Tarjan's edge-stack algorithm. This is numerical
regression evidence, not a proof or a certified optimization algorithm.
"""

from collections import deque
from decimal import Decimal, localcontext
from fractions import Fraction
import random
import sys

ZERO = Decimal(0)
ONE = Decimal(1)
TOL = Decimal('1e-9')
ROOT_TOL = Decimal('1e-40')
GRAD_TOL = Decimal('1e-28')
MAX_ERROR = ZERO
CHECKS = 0


def dec(value):
    if isinstance(value, Fraction):
        return Decimal(value.numerator) / Decimal(value.denominator)
    return Decimal(value)


def check(condition, message):
    global CHECKS
    CHECKS += 1
    if not condition:
        raise AssertionError(message)


def close(left, right, message):
    global MAX_ERROR
    error = abs(dec(left) - dec(right))
    MAX_ERROR = max(MAX_ERROR, error)
    check(error <= TOL, f'{message}: error {error}')


def adjacency(n, edges, chosen=None):
    adj = [[] for _ in range(n)]
    for e in range(len(edges)) if chosen is None else chosen:
        u, v, _ = edges[e]
        adj[u].append((v, e, 1))
        adj[v].append((u, e, -1))
    return adj


def path(adj, start, end):
    parents = {start: None}
    queue = deque([start])
    while queue and end not in parents:
        u = queue.popleft()
        for v, e, sign in adj[u]:
            if v not in parents:
                parents[v] = (u, e, sign)
                queue.append(v)
    check(end in parents, 'path endpoints disconnected')
    result = []
    v = end
    while v != start:
        u, e, sign = parents[v]
        result.append((u, v, e, sign))
        v = u
    return list(reversed(result))


def bracket_root(function):
    lo, hi = -ONE, ONE
    for _ in range(300):
        if function(lo) <= 0 <= function(hi):
            break
        lo *= 2
        hi *= 2
    else:
        raise AssertionError('root bracketing failed')
    check(function(lo) <= 0 <= function(hi), 'invalid root bracket')
    for _ in range(500):
        mid = (lo + hi) / 2
        value = function(mid)
        if value == 0:
            return mid
        if value < 0:
            lo = mid
        else:
            hi = mid
        if hi - lo <= ROOT_TOL:
            return (lo + hi) / 2
    raise AssertionError('root bisection failed')


def solve(n, edges, nomination):
    """Minimize sum beta |x|^3/3 over Ax=b, without using any blocks."""
    check(sum(nomination) == 0, 'unbalanced solver input')
    adj = adjacency(n, edges)
    parents = {0: None}
    order = [0]
    tree = []
    for u in order:
        for v, e, sign in adj[u]:
            if v not in parents:
                parents[v] = (u, e, sign)
                order.append(v)
                tree.append(e)
    check(len(order) == n, 'solver input disconnected')
    # A feasible routing is computed exactly before numerical minimization.
    surplus = list(map(Fraction, nomination))
    routing = [Fraction(0) for _ in edges]
    for v in reversed(order[1:]):
        u, e, sign = parents[v]
        routing[e] = -sign * surplus[v]
        surplus[u] += surplus[v]
    x = list(map(dec, routing))
    tree_adj = adjacency(n, edges, tree)
    tree_set = set(tree)
    cycles = []
    for e, (u, v, _) in enumerate(edges):
        if e not in tree_set:
            cycles.append([(e, 1)] + [(j, sign) for _, _, j, sign
                                     in path(tree_adj, v, u)])
    beta = [dec(edge[2]) for edge in edges]

    def gradient(cycle):
        return sum((sign * beta[e] * x[e] * abs(x[e])
                    for e, sign in cycle), ZERO)

    for _ in range(2000):
        if all(abs(gradient(c)) <= GRAD_TOL for c in cycles):
            break
        for cycle in cycles:
            def derivative(step):
                return sum((sign * beta[e] * (x[e] + sign * step)
                            * abs(x[e] + sign * step)
                            for e, sign in cycle), ZERO)
            step = bracket_root(derivative)
            for e, sign in cycle:
                x[e] += sign * step
    else:
        raise AssertionError('whole-graph energy minimization did not converge')
    check(all(abs(gradient(c)) <= GRAD_TOL for c in cycles),
          'global first-order condition failed')
    pi = [ZERO for _ in range(n)]
    for v in order[1:]:
        u, e, sign = parents[v]
        pi[v] = pi[u] - sign * beta[e] * x[e] * abs(x[e])
    divergence = [ZERO for _ in range(n)]
    for e, (u, v, _) in enumerate(edges):
        divergence[u] += x[e]
        divergence[v] -= x[e]
        close(pi[u] - pi[v], beta[e] * x[e] * abs(x[e]), 'edge law')
    for v in range(n):
        close(divergence[v], nomination[v], 'conservation')
    return x, pi


def blocks(n, edges):
    """Tarjan edge blocks; edge IDs distinguish parallel parent edges."""
    adj = adjacency(n, edges)
    discovery = [-1] * n
    low = [-1] * n
    stack, result = [], []
    clock = 0

    def visit(u, parent_edge):
        nonlocal clock
        discovery[u] = low[u] = clock
        clock += 1
        for v, e, _ in adj[u]:
            if e == parent_edge:
                continue
            if discovery[v] == -1:
                stack.append(e)
                visit(v, e)
                low[u] = min(low[u], low[v])
                if low[v] >= discovery[u]:
                    block = []
                    while True:
                        j = stack.pop()
                        block.append(j)
                        if j == e:
                            break
                    result.append(sorted(block))
            elif discovery[v] < discovery[u]:
                stack.append(e)
                low[u] = min(low[u], discovery[v])
    visit(0, None)
    check(sorted(e for block in result for e in block) == list(range(len(edges))),
          'blocks do not partition edges')
    return result


def component(n, edges, removed, start):
    adj = adjacency(n, edges, [e for e in range(len(edges)) if e not in removed])
    seen = {start}
    queue = deque([start])
    while queue:
        for v, _, _ in adj[queue.popleft()]:
            if v not in seen:
                seen.add(v)
                queue.append(v)
    return seen


def verify_graph(n, edges, b):
    x, pi = solve(n, edges, b)
    edge_blocks = blocks(n, edges)
    incidence = [[] for _ in range(n + len(edge_blocks))]
    local_potentials = []
    rank_sum = 0
    for i, block in enumerate(edge_blocks):
        vertices = sorted({v for e in block for v in edges[e][:2]})
        indices = {v: j for j, v in enumerate(vertices)}
        local_edges = [(indices[edges[e][0]], indices[edges[e][1]], edges[e][2])
                       for e in block]
        aggregates, parts = [], []
        for v in vertices:
            part = component(n, edges, set(block), v)
            check(part.intersection(vertices) == {v}, 'ambiguous block attachment')
            parts.append(part)
            aggregates.append(sum((b[w] for w in part), Fraction(0)))
            incidence[v].append((n + i, i, 1))
            incidence[n + i].append((v, i, -1))
        check(sum(map(len, parts)) == n and set.union(*parts) == set(range(n)),
              'aggregated sets do not partition vertices')
        local_x, local_pi = solve(len(vertices), local_edges, aggregates)
        local_potentials.append(dict(zip(vertices, local_pi)))
        for j, e in enumerate(block):
            close(x[e], local_x[j], 'block flow restriction')
        for u in vertices:
            for v in vertices:
                close(pi[u] - pi[v], local_pi[indices[u]] - local_pi[indices[v]],
                      'block potential restriction')
        if len(block) == 1:
            e = block[0]
            tail_component = component(n, edges, {e}, edges[e][0])
            close(x[e], sum((b[v] for v in tail_component), Fraction(0)),
                  'bridge tail-component nomination')
        degree = [len(a) for a in adjacency(len(vertices), local_edges)]
        rank = len(block) - len(vertices) + 1
        rank_sum += rank
        check(sum(d - 2 for d in degree) == 2 * rank - 2, 'degree-count identity')
        if len(block) > 1:
            check(min(degree) >= 2 and sum(d >= 3 for d in degree) <= 2 * rank - 2,
                  'nonbridge branching-vertex bound')
    check(rank_sum == len(edges) - n + 1, 'total rank is not sum of block ranks')
    # Every pair, including endpoints at cut vertices, checks the block path.
    for s in range(n):
        for t in range(s, n):
            route = path(incidence, s, t)
            check(len(route) % 2 == 0, 'invalid block incidence path')
            total = ZERO
            for j in range(0, len(route), 2):
                u, block_node, _, _ = route[j]
                _, v, _, _ = route[j + 1]
                local = local_potentials[block_node - n]
                total += local[u] - local[v]
            close(pi[s] - pi[t], total, 'block-path potential sum')
    dissipation = sum((dec(beta) * abs(x[e]) ** 3
                       for e, (_, _, beta) in enumerate(edges)), ZERO)
    close(sum((dec(b[v]) * pi[v] for v in range(n)), ZERO), dissipation,
          'dissipation identity')
    for q in (Fraction(0), Fraction(1, 3), Fraction(5, 2)):
        scaled_x, scaled_pi = solve(n, edges, [q * v for v in b])
        for e in range(len(edges)):
            close(scaled_x[e], dec(q) * x[e], 'homogeneous flow')
        for v in range(n):
            close(scaled_pi[v], dec(q * q) * pi[v], 'homogeneous potential')
    return len(edge_blocks)


def generate(rng, trial):
    """Glue random cycles and paths at old vertices; vary edge order and signs."""
    n, edges = 1, []
    for part in range(rng.randint(3, 6)):
        attach = rng.randrange(n)
        length = rng.randint(2, 5)
        is_cycle = (part % 2 == 0)
        walk = [attach] + list(range(n, n + length - (1 if is_cycle else 0)))
        n = max(walk) + 1
        if is_cycle:
            walk.append(attach)
        for u, v in zip(walk, walk[1:]):
            if rng.randrange(2):
                u, v = v, u
            edges.append((u, v, Fraction(rng.randint(1, 7), rng.randint(1, 5))))
    # Some extra tests have a rank-two block, exercising a coupled cycle solve
    # and a nonzero branching-vertex bound rather than only degree-two cycles.
    if trial % 6 == 0:
        attach, end = rng.randrange(n), n
        n += 1
        for _ in range(3):
            mid = n
            n += 1
            edges.extend([(attach, mid, Fraction(1)), (mid, end, Fraction(2))])
    rng.shuffle(edges)
    b = [Fraction(rng.randint(-5, 5), rng.randint(1, 4)) for _ in range(n - 1)]
    b.append(-sum(b))
    if not any(b):
        b[0], b[-1] = Fraction(1), Fraction(-1)
    check(any(b) and sum(b) == 0, 'generated nomination must be nonzero and balanced')
    return n, edges, b


def verify_cycles(rng):
    for _ in range(30):
        size = rng.randint(2, 8)
        b = [Fraction(rng.randint(-7, 7), 3) for _ in range(size - 1)]
        b.append(-sum(b))
        beta = [Fraction(rng.randint(1, 9), rng.randint(1, 5)) for _ in b]
        # Chord is last edge, oriented size-1 -> 0; other edges form a path.
        ell, running = [], Fraction(0)
        for value in b:
            running += value
            ell.append(running)
        check(ell[-1] == 0, 'nonzero spanning-path chord routing')

        def phi(q):
            return sum((dec(be) * (q + dec(le)) * abs(q + dec(le))
                        for be, le in zip(beta, ell)), ZERO)
        q = bracket_root(phi)
        check(phi(q - Decimal('1e-12')) < 0 < phi(q + Decimal('1e-12')),
              'cycle root lacks strict sign bracket')
        samples = [dec(j) / 7 for j in range(-30, 31)]
        check(all(phi(a) < phi(c) for a, c in zip(samples, samples[1:])),
              'cycle function not strictly increasing on test grid')
        edges = [(i, (i + 1) % size, beta[i]) for i in range(size)]
        x, _ = solve(size, edges, b)
        for i in range(size):
            close(x[i], q + dec(ell[i]), 'cycle parametrization')

    for a in (Fraction(1), Fraction(2), Fraction(3), Fraction(9, 4), Fraction(5, 7)):
        # Exact symbolic arithmetic in Q[r]/(r^2-a); q=r/(1+r).
        # For a != 1, q=(a-r)/(a-1). Squaring coefficient pairs verifies
        # q^2=a(1-q)^2 with Fractions, without substituting a float root.
        def square(pair):
            u, v = pair
            return (u * u + a * v * v, 2 * u * v)
        if a == 1:
            qpair = (Fraction(1, 2), Fraction(0))
        else:
            qpair = (a / (a - 1), -Fraction(1) / (a - 1))
        complement = (1 - qpair[0], -qpair[1])
        check(square(qpair) == tuple(a * c for c in square(complement)),
              'exact parallel-edge squared identity')
        root = dec(a).sqrt()
        expected = root / (1 + root)
        check(0 < expected < 1, 'parallel root has wrong sign branch')
        x, _ = solve(2, [(0, 1, Fraction(1)), (1, 0, a)],
                     [Fraction(1), Fraction(-1)])
        close(x[0], expected, 'parallel two-edge root')
        close(x[1], expected - 1, 'parallel reverse-oriented flow')


def main():
    rng = random.Random(6001)
    with localcontext() as context:
        context.prec = 60
        total_blocks = 0
        for trial in range(24):
            total_blocks += verify_graph(*generate(rng, trial))
        # A separate zero-nomination cycle regression preserves this boundary
        # case without suppressing any generated coupled rank-two solve.
        verify_graph(3, [(0, 1, Fraction(1)), (1, 2, Fraction(2)),
                         (2, 0, Fraction(3))], [Fraction(0)] * 3)
        # Degenerate topology and bridge signs are explicit regressions.
        verify_graph(1, [], [Fraction(0)])
        verify_graph(2, [(1, 0, Fraction(2))], [Fraction(3), Fraction(-3)])
        verify_cycles(rng)
    print(f'PASS: 24 glued graphs ({total_blocks} blocks), singleton/bridge cases, '
          'a zero-nomination cycle, 30 cycle brackets, and 5 exact parallel identities.')
    print(f'PASS: {CHECKS} checks; maximum numerical error {MAX_ERROR:.3E} '
          f'(tolerance {TOL}).')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (AssertionError, ArithmeticError) as error:
        print(f'FAIL: {error}', file=sys.stderr)
        sys.exit(1)
