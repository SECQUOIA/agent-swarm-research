"""Assemble and solve original one-pool bypass-copy networks.

No copied equality or source cone is added directly to the tested model.
Only node bounds, arc bounds, blending, and output quality bounds are used.
"""
from pathlib import Path
import argparse
import random
import sys

import gurobipy as gp
from gurobipy import GRB

sys.path.insert(0, str(Path(__file__).resolve().parents[1] /
                       'pooling_two_pools_two_outputs'))
from check_reduction import reference


class Network:
    def __init__(self):
        self.inputs = []   # quality, lower supply, upper supply
        self.outputs = []  # lower demand, upper demand, lower quality, upper quality
        self.direct = []   # input, output, capacity
        self.intakes = []  # input, capacity, profit
        self.pool_outputs = []
        self.mid_inputs = []

    def source(self, quality, low, high):
        i = len(self.inputs)
        self.inputs.append((quality, low, high))
        return i

    def output(self, low, high, qlow, qhigh):
        j = len(self.outputs)
        self.outputs.append((low, high, qlow, qhigh))
        return j

    def attach(self, port, source):
        j, quality = port
        assert quality == self.inputs[source][0]
        self.direct.append((source, j, 2))

    def private(self, port):
        self.attach(port, self.source(port[1], 0, 2))

    def gadget(self, alpha, beta):
        assert alpha != beta
        gamma = (alpha+beta)/2
        out = [self.output(4, 4, gamma, gamma) for _ in range(2)]
        mid = self.source(gamma, 4, 4)
        self.mid_inputs.append(mid)
        self.direct.extend((mid, j, 4) for j in out)
        return ((out[0], alpha), (out[1], alpha),
                (out[0], beta), (out[1], beta))


def build(a, b, rows):
    """Rows A z<=d on the simplex become (A-d) x<=0."""
    n = len(a)
    net = Network()
    cone = [[int(v-bound) for v in row] for row, bound in rows]
    assert all(v-bound == int(v-bound) for row, bound in rows for v in row)
    row_sources = [net.source(2, 0, 2*sum(-v for v in row if v < 0))
                   for row in cone]
    uses = [[] for _ in range(n)]
    for r, row in enumerate(cone):
        for i, coefficient in enumerate(row):
            uses[i].extend((r, coefficient > 0) for _ in range(abs(coefficient)))
    for i in range(n):
        previous = None
        for row, positive in uses[i]:
            aa, ba, ab, bb = net.gadget(0, 2)
            if previous is None:
                net.private(aa)
            else:
                source = net.source(0, 2, 2)
                net.attach(previous, source)
                net.attach(aa, source)
            chosen, unused = (ab, bb) if positive else (bb, ab)
            net.attach(chosen, row_sources[row])
            net.private(unused)
            previous = ba
        aa, ba, ab, bb = net.gadget(0, a[i])
        if previous is None:
            net.private(aa)
        else:
            source = net.source(0, 2, 2)
            net.attach(previous, source)
            net.attach(aa, source)
        net.private(ba)
        net.private(ab)
        source = net.source(a[i], 2, 2)
        net.attach(bb, source)
        net.intakes.append((source, 2, b[i]))
    out1 = net.output(0, 1, None, 1)
    out2 = net.output(0, 1, None, max(a))
    anchor = net.source(0, 0, 1)
    net.direct.append((anchor, out1, 1))
    net.pool_outputs.extend((j, 1) for j in [out1, out2])
    return net


def solve(net, *, shift=0, relax_middle_supply=False):
    model = gp.Model()
    model.Params.OutputFlag = 0
    model.Params.NonConvex = 2
    model.Params.MIPGap = 0
    model.Params.MIPGapAbs = 1e-8
    model.Params.FeasibilityTol = 1e-9
    model.Params.OptimalityTol = 1e-9
    model.Params.TimeLimit = 45
    direct = [model.addVar(ub=cap) for _, _, cap in net.direct]
    x = [model.addVar(ub=cap) for _, cap, _ in net.intakes]
    y = [model.addVar(ub=cap) for _, cap in net.pool_outputs]
    t = model.addVar(ub=2)
    pool_lam = [net.inputs[i][0]+shift for i, _, _ in net.intakes]
    q = model.addVar(lb=min(pool_lam), ub=max(pool_lam))
    model.addConstr(gp.quicksum(x) == t)
    model.addConstr(gp.quicksum(y) == t)
    model.addConstr(gp.quicksum(lam*v for lam, v in zip(pool_lam, x)) == q*t)
    for i, (_, low, high) in enumerate(net.inputs):
        flow = gp.quicksum(v for v, (ii, _, _) in zip(direct, net.direct) if ii == i)
        flow += gp.quicksum(v for v, (ii, _, _) in zip(x, net.intakes) if ii == i)
        if relax_middle_supply and i in net.mid_inputs:
            low = 0
        model.addConstr(flow >= low)
        model.addConstr(flow <= high)
    for j, (low, high, qlow, qhigh) in enumerate(net.outputs):
        flow = gp.quicksum(v for v, (_, jj, _) in zip(direct, net.direct) if jj == j)
        flow += gp.quicksum(v for v, (jj, _) in zip(y, net.pool_outputs) if jj == j)
        mass = gp.quicksum((net.inputs[i][0]+shift)*v
                           for v, (i, jj, _) in zip(direct, net.direct) if jj == j)
        mass += gp.quicksum(q*v for v, (jj, _) in zip(y, net.pool_outputs) if jj == j)
        model.addConstr(flow >= low)
        model.addConstr(flow <= high)
        if qlow is not None:
            model.addConstr(mass >= (qlow+shift)*flow)
        if qhigh is not None:
            model.addConstr(mass <= (qhigh+shift)*flow)
    model.setObjective(gp.quicksum(profit*v for v, (_, _, profit)
                                  in zip(x, net.intakes)), GRB.MAXIMIZE)
    model.optimize()
    assert model.Status == GRB.OPTIMAL, model.Status
    answer = model.ObjVal
    model.dispose()
    return answer


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--trials', type=int, default=12)
    args = parser.parse_args()
    rng = random.Random(args.seed)
    count = 0
    for trial in range(args.trials):
        n = 2+trial % 2
        a = [rng.randint(1, 6) for _ in range(n)]
        b = [rng.randint(0, 8) for _ in range(n)]
        rows = []
        for _ in range(2):
            row = [rng.randint(-2, 3) for _ in range(n)]
            rows.append((row, (sum(row)+n-1)//n))
        expected, vs = reference(a, b, rows)
        net = build(a, b, rows)
        for shift in [0, 3]:
            actual = solve(net, shift=shift)
            assert abs(actual-float(expected)) <= 2e-5, (trial, actual, expected)
            count += 1
        print(f'trial={trial} inputs={len(net.inputs)} '
              f'outputs={len(net.outputs)} profit={expected}', flush=True)
    for a, b, rows in [([2, 3], [4, 5], [([1, 1], -1)]),
                       ([2, 4], [0, 0], []),
                       ([1], [3], [])]:
        expected, _ = reference(a, b, rows)
        actual = solve(build(a, b, rows))
        assert abs(actual-float(expected)) <= 2e-5, (actual, expected)
        count += 1
    # The equality x0=x1 must hold on the actual pool intakes.
    net = build([1, 1], [0, 10], [([1, -1], 0), ([-1, 1], 0)])
    good = solve(net)
    broken = solve(net, relax_middle_supply=True)
    assert abs(good-10) <= 1e-5 and broken > 10.1, (good, broken)
    print(f'PASS {count} full original-network solves; '
          f'negative control exact={good:.8g}, relaxed-middle={broken:.8g}', flush=True)


if __name__ == '__main__':
    main()
