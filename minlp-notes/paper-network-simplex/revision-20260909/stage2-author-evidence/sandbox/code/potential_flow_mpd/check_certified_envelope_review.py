"""Independent stdlib audit of the original-instance envelope verifier.

Fixtures are built from rational physical potentials or a zero dual potential;
no numerical producer, energy-certificate producer, or graph package is used.
"""
import copy
from decimal import Decimal, localcontext
from fractions import Fraction as F
import itertools
import json
from math import isqrt
from pathlib import Path
import subprocess
import sys
import tempfile

from certified_envelope import check_graph, envelope, verify


def check(condition, message):
    if not condition:
        raise RuntimeError(message)


def connected(vertices, edges):
    if not vertices:
        return False
    reached = {min(vertices)}
    while True:
        more = {v for u, v in edges if u in reached and v in vertices}
        more |= {u for u, v in edges if v in reached and u in vertices}
        if more <= reached:
            return reached == set(vertices)
        reached |= more


def branch_partitions(n):
    # A K4 minor is precisely four disjoint connected nonempty branch sets
    # with an edge between each pair. Vertices labelled -1 are discarded.
    for labels in itertools.product(range(-1, 4), repeat=n):
        groups = [{v for v, label in enumerate(labels) if label == i} for i in range(4)]
        if all(groups) and [min(g) for g in groups] == sorted(min(g) for g in groups):
            yield groups


def graph_audit():
    count = rejected = 0
    for n in range(2, 6):
        pairs = list(itertools.combinations(range(n), 2))
        partitions = list(branch_partitions(n))
        for mask in range(1 << len(pairs)):
            edges = [list(edge) for i, edge in enumerate(pairs) if mask & (1 << i)]
            if not connected(set(range(n)), edges):
                continue
            minor = any(all(connected(g, edges) for g in groups) and
                        all(any((u in a and v in b) or (u in b and v in a)
                                for u, v in edges)
                            for a, b in itertools.combinations(groups, 2))
                        for groups in partitions)
            try:
                check_graph(edges, n)
                accepted = True
            except ValueError:
                accepted = False
            check(accepted != minor, 'graph recognition disagrees with branch-set definition')
            count += 1
            rejected += minor
    # Every edge of K4 subdivided once: no literal K4 subgraph remains.
    edges = []
    for i, (u, v) in enumerate(itertools.combinations(range(4), 2)):
        edges.extend([[u, i + 4], [i + 4, v]])
    try:
        check_graph(edges, 10)
    except ValueError:
        pass
    else:
        raise RuntimeError('accepted subdivided K4')
    return count, rejected


def certificate(flow, potentials, cp, cm, edges, zero_dual=False):
    if zero_dual:
        potentials = [F(0)] * len(potentials)
    roots = []
    for e, (u, v) in enumerate(edges):
        drop = potentials[u] - potentials[v]
        square = abs(drop)**3 / (cp[e] if drop >= 0 else cm[e])
        root = F(isqrt(square.numerator), isqrt(square.denominator))
        check(root**2 == square, 'fixture conjugate root must be rational')
        roots.append(root)
    gap = sum((cp[e] if x >= 0 else cm[e]) * abs(x)**3 / 3
              for e, x in enumerate(flow))
    gap -= sum((potentials[u] - potentials[v]) * flow[e]
               for e, (u, v) in enumerate(edges)) - F(2, 3) * sum(roots)
    radius = F(0) if gap == 0 else F(1)
    while radius**3 * min(cp + cm) < 6 * gap:
        radius *= 2
    return dict(flow=list(map(str, flow)), potentials=list(map(str, potentials)),
                root_upper=list(map(str, roots)), gap=str(gap), radius=str(radius))


def physical_fixture(sense, target, polarity, scale):
    edges = [[0, 2], [3, 0], [0, 4], [2, 1], [1, 3], [4, 1],
             [0, 5], [5, 6], [6, 0], [6, 7]]
    data = dict(edges=edges, b=['0'] * 8, target=target, sense=sense,
                resistances=[{'values': ['4', '1', '9/4', '1']} if i % 2 else
                             {'interval': ['1', '4']} for i in range(len(edges))])
    _, _, lower, upper, cp, cm, signs = envelope(data)
    if target == 0:
        check(signs == [1, -1, 1, -1, -1, 1, 0, 0, 0, 0], 'K2,3 adjoint signs')
    else:
        check(signs == [0] * 9 + [1], 'bridge adjoint signs')
    p = [F(v) * polarity * scale**2 for v in [4, 0, 4, 0, 4, 0, 4, 0]]
    x, beta = [], []
    b = [F(0)] * 8
    for e, (u, v) in enumerate(edges):
        drop = p[u] - p[v]
        coef = cp[e] if drop >= 0 else cm[e]
        square = abs(drop) / coef
        flow = F(isqrt(square.numerator), isqrt(square.denominator))
        check(flow**2 == square, 'fixture flow must be rational')
        if drop < 0:
            flow = -flow
        x.append(flow)
        beta.append(upper[e] if flow == 0 else coef)
        b[u] += flow
        b[v] -= flow
    data['b'] = list(map(str, b))
    payload = dict(version=1, instance=data, envelope=certificate(x, p, cp, cm, edges),
                   scenario=dict(resistances=list(map(str, beta)),
                                 certificate=certificate(x, p, beta, beta, edges)))
    report = verify(payload)
    check(report['scenario_exactly_optimal'] and report['scenario_loss_upper'] == 0,
          'exact rational physical state must certify exact endpoint optimality')
    check(report['optimum_interval'] == (x[target], x[target]), 'zero-gap singleton interval')
    return payload


def loose_fixture(sense, polarity):
    edges = [[0, 1], [0, 2], [2, 1]]
    data = dict(edges=edges, b=[str(polarity), str(-polarity), '0'], target=0, sense=sense,
                resistances=[{'values': ['1', '9/4', '4']}] * 3)
    _, _, _, _, cp, cm, _ = envelope(data)
    flow, p, beta = [F(0), F(polarity), F(polarity)], [F(0)] * 3, [F(4)] * 3
    payload = dict(version=1, instance=data, envelope=certificate(flow, p, cp, cm, edges, True),
                   scenario=dict(resistances=list(map(str, beta)),
                                 certificate=certificate(flow, p, beta, beta, edges, True)))
    report = verify(payload)
    check(not report['scenario_exactly_optimal'], 'loose certificate must not resolve switched signs')
    # Independent closed-form physical solution: two parallel paths of
    # resistance beta_0 and beta_1+beta_2, with equal pressure drop.
    with localcontext() as ctx:
        ctx.prec = 75
        def decimal(q):
            return Decimal(q.numerator) / Decimal(q.denominator)
        currents = [Decimal(polarity) * Decimal(b + c).sqrt() /
                    (Decimal(a).sqrt() + Decimal(b + c).sqrt())
                    for a, b, c in itertools.product([1, 4], repeat=3)]
        optimum = (max if sense == 'max' else min)(currents)
        attained = Decimal(polarity) * Decimal(8).sqrt() / (Decimal(4).sqrt() + Decimal(8).sqrt())
        check(decimal(report['optimum_interval'][0]) <= optimum <= decimal(report['optimum_interval'][1]),
              'closed-form optimum outside certified interval')
        check(decimal(report['scenario_interval'][0]) <= attained <= decimal(report['scenario_interval'][1]),
              'closed-form scenario outside certified interval')
        loss = optimum - attained if sense == 'max' else attained - optimum
        check(0 <= loss <= decimal(report['scenario_loss_upper']), 'direct loss bound failed')
    return payload


def corruption_audit(valid):
    controls = [(['version'], True), (['instance', 'target'], True),
                (['instance', 'target'], -1), (['instance', 'sense'], 'MAX'),
                (['instance', 'edges', 0], [True, 2]),
                (['instance', 'edges', 0], [0, 0]),
                (['instance', 'edges', 0], [0, 8]),
                (['instance', 'edges', 1], [2, 0]),
                (['instance', 'b', 0], 1.0), (['instance', 'b', 0], 'NaN'),
                (['instance', 'b', 0], '1/0'), (['instance', 'b', 0], '999'),
                (['instance', 'resistances', 0], {'interval': ['4', '1']}),
                (['instance', 'resistances', 0], {'interval': ['0', '4']}),
                (['instance', 'resistances', 0], {'values': []}),
                (['instance', 'resistances', 0], {'values': ['-1']}),
                (['instance', 'resistances', 0], {'values': ['1'], 'interval': ['1', '4']}),
                (['scenario', 'resistances', 0], '9/4'),
                (['envelope', 'flow', 0], '999'),
                (['envelope', 'root_upper', 0], '-1'),
                (['envelope', 'gap'], '-1'), (['envelope', 'gap'], '1'),
                (['envelope', 'radius'], '-1'),
                (['scenario', 'certificate', 'gap'], '1'),
                (['scenario', 'certificate', 'potentials'], []),
                (['envelope', 'root_upper'], []),
                (['envelope', 'extra'], 'unsupported'),
                (['instance', 'capacity'], ['100'] * 10)]
    script = str(Path(__file__).with_name('certified_envelope.py'))
    runs = 0
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / 'input.json'
        cases = []
        for indices, value in controls:
            bad = copy.deepcopy(valid)
            dest = bad
            for index in indices[:-1]:
                dest = dest[index]
            dest[indices[-1]] = value
            cases.append(json.dumps(bad))
        cases.extend([json.dumps(valid).replace('"version": 1', '"version": 1, "version": 1', 1),
                      '[]', 'null', '{', json.dumps(valid).replace('"max"', 'NaN')])
        for flags in (['-S'], ['-S', '-O']):
            path.write_text(json.dumps(valid))
            good = subprocess.run([sys.executable, *flags, script, 'verify', str(path)], capture_output=True)
            check(good.returncode == 0, good.stderr.decode())
            for i, text in enumerate(cases):
                path.write_text(text)
                result = subprocess.run([sys.executable, *flags, script, 'verify', str(path)], capture_output=True)
                check(result.returncode != 0, f'corruption {i} accepted with {flags}')
                runs += 1
    return runs


def run():
    count, rejected = graph_audit()
    fixtures = []
    for sense, target, polarity, scale in itertools.product(
            ['max', 'min'], [0, 9], [-1, 1], [F(0), F(1), F(1, 10**70)]):
        fixtures.append(physical_fixture(sense, target, polarity, scale))
    for sense, polarity in itertools.product(['max', 'min'], [-1, 1]):
        loose_fixture(sense, polarity)
    corruptions = corruption_audit(fixtures[1])
    print(f'{count} connected graph comparisons ({rejected} K4-minor rejections), '
          f'one subdivided K4 rejection; {len(fixtures)} exact physical fixtures; '
          f'4 independent closed-form loss checks; {corruptions} malformed CLI rejections.')


def producer_scaling_audit():
    """Optional numerical-producer check; needs the project environment."""
    from certified_envelope import solve
    count = 0
    for sense in ['max', 'min']:
        baseline = None
        for supply, resistance in [(F(1), F(1)), (F(1, 10**400), F(10**400)),
                                   (F(10**400), F(1, 10**400))]:
            data = dict(edges=[[0, 1], [0, 2], [2, 1]],
                        b=[str(supply), str(-supply), '0'], target=0, sense=sense,
                        resistances=[{'interval': [str(resistance), str(4 * resistance)]}] * 3)
            payload, report, _ = solve(data)
            normalized = tuple(v / supply for v in report['optimum_interval'])
            if baseline is None:
                baseline = normalized
            else:
                check(normalized == baseline, 'exact normalization loses supply/units invariance')
            check(report['scenario_exactly_optimal'], 'triangle endpoint signs should be resolved')
            with localcontext() as ctx:
                ctx.prec = 75
                # target minimum: resistance4 versus alternative total2;
                # target maximum: resistance1 versus alternative total8.
                root = Decimal(8 if sense == 'max' else 2).sqrt()
                exact = root / (Decimal(1 if sense == 'max' else 2) + root)
                lo, hi = (Decimal(q.numerator) / Decimal(q.denominator)
                          for q in (v / supply for v in report['optimum_interval']))
                check(lo <= exact <= hi, 'numerical producer certificate misses analytic solution')
            verify(payload)
            count += 1
    print(f'{count} producer checks passed: both senses and supply/resistance scales '
          '10^400 and 10^-400 preserve identical normalized rational bounds.')


def goal_integration_audit():
    payload = physical_fixture('max', 9, 1, F(1))
    edges, b, _, _, cp, cm, _ = envelope(payload['instance'])
    flow = list(map(F, payload['envelope']['flow']))
    beta = list(map(F, payload['scenario']['resistances']))
    payload['envelope'] = certificate(flow, [F(0)] * len(b), cp, cm, edges, True)
    payload['scenario']['certificate'] = certificate(flow, [F(0)] * len(b), beta, beta, edges, True)
    before = verify(payload)
    check(before['optimum_interval'][0] < before['optimum_interval'][1], 'loose bridge fixture')
    # All intervals contain zero, so every certified curvature is zero. The
    # target bridge functional is the cut potential with value1 except at leaf7.
    goals = {}
    for name, base in [('envelope', payload['envelope']),
                       ('scenario', payload['scenario']['certificate'])]:
        radius = F(base['radius'])
        check(radius > max(map(abs, flow)), 'all fixture curvatures must vanish')
        goals[name] = dict(intervals=[[str(x-radius), str(x+radius)] for x in flow],
                           potentials=['1'] * 7 + ['0'], factor='0', radius='0')
    payload['goal_bounds'] = goals
    after = verify(payload)
    check(after['optimum_interval'] == after['scenario_interval'] == (flow[9], flow[9]),
          'cut goal must give singleton bridge interval despite positive energy gap')
    check(after['scenario_loss_upper'] == 0 and all(after['goal_bounds_used'].values()),
          'goal bounds were not applied to both physical states')
    controls = [(['goal_bounds'], None), (['goal_bounds'], {}),
                (['goal_bounds', 'envelope', 'w'], ['0'] * 10),
                (['goal_bounds', 'envelope', 'potentials', 0], '2'),
                (['goal_bounds', 'scenario', 'potentials', 0], '2'),
                (['goal_bounds', 'envelope', 'factor'], '-1'),
                (['goal_bounds', 'envelope', 'radius'], '-1'),
                (['goal_bounds', 'envelope', 'intervals', 0], ['0']),
                (['goal_bounds', 'envelope', 'intervals', 0], ['0', '0']),
                (['goal_bounds', 'envelope', 'potentials'], []),
                (['goal_bounds', 'scenario', 'radius'], 0)]
    script = str(Path(__file__).with_name('certified_envelope.py'))
    count = 0
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / 'goal.json'
        for flags in (['-S'], ['-S', '-O']):
            path.write_text(json.dumps(payload))
            result = subprocess.run([sys.executable, *flags, script, 'verify', str(path)], capture_output=True)
            check(result.returncode == 0, result.stderr.decode())
            for indices, value in controls:
                bad = copy.deepcopy(payload)
                dest = bad
                for index in indices[:-1]:
                    dest = dest[index]
                dest[indices[-1]] = value
                path.write_text(json.dumps(bad))
                result = subprocess.run([sys.executable, *flags, script, 'verify', str(path)], capture_output=True)
                check(result.returncode != 0, 'malformed integrated goal witness accepted')
                count += 1
    print(f'Positive-gap, zero-curvature bridge goal integration passed; {count} malformed goal rejections.')


if __name__ == '__main__':
    run()
    goal_integration_audit()
    if '--producer' in sys.argv:
        producer_scaling_audit()
