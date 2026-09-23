"""Independent assembly audit of the bypass copy network.

Builds ordinary input/output arcs, exact supplies/demands, and one quality.
No signal equalities or encoded cone rows are inserted into the network LP.
Checks projection objectives and complete pooling at fixed compositions.
"""

import math

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix


def sparse(rows, columns):
    entries = [(r, c, value) for r, row in enumerate(rows) for c, value in row.items() if value]
    return coo_matrix(([v for _, _, v in entries], ([r for r, _, _ in entries], [c for _, c, _ in entries])),
                      shape=(len(rows), columns)).tocsr()


class Network:
    def __init__(self, cone, qualities, shift):
        self.inputs, self.outputs, self.arcs = [], [], []
        self.cone = np.asarray(cone, dtype=int)
        self.n = len(qualities)
        self.qualities = np.asarray(qualities, dtype=float)
        self.shift = shift
        row_inputs = [self.input(2, 0, 2 * sum(max(0, -int(c)) for c in row)) for row in self.cone]
        self.intakes = []
        for variable, quality in enumerate(qualities):
            positive_count = sum(max(0, int(row[variable])) for row in self.cone)
            negative_count = sum(max(0, -int(row[variable])) for row in self.cone)
            count = max(1, positive_count, negative_count)
            gadgets = [self.gadget(0, 2) for _ in range(count)] + [self.gadget(0, quality)]
            self.private_port(0, gadgets[0][0])
            for left, right in zip(gadgets, gadgets[1:]):
                connector = self.input(0, 2, 2)
                self.arc(connector, left[1], 2)
                self.arc(connector, right[0], 2)
            self.private_port(0, gadgets[-1][1])
            positive = [g[0] for g in gadgets[:-1]]
            negative = [g[1] for g in gadgets[:-1]]
            used_positive = used_negative = 0
            for row, source in zip(self.cone, row_inputs):
                coefficient = int(row[variable])
                for _ in range(max(0, coefficient)):
                    self.arc(source, positive[used_positive], 2)
                    used_positive += 1
                for _ in range(max(0, -coefficient)):
                    self.arc(source, negative[used_negative], 2)
                    used_negative += 1
            for target in positive[used_positive:] + negative[used_negative:]:
                self.private_port(2, target)
            self.private_port(quality, gadgets[-1][0])
            pool_input = self.input(quality, 2, 2)
            self.arc(pool_input, gadgets[-1][1], 2)
            self.intakes.append(self.arc(pool_input, None, 2))

    def input(self, quality, lower, upper):
        self.inputs.append((quality + self.shift, lower, upper, []))
        return len(self.inputs) - 1

    def arc(self, source, target, upper):
        index = len(self.arcs)
        self.arcs.append((source, target, upper))
        self.inputs[source][3].append(index)
        if target is not None:
            self.outputs[target][1].append(index)
        return index

    def private_port(self, quality, target):
        self.arc(self.input(quality, 0, 2), target, 2)

    def gadget(self, alpha, beta):
        gamma = (alpha + beta) / 2
        first = len(self.outputs)
        self.outputs.extend([(gamma + self.shift, []), (gamma + self.shift, [])])
        middle = self.input(gamma, 4, 4)
        self.arc(middle, first, 4)
        self.arc(middle, first + 1, 4)
        return first, first + 1

    def optimize(self, rewards, composition=None, break_middle=False):
        eq, eq_rhs, ub, ub_rhs = [], [], [], []
        for quality, lower, upper, arcs in self.inputs:
            row = {e: 1 for e in arcs}
            if lower == upper and not (break_middle and lower == 4):
                eq.append(row)
                eq_rhs.append(lower)
            else:
                ub.append(row)
                ub_rhs.append(upper)
                if lower and not break_middle:
                    ub.append({e: -1 for e in arcs})
                    ub_rhs.append(-lower)
        for quality, incoming in self.outputs:
            assert len(incoming) == 3
            eq.extend([{e: 1 for e in incoming},
                       {e: self.inputs[self.arcs[e][0]][0] for e in incoming}])
            eq_rhs.extend([4, 4 * quality])
        bounds = [(0, arc[2]) for arc in self.arcs]
        objective = np.zeros(len(bounds) + (3 if composition is not None else 0))
        for e, reward in zip(self.intakes, rewards):
            objective[e] = -reward
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
        return -result.fun


def main():
    rng = np.random.default_rng(61492)
    cones = [np.array([[1, -1], [-1, 1]])]
    for _ in range(6):
        rows = rng.integers(-2, 3, (4, 3))
        for row in rows:
            row -= max(0, math.ceil(sum(row) / 3))
        cones.append(rows)
    projection_checks = pooling_checks = invalid = 0
    for cone in cones:
        n = cone.shape[1]
        qualities = np.arange(n) * 2 + 3
        rewards = np.arange(n) * 3 + 2
        compositions = [np.ones(n) / n] + list(np.eye(n))
        for _ in range(4):
            weights = rng.integers(1, 8, n)
            compositions.append(weights / sum(weights))
        for shift in [0, 3]:
            network = Network(cone, qualities, shift)
            for _ in range(4):
                objective = rng.integers(-4, 5, n)
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
                invalid += not admissible
    # Break the exact middle supply: the row equations no longer enforce
    # equality of the two variables at their pool-intake interfaces.
    network = Network(cones[0], [3, 5], 0)
    intact = network.optimize([1, -1])
    broken = network.optimize([1, -1], break_middle=True)
    assert abs(intact) < 1e-8 and broken > 1
    print(f"PASS: {projection_checks} full copy-network projection LPs against explicit cones.")
    print(f"PASS: {pooling_checks} full pooling fixed-composition LPs, including {invalid} excluded compositions.")
    print(f"Negative control: weakening middle fixed supplies changes max(x0-x1) from {intact:g} to {broken:g}.")
    print("Both original and shifted qualities tested; no cone rows or signal-copy equalities inserted in network LP.")


if __name__ == "__main__":
    main()
