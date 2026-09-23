"""Independent exact and malformed-input checks for the design certificate.

No numerical optimization is used. Run normally and with python -O.
"""
from copy import deepcopy
from fractions import Fraction as F
import json
from pathlib import Path
from random import Random
import subprocess
import sys
import tempfile

from energy_design_certificate import demo, verify


def check(condition, message):
    if not condition:
        raise RuntimeError(message)


def encode(values):
    return [str(value) for value in values]


def tree_certificate(rng, n, optimal):
    edges, flows, lower, upper, profile = [], [], [], [], []
    potentials, nominations = [F(0)] * n, [F(0)] * n
    for child in range(1, n):
        parent = rng.randrange(child)
        u, v = (parent, child) if rng.randrange(2) else (child, parent)
        flow = F(rng.randrange(-6, 7), rng.randrange(1, 5))
        lo = F(rng.randrange(1, 5), rng.randrange(1, 4))
        hi = lo + F(rng.randrange(1, 5), rng.randrange(1, 4))
        beta = hi if optimal else (lo + hi) / 2
        drop = beta * flow * abs(flow)
        potentials[child] = potentials[parent] - drop if u == parent else potentials[parent] + drop
        nominations[u] += flow
        nominations[v] -= flow
        edges.append([u, v])
        flows.append(flow)
        lower.append(lo)
        upper.append(hi)
        profile.append(beta)
    weights = [abs(flow) ** 3 / 3 for flow in flows]
    expected_upper = sum(hi * abs(flow) ** 3 for hi, flow in zip(upper, flows))
    expected_selected = sum(beta * abs(flow) ** 3 for beta, flow in zip(profile, flows))
    data = {
        'format': 'quadratic-energy-design-v1', 'edges': edges,
        'nominations': encode(nominations), 'beta_lower': encode(lower),
        'beta_upper': encode(upper), 'polytope_rows': [], 'polytope_rhs': [],
        'profile': encode(profile), 'potentials': encode(potentials),
        'trial_flow': encode(flows),
        'dual_multipliers': encode(weights + [F(0)] * len(edges)),
        'root_upper': encode([beta * abs(flow) ** 3 for beta, flow in zip(profile, flows)]),
        'tolerance': str(expected_upper - expected_selected),
    }
    result = verify(data)
    check(F(result['global_dissipation_upper']) == expected_upper, 'tree global upper mismatch')
    check(F(result['selected_profile_lower']) == expected_selected, 'tree physical lower mismatch')
    check(F(result['certified_suboptimality']) == expected_upper - expected_selected, 'tree gap mismatch')
    return data


def reject(data, label):
    try:
        verify(data)
    except (ValueError, TypeError, KeyError, OverflowError):
        return
    raise RuntimeError('accepted corrupt certificate: ' + label)


def main():
    rng = Random(910621)
    good = []
    for n in range(1, 13):
        for _ in range(4):
            good.append(tree_certificate(rng, n, True))
            good.append(tree_certificate(rng, n, False))
    sample = demo()
    result = verify(sample)
    check(result['global_dissipation_upper'] == '3/4', 'triangle upper')
    check(result['selected_profile_lower'] == '3/4', 'triangle lower')
    saved = json.loads(Path(__file__).with_name('energy_design_certificate_example.json').read_text())
    check(verify(saved) == result, 'saved example differs')
    good.extend([sample, saved])

    # Parallel arcs are mathematically valid, including reversed orientation.
    parallel = deepcopy(sample)
    parallel.update(edges=[[0, 1], [1, 0]], nominations=[1, -1],
                    beta_lower=[1, 1], beta_upper=[1, 1],
                    polytope_rows=[], polytope_rhs=[], profile=[1, 1],
                    potentials=['1/4', 0], trial_flow=['1/2', '-1/2'],
                    dual_multipliers=['1/24', '1/24', 0, 0],
                    root_upper=['1/8', '1/8'], tolerance=0)
    check(F(verify(parallel)['global_dissipation_upper']) == F(1, 4), 'parallel arc law')
    good.append(parallel)

    for original in list(good):
        shifted = deepcopy(original)
        shifted['potentials'] = encode([F(value) + F(719, 17) for value in original['potentials']])
        check(verify(shifted) == verify(original), 'potential gauge changed certificate')

    corrupt = []
    def changed(label, action):
        data = deepcopy(sample)
        action(data)
        corrupt.append((label, data))

    for field in sample:
        changed('missing ' + field, lambda d, field=field: d.pop(field))
    changed('extra field', lambda d: d.update(extra=0))
    changed('wrong format', lambda d: d.update(format='different'))
    numeric_vectors = ['nominations', 'beta_lower', 'beta_upper', 'polytope_rhs',
                       'profile', 'potentials', 'trial_flow', 'dual_multipliers', 'root_upper']
    for field in numeric_vectors:
        changed('short ' + field, lambda d, field=field: d[field].pop())
        changed('long ' + field, lambda d, field=field: d[field].append(0))
        for bad in [0.0, True, None, {}, [], 'NaN', 'Infinity', '1/0', 'bad']:
            changed('invalid numeric ' + field + ' ' + repr(bad),
                    lambda d, field=field, bad=bad: d[field].__setitem__(0, bad))
    for bad in [0.0, True, None, [], '1/0', 'NaN', -1]:
        changed('bad tolerance ' + repr(bad), lambda d, bad=bad: d.update(tolerance=bad))
    for bad in [[0, 0], [0, 3], [-1, 1], [True, 1], [0.0, 1], [0], [0, 1, 2], '01']:
        changed('bad edge ' + repr(bad), lambda d, bad=bad: d['edges'].__setitem__(0, bad))
    changed('disconnected graph', lambda d: d.update(edges=[[0, 1], [0, 1], [0, 1]]))
    changed('no vertices', lambda d: d.update(nominations=[]))
    changed('unbalanced nomination', lambda d: d['nominations'].__setitem__(0, 2))
    changed('nonconserved flow', lambda d: d['trial_flow'].__setitem__(0, 0))
    changed('zero beta lower', lambda d: d['beta_lower'].__setitem__(0, 0))
    changed('negative beta lower', lambda d: d['beta_lower'].__setitem__(0, -1))
    changed('reversed beta interval', lambda d: d['beta_lower'].__setitem__(0, 5))
    changed('profile outside box', lambda d: d['profile'].__setitem__(0, 5))
    changed('profile outside global row', lambda d: d['profile'].__setitem__(0, 2))
    changed('negative multiplier', lambda d: d['dual_multipliers'].__setitem__(0, -1))
    changed('dual equality mismatch', lambda d: d['dual_multipliers'].__setitem__(0, 1))
    changed('negative root', lambda d: d['root_upper'].__setitem__(0, '-3/16'))
    changed('root underestimated', lambda d: d['root_upper'].__setitem__(0, '3/32'))
    changed('invalid zero-gap claim', lambda d: d['root_upper'].__setitem__(0, 1))
    changed('weakened global upper invalidates gap', lambda d: d['polytope_rhs'].__setitem__(0, 7))
    changed('wrong polytope row width', lambda d: d['polytope_rows'][0].append(0))
    changed('float polytope coefficient', lambda d: d['polytope_rows'][0].__setitem__(0, 1.0))
    changed('invalid polytope rows', lambda d: d.update(polytope_rows={}))
    for label, data in corrupt:
        reject(data, label)
    for data in [None, [], 1, 'certificate']:
        reject(data, 'wrong top-level type')

    # CLI must reject the same corruption under normal and optimized Python.
    module = Path(__file__).with_name('energy_design_certificate.py')
    with tempfile.TemporaryDirectory() as temp:
        target = Path(temp) / 'certificate.json'
        for optimized in [False, True]:
            command = [sys.executable] + (['-O'] if optimized else []) + [str(module), '--verify', str(target)]
            target.write_text(json.dumps(sample))
            run = subprocess.run(command, capture_output=True, text=True)
            check(run.returncode == 0 and json.loads(run.stdout) == result, 'CLI rejected valid certificate')
            for label, data in corrupt:
                target.write_text(json.dumps(data))
                run = subprocess.run(command, capture_output=True, text=True)
                check(run.returncode != 0 and not run.stdout.strip(), 'CLI accepted corruption: ' + label)
    print(f'PASS: {len(good)} exact physical/global certificates and {len(good)} gauge shifts.')
    print(f'PASS: {len(corrupt) + 4} malformed direct inputs rejected; '
          f'{2 * len(corrupt)} normal/-O CLI corruptions rejected.')


if __name__ == '__main__':
    main()
