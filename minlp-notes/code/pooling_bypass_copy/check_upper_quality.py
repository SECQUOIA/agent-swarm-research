"""Check the upper-quality-only cyclic degree-three construction in original pooling form."""
from collections import Counter
import argparse
import random

from check_copy_reduction import Network, solve, reference


class ThreePortNetwork(Network):
    def attach(self, port, source):
        j, quality = port[:2]
        cap = port[2] if len(port) == 3 else 2
        assert quality == self.inputs[source][0]
        self.direct.append((source, j, cap))

    def private(self, port):
        cap = port[2] if len(port) == 3 else 2
        self.attach(port, self.source(port[1], 0, cap))

    def half_gadget(self):
        out = [self.output(3, 3, 1, 1) for _ in range(2)]
        middle = self.source(1, 3, 3)
        self.mid_inputs.append(middle)
        self.direct.extend((middle, j, 3) for j in out)
        return ((out[0], 0, 2), (out[1], 0, 2),
                (out[0], 3, 1), (out[1], 3, 1))


def build_upper_quality(a, b, rows, *, split_inputs=False):
    n = len(a)
    net = ThreePortNetwork()
    uses = [[] for _ in range(n)]

    def new_signal():
        uses.append([])
        return len(uses)-1

    def request(literal, source, half=False):
        i, positive = literal
        uses[i].append((source, positive, half))

    zero = new_signal()
    request((zero, True), net.source(3, 0, 0))
    for row, bound in rows:
        coeff = [int(v-bound) for v in row]
        assert all(v-bound == int(v-bound) for v in row)
        leaves = [(i, c > 0) for i, c in enumerate(coeff)
                  for _ in range(abs(c))]
        if not leaves:
            continue
        size = 1 << (len(leaves)-1).bit_length()
        limit = 2*sum(-c for c in coeff if c < 0)
        leaves.extend([(zero, True)]*(size-len(leaves)))
        while len(leaves) > 1:
            parents = []
            for left, right in zip(leaves[::2], leaves[1::2]):
                v = new_signal()
                source = net.source(3, 2, 2)
                request((v, True), source)
                request((left[0], not left[1]), source, half=True)
                request((right[0], not right[1]), source, half=True)
                parents.append((v, True))
            leaves = parents
        request(leaves[0], net.source(3, 0, limit/size))

    # Separate full and half cycles have different quality inequalities.
    # Couple their signal values with one three-port source when needed.
    for occurrences in uses:
        if any(half for _, _, half in occurrences):
            couple = net.source(3, 2, 2)
            occurrences.extend([(couple, True, False),
                                (couple, False, True),
                                (couple, False, True)])
    net.cycle_links = []
    for i, occurrences in enumerate(uses):
        for half in [False, True]:
            modules = []
            for source, positive, requested_half in occurrences:
                if requested_half != half:
                    continue
                aa, ba, ab, bb = net.half_gadget() if half else net.gadget(0, 3)
                chosen, unused = (ab, bb) if positive else (bb, ab)
                net.attach(chosen, source)
                net.private(unused)
                modules.append((aa, ba))
            if i < n and not half:
                aa, ba, ab, bb = net.gadget(0, a[i])
                net.private(ab)
                source = net.source(a[i], 2, 2)
                net.attach(bb, source)
                net.intakes.append((source, 2, b[i]))
                modules.append((aa, ba))
            for k, (aa, _) in enumerate(modules):
                previous_ba = modules[k-1][1]
                link = net.source(0, 2, 2)
                net.cycle_links.append(link)
                net.attach(previous_ba, link)
                net.attach(aa, link)
    # The model uses only upper quality bounds. No hidden lower rows.
    net.outputs = [(lo, hi, None, qhi) for lo, hi, _, qhi in net.outputs]
    out1 = net.output(0, 1, None, 1)
    out2 = net.output(0, 1, None, max(a))
    anchor = net.source(0, 0, 1)
    net.direct.append((anchor, out1, 1))
    net.pool_outputs.extend((j, 1) for j in [out1, out2])

    indeg = Counter(i for i, _, _ in net.direct)
    indeg.update(i for i, _, _ in net.intakes)
    outdeg = Counter(j for _, j, _ in net.direct)
    outdeg.update(j for j, _ in net.pool_outputs)
    assert max(indeg.values()) <= 3
    assert max(outdeg.values()) <= 3
    assert len(net.pool_outputs) == 2
    assert all(0 <= low <= high <= 4 for _, low, high in net.inputs)
    assert all(0 <= low <= high <= 4 for low, high, _, _ in net.outputs)
    # Distinct occurrences must not accidentally become duplicate arcs.
    assert len(net.direct) == len({(i, j) for i, j, _ in net.direct})
    if split_inputs:
        split_three_port_sources(net)
    return net


def split_three_port_sources(net):
    """Project each three-port exact supply through complementary flows."""
    for i in range(len(net.inputs)):
        positions = [k for k, (ii, _, _) in enumerate(net.direct) if ii == i]
        if len(positions) != 3:
            continue
        quality, low, high = net.inputs[i]
        assert low == high == 2
        assert all(ii != i for ii, _, _ in net.intakes)
        capacities = [net.direct[k][2] for k in positions]
        assert sorted(capacities) in ([1, 1, 2], [2, 2, 2])
        collector = net.output(sum(capacities)-high,
                               sum(capacities)-high, None, quality)
        for h, (k, cap) in enumerate(zip(positions, capacities)):
            if h == 0:
                source = i
                net.inputs[i] = (quality, cap, cap)
            else:
                source = net.source(quality, cap, cap)
            _, j, _ = net.direct[k]
            net.direct[k] = (source, j, cap)
            net.direct.append((source, collector, cap))
    degrees = Counter(i for i, _, _ in net.direct)
    degrees.update(i for i, _, _ in net.intakes)
    assert max(degrees.values()) <= 2
    assert max(Counter(j for _, j, _ in net.direct).values()) <= 3
    assert len(net.direct) == len({(i, j) for i, j, _ in net.direct})


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--trials', type=int, default=10)
    parser.add_argument('--split-inputs', action='store_true')
    args = parser.parse_args()
    rng = random.Random(args.seed)
    count = 0
    for trial in range(args.trials):
        n = 2+trial % 2
        a = [rng.randint(1, 6) for _ in range(n)]
        b = [rng.randint(0, 8) for _ in range(n)]
        rows = []
        for _ in range(2):
            row = [rng.randint(-3, 4) for _ in range(n)]
            rows.append((row, (sum(row)+n-1)//n))
        expected, vs = reference(a, b, rows)
        net = build_upper_quality(a, b, rows, split_inputs=args.split_inputs)
        for shift in [0, 3]:
            actual = solve(net, shift=shift)
            assert abs(actual-float(expected)) <= 2e-5, (trial, actual, expected)
            count += 1
        print(f'trial={trial} inputs={len(net.inputs)} '
              f'outputs={len(net.outputs)} profit={expected}', flush=True)
    # m=0, m=1 with positive or complementary root, non-power-of-two
    # leaf counts, an empty source polytope, and zero reward.
    cases = [([1], [3], [([0], 0)]),
             ([2, 3], [3, 4], [([1, 0], 0)]),
             ([2, 3], [3, 4], [([-1, 0], 0)]),
             ([2, 3], [3, 4], [([2, -1], 0)]),
             ([2, 3], [4, 5], [([1, 1], -1)]),
             ([2, 4], [0, 0], [])]
    for a, b, rows in cases:
        expected, _ = reference(a, b, rows)
        actual = solve(build_upper_quality(a, b, rows, split_inputs=args.split_inputs))
        assert abs(actual-float(expected)) <= 2e-5, (actual, expected)
        count += 1
    # An relaxed cyclic supply upper bound can break quality tightness.
    rows = [([1, -1], 0), ([-1, 1], 0)]
    net = build_upper_quality([1, 1], [0, 10], rows, split_inputs=args.split_inputs)
    correct = solve(net)
    for k in net.cycle_links:
        q, lo, hi = net.inputs[k]
        net.inputs[k] = (q, lo, 4)
    changed = solve(net)
    assert abs(correct-10) <= 1e-5 and abs(changed-correct) > .1
    input_degree = 2 if args.split_inputs else 3
    print(f'PASS {count} full original-network solves; max input degree{input_degree}, '
          f'output degree3; scalar upper quality only; negative control {correct:.8g}->{changed:.8g}', flush=True)


if __name__ == '__main__':
    main()
