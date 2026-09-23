#!/usr/bin/env python3
"""A3 regression checks, using only the standard library.

Fraction tests cover suppression, physical smoothed states and their exact
adjoints, threshold faces, and zonotope membership against an independent
box-LP vertex enumeration. The support test uses every facet normal in the
actual span, plus exact affine-span membership; sampled directions would
not suffice. Decimal finite differences and small exhaustive grids provide
numerical regression evidence, not a certified QE implementation. Corner
search is used only on the explicitly monotone tiny parallel-path family.
"""

from decimal import Decimal, localcontext
from fractions import Fraction as F
from itertools import combinations, product
import random
import sys

import check_a1_preliminaries as a1

CHECKS = 0
STATS = {}


def check(condition, message):
    global CHECKS
    CHECKS += 1
    if not condition:
        raise AssertionError(message)


def count(name, amount=1):
    STATS[name] = STATS.get(name, 0) + amount


def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), F(0))


def linear_solve(matrix, rhs, columns=None):
    """Exact/Decimal rectangular solve; return None unless unique and consistent."""
    width = len(matrix[0]) if matrix else (columns or 0)
    rows = [list(row) + [value] for row, value in zip(matrix, rhs)]
    pivots = []
    for col in range(width):
        pivot = next((i for i in range(len(pivots), len(rows))
                      if rows[i][col] != 0), None)
        if pivot is None:
            continue
        row = len(pivots)
        rows[row], rows[pivot] = rows[pivot], rows[row]
        divisor = rows[row][col]
        rows[row] = [x/divisor for x in rows[row]]
        for i in range(len(rows)):
            if i != row:
                factor = rows[i][col]
                rows[i] = [x-factor*y for x, y in zip(rows[i], rows[row])]
        pivots.append(col)
    if any(all(x == 0 for x in row[:width]) and row[-1] != 0 for row in rows):
        return None
    if len(pivots) != width:
        return None
    answer = [rhs[0]*0 if rhs else F(0)] * width
    for i, col in enumerate(pivots):
        answer[col] = rows[i][-1]
    return answer


def determinant(matrix):
    if not matrix:
        return F(1)
    return sum(((-1)**i * matrix[0][i] * determinant(
        [row[:i] + row[i+1:] for row in matrix[1:]])
        for i in range(len(matrix))), F(0))


def adjoint(n, edges, resistances, rhs, ground):
    zero = resistances[0]*0
    lap = [[zero for _ in range(n)] for _ in range(n)]
    for (u, v, _), resistance in zip(edges, resistances):
        weight = 1/resistance
        lap[u][u] += weight
        lap[v][v] += weight
        lap[u][v] -= weight
        lap[v][u] -= weight
    keep = [v for v in range(n) if v != ground]
    solution = linear_solve([[lap[u][v] for v in keep] for u in keep],
                            [rhs[u] for u in keep])
    check(solution is not None, 'singular grounded Laplacian')
    h = [zero for _ in range(n)]
    for v, value in zip(keep, solution):
        h[v] = value
    return h


def subdivided(kind, rng):
    skeleton = [(0, 1)]*3 if kind == 'theta' else list(combinations(range(4), 2))
    n = 2 if kind == 'theta' else 4
    edges = []
    for u, v in skeleton:
        added = rng.randrange(1, 4)
        vertices = [u] + list(range(n, n+added)) + [v]
        n += added
        edges.extend((s, t, F(rng.randrange(1, 8), rng.randrange(1, 5)))
                     for s, t in zip(vertices, vertices[1:]))
    return n, edges


def core_paths(n, edges, a, c):
    adjacency = a1.adjacency(n, edges)
    core = {a, c} | {v for v in range(n) if len(adjacency[v]) >= 3}
    seen, paths = set(), []
    for start in sorted(core):
        for neighbor, edge, sign in adjacency[start]:
            if edge in seen:
                continue
            vertices, arc_ids, signs = [start, neighbor], [edge], [sign]
            seen.add(edge)
            while vertices[-1] not in core:
                candidates = [(v, e, s) for v, e, s in adjacency[vertices[-1]]
                              if e != arc_ids[-1]]
                check(len(candidates) == 1, 'path internal degree is not two')
                v, e, s = candidates[0]
                check(e not in seen, 'closed unmarked cycle')
                vertices.append(v)
                arc_ids.append(e)
                signs.append(s)
                seen.add(e)
            paths.append((vertices, arc_ids, signs))
    check(seen == set(range(len(edges))), 'suppression missed edges')
    interiors = [v for vertices, _, _ in paths for v in vertices[1:-1]]
    check(sorted(interiors) == sorted(set(range(n))-core), 'interiors not a partition')
    return core, paths


def patterns(size):
    return {tuple('F' if 2*i+1 in (left, right) else
                  'U' if left < 2*i+1 < right else 'L'
                  for i in range(size))
            for left in range(2*size+1) for right in range(left, 2*size+1)}


def check_path_levels(values):
    ordered = sorted(set(values))
    levels = ordered + [(a+b)/2 for a, b in zip(ordered, ordered[1:])]
    if ordered:
        levels += [ordered[0]-1, ordered[-1]+1]
    else:
        levels = [F(0)]
    allowed = patterns(len(values))
    for level in levels:
        status = tuple('F' if x == level else 'U' if x > level else 'L' for x in values)
        check(status.count('F') <= 2, 'more than two level vertices')
        upper = [i for i, x in enumerate(values) if x > level]
        check(not upper or upper == list(range(upper[0], upper[-1]+1)),
              'upper-level set is not an interval')
        check(status in allowed, 'threshold missing from face enumeration')
        count('threshold patterns')


def topology_and_adjoint(rng):
    for trial in range(24):
        n, topology = subdivided('theta' if trial % 2 == 0 else 'k4', rng)
        check(len(a1.blocks(n, topology)) == 1, 'generated graph is not one block')
        a, c = (0, 1) if trial % 3 == 0 else (n-1, n-3)
        core, paths = core_paths(n, topology, a, c)
        rank = len(topology)-n+1
        check(rank in (2, 3), 'unexpected block rank')
        check(len(core) <= 2*rank, 'marked vertex bound')
        check(len(paths) == rank+len(core)-1 <= 3*rank-1, 'path bound')
        check(len(core)+2*len(paths) <= 8*rank-2, 'free nomination bound')
        # Construct an exact rational smoothed physical state. Random flows
        # have the signs of rational potential drops; solve for positive beta.
        potential = list(map(F, rng.sample(range(3*n), n)))
        rho, delta = F(1, 3), F(2, 7)
        edges, nomination, resistances = [], [F(0)]*n, []
        for u, v, _ in topology:
            drop = potential[u]-potential[v]
            x = F(rng.randrange(1, 6), rng.randrange(1, 5)) * (1 if drop > 0 else -1)
            beta = drop/(x*abs(x)+rho*x)
            check(beta > 0, 'nonpositive constructed resistance')
            edges.append((u, v, beta))
            nomination[u] += x
            nomination[v] -= x
            resistances.append(beta*(2*abs(x)+rho))
            check(beta*(x*abs(x)+rho*x) == drop, 'smoothed physical law')
        check(sum(nomination) == 0, 'constructed balance')
        rhs = [delta if v not in core else F(0) for v in range(n)]
        rhs[a] += 1
        rhs[c] -= 1+delta*(n-len(core))
        h = adjoint(n, edges, resistances, rhs, c)
        divergence = [F(0)]*n
        for (u, v, _), resistance in zip(edges, resistances):
            current = (h[u]-h[v])/resistance
            divergence[u] += current
            divergence[v] -= current
        check(divergence == rhs, 'exact perturbed adjoint residual')
        for vertices, arc_ids, _ in paths:
            current = [(h[u]-h[v])/resistances[e]
                       for u, v, e in zip(vertices, vertices[1:], arc_ids)]
            check(all(y-x == delta for x, y in zip(current, current[1:])),
                  'positive-source increment identity')
            check(sum(j == 0 for j in current) <= 1, 'long plateau')
            signs = [(j > 0)-(j < 0) for j in current]
            check(signs == sorted(signs), 'adjoint phases reversed')
            check_path_levels([h[v] for v in vertices[1:-1]])
            count('suppressed paths')
        unit = [F(0)]*n
        unit[a], unit[c] = F(1), F(-1)
        ordinary = adjoint(n, edges, resistances, unit, c)
        check(all(ordinary[c] < ordinary[v] < ordinary[a]
                  for v in range(n) if v not in (a, c)), 'strict block ordering')
        check(all(abs((ordinary[u]-ordinary[v])/r) <= 1
                  for (u, v, _), r in zip(edges, resistances)), 'unit current bound')
        count('exact smoothed blocks')
    # Exact two-vertex plateau in an actual cycle adjoint, including zero flows.
    edges = [(i, i+1, F(1)) for i in range(5)] + [(0, 5, F(5, 2))]
    zero_x, zero_pi = a1.solve(6, edges, [F(0)]*6)
    check(not any(zero_x) and not any(zero_pi), 'zero-flow plateau base state')
    rhs = [F(1), F(1), F(1), F(1), F(1), F(-5)]
    h = adjoint(6, edges, [F(1)]*5 + [F(5, 2)], rhs, 5)
    check(h == list(map(F, [5, 6, 6, 5, 3, 0])),
          'explicit plateau missing')
    check_path_levels(h[1:5])
    # Equal endpoint values and a maximum plateau, with internal forcing one.
    values = list(map(F, [0, 2, 3, 3, 2, 0]))
    currents = [x-y for x, y in zip(values, values[1:])]
    check(all(y-x == 1 for x, y in zip(currents, currents[1:])), 'plateau increments')
    check_path_levels(values[1:-1])


def independent_columns(columns):
    basis = []
    for col in columns:
        if not any(col):
            continue
        matrix = [list(row) for row in zip(*basis)] if basis else [[] for _ in col]
        if linear_solve(matrix, col, len(basis)) is None:
            basis.append(col)
    return basis


def support_membership(columns, lower, upper, target):
    """All zonotope facets in its exact affine span, not sampled directions."""
    offset = [sum((lo*col[i] for lo, col in zip(lower, columns)), F(0))
              for i in range(len(target))]
    generators = [[(hi-lo)*x for x in col] for col, lo, hi in zip(columns, lower, upper)]
    basis = independent_columns(generators)
    rank = len(basis)
    residual = [x-y for x, y in zip(target, offset)]
    if rank == 0:
        return not any(residual)
    matrix = list(map(list, zip(*basis)))
    point = linear_solve(matrix, residual)
    if point is None:
        return False
    generators = [linear_solve(matrix, col) for col in generators]
    check(all(col is not None for col in generators), 'span coordinates failed')
    # In rank dimensions, every facet is parallel to rank-1 independent
    # generators. All their signed cofactor normals therefore suffice.
    for subset in combinations(generators, rank-1):
        rows = [list(row) for row in subset]
        normal = [(-1)**i * determinant([row[:i]+row[i+1:] for row in rows])
                  for i in range(rank)]
        if not any(normal):
            continue
        for sign in (-1, 1):
            direction = [sign*x for x in normal]
            support = sum((max(F(0), dot(direction, col)) for col in generators), F(0))
            if dot(direction, point) > support:
                return False
    return True


def box_lp_vertices(columns, lower, upper, target):
    """Independent tiny-instance LP oracle; exponential bound assignments allowed.

    Membership includes the objective row, so free supports can have size k+1,
    not merely k. Lower-dimensional and zero-rank systems are included.
    """
    m, dimension = len(columns), len(target)
    for size in range(min(m, dimension)+1):
        for free in combinations(range(m), size):
            bound = [i for i in range(m) if i not in free]
            for endpoints in product(*[(lower[i], upper[i]) for i in bound]):
                candidate = [F(0)]*m
                for i, value in zip(bound, endpoints):
                    candidate[i] = value
                rhs = [target[row]-sum((columns[i][row]*candidate[i] for i in bound), F(0))
                       for row in range(dimension)]
                matrix = [[columns[i][row] for i in free] for row in range(dimension)]
                solution = linear_solve(matrix, rhs, size)
                if solution is None:
                    continue
                for i, value in zip(free, solution):
                    candidate[i] = value
                if all(lo <= value <= hi for lo, value, hi in zip(lower, candidate, upper)):
                    return candidate
    return None


def support_value_membership(columns, lower, upper, linking_target, value, offset):
    """Apply the lemma's augmented value row, including its core-only offset."""
    return support_membership(columns, lower, upper, linking_target + [value-offset])


def strict_cone_feasible(rows, dimension):
    """Exact Fourier--Motzkin feasibility for rows * eta > 0.

    A finite homogeneous strict system is feasible iff it can be scaled to
    rows * eta >= 1. No bound on eta or sampled directions is used.
    """
    inequalities = [(list(row), F(1)) for row in rows]
    for _ in range(dimension):
        positive = [(a, b) for a, b in inequalities if a[-1] > 0]
        negative = [(a, b) for a, b in inequalities if a[-1] < 0]
        reduced = [(a[:-1], b) for a, b in inequalities if a[-1] == 0]
        for a, b in positive:
            for c, d in negative:
                reduced.append(([x/a[-1] - y/c[-1] for x, y in zip(a[:-1], c[:-1])],
                                b/a[-1] - d/c[-1]))
        inequalities = reduced
        if any(not any(a) and b > 0 for a, b in inequalities):
            return False
    return all(b <= 0 for _, b in inequalities)


def chamber_vertices(columns, lower, upper):
    """Incrementally enumerate full-dimensional central-arrangement chambers."""
    active = [i for i, col in enumerate(columns) if any(col) and lower[i] < upper[i]]
    chambers = [()]
    for length, edge in enumerate(active, 1):
        extended = []
        for chamber in chambers:
            for sign in (-1, 1):
                signs = chamber + (sign,)
                rows = [[s*x for x in columns[i]] for i, s in zip(active[:length], signs)]
                if strict_cone_feasible(rows, len(columns[edge])):
                    extended.append(signs)
        chambers = extended
    vertices = {}
    for chamber in chambers:
        beta = list(lower)
        for i, sign in zip(active, chamber):
            beta[i] = upper[i] if sign > 0 else lower[i]
        image = tuple(dot([col[row] for col in columns], beta)
                      for row in range(len(columns[0])))
        vertices.setdefault(image, beta)
    check(bool(vertices), 'chambers missed every zonotope vertex')
    count('recovery chambers', len(chambers))
    return list(vertices.items())


def recover_from_vertices(vertices, target):
    """Find at most dimension+1 affinely independent images and lift weights."""
    dimension = len(target)
    for size in range(1, min(dimension+1, len(vertices))+1):
        for subset in combinations(vertices, size):
            images, leaves = zip(*subset)
            matrix = [[point[i] for point in images] for i in range(dimension)]
            matrix.append([F(1)]*size)
            weights = linear_solve(matrix, list(target)+[F(1)])
            # Uniqueness of this rectangular solve also tests affine independence.
            if weights is None or any(weight < 0 for weight in weights):
                continue
            beta = [dot(weights, [leaf[i] for leaf in leaves]) for i in range(len(leaves[0]))]
            return beta, weights, images
    raise AssertionError('Caratheodory recovery failed for attainable target')


def recovery_tests(rng):
    check(strict_cone_feasible([[F(1), F(0)], [F(0), F(1)]], 2), 'nonempty chamber rejected')
    check(not strict_cone_feasible([[F(1)], [F(-1)]], 1), 'empty chamber accepted')
    for trial in range(36):
        k, m = trial % 3, 1+trial % 4
        z = F(rng.randrange(-3, 4), 3)
        columns = [[F(rng.randrange(-2, 3))+rng.randrange(-2, 3)*z
                    + rng.randrange(-1, 2)*z*z for _ in range(k+1)] for _ in range(m)]
        if trial % 6 == 0:
            columns = [[F(0)]*(k+1) for _ in range(m)]
        elif trial % 6 == 1:
            columns = [[col[0]]*(k+1) for col in columns]
        elif trial % 6 == 2 and m > 1:
            columns[1] = [-x for x in columns[0]]
        lower = [F(rng.randrange(-2, 3), 2) for _ in range(m)]
        upper = [lo+F(rng.randrange(0, 4), 2) for lo in lower]
        vertices = chamber_vertices(columns, lower, upper)
        for _ in range(3):
            original = [lo+(hi-lo)*F(rng.randrange(7), 6) for lo, hi in zip(lower, upper)]
            target = [dot([col[i] for col in columns], original) for i in range(k+1)]
            recovered, weights, images = recover_from_vertices(vertices, target)
            check(len(weights) <= k+2, 'too many recovery vertices')
            check(sum(weights) == 1 and all(w >= 0 for w in weights), 'invalid convex weights')
            check(all(lo <= value <= hi for lo, value, hi in zip(lower, recovered, upper)),
                  'recovered leaf violates its interval')
            check(all(dot([col[i] for col in columns], recovered) == target[i] for i in range(k+1)),
                  'recovered leaf image differs from target')
            check(all(dot(weights, [point[i] for point in images]) == target[i] for i in range(k+1)),
                  'convex image reconstruction failed')
            count('exact Caratheodory recoveries')
        count('recovery instances')


def box_support_tests(rng):
    positives = negatives = 0
    for trial in range(100):
        dimension, m = 1+trial % 3, 1+trial % 5
        z = F(rng.randrange(-3, 4), rng.randrange(1, 4))
        # Evaluate random degree-two alpha_e(z), g_e(z), c(z), g_0(z).
        columns = [[F(rng.randrange(-3, 4)) + rng.randrange(-2, 3)*z
                    + rng.randrange(-2, 3)*z*z for _ in range(dimension)] for _ in range(m)]
        if trial % 7 == 0:
            columns = [[col[0]]*dimension for col in columns]
        if trial % 11 == 0:
            columns[0] = [F(0)]*dimension
        lower = [F(rng.randrange(-3, 3)) for _ in range(m)]
        upper = [lo+F(rng.randrange(0, 4)) for lo in lower]
        beta = [lo+(hi-lo)*F(rng.randrange(5), 4) for lo, hi in zip(lower, upper)]
        image = [sum((b*col[i] for b, col in zip(beta, columns)), F(0))
                 for i in range(dimension)]
        shift = 1+z*z  # g_0(z): w's last coordinate is v-g_0(z).
        targets = [image,
                   [x+F(rng.randrange(-9, 10), 2) for x in image]]
        for target in targets:
            value = shift+target[-1]
            actual = support_value_membership(columns, lower, upper, target[:-1], value, shift)
            witness = box_lp_vertices(columns, lower, upper, target)
            check(actual == (witness is not None), 'support/LP disagreement')
            if witness is not None:
                check(all(dot([col[i] for col in columns], witness) == target[i]
                          for i in range(dimension)), 'recovered LP image')
                check(shift+dot([col[-1] for col in columns], witness) == value,
                      'recovered objective omits core-only offset')
                positives += 1
            else:
                negatives += 1
            count('exact support/LP comparisons')
    # The nonzero offset is essential: omitting or reversing it rejects this
    # feasible value. This calls the value interface without a local round trip.
    check(support_value_membership([[F(1)]], [F(0)], [F(1)], [], F(5, 2), F(2)),
          'nonzero core-only offset lost')
    check(not support_value_membership([[F(1)]], [F(0)], [F(1)], [], F(5, 2), F(0)),
          'offset-omission regression is ineffective')
    check(not support_value_membership([[F(1)]], [F(0)], [F(1)], [], F(5, 2), F(-2)),
          'offset-sign regression is ineffective')
    # Coordinate directions alone miss this point outside a diagonal segment.
    columns = [[F(1), F(1)]]
    check(not support_membership(columns, [F(0)], [F(1)], [F(1), F(0)]),
          'rank-deficient affine-hull rejection')
    check(support_membership([[F(0)]], [F(2)], [F(2)], [F(0)]), 'singleton zero image')
    # Full-dimensional slanted facet missed by the coordinate directions.
    columns = [[F(1), F(1)], [F(1), F(-1)]]
    check(not support_membership(columns, [F(0)]*2, [F(1)]*2, [F(0), F(1)]),
          'slanted facet not tested')
    check(positives > 90 and negatives > 50, 'membership tests lack both outcomes')
    STATS['feasible membership cases'], STATS['infeasible membership cases'] = positives, negatives


def derivative_tests(rng):
    worst = Decimal(0)
    for trial in range(8):
        if trial % 2:
            n, topology = subdivided('theta' if trial % 4 == 1 else 'k4', rng)
        else:
            n = 5
            topology = [(0, 1, F(1)), (1, 2, F(1)), (2, 0, F(1)),
                        (2, 3, F(1)), (3, 4, F(1)), (4, 2, F(1))]
        # Nonzero exact states avoid differentiability assumptions at rho=0.
        potential = list(map(F, rng.sample(range(2*n), n)))
        edges, expected, nomination = [], [], [F(0)]*n
        for u, v, _ in topology:
            drop = potential[u]-potential[v]
            x = F(rng.randrange(1, 4), 2)*(1 if drop > 0 else -1)
            edges.append((u, v, drop/(x*abs(x))))
            expected.append(x)
            nomination[u] += x
            nomination[v] -= x
        x, pi = a1.solve(n, edges, nomination)
        check(max(abs(y-a1.dec(t)) for y, t in zip(x, expected)) < Decimal('1e-20'),
              'base exact physical state recovery')
        a, c = 0, n-1
        rhs = [F(0)]*n
        rhs[a], rhs[c] = F(1), F(-1)
        derivative_r = [2*beta*abs(flow) for (_, _, beta), flow in zip(edges, expected)]
        h = adjoint(n, edges, derivative_r, rhs, c)
        for e in rng.sample(range(len(edges)), min(3, len(edges))):
            u, v, beta = edges[e]
            predicted = (h[u]-h[v])/derivative_r[e]*expected[e]*abs(expected[e])
            step = beta/F(10**7)
            plus, minus = list(edges), list(edges)
            plus[e], minus[e] = (u, v, beta+step), (u, v, beta-step)
            xp, pp = a1.solve(n, plus, nomination)
            xm, pm = a1.solve(n, minus, nomination)
            measured = ((pp[a]-pp[c])-(pm[a]-pm[c]))/(2*a1.dec(step))
            error = abs(measured-a1.dec(predicted))
            worst = max(worst, error)
            check(error < Decimal('1e-10'), 'resistance derivative finite difference')
            bound = sum(abs(b) for b in nomination)**2 * 2*step
            check(abs((pp[a]-pp[c])-(pm[a]-pm[c])) <= a1.dec(bound),
                  'resistance Lipschitz finite difference')
            count('resistance derivatives')
    STATS['maximum derivative error'] = f'{worst:.3e}'


def parallel_state(total, target_beta, other_beta):
    total, target_beta, other_beta = map(a1.dec, (total, target_beta, other_beta))
    flow = total*other_beta.sqrt()/(target_beta.sqrt()+other_beta.sqrt())
    return flow, target_beta*flow*abs(flow)


def arc_tests(rng):
    # Two parallel paths, with an unloaded subdivision on the other path.
    # Target flow has the sign of total injection. For nonnegative total it
    # increases with total and other resistance and decreases with target
    # resistance. Negative total reverses the latter two monotonicities.
    # Therefore this family's extrema really do occur at the tested corners.
    for trial in range(8):
        lo = F(rng.randrange(-4, 2), 2)
        hi = lo+F(rng.randrange(1, 5), 2)
        boxes = [(F(1), F(3+trial % 2)), (F(1, 2), F(2))]
        corner_values = [parallel_state(total, beta, other)[0]
                         for total, beta, other in product((lo, hi), *boxes)]
        low, high = min(corner_values), max(corner_values)
        for i, j, k in product(range(13), repeat=3):
            total = lo+(hi-lo)*F(i, 12)
            beta = boxes[0][0]+(boxes[0][1]-boxes[0][0])*F(j, 12)
            other = boxes[1][0]+(boxes[1][1]-boxes[1][0])*F(k, 12)
            value, _ = parallel_state(total, beta, other)
            check(low-Decimal('1e-60') <= value <= high+Decimal('1e-60'),
                  'tiny arc grid exceeds face/corner optimum')
            count('arc grid scenarios')
        # Compare the independent whole-graph solver with closed-form corners.
        for total, beta, other in product((lo, hi), *boxes):
            edges = [(0, 1, beta), (0, 2, other/2), (2, 1, other/2)]
            x, pi = a1.solve(3, edges, [total, -total, F(0)])
            expected, drop = parallel_state(total, beta, other)
            check(abs(x[0]-expected) < Decimal('1e-20'), 'arc closed form/solver')
            check(abs(pi[0]-pi[1]-drop) < Decimal('1e-20'), 'drop closed form/solver')
        count('arc extrema families')
    # Exact signed capacity decisions on this rank-one family, including ties.
    # phi(q) is strictly increasing and vanishes exactly at the physical flow;
    # rational signed-square evaluation therefore decides root <= capacity.
    for total, beta, other in [(F(1), F(1), F(1)), (F(-1), F(1), F(1)),
                               (F(0), F(2), F(3)), (F(1), F(2), F(1))]:
        flow, _ = parallel_state(total, beta, other)
        for capacity in map(F, [-1, F(-1, 2), 0, F(1, 3), F(1, 2), 1]):
            phi = beta*capacity*abs(capacity)-other*(total-capacity)*abs(total-capacity)
            if phi == 0:
                check(abs(flow-a1.dec(capacity)) < Decimal('1e-70'), 'exact capacity tie')
                count('exact capacity ties')
            else:
                check((flow < a1.dec(capacity)) == (phi > 0), 'exact capacity comparison')
            count('exact capacity decisions')
    first, drop_first = parallel_state(1, 1, 1)
    last, drop_last = parallel_state(1, 4, 1)
    check(first == Decimal(1)/2 and last == Decimal(1)/3, 'arc witness endpoints')
    check(first > last and drop_first < drop_last, 'pressure/flow optimizer difference')
    # Target-edge inverse estimate, both signs and zero, independent scenarios.
    for _ in range(100):
        b, c = F(rng.randrange(-6, 7), 3), F(rng.randrange(-6, 7), 3)
        beta, gamma = F(rng.randrange(1, 8), 2), F(rng.randrange(1, 8), 2)
        x, drop = parallel_state(b, beta, 1)
        y, other = parallel_state(c, gamma, 1)
        bound = 2*(abs(drop-other)+Decimal(4)*a1.dec(abs(beta-gamma)))/a1.dec(min(beta, gamma))
        check((x-y)**2 <= bound+Decimal('1e-60'), 'arc inverse estimate')
    # Rational bridge extrema under balance, including negative and singleton.
    for lower, upper in [([-2, -3, 1], [4, -1, 3]), ([0, 0], [0, 0])]:
        lo = max(F(lower[0]), -sum(map(F, upper[1:])))
        hi = min(F(upper[0]), -sum(map(F, lower[1:])))
        check(lo <= hi, 'bridge interval empty')
        for endpoint in (lo, hi):
            remainder = -endpoint-sum(map(F, lower[1:]))
            nomination = [endpoint] + list(map(F, lower[1:]))
            for i in range(1, len(lower)):
                add = min(remainder, upper[i]-lower[i])
                nomination[i] += add
                remainder -= add
            check(sum(nomination) == 0 and remainder == 0, 'bridge endpoint attainability')
            x, _ = a1.solve(len(lower), [(i-1, i, F(1)) for i in range(1, len(lower))], nomination)
            check(abs(x[0]-a1.dec(endpoint)) < Decimal('1e-30'), 'bridge cut sum')


def main():
    rng = random.Random(2026090703)
    with localcontext() as context:
        context.prec = 90
        topology_and_adjoint(rng)
        box_support_tests(rng)
        recovery_tests(random.Random(202609070302))
        derivative_tests(rng)
        arc_tests(rng)
    print(f'PASS: {CHECKS:,} A3 assertions; {a1.CHECKS:,} imported A1 assertions.')
    for name, value in STATS.items():
        print(f'  {name}: {value}')
    print('Exact Fraction identities and exhaustive support membership passed; numerical checks are regression evidence.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
