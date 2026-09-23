"""Check the degree-four averaging construction in original pooling form."""
from collections import Counter
import argparse
import random

from check_copy_reduction import Network, solve, reference


def build_degree_four(a, b, rows):
    n = len(a)
    net = Network()
    uses = [[] for _ in range(n)]

    def new_signal():
        uses.append([])
        return len(uses)-1

    def request(literal, source):
        i, positive = literal
        uses[i].append((source, positive))

    zero = new_signal()
    request((zero, True), net.source(2, 0, 0))
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
                source = net.source(2, 4, 4)
                request((v, True), source)
                request((v, True), source)
                request((left[0], not left[1]), source)
                request((right[0], not right[1]), source)
                parents.append((v, True))
            leaves = parents
        request(leaves[0], net.source(2, 0, limit/size))

    for i, occurrences in enumerate(uses):
        previous = None
        for source, positive in occurrences:
            aa, ba, ab, bb = net.gadget(0, 2)
            if previous is None:
                net.private(aa)
            else:
                link = net.source(0, 2, 2)
                net.attach(previous, link)
                net.attach(aa, link)
            chosen, unused = (ab, bb) if positive else (bb, ab)
            net.attach(chosen, source)
            net.private(unused)
            previous = ba
        if i < n:
            aa, ba, ab, bb = net.gadget(0, a[i])
            if previous is None:
                net.private(aa)
            else:
                link = net.source(0, 2, 2)
                net.attach(previous, link)
                net.attach(aa, link)
            net.private(ba)
            net.private(ab)
            source = net.source(a[i], 2, 2)
            net.attach(bb, source)
            net.intakes.append((source, 2, b[i]))
        elif previous is not None:
            net.private(previous)
    out1 = net.output(0, 1, None, 1)
    out2 = net.output(0, 1, None, max(a))
    anchor = net.source(0, 0, 1)
    net.direct.append((anchor, out1, 1))
    net.pool_outputs.extend((j, 1) for j in [out1, out2])

    indeg = Counter(i for i, _, _ in net.direct)
    indeg.update(i for i, _, _ in net.intakes)
    outdeg = Counter(j for _, j, _ in net.direct)
    outdeg.update(j for j, _ in net.pool_outputs)
    assert max(indeg.values()) <= 4
    assert max(outdeg.values()) <= 3
    assert len(net.pool_outputs) == 2
    assert all(0 <= low <= high <= 4 for _, low, high in net.inputs)
    assert all(0 <= low <= high <= 4 for low, high, _, _ in net.outputs)
    # Distinct occurrences must not accidentally become duplicate arcs.
    assert len(net.direct) == len({(i, j) for i, j, _ in net.direct})
    return net


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--trials', type=int, default=10)
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
        net = build_degree_four(a, b, rows)
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
        actual = solve(build_degree_four(a, b, rows))
        assert abs(actual-float(expected)) <= 2e-5, (actual, expected)
        count += 1
    # An independent wrong averaging supply breaks row equality.
    rows = [([1, -1], 0), ([-1, 1], 0)]
    net = build_degree_four([1, 1], [0, 10], rows)
    correct = solve(net)
    # Relax the second row x1<=x0, which restricts the rewarded input.
    # Copy midpoint sources have quality1 or1/2 in this instance.
    k = max(i for i, (q, lo, hi) in enumerate(net.inputs)
            if q == 2 and lo == hi == 4)
    net.inputs[k] = (2, 0, 4)
    changed = solve(net)
    assert abs(correct-10) <= 1e-5 and abs(changed-correct) > .1
    print(f'PASS {count} full original-network solves; max input degree4, '
          f'output degree3; negative control {correct:.8g}->{changed:.8g}', flush=True)


if __name__ == '__main__':
    main()
