"""Independent physical-network check of the constant-data two-feed circuit.

Uses only ordinary source/output/arc constraints in the network LP.
Circuit equations and the source rows appear only in the reference LP.
"""
from collections import defaultdict
from fractions import Fraction as F
from math import lcm

import numpy as np
from scipy.optimize import linprog

from independent_upper_quality_review import AveragingNetwork
from independent_review import sparse


class CircuitNetwork(AveragingNetwork):
    def __init__(self, weights, rewards, threshold, cone):
        self.inputs, self.outputs, self.arcs = [], [], []
        self.demands = {}
        self.shift = 0
        self.requests = defaultdict(list)
        self.signal_count = len(weights)
        self.zero = self.new_signal()
        self.unit = self.new_signal()
        self.request(self.zero, False, False, self.input(3, 0, 0))
        self.request(self.unit, False, False, self.input(3, 1, 1))
        for row in cone:
            self.row(row, 0)
        self.threshold_source = self.row([-F(b) for b in rewards], -F(threshold))
        total = self.sum_signals(list(range(len(weights))))
        high = self.sum_signals([self.multiply(i, F(w)) for i, w in enumerate(weights)])
        low = self.new_signal()
        self.add_equation(low, high, total)
        feeds = {low: 1, high: 33}
        self.monitors = []
        for i in range(len(weights)):
            source = self.input(3, 0, 2)
            self.monitors.append(source)
            self.request(i, False, False, source)
        for signal in range(self.signal_count):
            if any(half for half, _, _ in self.requests[signal]):
                source = self.input(3, 2, 2)
                self.requests[signal].extend([(False, False, source),
                                              (True, True, source),
                                              (True, True, source)])
        self.intakes, self.feed_qualities = [], []
        for signal in range(self.signal_count):
            for half in [False, True]:
                modules = []
                for requested_half, complement, source in self.requests[signal]:
                    if requested_half != half:
                        continue
                    first, second = self.half_gadget() if half else self.gadget(0, 3)
                    modules.append((first, second))
                    cap = 1 if half else 2
                    self.arc(source, second if complement else first, cap)
                    self.private_endpoint(3, first if complement else second, cap)
                if signal in feeds and not half:
                    quality = feeds[signal]
                    first, second = self.gadget(0, quality)
                    modules.append((first, second))
                    self.private_port(quality, first)
                    source = self.input(quality, 2, 2)
                    self.arc(source, second, 2)
                    self.intakes.append(self.arc(source, None, 2))
                    self.feed_qualities.append(quality)
                for j, (first, _) in enumerate(modules):
                    link = self.input(0, 2, 2)
                    self.arc(link, modules[j-1][1], 2)
                    self.arc(link, first, 2)
        self.split_sources()
        assert len(self.intakes) == 2
        assert max(len(arcs) for _, _, _, arcs in self.inputs) <= 2
        assert max(len(arcs) for _, arcs in self.outputs) <= 3
        assert all(upper in [0, 1, 2, 3, 4] for _, _, upper, _ in self.inputs)
        assert all(self.demands.get(i, 4) in [1, 2, 3, 4] for i in range(len(self.outputs)))
        assert all(cap in [1, 2, 3, 4] for _, _, cap in self.arcs)
        assert {q for q, _, _, _ in self.inputs} <= {0, .5, 1, 1.5, 3, 16.5, 33}
        assert len(self.arcs) == len({(s, t) for s, t, _ in self.arcs})

    def new_signal(self):
        signal = self.signal_count
        self.signal_count += 1
        return signal

    def request(self, signal, half, complement, source):
        self.requests[signal].append((half, complement, source))

    def average(self, u, w):
        v = self.new_signal()
        source = self.input(3, 2, 2)
        self.request(v, False, False, source)
        self.request(u, True, True, source)
        self.request(w, True, True, source)
        return v

    def add_equation(self, u, v, w):
        source = self.input(3, 2, 2)
        for signal, complement in [(u, False), (v, False), (w, True)]:
            self.request(signal, False, complement, source)

    def sum_signals(self, signals):
        if not signals:
            return self.zero
        current = signals[0]
        for signal in signals[1:]:
            parent = self.new_signal()
            self.add_equation(current, signal, parent)
            current = parent
        return current

    def multiply(self, signal, coefficient):
        coefficient = F(coefficient)
        assert 0 <= coefficient <= 1
        if coefficient == 1:
            return signal
        if coefficient == 0:
            return self.zero
        denominator = coefficient.denominator
        assert denominator & (denominator - 1) == 0
        current = self.zero
        for k in range(denominator.bit_length() - 1):
            current = self.average(current, signal if coefficient.numerator & (1 << k) else self.zero)
        return current

    def row(self, coefficients, bound):
        values = [F(c) for c in coefficients] + [F(bound)]
        scale = lcm(*(v.denominator for v in values))
        integers = [int(v * scale) for v in values]
        coeff, rhs = integers[:-1], integers[-1]
        normalizer = 1 << (sum(abs(c) for c in coeff) + abs(rhs)).bit_length()
        left, right = [], []
        for i, c in enumerate(coeff):
            if c:
                (left if c > 0 else right).append(self.multiply(i, F(abs(c), normalizer)))
        if rhs:
            (right if rhs > 0 else left).append(self.multiply(self.unit, F(abs(rhs), normalizer)))
        u, v = self.sum_signals(left), self.sum_signals(right)
        source = self.input(3, 0, 2)
        self.request(u, False, False, source)
        self.request(v, False, True, source)
        return source

    def split_sources(self):
        originals = [i for i, (_, _, _, arcs) in enumerate(self.inputs) if len(arcs) == 3]
        for original in originals:
            quality, lower, upper, old_arcs = self.inputs[original]
            assert lower == upper == 2
            arcs = list(old_arcs)
            caps = [self.arcs[e][2] for e in arcs]
            assert sorted(caps) in [[1, 1, 2], [2, 2, 2]]
            collector = len(self.outputs)
            self.outputs.append((quality, []))
            self.demands[collector] = sum(caps) - 2
            sources = [original]
            self.inputs[original] = quality, caps[0], caps[0], []
            for cap in caps[1:]:
                sources.append(len(self.inputs))
                self.inputs.append((quality, cap, cap, []))
            for source, e, cap in zip(sources, arcs, caps):
                _, target, _ = self.arcs[e]
                self.arcs[e] = source, target, cap
                self.inputs[source][3].append(e)
                self.arc(source, collector, cap)

    def solve(self, quality, complete=False):
        eq, erhs, ub, urhs, contracts = [], [], [], [], []
        for _, lower, upper, arcs in self.inputs:
            row = {e: 1 for e in arcs}
            if lower == upper:
                contracts.append((row, upper))
            if lower == upper and not complete:
                eq.append(row)
                erhs.append(upper)
            else:
                ub.append(row)
                urhs.append(upper)
        for j, (bound, incoming) in enumerate(self.outputs):
            demand = self.demands.get(j, 4)
            mass = {e: 1 for e in incoming}
            contracts.append((mass, demand))
            if complete:
                ub.append(mass)
                urhs.append(demand)
            else:
                eq.append(mass)
                erhs.append(demand)
            ub.append({e: self.inputs[self.arcs[e][0]][0] - bound for e in incoming})
            urhs.append(0)
        bounds = [(0, cap) for _, _, cap in self.arcs] + [(0, 1)] * 3
        first, second, anchor = range(len(self.arcs), len(self.arcs) + 3)
        eq.append({**{e: 1 for e in self.intakes}, first: -1, second: -1})
        erhs.append(0)
        eq.append({**{e: c for e, c in zip(self.intakes, self.feed_qualities)},
                   first: -quality, second: -quality})
        erhs.append(0)
        ub.extend([{first: 1, anchor: 1}, {first: quality-1, anchor: -1}, {second: quality-33}])
        urhs.extend([1, 0, 0])
        objective = np.zeros(len(bounds))
        if complete:
            for row, _ in contracts:
                for e, c in row.items():
                    objective[e] -= c
            assert set(objective) <= {0, -1, -2}
        result = linprog(objective, A_ub=sparse(ub, len(bounds)), b_ub=urhs,
                         A_eq=sparse(eq, len(bounds)), b_eq=erhs, bounds=bounds, method='highs')
        if not complete:
            return result.success
        assert result.success
        target = sum(rhs for _, rhs in contracts)
        return target + result.fun


def reference(weights, rewards, threshold, cone, quality):
    a = 1 + 32 * np.array(weights, dtype=float)
    rows = [np.array(row, dtype=float) for row in cone]
    rows += [-np.array(rewards), np.ones(len(a))]
    rhs = [0] * len(cone) + [-threshold, 1 + 1 / quality]
    answer = linprog(np.zeros(len(a)), A_ub=np.array(rows), b_ub=rhs,
                     A_eq=[a-quality], b_eq=[0], bounds=[(0, 2)] * len(a), method='highs')
    return answer.success


def main():
    cases = [([F(0), F(1, 2)], [2, 4], threshold, cone)
             for threshold in [3, 4, 5]
             for cone in [[], [[1, -1], [-1, 1]]]]
    cases += [([F(1, 8), F(3, 8)], [F(3, 2), F(5, 2)], F(5, 2), [[F(1, 3), F(-1, 2)]]),
              ([F(0), F(0)], [1, 1], 1, [[1, 1]])]
    checks = yes = no = 0
    for weights, rewards, threshold, cone in cases:
        network = CircuitNetwork(weights, rewards, threshold, cone)
        for quality in [1, 5, 9, 13, 17]:
            expected = reference(weights, rewards, threshold, cone, quality)
            actual = network.solve(quality)
            assert actual == expected, (quality, threshold, cone, expected, actual)
            deficit = network.solve(quality, complete=True)
            assert (deficit < 1e-7) == expected, (deficit, quality, threshold, expected)
            checks += 1
            yes += expected
            no += not expected
    network = CircuitNetwork([F(0), F(1, 2)], [2, 4], 5, [])
    assert not network.solve(1)
    source = network.threshold_source
    quality, lower, _, arcs = network.inputs[source]
    network.inputs[source] = quality, lower, 4, arcs
    assert network.solve(1)
    assert abs(network.solve(1, complete=True)) < 1e-7
    print('Negative control: relaxing only the threshold comparator changes infeasible to feasible and permits full completion.')
    for n in range(5, 9):
        source_size = n + n*n
        p = n ** (n**4)
        power = p ** (4*n)
        u0 = 2*power-p
        divisor = 1 << ((u0//2).bit_length()-1)
        umax = u0 + source_size*p**(2*n) + 2*source_size*p**(3*n)
        vmax = u0 + source_size*p**(2*n)
        threshold = 4*p**(8*n)
        assert 2*divisor <= u0 < 4*divisor
        assert source_size < p**n and power < u0 and umax < 20*divisor
        assert divisor*vmax < threshold
        assert 0 <= F(u0-2*divisor, 32*divisor) <= F(umax-2*divisor, 32*divisor) < 1
    print('PASS: exact Matsui normalization bounds at n=5,...,8 (thresholds up to786435 bits).')
    print(f'PASS: {checks} full physical two-feed circuit LPs against reference feasibility ({yes} yes, {no} no).')
    print(f'PASS: {checks} upper-only completion LPs reach the exact contract threshold iff feasible.')
    print('Includes dyadic and signed rational rows, zero weights, repeated copies, infeasible cones, and equality thresholds.')
    print('All quality/capacity alphabets fixed; input degree<=2, output degree<=3, pool feeds=2, outlets=2.')


if __name__ == '__main__':
    main()
