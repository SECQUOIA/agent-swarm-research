"""Exact diagnostics for TU filtration with disconnected coordinate domains.

This exercises the added union representation and its proof obligations.
It is not a second implementation of the full tree-DP/LP solver.
"""
from fractions import Fraction as Q
from itertools import combinations, product
from math import isqrt
import json
from pathlib import Path
import sympy as sp


def merge(intervals):
    answer = []
    for a, b in sorted(intervals):
        if answer and a <= answer[-1][1]:
            answer[-1] = (answer[-1][0], max(answer[-1][1], b))
        else:
            answer.append((a, b))
    return answer


def refine(intervals):
    return sorted({k for a, b in intervals for k in range(2*a, 2*b+1)})


def filter_cells(nodes, marginals, threshold):
    kept = []
    for i, a in enumerate(nodes):
        if marginals.get(a, threshold+1) <= threshold:
            kept.append((a, a))
        if i+1 < len(nodes) and nodes[i+1] == a+1:
            b = nodes[i+1]
            if min(marginals.get(a, threshold+1),
                   marginals.get(b, threshold+1)) <= threshold:
                kept.append((a, b))
    return merge(kept)


def contains(intervals, point):
    return any(a <= point <= b for a, b in intervals)


def ceil_sqrt(integer):
    root = isqrt(integer)
    return root + (root*root < integer)


def block_runs():
    results = []
    for blocks in (1, 4, 16):
        domains = [[0, 1] for _ in range(3)]
        max_states = 0
        full_witnesses = 0
        trace = []
        # The true set-growth constant is 1/6; L=12, kappa=72.
        bound = 2*(5+ceil_sqrt(4*3*blocks*72))
        for stage in range(13):
            denominator = 1 << stage
            xs, ts, zs = domains
            ts_set = set(ts)
            marginals = [{}, {}, {}]
            values = []
            for x, z in product(xs, zs):
                t = z-x
                if t not in ts_set:
                    continue
                numerator = 4*(2*x-z)**2 + z*(denominator-z)
                assert numerator >= 0
                full_witnesses += 1
                values.append(numerator)
                for i, a in enumerate((x, t, z)):
                    marginals[i][a] = min(marginals[i].get(a, numerator), numerator)
            assert min(values) == 0
            # 4*q^2 times the full m-block error n_c*12/(8*q^2).
            threshold = 18*blocks
            kept = [filter_cells(nodes, marginal, threshold)
                    for nodes, marginal in zip(domains, marginals)]
            for i in range(3):
                optima = (Q(0), Q(denominator, 2)) if i < 2 else (Q(0), Q(denominator))
                for optimum in optima:
                    assert contains(kept[i], optimum)
                # Every retained endpoint lies within a_j+h of S_i.
                for a, b in kept[i]:
                    for endpoint in (a, b):
                        distance = min(abs(endpoint-optimum) for optimum in optima)
                        if distance > 1:
                            assert (distance-1)**2 <= Q(3*blocks*72, 4)
            sizes = [len(nodes) for nodes in domains]
            max_states = max(max_states, *sizes)
            if stage > 0:
                assert max(sizes) <= bound
            trace.append({"stage": stage, "union_states": sizes,
                          "hull_z_states": denominator+1,
                          "z_components_after_filter": len(kept[2])})
            domains = [refine(intervals) for intervals in kept]
        assert trace[-1]["z_components_after_filter"] == 2
        assert trace[-1]["union_states"][2] < trace[-1]["hull_z_states"]
        results.append({"blocks": blocks, "optimum_count": 2**blocks,
                        "proved_state_bound": bound, "observed_max_states": max_states,
                        "feasible_grid_witnesses": full_witnesses, "trace": trace})
    return results


def original_objective(v):
    x, t, z = v
    return (2*x-z)**2 + z*(1-z)/4


def feasible_corner_distribution(point, corners):
    target = sp.Matrix([1]+[sp.Rational(v.numerator, v.denominator) for v in point])
    for count in range(1, min(4, len(corners))+1):
        for chosen in combinations(corners, count):
            matrix = sp.Matrix([[1]*count] + [[v[i] for v in chosen] for i in range(3)])
            if matrix.rank() < count:
                continue
            try:
                solution, parameters = matrix.gauss_jordan_solve(target)
            except ValueError:
                continue
            if parameters.rows:
                continue
            weights = [Q(int(a.p), int(a.q)) for a in solution]
            if min(weights) >= 0:
                return list(zip(weights, chosen))
    raise AssertionError(("No feasible mean-preserving corner distribution", point, corners))


def disconnected_rounding():
    domains = [[(Q(0), Q(1, 4)), (Q(1, 2), Q(3, 4))]]*2
    domains += [[(Q(0), Q(1, 4)), (Q(1, 2), Q(1))]]
    h = Q(1, 4)
    fine = [[Q(i, 16) for i in range(17) if contains(intervals, Q(i, 16))]
            for intervals in domains]
    count = 0
    strict_gap_count = 0
    for x, t in product(fine[0], fine[1]):
        z = x+t
        if z not in fine[2]:
            continue
        point = (x, t, z)
        coordinate_corners = []
        for coordinate, intervals in zip(point, domains):
            quotient = coordinate/h
            lower = quotient.numerator//quotient.denominator
            upper = -(-quotient.numerator//quotient.denominator)
            corners = sorted({lower*h, upper*h})
            assert all(contains(intervals, a) for a in corners)
            coordinate_corners.append(corners)
        corners = [v for v in product(*coordinate_corners) if v[0]+v[1] == v[2]]
        distribution = feasible_corner_distribution(point, corners)
        assert sum(weight for weight, _ in distribution) == 1
        for i in range(3):
            assert sum(weight*v[i] for weight, v in distribution) == point[i]
        expected = sum(weight*original_objective(v) for weight, v in distribution)
        allowance = 3*Q(12)*h*h/8
        assert expected <= original_objective(point)+allowance
        count += 1
        strict_gap_count += expected > original_objective(point)
    return {"feasible_points": count, "strict_positive_rounding_errors": strict_gap_count}


def premature_recovery_rejection():
    # On x=t in the unit square, F=x-x^2 has f*=0 at (0,0),(1,1).
    # Selecting only the equality at y=(1/2,1/2) returns the nonglobal
    # stationary point. An isolated exact value must govern acceptance.
    x, t, multiplier = sp.symbols("x t multiplier")
    solution = sp.solve([x-t, 1-2*x-multiplier, multiplier],
                        (x, t, multiplier), dict=True)[0]
    recovered_value = solution[x]-solution[x]**2
    assert solution[x] == solution[t] == sp.Rational(1, 2)
    assert recovered_value == sp.Rational(1, 4)
    assert recovered_value != 0
    return {"nonglobal_stationary_value": str(recovered_value),
            "isolated_global_value": "0", "accepted": False}


def main():
    results = {"status": "passed", "block_union_runs": block_runs(),
               "disconnected_TU_rounding": disconnected_rounding(),
               "premature_recovery": premature_recovery_rejection(),
               "scope": "Exact research diagnostics; no full DP/LP benchmark or CI checks."}
    destination = Path(__file__).with_name("nonunique-tu-results.json")
    destination.write_text(json.dumps(results, indent=2)+"\n")
    print(json.dumps({"status": results["status"],
                      "block_runs": len(results["block_union_runs"]),
                      "last_stage_comparisons": [
                          {"blocks": r["blocks"], **r["trace"][-1]}
                          for r in results["block_union_runs"]],
                      "disconnected_TU_rounding": results["disconnected_TU_rounding"],
                      "premature_recovery": results["premature_recovery"]}, indent=2))


if __name__ == "__main__":
    main()

