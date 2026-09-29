"""Exact finite checks of maximal-coupling tree repair; no CI checks."""

from collections import defaultdict, deque
from fractions import Fraction as Q
from itertools import product
import random


def projection(bag, state, separator):
    return tuple(state[bag.index(i)] for i in separator)


def marginal(bag, law, separator):
    result = defaultdict(Q)
    for state, probability in law.items():
        result[projection(bag, state, separator)] += probability
    return dict(result)


def tv(first, second):
    return sum(abs(first.get(x, Q()) - second.get(x, Q()))
               for x in first.keys() | second.keys()) / 2


def edge_coupling(bp, lp, bc, lc):
    sep = tuple(sorted(set(bp) & set(bc)))
    ap, ac = marginal(bp, lp, sep), marginal(bc, lc, sep)
    states = ap.keys() | ac.keys()
    common = {s: min(ap.get(s, Q()), ac.get(s, Q())) for s in states}
    epsilon = tv(ap, ac)
    sep_joint = {(s, s): probability for s, probability in common.items()
                 if probability}
    if epsilon:
        for s, t in product(states, repeat=2):
            probability = ((ap.get(s, Q()) - common[s])
                           * (ac.get(t, Q()) - common[t]) / epsilon)
            if probability:
                sep_joint[s, t] = sep_joint.get((s, t), Q()) + probability
    joint = {}
    for sp, sc in product(lp, lc):
        p, c = projection(bp, sp, sep), projection(bc, sc, sep)
        probability = sep_joint.get((p, c), Q()) * lp[sp] * lc[sc] / ap[p] / ac[c]
        if probability:
            joint[sp, sc] = probability
    assert tv({sp: sum(v for (p, _), v in joint.items() if p == sp)
               for sp in lp}, lp) == 0
    assert tv({sc: sum(v for (_, c), v in joint.items() if c == sc)
               for sc in lc}, lc) == 0
    assert sum(v for (p, c), v in joint.items()
               if projection(bp, p, sep) != projection(bc, c, sep)) == epsilon
    return joint, epsilon, sep


def check_case(bags, edges, laws, weights, root):
    adjacency = [[] for _ in bags]
    for a, b in edges:
        adjacency[a].append(b)
        adjacency[b].append(a)
    parent, order = {root: None}, []
    queue = deque([root])
    while queue:
        p = queue.popleft()
        order.append(p)
        for child in adjacency[p]:
            if child not in parent:
                parent[child] = p
                queue.append(child)
    probabilities = {tuple((s if b == root else None) for b in range(len(bags))): p
                     for s, p in laws[root].items()}
    epsilon, separators = {}, {}
    for child in order[1:]:
        p = parent[child]
        pair, epsilon[child], separators[child] = edge_coupling(
            bags[p], laws[p], bags[child], laws[child])
        updated = defaultdict(Q)
        for states, mass in probabilities.items():
            for sc in laws[child]:
                factor = pair.get((states[p], sc), Q()) / laws[p][states[p]]
                if factor:
                    new = list(states)
                    new[child] = sc
                    updated[tuple(new)] += mass * factor
        probabilities = dict(updated)
    variables = sorted(set().union(*map(set, bags)))
    anchors = {i: next(b for b in order if i in bags[b]) for i in variables}
    repaired = defaultdict(Q)
    for states, probability in probabilities.items():
        repaired[tuple(states[anchors[i]][bags[anchors[i]].index(i)]
                       for i in variables)] += probability
    assert sum(repaired.values()) == 1
    refined_cost, actual_cost, path_cost = Q(), Q(), Q()
    for b, bag in enumerate(bags):
        delta = tv(marginal(tuple(variables), repaired, bag), laws[b])
        path, node = [], b
        while parent[node] is not None:
            path.append(node)
            node = parent[node]
        bound = sum(epsilon[c] for c in path)
        refined = sum(epsilon[c] for c in path if set(separators[c]) & set(bag))
        assert delta <= min(1, refined) <= min(1, bound)
        actual_cost += weights[b] * delta
        refined_cost += weights[b] * refined
        path_cost += weights[b] * bound
    return actual_cost, refined_cost, path_cost


def main():
    rng = random.Random(290928)
    templates = [([(0, 1), (1, 2), (2, 3)], [(0, 1), (1, 2)]),
                 ([(0, 1), (0, 2), (0, 3)], [(0, 1), (1, 2)]),
                 ([(0, 1), (0, 2), (1, 3), (0, 4)], [(0, 1), (0, 2), (1, 3)])]
    count = 0
    for bags, edges in templates:
        for _ in range(8):
            laws = []
            for bag in bags:
                counts = {state: rng.randint(1, 9) for state in product((0, 1), repeat=len(bag))}
                denominator = sum(counts.values())
                laws.append({s: Q(c, denominator) for s, c in counts.items()})
            weights = [Q(rng.randint(0, 5)) for _ in bags]
            costs = [check_case(bags, edges, laws, weights, root) for root in range(len(bags))]
            cut_bound = Q()
            for a, b in edges:
                component = {a}
                changed = True
                while changed:
                    changed = False
                    for c, d in edges:
                        if {c, d} == {a, b}:
                            continue
                        if c in component and d not in component:
                            component.add(d)
                            changed = True
                        if d in component and c not in component:
                            component.add(c)
                            changed = True
                wa = sum(weights[c] for c in component)
                wb = sum(weights) - wa
                _, mismatch, _ = edge_coupling(bags[a], laws[a], bags[b], laws[b])
                cut_bound += mismatch * min(wa, wb)
            assert min(path for _, _, path in costs) == cut_bound
            assert min(actual for actual, _, _ in costs) <= cut_bound
            count += len(bags)
    for k in range(1, 7):
        n, epsilon = 2 * k, Q(1, 2 * k)
        local_objective = sum((1 if j < k else -1) * j * epsilon for j in range(n))
        cut_bound = sum(min(j, n - j) * epsilon for j in range(1, n))
        assert -local_objective == cut_bound == k * k * epsilon
    print(f"PASS: {count} exact rooted coupling checks; weighted-cut identity; six sharp objective examples")


if __name__ == "__main__":
    main()
