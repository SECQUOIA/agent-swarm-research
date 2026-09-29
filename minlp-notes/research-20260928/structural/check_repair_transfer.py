"""Targeted finite checks for the tree repair transfer and cyclic obstruction.

This is a numerical LP check, not a proof of the compact-space theorem.
The deterministic constants are enumerated with exact rational arithmetic.
"""

from fractions import Fraction
from itertools import product

import numpy as np
from scipy.optimize import linprog


def distance(x, y):
    return sum(abs(a - b) for a, b in zip(x, y))


def compatible(records, edges):
    return all(records[u][i] == records[v][j] for u, i, v, j in edges)


def residual(records, edges):
    return sum(abs(records[u][i] - records[v][j]) for u, i, v, j in edges)


def exact_data(bags, edges):
    tuples = list(product(*bags))
    feasible = [x for x in tuples if compatible(x, edges)]
    assert feasible
    constant = Fraction(0)
    witness = None
    for x in tuples:
        r = residual(x, edges)
        d = min(sum(distance(a, b) for a, b in zip(x, y)) for y in feasible)
        if r == 0:
            assert d == 0
        elif Fraction(d, r) > constant:
            constant, witness = Fraction(d, r), x
    return feasible, constant, witness


def law_residual(bags, laws, edges):
    # Every separator here is a single binary variable, for which W1 is
    # the absolute difference between success probabilities.
    return sum(
        abs(
            sum(p * x[i] for p, x in zip(laws[u], bags[u]))
            - sum(p * x[j] for p, x in zip(laws[v], bags[v]))
        )
        for u, i, v, j in edges
    )


def law_repair(bags, laws, feasible):
    # Variables: a common global law nu, and a transport from each local
    # bag law to its marginal under nu. This does not use the alternative
    # joint-tuple distance formula from the theorem being checked.
    nf = len(feasible)
    offsets = []
    nvars = nf
    for bag in bags:
        offsets.append(nvars)
        nvars += len(bag) * nf
    objective = np.zeros(nvars)
    rows, rhs = [], []
    for v, (bag, law) in enumerate(zip(bags, laws)):
        offset = offsets[v]
        for a, atom in enumerate(bag):
            row = np.zeros(nvars)
            row[offset + a * nf : offset + (a + 1) * nf] = 1
            rows.append(row)
            rhs.append(law[a])
            for k, target in enumerate(feasible):
                objective[offset + a * nf + k] = distance(atom, target[v])
        for k in range(nf):
            row = np.zeros(nvars)
            row[k] = -1
            for a in range(len(bag)):
                row[offset + a * nf + k] = 1
            rows.append(row)
            rhs.append(0)
    result = linprog(objective, A_eq=np.asarray(rows), b_eq=rhs,
                     bounds=(0, None), method="highs")
    assert result.success, result.message
    return result.fun


def check_exact_messages(bags, feasible, constant, witness):
    """Check tree DP certificates against exact enumeration of all tuples."""
    rng = np.random.default_rng(28092026)
    edges = [(0, 1, 1, 0), (1, 1, 2, 0)]
    for _ in range(20):
        costs = [[Fraction(int(a), 7) for a in rng.integers(-12, 13, len(bag))]
                 for bag in bags]
        for penalty in (Fraction(0), Fraction(1, 2), Fraction(2), Fraction(3)):
            messages = {}
            for v in (2, 1):
                # Both nonroot bags use their first coordinate for the parent
                # separator and their second coordinate for the child.
                av = [costs[v][i] + (messages[v + 1][x[1]] if v == 1 else 0)
                      for i, x in enumerate(bags[v])]
                messages[v] = {
                    s: min(a + penalty * abs(x[0] - s)
                           for a, x in zip(av, bags[v]))
                    for s in (0, 1)
                }
                assert abs(messages[v][0] - messages[v][1]) <= penalty
            local_mins = []
            for v, bag in enumerate(bags):
                local_mins.append(min(
                    costs[v][i]
                    + (messages[v + 1][x[1]] if v < 2 else 0)
                    - (messages[v][x[0]] if v > 0 else 0)
                    for i, x in enumerate(bag)
                ))
            enumerated = min(
                sum(costs[v][bags[v].index(x[v])] for v in range(3))
                + penalty * residual(x, edges)
                for x in product(*bags)
            )
            assert sum(local_mins) == enumerated

    # The distance objective centered at the sharp deterministic witness
    # proves the universal penalty threshold cannot be smaller.
    def cost(x):
        return sum(distance(a, b) for a, b in zip(witness, x))

    feasible_optimum = min(map(cost, feasible))
    for penalty in (constant - Fraction(1, 2), constant, constant + 1):
        values = [(cost(x) + penalty * residual(x, edges), x)
                  for x in product(*bags)]
        optimum = min(value for value, _ in values)
        if penalty < constant:
            assert optimum < feasible_optimum
        else:
            assert optimum == feasible_optimum
        if penalty > constant:
            assert all(compatible(x, edges) for value, x in values if value == optimum)
    print("messages: 80 exact rational dual/enumeration comparisons passed; "
          "sharp penalty threshold checked below, at, and above Cdet")


def main():
    bags = [
        [(0, 0), (0, 1), (1, 1)],
        [(0, 1), (1, 0), (1, 1)],
        [(0, 0), (0, 1), (1, 1)],
    ]
    edges = [(0, 1, 1, 0), (1, 1, 2, 0)]
    feasible, constant, witness = exact_data(bags, edges)
    rng = np.random.default_rng(9282026)
    largest_ratio = 0.0
    for _ in range(300):
        laws = [rng.dirichlet(np.ones(len(bag))) for bag in bags]
        r = law_residual(bags, laws, edges)
        d = law_repair(bags, laws, feasible)
        assert d <= float(constant) * r + 1e-8, (d, constant, r)
        if r > 1e-9:
            largest_ratio = max(largest_ratio, d / r)
    laws = [np.asarray([float(x == a) for x in bag])
            for bag, a in zip(bags, witness)]
    r = law_residual(bags, laws, edges)
    d = law_repair(bags, laws, feasible)
    assert abs(d / r - float(constant)) < 1e-8
    print(f"tree: exact Cdet={constant}; 300 law LP checks passed; "
          f"largest random ratio={largest_ratio:.9f}; Dirac witness attains Cdet")
    check_exact_messages(bags, feasible, constant, witness)

    full_bag = list(product((0, 1), repeat=2))
    bags = [full_bag] * 3  # coordinates 12, 23, 13
    edges = [(0, 1, 1, 0), (1, 1, 2, 1), (2, 0, 0, 0)]
    feasible, constant, _ = exact_data(bags, edges)
    equal = np.asarray([0.5, 0, 0, 0.5])
    unequal = np.asarray([0, 0.5, 0.5, 0])
    laws = [equal, equal, unequal]
    r = law_residual(bags, laws, edges)
    d = law_repair(bags, laws, feasible)
    assert constant == 1 and r == 0 and abs(d - 1) < 1e-8
    print("cycle: exact Cdet=1; law residual=0; numerical optimal repair=1")


if __name__ == "__main__":
    main()
