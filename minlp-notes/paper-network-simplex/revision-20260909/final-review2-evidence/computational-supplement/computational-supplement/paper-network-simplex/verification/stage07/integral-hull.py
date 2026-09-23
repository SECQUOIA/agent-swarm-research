"""Exact small-instance checks of the classical integral-flow hull corollary.

Enumerates all bounded-flow vertices by free-column/bound choices, with an
independent rational elimination routine. No production oracle or LP is used.
This is finite verification, not a computational proof of the general result.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import random


def solve_unique(columns, rhs):
    n = len(columns)
    rows = [[F(columns[j][i]) for j in range(n)] + [F(rhs[i])]
            for i in range(len(rhs))]
    pivots = []
    rank = 0
    for j in range(n):
        pivot = next((i for i in range(rank, len(rows)) if rows[i][j]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        scale = rows[rank][j]
        rows[rank] = [v / scale for v in rows[rank]]
        for i in range(len(rows)):
            if i != rank:
                scale = rows[i][j]
                rows[i] = [v - scale*w for v, w in zip(rows[i], rows[rank])]
        pivots.append(j)
        rank += 1
    if any(not any(row[:-1]) and row[-1] for row in rows) or rank != n:
        return None
    answer = [F(0)] * n
    for i, j in enumerate(pivots):
        answer[j] = rows[i][-1]
    return answer


def vertices(arcs, b, u):
    columns = []
    for tail, head in arcs:
        col = [0] * len(b)
        col[tail] -= 1
        col[head] += 1
        columns.append(col)
    result = set()
    for choices in product((-1, 0, 1), repeat=len(arcs)):
        free = [e for e, choice in enumerate(choices) if choice == -1]
        x = [F(u[e] if choice == 1 else 0) for e, choice in enumerate(choices)]
        rhs = [F(b[i]) - sum(columns[e][i]*x[e] for e in range(len(arcs)))
               for i in range(len(b))]
        value = solve_unique([columns[e] for e in free], rhs)
        if value is None:
            continue
        for e, v in zip(free, value):
            x[e] = v
        if all(0 <= v <= u[e] for e, v in enumerate(x)):
            assert all(sum(columns[e][i]*x[e] for e in range(len(arcs))) == b[i]
                       for i in range(len(b)))
            result.add(tuple(x))
    return sorted(result)


def main():
    rng = random.Random(7072026)
    cases = []
    total_vertices = decompositions = 0
    for case in range(18):
        n = 4
        arcs = [(rng.randrange(n), rng.randrange(n)) for _ in range(5 + case % 3)]
        u = [rng.randrange(4) for _ in arcs]
        ref = [rng.randrange(cap+1) for cap in u]
        b = [0] * n
        for e, (tail, head) in enumerate(arcs):
            b[tail] -= ref[e]
            b[head] += ref[e]
        vs = vertices(arcs, b, u)
        assert vs and all(v.denominator == 1 for x in vs for v in x)
        total_vertices += len(vs)
        for m in (0, 1, 3):
            raw = [rng.randrange(4) for _ in range(m+1)]
            raw[-1] += 1
            weights = [F(v, sum(raw)) for v in raw]
            states = []
            integral_terms = []
            for j, weight in enumerate(weights):
                first, second = rng.choice(vs), rng.choice(vs)
                state = tuple((a + 2*b)/3 for a, b in zip(first, second))
                states.append(state)
                if weight:
                    integral_terms.extend(((weight/3, j, first), (2*weight/3, j, second)))
            obs = [(e, j) for e in range(len(arcs)) for j in range(m)
                   if rng.randrange(2)]
            x = [sum(weights[j]*states[j][e] for j in range(m+1))
                 for e in range(len(arcs))]
            z = {(e, j): weights[j]*states[j][e] for e, j in obs}
            assert sum(t[0] for t in integral_terms) == 1
            assert all(x[e] == sum(w*v[e] for w, _, v in integral_terms)
                       for e in range(len(arcs)))
            assert all(weights[j] == sum(w for w, k, _ in integral_terms if k == j)
                       for j in range(m))
            assert all(z[e, j] == sum(w*v[e] for w, k, v in integral_terms if k == j)
                       for e, j in obs)
            decompositions += 1
        cases.append({'arcs': arcs, 'capacities': u, 'balances': b, 'vertices': len(vs)})
    assert vertices([], [1], []) == []
    assert vertices([], [0], []) == [()]
    # At m=0, a fractional flow needs more than m+1=1 integral graph point.
    parallel = vertices([(0, 1), (0, 1)], [-1, 1], [1, 1])
    half = (F(1, 2), F(1, 2))
    assert half not in parallel and len(parallel) == 2
    assert tuple((a+b)/2 for a, b in zip(*parallel)) == half
    result = {'status': 'PASS', 'random_instances': len(cases),
              'exact_vertices': total_vertices, 'exact_refined_decompositions': decompositions,
              'empty_and_zero_dimensional_cases': 2, 'integral_point_count_counterexample': True,
              'arithmetic': 'Fraction; independent elimination; no LP', 'cases': cases}
    Path(__file__).with_suffix('.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'cases'}, indent=2))


if __name__ == '__main__':
    main()
