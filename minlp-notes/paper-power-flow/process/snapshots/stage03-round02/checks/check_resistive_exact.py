#!/usr/bin/env python3
"""Exact finite checks of the original graph construction; no solver imports.

Checks original bus injections, not just eliminated gadget equations. Arbitrary
source assignments also test the residual identities, including unsatisfied
equations. These finite tests support, but do not replace, the manuscript proof.
"""

from dataclasses import dataclass
from fractions import Fraction as F
from itertools import product
import random


HALF, TWO, C = F(1, 2), F(2), F(5, 2)
FREE = (F(-85), F(85))
VOLTAGES = {(HALF, TWO), (F(1), F(1)), (F(1), F(4))}
INJECTIONS = {FREE, (F(-1, 2),) * 2, (F(1, 2),) * 2,
              (F(-5, 2),) * 2, (F(-1),) * 2}


@dataclass(frozen=True)
class Bus:
    voltage: tuple
    injection: tuple
    kind: str
    variable: str | None = None
    parity: int = 0


class Network:
    def __init__(self, variables, equations):
        self.variables = tuple(variables)
        self.equations = tuple(tuple(e) for e in equations)
        assert len(set(self.variables)) == len(self.variables)
        self.buses, self.edges, self.roots, self.gadgets = {}, {}, {}, []
        self.allocated = []
        self.paths = {x: [] for x in self.variables}

    def bus(self, kind, voltage, injection, variable=None, parity=0):
        i = len(self.buses)
        self.buses[i] = Bus(tuple(map(F, voltage)), tuple(map(F, injection)),
                            kind, variable, parity)
        return i

    def pin(self, kind, injection):
        return self.bus(kind, (1, 1), (injection, injection))

    def edge(self, i, j, g=1):
        assert i != j and i in self.buses and j in self.buses
        key = tuple(sorted((i, j)))
        assert key not in self.edges
        self.edges[key] = F(g)

    def neighbors(self, i):
        for (a, b), g in self.edges.items():
            if a == i:
                yield b, g
            elif b == i:
                yield a, g

    def power(self, i, voltage):
        return voltage[i] * sum((g * (voltage[i] - voltage[j])
                                 for j, g in self.neighbors(i)), F(0))


def build(variables, equations):
    net = Network(variables, equations)
    used = set()
    for x in net.variables:
        i = net.bus('value', (HALF, TWO), FREE, x)
        net.roots[x] = i
        net.paths[x].append(i)

    def take(x, parity):
        assert x in net.paths
        path = net.paths[x]
        while net.buses[path[-1]].parity != parity or path[-1] in used:
            end = path[-1]
            pin = net.pin('copy', -HALF)
            i = net.bus('value', (HALF, TWO), FREE, x,
                        1 - net.buses[end].parity)
            net.edge(end, pin)
            net.edge(pin, i)
            path.append(i)
        i = path[-1]
        used.add(i)
        net.allocated.append(i)
        return i

    for eq in net.equations:
        if eq[0] == 'add':
            _, x, y, z = eq
            a = net.pin('addition', HALF)
            for var, parity in ((x, 0), (y, 0), (z, 1)):
                net.edge(a, take(var, parity))
            net.gadgets.append((eq, (a,)))
        elif eq[0] == 'inv':
            _, x, y = eq
            i = net.bus('inversion', (HALF, TWO), (-1, -1), x)
            w = net.bus('auxiliary', (1, 4), FREE, x)
            ci = net.pin('tie', -HALF)
            d = net.pin('linear', F(-5, 2))
            net.edge(i, w)
            net.edge(i, ci)
            net.edge(ci, take(x, 1))
            net.edge(d, w)
            net.edge(d, take(x, 1), 2)
            net.edge(d, take(y, 1))
            net.gadgets.append((eq, (i, w, ci, d)))
        else:
            raise ValueError(eq)
    return net


def profile(net, assignment):
    """Canonical rational extension, also defined for nonsolutions."""
    assert set(assignment) == set(net.variables)
    assert all(HALF <= x <= TWO for x in assignment.values())
    result = {}
    for i, bus in net.buses.items():
        if bus.kind == 'value':
            x = assignment[bus.variable]
            result[i] = x if bus.parity == 0 else C - x
        elif bus.kind == 'inversion':
            result[i] = assignment[bus.variable]
        elif bus.kind == 'auxiliary':
            x = assignment[bus.variable]
            result[i] = 2*x - 1 + 1/x
        else:
            result[i] = F(1)
    return result


def structural_checks(net):
    assert len(net.buses) <= len(net.variables) + 16*len(net.equations)
    assert len(net.edges) <= 18*len(net.equations)
    assert len(net.allocated) == 3*len(net.equations)
    assert len(set(net.allocated)) == len(net.allocated)
    for i, bus in net.buses.items():
        neighbors = list(net.neighbors(i))
        degree = len(neighbors)
        assert degree <= 3
        assert bus.voltage in VOLTAGES and bus.injection in INJECTIONS
        if bus.kind in {'copy', 'tie', 'inversion', 'auxiliary'}:
            assert degree == 2
        elif bus.kind in {'addition', 'linear'}:
            assert degree == 3
        if bus.kind == 'value':
            assert sum(net.buses[j].kind != 'copy' for j, _ in neighbors) <= 1
        if bus.injection == FREE:
            assert bus.voltage[1] * sum(g for _, g in neighbors) * F(7, 2) <= 84
    assert all(g in {F(1), F(2)} for g in net.edges.values())


def check_assignment(net, assignment):
    """Verify all original bus equations and residuals with exact fractions."""
    v = profile(net, assignment)
    expected_residual = {}
    source_feasible = True
    for eq, buses in net.gadgets:
        if eq[0] == 'add':
            _, x, y, z = eq
            residual = assignment[z] - assignment[x] - assignment[y]
            expected_residual[buses[0]] = residual
        else:
            _, x, y = eq
            residual = assignment[y] - 1/assignment[x]
            expected_residual[buses[3]] = residual
        source_feasible &= residual == 0
    target_feasible = True
    for i, bus in net.buses.items():
        assert bus.voltage[0] <= v[i] <= bus.voltage[1]
        p = net.power(i, v)
        if bus.injection == FREE:
            assert -85 < p < 85
        else:
            assert p - bus.injection[0] == expected_residual.get(i, F(0))
        target_feasible &= bus.injection[0] <= p <= bus.injection[1]
    assert source_feasible == target_feasible
    assert {x: v[i] for x, i in net.roots.items()} == assignment
    assert sum((net.power(i, v) for i in net.buses), F(0)) == sum(
        (g*(v[i]-v[j])**2 for (i, j), g in net.edges.items()), F(0))
    return source_feasible


def main():
    rng = random.Random(20260907)
    checked, satisfying = 0, 0
    grid = tuple(F(i, 4) for i in range(2, 9))
    # Covers all variable-identification patterns for addition and inversion,
    # including x+x=x, and unused variables (the names stay x,y,z).
    names = ('x', 'y', 'z')
    equations = [('add', *e) for e in product(names, repeat=3)]
    equations += [('inv', *e) for e in product(names, repeat=2)]
    for eq in equations:
        net = build(names, [eq])
        structural_checks(net)
        for values in product(grid, repeat=3):
            satisfying += check_assignment(net, dict(zip(names, values)))
            checked += 1
    # Exact inversion witnesses include both endpoints and many non-grid values.
    net = build(('x', 'y', 'unused'), [('inv', 'x', 'y')])
    structural_checks(net)
    for k in range(101):
        x = HALF + F(3*k, 200)
        satisfying += check_assignment(net, {'x': x, 'y': 1/x, 'unused': F(7, 8)})
        checked += 1
    # Long paths and high fan-out, with a satisfiable boundary profile.
    net = build(('h', 'one', 'two', 'unused'),
                [('add', 'h', 'h', 'one'), ('add', 'one', 'one', 'two')]
                + [('inv', 'h', 'two')]*40 + [('inv', 'one', 'one')]*40)
    structural_checks(net)
    satisfying += check_assignment(net, {'h': HALF, 'one': F(1),
                                        'two': TWO, 'unused': F(5, 4)})
    checked += 1
    # General graph combinations test original equation residuals even when
    # the source formula is unsatisfied; this is not an infeasibility solver.
    for _ in range(300):
        n = rng.randrange(1, 9)
        names = tuple(f'x{i}' for i in range(n))
        eqs = []
        for _ in range(rng.randrange(21)):
            kind = rng.choice(('add', 'inv'))
            eqs.append((kind, *(rng.choice(names) for _ in range(3 if kind == 'add' else 2))))
        net = build(names, eqs)
        structural_checks(net)
        satisfying += check_assignment(net, {x: rng.choice(grid) for x in names})
        checked += 1
    net = build((), ())
    structural_checks(net)
    assert check_assignment(net, {})
    checked += 1
    satisfying += 1
    print(f'PASS: {checked} exact original-network profiles; {satisfying} source solutions.')
    print('PASS: repeated/unused variables, empty instance, residual identities,')
    print('      distinct copies, simple graphs, degree <= 3, fixed data, size, and dissipation.')
    print('Finite exact checks support the proof; no numerical solver was used.')


if __name__ == '__main__':
    main()
