"""Exact shared-schedule certificates for finite-scenario D-optimal design.

Every scenario is a rational stationary AR(1)-plus-nugget model. Individual
scenario optima are enclosed by recomputing existing exact certificates;
standardized efficiency never treats floating reference optima as exact.
"""

import argparse
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
from time import perf_counter

from certify_noisy_markov import (
    certify as certify_individual, fraction, log_enclosure, matrix, rational,
    require_spd, spectral_bound, true_information,
)
from integer_interval_scores import IntegerIntervalScores


def integer(value, name, minimum=0):
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")
    return value


def outward(value, grid, upper=False):
    scaled = rational(value)*grid
    ticks = (-((-scaled.numerator)//scaled.denominator) if upper
             else scaled.numerator//scaled.denominator)
    return Q(ticks, grid)


def bounded_window(value, n, k, max_states):
    L = min(integer(value, "L"), n-1)
    if L > 30 or 1+n*(k+1)*(1 << L) > max_states:
        raise MemoryError("exact count/history state cap exceeded")
    return L


def scenario_data(record, n, p, k):
    F, prior = matrix(record["F"]), matrix(record["prior"])
    if len(F) != n or any(len(row) != p for row in F) or len(prior) != p:
        raise ValueError("scenarios must have common candidate and parameter dimensions")
    require_spd(prior)
    if integer(record["k"], "scenario k") != k:
        raise ValueError("scenarios must use the common cardinality")
    rho, latent, nugget = map(rational, (
        record["rho"], record["latent_variance"], record["nugget_variance"]))
    if abs(rho) >= 1 or latent < 0 or nugget <= 0:
        raise ValueError("invalid stationary covariance")
    return F, prior, rho, latent, nugget


def certify(record, proposal, *, score_grid=10**8, reference_grid=10**8,
            integer_grid=10**12, log_grid=10**12, max_states=2_000_000):
    started = perf_counter()
    for value, name in ((score_grid, "score_grid"), (reference_grid, "reference_grid"),
                        (integer_grid, "integer_grid"), (log_grid, "log_grid"),
                        (max_states, "max_states")):
        integer(value, name, 1)
    records = record["scenarios"]
    if not isinstance(records, (list, tuple)) or not records:
        raise ValueError("at least one scenario is required")
    first_F = matrix(records[0]["F"])
    n, p, q = len(first_F), len(first_F[0]), len(records)
    k = integer(record["k"], "k")
    if k > n:
        raise ValueError("cardinality exceeds candidate count")
    data = [scenario_data(s, n, p, k) for s in records]
    L = bounded_window(proposal["L"], n, k, max_states)
    selected = tuple(proposal["selected"])
    if (len(selected) != k or len(set(selected)) != k
            or any(isinstance(t, bool) or not isinstance(t, int)
                   or not 0 <= t < n for t in selected)):
        raise ValueError("proposal must be a common cardinality-k subset")
    selected = tuple(sorted(selected))
    references = tuple(item["hull"] for item in record["references"])
    matrices = proposal["hull_information"]
    offsets = tuple(map(rational, record["offsets"]))
    proposed_weights = tuple(map(rational, proposal["dual_weights"]))
    if any(len(x) != q for x in (references, matrices, offsets, proposed_weights)):
        raise ValueError("one reference, center, offset and weight per scenario is required")
    clipped = tuple(max(Q(0), w) for w in proposed_weights)
    total = sum(clipped, Q(0))
    if total == 0:
        raise ValueError("at least one proposed weight must be positive")
    weights = tuple(w/total for w in clipped)

    # Recompute every individual reference; supplied numerical bounds are unused.
    individual = []
    reference_started = perf_counter()
    for s, reference in zip(records, references):
        bounded_window(reference["L"], n, k, max_states)
        individual.append(certify_individual(
            s, reference, score_grid=score_grid,
            reference_grid=reference_grid, max_states=max_states))
    reference_seconds = perf_counter()-reference_started
    ell = tuple(outward(c["lower_bound"], log_grid) for c in individual)
    upper_individual = tuple(outward(c["upper_bound"], log_grid, True) for c in individual)

    scorers, deltas, centers, constants, selected_intervals = [], [], [], [], []
    for (F, prior, rho, latent, nugget), M, w in zip(data, matrices, weights):
        delta = spectral_bound(n, L, rho, latent, nugget)
        if delta >= 1:
            raise ValueError("window gives no positive relative lower bound")
        M = matrix(M)
        if len(M) != p or any(len(row) != p for row in M):
            raise ValueError("tangent source must have the scenario matrix dimensions")
        reference = tuple(tuple(prior[i][j]+(M[i][j]-prior[i][j])/(1-delta)
                                for j in range(p)) for i in range(p))

        def nearest(x):
            value = x*reference_grid+Q(1, 2)
            return Q(value.numerator//value.denominator, reference_grid)

        N = tuple(tuple(nearest((reference[i][j]+reference[j][i])/2)
                        for j in range(p)) for i in range(p))
        exact_N = require_spd(N)
        inv = exact_N.inv()
        inverse = tuple(tuple(fraction(inv[i, j]) for j in range(p)) for i in range(p))
        H = tuple(tuple(w*x/(1-delta) for x in row) for row in inverse)
        scorers.append(IntegerIntervalScores(
            F, H, coefficient_grid=integer_grid, score_grid=score_grid))
        logN_upper = outward(log_enclosure(fraction(exact_N.det()))[1], log_grid, True)
        prior_trace = sum((inverse[i][j]*prior[j][i]
                           for i in range(p) for j in range(p)), Q(0))
        constants.append(w*(logN_upper-p+prior_trace))
        information = true_information(F, prior, selected, rho, latent, nugget)
        low, high = log_enclosure(fraction(require_spd(information).det()))
        selected_intervals.append((outward(low, log_grid), outward(high, log_grid, True)))
        deltas.append(delta)
        centers.append(N)

    patterns, scores = {}, {}

    def arc(time, mask):
        if (time, mask) not in scores:
            if mask not in patterns:
                ages = tuple(a for a in range(L, 0, -1) if mask & (1 << (a-1)))
                patterns[mask] = tuple(scorer.prepare_history(ages, *s[2:])
                                       for scorer, s in zip(scorers, data))
            scores[time, mask] = sum(scorer.upper(time, pattern)
                                    for scorer, pattern in zip(scorers, patterns[mask]))
        return scores[time, mask]

    states, visited = {(0, 0): (0, ())}, 1
    trim = (1 << L)-1
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
    common_upper = sum(constants, Q(0))+Q(price, score_grid)
    fixed_lower = min(interval[0]-c for interval, c in zip(selected_intervals, offsets))
    fixed_upper = common_upper-sum((w*c for w, c in zip(weights, offsets)), Q(0))
    standardized_lower = min(interval[0]-u for interval, u
                             in zip(selected_intervals, upper_individual))
    standardized_upper = min(Q(0), common_upper-sum((w*l for w, l in zip(weights, ell)), Q(0)))

    def bounds(lower, upper):
        lower, upper = outward(lower, log_grid), outward(upper, log_grid, True)
        if upper < lower:
            raise ArithmeticError("certified upper below feasible lower")
        return {"lower_bound": str(lower), "upper_bound": str(upper),
                "gap": str(upper-lower), "display_lower_bound": float(lower),
                "display_upper_bound": float(upper), "display_gap": float(upper-lower)}

    return {
        "status": "certified", "n": n, "p": p, "q": q, "k": k, "L": L,
        "selected": selected, "priced_selection": priced, "integer_price": price,
        "problem_data": [{"F": d[0], "prior": d[1], "rho": d[2],
                          "latent_variance": d[3], "nugget_variance": d[4], "k": k}
                         for d in data],
        "input_interpretation": "JSON decimals are exact rational model and proposal data",
        "offsets": offsets, "proposed_dual_weights": proposed_weights,
        "dual_weights": weights, "weight_rule": "clip negatives to zero and normalize exactly",
        "deltas": deltas, "tangent_references": centers,
        "selected_logdet_intervals": selected_intervals,
        "individual_optimum_lower_bounds": ell,
        "individual_optimum_upper_bounds": upper_individual,
        "individual_certificates": individual,
        "fixed_offset": bounds(fixed_lower, fixed_upper),
        "standardized": bounds(standardized_lower, standardized_upper),
        "standardized_target": "max_P min_s(logdet J_s(P)-max_Q logdet J_s(Q)); D-efficiency uses exp(value/p)",
        "score_grid": score_grid, "reference_grid": reference_grid,
        "integer_grid": integer_grid, "log_grid": log_grid,
        "conditional_patterns": len(patterns), "scored_arcs": len(scores),
        "visited_states": visited, "individual_certificate_seconds": reference_seconds,
        "wall_seconds": perf_counter()-started,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--selection", choices=("robust", "greedy_exchange"), default="robust")
    args = parser.parse_args()
    record = json.loads(args.input.read_text(), parse_float=str)
    proposal = dict(record["robust"])
    proposal["selected"] = record[args.selection]["selected"]
    result = certify(record, proposal)
    result["incumbent_source"] = args.selection
    result["source_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    result["dependency_sha256"] = {
        name: hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
        for name in ("certify_noisy_markov.py", "integer_interval_scores.py")}
    result["input_sha256"] = hashlib.sha256(args.input.read_bytes()).hexdigest()
    args.output.write_text(json.dumps(result, default=str, indent=2)+"\n")
    print(json.dumps({key: result[key] for key in (
        "n", "q", "fixed_offset", "standardized", "wall_seconds")}))


if __name__ == "__main__":
    main()
