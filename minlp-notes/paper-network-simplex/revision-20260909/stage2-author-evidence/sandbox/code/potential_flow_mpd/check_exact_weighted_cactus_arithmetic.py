"""Independent exact arithmetic, supplied-block mapping and schema review.

Run with python -S and python -S -O. No floating-point comparisons are used.
Graph reconstruction here tests explicit fixtures; the solver accepts blocks,
not an arbitrary graph, and does not certify a caller's graph decomposition.
"""
from copy import deepcopy
from fractions import Fraction as F
from pathlib import Path
import json
import subprocess
import sys
import tempfile

from exact_weighted_cactus import Quadratic as Q, solve_cycle, solve_cactus


def check(ok, message):
    if not ok:
        raise RuntimeError(message)


def rejects(fn, message):
    try:
        fn()
    except (ValueError, TypeError):
        return
    raise RuntimeError(message)


def decode(data):
    return Q(F(data['rational']), F(data['sqrt_coefficient']), F(data['radicand']))


def symbolic_add(total, value, weight=F(1)):
    total[F(0)] = total.get(F(0), F(0))+weight*value.a
    if value.b:
        total[value.d] = total.get(value.d, F(0))+weight*value.b
    return {key: value for key, value in total.items() if value}


def arithmetic():
    count = 0
    # Pell identities provide exact signs of numbers exponentially near zero.
    # No decimal precision threshold decides equality.
    p, q = 1, 0
    for n in range(1, 1001):
        p, q = p+2*q, p+q
        if n not in [1, 2, 5, 20, 100, 500, 999, 1000]:
            continue
        known = p*p-2*q*q
        check(known in [-1, 1], 'Pell fixture identity')
        value = Q(p, -q, 2)
        check(value.compare(0) == known, 'Pell nearzero comparison')
        huge = F(10**400)
        check(Q(huge+p, 0).compare(Q(huge, q, 2)) == known,
              'common huge rational cancellation')
        # Two different irrational fields, with nonzero rational difference.
        # e-(a+sqrt2)^2 = 2*a*(p/q-sqrt2), whose sign is known.
        a = F(7, 3)
        e = a*a+2+2*a*F(p, q)
        check(Q(a, 1, 2).compare(Q(0, 1, e)) == -known,
              'two-radical nearcancellation')
        count += 3
    for d in [F(2), F(3), F(2, 7), F(101, 17)]:
        for k in [F(2), F(1, 13), F(10**80, 3)]:
            for b in [F(1), F(-3, 7)]:
                x, y = Q(F(10**50), b, d), Q(F(10**50), b/k, d*k*k)
                check(x.compare(y) == y.compare(x) == 0 and x == y,
                      'equal differently represented radicals')
                check((x-F(1, 10**300)).compare(y) == -1,
                      'near equality incorrectly rounded to equality')
                count += 2
    for b in [F(10**300), F(-10**300), F(1, 10**300), F(-1, 10**300)]:
        for bits in [0, 1, 40, 1000]:
            x = Q(F(13, 7), b, F(5, 11))
            lo, hi = x.interval(bits)
            # Compare by independently squaring each transformed endpoint.
            root_lo, root_hi = sorted([(lo-x.a)/b, (hi-x.a)/b])
            check(0 <= root_lo and root_lo*root_lo <= x.d <= root_hi*root_hi,
                  'radical interval inclusion')
            check(hi-lo <= F(1, 1 << bits), 'large/small coefficient interval width')
            count += 1
    rejects(lambda: Q(0, 1, -1), 'negative radicand accepted')
    rejects(lambda: Q(0, 1, 2)+Q(0, 1, 3), 'unsupported field addition accepted')
    rejects(lambda: Q(0, 1, 2)*Q(0, 1, 3), 'unsupported field product accepted')
    rejects(lambda: Q(0, 1, 2).interval(True), 'boolean precision accepted')
    print(f'Arithmetic review passed: {count} exact cancellation/equality/interval controls.')


def mapping():
    cycles = [dict(offsets=[0, 0, 3], weights=[-2, 1, 4], lower=[1, 1, 1], upper=[1, 1, 1]),
              dict(offsets=[0, 1, 2], weights=[1, -3, 2], lower=[1, 2, 4], upper=[2, 3, 5])]
    graph_cycles = [[(0, 1), (1, 2), (2, 0)], [(0, 3), (3, 4), (4, 0)]]
    bridge = dict(flow=2, weight=-5, lower=1, upper=3)
    problem = dict(cycles=cycles, bridges=[bridge])
    for sense in ['max', 'min']:
        problem['sense'] = sense
        answer = solve_cactus(problem, bits=80)
        check(answer['status'] == 'optimal', 'fixture unexpectedly infeasible')
        edges, flows, drops, weights, offsets = [], [], [], [], []
        for block, arcs, result in zip(cycles, graph_cycles, answer['cycles']):
            q = decode(result['circulation'])
            for arc, t, w, beta in zip(arcs, block['offsets'], block['weights'], result['resistances']):
                x = q+t
                edges.append(arc)
                flows.append(x)
                drops.append(F(beta)*x*x*(1 if x >= 0 else -1))
                weights.append(F(w))
                offsets.append(F(t))
            # Reverse the coherent cycle orientation and its array order.
            reversed_block = dict(offsets=[-t for t in reversed(block['offsets'])],
                                  weights=[-w for w in reversed(block['weights'])],
                                  lower=list(reversed(block['lower'])),
                                  upper=list(reversed(block['upper'])))
            reversed_result = solve_cycle(**reversed_block, sense=sense)
            check(reversed_result['objective'] == decode(result['objective']),
                  'coherent orientation reversal changed optimum')
            shifted = deepcopy(block)
            shifted['offsets'] = [F(t)+F(10**100, 7) for t in block['offsets']]
            shifted['weights'] = [F(w)+F(10**90, 11) for w in block['weights']]
            shifted_result = solve_cycle(**shifted, sense=sense)
            check(shifted_result['objective'] == decode(result['objective']),
                  'circulation/weight gauge shifts changed optimum')
        edges.append((4, 5))
        flows.append(Q(bridge['flow']))
        drops.append(Q(F(answer['bridges'][0]['resistance'])*bridge['flow']**2))
        weights.append(F(bridge['weight']))
        offsets.append(F(bridge['flow']))
        # Reconstruct b=A*offset and c=A*w independently from an actual graph.
        b, c, actual = [F(0)]*6, [F(0)]*6, [{} for _ in range(6)]
        for (u, v), t, w, x in zip(edges, offsets, weights, flows):
            b[u] += t
            b[v] -= t
            c[u] += w
            c[v] -= w
            actual[u] = symbolic_add(actual[u], x)
            actual[v] = symbolic_add(actual[v], x, F(-1))
        check(all(value == ({F(0): load} if load else {}) for value, load in zip(actual, b)),
              'block offsets failed graph conservation')
        potentials = {0: Q(0)}
        while len(potentials) < 6:
            for (u, v), drop in zip(edges, drops):
                if u in potentials and v not in potentials:
                    potentials[v] = potentials[u]-drop
                elif v in potentials and u not in potentials:
                    potentials[u] = potentials[v]+drop
        check(all(potentials[u]-potentials[v] == drop for (u, v), drop in zip(edges, drops)),
              'returned blocks cannot reconstruct physical potentials')
        graph_value, block_value = {}, {}
        for node, weight in enumerate(c):
            graph_value = symbolic_add(graph_value, potentials[node], weight)
        for term in answer['objective_terms']:
            block_value = symbolic_add(block_value, decode(term))
        check(graph_value == block_value, 'c.T*pi differs from summed block objective')
    print('Mapping review passed: two cactus cycles plus bridge, both senses, '
          'reversed arcs and huge circulation/objective gauges.')


def schema():
    valid = dict(cycles=[dict(offsets=[0, 0, 3], weights=[-2, 1, 4],
                             lower=[1, 1, 1], upper=[1, 1, 1])],
                 bridges=[dict(flow=2, weight=-5, lower=1, upper=3)])
    bads = [{}, [], {'edges': [[0, 1]], 'b': [1, -1]}, {'cycles': None},
            {'cycles': [None]}, {'cycles': [[]]}, {'bridges': 'unsupported'}]
    paths = [(['cycles', 0, 'offsets'], None), (['cycles', 0, 'offsets'], '0,0,3'),
             (['cycles', 0, 'weights'], [0]), (['cycles', 0, 'lower'], [0, 1, 1]),
             (['cycles', 0, 'upper'], [0, 1, 1]), (['cycles', 0, 'offsets'], [True, 0, 3]),
             (['cycles', 0, 'offsets'], [0.0, 0, 3]), (['cycles', 0, 'capacity'], [1, 1, 1]),
             (['cycles', 0, 'flow_lower'], [0, 0]), (['bridges', 0, 'capacity'], 1),
             (['bridges', 0, 'lower'], -1), (['bridges', 0, 'flow'], 2.0),
             (['bridges', 0, 'flow_upper'], True), (['sense'], 'maximize')]
    for path, value in paths:
        bad = deepcopy(valid)
        cursor = bad
        for key in path[:-1]:
            cursor = cursor[key]
        cursor[path[-1]] = value
        bads.append(bad)
    late_bad = deepcopy(valid)
    late_bad['cycles'][0]['flow_lower'] = [10, 10, 10]
    late_bad['bridges'][0]['lower'] = -1
    bads.append(late_bad)
    late_bad = deepcopy(valid)
    late_bad['bridges'][0]['flow_upper'] = 1
    late_bad['bridges'].append(dict(flow=0, weight=0, lower=False, upper=1))
    bads.append(late_bad)
    for bad in bads:
        rejects(lambda bad=bad: solve_cactus(bad), 'invalid schema accepted')
    rejects(lambda: solve_cactus(valid, bits=True), 'boolean output precision accepted')
    for sense in ['max', 'min']:
        exact_capacity = deepcopy(valid)
        exact_capacity['sense'] = sense
        exact_capacity['bridges'][0].update(flow_lower=2, flow_upper=2)
        check(solve_cactus(exact_capacity)['status'] == 'optimal', 'tight bridge capacity rejected')
        exact_capacity['bridges'][0]['flow_upper'] = F(199, 100)
        exact_capacity['bridges'][0]['flow_lower'] = None
        check(solve_cactus(exact_capacity)['status'] == 'infeasible', 'bridge capacity ignored')
    print(f'Schema review passed: {len(bads)+1} invalid objects rejected and exact bridge capacities checked.')
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory)/'problem.json'
        script = str(Path(__file__).with_name('exact_weighted_cactus.py'))
        for flags in [['-S'], ['-S', '-O']]:
            path.write_text(json.dumps(valid))
            result = subprocess.run([sys.executable, *flags, script, str(path)], capture_output=True)
            check(result.returncode == 0 and json.loads(result.stdout)['status'] == 'optimal',
                  'valid CLI fixture failed')
            path.write_text('{"cycles":[],"cycles":[]}')
            result = subprocess.run([sys.executable, *flags, script, str(path)], capture_output=True)
            check(result.returncode != 0, 'duplicate JSON key accepted')
    print('CLI review passed under -S and -S -O, including duplicate-key rejection.')


if __name__ == '__main__':
    arithmetic()
    mapping()
    schema()
