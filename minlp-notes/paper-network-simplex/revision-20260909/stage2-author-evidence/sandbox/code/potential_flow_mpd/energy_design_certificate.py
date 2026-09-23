"""Standard-library exact checker for global quadratic energy design bounds.

The certificate describes the complete graph, nomination, positive resistance
box and additional polytope inequalities. It certifies an original resistance
profile's additive distance from maximum constitutive dissipation.
"""
from fractions import Fraction as F
import argparse
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def rational(value):
    require(type(value) in (int, str), 'rationals must be integer or exact string values')
    try:
        return F(value)
    except (ValueError, ZeroDivisionError) as error:
        raise ValueError('invalid exact rational') from error


def vector(value, length, label):
    require(type(value) is list and len(value) == length, label+' has wrong length')
    return [rational(x) for x in value]


def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), F(0))


def verify(data):
    fields = {'format', 'edges', 'nominations', 'beta_lower', 'beta_upper',
              'polytope_rows', 'polytope_rhs', 'profile', 'potentials',
              'trial_flow', 'dual_multipliers', 'root_upper', 'tolerance'}
    require(type(data) is dict and set(data) == fields, 'invalid certificate fields')
    require(data['format'] == 'quadratic-energy-design-v1', 'invalid format')
    require(type(data['nominations']) is list and len(data['nominations']) >= 1,
            'nonempty nomination vector required')
    n = len(data['nominations'])
    b = vector(data['nominations'], n, 'nominations')
    require(sum(b) == 0, 'nominations must be balanced')
    edges = data['edges']
    require(type(edges) is list, 'edges must be a list')
    neighbors = [set() for _ in range(n)]
    for edge in edges:
        require(type(edge) is list and len(edge) == 2, 'invalid edge')
        u, v = edge
        require(type(u) is int and type(v) is int and 0 <= u < n and 0 <= v < n and u != v,
                'invalid loopless edge endpoints')
        neighbors[u].add(v); neighbors[v].add(u)
    seen, pending = {0}, [0]
    while pending:
        u = pending.pop()
        for v in neighbors[u]-seen:
            seen.add(v); pending.append(v)
    require(len(seen) == n, 'graph must be connected')
    m = len(edges)
    lower = vector(data['beta_lower'], m, 'beta_lower')
    upper = vector(data['beta_upper'], m, 'beta_upper')
    require(all(0 < a <= z for a, z in zip(lower, upper)), 'invalid positive resistance box')
    extra = data['polytope_rows']
    require(type(extra) is list, 'polytope_rows must be a list')
    rows = [vector(row, m, 'polytope row') for row in extra]
    rhs = vector(data['polytope_rhs'], len(rows), 'polytope_rhs')
    # Multipliers refer first to all upper rows, then all lower rows,
    # then to the additional input rows in their supplied order.
    identity = [[F(int(i == j)) for j in range(m)] for i in range(m)]
    rows = identity + [[-x for x in row] for row in identity] + rows
    rhs = upper + [-x for x in lower] + rhs
    beta = vector(data['profile'], m, 'profile')
    require(all(dot(row, beta) <= bound for row, bound in zip(rows, rhs)),
            'profile is outside the original polytope')
    y = vector(data['trial_flow'], m, 'trial_flow')
    balance = [F(0)]*n
    for (u, v), flow in zip(edges, y):
        balance[u] += flow; balance[v] -= flow
    require(balance == b, 'trial flow is not conserved')
    multipliers = vector(data['dual_multipliers'], len(rows), 'dual_multipliers')
    require(all(x >= 0 for x in multipliers), 'negative LP multiplier')
    weights = [abs(x)**3/3 for x in y]
    require(all(sum(multipliers[i]*rows[i][j] for i in range(len(rows))) == weights[j]
                for j in range(m)), 'LP dual equality fails')
    pi = vector(data['potentials'], n, 'potentials')
    roots = vector(data['root_upper'], m, 'root_upper')
    require(all(t >= 0 for t in roots), 'negative conjugate bound')
    require(all(be*t*t >= abs(pi[u]-pi[v])**3
                for (u, v), be, t in zip(edges, beta, roots)), 'conjugate inequality fails')
    lower_value = dot(b, pi)-F(2, 3)*sum(roots)
    upper_value = dot(rhs, multipliers)
    loss = 3*(upper_value-lower_value)
    tolerance = rational(data['tolerance'])
    require(tolerance >= 0 and 0 <= loss <= tolerance, 'claimed global loss tolerance fails')
    return {'global_dissipation_lower': str(3*lower_value),
            'global_dissipation_upper': str(3*upper_value),
            'selected_profile_lower': str(3*lower_value),
            'certified_suboptimality': str(loss)}


def demo():
    return {'format': 'quadratic-energy-design-v1', 'edges': [[0, 1], [1, 2], [0, 2]],
            'nominations': [1, 0, -1], 'beta_lower': [1, 1, 1], 'beta_upper': [4, 4, 4],
            'polytope_rows': [[1, 1, 1], [-1, -1, -1]], 'polytope_rhs': [6, -6],
            'profile': ['3/2', '3/2', 3], 'potentials': ['3/4', '3/8', 0],
            'trial_flow': ['1/2', '1/2', '1/2'],
            'dual_multipliers': [0, 0, 0, 0, 0, 0, '1/24', 0],
            'root_upper': ['3/16', '3/16', '3/8'], 'tolerance': 0}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', type=Path)
    parser.add_argument('--write-demo', type=Path)
    arguments = parser.parse_args()
    certificate = json.loads(arguments.verify.read_text()) if arguments.verify else demo()
    result = verify(certificate)
    if arguments.write_demo:
        require(arguments.verify is None, '--write-demo cannot modify an input certificate')
        arguments.write_demo.write_text(json.dumps(certificate, indent=2)+'\n')
    print(json.dumps(result, indent=2))
