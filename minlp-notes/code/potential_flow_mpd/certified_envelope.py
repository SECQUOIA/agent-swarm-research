"""Original-instance envelope certificates. `verify` needs only Python stdlib.

Produce with `python certified_envelope.py solve instance.json certificate.json`;
check with `python -S certified_envelope.py verify certificate.json`.
Only connected simple, loopless, K4-minor-free graphs are supported here.
"""
import argparse
import json
from fractions import Fraction as F
from pathlib import Path

from envelope_rational_certificates import (
    Certificate, conserved_rounding, dyadic, law, make_certificate,
    require, verify_certificate,
)
from envelope_bregman_bounds import sharpen
from goal_flow_certificate import HessianCertificate, make_hessian, verify_hessian


def keys(value, expected, label):
    require(type(value) is dict and set(value) == set(expected), label + ' fields')


def rational(value):
    require(type(value) is str, 'rational values must be strings')
    try:
        return F(value)
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError('Invalid certificate: malformed rational') from exc


def rational_list(value):
    require(type(value) is list, 'rational vector must be a list')
    return [rational(x) for x in value]


def check_graph(edges, n):
    require(type(edges) is list and edges and n >= 2, 'nonempty graph')
    adjacency = [set() for _ in range(n)]
    for edge in edges:
        require(type(edge) is list and len(edge) == 2, 'edge pair')
        u, v = edge
        require(type(u) is int and type(v) is int and 0 <= u < n and
                0 <= v < n and u != v, 'loopless graph vertex indices')
        require(v not in adjacency[u], 'simple graph: no parallel edges')
        adjacency[u].add(v)
        adjacency[v].add(u)
    reached, stack = {0}, [0]
    while stack:
        for v in adjacency[stack.pop()] - reached:
            reached.add(v)
            stack.append(v)
    require(len(reached) == n, 'connected graph')
    # A connected graph is a partial 2-tree iff this reduction finishes.
    remaining = set(range(n))
    while remaining:
        vertex = next((v for v in sorted(remaining) if len(adjacency[v]) <= 2), None)
        require(vertex is not None, 'graph must be K4-minor-free')
        neighbors = sorted(adjacency[vertex])
        for v in neighbors:
            adjacency[v].remove(vertex)
        if len(neighbors) == 2:
            u, v = neighbors
            adjacency[u].add(v)
            adjacency[v].add(u)
        remaining.remove(vertex)
        adjacency[vertex].clear()


def exact_solve(matrix, rhs):
    """Rational elimination; intended for grounded positive definite Laplacians."""
    a = [[F(x) for x in row] + [F(y)] for row, y in zip(matrix, rhs)]
    n = len(a)
    for k in range(n):
        pivot = next((i for i in range(k, n) if a[i][k]), None)
        require(pivot is not None, 'nonsingular grounded Laplacian')
        a[k], a[pivot] = a[pivot], a[k]
        for i in range(k + 1, n):
            factor = a[i][k] / a[k][k]
            if factor:
                a[i][k] = F(0)
                for j in range(k + 1, n + 1):
                    a[i][j] -= factor * a[k][j]
    x = [F(0)] * n
    for i in reversed(range(n)):
        x[i] = (a[i][n] - sum(a[i][j] * x[j] for j in range(i + 1, n))) / a[i][i]
    return x


def envelope(instance):
    keys(instance, ['edges', 'b', 'resistances', 'target', 'sense'], 'instance')
    b = rational_list(instance['b'])
    edges = instance['edges']
    check_graph(edges, len(b))
    require(sum(b) == 0, 'balanced nominations')
    m, n = len(edges), len(b)
    target, sense = instance['target'], instance['sense']
    require(type(target) is int and 0 <= target < m, 'target index')
    require(sense in ('max', 'min'), 'extremum sense')
    data = instance['resistances']
    require(type(data) is list and len(data) == m, 'resistance dimensions')
    lower, upper = [], []
    for item in data:
        require(type(item) is dict and set(item) in ({'interval'}, {'values'}),
                'interval or finite resistance set')
        kind = next(iter(item))
        values = rational_list(item[kind])
        require(values and all(v > 0 for v in values), 'positive nonempty resistance set')
        if kind == 'interval':
            require(len(values) == 2 and values[0] <= values[1], 'ordered resistance interval')
        lower.append(min(values))
        upper.append(max(values))
    lap = [[F(0)] * n for _ in range(n)]
    for u, v in edges:
        lap[u][u] += 1
        lap[v][v] += 1
        lap[u][v] -= 1
        lap[v][u] -= 1
    q = [F(0)] * n
    u, v = edges[target]
    q[u], q[v] = F(1), F(-1)
    potentials = [F(0)] + exact_solve([row[1:] for row in lap[1:]], q[1:])
    signs = [(potentials[u] > potentials[v]) - (potentials[u] < potentials[v]) for u, v in edges]
    direction = 1 if sense == 'max' else -1
    status = [direction * sign for sign in signs]
    status[target] = -direction
    positive = [upper[e] if status[e] > 0 else lower[e] for e in range(m)]
    negative = [upper[e] if status[e] < 0 else lower[e] for e in range(m)]
    return edges, b, lower, upper, positive, negative, signs


def encode_certificate(cert):
    return {name: [str(x) for x in getattr(cert, name)]
            if name in ('flow', 'potentials', 'root_upper') else str(getattr(cert, name))
            for name in ('flow', 'potentials', 'root_upper', 'gap', 'radius')}


def decode_certificate(data):
    keys(data, ['flow', 'potentials', 'root_upper', 'gap', 'radius'], 'energy certificate')
    return Certificate(*(rational_list(data[name]) for name in ('flow', 'potentials', 'root_upper')),
                       rational(data['gap']), rational(data['radius']))


def encode_goal(cert):
    if cert is None:
        return None
    return {'intervals': [[str(lo), str(hi)] for lo, hi in cert.intervals],
            'potentials': [str(x) for x in cert.potentials],
            'factor': str(cert.factor), 'radius': str(cert.radius)}


def decode_goal(data):
    keys(data, ['intervals', 'potentials', 'factor', 'radius'], 'goal certificate')
    require(type(data['intervals']) is list, 'goal interval list')
    intervals = [rational_list(pair) for pair in data['intervals']]
    require(all(len(pair) == 2 for pair in intervals), 'goal interval pairs')
    return HessianCertificate(intervals, rational_list(data['potentials']),
                              rational(data['factor']), rational(data['radius']))


def target_goal(edges, b, cp, cm, base, target):
    w = [F(int(e == target)) for e in range(len(edges))]
    supply = sum(v for v in b if v > 0)
    if supply == 0:
        supply = F(1)
    scale = max(cp + cm)
    energy_scale = scale * supply**3
    normalized = Certificate(
        [x / supply for x in base.flow],
        [x / (scale * supply**2) for x in base.potentials],
        [x / energy_scale for x in base.root_upper],
        base.gap / energy_scale, base.radius / supply)
    try:
        goal = make_hessian(edges, [x / supply for x in b],
                            [x / scale for x in cp], [x / scale for x in cm],
                            normalized, w)
    except ValueError as exc:
        if 'goal must annihilate cycles supported entirely on zero-curvature edges' in str(exc):
            return None
        raise
    result = HessianCertificate(
        [(supply * lo, supply * hi) for lo, hi in goal.intervals],
        goal.potentials, goal.factor / (scale * supply), supply * goal.radius)
    verify_hessian(edges, b, cp, cm, base, w, result)
    return result


def intersect_goal(data, edges, b, cp, cm, base, target, interval):
    if data is None:
        return interval
    goal = decode_goal(data)
    w = [F(int(e == target)) for e in range(len(edges))]
    verify_hessian(edges, b, cp, cm, base, w, goal)
    center = base.flow[target]
    result = (max(interval[0], center - goal.radius), min(interval[1], center + goal.radius))
    require(result[0] <= result[1], 'consistent goal and Bregman intervals')
    return result


def verify(payload):
    """Recompute uncertainty mapping and return exact, independently checked claims."""
    fields = ['version', 'instance', 'envelope', 'scenario']
    keys(payload, fields + (['goal_bounds'] if 'goal_bounds' in payload else []), 'document')
    require(type(payload['version']) is int and payload['version'] == 1, 'format version')
    instance = payload['instance']
    edges, b, lower, upper, cp, cm, signs = envelope(instance)
    cert = decode_certificate(payload['envelope'])
    verify_certificate(edges, b, cp, cm, cert)
    bounds = sharpen(cp, cm, cert, steps=48)
    scenario = payload['scenario']
    keys(scenario, ['resistances', 'certificate'], 'scenario')
    beta = rational_list(scenario['resistances'])
    require(len(beta) == len(edges), 'scenario resistance dimensions')
    require(all(value in (lower[e], upper[e]) for e, value in enumerate(beta)),
            'scenario must use allowed endpoints')
    scenario_cert = decode_certificate(scenario['certificate'])
    verify_certificate(edges, b, beta, beta, scenario_cert)
    scenario_bounds = sharpen(beta, beta, scenario_cert, steps=48)
    compatible = all(cp[e] == cm[e] == beta[e] or
                     lo >= 0 and beta[e] == cp[e] or
                     hi <= 0 and beta[e] == cm[e] or
                     lo == hi == 0
                     for e, (lo, hi) in enumerate(bounds))
    target = instance['target']
    optimum, attained = bounds[target], scenario_bounds[target]
    goal_data = payload.get('goal_bounds', {'envelope': None, 'scenario': None})
    keys(goal_data, ['envelope', 'scenario'], 'goal bounds')
    optimum = intersect_goal(goal_data['envelope'], edges, b, cp, cm, cert, target, optimum)
    attained = intersect_goal(goal_data['scenario'], edges, b, beta, beta, scenario_cert, target, attained)
    raw_loss = optimum[1] - attained[0] if instance['sense'] == 'max' else attained[1] - optimum[0]
    require(raw_loss >= 0, 'consistent optimum and scenario enclosures')
    return {'optimum_interval': optimum, 'scenario_interval': attained,
            'scenario_loss_upper': F(0) if compatible else raw_loss,
            'scenario_exactly_optimal': compatible, 'adjoint_signs': signs,
            'bregman_optimum_interval': bounds[target],
            'goal_bounds_used': {name: value is not None for name, value in goal_data.items()},
            'unresolved_envelope_signs': sum(lo < 0 < hi for lo, hi in bounds)}


def numerical_certificate(edges, b, cp, cm, numerical=None):
    import numpy as np
    from envelope_socp_checks import conic_flow
    n, m = len(b), len(edges)
    A = np.zeros((n, m))
    for e, (u, v) in enumerate(edges):
        A[u, e], A[v, e] = 1., -1.
    status = 'reused feasible flow'
    if all(v == 0 for v in b):
        certificate = make_certificate(edges, b, cp, cm, [F(0)] * m, [F(0)] * n)
        return certificate, 'exact zero nomination'
    # Normalize both optimization and certification; then lift exactly. This
    # preserves relative certificate accuracy for very small nomination units.
    supply = sum(v for v in b if v > 0)
    scale = max(cp + cm)
    bn = [v / supply for v in b]
    cpn, cmn = [v / scale for v in cp], [v / scale for v in cm]
    if numerical is None:
        normalized, _, _, status = conic_flow(
            A, np.array(list(map(float, bn))),
            np.array(list(map(float, cpn))), np.array(list(map(float, cmn))))
    else:
        normalized = np.array([float(F(v) / supply) for v in numerical])
    require(np.all(np.isfinite(normalized)), 'finite numerical primal output')
    y = conserved_rounding(edges, bn, normalized, bits=96)
    drops = np.array([float(law(x, cpn[e], cmn[e])) for e, x in enumerate(y)])
    p = [dyadic(x, bits=96) for x in np.linalg.lstsq(A.T, drops, rcond=None)[0]]
    normalized_cert = make_certificate(edges, bn, cpn, cmn, y, p, bits=96)
    energy_scale = scale * supply**3
    certificate = Certificate(
        [supply * x for x in normalized_cert.flow],
        [scale * supply**2 * x for x in normalized_cert.potentials],
        [energy_scale * x for x in normalized_cert.root_upper],
        energy_scale * normalized_cert.gap, supply * normalized_cert.radius)
    verify_certificate(edges, b, cp, cm, certificate)
    return certificate, status


def solve(instance):
    edges, b, lower, upper, cp, cm, signs = envelope(instance)
    cert, status = numerical_certificate(edges, b, cp, cm)
    beta = [cp[e] if x >= 0 else cm[e] for e, x in enumerate(cert.flow)]
    # Reusing the feasible flow is safe: the second exact primal-dual check
    # certifies its error under the actual recovered endpoint scenario.
    scenario_cert, _ = numerical_certificate(edges, b, beta, beta,
                                             cert.flow)
    payload = {'version': 1, 'instance': instance, 'envelope': encode_certificate(cert),
               'scenario': {'resistances': [str(x) for x in beta],
                            'certificate': encode_certificate(scenario_cert)}}
    payload['goal_bounds'] = {
        'envelope': encode_goal(target_goal(edges, b, cp, cm, cert, instance['target'])),
        'scenario': encode_goal(target_goal(edges, b, beta, beta, scenario_cert, instance['target']))}
    return payload, verify(payload), status


def load(path):
    def distinct(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, 'duplicate JSON key')
            result[key] = value
        return result
    return json.loads(Path(path).read_text(), object_pairs_hook=distinct)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    checker = commands.add_parser('verify')
    checker.add_argument('certificate')
    producer = commands.add_parser('solve')
    producer.add_argument('instance')
    producer.add_argument('output')
    args = parser.parse_args()
    if args.command == 'verify':
        report = verify(load(args.certificate))
    else:
        payload, report, status = solve(load(args.instance))
        Path(args.output).write_text(json.dumps(payload, indent=2) + '\n')
        print('Numerical solver status:', status)
    print(json.dumps(report, default=str, indent=2))


if __name__ == '__main__':
    main()
