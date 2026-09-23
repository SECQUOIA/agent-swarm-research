"""Exact weighted-trace certificates for the fixed two-mode drift probe.

Latent transitions are diag(2/5,1/5), the observation row is (3/5,4/5),
and both latent marginal covariance and measurement variance have scale v.
JSON decimals specify exact rational sensitivities, prior, weight and scale.
"""

import argparse
from fractions import Fraction as Q
import hashlib
import json
from math import isqrt
from pathlib import Path
from time import perf_counter

import sympy as sp

from certify_noisy_markov import fraction, matrix, rational
from integer_interval_scores import IntegerIntervalScores


def integer(value, name, minimum=0):
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")
    return value


def psd_matrix(value, name, dimension=None):
    rows = matrix(value)
    if (any(len(row) != len(rows) for row in rows)
            or dimension is not None and len(rows) != dimension):
        raise ValueError(name+" must have the required square dimensions")
    result = sp.Matrix(rows)
    if result != result.T or result.is_positive_semidefinite is not True:
        raise ValueError(name+" must be exactly symmetric positive semidefinite")
    return result


class TwoModeFilter:
    """Exact innovations; columns track deterministic observation responses."""

    def __init__(self, variance, columns):
        self.variance = rational(variance)
        if self.variance <= 0:
            raise ValueError("variance must be positive")
        self.P = sp.eye(2)*self.variance
        self.mean = sp.zeros(2, integer(columns, "columns", 1))
        self.last = None
        self.h = sp.Matrix([[sp.Rational(3, 5), sp.Rational(4, 5)]])

    def innovation(self, time, row, *, update=True):
        if isinstance(time, bool) or not isinstance(time, int):
            raise ValueError("time must be an integer")
        if self.last is not None:
            gap = time-self.last
            if gap <= 0:
                raise ValueError("filter times must strictly increase")
            a = sp.diag(sp.Rational(2, 5)**gap, sp.Rational(1, 5)**gap)
            self.P = a*self.P*a.T+self.variance*(sp.eye(2)-a*a.T)
            self.mean = a*self.mean
        row = sp.Matrix([tuple(map(rational, row))])
        if row.shape != (1, self.mean.cols):
            raise ValueError("observation response has incorrect dimension")
        covariance = self.P*self.h.T
        variance = self.variance+(self.h*covariance)[0]
        residual = row-self.h*self.mean
        if update:
            self.mean += covariance*residual/variance
            self.P -= covariance*covariance.T/variance
        self.last = time
        return tuple(fraction(x) for x in residual), fraction(variance)


def local_pattern(ages, variance):
    ages = tuple(ages)
    if (any(isinstance(a, bool) or not isinstance(a, int) or a <= 0 for a in ages)
            or ages != tuple(sorted(set(ages), reverse=True))):
        raise ValueError("ages must be distinct positive integers in decreasing order")
    if not ages:
        return (), 2*rational(variance)
    filter_ = TwoModeFilter(variance, len(ages))
    for j, age in enumerate(ages):
        filter_.innovation(-age, tuple(int(i == j) for i in range(len(ages))))
    residual, conditional_variance = filter_.innovation(0, (0,)*len(ages), update=False)
    return tuple(-x for x in residual), conditional_variance


def exact_information(F, prior, selected, variance):
    filter_ = TwoModeFilter(variance, len(F[0]))
    information = sp.Matrix(prior)
    for time in selected:
        residual, innovation_variance = filter_.innovation(time, F[time])
        vector = sp.Matrix(residual)
        information += vector*vector.T/innovation_variance
    return information


def delta_bound(n, L, *, normalized=True, square_root_grid=10**12):
    integer(n, "n", 1)
    integer(L, "L")
    integer(square_root_grid, "square_root_grid", 1)
    if not isinstance(normalized, bool):
        raise ValueError("normalized must be a boolean")
    if L >= n-1:
        return Q(0), Q(0)
    gamma = Q(2, 5)
    coefficient, prefactor = Q(1), Q(2)
    if normalized:
        # Exact ceiling of sqrt(1/2) on the stated rational grid.
        root = isqrt(square_root_grid**2//2)
        if 2*root*root < square_root_grid**2:
            root += 1
        coefficient, prefactor = Q(root, square_root_grid), Q(1)
    near = (gamma**(L+2)*(1-gamma**L)*(1-gamma**(L+1))
            / ((1-gamma)*(1-gamma**2)))
    delta = prefactor*(gamma**(L+1)/(1-gamma)+coefficient*near)
    return delta, coefficient


def certify(record, proposal, *, normalized=True, score_grid=10**8,
            integer_grid=10**12, max_states=2_000_000):
    started = perf_counter()
    for value, name in ((score_grid, "score_grid"), (integer_grid, "integer_grid"),
                        (max_states, "max_states")):
        integer(value, name, 1)
    F = matrix(record["F"])
    n, p = len(F), len(F[0])
    if any(len(row) != p for row in F):
        raise ValueError("F must be rectangular")
    prior = psd_matrix(record["prior"], "prior", p)
    weight = psd_matrix(record["W"], "weight", p)
    k, L = integer(record["k"], "k"), integer(proposal["L"], "L")
    if k > n:
        raise ValueError("cardinality exceeds horizon")
    L = min(L, n-1)
    # Refuse before constructing an unbounded exponential integer or arrays.
    if L > 30 or 1+n*(k+1)*(1 << L) > max_states:
        raise MemoryError("exact count/history state cap exceeded")
    selected = tuple(proposal["selected"])
    if (len(selected) != k or len(set(selected)) != k
            or any(isinstance(t, bool) or not isinstance(t, int) or not 0 <= t < n
                   for t in selected)):
        raise ValueError("proposal is not a cardinality-k subset")
    selected = tuple(sorted(selected))
    variance = rational(record["variance"])
    if variance <= 0:
        raise ValueError("variance must be positive")
    delta, near_coefficient = delta_bound(n, L, normalized=normalized)
    if delta >= 1:
        raise ValueError("window gives no positive relative lower bound")
    H = tuple(tuple(fraction(weight[i, j])/(1-delta) for j in range(p)) for i in range(p))
    scorer = IntegerIntervalScores(F, H, coefficient_grid=integer_grid, score_grid=score_grid)
    patterns, scores = {}, {}

    def arc(time, mask):
        key = time, mask
        if key not in scores:
            if mask not in patterns:
                ages = tuple(a for a in range(L, 0, -1) if mask & (1 << (a-1)))
                coefficients, d = local_pattern(ages, variance)
                patterns[mask] = scorer.prepare(ages, coefficients, d)
            scores[key] = scorer.upper(time, patterns[mask])
        return scores[key]

    trim = (1 << L)-1
    states, visited = {(0, 0): (0, ())}, 1
    for time in range(n):
        following = {}
        for (count, mask), (value, path) in states.items():
            shifted = (mask << 1) & trim
            moves = []
            if count+n-time-1 >= k:
                moves.append(((count, shifted), (value, path)))
            if count < k:
                moves.append(((count+1, shifted | (1 if L else 0)),
                              (value+arc(time, mask), path+(time,))))
            for state, candidate in moves:
                if state not in following or candidate > following[state]:
                    following[state] = candidate
        states = following
        visited += len(states)
    price, priced = max(v for (count, _), v in states.items() if count == k)
    information = exact_information(F, prior, selected, variance)
    lower = fraction(sp.trace(weight*information))
    upper = fraction(sp.trace(weight*prior))+Q(price, score_grid)
    if upper < lower:
        raise ArithmeticError("upper bound below feasible exact value")
    problem = {"F": F, "prior": matrix(record["prior"]), "W": matrix(record["W"]),
               "k": k, "variance": variance, "latent_transition": (Q(2, 5), Q(1, 5)),
               "observation_row": (Q(3, 5), Q(4, 5))}
    return {"status": "certified", "n": n, "p": p, "k": k, "L": L,
            "problem_data": problem, "input_interpretation": "JSON decimals define exact rational data",
            "bound_kind": "normalized partial observation" if normalized else "original partial observation",
            "delta": delta, "near_coefficient_upper": near_coefficient,
            "square_root_grid": 10**12, "selected": selected, "priced_selection": priced,
            "integer_price": price, "score_grid": score_grid,
            "integer_coefficient_grid": integer_grid, "integer_feature_grid": scorer.feature_grid,
            "conditional_patterns": len(patterns), "priced_arcs": len(scores),
            "visited_states": visited, "state_count_bound": 1+n*(k+1)*(1 << L),
            "lower_bound": lower, "upper_bound": upper, "gap": upper-lower,
            "relative_gap": None if lower == 0 else (upper-lower)/lower,
            "display_lower_bound": float(lower), "display_upper_bound": float(upper),
            "display_relative_gap": None if lower == 0 else float((upper-lower)/lower),
            "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "integer_scorer_sha256": hashlib.sha256(Path(__file__).with_name(
                "integer_interval_scores.py").read_bytes()).hexdigest(),
            "wall_seconds": perf_counter()-started}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--case", type=int, default=0)
    parser.add_argument("--dp", type=int, default=-1)
    parser.add_argument("--original-bound", action="store_true")
    args = parser.parse_args()
    record = json.loads(args.input.read_text(), parse_float=str)["results"][args.case]
    result = certify(record, record["dp"][args.dp], normalized=not args.original_bound)
    result.update({"input_file": str(args.input), "input_case_index": args.case,
                   "input_dp_index": args.dp,
                   "input_sha256": hashlib.sha256(args.input.read_bytes()).hexdigest()})
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, default=str, indent=2)+"\n")
    print(json.dumps({key: result[key] for key in
                      ("status", "n", "L", "display_relative_gap", "wall_seconds")}))


if __name__ == "__main__":
    main()
