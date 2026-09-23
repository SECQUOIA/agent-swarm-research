"""Independent finite audit of the candidate quadratic-lift upper certificate.

Exact vertex inequalities validate the displayed quadratic dual expression
on selected boxes. LPs select full-box moment distributions; their weights,
equations, and objective bounds are then checked with exact fractions.
These finite checks supplement, and do not replace, the universal proof.
"""

from fractions import Fraction as Q
from itertools import product
import json
from pathlib import Path

import numpy as np
from scipy.optimize import linprog


def main():
    points = [Q(-1), Q(-1, 2), Q(0), Q(1, 2), Q(1)]
    intervals = [(a, b) for a in points for b in points if a <= b]
    checked = 0
    boxes = 0
    # q = 3h/2 - sign/2 * [u(x_k-a_k)+a_k(x_i*x_j-a_i*a_j)]
    # objective-corner+3h/2 = q-sign/2*(e2+a_k*e1).
    for bounds in product(intervals, repeat=3):
        a, b, c = [entry[0] for entry in bounds]
        h = max(hi - lo for lo, hi in bounds)
        boxes += 1
        for x, y, z, u, v in product(*bounds, (-1, 1), (-1, 1)):
            e1, e2 = u - x*y, v - u*z
            for sign in (-1, 1):
                q = 3*h/2 - sign*(u*(z-c)+c*(x*y-a*b))/2
                lhs = sign*(a*b*c-v)/2 + 3*h/2
                assert q >= 0
                assert lhs == q-sign*(e2+c*e1)/2
                checked += 1

    lp_count = outside_graph = strict_graph_gap = 0
    examples = []
    narrow = [(Q(-1), Q(-1, 2)), (Q(-1, 2), Q(0)),
              (Q(0), Q(1, 2)), (Q(1, 2), Q(1)),
              (Q(-1, 2), Q(1, 2))]
    for bounds in product(narrow, repeat=3):
        vertices = list(product(*bounds, (-1, 1), (-1, 1)))
        a, b, c = [entry[0] for entry in bounds]
        h = max(hi-lo for lo, hi in bounds)
        rows = [[Q(1) for _ in vertices],
                [u-x*y for x, y, z, u, v in vertices],
                [v-u*z for x, y, z, u, v in vertices]]
        for sign in (-1, 1):
            objective = [(1-sign*v)/Q(2) for x, y, z, u, v in vertices]
            solved = linprog(np.array(objective, dtype=float),
                             A_eq=np.array(rows, dtype=float),
                             b_eq=[1, 0, 0], bounds=(0, None), method="highs")
            assert solved.success
            weights = [Q(float(w)).limit_denominator(10**6) for w in solved.x]
            assert all(w >= 0 for w in weights)
            assert [sum(w*q for w, q in zip(weights, row)) for row in rows] == [1, 0, 0]
            value = sum(w*q for w, q in zip(weights, objective))
            assert value >= (1-sign*a*b*c)/2-3*h/2
            graph_min = min((1-sign*x*y*z)/2 for x, y, z in product(*bounds))
            nongraph = any(w and (u != x*y or v != u*z)
                           for w, (x, y, z, u, v) in zip(weights, vertices))
            outside_graph += bool(nongraph)
            strict_graph_gap += value < graph_min
            lp_count += 1
            if value < graph_min and len(examples) < 3:
                examples.append({"box": [[str(a), str(b)] for a, b in bounds],
                                 "sign": sign, "moment_value": str(value),
                                 "graph_minimum": str(graph_min),
                                 "support": [{"point": list(map(str, vertex)),
                                              "weight": str(w)}
                                             for w, vertex in zip(weights, vertices) if w]})
    result = {"status": "PASS", "exact_box_cases": boxes,
              "exact_quadratic_vertex_identities_and_inequalities": checked,
              "exactly_reconstructed_lp_distributions": lp_count,
              "distributions_with_support_outside_graph": outside_graph,
              "values_strictly_below_node_graph_optimum": strict_graph_gap,
              "examples": examples,
              "scope": "Finite checks, including degenerate boxes and non-graph-supported moment realizations; the universal certificate requires its analytic proof."}
    Path(__file__).with_suffix('.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'examples'}, indent=2))


if __name__ == '__main__':
    main()
