"""Rational global certificates from arbitrary latent-separator witnesses.

The proposal supplies an SPD reference, a nuisance matrix and a feasible
selection. Exact bridge filtering and integer interval scores recompute a
cardinality-constrained upper price. No covariance truncation is used.
"""

import argparse
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
from time import perf_counter

from certify_noisy_markov import (fraction, log_enclosure, matrix, rational,
                                 require_spd, true_information)
from integer_interval_scores import IntegerIntervalScores


def integer(value, name, lower=1):
    if isinstance(value, bool) or not isinstance(value, int) or value < lower:
        raise ValueError(name + " must be an integer >= " + str(lower))
    return value


def conditional_variance(t, left, right, rho, latent):
    value = latent
    if left is not None:
        value *= 1-rho**(2*(t-left))
    if right is not None:
        value *= 1-rho**(2*(right-t))
    if left is not None and right is not None:
        value /= 1-rho**(2*(right-left))
    return value


def bridge_patterns(length, left, right, rho, latent, nugget, scorer):
    """Prepare every selected-pattern final innovation using a depth-first filter.

    Coordinates are local to the block. Only ancestors' exact filter states
    remain live; the returned prepared intervals are reusable for equal blocks.
    """
    variances = [conditional_variance(t, left, right, rho, latent)
                 for t in range(length)]
    prepared = []

    def visit(history, mask, coefficients, posterior):
        previous = history[-1] if history else None
        for t in range(0 if previous is None else previous+1, length):
            if previous is None:
                prediction, predicted = variances[t], ()
            else:
                a = rho**(t-previous)
                if right is not None:
                    a *= (1-rho**(2*(right-t)))/(1-rho**(2*(right-previous)))
                process_variance = variances[t]-a*a*variances[previous]
                if process_variance < 0:
                    raise ArithmeticError("Negative exact bridge process variance")
                prediction = process_variance+a*a*posterior
                predicted = tuple(a*x for x in coefficients)
            variance = prediction+nugget
            pattern = scorer.prepare(tuple(t-s for s in history), predicted, variance)
            following = mask | (1 << t)
            prepared.append((mask, following, t, pattern))
            gain = prediction/variance
            filtered = tuple((1-gain)*x for x in predicted)+(gain,)
            visit(history+(t,), following, filtered, (1-gain)*prediction)

    visit((), 0, (), latent)
    return prepared


def quadratic(vector, W):
    return sum((W[i][j]*vector[i]*vector[j]
                for i in range(len(W)) for j in range(len(W))), Q(0))


def certify(record, proposal, *, reference_grid=10**8, coefficient_grid=10**12,
            feature_grid=10**18, score_grid=10**8, log_grid=10**12,
            max_patterns=2_000_000):
    started = perf_counter()
    for value, name in ((reference_grid, "reference_grid"),
                        (coefficient_grid, "coefficient_grid"),
                        (feature_grid, "feature_grid"), (score_grid, "score_grid"),
                        (log_grid, "log_grid"), (max_patterns, "max_patterns")):
        integer(value, name)
    F, prior = matrix(record["F"]), matrix(record["prior"])
    n, p = len(F), len(prior)
    if any(len(row) != p for row in F):
        raise ValueError("Sensitivity/prior dimensions differ")
    require_spd(prior)
    k = integer(record["k"], "cardinality", 0)
    if k > n:
        raise ValueError("Cardinality exceeds the candidate count")
    rho, latent, nugget = map(rational, (record["rho"], record["latent_variance"],
                                       record["nugget_variance"]))
    if abs(rho) >= 1 or latent < 0 or nugget <= 0:
        raise ValueError("Require abs(rho)<1, latent>=0 and nugget>0")
    b = min(integer(proposal["block_size"], "block_size"), n)
    # Check the exponent before constructing a potentially enormous integer.
    if b >= max_patterns.bit_length():
        raise MemoryError("Block pattern cap exceeded")
    blocks = tuple(tuple(range(t, min(t+b, n))) for t in range(0, n, b))
    pattern_count = sum(1 << len(times) for times in blocks)
    if pattern_count > max_patterns:
        raise MemoryError("Total block pattern cap exceeded")
    anchors = tuple(times[-1] for times in blocks[:-1]) if latent and rho else ()
    selected = tuple(proposal["selected"])
    if (len(selected) != k or len(set(selected)) != k
            or any(isinstance(t, bool) or not isinstance(t, int) or not 0 <= t < n
                   for t in selected)):
        raise ValueError("Incumbent must be a cardinality-k subset")
    selected = tuple(sorted(selected))
    witness = proposal["best_tangent_witness"]
    source = matrix(witness["schur_information"])
    if len(source) != p or any(len(row) != p for row in source):
        raise ValueError("Reference dimension differs from the target dimension")

    def nearest(value):
        value = value*reference_grid+Q(1, 2)
        return Q(value.numerator//value.denominator, reference_grid)

    N = tuple(tuple(nearest((source[i][j]+source[j][i])/2)
                    for j in range(p)) for i in range(p))
    exact_N = require_spd(N)
    inv = exact_N.inv()
    W = tuple(tuple(fraction(inv[i, j]) for j in range(p)) for i in range(p))
    rows = tuple(tuple(rational(x) for x in row) for row in witness["nuisance_minimizer"])
    if len(rows) != len(anchors) or any(len(row) != p for row in rows):
        raise ValueError("Nuisance witness does not match the recomputed anchors")
    G = tuple(tuple(nearest(x) for x in row) for row in rows)
    adjusted = [list(row) for row in F]
    for index, times in enumerate(blocks):
        left_index = index-1 if anchors and index else None
        right_index = index if anchors and index < len(anchors) else None
        left = anchors[left_index] if left_index is not None else None
        right = anchors[right_index] if right_index is not None else None
        for t in times:
            terms = []
            if left is not None:
                h = rho**(t-left)
                if right is not None:
                    h *= (1-rho**(2*(right-t)))/(1-rho**(2*(right-left)))
                terms.append((left_index, h))
            if right is not None:
                h = rho**(right-t)
                if left is not None:
                    h *= (1-rho**(2*(t-left)))/(1-rho**(2*(right-left)))
                terms.append((right_index, h))
            for j in range(p):
                adjusted[t][j] += sum((h*G[a][j] for a, h in terms), Q(0))
    scorer = IntegerIntervalScores(adjusted, W, feature_grid=feature_grid,
                                   coefficient_grid=coefficient_grid, score_grid=score_grid)
    prior_trace = sum((W[i][j]*prior[j][i] for i in range(p) for j in range(p)), Q(0))
    anchor_trace = Q(0)
    if anchors:
        anchor_trace = quadratic(G[0], W)/latent
        for j in range(1, len(anchors)):
            a = rho**(anchors[j]-anchors[j-1])
            difference = tuple(x-a*y for x, y in zip(G[j], G[j-1]))
            anchor_trace += quadratic(difference, W)/(latent*(1-a*a))
    prepared_cache = {}
    states = {0: (0, ())}
    local_choices, priced_arcs = [], 0
    for index, times in enumerate(blocks):
        origin, length = times[0], len(times)
        left = -1 if anchors and index else None
        right = length-1 if anchors and index < len(anchors) else None
        key = length, left, right
        if key not in prepared_cache:
            prepared_cache[key] = bridge_patterns(length, left, right, rho, latent,
                                                   nugget, scorer)
        scores = [0]*(1 << length)
        best = {0: (0, 0)}
        for previous, mask, t, pattern in prepared_cache[key]:
            score = scores[previous]+scorer.upper(origin+t, pattern)
            scores[mask] = score
            count = mask.bit_count()
            if count <= k and (count not in best or (score, mask) > best[count]):
                best[count] = score, mask
        priced_arcs += len(prepared_cache[key])
        local_choices.append({str(count): {"integer_score": score, "mask": mask}
                              for count, (score, mask) in sorted(best.items())})
        following = {}
        for used, (value, masks) in states.items():
            for count, (score, mask) in best.items():
                if used+count <= k:
                    candidate = value+score, masks+(mask,)
                    if used+count not in following or candidate > following[used+count]:
                        following[used+count] = candidate
        states = following
    maximum, priced_masks = states[k]
    priced_selection = tuple(t for times, mask in zip(blocks, priced_masks)
                             for j, t in enumerate(times) if mask & (1 << j))

    def outward(value, upper):
        value *= log_grid
        rounded = -((-value.numerator)//value.denominator) if upper else value.numerator//value.denominator
        return Q(rounded, log_grid)

    logdet_reference_upper = outward(log_enclosure(fraction(exact_N.det()))[1], True)
    upper = outward(logdet_reference_upper-p+prior_trace+anchor_trace+Q(maximum, score_grid), True)
    J = true_information(F, prior, selected, rho, latent, nugget)
    lower = outward(log_enclosure(fraction(require_spd(J).det()))[0], False)
    if upper < lower:
        raise ArithmeticError("Exact global upper bound lies below the feasible lower bound")
    return {"status": "certified", "n": n, "p": p, "k": k, "block_size": b,
            "input_interpretation": "JSON decimals define exact rational data",
            "problem_data": {"F": F, "prior": prior, "rho": rho,
                             "latent_variance": latent, "nugget_variance": nugget, "k": k},
            "bound_scope": "Original selected-covariance objective; no truncation correction",
            "anchors": anchors, "blocks": blocks, "tangent_reference": N,
            "nuisance_witness": G, "reference_grid": reference_grid,
            "coefficient_grid": coefficient_grid, "feature_grid": feature_grid,
            "score_grid": score_grid, "log_grid": log_grid,
            "logdet_reference_upper": logdet_reference_upper,
            "prior_trace": prior_trace, "anchor_prior_trace": anchor_trace,
            "integer_price": maximum, "local_count_choices": local_choices,
            "priced_block_masks": priced_masks, "priced_selection": priced_selection,
            "selected": selected, "pattern_count": pattern_count, "priced_arcs": priced_arcs,
            "prepared_patterns": sum(len(patterns) for patterns in prepared_cache.values()),
            "lower_bound": lower, "upper_bound": upper, "gap": upper-lower,
            "display_lower_bound": float(lower), "display_upper_bound": float(upper),
            "display_gap": float(upper-lower), "wall_seconds": perf_counter()-started}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--case", type=int, default=-1)
    parser.add_argument("--selected", type=int, nargs="+", help="Optional independently rechecked incumbent")
    args = parser.parse_args()
    record = json.loads(args.input.read_text(), parse_float=str)
    proposal = dict(record["results"][args.case])
    if args.selected is not None:
        proposal["selected"] = args.selected
    result = certify(record["problem_data"], proposal)
    result.update(input_file=str(args.input), input_case_index=args.case,
                  input_sha256=hashlib.sha256(args.input.read_bytes()).hexdigest(),
                  source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  dependency_sha256={name: hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
                                     for name in ("certify_noisy_markov.py", "integer_interval_scores.py")})
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, default=str, indent=2)+"\n")
    print(json.dumps({key: result[key] for key in
                      ("status", "n", "block_size", "display_gap", "wall_seconds")}))


if __name__ == "__main__":
    main()
