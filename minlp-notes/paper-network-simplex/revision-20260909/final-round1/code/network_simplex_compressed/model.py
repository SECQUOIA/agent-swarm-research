"""Exact rational model assembly, followed by floating point HiGHS solves.

Incidence is incoming minus outgoing. Biconnected edge blocks and normalized
fundamental-cycle rows provide path compression without explicitly suppressing
degree-two vertices. No graph package or generator metadata is required.
"""

from collections import deque
from dataclasses import dataclass
from fractions import Fraction as F
from time import perf_counter

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix


def rational(value):
    return F(str(value)) if isinstance(value, (float, np.floating)) else F(value)


@dataclass
class Block:
    edges: tuple
    chords: tuple
    rows: tuple
    groups: tuple
    lower: tuple
    upper: tuple
    labels: tuple
    offsets: dict
    observations: dict

    @property
    def rank(self):
        return len(self.chords)


class CompressedNetworkSimplex:
    """Exact extended hull assembled in original x,y,z and sparse auxiliaries.

    ``arcs`` contains (tail, head, capacity), ``balances`` has one entry per
    vertex, and observations are (arc, explicit simplex state) pairs. Original
    variable order is x, y, then z in sorted observation order. Model rows and
    bounds are rational; optimization and membership are numerical, not exact
    certification. Input may contain parallel edges, loops, and isolated nodes.
    Structural infeasibility is represented by an inconsistent LP row.
    """

    def __init__(self, arcs, balances, simplex_size, observations, eliminate_observed=False):
        self.arcs = tuple((a, b, rational(u)) for a, b, u in arcs)
        self.balances = tuple(map(rational, balances))
        self.simplex_size = simplex_size
        if not isinstance(simplex_size, int) or simplex_size < 0:
            raise ValueError("simplex_size must be a nonnegative integer")
        n = len(self.balances)
        if any(not isinstance(a, (int, np.integer)) or not isinstance(b, (int, np.integer))
               or not (0 <= a < n and 0 <= b < n) for a, b, _ in self.arcs):
            raise ValueError("Arc endpoints must index balances")
        self.observations = tuple(sorted(set(observations)))
        if any(not isinstance(e, (int, np.integer)) or not isinstance(j, (int, np.integer))
               or not (0 <= e < len(self.arcs) and 0 <= j < simplex_size)
               for e, j in self.observations):
            raise ValueError("Observation index out of range")
        self.observed_by_edge = {}
        for e, j in self.observations:
            self.observed_by_edge.setdefault(e, []).append(j)
        self.original_n = len(self.arcs) + simplex_size + len(self.observations)
        self.n = self.original_n
        self.eq, self.ub = [], []
        self._preprocess()
        self._assemble()
        self.eliminated_variables = 0
        self.observed_ranks = {}
        if eliminate_observed:
            self._eliminate_observed()

    def _preprocess(self):
        """Iterative multigraph Tarjan and an unconstrained rational reference."""
        n, E = len(self.balances), len(self.arcs)
        adjacency = [[] for _ in range(n)]
        loops = []
        for e, (a, b, _) in enumerate(self.arcs):
            if a == b:
                loops.append([e])
            else:
                adjacency[a].append((b, e)); adjacency[b].append((a, e))
        discovery, low = [-1] * n, [0] * n
        subtree, reference = list(self.balances), [F(0)] * E
        components, edge_stack = [], []
        clock = 0
        self.structurally_empty = any(u < 0 for _, _, u in self.arcs)
        for root in range(n):
            if discovery[root] >= 0:
                continue
            discovery[root] = low[root] = clock; clock += 1
            stack = [[root, -1, -1, 0]]
            while stack:
                node, parent, parent_edge, cursor = stack[-1]
                if cursor < len(adjacency[node]):
                    neighbor, edge = adjacency[node][cursor]
                    stack[-1][3] += 1
                    if edge == parent_edge:
                        continue
                    if discovery[neighbor] < 0:
                        edge_stack.append(edge)
                        discovery[neighbor] = low[neighbor] = clock; clock += 1
                        stack.append([neighbor, node, edge, 0])
                    elif discovery[neighbor] < discovery[node]:
                        low[node] = min(low[node], discovery[neighbor])
                        edge_stack.append(edge)
                else:
                    stack.pop()
                    if parent >= 0:
                        subtree[parent] += subtree[node]
                        reference[parent_edge] = subtree[node] if self.arcs[parent_edge][1] == node else -subtree[node]
                        low[parent] = min(low[parent], low[node])
                        if low[node] >= discovery[parent]:
                            component = []
                            while True:
                                edge = edge_stack.pop(); component.append(edge)
                                if edge == parent_edge:
                                    break
                            components.append(component)
                    elif subtree[node]:
                        self.structurally_empty = True
        self.reference = tuple(reference)
        self.blocks, self.location = [], {}
        for edges in components + loops:
            if len(edges) == 1 and self.arcs[edges[0]][0] != self.arcs[edges[0]][1]:
                continue
            self._add_block(tuple(sorted(edges)))

    def _add_block(self, edges):
        adjacency = {}
        for e in edges:
            a, b, _ = self.arcs[e]
            adjacency.setdefault(a, []).append((b, e))
            adjacency.setdefault(b, []).append((a, e))
        root = min(adjacency)
        parent, depth, tree = {root: (None, None)}, {root: 0}, set()
        queue = deque([root])
        while queue:
            a = queue.popleft()
            for b, e in adjacency[a]:
                if b not in parent:
                    parent[b] = (a, e); depth[b] = depth[a] + 1
                    tree.add(e); queue.append(b)
        chords = tuple(e for e in edges if e not in tree)
        edge_rows = {e: {} for e in edges}
        for h, e in enumerate(chords):
            tail, head, _ = self.arcs[e]
            edge_rows[e][h] = 1
            # The chord goes tail -> head; its tree return goes head -> tail.
            a, b = head, tail
            while a != b:
                if depth[a] >= depth[b]:
                    up, f = parent[a]
                    edge_rows[f][h] = 1 if self.arcs[f][:2] == (a, up) else -1
                    a = up
                else:
                    up, f = parent[b]
                    edge_rows[f][h] = 1 if self.arcs[f][:2] == (up, b) else -1
                    b = up
        grouped = {}
        for e, values in edge_rows.items():
            if not values:
                raise AssertionError("A cyclic block contains a zero cycle row")
            sign = values[min(values)]
            row = tuple((h, sign * c) for h, c in sorted(values.items()))
            grouped.setdefault(row, []).append((e, sign))
        rows, groups = tuple(grouped), tuple(tuple(v) for v in grouped.values())
        lower, upper = [], []
        for group in groups:
            intervals = [(-self.reference[e], self.arcs[e][2] - self.reference[e]) if s == 1
                         else (self.reference[e] - self.arcs[e][2], self.reference[e]) for e, s in group]
            lower.append(max(a for a, _ in intervals)); upper.append(min(b for _, b in intervals))
        observations = {}
        for e in edges:
            for j in self.observed_by_edge.get(e, ()):
                observations.setdefault(j, []).append((e, j))
        labels = tuple(sorted(observations))
        offsets = {j: self.n + i * len(chords) for i, j in enumerate(labels)}
        self.n += len(chords) * len(labels)
        block = Block(edges, chords, rows, groups, tuple(lower), tuple(upper), labels, offsets, observations)
        index = len(self.blocks); self.blocks.append(block)
        for p, group in enumerate(groups):
            for e, sign in group:
                self.location[e] = (index, p, sign)

    @staticmethod
    def _add(rows, terms, rhs):
        coefficients = {}
        for column, value in terms:
            coefficients[column] = coefficients.get(column, F(0)) + rational(value)
        rows.append(({k: v for k, v in coefficients.items() if v}, rational(rhs)))

    def _assemble(self):
        E, m = len(self.arcs), self.simplex_size
        balances = [[] for _ in self.balances]
        for e, (a, b, _) in enumerate(self.arcs):
            if a != b:
                balances[a].append((e, -1)); balances[b].append((e, 1))
        for terms, rhs in zip(balances, self.balances):
            self._add(self.eq, terms, rhs)
        if self.structurally_empty:
            self._add(self.eq, [], 1)
        self._add(self.ub, [(E+j, 1) for j in range(m)], 1)
        for block in self.blocks:
            if not block.labels:
                continue
            for p, row in enumerate(block.rows):
                lower, upper = block.lower[p], block.upper[p]
                for j in block.labels:
                    terms = [(block.offsets[j]+h, c) for h, c in row]
                    self._add(self.ub, terms + [(E+j, -upper)], 0)
                    self._add(self.ub, [(k, -v) for k, v in terms] + [(E+j, lower)], 0)
                e, sign = block.groups[p][0]
                terms = [(e, sign)] + [(block.offsets[j]+h, -c) for j in block.labels for h, c in row]
                self._add(self.ub, terms + [(E+j, upper) for j in block.labels], upper + sign*self.reference[e])
                self._add(self.ub, [(k, -v) for k, v in terms] + [(E+j, -lower) for j in block.labels], -lower - sign*self.reference[e])
        self.observation_equations = {}
        for k, (e, j) in enumerate(self.observations):
            terms = [(E+m+k, 1), (E+j, -self.reference[e])]
            if e in self.location:
                b, p, sign = self.location[e]; block = self.blocks[b]
                terms.extend((block.offsets[j]+h, -sign*c) for h, c in block.rows[p])
            self.observation_equations[e, j] = len(self.eq)
            self._add(self.eq, terms, 0)
        self.bounds = [(F(0), max(F(0), u)) for _, _, u in self.arcs] + [(F(0), F(1))]*m
        self.bounds += [(None, None)] * (self.n - E - m)

    def _eliminate_observed(self):
        """Eliminate independent observed coordinates by exact blockwise pivots.

        Each eliminated coordinate is free before substitution. For state j in
        block B, r_B-d_Bj coordinates remain, where d_Bj is the rank of observed
        fundamental-cycle rows. This equals the cycle rank of the unobserved
        subgraph. Block offsets describe the pre-elimination cycle coordinates;
        final LP coordinates are available through retained_variable_map.
        """
        substitutions = {}

        def substitute(terms, rhs, expressions):
            result = dict(terms)
            for pivot in tuple(k for k in result if k in expressions):
                scale = result.pop(pivot)
                expression, constant = expressions[pivot]
                rhs -= scale*constant
                for k, a in expression.items():
                    result[k] = result.get(k, F(0)) + scale*a
                    if not result[k]:
                        del result[k]
            return result, rhs

        for index, block in enumerate(self.blocks):
            for state in block.labels:
                local = {}
                observed = block.observations[state]
                for key in observed:
                    terms, rhs = self.eq[self.observation_equations[key]]
                    terms, rhs = substitute(terms, rhs, local)
                    candidates = [k for k in terms if k >= self.original_n]
                    if not candidates:
                        continue
                    pivot = min(candidates); scale = terms.pop(pivot)
                    expression = {k: -a/scale for k, a in terms.items()}
                    constant = rhs/scale
                    # Keep previously chosen pivot expressions fully reduced.
                    for old, (old_terms, old_constant) in tuple(local.items()):
                        reduced, negative_constant = substitute(old_terms, -old_constant, {pivot: (expression, constant)})
                        local[old] = (reduced, -negative_constant)
                    local[pivot] = (expression, constant)
                self.observed_ranks[index, state] = len(local)
                substitutions.update(local)
        retained = [k for k in range(self.n) if k not in substitutions]
        self.retained_variable_map = {old: new for new, old in enumerate(retained)}
        def reduce_rows(rows):
            result = []
            for terms, rhs in rows:
                terms, rhs = substitute(terms, rhs, substitutions)
                if terms or rhs:
                    result.append(({self.retained_variable_map[k]: a for k, a in terms.items()}, rhs))
            return result
        self.eq, self.ub = reduce_rows(self.eq), reduce_rows(self.ub)
        self.bounds = [self.bounds[k] for k in retained]
        self.eliminated_variables = len(substitutions)
        self.n = len(retained)

    def matrices(self):
        """Convert the retained rational rows to SciPy CSR floating matrices."""
        def convert(rows):
            ii, jj, vv, rhs = [], [], [], []
            for i, (terms, b) in enumerate(rows):
                for j, a in terms.items():
                    ii.append(i); jj.append(j); vv.append(float(a))
                rhs.append(float(b))
            return coo_matrix((vv, (ii, jj)), shape=(len(rows), self.n)).tocsr(), np.asarray(rhs)
        ae, be = convert(self.eq); au, bu = convert(self.ub)
        return ae, be, au, bu

    def optimize(self, objective, y_fixed=None, point=None):
        """Numerically minimize a linear objective, optionally fixing y or x,y,z."""
        assembly_start = perf_counter()
        if len(objective) != self.original_n:
            raise ValueError("Objective dimension must match x,y,z")
        bounds = list(self.bounds)
        E, m = len(self.arcs), self.simplex_size
        if y_fixed is not None:
            if len(y_fixed) != m:
                raise ValueError("Wrong y dimension")
            if any(not 0 <= rational(v) <= 1 for v in y_fixed):
                raise ValueError("Fixed simplex weights must lie in [0,1]")
            bounds[E:E+m] = [(rational(v), rational(v)) for v in y_fixed]
        if point is not None:
            if len(point.x) != E or len(point.y) != m or set(point.z) != set(self.observations):
                raise ValueError("Point dimensions or observation keys do not match")
            values = tuple(point.x) + tuple(point.y) + tuple(point.z[key] for key in self.observations)
            # Fixing a coordinate must preserve original domain bounds.
            if any((lo is not None and rational(v) < lo) or (hi is not None and rational(v) > hi)
                   for v, (lo, hi) in zip(values, bounds)):
                from scipy.optimize import OptimizeResult
                return OptimizeResult(success=False, status=2, message="Point violates an original variable bound")
            bounds[:self.original_n] = [(rational(v), rational(v)) for v in values]
        ae, be, au, bu = self.matrices()
        c = np.r_[np.asarray(objective, dtype=float), np.zeros(self.n-self.original_n)]
        numeric_bounds = [(None if a is None else float(a), None if b is None else float(b)) for a, b in bounds]
        assembly_seconds = perf_counter() - assembly_start
        solve_start = perf_counter()
        # scipy.linprog requires at least one column, even for the empty model.
        if self.n == 0:
            from scipy.optimize import OptimizeResult
            feasible = all(b == 0 for _, b in self.eq) and all(b >= 0 for _, b in self.ub)
            result = OptimizeResult(success=feasible, status=0 if feasible else 2,
                                    message="Empty model", x=np.array([]), fun=0. if feasible else None)
        else:
            result = linprog(c, A_eq=ae, b_eq=be, A_ub=au, b_ub=bu, bounds=numeric_bounds, method="highs")
        result.assembly_seconds = assembly_seconds
        result.solve_seconds = perf_counter() - solve_start
        if result.success:
            result.original_point = result.x[:self.original_n]
        result.model_stats = dict(variables=self.n, auxiliary_variables=self.n-self.original_n,
                                 rows=ae.shape[0]+au.shape[0], nonzeros=ae.nnz+au.nnz,
                                 matrix_bytes=sum(a.data.nbytes+a.indices.nbytes+a.indptr.nbytes for a in (ae, au)))
        return result

    def membership(self, point):
        """Floating point LP hull-membership check; no exact certificate."""
        return self.optimize(np.zeros(self.original_n), point=point)
