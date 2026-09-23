"""Bounded integration benchmarks and adversarial original-instance controls."""
import copy
import itertools
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time

import numpy as np
from certified_envelope import envelope, solve, verify
from series_parallel_envelope_checks import physical


def instance(k, sense='max', ratio=1, tiny=False, branch=False, zero=False):
    edges = [[0, i] for i in range(2, k + 2)] + [[i, 1] for i in range(2, k + 2)]
    if branch:
        edges += [[0, k + 2], [k + 2, k + 3], [k + 3, 0]]
    n = k + 4 if branch else k + 2
    b = ['0'] * n
    b[0], b[1] = ('0', '0') if zero else (('1/100000000', '-1/100000000') if tiny else ('1', '-1'))
    if not tiny and not zero and k > 3:
        for i in range(2, k + 2):
            b[i] = str((i % 3) - 1)
        b[1] = str(-sum(map(int, b[:1] + b[2:])))
    resistances = []
    for e in range(len(edges)):
        base = ratio if e % 3 == 0 else 1
        resistances.append({'values': [str(base), str(2 * base), str(3 * base)]}
                           if e % 2 else {'interval': [str(base), str(3 * base)]})
    for e in range(1, len(edges), 3):
        edges[e].reverse()
    return {'edges': edges, 'b': b, 'resistances': resistances, 'target': 0, 'sense': sense}


def ambiguous_instance():
    # An exact rational potential state with zero flows on coefficient-switching
    # edges. Its loads are constructed from square drops under the envelope.
    from fractions import Fraction as F
    from math import isqrt
    data = instance(3)
    data['resistances'] = [{'interval': ['1', '4']} for _ in data['edges']]
    edges, b, lower, upper, cp, cm, signs = envelope(data)
    potentials = [F(0), F(-4), F(0), F(0), F(-4)]
    b = [F(0)] * 5
    for e, (u, v) in enumerate(edges):
        drop = potentials[u] - potentials[v]
        square = abs(drop) / (cp[e] if drop >= 0 else cm[e])
        x = F(isqrt(square.numerator), isqrt(square.denominator))
        if x*x != square:
            raise RuntimeError('Fixture must have rational exact flow')
        if drop < 0:
            x = -x
        b[u] += x
        b[v] -= x
    data['b'] = list(map(str, b))
    return data


def run():
    rows = []
    fixtures = [('small_max', instance(3)), ('small_min', instance(3, 'min')),
                ('rank14', instance(15)), ('rank39', instance(40)),
                ('ratio1e6', instance(15, ratio=10**6)),
                ('near_zero', instance(15, tiny=True)),
                ('zero_adjoint_block', instance(5, branch=True)),
                ('zero_nomination', instance(5, zero=True)),
                ('ambiguous_active_signs', ambiguous_instance()),
                ('water_topology_quadratic_adaptation', json.loads(Path(__file__).with_name(
                    'certified_envelope_water_topology_instance.json').read_text()))]
    saved = None
    for name, data in fixtures:
        start = time.perf_counter()
        try:
            payload, report, status = solve(data)
            elapsed = time.perf_counter() - start
            start = time.perf_counter()
            verify(payload)
            verification_seconds = time.perf_counter() - start
            lo, hi = report['optimum_interval']
            row = dict(case=name, edges=len(data['edges']), solve_and_verify_seconds=round(elapsed, 3),
                       verify_seconds=round(verification_seconds, 3), status=status,
                       target_width=float(hi-lo),
                       bregman_target_width=float(report['bregman_optimum_interval'][1] - report['bregman_optimum_interval'][0]),
                       goal_bounds_used=report['goal_bounds_used'],
                       loss_bound=float(report['scenario_loss_upper']),
                       exact_endpoint_optimum=report['scenario_exactly_optimal'],
                       unresolved_signs=report['unresolved_envelope_signs'])
            if name.startswith('small'):
                edges, b, lower, upper, cp, cm, signs = envelope(data)
                A = np.zeros((len(b), len(edges)))
                for e, (u, v) in enumerate(edges):
                    A[u, e], A[v, e] = 1., -1.
                values = []
                for beta in itertools.product(*zip(lower, upper)):
                    coef = np.array(list(map(float, beta)))
                    values.append(physical(A, np.array(list(map(float, b))), coef, coef)[0])
                reference = max(values) if data['sense'] == 'max' else min(values)
                if not float(lo)-1e-10 <= reference <= float(hi)+1e-10:
                    raise RuntimeError('Exhaustive endpoint result outside certified interval')
                row['exhaustive_endpoint_scenarios'] = len(values)
            if name == 'ambiguous_active_signs' and not lo <= 0 <= hi:
                raise RuntimeError('Known exact zero target outside certified interval')
            if name == 'zero_adjoint_block':
                if report['adjoint_signs'][-3:] != [0, 0, 0]:
                    raise RuntimeError('Dangling cyclic block must have exact zero adjoint')
            if name == 'small_max':
                saved = payload
        except Exception as exc:
            row = dict(case=name, failure=type(exc).__name__ + ': ' + str(exc))
        rows.append(row)
        print(json.dumps(row), flush=True)
    if saved is None:
        raise RuntimeError('No basic certificate produced')
    corruptions = []
    for name in ['target', 'sense', 'resistance', 'nomination', 'gap', 'scenario',
                 'K4', 'disconnected', 'parallel', 'loop', 'float', 'unknown', 'bool',
                 'goal_radius', 'goal_factor', 'goal_intervals']:
        bad = copy.deepcopy(saved)
        data = bad['instance']
        if name == 'target': data['target'] = 100
        elif name == 'sense': data['sense'] = 'maximum'
        elif name == 'resistance': data['resistances'][0] = {'interval': ['0', '1']}
        elif name == 'nomination': data['b'][0] = '2'
        elif name == 'gap': bad['envelope']['gap'] = '-1'
        elif name == 'scenario': bad['scenario']['resistances'][0] = '2'
        elif name == 'K4': data['b'] = ['0']*4; data['edges'] = [list(e) for e in itertools.combinations(range(4), 2)]
        elif name == 'disconnected': data['b'] += ['0']
        elif name == 'parallel': data['edges'][1] = data['edges'][0][:]
        elif name == 'loop': data['edges'][0] = [0, 0]
        elif name == 'float': data['b'][0] = 1.0
        elif name == 'unknown': data['capacity'] = ['1']*6
        elif name == 'bool': data['target'] = True
        elif name == 'goal_radius': bad['goal_bounds']['envelope']['radius'] = '0'
        elif name == 'goal_factor': bad['goal_bounds']['scenario']['factor'] = '-1'
        elif name == 'goal_intervals': bad['goal_bounds']['envelope']['intervals'][0] = ['0', '0']
        corruptions.append((name, bad))
    script = str(Path(__file__).with_name('certified_envelope.py'))
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory)/'certificate.json'
        path.write_text(json.dumps(saved))
        good = subprocess.run([sys.executable, '-S', '-O', script, 'verify', str(path)], capture_output=True)
        if good.returncode:
            raise RuntimeError(good.stderr.decode())
        for name, bad in corruptions:
            path.write_text(json.dumps(bad))
            result = subprocess.run([sys.executable, '-S', '-O', script, 'verify', str(path)], capture_output=True)
            if result.returncode == 0:
                raise RuntimeError('Accepted corruption: ' + name)
    Path(__file__).with_name('certified_envelope_example.json').write_text(json.dumps(saved, indent=2)+'\n')
    Path(__file__).with_name('certified_envelope_benchmark_results.json').write_text(json.dumps(rows, indent=2)+'\n')
    failures = [row for row in rows if 'failure' in row]
    if failures:
        raise RuntimeError('Benchmark failures: ' + json.dumps(failures))
    print('128 exhaustive endpoint scenarios; 16 malformed inputs rejected under -S -O; valid certificate checked without site packages.')


if __name__ == '__main__':
    run()
