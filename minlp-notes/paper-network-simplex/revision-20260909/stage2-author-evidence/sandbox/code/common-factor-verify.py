"""Check balanced-star scalar partition against independent global optimization.

The partition uses exact rational breakpoints and coefficients. Stationary-point
evaluation and the independent Gurobi comparison use floating point. This checks
the simple fixed-total specialization, not the whole fixed-linking-row theorem.
Run with /home/sgusev/miniconda3/envs/minlp-notes/bin/python.
"""
from fractions import Fraction as F
from math import sqrt, inf
import random
import gurobipy as gp


def add_root(points, a, b, left, right):
    """Root of a+b/x=0, if strictly inside the positive interval."""
    if a:
        root = -b / a
        if left < root < right:
            points.add(root)


def solve_partition(data):
    a, b, lower, upper, plower, pupper, total, alpha, beta, gamma = data
    n = len(lower)
    points = {a, b}
    # All pairwise boundary crossings, including lower/upper feasibility.
    for j in range(n):
        for constant in (lower[j], upper[j]):
            for product in (plower[j], pupper[j]):
                add_root(points, constant, -product, a, b)
    for j in range(n):
        for k in range(j):
            if gamma[j] != gamma[k]:
                root = -(beta[j] - beta[k]) / (gamma[j] - gamma[k])
                if a < root < b:
                    points.add(root)
    initial = sorted(points)
    pieces = []
    for left, right in zip(initial, initial[1:]):
        mid = (left + right) / 2
        lo = [(lower[j], F(0)) if lower[j] >= plower[j]/mid
              else (F(0), plower[j]) for j in range(n)]
        up = [(upper[j], F(0)) if upper[j] <= pupper[j]/mid
              else (F(0), pupper[j]) for j in range(n)]
        if any(lo[j][0]+lo[j][1]/mid > up[j][0]+up[j][1]/mid for j in range(n)):
            continue
        order = sorted(range(n), key=lambda j: (beta[j]+gamma[j]*mid, j))
        cuts = {left, right}
        prefix_a = sum(t[0] for t in lo)
        prefix_b = sum(t[1] for t in lo)
        add_root(cuts, prefix_a-total, prefix_b, left, right)
        for j in order:
            prefix_a += up[j][0]-lo[j][0]
            prefix_b += up[j][1]-lo[j][1]
            add_root(cuts, prefix_a-total, prefix_b, left, right)
        points.update(cuts)
        cuts = sorted(cuts)
        for ll, rr in zip(cuts, cuts[1:]):
            mm = (ll+rr)/2
            ys = list(lo)
            remaining_a = total-sum(t[0] for t in lo)
            remaining_b = -sum(t[1] for t in lo)
            if remaining_a+remaining_b/mm < 0:
                continue
            for j in order:
                capacity_a = up[j][0]-lo[j][0]
                capacity_b = up[j][1]-lo[j][1]
                if remaining_a+remaining_b/mm >= capacity_a+capacity_b/mm:
                    ys[j] = up[j]
                    remaining_a -= capacity_a
                    remaining_b -= capacity_b
                else:
                    ys[j] = (lo[j][0]+remaining_a, lo[j][1]+remaining_b)
                    remaining_a = remaining_b = F(0)
                    break
            if remaining_a+remaining_b/mm > 0:
                continue
            aa = alpha+sum(gamma[j]*ys[j][0] for j in range(n))
            bb = sum(beta[j]*ys[j][0]+gamma[j]*ys[j][1] for j in range(n))
            cc = sum(beta[j]*ys[j][1] for j in range(n))
            pieces.append((ll, rr, aa, bb, cc))
    best = (inf, None)
    for ll, rr, aa, bb, cc in pieces:
        candidates = [float(ll), float(rr)]
        if aa > 0 and cc > 0:
            root = sqrt(float(cc/aa))
            if ll < root < rr:
                candidates.append(root)
        for x in candidates:
            value = float(aa)*x+float(bb)+float(cc)/x
            if value < best[0]:
                best = (value, x)
    # Endpoint LPs also capture isolated feasible scalar values.
    for x in points:
        lo = [max(lower[j], plower[j]/x) for j in range(n)]
        up = [min(upper[j], pupper[j]/x) for j in range(n)]
        if any(l > u for l, u in zip(lo, up)) or not sum(lo) <= total <= sum(up):
            continue
        y = list(lo)
        remaining = total-sum(y)
        for j in sorted(range(n), key=lambda j: (beta[j]+gamma[j]*x, j)):
            delta = min(up[j]-lo[j], remaining)
            y[j] += delta
            remaining -= delta
        value = alpha*x+sum((beta[j]+gamma[j]*x)*y[j] for j in range(n))
        if value < best[0]:
            best = (float(value), float(x))
    return best


def solve_global(data, env):
    a, b, lower, upper, plower, pupper, total, alpha, beta, gamma = data
    n = len(lower)
    model = gp.Model(env=env)
    model.Params.NonConvex = 2
    model.Params.OptimalityTol = 1e-9
    model.Params.FeasibilityTol = 1e-9
    model.Params.MIPGap = 1e-9
    model.Params.MIPGapAbs = 1e-8
    x = model.addVar(lb=float(a), ub=float(b))
    y = [model.addVar(lb=float(lower[j]), ub=float(upper[j])) for j in range(n)]
    w = [model.addVar(lb=float(plower[j]), ub=float(pupper[j])) for j in range(n)]
    for j in range(n):
        model.addQConstr(w[j] == x*y[j])
    model.addConstr(gp.quicksum(y) == float(total))
    model.setObjective(float(alpha)*x+gp.quicksum(float(beta[j])*y[j]+float(gamma[j])*w[j] for j in range(n)))
    model.optimize()
    if model.Status == gp.GRB.INFEASIBLE:
        return inf
    assert model.Status == gp.GRB.OPTIMAL, model.Status
    return model.ObjVal


def main():
    rng = random.Random(604911)
    env = gp.Env(empty=True)
    env.setParam('OutputFlag', 0)
    env.start()
    count = 0
    for n in range(1, 9):
        for rep in range(25):
            a, b = F(1), F(rng.randint(2, 5))
            lower = [F(rng.randint(-3, 2)) for _ in range(n)]
            upper = [l+F(rng.randint(1, 5)) for l in lower]
            plower = [F(rng.randint(-9, 5)) for _ in range(n)]
            pupper = [p+F(rng.randint(1, 14)) for p in plower]
            total = F(rng.randint(-3*n, 5*n), 2)
            alpha = F(rng.randint(-5, 5))
            beta = [F(rng.randint(-5, 5)) for _ in range(n)]
            gamma = [F(rng.randint(-5, 5)) for _ in range(n)]
            if rep == 0:  # Tied original costs and zero objective.
                alpha = F(0)
                beta = gamma = [F(0)]*n
            data = (a,b,lower,upper,plower,pupper,total,alpha,beta,gamma)
            ours, at = solve_partition(data)
            theirs = solve_global(data, env)
            assert (ours == theirs == inf) or abs(ours-theirs) <= 2e-6*max(1,abs(ours)), (data, ours, theirs, at)
            count += 1
    # Feasibility only at one scalar point, with no feasible open interval.
    isolated = (F(1),F(3),[F(1)],[F(1)],[F(2)],[F(2)],F(1),F(1),[F(0)],[F(0)])
    assert solve_partition(isolated) == (2., 2.)
    print(f'Passed {count} seeded mixed-sign balanced-star comparisons against global Gurobi.')
    print('Passed isolated feasible scalar regression x=2.')
    print('This is numerical corroboration of the fixed-total specialization; it is not a proof.')


if __name__ == '__main__':
    main()
