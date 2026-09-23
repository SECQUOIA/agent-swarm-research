#!/usr/bin/env python3
"""Distinct exact checks for Section 11, plus an optional numerical replay.

The quadratic optimum is computed in a supplied circulation basis, independently
of the implementation's node-potential saddle-point equations. These finite
checks supplement the manuscript proofs. Run with --numerical for the ambiguous
original-instance comparison; only that branch imports scientific packages.
"""
from fractions import Fraction as F
import itertools
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
CODE = ROOT / 'code/potential_flow_mpd'
sys.path.insert(0, str(CODE))
from envelope_rational_certificates import Certificate, verify_certificate, energy, law
from envelope_bregman_bounds import sharpen, divergence
from goal_flow_certificate import (optimal_goal_potentials, make_hessian,
                                   SupportCertificate, verify_support)


def require(test, message):
    if not test:
        raise RuntimeError(message)


def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), F(0))


def cycle_optimum(gram, linear):
    """Solve in independent cycle coordinates; None means an unbounded goal."""
    rows = [list(map(F, row)) + [F(rhs)] for row, rhs in zip(gram, linear)]
    size = len(linear)
    pivots = []
    for column in range(size):
        selected = next((i for i in range(len(pivots), size) if rows[i][column]), None)
        if selected is None:
            continue
        k = len(pivots)
        rows[k], rows[selected] = rows[selected], rows[k]
        divisor = rows[k][column]
        rows[k] = [value/divisor for value in rows[k]]
        for i in range(k+1, size):
            factor = rows[i][column]
            rows[i] = [a-factor*b for a, b in zip(rows[i], rows[k])]
        pivots.append(column)
    if any(not any(row[:size]) and row[size] for row in rows):
        return None
    solution = [F(0)]*size
    for i, column in reversed(list(enumerate(pivots))):
        solution[column] = rows[i][size] - dot(rows[i][column+1:size], solution[column+1:])
    return dot(linear, solution), solution


def projection_checks():
    cases = finite = obstructed = 0
    fixtures = [
        ([(0, 1), (1, 2), (0, 2), (2, 3), (0, 3)], 4,
         [[1, 1, -1, 0, 0], [0, 0, 1, 1, -1]]),
        ([(0, 1), (0, 1), (2, 3)], 5, [[1, -1, 0]]),
    ]
    for edges, n, cycles in fixtures:
        m = len(edges)
        require(len(cycles) == (2 if m == 5 else 1), 'fixture cycle dimension')
        for cycle in cycles:
            load = [0]*n
            for (u, v), x in zip(edges, cycle):
                load[u] += x
                load[v] -= x
            require(not any(load), 'fixture basis must conserve')
        for hraw in itertools.product([0, 1, 2], repeat=m):
            h = list(map(F, hraw))
            goals = [[F(int(e == 0)) for e in range(m)],
                     [F((e+1)*(-1)**e) for e in range(m)],
                     [F(u-v) for u, v in edges]]
            gram = [[sum((he*a*b for he, a, b in zip(h, c1, c2)), F(0))
                     for c2 in cycles] for c1 in cycles]
            for w in goals:
                linear = [dot(w, c) for c in cycles]
                independent = cycle_optimum(gram, linear)
                try:
                    v = optimal_goal_potentials(edges, n, w, h)
                except ValueError:
                    require(independent is None, 'finite cycle optimum rejected')
                    obstructed += 1
                else:
                    require(independent is not None, 'unbounded cycle goal accepted')
                    residual = [we-v[u]+v[z] for we, (u, z) in zip(w, edges)]
                    require(all(s == 0 for s, he in zip(residual, h) if he == 0),
                            'zero-edge equality failed')
                    factor = sum((s*s/he for s, he in zip(residual, h) if he), F(0))
                    require(factor == independent[0], 'node and cycle optimal factors disagree')
                    d = [sum((alpha*c[e] for alpha, c in zip(independent[1], cycles)), F(0))
                         for e in range(m)]
                    require(dot(w, d) == factor and dot(h, [x*x for x in d]) == factor,
                            'sharpness circulation identities failed')
                    finite += 1
                cases += 1
    return dict(cases=cases, finite=finite, zero_curvature_obstructions=obstructed)


def support_checks():
    cases = 0
    for length in [1, 2, 8, 32]:
        edges, paths, next_node = [], [], 2
        for _ in range(2):
            nodes = [0] + list(range(next_node, next_node+length-1)) + [1]
            next_node += length-1
            paths.append(nodes)
            edges.extend(zip(nodes[:-1], nodes[1:]))
        b = [F(2), F(-2)] + [F(0)]*(next_node-2)
        c = [F(1)]*len(edges)
        for eps in [F(1, 10), F(1, 1000)]:
            y = [1+eps]*length + [1-eps]*length
            require(energy(y, c, c)-F(2*length, 3) == 2*length*eps**2,
                    'exact path energy gap')
            for sign in [1, -1]:
                w = [F(sign)] + [F(0)]*(len(edges)-1)
                t = [1+sign*eps]*length + [1-sign*eps]*length
                lam = 1/(4*length*eps)
                v = [None]*next_node
                v[0] = F(0)
                for k, nodes in enumerate(paths):
                    for j, (u, z) in enumerate(zip(nodes[:-1], nodes[1:])):
                        e = k*length+j
                        candidate = v[u]-w[e]+lam*t[e]**2
                        require(v[z] is None or v[z] == candidate, 'potential cycle consistency')
                        v[z] = candidate
                roots = [lam*x**3 for x in t]
                cert = SupportCertificate(lam, v, roots, F(sign)+eps)
                verify_support(edges, b, c, c, y, w, cert)
                require(dot(w, t) == cert.upper, 'support equality witness')
                cases += 1
    require(divergence(F(11, 10), F(9, 10), F(1), F(1)) == F(29, 750) > F(1, 50),
            'support endpoint versus physical Bregman distinction')
    return dict(exact_upper_and_lower_support_witnesses=cases,
                support_bregman_counterexample='29/750 > 1/50')


def saved_comparison():
    payload = json.loads((CODE/'envelope_certificate_example.json').read_text())
    edges = payload['edges']
    b, cp, cm = [list(map(F, payload[k])) for k in ['b', 'positive', 'negative']]
    cert = Certificate(*[list(map(F, payload[k])) for k in ['flow', 'potentials', 'root_upper']],
                       F(payload['gap']), F(payload['radius']))
    verify_certificate(edges, b, cp, cm, cert)
    intervals = sharpen(cp, cm, cert)
    rows = []
    for e, (lo, hi) in enumerate(intervals):
        w = [F(int(j == e)) for j in range(len(edges))]
        hc = make_hessian(edges, b, cp, cm, cert, w)
        rows.append(dict(edge=e, bregman_width=hi-lo, laplacian_width=2*hc.radius,
                         edge_drop_width=law(hi, cp[e], cm[e])-law(lo, cp[e], cm[e])))
    require(2*cert.radius < F('0.0003405'), 'printed uniform enclosure bound')
    require(max(row['bregman_width'] for row in rows) < F('0.000002894'), 'printed Bregman bound')
    require(max(row['laplacian_width'] for row in rows) < F('0.0000009447'), 'printed Laplacian bound')
    require(max(row['edge_drop_width'] for row in rows) < F('0.000004'), 'printed edge-drop bound')
    require(all(lo > 0 or hi < 0 for lo, hi in intervals), 'saved signs')
    return dict(uniform_width=2*cert.radius, edges=rows)


def numerical_comparison():
    from copy import deepcopy
    from certified_envelope import solve, verify
    from certified_envelope_benchmarks import ambiguous_instance
    payload, with_goal, status = solve(ambiguous_instance())
    without = deepcopy(payload)
    without.pop('goal_bounds')
    plain = verify(without)
    widths = [(report['optimum_interval'][1]-report['optimum_interval'][0])
              for report in [plain, with_goal]]
    losses = [report['scenario_loss_upper'] for report in [plain, with_goal]]
    require(not with_goal['scenario_exactly_optimal'], 'ambiguous case must retain scope')
    require(F(113) < widths[0]/widths[1] < F(115), 'printed width improvement')
    require(F(130) < losses[0]/losses[1] < F(132), 'printed loss improvement')
    return dict(status=status, exact_payload=payload,
                bregman_only=plain, with_goal=with_goal,
                width_ratio=widths[0]/widths[1], loss_ratio=losses[0]/losses[1])


if __name__ == '__main__':
    result = dict(projection=projection_checks(), support=support_checks(), saved=saved_comparison())
    if '--numerical' in sys.argv:
        result['numerical'] = numerical_comparison()
    print(json.dumps(result, default=str, indent=2))
