"""Connect the K4/Fibonacci section obstructions to exact recovered cuts.

PYTHONPATH=code python -m network_simplex_compressed.integration
"""

from fractions import Fraction as F
import json
from types import SimpleNamespace as Point

import numpy as np

from network_simplex_compressed import CompressedNetworkSimplex, separate
from network_simplex_compressed.certificate import inequalities
from network_simplex_benchmarks.baselines import Instance, full_ef


def check(name, arcs, balances, point, free, expected_ratio):
    output = []
    for eliminate in (False, True):
        model = CompressedNetworkSimplex(arcs, balances, len(point.y), point.z,
                                        eliminate_observed=eliminate)
        certificate = separate(model, point)
        assert certificate.status == "certified_outside", certificate
        cut = certificate.cut
        ratio = cut.coefficients[("z", *free[0])]/cut.coefficients[("z", *free[1])]
        assert ratio == expected_ratio
        assert cut.evaluate(point) > 0
        # Recheck the returned multipliers independently of the recovery path.
        cancellation = {}
        rows = inequalities(model)
        for row, weight in certificate.multipliers:
            assert weight >= 0
            for k, value in rows[row][0].items():
                if k >= model.original_n:
                    cancellation[k] = cancellation.get(k, F(0))+weight*value
        assert not any(cancellation.values())
        E, m = len(arcs), len(point.y)
        objective = np.zeros(model.original_n)
        for key, value in cut.coefficients.items():
            k = key[1] if key[0] == "x" else E+key[1] if key[0] == "y" else E+m+model.observations.index(key[1:])
            objective[k] = -float(value)
        baseline = Instance(arcs, -np.asarray(balances, dtype=float), m, list(model.observations),
                            np.asarray(point.x, dtype=float))
        optimum = full_ef(baseline, objective)
        assert optimum.success and -optimum.fun+float(cut.constant) < 1e-8
        output.append(dict(instance=name, eliminate_observed=eliminate,
                           auxiliary_variables=model.n-model.original_n,
                           product_coefficient_ratio=str(ratio), exact_violation=str(cut.evaluate(point)),
                           reconstruction=certificate.reconstruction))
    return output


def main():
    arcs = [(1, 2, 1), (1, 3, 1), (2, 3, 1), (0, 1, 1), (0, 2, 1), (0, 3, 1)]
    balances = [F(-3, 2), F(-1, 2), F(1, 2), F(3, 2)]
    observed = [(0, 0), (1, 0), (4, 0), (0, 1), (5, 1), (2, 2), (3, 2)]
    z = {key: F(1, 8) for key in observed}; z[0, 0] -= F(1, 1024)
    point = Point(x=(F(5, 8), F(1, 2), F(5, 8), F(5, 8), F(1, 2), F(3, 8)),
                  y=(F(1, 4),)*3, z=z)
    report = check("K4 sharp rank-three section", arcs, balances, point, [(0, 0), (1, 0)], F(2))
    for q in (5, 8):
        n = 2*q-1
        columns = [{q, 0}, {q, 1}]
        for i in range(2, q):
            columns.extend([{q+i-1, i}, {q+i-1, i-1, i-2}])
        columns.append({q-1, q-2})
        c, a = F(1, 8*n), F(1, 2*n)
        arcs = [(i, i+1, 1) for i in range(n) for _ in range(2)] + [(0, n, 1)]
        z = {(2*i, j): c for j, column in enumerate(columns) for i in column}
        x = []
        for i in range(n):
            degree = sum(i in column for column in columns)
            value = (n-degree)*a+degree*c
            x.extend([value, F(1, 2)-value])
        x.append(F(1, 2))
        fibonacci = [1, 1]
        for i in range(2, q):
            fibonacci.append(sum(fibonacci[-2:]))
        free = [(2*(q-1), n-1), (0, 0)]
        z[free[0]] -= c/(100*(fibonacci[-1]+1))
        point = Point(x=x, y=(F(1, n),)*n, z=z)
        report.extend(check(f"Series-parallel Fibonacci q={q}", arcs, [-1]+[0]*(n-1)+[1],
                            point, free, F(fibonacci[-1])))
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
