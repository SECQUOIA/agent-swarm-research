#!/usr/bin/env python3
"""Exact checks of structural and residual extensions, using original bus laws.

The established builder supplies topology, but injections are independently
aggregated edge by edge. No numerical solver or third-party package is used.
Finite checks do not replace the topological or analytic proofs.
"""

from collections import deque
from dataclasses import replace
from fractions import Fraction as F
from itertools import product
import json
import random

from check_resistive_exact import Network, FREE, build, profile


def powers(net, v):
    current = dict.fromkeys(net.buses, F(0))
    for (i, j), g in net.edges.items():
        flow = g * (v[i] - v[j])
        current[i] += flow
        current[j] -= flow
    result = {i: v[i] * current[i] for i in net.buses}
    assert sum(result.values(), F(0)) == sum(
        (g * (v[i] - v[j])**2 for (i, j), g in net.edges.items()), F(0))
    return result


def box_check(net, v):
    assert set(v) == set(net.buses)
    assert all(b.voltage[0] <= v[i] <= b.voltage[1]
               for i, b in net.buses.items())


def violations(net, v):
    p = powers(net, v)
    return {i: max(F(0), b.injection[0] - p[i], p[i] - b.injection[1])
            for i, b in net.buses.items()}


def source_residual(equations, x):
    return max((abs(x[e[1]] + x[e[2]] - x[e[3]]) if e[0] == 'add'
                else abs(x[e[1]] * x[e[2]] - 1)
                for e in equations), default=F(0))


def widened(variables, equations, sum_variables=()):
    """Reuse only the proven topology; substitute all generalized bus data."""
    net = build(variables, equations)
    roots = set(net.roots.values())
    for i, b in list(net.buses.items()):
        if b.kind == 'value':
            bounds = (F(1), F(4)) if b.variable in sum_variables else (F(1, 2), F(2))
            net.buses[i] = replace(b, voltage=bounds if i in roots else (F(1, 2), F(4)))
        elif b.kind == 'inversion':
            net.buses[i] = replace(b, voltage=(F(1, 2), F(4)))
        elif b.kind in ('copy', 'tie'):
            net.buses[i] = replace(b, injection=(F(-5, 2),) * 2)
        elif b.kind == 'addition':
            net.buses[i] = replace(b, injection=(F(-3, 2),) * 2)
        elif b.kind == 'linear':
            net.buses[i] = replace(b, injection=(F(-17, 2),) * 2)
    return net


def wide_profile(net, x):
    v = {}
    for i, b in net.buses.items():
        if b.kind == 'value':
            v[i] = F(9, 2) - x[b.variable] if b.parity else x[b.variable]
        elif b.kind == 'inversion':
            v[i] = x[b.variable]
        elif b.kind == 'auxiliary':
            a = x[b.variable]
            v[i] = 2 * a - 1 + 1/a
        else:
            v[i] = F(1)
    return v


def adjacency(net):
    adj = {i: [] for i in net.buses}
    for i, j in net.edges:
        adj[i].append(j)
        adj[j].append(i)
    return adj


def components(net):
    adj = adjacency(net)
    remaining = set(adj)
    result = []
    while remaining:
        todo = [min(remaining)]
        comp = set(todo)
        remaining.difference_update(comp)
        while todo:
            for j in adj[todo.pop()]:
                if j in remaining:
                    remaining.remove(j)
                    comp.add(j)
                    todo.append(j)
        result.append(comp)
    return result


def connect(net, v):
    """Add the fixed-voltage connector path to the actual network object."""
    old_roots = set(net.roots.values())
    last = None
    for comp in components(net):
        root = min(comp & old_roots)
        assert len(list(net.neighbors(root))) <= 2
        assert net.buses[root].injection == FREE
        new = net.bus('connector', (1, 1), FREE)
        v[new] = F(1)
        net.edge(root, new)
        if last is not None:
            net.edge(last, new)
        last = new
    assert len(components(net)) == 1
    return net, v


def subdivide(net, v, length_scale):
    out = Network((), ())
    out.buses = dict(net.buses)
    for i, b in list(out.buses.items()):
        out.buses[i] = replace(b, injection=tuple(p / (4 * length_scale)
                                                for p in b.injection))
    w = dict(v)
    for (i, j), conductance in net.edges.items():
        count = int(4 * length_scale / conductance)
        assert F(count) == 4 * length_scale / conductance
        previous = i
        for step in range(1, count):
            new = out.bus('subdivision', (F(1, 2), 4), (0, 0))
            out.edge(previous, new)
            w[new] = ((count - step) * v[i] + step * v[j]) / count
            previous = new
        out.edge(previous, j)
    return out, w


def bipartite_and_girth(net):
    adj = adjacency(net)
    colors = {}
    for comp in components(net):
        root = min(comp)
        colors[root] = 0
        todo = deque([root])
        while todo:
            i = todo.popleft()
            for j in adj[i]:
                if j not in colors:
                    colors[j] = 1 - colors[i]
                    todo.append(j)
                assert colors[j] != colors[i]
    girth = float('inf')
    for root in adj:
        distances, parents = {root: 0}, {root: None}
        todo = deque([root])
        while todo:
            i = todo.popleft()
            for j in adj[i]:
                if j not in distances:
                    distances[j], parents[j] = distances[i] + 1, i
                    todo.append(j)
                elif parents[i] != j:
                    girth = min(girth, distances[i] + distances[j] + 1)
    return girth


def tiny_source(k):
    x = {'t': F(1), 'h': F(1, 2), 'x0': F(3, 2)}
    eqs = [('inv', 't', 't'), ('add', 'h', 'h', 't'), ('add', 't', 'h', 'x0')]
    denominator = 2
    for j in range(k):
        old, new = f'x{j}', f'x{j+1}'
        a, b, c = f'a{j}', f'b{j}', f'c{j}'
        x[a], x[b] = x[old] - x['h'], 1/x[old]
        x[c] = x[a] + x[b]
        x[new] = x[c] - x['h']
        denominator *= denominator + 1
        assert x[new] == 1 + F(1, denominator)
        eqs.extend([('add', a, 'h', old), ('inv', old, b),
                    ('add', a, b, c), ('add', new, 'h', c)])
    eqs.append(('inv', f'x{k}', 't'))
    return x, eqs, denominator


def main():
    counts = {}
    grid = [F(i, 4) for i in range(2, 9)]
    # Entire crossover network: original and outgoing variables keep [1/2,2],
    # while its new sum alone may exceed 2. Check the physical bus injections.
    variables = ('X', 'Y', 'Xp', 'Yp', 'Z')
    eqs = [('add', 'X', 'Y', 'Z'), ('add', 'X', 'Yp', 'Z'),
           ('add', 'Xp', 'Y', 'Z')]
    net = widened(variables, eqs, {'Z'})
    for x, y in product(grid, repeat=2):
        v = wide_profile(net, {'X': x, 'Y': y, 'Xp': x, 'Yp': y, 'Z': x+y})
        box_check(net, v)
        assert not any(violations(net, v).values())
    counts['generalized_crossover_profiles'] = len(grid)**2
    # Generalized inversion includes a repeated-name equation and endpoints.
    for same in (False, True):
        variables = ('x',) if same else ('x', 'y')
        net = widened(variables, [('inv', 'x', 'x' if same else 'y')])
        for x in ([F(1)] if same else grid):
            assignment = {'x': x} if same else {'x': x, 'y': 1/x}
            v = wide_profile(net, assignment)
            box_check(net, v)
            assert not any(violations(net, v).values())
    counts['generalized_inversion_profiles'] = len(grid) + 1

    # Connector buses retain unique voltage and do not restrict old feasible
    # points, including components consisting solely of unused variables.
    net = build(('h', 'one', 'u', 'v'), [('add', 'h', 'h', 'one')])
    v = profile(net, {'h': F(1, 2), 'one': F(1), 'u': F(2), 'v': F(7, 8)})
    net, v = connect(net, v)
    assert not any(violations(net, v).values())
    assert max(map(len, adjacency(net).values())) <= 3
    counts['connected_components_joined'] = 3

    # An independent arbitrary network includes a triangle, a conductance-2
    # edge, unequal voltages, and a pendant edge. It is deliberately infeasible
    # at this profile: subdivision must preserve scaled residuals, not just zeros.
    raw = Network((), ())
    for _ in range(4):
        raw.bus('original', (F(1, 2), 4), (F(-1, 3), F(1, 5)))
    for i, j, g in ((0, 1, 1), (1, 2, 2), (2, 0, 1), (2, 3, 2)):
        raw.edge(i, j, g)
    assignment = {0: F(1, 2), 1: F(7, 4), 2: F(4), 3: F(5, 2)}
    for length_scale in (1, 2, 4):
        out, w = subdivide(raw, assignment, length_scale)
        box_check(out, w)
        old_power, new_power = powers(raw, assignment), powers(out, w)
        for i in raw.buses:
            assert new_power[i] == old_power[i] / (4 * length_scale)
            assert violations(out, w)[i] == violations(raw, assignment)[i] / (4 * length_scale)
        assert all(new_power[i] == 0 for i in out.buses if i not in raw.buses)
        assert set(out.edges.values()) == {F(1)}
        assert max(map(len, adjacency(out).values())) <= 3
        assert bipartite_and_girth(out) == 10 * length_scale
        assert len(components(out)) == 1
    counts['subdivision_scales_checked'] = 3

    rng = random.Random(20260907)
    residual_profiles = 0
    for _ in range(120):
        names = tuple(f'x{i}' for i in range(rng.randrange(1, 7)))
        eqs = []
        for _ in range(rng.randrange(0, 16)):
            kind = rng.choice(('add', 'inv'))
            eqs.append((kind, *(rng.choice(names) for _ in range(3 if kind == 'add' else 2))))
        net = build(names, eqs)
        x = {name: rng.choice(grid) for name in names}
        v = profile(net, x)
        box_check(net, v)
        assert max(violations(net, v).values(), default=F(0)) <= 2 * source_residual(eqs, x)
        # Perturb every unpinned voltage independently, preserving the exact box.
        for exponent in (0, 4, 12):
            w = {i: min(b.voltage[1], max(b.voltage[0],
                       v[i] + F(rng.randrange(-5, 6), 2**exponent)))
                 for i, b in net.buses.items()}
            box_check(net, w)
            residual = max(violations(net, w).values(), default=F(0))
            roots = {name: w[i] for name, i in net.roots.items()}
            assert source_residual(eqs, roots) <= 10 * (6 * len(eqs) + 1) * residual
            residual_profiles += 1
    counts['perturbed_original_network_profiles'] = residual_profiles

    tiny = []
    for k in range(11):
        x, eqs, denominator = tiny_source(k)
        assert len(x) == 4*k + 3 and len(eqs) == 4*k + 4
        net = build(tuple(x), eqs)
        v = profile(net, x)
        box_check(net, v)
        residuals = violations(net, v)
        nonzero = {i: r for i, r in residuals.items() if r}
        assert nonzero == {net.gadgets[-1][1][3]: F(1, denominator + 1)}
        assert F(1, denominator + 1) < F(1, 2**(2**k))
        assert len(net.buses) <= 68*k + 67 and len(net.edges) <= 72*k + 72
        assert len(components(net)) == 1
        tiny.append({'k': k, 'buses': len(net.buses), 'lines': len(net.edges),
                     'residual_denominator_bits': (denominator + 1).bit_length()})
    counts['tiny_residual_instances'] = tiny
    # Exact graph-Poincare and interval Lipschitz checks, independent of any
    # eigenvalue computation or trigonometric approximations.
    for _ in range(100):
        n = rng.randrange(2, 9)
        net = Network((), ())
        for _ in range(n):
            net.bus('random', (F(1, 2), 4), FREE)
        for i in range(1, n):
            net.edge(i, rng.randrange(i), rng.choice((1, 2)))
        theta = {i: F(rng.randrange(-20, 21), 8) for i in net.buses}
        mean = sum(theta.values(), F(0))/n
        norm2 = sum(((t - mean)**2 for t in theta.values()), F(0))
        energy = sum((g*(theta[i]-theta[j])**2 for (i,j),g in net.edges.items()), F(0))
        assert 2*min(net.edges.values())*norm2 <= (n-1)**2*energy
        v = {i: F(rng.randrange(2, 17), 4) for i in net.buses}
        w = {i: F(rng.randrange(2, 17), 4) for i in net.buses}
        degree = max(sum(g for _, g in net.neighbors(i)) for i in net.buses)
        gap = max(abs(v[i]-w[i]) for i in net.buses)
        pv, pw = powers(net, v), powers(net, w)
        assert all(abs(pv[i]-pw[i]) <= 4*4*degree*gap for i in net.buses)
    counts['rational_poincare_and_lipschitz_profiles'] = 100
    print(json.dumps({'status': 'PASS', 'checks': counts}, indent=2))
    print('Finite exact checks support, and do not replace, the manuscript proofs.')


if __name__ == '__main__':
    main()
