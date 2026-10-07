"""Exact finite min-sum computations on a supplied tree decomposition.

Costs are integers or Fractions; None denotes an infeasible assignment.
Every original factor must be assigned exactly once in the input bag tables.
This module optimizes those tables. It does not prove how they bound a
continuous problem; that obligation belongs to each caller and its checker.
"""

from dataclasses import dataclass
from fractions import Fraction
from math import prod


@dataclass(frozen=True)
class TreeLayout:
    bags: tuple
    edges: tuple
    n: int
    neighbors: tuple
    parents: tuple
    order: tuple
    home: tuple
    positions: tuple
    separators: dict
    projections: dict


def prepare_tree(bags, edges, n):
    """Validate a decomposition and prepare reusable index projections."""
    if type(n) is not int or n < 0:
        raise ValueError("invalid coordinate count")
    bags = tuple(tuple(bag) for bag in bags)
    edges = tuple(tuple(edge) for edge in edges)
    if not bags or len(edges) != len(bags) - 1:
        raise ValueError("decomposition must have a nonempty tree of bags")
    occurrences = [[] for _ in range(n)]
    for u, bag in enumerate(bags):
        if len(set(bag)) != len(bag) or any(
                type(i) is not int or not 0 <= i < n for i in bag):
            raise ValueError("invalid bag coordinate")
        for i in bag:
            occurrences[i].append(u)
    neighbors = [[] for _ in bags]
    seen = set()
    for edge in edges:
        if len(edge) != 2 or any(type(u) is not int or not 0 <= u < len(bags)
                                for u in edge):
            raise ValueError("invalid decomposition edge")
        u, v = edge
        canonical = tuple(sorted(edge))
        if u == v or canonical in seen:
            raise ValueError("decomposition edges must form a simple tree")
        seen.add(canonical)
        neighbors[u].append(v)
        neighbors[v].append(u)
    parents, order = [-2] * len(bags), [0]
    parents[0] = -1
    for u in order:
        for v in neighbors[u]:
            if parents[v] == -2:
                parents[v] = u
                order.append(v)
    if len(order) != len(bags):
        raise ValueError("decomposition tree is disconnected")
    positions = tuple({i: j for j, i in enumerate(bag)} for bag in bags)
    separators, projections = {}, {}
    occurrence_edges = [0] * n
    for u, v in edges:
        separator = tuple(sorted(set(bags[u]) & set(bags[v])))
        for i in separator:
            occurrence_edges[i] += 1
        for a, b in ((u, v), (v, u)):
            separators[a, b] = separator
            projections[a, b] = tuple(positions[a][i] for i in separator)
    for i in range(n):
        # An induced subgraph of a tree is connected iff it has |V|-1 edges.
        if not occurrences[i] or occurrence_edges[i] != len(occurrences[i]) - 1:
            raise ValueError("missing coordinate or failed running intersection")
    return TreeLayout(bags, edges, n, tuple(map(tuple, neighbors)),
                      tuple(parents), tuple(order),
                      tuple(row[0] for row in occurrences), positions,
                      separators, projections)


def solve_tree(bags, edges, domain_sizes, local_tables, *, home=None,
               check=None, layout=None):
    """Return global minimum, traceback, all unary margins, and messages.

    Each local table is a full dict from bag index tuples to a finite exact
    cost or None. Infeasible states remain explicit in outgoing messages.
    A reusable layout avoids repeating structural validation between stages.
    The optional check() is called during table validation and message work.
    """
    sizes = tuple(domain_sizes)
    if any(type(k) is not int or k < 1 for k in sizes):
        raise ValueError("coordinate domains must have positive integer sizes")
    bags = tuple(tuple(bag) for bag in bags)
    edges = tuple(tuple(edge) for edge in edges)
    if layout is None:
        layout = prepare_tree(bags, edges, len(sizes))
    elif not isinstance(layout, TreeLayout) or (
            layout.bags, layout.edges, layout.n) != (bags, edges, len(sizes)):
        raise ValueError("layout does not match the supplied decomposition")
    home = layout.home if home is None else tuple(home)
    if len(home) != len(sizes) or any(type(u) is not int or
            not 0 <= u < len(bags) or i not in bags[u] for i, u in enumerate(home)):
        raise ValueError("invalid coordinate home")
    if len(local_tables) != len(bags):
        raise ValueError("one local table is required per bag")
    check = (lambda: None) if check is None else check
    table_states = 0
    for bag, table in zip(bags, local_tables):
        expected = prod(sizes[i] for i in bag)
        if len(table) != expected:
            raise ValueError("local table does not cover its complete domain")
        table_states += expected
        for state, cost in table.items():
            check()
            if not isinstance(state, tuple) or len(state) != len(bag) or any(
                    type(k) is not int or not 0 <= k < sizes[i]
                    for i, k in zip(bag, state)):
                raise ValueError("invalid local table state")
            if cost is not None and (isinstance(cost, bool) or
                                     not isinstance(cost, (int, Fraction))):
                raise ValueError("local costs must use exact rational arithmetic")

    def key(state, u, v):
        return tuple(state[k] for k in layout.projections[u, v])

    messages, witnesses = {}, {}

    def reduce_message(u, v, values, keep_witness):
        message, witness = {}, {}
        for state, cost in values:
            check()
            separator = key(state, u, v)
            previous = message.get(separator)
            if separator not in message or (cost is not None and
                                            (previous is None or cost < previous)):
                message[separator] = cost
                if keep_witness and cost is not None:
                    witness[separator] = state
        messages[u, v] = message
        if keep_witness:
            witnesses[u, v] = witness

    def upward_values(u, parent):
        for state, local in local_tables[u].items():
            check()
            if local is None:
                yield state, None
                continue
            total = Fraction(local)
            for v in layout.neighbors[u]:
                if v == parent:
                    continue
                incoming = messages[v, u][key(state, u, v)]
                if incoming is None:
                    total = None
                    break
                total += incoming
            yield state, total

    for u in reversed(layout.order[1:]):
        parent = layout.parents[u]
        reduce_message(u, parent, upward_values(u, parent), True)

    marginals = [[None] * k for k in sizes]
    owned = [[] for _ in bags]
    for i, u in enumerate(home):
        owned[u].append(i)
    lower, root_state = None, None
    for u in layout.order:
        # Sum each incoming message once. Excluding a child then takes one
        # subtraction and one infeasibility-count update, including at stars.
        totals = {}
        for state, local in local_tables[u].items():
            check()
            total = Fraction(0) if local is None else Fraction(local)
            invalid = int(local is None)
            for v in layout.neighbors[u]:
                incoming = messages[v, u][key(state, u, v)]
                if incoming is None:
                    invalid += 1
                else:
                    total += incoming
            totals[state] = (total, invalid)
            if invalid:
                continue
            if u == 0 and (lower is None or total < lower):
                lower, root_state = total, state
            for i in owned[u]:
                index = state[layout.positions[u][i]]
                previous = marginals[i][index]
                if previous is None or total < previous:
                    marginals[i][index] = total

        def excluding(v):
            for state, (total, invalid) in totals.items():
                incoming = messages[v, u][key(state, u, v)]
                remaining = invalid - int(incoming is None)
                yield state, (None if remaining else
                              total - (Fraction(0) if incoming is None else incoming))

        for v in layout.neighbors[u]:
            if layout.parents[v] == u:
                reduce_message(u, v, excluding(v), False)

    point_indices = None
    if lower is not None:
        selected, indices = {0: root_state}, [None] * len(sizes)
        for u in layout.order:
            state = selected.pop(u)
            for i, index in zip(bags[u], state):
                if indices[i] is not None and indices[i] != index:
                    raise ArithmeticError("inconsistent traceback")
                indices[i] = index
            for v in layout.neighbors[u]:
                if layout.parents[v] == u:
                    selected[v] = witnesses[v, u][key(state, u, v)]
        point_indices = tuple(indices)
    return {"lower": lower, "point_indices": point_indices,
            "marginals": tuple(map(tuple, marginals)), "messages": messages,
            "table_states": table_states}
