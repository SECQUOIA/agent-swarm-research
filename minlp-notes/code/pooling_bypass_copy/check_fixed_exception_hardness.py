"""Original physical networks for the five-exception hardness refinement.

Uses the existing signal-circuit front end. This separate compiler groups
unused ports into exact sources and splits arbitrary exact three-port
supplies. The solver receives only physical arc, node, and quality rows.
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
import random

import gurobipy as gp
from gurobipy import GRB

from check_constant_data import Circuit
from check_copy_reduction import reference


class ExactCircuit(Circuit):
    def compare(self, u, v, *, equality=False):
        source = self.net.source(3, 2, 2)
        self.request(u, source)
        self.request(v, source, positive=False)
        if not equality:
            slack = self.signal()
            self.request(slack, source)
        self.last_comparison_source = source

    def build(self):
        net = self.net
        for occurrences in self.uses:
            if any(half for _, _, half in occurrences):
                source = net.source(3, 2, 2)
                occurrences.extend([(source, True, False),
                                    (source, False, True), (source, False, True)])
        unused_by_gate = defaultdict(list)
        for i, occurrences in enumerate(self.uses):
            for half in [False, True]:
                modules = []
                for source, positive, is_half in occurrences:
                    if is_half != half:
                        continue
                    aa, ba, ab, bb = net.half_gadget() if half else net.gadget(0, 3)
                    chosen, unused = (ab, bb) if positive else (bb, ab)
                    net.attach(chosen, source)
                    unused_by_gate[source].append(unused)
                    modules.append((aa, ba))
                if i in self.intake_specs and not half:
                    quality = self.intake_specs[i]
                    aa, ba, ab, bb = net.gadget(0, quality)
                    net.private(ab)  # Two intended exceptional converter inputs.
                    source = net.source(quality, 2, 2)
                    net.attach(bb, source)
                    net.intakes.append((source, 2, 0))
                    modules.append((aa, ba))
                for k, (aa, _) in enumerate(modules):
                    link = net.source(0, 2, 2)
                    net.attach(modules[k-1][1], link)
                    net.attach(aa, link)
        for gate, ports in unused_by_gate.items():
            quality, lower, upper = net.inputs[gate]
            assert quality == 3 and lower == upper
            total_cap = sum(port[2] if len(port) == 3 else 2 for port in ports)
            complement = net.source(3, total_cap-upper, total_cap-upper)
            for port in ports:
                net.attach(port, complement)
        # Full and half gadget outputs were created with exact qualities.
        first = net.output(0, 1, None, 1)
        second = net.output(0, 1, None, 33)
        anchor = net.source(0, 0, 1)
        net.direct.append((anchor, first, 1))
        net.pool_outputs.extend([(first, 1), (second, 1)])
        split_exact_sources(net)
        check_restrictions(net)
        return net


def split_exact_sources(net):
    """Split supply two OR four sources without hidden port equations."""
    positions = defaultdict(list)
    for k, (i, _, _) in enumerate(net.direct):
        positions[i].append(k)
    for i, indices in positions.items():
        if len(indices) <= 2:
            continue
        assert len(indices) == 3
        quality, lower, upper = net.inputs[i]
        assert quality == 3 and lower == upper and upper in [2, 4]
        assert all(ii != i for ii, _, _ in net.intakes)
        caps = [net.direct[k][2] for k in indices]
        demand = sum(caps)-upper
        collector = net.output(demand, demand, quality, quality)
        for h, (k, cap) in enumerate(zip(indices, caps)):
            if h == 0:
                source = i
                net.inputs[i] = (quality, cap, cap)
            else:
                source = net.source(quality, cap, cap)
            _, target, _ = net.direct[k]
            net.direct[k] = (source, target, cap)
            net.direct.append((source, collector, cap))


def check_restrictions(net):
    ideg = Counter(i for i, _, _ in net.direct)
    ideg.update(i for i, _, _ in net.intakes)
    odeg = Counter(j for _, j, _ in net.direct)
    odeg.update(j for j, _ in net.pool_outputs)
    assert max(ideg.values()) <= 2 and max(odeg.values()) <= 3
    assert len(net.intakes) == len(net.pool_outputs) == 2
    assert len(net.direct) == len({(i, j) for i, j, _ in net.direct})
    input_exceptions = [i for i, (_, low, high) in enumerate(net.inputs) if low != high]
    output_exceptions = [j for j, (low, high, qlow, qhigh) in enumerate(net.outputs)
                         if low != high or qlow != qhigh]
    assert len(input_exceptions) == 3 and len(output_exceptions) == 2
    palette = {0, F(1, 2), 1, F(3, 2), 3, F(33, 2), 33}
    assert all(q in palette for q, _, _ in net.inputs)
    assert all(qhi in palette and (qlo is None or qlo in palette)
               for _, _, qlo, qhi in net.outputs)
    assert all(v in {0, 1, 2, 3, 4}
               for _, lo, hi in net.inputs for v in [lo, hi])
    assert all(v in {0, 1, 2, 3, 4}
               for lo, hi, _, _ in net.outputs for v in [lo, hi])
    assert all(cap in {0, 1, 2, 3, 4} for _, _, cap in net.direct)


def build(a, b, rows, threshold):
    circuit = ExactCircuit(len(a))
    for row, bound in rows:
        circuit.row({i: F(c-bound) for i, c in enumerate(row)}, 0)
    total = circuit.total(range(len(a)))
    high = circuit.total([circuit.scale(i, (F(a[i])-1)/32) for i in range(len(a))])
    low = circuit.signal()
    circuit.compare(circuit.add(low, high), total, equality=True)
    circuit.intake_specs = {low: 1, high: 33}
    circuit.row({i: -F(b[i]) for i in range(len(a))}, -F(threshold))
    return circuit.build()


def feasible(net):
    model = gp.Model()
    model.Params.OutputFlag = 0
    model.Params.NonConvex = 2
    model.Params.FeasibilityTol = 1e-9
    model.Params.TimeLimit = 60
    direct = [model.addVar(ub=cap) for _, _, cap in net.direct]
    feeds = [model.addVar(ub=cap) for _, cap, _ in net.intakes]
    outlets = [model.addVar(ub=cap) for _, cap in net.pool_outputs]
    q = model.addVar(lb=1, ub=33)
    total = gp.quicksum(feeds)
    model.addConstr(total == gp.quicksum(outlets))
    model.addConstr(gp.quicksum(net.inputs[i][0]*v for v, (i, _, _) in zip(feeds, net.intakes)) == q*total)
    for i, (_, lower, upper) in enumerate(net.inputs):
        flow = gp.quicksum(v for v, (ii, _, _) in zip(direct, net.direct) if ii == i)
        flow += gp.quicksum(v for v, (ii, _, _) in zip(feeds, net.intakes) if ii == i)
        model.addConstr(flow >= lower)
        model.addConstr(flow <= upper)
    for j, (lower, upper, qlow, qhigh) in enumerate(net.outputs):
        flow = gp.quicksum(v for v, (_, jj, _) in zip(direct, net.direct) if jj == j)
        mass = gp.quicksum(net.inputs[i][0]*v for v, (i, jj, _) in zip(direct, net.direct) if jj == j)
        pool = gp.quicksum(v for v, (jj, _) in zip(outlets, net.pool_outputs) if jj == j)
        flow += pool
        mass += q*pool
        model.addConstr(flow >= lower)
        model.addConstr(flow <= upper)
        if qlow is not None:
            model.addConstr(mass >= qlow*flow)
        if qhigh is not None:
            model.addConstr(mass <= qhigh*flow)
    model.optimize()
    assert model.Status in [GRB.OPTIMAL, GRB.INFEASIBLE], model.Status
    answer = model.Status == GRB.OPTIMAL
    model.dispose()
    return answer


def main():
    rng = random.Random(9361)
    cases = [([1], [2], [], 4), ([1], [2], [], 5),
             ([2, 3], [3, 4], [([1, -1], 0), ([-1, 1], 0)], 4),
             ([2, 3], [3, 4], [([1, 1], -1)], 1)]
    for _ in range(6):
        a = [rng.randint(1, 5) for _ in range(2)]
        b = [rng.randint(1, 6) for _ in range(2)]
        row = [rng.randint(-2, 2) for _ in range(2)]
        rows = [(row, (sum(row)+1)//2)]
        optimum, _ = reference(a, b, rows)
        cases.extend((a, b, rows, threshold) for threshold in [max(1, int(optimum)), int(optimum)+1])
    for k, (a, b, rows, threshold) in enumerate(cases):
        optimum, _ = reference(a, b, rows)
        net = build(a, b, rows, threshold)
        actual = feasible(net)
        assert actual == (optimum >= threshold), (a, b, rows, threshold, optimum, actual)
        print(f'case={k} exact_reference={optimum} threshold={threshold} feasible={actual} '
              f'inputs={len(net.inputs)} outputs={len(net.outputs)} exceptions=5', flush=True)
    print(f'PASS {len(cases)} original physical feasibility solves; '
          'exact ordinary contracts, five exceptions, fixed palette, input degree2/output degree3')


if __name__ == '__main__':
    main()
