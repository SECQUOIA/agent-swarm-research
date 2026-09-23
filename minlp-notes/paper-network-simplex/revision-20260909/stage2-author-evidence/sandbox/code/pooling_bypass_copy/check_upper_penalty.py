"""Small original-network experiments for restoring removed flow contracts.

These use moderate experimental penalties. They do not numerically verify
the much larger bit-complexity bound in the mathematical reduction.
"""
import argparse
import random

import gurobipy as gp
from gurobipy import GRB

from check_degree_three import build_degree_three
from check_upper_quality import build_upper_quality
from check_copy_reduction import reference


def penalized(net, penalty, *, private_reward=False, keep_contracts=False):
    model = gp.Model()
    model.Params.OutputFlag = 0
    model.Params.NonConvex = 2
    model.Params.MIPGap = 0
    model.Params.MIPGapAbs = 1e-7
    model.Params.FeasibilityTol = 1e-9
    model.Params.OptimalityTol = 1e-9
    model.Params.TimeLimit = 40
    d = [model.addVar(ub=cap) for _, _, cap in net.direct]
    x = [model.addVar(ub=cap) for _, cap, _ in net.intakes]
    y = [model.addVar(ub=cap) for _, cap in net.pool_outputs]
    t = model.addVar(ub=2)
    qualities = [net.inputs[i][0] for i, _, _ in net.intakes]
    q = model.addVar(lb=min(qualities), ub=max(qualities))
    model.addConstr(gp.quicksum(x) == t)
    model.addConstr(gp.quicksum(y) == t)
    model.addConstr(gp.quicksum(a*v for a, v in zip(qualities, x)) == q*t)
    deficits = []
    for i, (_, lo, hi) in enumerate(net.inputs):
        flow = gp.quicksum(v for v, (ii, _, _) in zip(d, net.direct) if ii == i)
        flow += gp.quicksum(v for v, (ii, _, _) in zip(x, net.intakes) if ii == i)
        model.addConstr(flow <= hi)
        model.addConstr(flow >= lo if keep_contracts else flow >= 0)
        if lo > 0:
            assert lo == hi
            deficits.append(hi-flow)
    for j, (lo, hi, qlo, qhi) in enumerate(net.outputs):
        flow = gp.quicksum(v for v, (_, jj, _) in zip(d, net.direct) if jj == j)
        flow += gp.quicksum(v for v, (jj, _) in zip(y, net.pool_outputs) if jj == j)
        mass = gp.quicksum(net.inputs[i][0]*v for v, (i, jj, _) in zip(d, net.direct) if jj == j)
        mass += gp.quicksum(q*v for v, (jj, _) in zip(y, net.pool_outputs) if jj == j)
        model.addConstr(flow <= hi)
        model.addConstr(flow >= lo if keep_contracts else flow >= 0)
        if qlo is not None:
            model.addConstr(mass >= qlo*flow)
        if qhi is not None:
            model.addConstr(mass <= qhi*flow)
        if lo > 0:
            assert lo == hi
            deficits.append(hi-flow)
    reward = gp.LinExpr()
    if private_reward:
        for source, _, b in net.intakes:
            quality = net.inputs[source][0]
            out_b = next(j for i, j, _ in net.direct if i == source)
            out_a = out_b-1
            candidates = [(v, i) for v, (i, j, _) in zip(d, net.direct)
                          if j == out_a and net.inputs[i][0] == quality]
            assert len(candidates) == 1
            v, i = candidates[0]
            assert sum(ii == i for ii, _, _ in net.direct) == 1
            reward += b*v
    else:
        reward = gp.quicksum(b*v for v, (_, _, b) in zip(x, net.intakes))
    deficit = gp.quicksum(deficits)
    model.setObjective(reward-penalty*deficit, GRB.MAXIMIZE)
    model.optimize()
    assert model.Status == GRB.OPTIMAL, model.Status
    result = (model.ObjVal, reward.getValue(), deficit.getValue())
    model.dispose()
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--trials', type=int, default=6)
    parser.add_argument('--upper-quality', action='store_true')
    parser.add_argument('--split-inputs', action='store_true')
    args = parser.parse_args()
    rng = random.Random(args.seed)
    if args.split_inputs:
        assert args.upper_quality
    build = (lambda a, b, rows: build_upper_quality(
        a, b, rows, split_inputs=args.split_inputs)) if args.upper_quality else build_degree_three
    count = 0
    for trial in range(args.trials):
        a = [rng.randint(2, 5), rng.randint(2, 5)]
        b = [rng.randint(0, 6), rng.randint(0, 6)]
        row = [rng.randint(-2, 3), rng.randint(-2, 3)]
        rows = [(row, (sum(row)+1)//2)]
        expected, _ = reference(a, b, rows)
        net = build(a, b, rows)
        for private in [False, True]:
            value, reward, delta = penalized(net, 100, private_reward=private)
            assert abs(value-float(expected)) <= 2e-4, (trial, value, expected)
            assert abs(delta) <= 1e-6, (trial, delta)
            count += 1
        print(f'trial={trial} exactprofit={expected} penalty100 restoredcontracts', flush=True)
    # Without a penalty, breaking copy contracts can improve the reward.
    net = build([2, 2], [0, 10],
                             [([1, -1], 0), ([-1, 1], 0)])
    expected, _ = reference([2, 2], [0, 10],
                             [([1, -1], 0), ([-1, 1], 0)])
    loose = penalized(net, 0)
    restored = penalized(net, 100)
    assert loose[0] > float(expected)+1 and loose[2] > 1e-3
    assert abs(restored[0]-float(expected)) <= 2e-4 and abs(restored[2]) < 1e-6
    print(f'PASS {count} moderate-penalty original-network solves; '
          f'negative control M0={loose}, M100={restored}; exact={expected}', flush=True)


if __name__ == '__main__':
    main()
