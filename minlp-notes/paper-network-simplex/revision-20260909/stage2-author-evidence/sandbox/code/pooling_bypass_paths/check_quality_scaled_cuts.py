"""Exact quality scaling and connected cuts versus original physical LPs."""
from fractions import Fraction as F
from itertools import product
from random import Random

from check_all_product_contracts import LP, compare, instances


def connected_sets(nodes, arcs):
    adj = {v: set() for v in nodes}
    for u, v in arcs:
        adj[u].add(v)
        adj[v].add(u)
    unseen = set(nodes)
    while unseen:
        start = next(iter(unseen))
        comp, stack = set(), [start]
        while stack:
            v = stack.pop()
            if v not in comp:
                comp.add(v)
                stack.extend(adj[v]-comp)
        unseen -= comp
        assert all(len(adj[v]) <= 2 for v in comp)
        endpoints = [v for v in comp if len(adj[v]) < 2]
        cyclic = not endpoints
        order, previous, current = [], None, endpoints[0] if endpoints else start
        while current not in order:
            order.append(current)
            choices = adj[current]-({previous} if previous is not None else set())
            if not choices:
                break
            previous, current = current, next(iter(choices))
        assert set(order) == comp
        if cyclic:
            for i in range(len(order)):
                for size in range(1, len(order)):
                    yield set(order[(i+j) % len(order)] for j in range(size))
            yield comp
        else:
            for i in range(len(order)):
                for j in range(i+1, len(order)+1):
                    yield set(order[i:j])


def cuts_hold(nodes, arcs, node_bounds, edge_bounds, subsets=None):
    if any(lo > hi for lo, hi in node_bounds.values()) or any(lo > hi for lo, hi in edge_bounds.values()):
        return False
    if subsets is None:
        subsets = connected_sets(nodes, arcs)
    for S in subsets:
        incoming = [e for e in arcs if e[0] not in S and e[1] in S]
        outgoing = [e for e in arcs if e[0] in S and e[1] not in S]
        lower_div = sum(node_bounds[v][0] for v in S)
        upper_div = sum(node_bounds[v][1] for v in S)
        attainable_upper = sum(edge_bounds[e][1] for e in outgoing)-sum(edge_bounds[e][0] for e in incoming)
        attainable_lower = sum(edge_bounds[e][0] for e in outgoing)-sum(edge_bounds[e][1] for e in incoming)
        if lower_div > attainable_upper or upper_div < attainable_lower:
            return False
    return True


def scaled_cut_decision(net, q):
    C, a, B, b, edges, feeds, outlets = net
    assert q not in C
    nodes = [('i', i) for i in range(len(C))] + [('o', j) for j in range(len(B))]
    arcs = [(('i', i), ('o', j)) for i, j in edges]
    gamma = [ci-q for ci in C]
    node_bounds = {}
    lower, upper = {}, {}
    for i in range(len(C)):
        endpoints = [gamma[i]*(a[i]-feeds.get(i, F(0))), gamma[i]*a[i]]
        node_bounds['i', i] = min(endpoints), max(endpoints)
    for i, j in edges:
        e = (('i', i), ('o', j))
        endpoints = [F(0), 2*gamma[i]]
        lower[e], upper[e] = [min(endpoints)], [max(endpoints)]
    for j in range(len(B)):
        R = b[j]*(B[j]-q)
        node_bounds['o', j] = -R, -R
        incoming = [i for i, jj in edges if jj == j]
        s_lo, s_hi = b[j]-outlets.get(j, F(0)), b[j]
        if len(incoming) == 2 and C[incoming[0]] != C[incoming[1]]:
            i, k = incoming
            endpoints = [gamma[i]*(R-gamma[k]*s)/(C[i]-C[k]) for s in (s_lo, s_hi)]
            e = (('i', i), ('o', j))
            lower[e].append(min(endpoints))
            upper[e].append(max(endpoints))
        elif len(incoming) == 2:
            endpoints = [gamma[incoming[0]]*s for s in (s_lo, s_hi)]
            if not min(endpoints) <= R <= max(endpoints):
                return False
        elif len(incoming) == 1:
            i = incoming[0]
            endpoints = [gamma[i]*s for s in (s_lo, s_hi)]
            e = (('i', i), ('o', j))
            lower[e].append(min(endpoints))
            upper[e].append(max(endpoints))
        elif not s_lo <= 0 <= s_hi:
            return False
    effective = {e: (max(lower[e]), min(upper[e])) for e in arcs}
    if any(lo > hi for lo, hi in effective.values()):
        return False
    # Check all-candidate cuts agree with effective max/min, using no branch partition.
    for S in connected_sets(nodes, arcs):
        cut = [(e, 1 if e[0] in S else -1) for e in arcs if (e[0] in S) != (e[1] in S)]
        assert len(cut) <= 2
        uppers = [sum(sign*value for (_, sign), value in zip(cut, values))
                  for values in product(*(upper[e] if sign == 1 else lower[e] for e, sign in cut))]
        lowers = [sum(sign*value for (_, sign), value in zip(cut, values))
                  for values in product(*(lower[e] if sign == 1 else upper[e] for e, sign in cut))]
        direct_upper = sum(effective[e][1] if sign == 1 else -effective[e][0] for e, sign in cut)
        direct_lower = sum(effective[e][0] if sign == 1 else -effective[e][1] for e, sign in cut)
        assert min(uppers) == direct_upper and max(lowers) == direct_lower
    return cuts_hold(nodes, arcs, node_bounds, effective)


def main():
    tested = feasible = singular = 0
    for net, known_q in instances():
        for q in sorted({known_q, *(F(j, 3) for j in range(13))}):
            physical, _ = compare(net, q)
            if q in net[0]:
                singular += 1  # The algorithm explicitly uses this rational LP branch.
                continue
            cut_answer = scaled_cut_decision(net, q)
            assert cut_answer == physical, (q, cut_answer, physical)
            tested += 1
            feasible += physical
    # Independently test signed node/edge intervals and connected-cut reduction.
    rng = Random(1102175)
    signed_checks = 0
    for n in range(2, 9):
        for case in range(12):
            nodes = list(range(n))
            pairs = [(i, i+1) for i in range(n-1)]
            if case % 2 and n > 2:
                pairs.append((n-1, 0))
            arcs = [pair if rng.randrange(2) else pair[::-1] for pair in pairs]
            edge_bounds = {e: tuple(sorted(F(rng.randrange(-8, 9), 2) for _ in range(2))) for e in arcs}
            node_bounds = {v: tuple(sorted(F(rng.randrange(-8, 9), 2) for _ in range(2))) for v in nodes}
            lp = LP(edge_bounds)
            for v in nodes:
                row = {e: F(1) if e[0] == v else F(-1) for e in arcs if v in e}
                lp.add(row, node_bounds[v][1])
                lp.add({e: -coef for e, coef in row.items()}, -node_bounds[v][0])
            connected = cuts_hold(nodes, arcs, node_bounds, edge_bounds)
            all_subsets = ({v for v, bit in zip(nodes, bits) if bit} for bits in product((0, 1), repeat=n))
            assert connected == cuts_hold(nodes, arcs, node_bounds, edge_bounds, all_subsets)
            assert connected == lp.feasible()
            signed_checks += 1
    print(f'PASS: {tested} exact transformed-cut versus original physical LP comparisons; {feasible} feasible.')
    print(f'PASS: {singular} singular-quality cases use the original rational LP branch.')
    print(f'PASS: {signed_checks} signed path/cycle systems, all-subset cuts, connected cuts, and LP feasibility agree.')
    print('Candidate-cut algebra is exact rational arithmetic; LP comparisons use numerical HiGHS.')


if __name__ == '__main__':
    main()
