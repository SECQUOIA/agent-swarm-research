"""Independent degree-four network assembly and projection checks.

Reuses only the earlier independent checker's ordinary node/arc LP backend.
The constructor below uses actual averaging-source supplies and copy gadgets;
no averaging equations, source-cone rows, or hidden signal equalities enter
the network LP.
"""

import math
from collections import defaultdict

import numpy as np
from scipy.optimize import linprog

from independent_review import Network


class AveragingNetwork(Network):
    def __init__(self, cone, qualities, shift):
        self.inputs, self.outputs, self.arcs = [], [], []
        self.cone = np.asarray(cone, dtype=int)
        self.n = len(qualities)
        self.qualities = np.asarray(qualities, dtype=float)
        self.shift = shift
        requests = defaultdict(list)
        zero = self.n
        signal_count = self.n + 1
        self.averaging_sources = []
        requests[zero].append((False, self.input(2, 0, 0)))
        for row in self.cone:
            leaves = [(i, c < 0) for i, c in enumerate(row) for _ in range(abs(int(c)))]
            if not leaves:
                continue
            count = 1 << (len(leaves) - 1).bit_length()
            leaves.extend([(zero, False)] * (count - len(leaves)))
            level = leaves
            while len(level) > 1:
                next_level = []
                for left, right in zip(level[::2], level[1::2]):
                    parent = signal_count
                    signal_count += 1
                    source = self.input(2, 4, 4)
                    self.averaging_sources.append(source)
                    requests[parent].extend([(False, source), (False, source)])
                    requests[left[0]].append((not left[1], source))
                    requests[right[0]].append((not right[1], source))
                    next_level.append((parent, False))
                level = next_level
            root = level[0]
            capacity = 2 * sum(max(0, -int(c)) for c in row) / count
            requests[root[0]].append((root[1], self.input(2, 0, capacity)))

        self.intakes = []
        for signal in range(signal_count):
            needed = requests[signal]
            ordinary_count = max(1, len(needed))
            gadgets = [self.gadget(0, 2) for _ in range(ordinary_count)]
            original = signal < self.n
            if original:
                gadgets.append(self.gadget(0, qualities[signal]))
            self.private_port(0, gadgets[0][0])
            for left, right in zip(gadgets, gadgets[1:]):
                connector = self.input(0, 2, 2)
                self.arc(connector, left[1], 2)
                self.arc(connector, right[0], 2)
            self.private_port(0, gadgets[-1][1])
            for index in range(ordinary_count):
                first, second = gadgets[index]
                if index < len(needed):
                    complement, source = needed[index]
                    self.arc(source, second if complement else first, 2)
                    self.private_port(2, first if complement else second)
                else:
                    self.private_port(2, first)
                    self.private_port(2, second)
            if original:
                quality = qualities[signal]
                self.private_port(quality, gadgets[-1][0])
                pool_source = self.input(quality, 2, 2)
                self.arc(pool_source, gadgets[-1][1], 2)
                self.intakes.append(self.arc(pool_source, None, 2))

        assert max(len(arcs) for _, _, _, arcs in self.inputs) <= 4
        assert all(len(incoming) == 3 for _, incoming in self.outputs)
        assert max(upper for _, _, upper, _ in self.inputs) <= 4
        assert max(upper for _, _, upper in self.arcs) <= 4
        assert len({(u, v) for u, v, _ in self.arcs}) == len(self.arcs)

    def weakened_average_optimum(self, rewards):
        old = {i: self.inputs[i] for i in self.averaging_sources}
        for i, (quality, _, upper, arcs) in old.items():
            self.inputs[i] = quality, 0, upper, arcs
        result = self.optimize(rewards)
        for i, data in old.items():
            self.inputs[i] = data
        return result


def main():
    random = np.random.default_rng(84316)
    cones = [np.array([[1, -1], [-1, 1]]),
             np.array([[1, 0], [0, -1]]),
             np.array([[0, 0], [1, 1]]),
             np.array([[2, -1, -2]])]
    for _ in range(6):
        rows = random.integers(-2, 3, (3, 3))
        for row in rows:
            row -= max(0, math.ceil(sum(row) / 3))
        cones.append(rows)
    projection_checks = pooling_checks = excluded = 0
    for cone in cones:
        n = cone.shape[1]
        qualities = np.arange(n) * 2 + 3
        rewards = np.arange(n) * 3 + 2
        compositions = [np.ones(n) / n] + list(np.eye(n))
        weights = random.integers(1, 8, n)
        compositions.append(weights / sum(weights))
        for shift in [0, 3]:
            network = AveragingNetwork(cone, qualities, shift)
            for _ in range(4):
                objective = random.integers(-4, 5, n)
                reference = linprog(-objective, A_ub=np.vstack([cone, np.ones(n)]),
                                    b_ub=np.r_[np.zeros(len(cone)), 2], bounds=[(0, 2)] * n,
                                    method="highs")
                assert reference.success
                assert abs(network.optimize(objective) + reference.fun) < 1e-8
                projection_checks += 1
            for z in compositions:
                admissible = np.max(cone @ z) <= 1e-10
                expected = float(z @ rewards) * (1 + 1 / float(z @ qualities)) if admissible else 0.0
                assert abs(network.optimize(rewards, composition=z) - expected) < 1e-8
                pooling_checks += 1
                excluded += not admissible
    network = AveragingNetwork(cones[0], [3, 5], 0)
    intact, broken = network.optimize([1, -1]), network.weakened_average_optimum([1, -1])
    assert abs(intact) < 1e-8 and broken > 1
    print(f"PASS: {projection_checks} degree-four network projection LPs against explicit cones.")
    print(f"PASS: {pooling_checks} complete fixed-composition pooling LPs, including {excluded} excluded compositions.")
    print("Includes zero rows, one-port rows, repeated variables, padded trees, empty simplex sections, and shifted qualities.")
    print(f"Negative control weakening only averaging supplies: max(x0-x1) changes from {intact:g} to {broken:g}.")
    print("All generated input degrees <=4, output degrees=3, flow upper bounds<=4, and no parallel arcs.")


if __name__ == "__main__":
    main()
