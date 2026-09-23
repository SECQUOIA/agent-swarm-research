"""Physical-network test of binary circuits, two feeds, and contract completion."""
from collections import Counter
from fractions import Fraction as F
from math import lcm
import argparse
import random

from check_degree_three import ThreePortNetwork
from check_upper_quality import split_three_port_sources
from check_upper_penalty import penalized
from check_copy_reduction import reference


class Circuit:
    def __init__(self, n):
        self.net = ThreePortNetwork()
        self.uses = [[] for _ in range(n)]
        self.intake_specs = {}
        self.zero = self.signal()
        self.one = self.signal()
        self.request(self.zero, self.net.source(3, 0, 0))
        self.request(self.one, self.net.source(3, 1, 1))

    def signal(self):
        self.uses.append([])
        return len(self.uses)-1

    def request(self, signal, source, positive=True, half=False):
        self.uses[signal].append((source, positive, half))

    def average(self, u, w):
        v = self.signal()
        source = self.net.source(3, 2, 2)
        self.request(v, source)
        self.request(u, source, positive=False, half=True)
        self.request(w, source, positive=False, half=True)
        return v

    def add(self, u, v):
        w = self.signal()
        source = self.net.source(3, 2, 2)
        self.request(u, source)
        self.request(v, source)
        self.request(w, source, positive=False)
        return w

    def total(self, signals):
        total = self.zero
        for signal in signals:
            total = self.add(total, signal)
        return total

    def compare(self, u, v, *, equality=False):
        source = self.net.source(3, 2 if equality else 0, 2)
        self.last_comparison_source = source
        self.request(u, source)
        self.request(v, source, positive=False)

    def scale(self, signal, factor):
        factor = F(factor)
        assert 0 <= factor <= 1
        if factor == 0:
            return self.zero
        if factor == 1:
            return signal
        denominator = factor.denominator
        assert denominator & (denominator-1) == 0
        result = self.zero
        for k in range(denominator.bit_length()-1):
            result = self.average(result, signal if (factor.numerator >> k) & 1 else self.zero)
        return result

    def row(self, terms, bound):
        terms = {i: F(c) for i, c in terms.items() if c}
        bound = F(bound)
        denom = lcm(bound.denominator, *(c.denominator for c in terms.values()))
        coeff = {i: int(c*denom) for i, c in terms.items()}
        rhs = int(bound*denom)
        magnitude = sum(abs(c) for c in coeff.values())+abs(rhs)
        base = 1 << magnitude.bit_length()
        positive, negative = [], []
        for i, c in coeff.items():
            term = self.scale(i, F(abs(c), base))
            (positive if c > 0 else negative).append(term)
        if rhs:
            constant = self.scale(self.one, F(abs(rhs), base))
            (negative if rhs > 0 else positive).append(constant)
        self.compare(self.total(positive), self.total(negative))

    def build(self):
        net = self.net
        for occurrences in self.uses:
            if any(half for _, _, half in occurrences):
                source = net.source(3, 2, 2)
                occurrences.extend([(source, True, False),
                                    (source, False, True), (source, False, True)])
        for i, occurrences in enumerate(self.uses):
            for half in [False, True]:
                modules = []
                for source, positive, is_half in occurrences:
                    if is_half != half:
                        continue
                    aa, ba, ab, bb = net.half_gadget() if half else net.gadget(0, 3)
                    chosen, unused = (ab, bb) if positive else (bb, ab)
                    net.attach(chosen, source)
                    net.private(unused)
                    modules.append((aa, ba))
                if i in self.intake_specs and not half:
                    quality = self.intake_specs[i]
                    aa, ba, ab, bb = net.gadget(0, quality)
                    net.private(ab)
                    source = net.source(quality, 2, 2)
                    net.attach(bb, source)
                    net.intakes.append((source, 2, 0))
                    modules.append((aa, ba))
                for k, (aa, _) in enumerate(modules):
                    link = net.source(0, 2, 2)
                    net.attach(modules[k-1][1], link)
                    net.attach(aa, link)
        net.outputs = [(lo, hi, None, qhi) for lo, hi, _, qhi in net.outputs]
        first = net.output(0, 1, None, 1)
        second = net.output(0, 1, None, 33)
        anchor = net.source(0, 0, 1)
        net.direct.append((anchor, first, 1))
        net.pool_outputs.extend([(first, 1), (second, 1)])
        split_three_port_sources(net)
        input_degrees = Counter(i for i, _, _ in net.direct)
        input_degrees.update(i for i, _, _ in net.intakes)
        output_degrees = Counter(j for _, j, _ in net.direct)
        output_degrees.update(j for j, _ in net.pool_outputs)
        assert max(input_degrees.values()) <= 2
        assert max(output_degrees.values()) <= 3
        assert len(net.intakes) == len(net.pool_outputs) == 2
        assert all(v in {0, 1, 2, 3, 4} for _, lo, hi in net.inputs for v in [lo, hi])
        assert all(v in {0, 1, 2, 3, 4} for lo, hi, _, _ in net.outputs for v in [lo, hi])
        palette = {0, F(1, 2), 1, F(3, 2), 3, F(33, 2), 33}
        assert all(q in palette for q, _, _ in net.inputs)
        assert all(qlo is None and qhi in palette for _, _, qlo, qhi in net.outputs)
        assert len(net.direct) == len({(i, j) for i, j, _ in net.direct})
        return net


def build_constant_data(a, b, rows, threshold):
    n = len(a)
    circuit = Circuit(n)
    for row, bound in rows:
        circuit.row({i: F(c-bound) for i, c in enumerate(row)}, 0)
    total = circuit.total(range(n))
    high = circuit.total([circuit.scale(i, (F(a[i])-1)/32) for i in range(n)])
    low = circuit.signal()
    circuit.compare(circuit.add(low, high), total, equality=True)
    circuit.intake_specs = {low: 1, high: 33}
    circuit.row({i: -F(b[i]) for i in range(n)}, -F(threshold))
    circuit.net.threshold_comparison = circuit.last_comparison_source
    return circuit.build()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--trials', type=int, default=4)
    args = parser.parse_args()
    rng = random.Random(args.seed)
    checked = 0
    for trial in range(args.trials):
        a = [rng.randint(2, 5), rng.randint(2, 5)]
        b = [rng.randint(2, 5), rng.randint(2, 5)]
        row = [rng.randint(-2, 2), rng.randint(-2, 2)]
        rows = [(row, (sum(row)+1)//2)]
        optimum, _ = reference(a, b, rows)
        floor = int(optimum)
        for threshold in [max(1, floor), floor+1]:
            net = build_constant_data(a, b, rows, threshold)
            value, _, deficit = penalized(net, 1)
            expected = optimum >= threshold
            observed = deficit <= 1e-6
            assert observed == expected, (a, b, rows, threshold, optimum, value, deficit)
            print(f'trial={trial} originalopt={optimum} threshold={threshold} '
                  f'yes={observed} deficit={deficit:.8g} inputs={len(net.inputs)} '
                  f'outputs={len(net.outputs)}', flush=True)
            checked += 1
    # Feasible source slice, impossible slice, exact equality at a boundary,
    # and the a=1 master-low endpoint.
    cases = [([2, 3], [3, 4], [([1, -1], 0), ([-1, 1], 0)], 4),
             ([2, 3], [3, 4], [([1, 1], -1)], 1),
             ([1], [2], [], 4), ([1], [2], [], 5)]
    for a, b, rows, threshold in cases:
        optimum, _ = reference(a, b, rows)
        net = build_constant_data(a, b, rows, threshold)
        value, _, deficit = penalized(net, 1)
        assert (deficit <= 1e-6) == (optimum >= threshold), (optimum, threshold, deficit)
        checked += 1
    net = build_constant_data([1], [2], [], 5)
    _, _, true_deficit = penalized(net, 1)
    i = net.threshold_comparison
    quality, low, high = net.inputs[i]
    assert low == 0 and high == 2
    net.inputs[i] = (quality, 0, 4)
    _, _, broken_deficit = penalized(net, 1)
    assert true_deficit > 1e-3 and abs(broken_deficit) <= 1e-6
    print(f'PASS {checked} full original-network contract-completion solves; '
          'fixed numeric palette, pool in/out degree2, input degree2/output degree3; '
          f'negative control deficit {true_deficit:.8g}->{broken_deficit:.8g}')


if __name__ == '__main__':
    main()
