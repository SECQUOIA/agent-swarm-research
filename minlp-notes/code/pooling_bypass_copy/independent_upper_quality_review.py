"""Independent upper-quality cyclic network assembly and projection checks.

Reuses only the earlier independent checker's ordinary node/arc LP backend.
The constructor below uses actual averaging-source supplies and copy gadgets;
no averaging equations, source-cone rows, or hidden signal equalities enter
the network LP.
"""

import math
from collections import defaultdict

import numpy as np
from scipy.optimize import linprog

from independent_review import Network, sparse


class AveragingNetwork(Network):
    def __init__(self, cone, qualities, shift):
        self.inputs, self.outputs, self.arcs = [], [], []
        self.demands = {}
        self.cone = np.asarray(cone, dtype=int)
        self.n = len(qualities)
        self.qualities = np.asarray(qualities, dtype=float)
        self.shift = shift
        requests = defaultdict(list)
        zero = self.n
        signal_count = self.n + 1
        self.averaging_sources = []
        requests[zero].append((False, False, self.input(3, 0, 0)))
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
                    source = self.input(3, 2, 2)
                    self.averaging_sources.append(source)
                    requests[parent].append((False, False, source))
                    requests[left[0]].append((True, not left[1], source))
                    requests[right[0]].append((True, not right[1], source))
                    next_level.append((parent, False))
                level = next_level
            root = level[0]
            capacity = 2 * sum(max(0, -int(c)) for c in row) / count
            requests[root[0]].append((False, root[1], self.input(3, 0, capacity)))

        for signal in range(signal_count):
            if any(half for half, _, _ in requests[signal]):
                source = self.input(3, 2, 2)
                requests[signal].extend([(False, False, source),
                                         (True, True, source),
                                         (True, True, source)])
        self.intakes, self.cycle_sources, self.reward_inputs = [], [], []
        for signal in range(signal_count):
            for half in (False, True):
                gadgets = []
                for requested_half, complement, source in requests[signal]:
                    if requested_half != half:
                        continue
                    first, second = self.half_gadget() if half else self.gadget(0, 3)
                    gadgets.append((first, second))
                    cap = 1 if half else 2
                    self.arc(source, second if complement else first, cap)
                    self.private_endpoint(3, first if complement else second, cap)
                if signal < self.n and not half:
                    quality = qualities[signal]
                    first, second = self.gadget(0, quality)
                    gadgets.append((first, second))
                    reward_input = self.input(quality, 0, 2)
                    self.arc(reward_input, first, 2)
                    self.reward_inputs.append(reward_input)
                    pool_source = self.input(quality, 2, 2)
                    self.arc(pool_source, second, 2)
                    self.intakes.append(self.arc(pool_source, None, 2))
                for index, gadget in enumerate(gadgets):
                    previous = gadgets[index - 1]
                    connector = self.input(0, 2, 2)
                    self.cycle_sources.append(connector)
                    self.arc(connector, previous[1], 2)
                    self.arc(connector, gadget[0], 2)

        assert max(len(arcs) for _, _, _, arcs in self.inputs) <= 3
        assert all(len(incoming) == 3 for _, incoming in self.outputs)
        assert max(upper for _, _, upper, _ in self.inputs) <= 4
        assert max(upper for _, _, upper in self.arcs) <= 4
        assert len({(u, v) for u, v, _ in self.arcs}) == len(self.arcs)

    def split_three_port_inputs(self):
        targets = [i for i, (_, lower, upper, arcs) in enumerate(self.inputs)
                   if len(arcs) == 3]
        for original in targets:
            quality, lower, upper, original_arcs = self.inputs[original]
            assert lower == upper == 2
            arcs = list(original_arcs)
            caps = [self.arcs[e][2] for e in arcs]
            assert sorted(caps) == [1, 1, 2]
            collector = len(self.outputs)
            self.outputs.append((quality, []))
            self.demands[collector] = 2
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
        assert max(len(arcs) for _, _, _, arcs in self.inputs) <= 2
        assert all(len(arcs) == 3 for _, arcs in self.outputs)
        assert len({(u, v) for u, v, _ in self.arcs}) == len(self.arcs)

    def private_endpoint(self, quality, target, cap):
        self.arc(self.input(quality, 0, cap), target, cap)

    def half_gadget(self):
        first = len(self.outputs)
        self.outputs.extend([(1 + self.shift, []), (1 + self.shift, [])])
        self.demands[first] = self.demands[first + 1] = 3
        middle = self.input(1, 3, 3)
        self.arc(middle, first, 3)
        self.arc(middle, first + 1, 3)
        return first, first + 1

    def optimize(self, rewards, composition=None, penalty=None, private_rewards=False):
        eq, eq_rhs, ub, ub_rhs = [], [], [], []
        contracts = []
        for quality, lower, upper, arcs in self.inputs:
            row = {e: 1 for e in arcs}
            if lower == upper:
                contracts.append((row, lower))
            if lower == upper and penalty is None:
                eq.append(row)
                eq_rhs.append(lower)
            else:
                ub.append(row)
                ub_rhs.append(upper)
                if lower and penalty is None:
                    ub.append({e: -1 for e in arcs})
                    ub_rhs.append(-lower)
        for output_index, (quality, incoming) in enumerate(self.outputs):
            assert len(incoming) == 3
            demand = self.demands.get(output_index, 4)
            mass = {e: 1 for e in incoming}
            contracts.append((mass, demand))
            if penalty is None:
                eq.append(mass)
                eq_rhs.append(demand)
            else:
                ub.append(mass)
                ub_rhs.append(demand)
            ub.append({e: self.inputs[self.arcs[e][0]][0] - quality for e in incoming})
            ub_rhs.append(0)

        bounds = [(0, arc[2]) for arc in self.arcs]
        objective = np.zeros(len(bounds) + (3 if composition is not None else 0))
        for i, (e, reward) in enumerate(zip(self.intakes, rewards)):
            rewarded_arcs = self.inputs[self.reward_inputs[i]][3] if private_rewards else [e]
            for arc in rewarded_arcs:
                objective[arc] -= reward
        if penalty is not None:
            for row, _ in contracts:
                for e, coefficient in row.items():
                    objective[e] -= penalty * coefficient
        ub.append({e: 1 for e in self.intakes})
        ub_rhs.append(2)
        if composition is not None:
            z = np.asarray(composition)
            for e, zi in zip(self.intakes, z):
                row = {f: -zi for f in self.intakes}
                row[e] += 1
                eq.append(row)
                eq_rhs.append(0)
            y1, y2, anchor = range(len(bounds), len(bounds) + 3)
            bounds.extend([(0, 1)] * 3)
            eq.append({**{e: 1 for e in self.intakes}, y1: -1, y2: -1})
            eq_rhs.append(0)
            ub.append({y1: 1, anchor: 1})
            ub_rhs.append(1)
            pool_quality = float(z @ self.qualities) + self.shift
            ub.extend([{y1: pool_quality - (1 + self.shift), anchor: self.shift - (1 + self.shift)},
                       {y2: pool_quality - (max(self.qualities) + self.shift)}])
            ub_rhs.extend([0, 0])
        result = linprog(objective, A_ub=sparse(ub, len(bounds)), b_ub=ub_rhs,
                         A_eq=sparse(eq, len(bounds)), b_eq=eq_rhs, bounds=bounds, method="highs")
        assert result.success, result.message
        self.last_deficit = sum(rhs - sum(coef * result.x[e] for e, coef in row.items())
                                for row, rhs in contracts)
        self.last_offset = (penalty or 0) * sum(rhs for _, rhs in contracts)
        return -result.fun - self.last_offset

    def weakened_average_optimum(self, rewards):
        old = {i: self.inputs[i] for i in self.averaging_sources}
        for i, (quality, _, upper, arcs) in old.items():
            self.inputs[i] = quality, 0, upper, arcs
        result = self.optimize(rewards)
        for i, data in old.items():
            self.inputs[i] = data
        return result


def main():
    random = np.random.default_rng(455817)
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
            for _ in range(5):
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
    intact = network.optimize([1, -1])
    for i in network.cycle_sources:
        quality, lower, _, arcs = network.inputs[i]
        network.inputs[i] = quality, lower, 4, arcs
    broken = network.optimize([1, -1])
    assert abs(intact) < 1e-8 and broken > 1
    print(f"PASS: {projection_checks} cyclic upper-quality network projection LPs against explicit cones.")
    print(f"PASS: {pooling_checks} complete fixed-composition pooling LPs, including {excluded} excluded compositions.")
    print("Includes zero rows, one-port rows, repeated variables, padded trees, empty simplex sections, and shifted qualities.")
    print(f"Negative control increasing only cyclic supply upper bounds: max(x0-x1) changes from {intact:g} to {broken:g}.")
    penalty_checks = 0
    for cone in cones[:4]:
        n = cone.shape[1]
        for private in [False, True]:
            network = AveragingNetwork(cone, [3] * n, 0)
            rewards = np.arange(n) * 3 + 2
            # Common composition is admissible or zero; this test compares
            # fixed-composition exact-contract and penalized LPs directly.
            composition = np.ones(n) / n
            exact = network.optimize(rewards, composition=composition, private_rewards=private)
            penalized = network.optimize(rewards, composition=composition,
                                         penalty=1000, private_rewards=private)
            assert abs(exact - penalized) < 1e-7
            assert abs(network.last_deficit) < 1e-8
            penalty_checks += 1
    split_checks = 0
    for cone in cones[:4]:
        n = cone.shape[1]
        for shift in [0, 3]:
            network = AveragingNetwork(cone, [3] * n, shift)
            rewards = np.arange(n) * 3 + 2
            exact = network.optimize(rewards)
            network.split_three_port_inputs()
            assert abs(network.optimize(rewards) - exact) < 1e-8
            split_checks += 1
            composition = np.ones(n) / n
            for private in [False, True]:
                exact = network.optimize(rewards, composition=composition, private_rewards=private)
                penalized = network.optimize(rewards, composition=composition,
                                             penalty=1000, private_rewards=private)
                assert abs(exact - penalized) < 1e-7
                assert abs(network.last_deficit) < 1e-8
                split_checks += 1
    print(f"PASS: {split_checks} degree-two input splitter checks, including scalar upper quality and penalties.")
    print(f"PASS: {penalty_checks} penalty LPs with both intake and private-source rewards; every contract restored.")
    print("All generated input degrees <=3, output degrees=3, flow upper bounds<=4, and no parallel arcs.")


if __name__ == "__main__":
    main()
