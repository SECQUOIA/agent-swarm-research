"""Exact noisy-Markov design certificate with a minimum sampling gap.

The optimizer supplies only an SPD reference candidate and a feasible subset.
Local coefficients, feasible history transitions, integer prices, information
and logarithm bounds are recomputed. JSON decimals define the exact model.
"""

import argparse
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
from time import perf_counter

from certify_noisy_markov import (fraction, local_coefficients, log_enclosure,
                                 matrix, rational, require_spd, true_information)
from noisy_markov_spacing_bound import spacing_bound, spacing_mask_count


def positive_integer(value, name):
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError(name+" must be a positive integer")
    return value


def certify(record, hull, *, score_grid=10**8, reference_grid=10**8,
            max_states=2_000_000, integer_grid=None, refined_pairs=False):
    started = perf_counter()
    for value, name in ((score_grid, "score_grid"),
                        (reference_grid, "reference_grid"), (max_states, "max_states")):
        positive_integer(value, name)
    if integer_grid is not None:
        positive_integer(integer_grid, "integer_grid")
    F, prior = matrix(record["F"]), matrix(record["prior"])
    n, p = len(F), len(prior)
    if any(len(row) != p for row in F):
        raise ValueError("Sensitivity/prior dimensions differ")
    require_spd(prior)
    k, L = record["k"], hull["L"]
    g = positive_integer(record["minimum_gap"], "minimum_gap")
    if (isinstance(k, bool) or not isinstance(k, int) or not 0 <= k <= (n+g-1)//g
            or isinstance(L, bool) or not isinstance(L, int) or L < 0):
        raise ValueError("Invalid cardinality or information window")
    L = min(L, n-1)
    width = max(L, min(g-1, n-1))
    count = spacing_mask_count(width, g)
    state_bound = 1+n*(k+1)*count  # Initial state plus every later time layer.
    if state_bound > max_states:
        raise MemoryError("Exact separated-mask/count state cap exceeded")
    rho, latent, nugget = map(rational, (record["rho"], record["latent_variance"],
                                       record["nugget_variance"]))
    bound = spacing_bound(n, L, g, rho, latent, nugget,
                          refined_pairs=refined_pairs)
    delta = bound["delta"]
    if delta >= 1:
        raise ValueError("Information window gives no positive relative lower bound")
    selected = tuple(hull["selected"])
    if (len(selected) != k or len(set(selected)) != k
            or any(isinstance(t, bool) or not isinstance(t, int) or not 0 <= t < n
                   for t in selected)):
        raise ValueError("Incumbent is not a cardinality-k subset")
    selected = tuple(sorted(selected))
    if any(b-a < g for a, b in zip(selected, selected[1:])):
        raise ValueError("Incumbent violates minimum sampling gap")
    M = matrix(hull["hull_information"])
    if len(M) != p or any(len(row) != p for row in M):
        raise ValueError("Tangent source dimensions differ")
    def nearest(value):
        y = value*reference_grid+Q(1, 2)
        return Q(y.numerator//y.denominator, reference_grid)
    N = tuple(tuple(nearest(prior[i][j]+((M[i][j]+M[j][i])/2-prior[i][j])/(1-delta))
                    for j in range(p)) for i in range(p))
    exact_N = require_spd(N)
    inverse = exact_N.inv()
    inverse = tuple(tuple(fraction(inverse[i, j]) for j in range(p)) for i in range(p))
    H = tuple(tuple(x/(1-delta) for x in row) for row in inverse)
    conditional_cache, scores = {}, {}
    interval_scorer, integer_patterns = None, {}
    if integer_grid is not None:
        from integer_interval_scores import IntegerIntervalScores
        interval_scorer = IntegerIntervalScores(
            F, H, coefficient_grid=integer_grid, score_grid=score_grid)
    information_mask, state_mask = (1 << L)-1, (1 << width)-1
    forbidden = (1 << min(g-1, width))-1

    def arc_score(t, mask):
        recent = mask & information_mask
        key = (t, recent)
        if key not in scores:
            if recent not in conditional_cache:
                ages = tuple(age for age in range(L, 0, -1)
                             if recent & (1 << (age-1)))
                coefficients, variance = local_coefficients(
                    tuple(-age for age in ages), 0, rho, latent, nugget)
                conditional_cache[recent] = ages, coefficients, variance
                if interval_scorer is not None:
                    integer_patterns[recent] = interval_scorer.prepare(ages, coefficients, variance)
            ages, coefficients, variance = conditional_cache[recent]
            if interval_scorer is not None:
                scores[key] = interval_scorer.upper(t, integer_patterns[recent])
                return scores[key]
            adjusted = [F[t][j]-sum((b*F[t-age][j] for age, b in zip(ages, coefficients)), Q(0))
                        for j in range(p)]
            score = sum((H[i][j]*adjusted[i]*adjusted[j]
                         for i in range(p) for j in range(p)), Q(0))/variance
            scaled = score*score_grid
            scores[key] = -((-scaled.numerator)//scaled.denominator)
        return scores[key]

    states = {(0, 0): (0, ())}
    visited = 1
    for t in range(n):
        following = {}
        for (chosen, mask), (score, path) in states.items():
            shifted = (mask << 1) & state_mask
            moves = []
            if chosen+n-t-1 >= k:
                moves.append(((chosen, shifted), (score, path)))
            if chosen < k and not (mask & forbidden):
                moves.append(((chosen+1, shifted | (1 if width else 0)),
                              (score+arc_score(t, mask), path+(t,))))
            for state, candidate in moves:
                if state not in following or candidate > following[state]:
                    following[state] = candidate
        states = following
        visited += len(states)
    maximum, priced = max(value for (chosen, _), value in states.items() if chosen == k)
    prior_trace = sum((inverse[i][j]*prior[j][i] for i in range(p) for j in range(p)), Q(0))
    upper = log_enclosure(fraction(exact_N.det()))[1]-p+prior_trace+Q(maximum, score_grid)
    J = true_information(F, prior, selected, rho, latent, nugget)
    lower = log_enclosure(fraction(require_spd(J).det()))[0]
    if upper < lower:
        raise ArithmeticError("Exact upper bound is below feasible lower bound")
    return {"status": "certified", "n": n, "p": p, "k": k, "L": L,
            "minimum_gap": g, "state_memory_width": width,
            "input_interpretation": "JSON decimal values define exact rational data",
            "problem_data": {"F": F, "prior": prior, "rho": rho,
                             "latent_variance": latent, "nugget_variance": nugget,
                             "k": k, "minimum_gap": g},
            "delta": delta, "spacing_bound_details": bound,
            "pair_majorant": ("fresh-filter refinement" if refined_pairs else
                              "original triangle bound"),
            "tangent_reference": N, "score_grid": score_grid,
            "arc_arithmetic": ("exact rational" if interval_scorer is None else
                               "outward integer intervals"),
            "integer_coefficient_grid": integer_grid,
            "integer_feature_grid": (None if interval_scorer is None else
                                     interval_scorer.feature_grid),
            "integer_scorer_sha256": (None if interval_scorer is None else
                                      hashlib.sha256(Path(__file__).with_name(
                                          "integer_interval_scores.py").read_bytes()).hexdigest()),
            "reference_grid": reference_grid, "integer_price": maximum,
            "priced_selection": priced, "selected": selected,
            "conditional_patterns": len(conditional_cache), "priced_arcs": len(scores),
            "separated_mask_count": count, "state_count_bound": state_bound,
            "visited_states_including_terminal": visited,
            "lower_bound": lower, "upper_bound": upper, "gap": upper-lower,
            "display_lower_bound": float(lower), "display_upper_bound": float(upper),
            "display_gap": float(upper-lower), "wall_seconds": perf_counter()-started}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--case", type=int, default=0)
    parser.add_argument("--hull", type=int, default=-1)
    parser.add_argument("--integer-grid", type=int,
                        help="Use outward integer interval scores on this positive grid")
    parser.add_argument("--refined-pairs", action="store_true",
                        help="Use the reviewed stationary fresh-filter pair bounds")
    args = parser.parse_args()
    record = json.loads(args.input.read_text(), parse_float=str)["results"][args.case]
    result = certify(record, record["hulls"][args.hull], integer_grid=args.integer_grid,
                     refined_pairs=args.refined_pairs)
    result.update({"input_file": str(args.input), "input_case_index": args.case,
                   "input_hull_index": args.hull,
                   "input_sha256": hashlib.sha256(args.input.read_bytes()).hexdigest(),
                   "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()})
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, default=str, indent=2)+"\n")
    print(json.dumps({key: result[key] for key in
                      ("status", "n", "L", "minimum_gap", "display_gap", "wall_seconds")}), flush=True)


if __name__ == "__main__":
    main()
